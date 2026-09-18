---
name: m-drive-explorer
description: >
  Mapa dysku M:\ — lokalizacje projektów, narzędzi i zasobów. Używaj gdy
  musisz odnaleźć pliki na dysku M:\ lub zrozumieć strukturę workspace.
applyTo: "**"
---

# M:\ Drive — Mapa Zasobów

## Dysk M:\ — Główne Projekty

```
M:\
├── CHATboxJIMBO\           ← AKTYWNY projekt (Jimbo chatbot + Astro)
├── CHATboxJIMBO\.github\   ← Skills, prompts, agents
│   ├── skills\             ← Niniejszy skill i inne
│   └── prompts\            ← Copilot prompts
│
├── CHATboxJIMBO\openspec\  ← Workflow management
│   ├── schemas\            ← Schematy: quick-fix, research-first, hotfix, api-feature
│   └── changes\            ← Aktywne i archiwalne zmiany
│
├── (inne projekty w M:\)   ← Skan via MCP filesystem-m-drive
```

## Dysk M:\ — Skanowanie przez MCP

MCP Server `filesystem-m-drive` daje dostęp do całego M:\:

```
# W Copilot chat (po restarcie) wpisz:
@filesystem-m-drive list_directory M:\
@filesystem-m-drive read_file M:\CHATboxJIMBO\package.json
```

## Kluczowe Ścieżki CHATboxJIMBO

| Ścieżka | Zawartość |
|---------|-----------|
| `M:\CHATboxJIMBO\` | Root projektu |
| `M:\CHATboxJIMBO\.env` | API klucze (OpenRouter, OpenAI) |
| `M:\CHATboxJIMBO\Chatbotlocal\backend\app\` | FastAPI backend |
| `M:\CHATboxJIMBO\Chatbotlocal\backend\app\model.py` | MultiProviderModel (OpenRouter/OpenAI/Ollama) |
| `M:\CHATboxJIMBO\Chatbotlocal\backend\app\main.py` | FastAPI endpoints |
| `M:\CHATboxJIMBO\Chatbotlocal\src\components\ChatWidgetJimbo.jsx` | Chat UI (React) |
| `M:\CHATboxJIMBO\src\pages\index.astro` | Główna strona Astro |
| `M:\CHATboxJIMBO\openspec\changes\` | Aktywne zmiany OpenSpec |
| `M:\CHATboxJIMBO\.github\skills\` | Skills dla Copilot |
| `M:\CHATboxJIMBO\.github\prompts\` | Prompts dla Copilot |

## Narzędzia Globalne (C:\)

| Ścieżka | Narzędzie |
|---------|-----------|
| `C:\Python313\python.exe` | Python 3.13 |
| `C:\nvm4w\nodejs\node.exe` | Node.js v24.14.1 |
| `C:\nvm4w\nodejs\openspec.cmd` | OpenSpec CLI v1.3.1 |
| `C:\WORKSPACE_META_TEMPLATE\` | Szablony + openspec-speckit-guide.html |
| `Z:\OpenSpec\` | Źródło OpenSpec |

## VS Code Insiders — Konfiguracja

| Ścieżka | Plik |
|---------|------|
| `C:\Users\Bonzo2\AppData\Roaming\Code - Insiders\User\settings.json` | Ustawienia globalne |
| `C:\Users\Bonzo2\AppData\Roaming\Code - Insiders\User\globalStorage\kilocode.kilo-code\settings\mcp_settings.json` | MCP serwery |
| `C:\Users\Bonzo2\AppData\Roaming\Code - Insiders\User\prompts\` | User-scoped prompts |

## MCP Server: filesystem-m-drive

Serwer MCP daje modelowi bezpośredni dostęp do plików na M:\.  
Konfiguracja: `mcp_settings.json` → `@modelcontextprotocol/server-filesystem M:\`  
Copilot settings.json: blok `"mcp"` → `filesystem-m-drive`
