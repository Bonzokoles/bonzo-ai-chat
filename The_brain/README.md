# THE BRAIN — COGNITIVE ARCHITECTURE & KNOWLEDGE ENGINE

Główny rdzeń kognitywny The Buch (`Z:\36_chambers\The_Buch\The_brain`).
Odpowiada za inteligencję bazową, reguły inżynierskie, modele myślowe, datasety i silniki wykonawcze agentów.

---

## MAPA ARCHITEKTURY

```
Z:\36_chambers\The_Buch\
├── The_brain/                    # Kognitywny rdzeń systemu (Cognitive Core)
│   ├── agents/                   # Silniki agentowe (smolagents, CodeAgent, runners)
│   ├── cinema/                   # Wzorce narracyjne, kinematografia, archetypy
│   │   ├── movies/               # Zbiory JSON z analizą stylistyczną filmów
│   │   └── movies_api/           # Cache metadanych TMDB/OMDB
│   ├── coding/                   # Inżynieria oprogramowania
│   │   ├── agent-rules-books/    # 14 książek inżynierskich (Full / Mini / Nano)
│   │   ├── code_alpaca.md        # Instrukcje kodowania Alpaca
│   │   └── python_instructions.md# Wytyczne implementacyjne Pythona
│   ├── datasets/                 # Zbiory treningowe, few-shoty i skrypty ChatML
│   │   ├── DATASETNO2_clean.jsonl# Few-shoty charakterologiczne asystenta
│   │   └── convert_pack*.py      # Konwertery formatów
│   ├── notes/                    # Notatki operacyjne i szkice architektoniczne Bonzo
│   ├── philosophy/               # Modele logiczne i klasyczna myśl (Arystoteles, Hume, Kant...)
│   ├── bonzo_diary.json          # Pamięć długoterminowa i preferencje Bonzo
│   └── bonzo_diary_log.jsonl     # Log interakcji i ewolucji kontekstu
├── PINKY_one/                    # Domena: E-commerce, Shopify, Operacje Sklepu
├── the_deal_BOYS/                # Domena: Hurt B2B, Sourcing, Arbitraż, Polaczki Workers
└── knowledge_mood/               # Hub agregacji (NTFS Junctions dla kompatybilności)
```

---

## OBSŁUGA MODUŁÓW I API

### 1. Inżynieria i Reguły Kodu (`coding/agent-rules-books`)
- **Loader:** `backend/app/coding_rules_loader.py`
- **Profil zadania:** `coding` ("Coding & Architecture")
- **Endpointy:**
  - `GET /api/coding-rules/list` — lista 14 ksiąg i dostępnych poziomów (`nano`, `mini`, `full`)
  - `GET /api/coding-rules/{slug}?tier=nano` — pobranie konkretnej reguły decyzyjnej
  - `POST /api/coding-rules/match` — dopasowanie reguł pod zapytanie dewelopera

### 2. Silniki Agentowe (`agents/`)
- Integracja `smolagents` (`CodeAgent`) zoptymalizowana pod API MyBonzo Cloudflare Workers AI.
- Pisanie bezpośredniego kodu Python zamiast kosztownego parsowania JSON tool-calli.

### 3. Pamięć i Profil Użytkownika (`bonzo_diary.json`)
- **Moduł:** `backend/app/diary.py`
- Automatyczne rejestrowanie faktów, preferencji i celów operacyjnych Bonzo.
