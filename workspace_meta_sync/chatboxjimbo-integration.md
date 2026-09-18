# CHATboxJIMBO integration note

Updated: 2026-05-08 04:57:46

## Why this is worth integrating
- WORKSPACE_META_TEMPLATE gives reusable metadata backbone (.workspace_meta + GIT_HOOB_catalogi).
- For CHATboxJIMBO this is useful as control-plane layer: active tools, deployed parts, priorities.
- Keep primary knowledge local in CHATboxJIMBO\knowledge_base and mirror only curated statuses/notes.

## Recommended split
- Local-first knowledge and memory: CHATboxJIMBO\knowledge_base + diary/profile endpoints.
- Workspace meta/control: WORKSPACE_META_TEMPLATE\.workspace_meta\notes + GIT_HOOB_catalogi\ai-status-updates.json.

## Added CLI surface in CHATbox
- jimbo-cli.py
- jimbo-cli.cmd

Commands:
- health
- research <query>
- tmdb <query>
- decide <topic> [--option ...] [--constraint ...]
- memory show|add-fact|add-pref|add-goal|clear
