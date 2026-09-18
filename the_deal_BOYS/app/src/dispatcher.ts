// Dispatcher — keyword-based routing do workerów Polaczki + structured logging.
// Workery NIE mają tooli (modele 9router mają problem z tool calls).
// Zamiast tego dispatcher ładuje RAG i dokleja do pytania jako blok kontekstu.
import { POLACZKI, type PolaczekName } from "./orchestrator.js";
import { buildRagContext } from "./rag/context.js";
import { SESSION_CONVERSATION_ID } from "./agents/memory.js";

type WorkerKey = PolaczekName;

const RULES: Array<{ worker: WorkerKey; patterns: RegExp[] }> = [
	{
		worker: "zlotowa",
		patterns: [
			/\b(sourc|skan|marż|okazj|arbitraż|aliexpress|alibaba|walmart|amazon[-\s]?to[-\s]?amazon|zakup|rentown|promocj)\b/i,
		],
	},
	{
		worker: "bulka",
		patterns: [/\b(lejek|funnel|publikacj|wystawi[ćc]|klient.*\b(szuk|gdzie)|konwersj|wyciek|setup|sklep|checklist)\b/i],
	},
	{
		worker: "cwaniaczek",
		patterns: [/\b(sprzedaż|sprzeda[cw]|cross[-\s]?sell|upsell|koszyk|follow[-\s]?up|sekwencj|komunikat|ofert\w+)\b/i],
	},
	{
		worker: "bohdah",
		patterns: [/\b(whatsapp|meta\s*api|bot\w*\s*ai|komplianc|regulacj|rodo|ryzyk|nachaln|bot\w+)\b/i],
	},
	{
		worker: "krzysiu",
		patterns: [/\b(b2b|cennik|pricing|negocjacj|warunki|handl\w+|kontrakt|net\s*30|net\s*60|net\s*90|próg|progow)\b/i],
	},
];

const FORCE_BOHDAN_PATTERNS = [/\b(whatsapp|meta\s*api|bot.*\b(ai|komunik))\b/i];

export function pickWorkers(prompt: string): WorkerKey[] {
	const matched = new Set<WorkerKey>();

	// Explicit override tags (allows running multiple agents simultaneously on demand)
	if (prompt.includes("@all")) {
		return ["zlotowa", "bulka", "cwaniaczek", "bohdah", "krzysiu"];
	}

	const explicit: WorkerKey[] = [];
	if (prompt.includes("@zlotowa")) explicit.push("zlotowa");
	if (prompt.includes("@bulka")) explicit.push("bulka");
	if (prompt.includes("@cwaniaczek")) explicit.push("cwaniaczek");
	if (prompt.includes("@bohdan") || prompt.includes("@bohdah")) explicit.push("bohdah");
	if (prompt.includes("@krzysiu")) explicit.push("krzysiu");

	if (explicit.length > 0) {
		return explicit;
	}

	for (const rule of RULES) {
		for (const re of rule.patterns) {
			if (re.test(prompt)) {
				matched.add(rule.worker);
				break;
			}
		}
	}
	for (const re of FORCE_BOHDAN_PATTERNS) {
		if (re.test(prompt)) matched.add("bohdah");
	}
	if (matched.size === 0) matched.add("zlotowa");
	return [...matched];
}

function buildWorkerPrompt(workerName: WorkerKey, userQuestion: string): string {
	const ctx = buildRagContext(workerName, userQuestion);
	return `Pytanie od Bonzo:\n${userQuestion}\n\n=== RAG CONTEXT (${workerName}) ===\n${ctx}\n\n=== KONIEC RAG ===\n\nOdpowiedz konkretnie, w tonie i roli ${workerName}, na podstawie powyższego.`;
}

function obsLog(event: string, fields: Record<string, unknown>): void {
	console.log(`[obs] ${JSON.stringify({ ts: new Date().toISOString(), event, ...fields })}`);
}

export async function dispatchToWorkers(prompt: string): Promise<{ workers: WorkerKey[]; combined: string }> {
	const workers = pickWorkers(prompt);
	obsLog("dispatch.start", { workers, promptPreview: prompt.slice(0, 100) });

	const startedAt = Date.now();
	const results = await Promise.all(
		workers.map(async (name) => {
			const t0 = Date.now();
			try {
				const r = await POLACZKI[name].generateText(buildWorkerPrompt(name, prompt), {
					conversationId: `${SESSION_CONVERSATION_ID}:${name}`,
				});
				const ms = Date.now() - t0;
				obsLog("worker.end.ok", {
					worker: name,
					ms,
					promptTokens: r.usage?.promptTokens,
					completionTokens: r.usage?.completionTokens,
					totalTokens: r.usage?.totalTokens,
					preview: r.text.slice(0, 150),
				});
				return { name, text: r.text };
			} catch (err) {
				const ms = Date.now() - t0;
				const msg = err instanceof Error ? err.message : String(err);
				obsLog("worker.end.error", { worker: name, ms, error: msg });
				return { name, text: `[błąd workera ${name}: ${msg}]` };
			}
		}),
	);
	obsLog("dispatch.end", { workers, totalMs: Date.now() - startedAt });

	const combined = results.map(({ name, text }) => `## ${name}\n\n${text}`).join("\n\n---\n\n");
	return { workers, combined };
}
