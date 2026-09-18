// Wspólny tool RAG dla wszystkich 5 Polaczków.
// Każdy worker dostaje tool, który czyta TYLKO chunki z jego target_workers.
// Cache per-process — chunki wczytywane raz.
import { z } from "zod";
import { createTool } from "@voltagent/core";
import { loadChunks, chunksForWorker, criticalChunks, type RagChunk } from "../rag/loader.js";

let cached: RagChunk[] | null = null;

function getChunks(): RagChunk[] {
	if (!cached) {
		const ragRoot = process.env.RAG_ROOT ?? "../rag";
		cached = loadChunks(ragRoot);
	}
	return cached;
}

export function createRagTool(workerName: string, scope: "worker" | "all" = "worker") {
	const toolName = scope === "all" ? "ask_rag_full" : "ask_rag";
	return createTool({
		name: toolName,
		description:
			scope === "all"
				? "Wyszukuje chunki RAG w CAŁEJ kolekcji bonzo_private_strategy. Używaj tylko jako supervisor/orchestrator."
				: `Wyszukuje chunki RAG dostępne dla ${workerName}. Zwraca tytuły, tagi, body i oznaczenie ⚠CRITICAL.`,
		parameters: z.object({
			question: z.string().describe("Pytanie do bazy wiedzy handlowej"),
			maxChunks: z.coerce.number().int().min(1).max(5).default(3),
		}),
		execute: async ({ question, maxChunks }) => {
			const all = getChunks();
			const mine = scope === "all" ? all : chunksForWorker(all, workerName);

			// Prosty scoring: liczba trafień tokenów (>=3 znaki) w tytule+tagach+body.
			const tokens = new Set(
				question
					.toLowerCase()
					.split(/\W+/u)
					.filter((t) => t.length >= 3),
			);
			const scored = mine
				.map((c) => {
					const hay = `${c.title} ${c.tags.join(" ")} ${c.body}`.toLowerCase();
					let score = 0;
					for (const t of tokens) if (hay.includes(t)) score += 1;
					return { c, score };
				})
				.filter((x) => x.score > 0)
				.sort((a, b) => b.score - a.score)
				.slice(0, maxChunks);

			// Dociągnij chunki krytyczne (np. regulacje WhatsApp) zawsze gdy worker ma do nich dostęp.
			const critical = criticalChunks(mine);
			const out: RagChunk[] = [...scored.map((s) => s.c)];
			for (const c of critical) if (!out.find((x) => x.id === c.id)) out.push(c);

			if (out.length === 0) {
				return `Brak chunków w bazie dla pytania: "${question}". Odpowiedz na podstawie ogólnej wiedzy i oznacz to jawnie.`;
			}
			return out
				.map(
					(c) =>
						`### ${c.id} — ${c.title}${c.priority === "critical" ? " ⚠PRIORITY:CRITICAL" : ""}\n[tags: ${c.tags.join(", ")}]\n${c.body}`,
				)
				.join("\n\n---\n\n");
		},
	});
}
