# O Projekcie JIMBO

## Co to jest

JIMBO to lokalny chat operacyjny dla Bonzo. Ma odpowiadać konkretnie, bez marketingowej papki, z dostępem do pamięci, lokalnej bazy wiedzy i terminala w przeglądarce.

## Aktualny stack

- frontend: statyczne `index.html` + `app.js`
- backend: FastAPI w `backend/app/main.py`
- port lokalny: `4149`
- terminal: `xterm.js` + websocket `/ws/terminal`
- modele: OpenRouter, OpenAI albo Ollama
- historia rozmów: SQLite
- wiedza: `knowledge_base/`

## Aktualne uruchamianie

Główny launcher:

```bat
start.bat
```

CLI pomocnicze:

```bat
jimbo-cli.cmd health
```

## Kluczowe katalogi

- `backend/` - backend i lokalny Python
- `knowledge_base/` - aktywna baza wiedzy
- `knowledge_base/private_help/` - prywatna wiedza sklepu i platformy
- `themes/` - motywy UI
- `Icons33eeewwee/` - ikony serwowane przez backend
- `The_brain/` - starsze zasoby wiedzy i dane historyczne

## Endpointy, które mają znaczenie przy starcie

- `GET /api/health`
- `GET /api/models`
- `GET /api/tools`
- `POST /api/chat`
- `POST /api/chat/stream`
- `GET /api/knowledge`
- `POST /api/knowledge/upload`
- `DELETE /api/knowledge/{filename}`
- `GET /api/diary`
- `WS /ws/terminal`

## Uwaga

Starsze opisy Astro, Electron, Cloudflare Pages i portów `4433/4444` nie opisują już aktywnego układu tej aplikacji.
