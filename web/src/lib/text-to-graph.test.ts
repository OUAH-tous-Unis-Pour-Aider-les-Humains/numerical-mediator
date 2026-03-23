import assert from "node:assert/strict";
import test from "node:test";
import { parseDraftGraph } from "@/lib/text-to-graph";

test("parseDraftGraph dedupe les noeuds et limite le volume", () => {
  const nodes = Array.from({ length: 20 }, (_, index) => ({
    key: `n${index % 6}`,
    label: `Noeud ${index}`,
  }));

  const raw = JSON.stringify({
    diagramTitle: "Test",
    nodes,
    edges: [
      { sourceKey: "n0", targetKey: "n1", label: "a" },
      { sourceKey: "n0", targetKey: "n1", label: "a" },
      { sourceKey: "n1", targetKey: "n2", label: "b" },
    ],
  });

  const graph = parseDraftGraph(raw);

  assert.equal(graph.nodes.length, 6);
  assert.equal(graph.edges.length, 2);
});

test("parseDraftGraph rejette une reponse sans lien exploitable", () => {
  const raw = JSON.stringify({
    diagramTitle: "Sans lien",
    nodes: [
      { key: "n1", label: "Alpha" },
      { key: "n2", label: "Beta" },
    ],
    edges: [{ sourceKey: "n1", targetKey: "n999", label: "invalide" }],
  });

  assert.throws(
    () => parseDraftGraph(raw),
    /aucun lien exploitable/
  );
});

test("parseDraftGraph rejette le JSON invalide", () => {
  assert.throws(
    () => parseDraftGraph("{not-json}"),
    /JSON valide/
  );
});
