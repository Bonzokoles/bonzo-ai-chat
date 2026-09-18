# Polaczki_workers — specyfikacje workerów

**Status: PRYWATNE.** Flota wyspecjalizowanych agentów wywoływanych przez `czhatbot_orkiestrator`. Każdy ma ograniczony dostęp do RAG wg tagów w `rag/manifest.md`, a wykonanie zawsze wymaga decyzji Bonzo.

## Zasada ogólna

- to mają być agenty-modely AI, nie wielkie pythonowe monolity
- kod pomocniczy ma być tylko cienką warstwą helperów i routingu
- każdy worker ma mieć własną, małą odpowiedzialność i prosty zakres danych
- żaden worker nie działa samodzielnie na pieniądzach, cenach ani kanałach kontaktu

## 1. Polaczek_zlotowa_01

Rola: łowca okazji, promocji i potencjalnych deali.

- **Wejście**: link/opis produktu, cena źródłowa, kanał sprzedaży docelowy
- **Logika rdzenia**: sprawdza kategorię, źródło, rentowność i podstawowy kontekst rynku przed zakupem
- **Wyjście**: rekomendacja kup/nie kup + marża netto + szybkie uzasadnienie
- **Wiedza RAG**: `chunk_01`, `chunk_02`, `chunk_03`, `chunk_04`
- **Ryzyko**: błędny koszt całkowity rozwala ocenę marży

## 2. Polaczek_Bulka_01

Rola: sprawdza, czy deal ma sens, czy jest klient i czy warto wystawić go tymczasowo na stronę.

- **Wejście**: produkt, cena, grupa docelowa, kanał sprzedaży, dane o ruchu/sklepie
- **Logika rdzenia**: łączy ocenę okazji z prostą diagnozą lejka i sensowności ekspozycji
- **Wyjście**: werdykt czy publikować, jak opisać i gdzie szukać klienta
- **Wiedza RAG**: `chunk_03`, `chunk_05`, `chunk_09`, opcjonalnie `chunk_14`
- **Ryzyko**: zła ocena popytu przy zbyt małej ilości danych

## 3. Polaczek_cwaniaczek_01

Rola: sprzedawca. Ma zwiększać szansę sprzedaży bez wciskania kitu.

- **Wejście**: oferta, grupa docelowa, etap klienta, cena, przewagi produktu
- **Logika rdzenia**: dobiera argumentację, cross-sell, odzysk koszyka, sekwencję follow-up
- **Wyjście**: gotowa propozycja komunikatu, sekwencji lub planu sprzedażowego
- **Wiedza RAG**: `chunk_10`, `chunk_14`, przy komunikatorach zawsze też `chunk_11`
- **Ryzyko**: wejście w zbyt agresywną sprzedaż albo kanał niezgodny z compliance

## 4. Polaczek_Bohdan_01

Rola: ochrona i porządek. Pilnuje ryzyk, regulacji i zbyt nachalnych automatyzacji.

- **Wejście**: plan automatyzacji, opis działań bota, kanał komunikacji, zakres danych
- **Logika rdzenia**: sprawdza, czy plan nie łamie zasad, czy nie idzie za ostro i czy nie miesza danych prywatnych z publicznymi
- **Wyjście**: zielone światło / ostrzeżenie / blokada + powód
- **Wiedza RAG**: `chunk_11`, `chunk_12`, `chunk_13`
- **Ryzyko**: zbyt miękka walidacja przy integracjach z komunikatorami

## 5. Polaczek_Krzysiu_01

Rola: biznes i B2B. Rozmowy handlowe, wymiana towarów, cenniki, warunki i pilnowanie żeby nie schodzić na minus.

- **Wejście**: produkt, cena bazowa, typ klienta, wolumen, warunki płatności, cel negocjacji
- **Logika rdzenia**: buduje ofertę B2B, progi cenowe, warunki Net 30/60/90 i sprawdza czy układ nadal jest opłacalny
- **Wyjście**: propozycja cennika/oferty/kontrargumentów + granice negocjacyjne
- **Wiedza RAG**: `chunk_06`, `chunk_07`, `chunk_08`, pomocniczo `chunk_01`
- **Ryzyko**: zejście z ceną za nisko bez spięcia z marżą źródłową

## Reguła wspólna

Każdy worker diagnozuje i rekomenduje. Decyzję wykonawczą podejmuje `czhatbot_orkiestrator` razem z Bonzo.
