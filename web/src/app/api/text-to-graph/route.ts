import { NextResponse } from "next/server";
import { query } from "@/lib/db";
import { sanitizeGraphData, type GraphData } from "@/lib/graph-data";
import { generateWithOllama } from "@/lib/ollama";
import {
  buildTextToGraphPrompt,
  getNodePosition,
  parseDraftGraph,
  type DraftGraph,
} from "@/lib/text-to-graph";

type CreateDiagramRow = { id: number };
type CreateNodeRow = { id: number; label: string; x: number; y: number };
type CreateEdgeRow = {
  id: number;
  source_node_id: number;
  target_node_id: number;
  label: string | null;
};

function getRequestText(payload: unknown): string {
  if (!payload || typeof payload !== "object") {
    return "";
  }

  const candidate = (payload as { text?: unknown }).text;
  if (typeof candidate !== "string") {
    return "";
  }

  return candidate.trim();
}

async function persistDraftGraph(draft: DraftGraph): Promise<GraphData> {
  const diagramRows = await query<CreateDiagramRow>(
    "INSERT INTO diagrams (title) VALUES ($1) RETURNING id",
    [draft.diagramTitle]
  );

  const diagramId = diagramRows[0].id;
  const nodeIdByKey = new Map<string, number>();
  const nodes: CreateNodeRow[] = [];

  for (let index = 0; index < draft.nodes.length; index += 1) {
    const node = draft.nodes[index];
    const position = getNodePosition(index);

    const rows = await query<CreateNodeRow>(
      "INSERT INTO nodes (diagram_id, label, x, y) VALUES ($1, $2, $3, $4) RETURNING id, label, x, y",
      [diagramId, node.label, position.x, position.y]
    );

    const created = rows[0];
    nodeIdByKey.set(node.key, created.id);
    nodes.push(created);
  }

  const edges: CreateEdgeRow[] = [];

  for (const edge of draft.edges) {
    const sourceNodeId = nodeIdByKey.get(edge.sourceKey);
    const targetNodeId = nodeIdByKey.get(edge.targetKey);

    if (!sourceNodeId || !targetNodeId || sourceNodeId === targetNodeId) {
      continue;
    }

    const rows = await query<CreateEdgeRow>(
      "INSERT INTO edges (diagram_id, source_node_id, target_node_id, label) VALUES ($1, $2, $3, $4) RETURNING id, source_node_id, target_node_id, label",
      [diagramId, sourceNodeId, targetNodeId, edge.label]
    );

    edges.push(rows[0]);
  }

  return sanitizeGraphData({
    diagramTitle: draft.diagramTitle,
    nodes: nodes.map((node) => ({
      id: node.id,
      label: node.label,
      x: node.x,
      y: node.y,
    })),
    edges: edges.map((edge) => ({
      id: edge.id,
      sourceNodeId: edge.source_node_id,
      targetNodeId: edge.target_node_id,
      label: edge.label,
    })),
  });
}

export async function POST(request: Request) {
  try {
    const payload = (await request.json().catch(() => ({}))) as unknown;
    const text = getRequestText(payload);
    const maxChars = Number(process.env.TEXT_TO_GRAPH_MAX_CHARS ?? "5000");

    if (text.length < 10) {
      return NextResponse.json(
        { error: "Le texte doit contenir au moins 10 caracteres." },
        { status: 400 }
      );
    }

    if (text.length > maxChars) {
      return NextResponse.json(
        { error: `Le texte depasse la limite (${maxChars} caracteres).` },
        { status: 400 }
      );
    }

    const prompt = buildTextToGraphPrompt(text);
    const rawJson = await generateWithOllama(prompt);
    const draft = parseDraftGraph(rawJson);
    const graph = await persistDraftGraph(draft);

    return NextResponse.json<GraphData>(graph);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Erreur inconnue";
    return NextResponse.json(
      { error: `Impossible de generer le schema: ${message}` },
      { status: 500 }
    );
  }
}
