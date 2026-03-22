"use client";

import { useMemo } from "react";
import {
  Background,
  Controls,
  MarkerType,
  ReactFlow,
  type Edge,
  type Node,
} from "reactflow";
import "reactflow/dist/style.css";
import type { GraphData } from "@/lib/graph-data";
import styles from "@/app/page.module.css";

type GraphCanvasProps = {
  graph: GraphData;
};

export function GraphCanvas({ graph }: GraphCanvasProps) {
  const nodes = useMemo<Node[]>(
    () =>
      graph.nodes.map((node) => ({
        id: String(node.id),
        position: { x: node.x, y: node.y },
        data: { label: node.label },
        style: {
          border: "1px solid #94a3b8",
          borderRadius: 10,
          padding: 8,
          width: 180,
          background: "#f8fafc",
          color: "#0f172a",
          textAlign: "center",
          fontWeight: 600,
        },
      })),
    [graph.nodes]
  );

  const edges = useMemo<Edge[]>(
    () =>
      graph.edges.map((edge) => ({
        id: String(edge.id),
        source: String(edge.sourceNodeId),
        target: String(edge.targetNodeId),
        label: edge.label ?? undefined,
        markerEnd: { type: MarkerType.ArrowClosed, color: "#64748b" },
        style: { stroke: "#94a3b8", strokeWidth: 2 },
        labelStyle: { fill: "#334155", fontSize: 12 },
      })),
    [graph.edges]
  );

  return (
    <section className={styles.schemaSection}>
      <header className={styles.schemaHeader}>
        <div>
          <h1>{graph.diagramTitle}</h1>
          <p>{graph.nodes.length} nœuds · {graph.edges.length} liens</p>
        </div>
        <p className={styles.helpText}>Zoom: molette | Déplacement: clic + glisser</p>
      </header>

      <div className={styles.viewport}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          minZoom={0.3}
          maxZoom={2}
          proOptions={{ hideAttribution: true }}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          className={styles.reactFlow}
        >
          <Background color="#e2e8f0" gap={24} size={1} />
          <Controls showInteractive={false} />
        </ReactFlow>
      </div>
    </section>
  );
}
