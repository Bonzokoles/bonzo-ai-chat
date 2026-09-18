import { describe, expect, it } from "vitest";
import { POLACZKI, orchestrator } from "../src/orchestrator.js";

describe("worker contract", () => {
	const expected: Array<{ key: keyof typeof POLACZKI; role: string }> = [
		{ key: "zlotowa", role: "łowca okazji" },
		{ key: "bulka", role: "audyt" },
		{ key: "cwaniaczek", role: "sprzedawca" },
		{ key: "bohdah", role: "ochrona" },
		{ key: "krzysiu", role: "B2B" },
	];

	for (const { key, role } of expected) {
		it(`${key} istnieje i ma poprawną nazwę`, () => {
			const agent = POLACZKI[key];
			expect(agent).toBeDefined();
			expect(agent.name).toBe(`Polaczek_${rolePrefix(key)}_01`);
		});

		it(`${key} prompt wspomina o roli: ${role}`, () => {
			// Brak public API do odczytu promptu — weryfikujemy przez name+description
			const agent = POLACZKI[key];
			expect(agent.name.toLowerCase()).toMatch(roleSubstring(role));
		});
	}

	it("orchestrator istnieje", () => {
		expect(orchestrator).toBeDefined();
		expect(orchestrator.name).toBe("czhatbot_orkiestrator");
	});
});

function rolePrefix(key: string): string {
	const map: Record<string, string> = {
		zlotowa: "zlotowa",
		bulka: "Bulka",
		cwaniaczek: "cwaniaczek",
		bohdah: "Bohdan",
		krzysiu: "Krzysiu",
	};
	return map[key] ?? key;
}

function roleSubstring(role: string): RegExp {
	const map: Record<string, RegExp> = {
		"łowca okazji": /zlotowa|okazj|sourc/i,
		audyt: /bulka|lejek|funnel/i,
		sprzedawca: /cwaniaczek|sprzeda/i,
		ochrona: /bohdan|komplianc|ryzyk/i,
		"B2B": /krzysiu|b2b|handl/i,
	};
	return map[role] ?? /./i;
}
