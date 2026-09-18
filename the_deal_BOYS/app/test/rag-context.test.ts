import { beforeAll, describe, expect, it } from "vitest";
import { buildRagContext } from "../src/rag/context.js";
import { loadChunks, chunksForWorker, criticalChunks } from "../src/rag/loader.js";

beforeAll(() => {
	process.env.RAG_ROOT = "../rag";
});

describe("buildRagContext", () => {
	it("zwraca string dla scope=worker", () => {
		const ctx = buildRagContext("Polaczek_zlotowa_01", "marża sourcing");
		expect(ctx).toBeTruthy();
		expect(ctx.length).toBeGreaterThan(50);
	});

	it("zwraca string dla scope=all (orchestrator)", () => {
		const ctx = buildRagContext("orchestrator", "regulacje Meta", { scope: "all" });
		expect(ctx).toBeTruthy();
		expect(ctx).toContain("PRIORITY:CRITICAL"); // chunk_11 powinien tu trafić
	});

	it("dodaje ⚠PRIORITY:CRITICAL dla chunk_11 przy workerze bohdah", () => {
		const ctx = buildRagContext("Polaczek_Bohdan_01", "whatsapp");
		expect(ctx).toContain("PRIORITY:CRITICAL");
	});

	it("NIE dodaje chunk_11 dla zlotowej (nie ma w jego target_workers)", () => {
		const ctx = buildRagContext("Polaczek_zlotowa_01", "marża");
		expect(ctx).not.toContain("chunk_11");
	});

	it("zwraca placeholder gdy brak dopasowań", () => {
		const ctx = buildRagContext("Polaczek_zlotowa_01", "xzq123");
		expect(ctx).toMatch(/brak dopasowanych/i);
	});
});

describe("loader integration", () => {
	it("loadChunks zwraca 14 chunków", () => {
		const chunks = loadChunks("../rag");
		expect(chunks.length).toBe(14);
	});

	it("chunksForWorker filtruje po target_workers", () => {
		const chunks = loadChunks("../rag");
		const zlotowa = chunksForWorker(chunks, "Polaczek_zlotowa_01");
		expect(zlotowa.length).toBeGreaterThan(0);
		expect(zlotowa.every((c) => c.targetWorkers.includes("Polaczek_zlotowa_01"))).toBe(true);
	});

	it("criticalChunks zwraca tylko priority:critical", () => {
		const chunks = loadChunks("../rag");
		const critical = criticalChunks(chunks);
		expect(critical.length).toBeGreaterThan(0);
		expect(critical.every((c) => c.priority === "critical")).toBe(true);
	});
});
