"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { GraphCanvas } from "@/components/graph-canvas";
import type { GraphData } from "@/lib/graph-data";
import styles from "@/app/page.module.css";

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; graph: GraphData };

export function GraphLoader() {
  const [state, setState] = useState<LoadState>({ status: "loading" });
  const [prompt, setPrompt] = useState(
    "Alice défend la rapidité, Bob défend la robustesse. Trouver une solution commune."
  );
  const [model, setModel] = useState("qwen2.5:7b");
  const [customModel, setCustomModel] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generationError, setGenerationError] = useState<string | null>(null);

  const effectiveModel =
    model === "custom" ? customModel.trim() : model;

  const loadGraph = useCallback(async () => {
    setState({ status: "loading" });

    try {
      const response = await fetch("/api/graph");

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const graph = (await response.json()) as GraphData;
      setState({ status: "ready", graph });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Erreur inconnue";
      setState({ status: "error", message });
    }
  }, []);

  useEffect(() => {
    loadGraph().catch(() => {
      return;
    });
  }, [loadGraph]);

  async function handleGenerate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setGenerating(true);
    setGenerationError(null);

    try {
      const response = await fetch("/api/text-to-graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: prompt, model: effectiveModel }),
      });

      if (!response.ok) {
        const payload = (await response.json().catch(() => null)) as
          | { error?: string }
          | null;
        throw new Error(payload?.error ?? `HTTP ${response.status}`);
      }

      await loadGraph();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Erreur inconnue";
      setGenerationError(message);
    } finally {
      setGenerating(false);
    }
  }

  return (
    <section className={styles.loaderSection}>
      <form className={styles.aiPanel} onSubmit={handleGenerate}>
        <label className={styles.aiLabel} htmlFor="schema-prompt">
          Générer un schéma avec Ollama
        </label>
        <select
          className={styles.aiSelect}
          value={model}
          onChange={(event) => setModel(event.target.value)}
          aria-label="Modele Ollama"
        >
          <option value="qwen2.5:7b">qwen2.5:7b</option>
          <option value="llama3.1:8b">llama3.1:8b</option>
          <option value="mistral:7b">mistral:7b</option>
          <option value="custom">Autre modele...</option>
        </select>
        {model === "custom" ? (
          <input
            className={styles.aiCustomModel}
            value={customModel}
            onChange={(event) => setCustomModel(event.target.value)}
            placeholder="ex: llama3:latest"
            aria-label="Nom du modele Ollama personnalise"
          />
        ) : null}
        <textarea
          className={styles.aiInput}
          id="schema-prompt"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          rows={4}
          placeholder="Décris le désaccord et la solution à construire..."
          maxLength={5000}
        />
        <div className={styles.aiActions}>
          <button
            disabled={
              generating ||
              prompt.trim().length < 10 ||
              (model === "custom" && effectiveModel.length < 2)
            }
            type="submit"
          >
            {generating ? "Génération en cours..." : "Générer le schéma"}
          </button>
          <button onClick={() => loadGraph()} type="button">
            Recharger depuis la base
          </button>
        </div>
        {generationError ? <p className={styles.errorText}>{generationError}</p> : null}
      </form>

      {state.status === "loading" ? <p>Chargement du schéma…</p> : null}
      {state.status === "error" ? <p>Erreur de chargement : {state.message}</p> : null}
      {state.status === "ready" ? <GraphCanvas graph={state.graph} /> : null}
    </section>
  );
}
