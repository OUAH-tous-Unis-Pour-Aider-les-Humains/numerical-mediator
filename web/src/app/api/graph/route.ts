import { NextResponse } from "next/server";
import { query } from "@/lib/db";
import { sanitizeGraphData, type GraphData } from "@/lib/graph-data";

type DiagramRow = { id: number; title: string };
type NodeRow = { id: number; label: string; x: number; y: number };
type EdgeRow = {
  id: number;
  source_node_id: number;
  target_node_id: number;
  label: string | null;
};

export async function GET() {
  try {
    const diagrams = await query<DiagramRow>(
      "SELECT id, title FROM diagrams ORDER BY created_at DESC LIMIT 1"
    );

    if (diagrams.length === 0) {
      return NextResponse.json<GraphData>({
        diagramTitle: "Aucun schéma disponible",
        nodes: [],
        edges: [],
      });
    }

    const diagramId = diagrams[0].id;

    const [nodes, edges] = await Promise.all([
      query<NodeRow>(
        "SELECT id, label, x, y FROM nodes WHERE diagram_id = $1 ORDER BY id",
        [diagramId]
      ),
      query<EdgeRow>(
        "SELECT id, source_node_id, target_node_id, label FROM edges WHERE diagram_id = $1 ORDER BY id",
        [diagramId]
      ),
    ]);

    const graph = sanitizeGraphData({
      diagramTitle: diagrams[0].title,
      nodes,
      edges: edges.map((edge) => ({
        id: edge.id,
        sourceNodeId: edge.source_node_id,
        targetNodeId: edge.target_node_id,
        label: edge.label,
      })),
    });

    return NextResponse.json<GraphData>(graph);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Erreur inconnue";
    return NextResponse.json(
      { error: `Impossible de charger le schéma: ${message}` },
      { status: 500 }
    );
  }
}
