# Manifest RAG — handel_agenci

Indeks routingu: które chunki widzi orkiestrator i które trafiają do których workerów Polaczki_workers. Kolekcja wektorowa: **`bonzo_private_strategy`** (oddzielna od kolekcji klienckich — patrz README → "Ważne").

## Tabela routingu

| Chunk | Tytuł | Tagi | Worker(zy) docelowy(i) |
|---|---|---|---|
| chunk_01 | Mini-marża: realistyczne liczby | arbitraż, marża, sourcing, decyzja-biznesowa | Polaczek_zlotowa_01, Polaczek_Krzysiu_01 |
| chunk_02 | Gdzie szukać tanich źródeł | sourcing, dostawcy, arbitraż | Polaczek_zlotowa_01 |
| chunk_03 | Proces zakup→sprzedaż krok po kroku | arbitraż, proces, automatyzacja | Polaczek_zlotowa_01, Polaczek_Bulka_01 |
| chunk_04 | Porównanie modeli biznesowych | strategia, model-biznesowy, decyzja | Polaczek_zlotowa_01, Polaczek_Krzysiu_01 |
| chunk_05 | Lejek B2C: gdzie szukać wycieku | lejek, konwersja, diagnoza, funnel | Polaczek_Bulka_01 |
| chunk_06 | Lejek B2B: jak dziś kupują firmy | b2b, lejek, sprzedaż, funnel | Polaczek_Krzysiu_01 |
| chunk_07 | Skala i mechanika rynku B2B | b2b, rynek, statystyki, decyzja | Polaczek_Krzysiu_01 |
| chunk_08 | Modele cenowe B2B | b2b, cennik, pricing, wdrożenie | Polaczek_Krzysiu_01 |
| chunk_09 | Checklist budowy sklepu od zera | sklep, setup, checklist, operacje | Polaczek_Bulka_01, orchestrator |
| chunk_10 | Boty AI: 3 kategorie + co działa | ai, automatyzacja, boty, narzędzia | orchestrator, Polaczek_cwaniaczek_01, Polaczek_Bohdan_01 |
| chunk_11 | KRYTYCZNE: regulacje WhatsApp/Meta 2026 | regulacje, ryzyko, whatsapp, compliance | orchestrator, Polaczek_Bohdan_01, Polaczek_cwaniaczek_01 |
| chunk_12 | Self-hosting AI = przewaga konkurencyjna | infrastruktura, rodo, self-hosting | orchestrator, Polaczek_Bohdan_01 |
| chunk_13 | 7 błędów wdrożeniowych + plan 5 kroków | wdrożenie, błędy, plan-działania | orchestrator, Polaczek_Bohdan_01 |
| chunk_14 | Cross-sell/upselling: mechanika i liczby | upsell, cross-sell, konwersja, revenue | Polaczek_cwaniaczek_01, Polaczek_Bulka_01 |

## Reguła routingu (dla orkiestratora)

1. Sklasyfikuj zapytanie po słowach kluczowych/intencji → dopasuj do `tags`.
2. Wybierz workera, dla którego dany tag jest w `target_workers`.
3. Jeśli zapytanie dotyczy >1 workera (np. "czy mogę sprzedawać to na WhatsApp z marżą 30%?") — orchestrator zbiera odpowiedzi cząstkowe z obu (`Polaczek_zlotowa_01` + `Polaczek_Bohdan_01`/regulacje z chunk_11) i syntetyzuje.
4. Chunk_11 (regulacje WhatsApp) ma `priority: critical` we frontmatterze — orchestrator zawsze go dociąga przy KAŻDYM temacie dot. komunikatorów/botów, niezależnie od dopasowania tagów.

## Filtrowanie metadanych przy zapytaniu (przykład)

```
query: "ile mogę zarobić kupując na wyprzedażach i odsprzedając na Amazon?"
filter: tags ∋ {arbitraż, marża, sourcing}
→ trafia: chunk_01, chunk_02, chunk_03, chunk_04
→ worker: Polaczek_zlotowa_01
```

## Świeżość danych

Statystyki rynkowe (np. "rynek B2B $32 bln", "59,6% self-hosted AI") mają punkt odniesienia 2025/2026 — przy odpowiedziach długoterminowych (>12 mies. od daty source) oznaczaj jako wymagające odświeżenia przez nowy research.
