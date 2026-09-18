// Cienka warstwa nad rag/chunks + rag/manifest.md — bez monolitu, tylko odczyt + filtrowanie wg tagów/workera.
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import matter from "gray-matter";

export interface RagChunk {
  id: string; // np. "chunk_01"
  file: string;
  title: string;
  tags: string[];
  priority?: "critical" | "normal";
  targetWorkers: string[];
  body: string;
}

const CHUNK_FILE_RE = /^chunk_(\d{2})_.*\.md$/;

/**
 * Wczytuje wszystkie chunki z rag/chunks/*.md.
 * Frontmatter każdego pliku MUSI zawierać: id, title, tags, target_workers, (opcjonalnie) priority.
 * Jeśli frontmatter nie zawiera tych pól — chunk jest pomijany z ostrzeżeniem (fail-soft, nie fail-hard).
 */
export function loadChunks(ragRoot: string): RagChunk[] {
  const chunksDir = join(ragRoot, "chunks");
  const files = readdirSync(chunksDir).filter((f) => CHUNK_FILE_RE.test(f));
  const chunks: RagChunk[] = [];

  for (const file of files) {
    const raw = readFileSync(join(chunksDir, file), "utf-8");
    const { data, content } = matter(raw);

    const id = String(data.id ?? file.match(CHUNK_FILE_RE)?.[0]?.replace(/\.md$/, "") ?? file);
    const tags: string[] = Array.isArray(data.tags) ? data.tags : [];
    const targetWorkers: string[] = Array.isArray(data.target_workers) ? data.target_workers : [];

    chunks.push({
      id,
      file,
      title: String(data.title ?? id),
      tags,
      priority: data.priority === "critical" ? "critical" : "normal",
      targetWorkers,
      body: content.trim(),
    });
  }

  return chunks.sort((a, b) => a.id.localeCompare(b.id));
}

/** Chunki, do których dany worker MA dostęp (wg target_workers w frontmatter). */
export function chunksForWorker(chunks: RagChunk[], workerName: string): RagChunk[] {
  return chunks.filter((c) => c.targetWorkers.includes(workerName));
}

/** Chunki oznaczone jako priority: critical — orchestrator dociąga je ZAWSZE przy danym temacie (np. compliance WhatsApp/Meta). */
export function criticalChunks(chunks: RagChunk[]): RagChunk[] {
  return chunks.filter((c) => c.priority === "critical");
}

/** Proste dopasowanie po tagach — do wstępnej klasyfikacji intencji przez orchestratora. */
export function chunksByTags(chunks: RagChunk[], tags: string[]): RagChunk[] {
  const wanted = new Set(tags.map((t) => t.toLowerCase()));
  return chunks.filter((c) => c.tags.some((t) => wanted.has(t.toLowerCase())));
}

/** Renderuje wybrane chunki do pojedynczego bloku kontekstu wstrzykiwanego w prompt agenta. */
export function renderContext(chunks: RagChunk[]): string {
  if (chunks.length === 0) return "(brak dopasowanych chunków RAG — odpowiadaj wyłącznie na podstawie ogólnej wiedzy i zaznacz to wyraźnie)";
  return chunks
    .map((c) => `### ${c.id} — ${c.title} [tags: ${c.tags.join(", ")}]${c.priority === "critical" ? " ⚠ PRIORITY: CRITICAL" : ""}\n${c.body}`)
    .join("\n\n---\n\n");
}
