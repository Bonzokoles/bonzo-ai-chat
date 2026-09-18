---
name: terminal-cli
description: >
  Wzorce komend CLI dla projektu CHATboxJIMBO. Używaj gdy musisz uruchomić
  terminal, openspec, npm, python lub git w tym projekcie.
applyTo: "**"
---

# Terminal CLI — Wzorce Komend

## WAŻNE: Node.js nie jest domyślnie w PATH

Przed każdą komendą `openspec` lub `node` dodaj:

```powershell
$env:PATH = "C:\nvm4w\nodejs;$env:PATH"
```

## OpenSpec

```powershell
# Inicjalizacja (jednorazowo)
$env:PATH = "C:\nvm4w\nodejs;$env:PATH"; cd M:\CHATboxJIMBO; openspec init --tools github-copilot

# Nowa zmiana z schematem
openspec new change <nazwa> --schema <quick-fix|research-first|hotfix|api-feature|spec-driven>

# Status projektu
openspec view
openspec status
openspec schemas

# Archiwizacja ukończonej zmiany
openspec archive <nazwa>
```

## Backend Python (Chatbotlocal)

```powershell
# Uruchomienie backendu
cd M:\CHATboxJIMBO\Chatbotlocal\backend\app; python main.py

# Backend słucha na: http://localhost:8000
# Health check: http://localhost:8000/api/health
# Modele: http://localhost:8000/api/models
```

## npm / Astro (Frontend)

```powershell
cd M:\CHATboxJIMBO

# Dev server
npm run dev

# Build
npm run build

# Zainstaluj zależności
npm install
```

## Git

```powershell
cd M:\CHATboxJIMBO

# Status i push
git status
git add .
git commit -m "opis"
git push

# Sprawdź remote
git remote -v
```

## Środowisko

| Tool | Ścieżka | Wersja |
|------|---------|--------|
| Node.js | `C:\nvm4w\nodejs\node.exe` | v24.14.1 |
| openspec | `C:\nvm4w\nodejs\openspec.cmd` | v1.3.1 |
| Python | `C:\Python313\python.exe` | 3.13 |
| specify | `C:\Users\Bonzo2\pipx\venvs\specify-cli\Scripts\specify.exe` | v0.8.5 |
| npm | `C:\nvm4w\nodejs\npm.cmd` | — |

## Zmienne środowiskowe (.env)

Plik `.env` w `M:\CHATboxJIMBO\.env`:
- `OPENROUTER_API_KEY` — klucz OpenRouter (domyślny LLM provider)
- `OPENAI_API_KEY` — klucz OpenAI (fallback)
- Model domyślny: `google/gemma-4-31b-it:free`
