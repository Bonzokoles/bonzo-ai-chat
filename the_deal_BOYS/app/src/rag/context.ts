// Loader kontekstu RAG — zwraca string gotowy do wstrzyknięcia w prompt.
// Oddzielone od createRagTool, bo w nowej architekturze workery nie mają tools
// (RAG jest prelowadowany w prompcie, żeby uniknąć kruchości model tool calls).
import { loadChunks, chunksForWorker, criticalChunks, type RagChunk } from "./loader.js";

let cached: RagChunk[] | null = null;

function getChunks(): RagChunk[] {
	if (!cached) {
		const ragRoot = process.env.RAG_ROOT ?? "../rag";
		cached = loadChunks(ragRoot);
	}
	return cached;
}

export function buildRagContext(workerName: string, question: string, opts?: { scope?: "worker" | "all" }): string {
	const all = getChunks();
	const scope = opts?.scope ?? "worker";
	const pool = scope === "all" ? all : chunksForWorker(all, workerName);

	const tokens = new Set(
		question
			.toLowerCase()
			.split(/\W+/u)
			.filter((t) => t.length >= 3),
	);
	const scored = pool
		.map((c) => {
			const hay = `${c.title} ${c.tags.join(" ")} ${c.body}`.toLowerCase();
			let score = 0;
			for (const t of tokens) if (hay.includes(t)) score += 1;
			return { c, score };
		})
		.filter((x) => x.score > 0)
		.sort((a, b) => b.score - a.score)
		.slice(0, 3);

	// Chunki krytyczne (priority: critical) są dociągane ZAWSZE gdy worker ma do nich dostęp.
	const critical = criticalChunks(pool);
	const out: RagChunk[] = [...scored.map((s) => s.c)];
	for (const c of critical) if (!out.find((x) => x.id === c.id)) out.push(c);

	if (out.length === 0) {
		return "(brak dopasowanych chunków RAG w zakresie workera)";
	}
	return out
		.map(
			(c) =>
				`### ${c.id} — ${c.title}${c.priority === "critical" ? " ⚠PRIORITY:CRITICAL" : ""}\n[tags: ${c.tags.join(", ")}]\n${c.body}`,
		)
		.join("\n\n---\n\n");
}
