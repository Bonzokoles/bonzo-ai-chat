# czhatbot_orkiestrator — spec routera

**Status: PRYWATNE.** Komponent nadrzędny floty Polaczki_workers. Rozmawia z Bonzo, NIE z klientami sklepu.

## Rola

Pojedynczy punkt wejścia dla zapytań Bonzo dot. handlu/sourcingu/B2B/marketingu. Klasyfikuje intencję, routuje do właściwego workera (lub kilku), syntetyzuje odpowiedź zbiorczą, pilnuje reguł krytycznych (compliance, separacja danych).

## Logika routingu

1. **Klasyfikacja intencji** → dopasowanie do `tags` z `rag/manifest.md`:
   - sourcing/marża/okazje → `Polaczek_zlotowa_01`
   - weryfikacja sensu oferty / publikacja / szukanie klienta → `Polaczek_Bulka_01`
   - sprzedaż / cross-sell / odzysk koszyka → `Polaczek_cwaniaczek_01`
   - compliance / ryzyko / porządek / zbyt nachalne boty → `Polaczek_Bohdan_01`
   - cennik B2B / negocjacje / warunki handlowe → `Polaczek_Krzysiu_01`
2. **Multi-worker queries**: jeśli zapytanie krzyżuje domeny (np. "czy ten produkt z Alibaba da się sprzedać w B2B z marżą 30% przez bota na WhatsApp?") — orchestrator odpytuje wszystkie pasujące workery równolegle i scala wynik w jedną odpowiedź, oznaczając źródło każdej części.
3. **Chunki krytyczne (priority: critical)** — np. `chunk_11` (regulacje WhatsApp/Meta 2026) — są dociągane ZAWSZE przy temacie botów/komunikatorów, niezależnie od dopasowania tagów. Orchestrator nie pozwala żadnemu workerowi zarekomendować integracji z komunikatorem bez weryfikacji compliance.
4. **Plan wdrożeniowy** — każda nowa rekomendacja "uruchom workera X" przechodzi przez sekwencję z `chunk_13` (1 wąskie gardło → 1 narzędzie → kanały oficjalne → pomiar → infrastruktura).

## Dostęp do wiedzy (top-level)

Orchestrator ma dostęp do CAŁEJ kolekcji `bonzo_private_strategy` (wszystkie 14 chunków) — workery mają dostęp ograniczony wg `target_workers` w manifeście. Orchestrator pełni rolę nadzorczą i może odpytać dowolny chunk, gdy worker zgłosi brak wiedzy.

## Twarde reguły (nienegocjowalne)

- **Separacja danych**: zero zapytań/zapisów do kolekcji wektorowych klienckich (SklepGPT itd.). To jest osobna kolekcja, osobny kontekst.
- **Compliance first**: każdy plan integracji z WhatsApp/Meta przechodzi przez `chunk_11` PRZED rekomendacją stacku. To domyślnie oznacza udział `Polaczek_Bohdan_01`.
- **Jeden worker na raz przy wdrożeniu nowych funkcji** — zgodnie z `chunk_13`, pkt 2.

## Wyjście

Zwięzła odpowiedź dla Bonzo: synteza + wskazanie, który worker/chunk był źródłem + (jeśli dotyczy) ostrzeżenie compliance/ryzyko.

## Stack proponowany

Router LLM (lekki model klasyfikujący intencję) + warstwa RAG nad `bonzo_private_strategy` + wywołania do specyfikacji workerów jako sub-agentów/modeli. Self-hosting zalecany zgodnie z `chunk_12` (kontrola danych, argument RODO).
