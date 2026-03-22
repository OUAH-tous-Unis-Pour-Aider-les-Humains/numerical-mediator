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

  const diagramTitle =
    typeof parsed.diagramTitle === "string" && parsed.diagramTitle.trim().length > 0
      ? parsed.diagramTitle.trim().slice(0, 120)
      : "Schema genere par IA";

  const rawNodes = Array.isArray(parsed.nodes) ? (parsed.nodes as RawNode[]) : [];
  const nodes: DraftNode[] = rawNodes
    .map((node, index) => {
      const key = typeof node.key === "string" ? node.key.trim() : `n${index + 1}`;
      const label = typeof node.label === "string" ? node.label.trim() : "";
      return { key, label };
    })
    .filter((node) => node.key.length > 0 && node.label.length > 0)
    .slice(0, 24);

  if (nodes.length < 2) {
    throw new Error("La reponse IA contient trop peu de noeuds exploitables");
  }

  const allowedKeys = new Set(nodes.map((node) => node.key));
  const rawEdges = Array.isArray(parsed.edges) ? (parsed.edges as RawEdge[]) : [];

  const edges: DraftEdge[] = rawEdges
    .map((edge) => {
      const sourceKey = typeof edge.sourceKey === "string" ? edge.sourceKey.trim() : "";
      const targetKey = typeof edge.targetKey === "string" ? edge.targetKey.trim() : "";
      const label = typeof edge.label === "string" ? edge.label.trim().slice(0, 80) : null;

      return {
        sourceKey,
        targetKey,
        label: label && label.length > 0 ? label : null,
      };
    })
    .filter(
      (edge) =>
        edge.sourceKey.length > 0 &&
        edge.targetKey.length > 0 &&
        edge.sourceKey !== edge.targetKey &&
        allowedKeys.has(edge.sourceKey) &&
        allowedKeys.has(edge.targetKey)
    )
    .slice(0, 64);

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
