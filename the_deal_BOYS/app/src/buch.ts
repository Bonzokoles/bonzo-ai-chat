// Buch — terminal CLI, szef wszystkich.
// Pętla REPL: czyta pytanie z stdin, przepuszcza przez dispatcher (keyword-based)
// do 1+ Polaczków, scala odpowiedzi, drukuje wynik.
import { createInterface } from "node:readline/promises";
import { stdin, stdout } from "node:process";
import { dispatchToWorkers, pickWorkers } from "./dispatcher.js";

const PROMPT = "\n[buch] > ";

function render(workers: string[], combined: string): string {
	const head = `[buch] pracuje: ${workers.join(", ")}`;
	return `${head}\n\n${combined}`;
}

export async function startBuch(): Promise<void> {
	const rl = createInterface({ input: stdin, output: stdout, terminal: false });

	console.log("╔══════════════════════════════════════════╗");
	console.log("║  Buch — terminal CLI, szef wszystkich   ║");
	console.log("║  pod spodem: dispatcher + 5 Polaczków   ║");
	console.log("║  exit / /quit = wyjście                 ║");
	console.log("╚══════════════════════════════════════════╝");

	while (true) {
		let line: string;
		try {
			line = (await rl.question(PROMPT)).trim();
		} catch {
			console.log("");
			break;
		}
		if (!line) continue;
		if (line === "exit" || line === "/quit" || line === "/exit") break;
		// Diagnostyka routingu — pokaż kogo dispatcher wybrał, BEZ odpalania LLM
		if (line === "/route" || line === "/who") {
			const w = pickWorkers("przykładowe pytanie");
			console.log(`\n[buch] (demo) dispatcher wybrałby: ${w.join(", ")}`);
			continue;
		}

		try {
			const { workers, combined } = await dispatchToWorkers(line);
			console.log("\n" + render(workers, combined));
		} catch (err) {
			const msg = err instanceof Error ? (err.stack ?? err.message) : JSON.stringify(err);
			console.error(`\n[błąd] ${msg}`);
		}
	}

	rl.close();
	console.log("[buch] papa.");
}
