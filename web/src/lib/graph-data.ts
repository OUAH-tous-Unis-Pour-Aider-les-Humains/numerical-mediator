export type GraphNode = {
  id: number;
  label: string;
  x: number;
  y: number;
};

export type GraphEdge = {
  id: number;
  sourceNodeId: number;
  targetNodeId: number;
  label: string | null;
};

export type GraphData = {
  diagramTitle: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export function sanitizeGraphData(data: GraphData): GraphData {
  const knownNodeIds = new Set(data.nodes.map((node) => node.id));

  return {
    ...data,
    edges: data.edges.filter(
      (edge) =>
        knownNodeIds.has(edge.sourceNodeId) && knownNodeIds.has(edge.targetNodeId)
    ),
  };
}

export function clampZoom(zoom: number): number {
  return Math.min(2, Math.max(0.4, zoom));
}
