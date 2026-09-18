// Entry point — rejestruje agentów w VoltAgent, custom HTTP endpoints, startuje Buch REPL.
import "dotenv/config";
import { VoltAgent } from "@voltagent/core";
import { orchestrator } from "./orchestrator.js";
import { zlotowa } from "./workers/zlotowa.js";
import { bulka } from "./workers/bulka.js";
import { cwaniaczek } from "./workers/cwaniaczek.js";
import { bohdah } from "./workers/bohdah.js";
import { krzysiu } from "./workers/krzysiu.js";
import { startBuch } from "./buch.js";
import { registerHttpEndpoints } from "./http.js";

new VoltAgent({
	agents: {
		orchestrator,
		Polaczek_zlotowa_01: zlotowa,
		Polaczek_Bulka_01: bulka,
		Polaczek_cwaniaczek_01: cwaniaczek,
		Polaczek_Bohdan_01: bohdah,
		Polaczek_Krzysiu_01: krzysiu,
	},
});

registerHttpEndpoints();

await startBuch();
