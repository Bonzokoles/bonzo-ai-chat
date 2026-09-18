// Wspólna pamięć dla wszystkich agentów (file-based libsql).
// Workery pamiętają kontekst między pytaniami Bonzo — dispatcher przekazuje
// conversationId, dzięki czemu kolejne pytania w sesji widzą poprzednie.
import { LibSQLStorage } from "@voltagent/core";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";

const DB_PATH = process.env.MEMORY_DB_PATH ?? "./data/agent.db";

let cached: LibSQLStorage | null = null;

export function getMemory(): LibSQLStorage {
	if (cached) return cached;
	mkdirSync(dirname(DB_PATH), { recursive: true });
	cached = new LibSQLStorage({ url: `file:${DB_PATH}` });
	return cached;
}

/** Stabilny conversationId dla bieżącej sesji Buch. Wszystkie wywołania w sesji
 *  widzą swoje poprzednie odpowiedzi (per worker). */
export const SESSION_CONVERSATION_ID = "buch-repl-session";
