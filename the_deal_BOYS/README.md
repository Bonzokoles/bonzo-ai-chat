# handel_agenci — prywatna baza RAG: handel, marże, B2B, agenci

**Status: PRYWATNE.** Wyłącznie do użytku własnego Bonzo — wsparcie przy sklepie i biznesie. NIE dla klientów końcowych, NIE do podpięcia pod chatboty publiczne (SklepGPT itp.). Zasada zgodna z konwencją sąsiedniego folderu [`private_help/`](../private_help/README.md) — ten sam reżim separacji.

## Cel

Dostarczyć gotową do wektoryzacji bazę wiedzy o sprzedaży/zakupach/marżach/B2B/automatyzacji handlu, na bazie której działają dwie własne aplikacje:

- **czhatbot_orkiestrator** — router zapytań do specjalistycznych agentów
- **Polaczki_workers** — flota 5 wyspecjalizowanych agentów handlowych:
  - `Polaczek_zlotowa_01`
  - `Polaczek_Bulka_01`
  - `Polaczek_cwaniaczek_01`
  - `Polaczek_Bohdan_01`
  - `Polaczek_Krzysiu_01`

## Co jest w środku

```
handel_agenci/
├── README.md                      ← ten plik
├── SOURCE_MAP.md                  ← mapa źródeł (raw → chunki)
├── raw/                           ← surowe materiały źródłowe (pełne dokumenty)
│   ├── RESEARCH_ECOMMERCE_SPRZEDAZ_B2B_BOTY_2026.md
│   └── PRYWATNA_BAZA_RAG_AGENCI_HANDLOWI.md
└── rag/
    ├── manifest.md                ← indeks/routing: chunk → tagi → który worker
    ├── chunks/                    ← 14 atomowych chunków gotowych do embeddingu
    │   └── chunk_01..14_*.md      (frontmatter: id/title/tags/target_workers/source)
    └── apps/
        ├── czhatbot_orkiestrator.md   ← spec routera
        └── polaczki_workers.md        ← specyfikacje 5 agentów-workerów  (muj dopis ,agenci ; nazwy wsztstkie agenty ten sam początek: Polaczek_(wtedy w tm miejscu nazwa tematyczna)_nr (nieraz kilku od tego samego to puzniej numery)   = Polaczek_złotówa_01( i dalej _02 i _03 =jesli bedzie trzeba) = wszykiwanie dealów, super promocji i super okazji,   no2: Polaczek_Bułka_01 sprawdza czy deale mają sens ,ustwiają logike szukają klijenta,kopiują info o rzeczach na sprzedarz i dodają tymczasowo do strony,Polaczek_cwaniaczek_01 -sprzedawca ,sprzedaja robi wszystko zeby sprzedać, Polaczek_Bohdan_01=ochrona,sprawdza co sie dzieje ,trzuma porząsek,broni prze zbyt nachalnymi botami,anawet wyłapuje te za bardzo brojące, Polaczek_Krzysiu_01 =biznesowy,rozmowy biznesowe,biznesy,wymiana towarów,nie daje sie nigdu zrobić na minus.    
        
        wszytkie agenty mają byc modelami AI ewntualnie transformersami ,nie python kody. python kody bedą tradlers_helper ,
```

## Zakres odpowiedzi (czego ta baza ma uczyć agentów)

- jak liczyć realną marżę i kiedy odpuścić okazję (arbitraż, sourcing),
- gdzie szukać tanich źródeł i jakimi narzędziami skanować okazje,
- jak budować/diagnozować lejek sprzedażowy B2C i B2B,
- jak projektować cenniki progowe i oferty B2B (Net 30/60/90, rabaty),
- jak bezpiecznie wdrażać boty AI (regulacje Meta/WhatsApp 2026, self-hosting/RODO),
- jak odzyskiwać porzucone koszyki i robić cross-sell,
- jak monitorować konkurencję i repricing.

## Ważne

- To jest **warstwa wiedzy + specyfikacja**, NIE gotowa aplikacja — wymaga podłączenia do silnika RAG (embedding + vector store) i runtime'u agentów.
- Workerzy są projektowani jako osobne agenty-modely AI z cienką warstwą helperów, nie jako jeden duży plik kodu.
- Kolekcja wektorowa MUSI być oddzielna od kolekcji klienckich (np. `bonzo_private_strategy` ≠ kolekcje SklepGPT). Zero mieszania.
- Każdy chunk ma frontmatter z `tags` i `target_workers` — to jest klucz routingu dla orkiestratora.
- Pełny kontekst/uzasadnienie poszczególnych twierdzeń → zawsze sprawdzaj `raw/PRYWATNA_BAZA_RAG_AGENCI_HANDLOWI.md` (Część C — uwagi wdrożeniowe RAG).
Niech agenci mają własne foldery i bazy ,nic duzego,zadnych wielkich plików kodu,wszytko modółowe i łatwe do przerónienia rozwoju
