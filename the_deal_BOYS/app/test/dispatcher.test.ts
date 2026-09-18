import { describe, expect, it } from "vitest";
import { pickWorkers } from "../src/dispatcher.js";

describe("pickWorkers", () => {
	it("kieruje pytanie sourcingowe do zlotowej", () => {
		expect(pickWorkers("Szukam okazji na Alibaba")).toEqual(["zlotowa"]);
	});

	it("kieruje pytanie o lejek do Bulki", () => {
		const w = pickWorkers("Mam wyciek w lejku sprzedażowym");
		expect(w).toContain("bulka");
	});

	it("kieruje pytanie o sprzedaż do cwaniaczka", () => {
		expect(pickWorkers("Jak zrobić follow-up po porzuconym koszyku?")).toEqual(["cwaniaczek"]);
	});

	it("kieruje pytanie o WhatsApp/Meta do Bohdan", () => {
		expect(pickWorkers("Jakie są regulacje Meta 2026 dla WhatsApp?")).toEqual(["bohdah"]);
	});

	it("kieruje pytanie o B2B do Krzysia", () => {
		expect(pickWorkers("Potrzebuję cennika progowego dla B2B, Net 30")).toEqual(["krzysiu"]);
	});

	it("dla multi-domain query wybiera wielu workerów", () => {
		const w = pickWorkers("Czy mogę sprzedać produkt z Alibaba przez bota na WhatsApp z marżą 30%?");
		expect(w).toContain("zlotowa"); // Alibaba → sourcing
		expect(w).toContain("bohdah"); // WhatsApp → compliance
	});

	it("zawsze dołącza Bohdan dla WhatsApp nawet gdy pytanie nie pasuje do bohdah bezpośrednio", () => {
		const w = pickWorkers("Mam okazję na Alibaba, chcę ją reklamować przez bota na WhatsApp");
		expect(w).toContain("zlotowa");
		expect(w).toContain("bohdah");
	});

	it("fallback do zlotowej gdy nic nie pasuje", () => {
		const w = pickWorkers("lorem ipsum dolor sit amet");
		expect(w).toEqual(["zlotowa"]);
	});

	it("zwraca unikalne wartości (bez duplikatów)", () => {
		const w = pickWorkers("sourcing sourcing lejek lejek WhatsApp");
		expect(new Set(w).size).toBe(w.length);
	});
});
