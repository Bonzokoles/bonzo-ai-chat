# PRYWATNA baza wiedzy RAG + specyfikacja agentów handlowych (Bonzo-only)
**Data:** 2026-06-07 | **Status:** PRYWATNE — wyłącznie do Twojego użytku, NIE wgrywać do botów klienckich (SklepGPT itd.)
**Źródło danych:** `_RESEARCH/RESEARCH_ECOMMERCE_SPRZEDAZ_B2B_BOTY_2026.md`, sekcja 6 + powiązane fakty z sekcji 1-5
**Cel:** (A) gotowe chunk'i pod system RAG do Twojego osobistego asystenta strategicznego, (B) specyfikacje kilku małych agentów sklepowo-kupująco-sprzedających, które możesz zacząć budować

---

# CZĘŚĆ A — CHUNK'I RAG (gotowe do embeddingu)

Każdy blok to samodzielna, atomowa jednostka wiedzy — tak skonstruowana, żeby dobrze działała jako pojedynczy fragment w wektorowej bazie (jedna idea = jeden chunk, z tagami do filtrowania).

---
**[CHUNK 01] — Mini-marża: realistyczne liczby**
TAGI: `arbitraż` `marża` `sourcing` `decyzja-biznesowa`

W modelu arbitrażu/mini-marży realistyczne oczekiwanie to **20-50% marży**, sporadyczne skoki >100% na szybko rotujących produktach (rzadkość, nie norma). To gra na WOLUMENIE, nie na wartości jednostkowej. 58% nowych sprzedawców Amazon osiąga rentowność w pierwszym roku — niski próg wejścia. Ponad 25% sprzedawców Amazon korzysta z arbitrażu — model sprawdzony, ale konkurencja rośnie z każdym rokiem (baza aktywnych sprzedawców: 2-2,5 mln).

DECYZJA: jeśli liczysz opłacalność produktu i wychodzi <15% marży po doliczeniu prowizji/wysyłki/podatku — odpuść, to sygnał złego sourcingu, nie "da się nadgonić wolumenem".

---
**[CHUNK 02] — Gdzie szukać tanich źródeł (konkretna lista operacyjna)**
TAGI: `sourcing` `dostawcy` `arbitraż`

Kanały online: eBay (presja cenowa od sprzedawców 3.), Alibaba (zakupy hurtowe B2B od producentów), AliExpress (małe ilości, zamówienia testowe), Walmart (wyprzedaże/promocje), **Amazon-to-Amazon** (kupno przecenionych i odsprzedaż na innym rynku — UK/Włochy), Etsy (produkty unikalne z premią), serwisy rabatowe (Groupon, Slickdeals, RetailMeNot).
Kanały stacjonarne: dyskonty z dużą przeceną (typu TJ Maxx), promocje w supermarketach/drogeriach, **sklepy likwidacyjne** (opisane wprost jako "żyła złota" — końcówki serii, nadwyżki), outlety fabryczne.

NARZĘDZIA do porównywania cen: Google Shopping, Keepa, CamelCamelCamel.
NARZĘDZIA do skanowania produktów: Scoutify, SellerAmp SAS, Amazon Seller App (sprawdzają rangę/cenę/uprawnienia w czasie rzeczywistym).

---
**[CHUNK 03] — Proces zakupu→sprzedaży krok po kroku (do zaprogramowania jako workflow agenta)**
TAGI: `arbitraż` `proces` `automatyzacja` `agent-sourcing`

1. Konto sprzedawcy — wybór FBA (magazyn/wysyłka po stronie platformy) vs. FBM (sam przechowujesz/wysyłasz)
2. Sprawdzenie kategorii zastrzeżonych (gated) — błąd tutaj = szybki ban konta
3. Szukanie okazji (priorytet: sekcje wyprzedażowe, likwidacje)
4. Skan narzędziem (ranga sprzedaży, cena, uprawnienia)
5. **Zawsze policz rentowność kalkulatorem PRZED zakupem** — uwzględnij prowizję platformy + wysyłkę + podatek
6. Analiza konkurencji: kto ma Buy Box, ranking, poziom nasycenia
7. Wystawienie + oznaczenie + wysyłka
8. Monitoring + repricing (AI repricer dostosowujący cenę do konkurencji w czasie rzeczywistym)

To jest gotowy szkielet pętli decyzyjnej dla **Agenta Skanera Okazji** (patrz Część B, Agent 1).

---
**[CHUNK 04] — Porównanie modeli biznesowych sprzedaży online**
TAGI: `strategia` `model-biznesowy` `decyzja`

| Model | Inwestycja | Marże | Kontrola nad produktem | Skalowalność | Czas startu |
|---|---|---|---|---|---|
| Arbitraż detaliczny | Niska | 20-50% | Brak | Ograniczona | Bardzo szybki |
| Hurt (wholesale) | Wysoka | Umiarkowane-wysokie | Ograniczona | Umiarkowana | Średni |
| Marka własna (private label) | Wysoka | Wysokie (po zbudowaniu marki) | Pełna | Wysoka | Wolny |
| Dropshipping | Bardzo niska | Niskie-umiarkowane | Brak | Wysoka (przy dobrych dostawcach) | Szybki |

ZASTOSOWANIE: arbitraż = dobry test rynku małym kosztem / model na "zarobić od razu". Private label = długoterminowa budowa wartości, ale wymaga kapitału i czasu. Wybór zależy od tego, czy grasz pod gotówkę "teraz" czy pod aktywo "za rok".

---
**[CHUNK 05] — Lejek B2C: gdzie szukać "wycieku" w sprzedaży**
TAGI: `lejek` `konwersja` `diagnoza` `funnel`

5 warstw: Awareness (świadomość) → Discover (odkrycie) → Consideration (rozważanie) → Conversion (konwersja) → Retention (utrzymanie). Każda warstwa ma inny cel i inną metrykę:
- Awareness: maks. zasięg → CTR/CPC/CPM
- Discover: obniżyć bounce rate → wyświetlenia stron produktowych, koszt wizyty
- Consideration: zbudować zaufanie → czas na stronie, dodania do koszyka
- Conversion: usunąć bariery płatności → conversion rate, cart abandonment, AOV
- Retention: zwiększyć LTV → retention rate, CAC:LTV ratio

ZASADA DIAGNOSTYCZNA: "ruch wysoki, sprzedaż niska" = wyciek w środku/dole lejka (zaufanie, UI, checkout), NIE problem z zasięgiem. Mierz każdą warstwę osobno, żeby zlokalizować dokładnie gdzie tracisz klientów — nie "ulepszaj wszystko naraz".

---
**[CHUNK 06] — Lejek B2B: jak dziś kupują firmy**
TAGI: `b2b` `lejek` `sprzedaż` `funnel`

69% procesu zakupowego B2B kończy się, zanim klient skontaktuje się ze sprzedawcą ("rep-free buying"). Kupujący konsumują średnio **13 treści przed zakupem** (8 od dostawcy + 5 zewnętrznych). Średnia konwersja B2B = 1,8% (najlepsi osiągają 311% więcej niż przeciętni — różnica robi konkretny proces, nie szczęście).

5 etapów: Awareness (treści edukacyjne) → Consideration (porównania, case studies) → Evaluation (dokumentacja, certyfikaty) → Decision (cennik, umowy) → Retention (wsparcie, ekspansja).

ZASTOSOWANIE: jeśli sprzedajesz B2B (np. licencje SaaS, usługi dla sklepów IdoSell) — potrzebujesz biblioteki materiałów na KAŻDY etap, nie tylko strony produktowej. Brak treści na etapie "Evaluation" (dokumentacja API, dowody bezpieczeństwa) to typowy powód, dla którego duzi klienci odpadają mimo zainteresowania.

---
**[CHUNK 07] — Skala i mechanika rynku B2B (kontekst strategiczny do decyzji "czy wchodzić w B2B")**
TAGI: `b2b` `rynek` `statystyki` `decyzja`

Globalny rynek B2B e-commerce: $32,1 bln (2025) → $62,2 bln (2030), CAGR 14,5%. B2B jest **5x większy niż B2C**. 90% kupujących B2B przełączy dostawcę dla lepszego doświadczenia cyfrowego. 87% zapłaci więcej za świetny portal zakupowy. 65% transakcji B2B wymaga etapu negocjacji (zapytanie→oferta→negocjacja→zamówienie).

Marketplace'y trzymają 65% udziału w rynku B2B (rosną 18%/rok); Amazon Business = 6 mln klientów biznesowych.

DECYZJA: B2B to ogromny, niedoceniany rynek — ale wymaga innej infrastruktury (cenniki progowe, konta wieloosobowe, terminy płatności Net 30/60/90). To NIE jest "ten sam sklep z wyższymi cenami" — to inny produkt.

---
**[CHUNK 08] — Modele cenowe B2B (do zaimplementowania, jeśli wchodzisz w hurt)**
TAGI: `b2b` `cennik` `pricing` `wdrożenie`

| Model | Opis | Kiedy |
|---|---|---|
| Rabat globalny | Cena standard − % rabatu klienta | Proste hurtownie |
| Progowy (tiered) | Cena spada przy progach ilości | Produkty komodytyzowane |
| Indywidualny | Unikalna cena per klient | Długie relacje, kontrakty |
| Na zapytanie (quote) | Brak cennika, oferta na żądanie | Produkty niestandardowe |

Przykładowa drabinka progowa: 1-99 szt = 12,50$ → 100-499 = -14% → 500-999 = -26% → 1000-4999 = -36% → 5000+ = wycena indywidualna. Kontrakt roczny = dodatkowe -8%.

PŁATNOŚCI: większość rozliczeń na termin (Net 30/60/90), rabat za wczesną płatność typu "2/10 Net 30". Dwie trzecie kupujących porzuci zakup, jeśli nie znajdzie preferowanej formy płatności na termin.

---
**[CHUNK 09] — Checklist budowy sklepu od zera (skondensowana operacyjnie)**
TAGI: `sklep` `setup` `checklist` `operacje`

Kolejność krytyczna: (1) walidacja produktu z realnymi ludźmi PRZED inwestycją, (2) wybór modelu zaopatrzenia (zapasy / dropshipping / produkcja na żądanie / subskrypcja), (3) forma prawna, (4) **pełny rachunek kosztów** (SSL, hosting, domena, prowizje płatnicze, magazyn, wysyłka, opakowania — nie tylko "cena produktu"), (5) struktura kategorii/SKU, (6) opisy z SEO i CTA, (7) social proof (recenzje, UGC), (8) polityki (zwroty, prywatność, regulamin, bezpieczeństwo), (9) płatności — **30% porzuca zakup przy konieczności ponownego wpisania karty, 25% przy ponownym adresie** → 1-click checkout to wymóg konwersyjny, nie dodatek, (10) test pełnej ścieżki przed startem, (11) promocja: e-mail (3x wyższa konwersja niż social wg Forbes), SEO, social, marketplace'y, programy lojalnościowe.

---
**[CHUNK 10] — Boty AI w e-commerce: 3 kategorie + co naprawdę działa**
TAGI: `ai` `automatyzacja` `boty` `narzędzia`

1. **Wsparcie**: automatyzacja obsługuje 30-50% powtarzalnych kontaktów (Gorgias, Zendesk, Tidio, Siena — do 80% ticketów u niektórych)
2. **Sprzedaż**: personalizacja AI podnosi przychód nawet o 40% (Nosto, Algolia, Rebuy); automatyczne sekwencje e-mail generują 41% przychodu z e-maili przy 5,3% wysyłek (Klaviyo)
3. **Automatyzacja rutyny**: kampanie, odzyskiwanie koszyków, synchro danych, faktury, wykrywanie oszustw (n8n — może być self-hosted na VPS bez limitów wykonań, Make, Zapier)

Ruch generowany przez AI wzrósł o 4700% (2024→2025) — coraz więcej klientów odkrywa produkty rozmawiając z asystentem zamiast szukać w wyszukiwarce.

---
**[CHUNK 11] — KRYTYCZNE: regulacje WhatsApp/Meta 2026 (ryzyko prawne dla każdego bota)**
TAGI: `regulacje` `ryzyko` `whatsapp` `compliance` `2026`

Od stycznia 2026 Meta **zakazuje generycznych/niecertyfikowanych botów AI w oficjalnym WhatsApp Business API**. Sklep używający nieoficjalnego bota ryzykuje **zablokowanie numeru telefonu**. Zasada twarda: integracje wyłącznie z platformami certyfikowanymi przez Meta — żadnych "szybkich" obejść przez nieoficjalne API.

ZASTOSOWANIE: przy projektowaniu KAŻDEGO nowego bota komunikującego się przez WhatsApp — to pierwszy punkt audytu, przed wyborem stacka technicznego.

---
**[CHUNK 12] — Self-hosting AI = przewaga, nie tylko koszt**
TAGI: `infrastruktura` `rodo` `self-hosting` `przewaga-konkurencyjna`

W 2026 ok. 59,6% rynku AI w e-commerce to rozwiązania on-premise/self-hosted (napędzane RODO i kontrolą danych). Modele open-source (Llama, Qwen, DeepSeek) hostowane na własnym VPS oznaczają, że dane klientów (historia zakupów, treść rozmów) NIE opuszczają Twojej infrastruktury.

ZASTOSOWANIE: to bezpośrednio pasuje do architektury Railway + własne API, którą już masz (OpisAI/SklepGPT/ContentFactory). To nie jest "techniczny detal" — to ARGUMENT SPRZEDAŻOWY do komunikowania klientom B2B ("Twoje dane nie trafiają do chmury OpenAI/Google") i realna przewaga regulacyjna nad konkurencją opartą na cudzych API.

---
**[CHUNK 13] — 7 błędów wdrożeniowych do unikania + plan 5 kroków**
TAGI: `wdrożenie` `błędy` `plan-działania` `agent-design`

BŁĘDY: (1) nieoficjalny bot na WhatsApp, (2) wdrożenie bez strategii / na "brudnych" danych, (3) zbyt częste wysyłki (spalanie reputacji kanału), (4) oczekiwanie pełnego zastąpienia ludzi, (5) ignorowanie ochrony danych, (6) przepłacanie za enterprise przy małej skali, (7) brak pomiaru wyników.

PLAN 5 KROKÓW (uniwersalny szkielet wdrożenia każdego nowego agenta/bota):
1. Zidentyfikuj WĄSKIE GARDŁO (wsparcie? konwersja? rutyna?)
2. Wybierz JEDNO narzędzie i opanuj je w pełni przed dodaniem kolejnego
3. Łącz się tylko z oficjalnymi/certyfikowanymi kanałami
4. Mierz efekt kilka tygodni, koryguj na podstawie danych
5. Planuj infrastrukturę z wyprzedzeniem (co w chmurze, co self-hosted — koszt vs. prywatność)

---
**[CHUNK 14] — Cross-sell/upselling: mechanika i liczby (z case studies)**
TAGI: `upsell` `cross-sell` `konwersja` `revenue`

Najlepszy moment na cross-sell = **zaraz po zakupie**, w portalu pobierania/na stronie podziękowania — to chwila najwyższej gotowości zakupowej klienta. Konkretny case: grid rekomendacji wbudowany w portal pobierania = **+22% przychodu z cross-sell**. Zasady: transparentność cenowa (zero ukrytych opłat — klient już zapłacił i jest czujny), integracja z jednym kontem, 30-60s wideo-teasery, follow-up mailowy (Klaviyo) po pobraniu.

ZASTOSOWANIE: dotyczy zarówno produktów cyfrowych (Yutro: OpisAI→SklepGPT cross-sell), jak i fizycznych (po dostawie → propozycja komplementarnego produktu).

---

# CZĘŚĆ B — SPECYFIKACJE AGENTÓW (małe, wyspecjalizowane, budowalne pojedynczo)

Zasada nadrzędna z Chunk 13: **buduj i opanuj jednego agenta na raz**. Poniżej kolejność wg rosnącej złożoności (zacznij od Agenta 1).

---

## AGENT 1 — Skaner Okazji + Kalkulator Marży (sourcing/kupujący)
**Po co:** automatycznie wykrywa okazje cenowe i liczy, czy się opłacają, zanim Ty wydasz pieniądze.

| Element | Specyfikacja |
|---|---|
| **Wejście** | Lista monitorowanych produktów/kategorii + lista źródeł (np. Keepa API, scraping wyprzedaży, kanały RSS sklepów likwidacyjnych) |
| **Logika rdzenia** | Pętla z Chunk 03, krok 5: dla każdej okazji licz `cena_docelowa − (cena_zakupu + prowizja_platformy + koszt_wysyłki + podatek)`. Filtruj wyniki <15-20% marży (próg z Chunk 01) |
| **Wyjście** | Alert (Telegram/e-mail/Slack) z: produktem, marżą szacowaną, linkiem do źródła, rekomendacją kup/pomiń |
| **Wiedza RAG (tagi)** | `arbitraż`, `sourcing`, `marża`, `dostawcy` (Chunk 01, 02, 03) |
| **Stack proponowany** | n8n (orkiestracja, self-host na Railway) + Keepa/CamelCamelCamel API + prosty kalkulator w Pythonie |
| **Ryzyko do pilnowania** | kategorie zastrzeżone (gated) — agent MUSI sprawdzać to przed alertem, inaczej generuje fałszywe okazje |

---

## AGENT 2 — Recenzent Cennika B2B / Generator Ofert Progowych
**Po co:** jeśli wejdziesz w sprzedaż hurtową — automatycznie generuje wyceny progowe i pilnuje spójności cennika.

| Element | Specyfikacja |
|---|---|
| **Wejście** | Cennik bazowy + reguły progowe (z Chunk 08) + dane klienta (segment/historia zakupów) |
| **Logika rdzenia** | Dopasowuje klienta do segmentu cenowego → generuje ofertę z drabinką progową → flaguje rozbieżności (np. klient powinien być w wyższym progu, ale nie jest) |
| **Wyjście** | Gotowa oferta PDF/e-mail + log rozbieżności do przeglądu |
| **Wiedza RAG (tagi)** | `b2b`, `cennik`, `pricing` (Chunk 06, 07, 08) |
| **Stack proponowany** | własne API (wzorem OpisAI) + szablon PDF + integracja z kontem klienta |
| **Kiedy budować** | TYLKO jeśli realnie planujesz ofertę B2B — to najbardziej złożony z 5 agentów, zostaw na koniec |

---

## AGENT 3 — Asystent Audytu Lejka (diagnostyczny, dla Twoich własnych sklepów)
**Po co:** regularnie sprawdza Twoje sklepy (Yutro, przyszłe) i wskazuje, w której warstwie lejka tracisz klientów — zamiast Ty ręcznie analizujesz Analytics.

| Element | Specyfikacja |
|---|---|
| **Wejście** | Dane z Google Analytics / Shopify Analytics (ruch, bounce rate, dodania do koszyka, checkout starts, zakupy) |
| **Logika rdzenia** | Mapuje metryki na 5 warstw lejka (Chunk 05) → wykrywa, która warstwa ma anomalny spadek względem poprzedniego okresu → generuje hipotezę przyczyny na podstawie wzorców z bazy wiedzy |
| **Wyjście** | Cotygodniowy raport: "Warstwa X spadła o Y% — prawdopodobna przyczyna: Z (np. brak 1-click checkout, brak social proof)" |
| **Wiedza RAG (tagi)** | `lejek`, `konwersja`, `diagnoza`, `funnel` (Chunk 05, 09) |
| **Stack proponowany** | n8n + GA4 API/Shopify Admin API + LLM do generowania hipotez na podstawie chunków RAG |
| **Wartość dodatkowa** | to jest dokładnie to narzędzie, którego SAM potrzebujesz do Yutro — można uruchomić od razu na istniejącym sklepie |

---

## AGENT 4 — Agent Odzyskiwania Koszyków + Cross-sell
**Po co:** automatyczna sekwencja po porzuconym koszyku i po zakupie — bez ręcznego pisania kampanii za każdym razem.

| Element | Specyfikacja |
|---|---|
| **Wejście** | Webhook "porzucony koszyk" / "zakup zakończony" z Shopify |
| **Logika rdzenia** | (a) Porzucony koszyk → sekwencja 3 wiadomości (1h / 24h / 72h) z rosnącą zachętą (przypomnienie → social proof → mały rabat); (b) Zakup zakończony → grid rekomendacji w portalu/follow-up mailowy (mechanizm z Chunk 14, +22% przychodu w case study) |
| **Wyjście** | Wysłane wiadomości e-mail/WhatsApp (TYLKO przez kanały certyfikowane — patrz Chunk 11!) |
| **Wiedza RAG (tagi)** | `upsell`, `cross-sell`, `konwersja`, `revenue`, `regulacje` (Chunk 14, 11) |
| **Stack proponowany** | Klaviyo (gotowe sekwencje) ALBO własny agent na n8n + certyfikowany WhatsApp Business provider |
| **Uwaga krytyczna** | Sprawdź certyfikację KAŻDEGO providera WhatsApp przed wdrożeniem (Chunk 11) — to jedyny punkt, który może Cię prawnie zablokować |

---

## AGENT 5 — Agent Repricer / Monitor Konkurencji
**Po co:** w modelu arbitrażu/marketplace pilnuje, żeby Twoja cena zawsze była konkurencyjna, ale nie poniżej progu opłacalności.

| Element | Specyfikacja |
|---|---|
| **Wejście** | Lista Twoich aktywnych ofert + monitoring cen konkurencji (Keepa/scraping) |
| **Logika rdzenia** | `nowa_cena = max(próg_opłacalności, cena_konkurencji − mały_margines)` — agent NIGDY nie schodzi poniżej progu z Chunk 01 (15-20% marży) |
| **Wyjście** | Automatyczna aktualizacja ceny + log zmian + alert przy próbie zejścia poniżej progu (wymaga Twojej decyzji ręcznej) |
| **Wiedza RAG (tagi)** | `arbitraż`, `marża`, `model-biznesowy` (Chunk 01, 04) |
| **Stack proponowany** | SELLERLOGIC Repricer (gotowe) ALBO własny skrypt jeśli chcesz pełną kontrolę nad logiką progu |

---

# CZĘŚĆ C — JAK PODŁĄCZYĆ TO DO RAG (uwagi techniczne)

1. **Chunking:** powyższe 14 bloków [CHUNK 01-14] to gotowe jednostki — każdy ma jasny temat, tagi i samodzielną treść (nie wymaga kontekstu sąsiednich bloków). To format idealny pod embedding (np. `text-embedding-3-small` lub lokalny model).
2. **Metadane do filtrowania:** każdy chunk ma TAGI — użyj ich jako metadanych w wektorowej bazie (np. Qdrant/Chroma), żeby agent mógł zawężać wyszukiwanie (np. Agent 1 szuka tylko w `arbitraż`+`sourcing`, Agent 3 tylko w `lejek`+`konwersja`)
3. **Separacja od wiedzy klienckiej:** ten plik i jego embeddingi NIE powinny trafić do tej samej kolekcji wektorowej co `WIEDZA_FINANSOWA_ECOMMERCE_PL.md` czy `TON_I_OSOBOWOSC_CHATBOTA.md` (te są dla SklepGPT = klienci). Rekomendacja: osobna kolekcja np. `bonzo_private_strategy`, dostępna tylko Twoim agentom wewnętrznym.
4. **Aktualizacja:** statystyki rynkowe (B2B $32Tn, marże arbitrażu, regulacje Meta) mają datę ważności — oznacz w metadanych `data_aktualności: 2026-06` i zaplanuj odświeżenie researchu za ~6 miesięcy (rynek AI/regulacje zmieniają się szybko — zwłaszcza Chunk 11).

---
*Plik prywatny — wyodrębniony i przeorganizowany z `_RESEARCH/RESEARCH_ECOMMERCE_SPRZEDAZ_B2B_BOTY_2026.md`, sekcja 6 + powiązane fakty | 2026-06-07*
