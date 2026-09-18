# Source Map — handel_agenci

## Pliki źródłowe (raw/)

- **`raw/RESEARCH_ECOMMERCE_SPRZEDAZ_B2B_BOTY_2026.md`** (24 KB)
  Pełny research syntetyczny: lejki sprzedażowe (B2C 5-warstwowy + B2B 5-etapowy), wiedza handlowa B2B (statystyki rynku, modele cenowe, terminy płatności), organizacja sklepu (18-krokowy przewodnik), boty sprzedażowo-zakupowe (3 kategorie AI, regulacja Meta/WhatsApp 2026, self-hosting/RODO), tani sourcing/arbitraż (marże, model biznesowy, kanały/narzędzia), synteza strategiczna dla Bonzo (5 podbloków A-E).

- **`raw/PRYWATNA_BAZA_RAG_AGENCI_HANDLOWI.md`** (19 KB) — PLIK KLUCZOWY
  Już wstępnie ustrukturyzowany pod RAG:
  - Część A: 14 chunków `[CHUNK 01]`–`[CHUNK 14]` z TAGI — źródło dla `rag/chunks/`
  - Część B: 5 specyfikacji agentów (Wejście/Logika/Wyjście/Wiedza RAG/Stack/Ryzyko) — źródło dla `rag/apps/polaczki_workers.md`
  - Część C: notatki implementacyjne RAG (chunking, metadane, separacja kolekcji, świeżość danych)

## Mapowanie raw → RAG

| Źródło | Sekcja | Trafia do |
|---|---|---|
| PRYWATNA_BAZA / Część A | [CHUNK 01-14] | `rag/chunks/chunk_01..14_*.md` (rozbite na osobne pliki + frontmatter) |
| PRYWATNA_BAZA / Część B | 5 specyfikacji agentów | `rag/apps/polaczki_workers.md` |
| PRYWATNA_BAZA / Część C | Uwagi RAG | `rag/manifest.md` + `README.md` (sekcja "Ważne") |
| RESEARCH_ECOMMERCE... | całość (kontekst źródłowy) | pozostaje jako `raw/` — punkt odniesienia, NIE jest dzielony na chunki (zawiera te same fakty co PRYWATNA_BAZA, ale w formie narracyjnej, nie atomowej) |

## Status

✅ Chunki rozbite na pliki (14/14), gotowe do embeddingu.
✅ Specyfikacje aplikacji napisane (`czhatbot_orkiestrator.md`, `polaczki_workers.md`).
⏳ Wektoryzacja i podłączenie do silnika RAG — runtime jeszcze nie istnieje (patrz `README.md` → "Ważne").
