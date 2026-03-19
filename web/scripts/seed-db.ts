import { readFile } from "node:fs/promises";
import { query } from "../src/lib/db";

type DiagramRow = { id: number };
type NodeRow = { id: number };

async function loadLocalEnv() {
  if (process.env.DATABASE_URL) {
    return;
  }

  const envContent = await readFile(
    new URL("../.env.local", import.meta.url),
    "utf8"
  );

  for (const line of envContent.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    const [key, ...rest] = trimmed.split("=");
    process.env[key] = rest.join("=");
  }
}

async function main() {
  await loadLocalEnv();
  await query("DELETE FROM diagrams");

  const diagramRows = await query<DiagramRow>(
    "INSERT INTO diagrams (title) VALUES ($1) RETURNING id",
    ["Exemple - Médiation numérique"]
  );

  const diagramId = diagramRows[0].id;

  const labels = [
    ["Problème", 40, 40],
    ["Argument A", 280, 30],
    ["Argument B", 280, 150],
    ["Solution commune", 520, 90],
  ] as const;

  const nodeIds: number[] = [];

  for (const [label, x, y] of labels) {
    const rows = await query<NodeRow>(
      "INSERT INTO nodes (diagram_id, label, x, y) VALUES ($1, $2, $3, $4) RETURNING id",
      [diagramId, label, x, y]
    );

    nodeIds.push(rows[0].id);
  }

  await query(
    "INSERT INTO edges (diagram_id, source_node_id, target_node_id, label) VALUES ($1, $2, $3, $4), ($1, $5, $6, $7), ($1, $8, $9, $10)",
    [
      diagramId,
      nodeIds[0],
      nodeIds[1],
      "exprime",
      nodeIds[0],
      nodeIds[2],
      "exprime",
      nodeIds[1],
      nodeIds[3],
      "converge",
    ]
  );

  console.log("✅ Données factices insérées.");
}

main().catch((error) => {
  console.error("❌ Impossible d'insérer les données:", error);
  process.exit(1);
});
