"use client";

import { useEffect, useState } from "react";
import { GraphCanvas } from "@/components/graph-canvas";
import type { GraphData } from "@/lib/graph-data";

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; graph: GraphData };

export function GraphLoader() {
  const [state, setState] = useState<LoadState>({ status: "loading" });

  useEffect(() => {
    let mounted = true;

    async function load() {
      try {
        const response = await fetch("/api/graph");

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const graph = (await response.json()) as GraphData;

        if (mounted) {
          setState({ status: "ready", graph });
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : "Erreur inconnue";

        if (mounted) {
          setState({ status: "error", message });
        }
      }
    }

    load();

    return () => {
      mounted = false;
    };
  }, []);

  if (state.status === "loading") {
    return <p>Chargement du schéma…</p>;
  }

  if (state.status === "error") {
    return <p>Erreur de chargement : {state.message}</p>;
  }

  return <GraphCanvas graph={state.graph} />;
}
