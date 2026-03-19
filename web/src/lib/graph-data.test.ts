import assert from "node:assert/strict";
import test from "node:test";
import { clampZoom, sanitizeGraphData } from "@/lib/graph-data";

test("clampZoom applique les bornes min/max", () => {
  assert.equal(clampZoom(0.1), 0.4);
  assert.equal(clampZoom(0.8), 0.8);
  assert.equal(clampZoom(3), 2);
});

test("sanitizeGraphData supprime les liens vers des nœuds absents", () => {
  const sanitized = sanitizeGraphData({
    diagramTitle: "Test",
    nodes: [
      { id: 1, label: "A", x: 0, y: 0 },
      { id: 2, label: "B", x: 100, y: 100 },
    ],
    edges: [
      { id: 10, sourceNodeId: 1, targetNodeId: 2, label: null },
      { id: 11, sourceNodeId: 1, targetNodeId: 999, label: null },
    ],
  });

  assert.equal(sanitized.edges.length, 1);
  assert.equal(sanitized.edges[0].id, 10);
});
