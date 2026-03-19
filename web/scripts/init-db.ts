import { readFile } from "node:fs/promises";
import { query } from "../src/lib/db";

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
  const schemaSql = await readFile(new URL("../db/schema.sql", import.meta.url), "utf8");
  await query(schemaSql);
  console.log("✅ Schéma PostgreSQL initialisé.");
}

main().catch((error) => {
  console.error("❌ Impossible d'initialiser la base:", error);
  process.exit(1);
});
