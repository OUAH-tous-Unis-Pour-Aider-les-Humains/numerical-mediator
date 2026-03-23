type OllamaGenerateResponse = {
  response?: string;
};

const MODEL_PATTERN = /^[a-zA-Z0-9_.:-]{2,80}$/;

function getRequiredEnv(name: string, fallback?: string): string {
  const value = process.env[name] ?? fallback;
  if (!value) {
    throw new Error(`${name} doit être défini`);
  }
  return value;
}

function withTimeout(timeoutMs: number): AbortSignal {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), timeoutMs);
  return controller.signal;
}

function resolveModelName(modelOverride?: string): string {
  const modelFromEnv = getRequiredEnv("OLLAMA_MODEL", "qwen2.5:7b");
  const candidate = (modelOverride ?? modelFromEnv).trim();

  if (!MODEL_PATTERN.test(candidate)) {
    throw new Error("Nom de modele Ollama invalide");
  }

  return candidate;
}

export async function generateWithOllama(
  prompt: string,
  modelOverride?: string
): Promise<string> {
  const baseUrl = getRequiredEnv("OLLAMA_BASE_URL", "http://localhost:11434");
  const model = resolveModelName(modelOverride);
  const timeoutMs = Number(process.env.OLLAMA_TIMEOUT_MS ?? "120000");

  const response = await fetch(`${baseUrl}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    signal: withTimeout(timeoutMs),
    body: JSON.stringify({
      model,
      prompt,
      stream: false,
      format: "json",
      options: {
        temperature: 0.2,
      },
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      `Ollama indisponible (${response.status}): ${body.slice(0, 200)}`
    );
  }

  const payload = (await response.json()) as OllamaGenerateResponse;
  if (!payload.response) {
    throw new Error("Réponse Ollama invalide: champ response absent");
  }

  return payload.response;
}
