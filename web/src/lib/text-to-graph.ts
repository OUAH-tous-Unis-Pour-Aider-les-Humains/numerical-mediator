export type DraftNode = {
  key: string;
  label: string;
};

export type DraftEdge = {
  sourceKey: string;
  targetKey: string;
  label: string | null;
};

export type DraftGraph = {
  diagramTitle: string;
  nodes: DraftNode[];
  edges: DraftEdge[];
};

type RawNode = {
  key?: unknown;
  label?: unknown;
};

type RawEdge = {
  sourceKey?: unknown;
  targetKey?: unknown;
  label?: unknown;
};

type RawGraph = {
  diagramTitle?: unknown;
  nodes?: unknown;
  edges?: unknown;
};

const NODE_LIMIT = 12;
const EDGE_LIMIT = 32;
const KEY_PATTERN = /^[a-zA-Z0-9_-]{1,32}$/;

function normalizeNodeKey(value: unknown, fallback: string): string {
  if (typeof value !== "string") {
    return fallback;
  }

  const key = value.trim();
  return KEY_PATTERN.test(key) ? key : fallback;
}

function normalizeLabel(value: unknown, maxLength: number): string {
  if (typeof value !== "string") {
    return "";
  }

  return value.replace(/\s+/g, " ").trim().slice(0, maxLength);
}

export function buildTextToGraphPrompt(text: string): string {
  return [
    "Tu es un assistant de mediation.",
    "Transforme le texte en graphe structure.",
    "Tu dois repondre UNIQUEMENT en JSON valide.",
    "Format strict:",
    "{",
    '  "diagramTitle": "string",',
    '  "nodes": [{ "key": "n1", "label": "string" }],',
    '  "edges": [{ "sourceKey": "n1", "targetKey": "n2", "label": "string ou null" }]',
    "}",
    "Contraintes:",
    "- 2 a 12 nodes",
    "- labels courts et clairs",
    "- pas de markdown",
    "- pas de texte hors JSON",
    "Texte source:",
    text,
  ].join("\n");
}

export function parseDraftGraph(rawJson: string): DraftGraph {
  let parsed: RawGraph;
  try {
    parsed = JSON.parse(rawJson) as RawGraph;
  } catch {
    throw new Error("La reponse IA n'est pas un JSON valide");
  }

  if (!parsed || typeof parsed !== "object") {
    throw new Error("La reponse IA doit etre un objet JSON");
  }

  const diagramTitle =
    typeof parsed.diagramTitle === "string" && parsed.diagramTitle.trim().length > 0
      ? parsed.diagramTitle.trim().slice(0, 120)
      : "Schema genere par IA";

  const rawNodes = Array.isArray(parsed.nodes) ? (parsed.nodes as RawNode[]) : [];
  const seenNodeKeys = new Set<string>();
  const nodes: DraftNode[] = [];

  for (let index = 0; index < rawNodes.length; index += 1) {
    if (nodes.length >= NODE_LIMIT) {
      break;
    }

    const rawNode = rawNodes[index];
    const key = normalizeNodeKey(rawNode.key, `n${index + 1}`);
    const label = normalizeLabel(rawNode.label, 80);

    if (label.length < 2 || seenNodeKeys.has(key)) {
      continue;
    }

    nodes.push({ key, label });
    seenNodeKeys.add(key);
  }

  if (nodes.length < 2) {
    throw new Error("La reponse IA contient trop peu de noeuds exploitables");
  }

  const allowedKeys = new Set(nodes.map((node) => node.key));
  const rawEdges = Array.isArray(parsed.edges) ? (parsed.edges as RawEdge[]) : [];

  const seenEdges = new Set<string>();
  const edges: DraftEdge[] = [];

  for (const rawEdge of rawEdges) {
    if (edges.length >= EDGE_LIMIT) {
      break;
    }

    const sourceKey = normalizeNodeKey(rawEdge.sourceKey, "");
    const targetKey = normalizeNodeKey(rawEdge.targetKey, "");
    const label = normalizeLabel(rawEdge.label, 80);

    if (
      sourceKey.length === 0 ||
      targetKey.length === 0 ||
      sourceKey === targetKey ||
      !allowedKeys.has(sourceKey) ||
      !allowedKeys.has(targetKey)
    ) {
      continue;
    }

    const edgeSignature = `${sourceKey}->${targetKey}:${label}`;
    if (seenEdges.has(edgeSignature)) {
      continue;
    }

    edges.push({
      sourceKey,
      targetKey,
      label: label.length > 0 ? label : null,
    });
    seenEdges.add(edgeSignature);
  }

  if (edges.length === 0) {
    throw new Error("La reponse IA ne contient aucun lien exploitable");
  }

  return { diagramTitle, nodes, edges };
}

export function getNodePosition(index: number) {
  const perRow = 4;
  const xGap = 260;
  const yGap = 150;
  const x = 60 + (index % perRow) * xGap;
  const y = 40 + Math.floor(index / perRow) * yGap;
  return { x, y };
}
