# the_deal_BOYS/app

Supervisor + 5 sub-agentów (Polaczki) dla prywatnej bazy RAG `bonzo_private_strategy`.
Gateway LLM: 9router (OpenAI-compatible) na `127.0.0.1:20128`. Framework: VoltAgent.

## Hierarchia

```
Buch (terminal CLI, REPL)                   ← szef, user-facing
  └─ dispatcher (keyword router, src/dispatcher.ts)
       ├─ Polaczek_zlotowa_01   (łowca okazji)        chunks 01..04
       ├─ Polaczek_Bulka_01     (audyt sensu)         chunks 03, 05, 09, 14
       ├─ Polaczek_cwaniaczek_01 (sprzedawca)         chunks 10, 14 (+11 jeśli WhatsApp)
       ├─ Polaczek_Bohdan_01    (ochrona)             chunks 11, 12, 13
       └─ Polaczek_Krzysiu_01   (B2B)                 chunks 06, 07, 08 (+01)
  └─ czhatbot_orkiestrator    (fallback, pełny RAG)
```

## Dlaczego dispatcher w kodzie, nie subAgents?

9router w trybie caveman (oszczędność 20-40% tokenów) injectuje system prompt
który psuje tool calling modeli — zwracają JSON Schema zamiast flat args albo
odmawiają odpowiedzi ("function definitions not comprehensive"). Dlatego workery
nie mają tools, RAG jest prelowadowany w prompcie przez dispatcher, a routowanie
idzie przez keyword/regex w `src/dispatcher.ts` (deterministyczne, debugowalne).

## Uruchomienie

```bash
# 1. Zainstaluj deps
npm install --ignore-scripts

# 2. Skopiuj .env (klucz 9router jest już w .env)
cp .env.example .env

# 3. Upewnij się że 9router działa (port 20128)
# 4. Uruchom Buch
npm start
```

## Komendy w REPL

- pytanie → dispatcher → 1+ Polaczków → odpowiedź
- `/route` — pokaż kogo dispatcher wybrałby na "przykładowe pytanie" (test routingu)
- `exit` / `/quit` / `/exit` — wyjście

## Znane obejścia 9router bugów

W `src/providers/router.ts` jest monkey-patch `globalThis.fetch` który:
- stripuje trailing `}data: [DONE]` doklejane do non-stream JSON
- redukuje podwójne `data: [DONE]` w stream mode

Bez tego Vercel AI SDK rzuca "Invalid JSON response".

## HTTP/Web UI

Po `npm start` serwer nasłuchuje na `http://127.0.0.1:3141` (port z VoltAgent default).

Endpointy:
- `GET /` — statyczny web UI (formularz pytanie + wynik)
- `GET /api/health` — status, lista workerów
- `GET /api/workers` — same worker IDs
- `POST /api/who` — `{prompt: "..."}` → `{workers: [...]}` (test routingu bez LLM)
- `POST /api/dispatch` — `{prompt: "..."}` → `{workers, combined}` (dispatcher + 1+ workerów)

Swagger UI: `http://127.0.0.1:3141/ui` (VoltAgent auto-generated dla agentów).

## Memory

Workery pamiętają kontekst między pytaniami w sesji. Backend: LibSQL file (`./data/agent.db`).
ConversationId per worker: `buch-repl-session:{worker_name}`. Wyczyść: `rm data/agent.db`.

## Observability

Dispatcher loguje structured JSON na stdout:
```
[obs] {"ts":"...","event":"worker.end.ok","worker":"bulka","ms":3139,"promptTokens":288,"completionTokens":95,"totalTokens":383,"preview":"..."}
```

Pipe do pliku / log aggreatora: `npm start 2>&1 | grep '^\[obs\]' > /var/log/buch.jsonl`.

## Testy

```bash
npm test
```

3 pliki: `dispatcher.test.ts` (routing, 9 testów), `rag-context.test.ts` (RAG context, 6), `worker-contract.test.ts` (workery istnieją, 13). łącznie 28.
