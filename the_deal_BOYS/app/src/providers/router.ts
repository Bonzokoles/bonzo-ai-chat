// 9router — OpenAI-compatible gateway na 127.0.0.1:20128.
// Zwraca LanguageModelV1 z Vercel AI SDK, opakowywany przez VercelAIProvider w VoltAgent.
//
// BUG W 9ROUTER (obejście):
// 9router dokleja `}data: [DONE]\n` do KAŻDEGO response (stream i non-stream), bez separatora.
// W stream mode wysyła dodatkowo podwójny `data: [DONE]` na końcu.
// Vercel AI SDK próbuje sparsować całość jako JSON i rzuca "Invalid JSON response".
// Obejście: patchujemy globalThis.fetch żeby stripował trailing `data: [DONE]` i podwójne DONE.
import { createOpenAICompatible } from "@ai-sdk/openai-compatible";

const BASE_URL = process.env.ROUTER_BASE_URL ?? "http://127.0.0.1:20128/v1";
const API_KEY = process.env.ROUTER_API_KEY ?? "no-key-needed";

if (!("__patchedFor9router" in globalThis)) {
	(globalThis as { __patchedFor9router?: boolean }).__patchedFor9router = true;
	const origFetch = globalThis.fetch.bind(globalThis);
	globalThis.fetch = (async (input: string | URL, init?: RequestInit) => {
		const res = await origFetch(input, init);
		const url = typeof input === "string" ? input : input.toString();
		if (!url.includes("127.0.0.1:20128") && !url.includes("localhost:20128")) {
			return res;
		}
		const ct = res.headers.get("content-type") ?? "";
		if (!ct.includes("text/event-stream") && !ct.includes("application/json")) {
			return res;
		}
		const body = await res.text();
		// Strip trailing `}data: [DONE]` (doklejony do JSON-a bez separatora)
		// oraz podwójne `data: [DONE]\ndata: [DONE]` na końcu streamów.
		let cleaned = body
			.replace(/}data:\s*\[DONE\]\s*$/s, "}")
			.replace(/data:\s*\[DONE\]\s*\ndata:\s*\[DONE\]\s*$/s, "data: [DONE]");
		// Nowy Response z zachowaniem statusu i nagłówków.
		return new Response(cleaned, {
			status: res.status,
			statusText: res.statusText,
			headers: res.headers,
		});
	}) as typeof globalThis.fetch;
}

export const router = createOpenAICompatible({
	name: "9router",
	baseURL: BASE_URL,
	apiKey: API_KEY,
});

export const ROUTER_INFO = {
	baseURL: BASE_URL,
	defaultBuchModel: process.env.BUCH_MODEL ?? "buch-chat",
	defaultOrchestratorModel: process.env.ORCHESTRATOR_MODEL ?? "buch-agents",
	defaultWorkerModel: process.env.WORKER_MODEL ?? "buch-agents",
};
