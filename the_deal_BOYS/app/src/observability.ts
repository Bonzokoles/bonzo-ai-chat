// Observability — structured logging przez VoltAgent AgentHooks.
// Loguje: agent name, event, prompt, response time, token usage.
// Output: linia JSON do stdout (łatwa do późniejszego pipe'owania do pliku/Elastic/etc).
import type { AgentHooks } from "@voltagent/core";

function log(event: string, fields: Record<string, unknown>): void {
	const line = JSON.stringify({ ts: new Date().toISOString(), event, ...fields });
	// tag [obs] żeby odróżnić od logów VoltAgent
	console.log(`[obs] ${line}`);
}

export function makeObservabilityHooks(agentName: string): AgentHooks {
	let startedAt = 0;
	return {
		onStart: async () => {
			startedAt = Date.now();
		},
		onEnd: async (args) => {
			const ms = Date.now() - startedAt;
			const err = args.error as Error | undefined;
			if (err) {
				log("agent.end.error", { agent: agentName, ms, error: err.message });
				return;
			}
			const out = args as {
				conversationId?: string;
				output?: unknown;
				usage?: { promptTokens?: number; completionTokens?: number; totalTokens?: number };
			};
			const text = typeof out.output === "string" ? out.output.slice(0, 200) : undefined;
			log("agent.end.ok", {
				agent: agentName,
				ms,
				promptTokens: out.usage?.promptTokens,
				completionTokens: out.usage?.completionTokens,
				totalTokens: out.usage?.totalTokens,
				preview: text,
			});
		},
	};
}
