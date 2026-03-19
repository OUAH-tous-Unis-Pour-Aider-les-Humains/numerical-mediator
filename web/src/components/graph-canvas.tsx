"use client";

import { useMemo, useState } from "react";
import { clampZoom, type GraphData } from "@/lib/graph-data";
import styles from "@/app/page.module.css";

type GraphCanvasProps = {
  graph: GraphData;
};

type DragState = {
  active: boolean;
  startX: number;
  startY: number;
};

export function GraphCanvas({ graph }: GraphCanvasProps) {
  const [zoom, setZoom] = useState(1);
  const [offsetX, setOffsetX] = useState(120);
  const [offsetY, setOffsetY] = useState(80);
  const [drag, setDrag] = useState<DragState>({
    active: false,
    startX: 0,
    startY: 0,
  });

  const nodesById = useMemo(
    () => new Map(graph.nodes.map((node) => [node.id, node])),
    [graph.nodes]
  );

  function changeZoom(delta: number) {
    setZoom((current) => clampZoom(Number((current + delta).toFixed(2))));
  }

  return (
    <section className={styles.schemaSection}>
      <header className={styles.schemaHeader}>
        <div>
          <h1>{graph.diagramTitle}</h1>
          <p>{graph.nodes.length} nœuds · {graph.edges.length} liens</p>
        </div>
        <div className={styles.toolbar}>
          <button onClick={() => changeZoom(-0.1)} type="button">
            -
          </button>
          <span>{Math.round(zoom * 100)}%</span>
          <button onClick={() => changeZoom(0.1)} type="button">
            +
          </button>
          <button
            onClick={() => {
              setZoom(1);
              setOffsetX(120);
              setOffsetY(80);
            }}
            type="button"
          >
            Réinitialiser
          </button>
        </div>
      </header>

      <div
        className={styles.viewport}
        onMouseDown={(event) => {
          if (event.button !== 0) {
            return;
          }

          setDrag({
            active: true,
            startX: event.clientX - offsetX,
            startY: event.clientY - offsetY,
          });
        }}
        onMouseLeave={() => setDrag({ active: false, startX: 0, startY: 0 })}
        onMouseMove={(event) => {
          if (!drag.active) {
            return;
          }

          setOffsetX(event.clientX - drag.startX);
          setOffsetY(event.clientY - drag.startY);
        }}
        onMouseUp={() => setDrag({ active: false, startX: 0, startY: 0 })}
        onWheel={(event) => {
          event.preventDefault();
          changeZoom(event.deltaY < 0 ? 0.05 : -0.05);
        }}
      >
        <div
          className={styles.canvas}
          style={{ transform: `translate(${offsetX}px, ${offsetY}px) scale(${zoom})` }}
        >
          <svg className={styles.edges}>
            {graph.edges.map((edge) => {
              const source = nodesById.get(edge.sourceNodeId);
              const target = nodesById.get(edge.targetNodeId);

              if (!source || !target) {
                return null;
              }

              return (
                <line
                  key={edge.id}
                  x1={source.x + 70}
                  y1={source.y + 24}
                  x2={target.x + 70}
                  y2={target.y + 24}
                  stroke="#94a3b8"
                  strokeWidth="2"
                />
              );
            })}
          </svg>

          {graph.nodes.map((node) => (
            <article
              className={styles.node}
              key={node.id}
              style={{ left: node.x, top: node.y }}
            >
              <strong>{node.label}</strong>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
