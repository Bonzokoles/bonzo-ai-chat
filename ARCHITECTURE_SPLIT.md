# BUCH Architecture Split

## Cel

Rozbić system maksymalnie mocno, bez mieszania prywatnej pomocy operacyjnej, runtime lokalnego i przyszłych agentów dealowych.

## Zasada główna

Jeden problem = jeden moduł.

Nie budujemy:

- jednego wielkiego promptu
- jednego wielkiego runtime
- jednego wielkiego pliku orkiestracji
- jednego wspólnego "mózgu" dla sklepu, strategii, B2B i agentów

Budujemy:

- małe moduły
- małe profile
- małe helpery
- osobne tory wiedzy
- osobne punkty wejścia

## Podział odpowiedzialności

### 1. BUCH

Rola:

- lokalny operator
- główny chat
- terminal
- pliki
- konfiguracja
- kontrola i diagnostyka

Nie powinien:

- być od razu pełnym orkiestratorem Polaczków
- zawierać całej strategii dealowej w głównym promptcie
- robić za monolit biznesowo-agentowy

### 2. PINKY_one

Rola:

- prywatna pomoc operacyjna
- sklep
- Shopify
- panel
- konfiguracja
- checklisty
- FAQ

Tryb runtime:

- profil `private_help`
- wiedza operacyjna
- bez mieszania z agentami handlowymi
- osobne endpointy:
  - `/api/private-help/info`
  - `/api/private-help/context`
  - `/api/private-help/chat`

### 3. the_deal_BOYS

Rola:

- sourcing
- marże
- B2B
- lejki
- automatyzacja handlowa
- orkiestrator i Polaczki

Tryb runtime:

- profil `deal_ops`
- osobny subsystem
- docelowo osobny runtime orkiestratora

Nie powinno być:

- wpychane do głównego promptu BUCH
- mieszane z codzienną pomocą operacyjną

## Docelowa kolejność wdrożenia

### Etap 1 — BUCH jako stabilny operator

- lokalny chat
- terminal
- task profiles
- wiedza z `knowledge_mood`
- diagnostyka modeli i routingu

### Etap 2 — twarde rozdzielenie logiki

- `private_help` jako tor operacyjny
- `deal_ops` jako tor strategiczny
- osobne reguły odpowiedzi
- osobne helpery, jeśli potrzebne

### Etap 3 — osobny orchestrator dla deali

- osobny runtime dla `czhatbot_orkiestrator`
- osobne wywołania workerów
- osobny config
- osobny lifecycle

Stan przejściowy:

- `the_deal_BOYS` ma już osobny mini-loader backendowy
- ma osobne endpointy:
  - `/api/deal-ops/info`
  - `/api/deal-ops/context`
  - `/api/deal-ops/chat`
- to nadal nie jest pełny runtime Polaczków, ale przestało być zwykłym ogólnym webhookiem BUCH

### Etap 4 — osobne workery

- `Polaczek_zlotowa_01`
- `Polaczek_Bulka_01`
- `Polaczek_cwaniaczek_01`
- `Polaczek_Bohdan_01`
- `Polaczek_Krzysiu_01`

Każdy jako:

- mały moduł
- mały prompt/spec
- mały zakres danych
- bez wielkiego wspólnego kodu

## Reguły implementacyjne

- nie dodawać dużych plików orkiestracji do `backend/app/main.py`
- nie mieszać `PINKY_one` i `the_deal_BOYS` w jednym promptcie bazowym
- helpery mają być cienkie
- kod agentowy ma być modularny i łatwy do przenoszenia
- jeśli coś jest tylko specyfikacją, nie udawać gotowego runtime

## Co jest już zrobione

- `BUCH` ma aktywny runtime lokalny
- `knowledge_mood` jest aktywną bazą wiedzy
- `PINKY_one` i `the_deal_BOYS` są jawnie rozdzielone
- `private_help` i `deal_ops` są wprowadzone jako osobne profile zadaniowe
- `PINKY_one` ma własny mini-loader backendowy i osobne wejścia API
- `the_deal_BOYS` ma własny mini-loader backendowy i osobne wejścia API

## Najbliższy sensowny ruch

Nie pisać jeszcze wielkiej orkiestracji agentów.

Najpierw:

1. utrzymać prostego `BUCH`
2. dopiąć lepsze filtrowanie wiedzy per profil
3. dopiero potem budować osobny runtime `the_deal_BOYS/app`
