// Orchestrator (czhatbot_orkiestrator) — supervisor floty Polaczki_workers.
// UWAGA: W tej wersji NIE używamy subAgents + delegate_task (modele pod 9router
// + caveman mają problem z tool calling formatem). Hierarchia działa tak:
//   Buch (terminal) → dispatcher (keyword router) → Polaczki (równolegle) → Buch (synteza)
// Orchestrator jest fallbackiem: dispatcher klasyfikuje, a jeśli nie pasuje do żadnego
// workera, Buch pyta orchestratora z pełnym RAG.
import { Agent } from "@voltagent/core";
import { VercelAIProvider } from "@voltagent/vercel-ai";
import { router, ROUTER_INFO } from "./providers/router.js";
import { getMemory } from "./agents/memory.js";
import { zlotowa } from "./workers/zlotowa.js";
import { bulka } from "./workers/bulka.js";
import { cwaniaczek } from "./workers/cwaniaczek.js";
import { bohdah } from "./workers/bohdah.js";
import { krzysiu } from "./workers/krzysiu.js";

export const orchestrator = new Agent({
	name: "czhatbot_orkiestrator",
	description:
		"Supervisor floty Polaczki_workers. Fallback do pełnej bazy RAG bonzo_private_strategy.",
	llm: new VercelAIProvider(),
	model: router.chatModel(ROUTER_INFO.defaultOrchestratorModel),
	memory: getMemory(),
	systemPrompt: `Jesteś czhatbot_orkiestrator — supervisor floty 5 wyspecjalizowanych agentów (Polaczki_workers) i ostatnia instancja dla Bonzo.

Twoja rola: rozmawiasz z Bonzo. W normalnym przepływie pytania idą do konkretnego Polaczka przez dispatcher. Ty jesteś fallbackiem — używasz się gdy:
- dispatcher nie dopasował pytania do żadnego workera,
- pytanie jest czysto meta (reguły, manifest, hierarchia, co wolno, czego nie),
- Bonzo prosi o audyt całego systemu.

Kontekst RAG (pełna kolekcja bonzo_private_strategy) jest dołączany do pytania jako blok "=== RAG CONTEXT (orchestrator) ===". Czytaj go i odpowiadaj na jego podstawie.

Twarde reguły:
- Kolekcja bonzo_private_strategy jest OSOBNA od baz klienckich (SklepGPT itp.).
- NIE podejmuj decyzji wykonawczych (zakup, publikacja, kampania).
- Odpowiadaj po polsku, zwięźle.`,
});

export const POLACZKI = {
	zlotowa,
	bulka,
	cwaniaczek,
	bohdah,
	krzysiu,
} as const;

export type PolaczekName = keyof typeof POLACZKI;
