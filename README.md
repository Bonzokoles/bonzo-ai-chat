# The_Buch

Lokalna aplikacja `EastWood Ops` do pracy prywatnej i operacyjnej. To nie jest już projekt Astro, Electron ani Cloudflare Pages. Aktualny runtime to statyczny frontend plus backend FastAPI uruchamiany lokalnie.

## Aktualny model działania

- frontend: [index.html](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/index.html) + [app.js](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/app.js)
- backend: [backend/app/main.py](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/backend/app/main.py)
- port lokalny: `4149`
- terminal w UI: `xterm.js` + websocket `/ws/terminal`
- Python runtime: `backend/venv/Scripts/python.exe`

## Co jest krytyczne

- `start.bat` uruchamia backend na `4149` i otwiera frontend
- `backend/venv` musi istnieć, bo launcher korzysta z lokalnego Pythona
- `themes/` musi zostać, bo frontend ładuje motywy dynamicznie
- `Icons33eeewwee/` musi zostać, bo backend serwuje faviconę i ikonę aplikacji
- `knowledge_mood/` to aktywna baza wiedzy dla aplikacji
- `knowledge_base/` jest wyłączone z tych prac i zostaje dla osobnego procesu
- `The_brain/` zostaje jako zasób wiedzy i danych historycznych, dopóki nie potwierdzimy pełnego zakresu użycia

## Bieżąca struktura

```text
The_Buch/
|- backend/
|  |- app/
|  |- venv/
|- knowledge_mood/
|  |- PINKY_one/
|  |- the_deal_BOYS/
|- The_brain/
|- themes/
|- Icons33eeewwee/
|- index.html
|- app.js
|- start.bat
|- launch-jimbo.cmd
|- run-jimbo-always.cmd
|- jimbo-cli.py
|- jimbo-cli.cmd
|- .env
```

## Launchery

- `start.bat` - glowny start lokalny
- `launch-jimbo.cmd` - cienki wrapper do `start.bat`
- `run-jimbo-always.cmd` - wariant autostartu z logowaniem i opoznieniem po starcie systemu
- `jimbo-cli.cmd` / `jimbo-cli.py` - CLI do health, memory, research i decyzji

## Baza wiedzy

Aktywnie przygotowana wiedza prywatna jest teraz w:

- [knowledge_mood/PINKY_one](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/knowledge_mood/PINKY_one)
- [knowledge_mood/the_deal_BOYS](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/knowledge_mood/the_deal_BOYS)

`PINKY_one` odpowiada za prywatną wiedzę operacyjną sklepu i platformy.
`the_deal_BOYS` odpowiada za prywatną wiedzę strategiczną B2B, sourcing i agentów handlowych.

`PINKY_one` ma już własne wejścia backendowe:

- `/api/private-help/info`
- `/api/private-help/context`
- `/api/private-help/chat`

To jest mały osobny tor operacyjny. Nie miesza się z torem strategicznym `the_deal_BOYS`.

`the_deal_BOYS` ma już własne wejścia backendowe:

- `/api/deal-ops/info`
- `/api/deal-ops/context`
- `/api/deal-ops/chat`

To jest mały osobny tor strategiczny. Nie miesza się z głównym webhookiem `BUCH`.

## Granice systemu

`BUCH` ma zostać prosty i główny:

- `BUCH` = operator lokalny, chat, terminal, pliki, ustawienia, codzienna robota
- `PINKY_one` = prywatna pomoc operacyjna sklepu i platformy
- `the_deal_BOYS` = osobny tor strategiczny: sourcing, marże, B2B, Polaczki i orkiestrator

To ma być rozdzielone możliwie mocno:

- bez mieszania promptów w jeden wielki system
- bez jednego wielkiego runtime dla wszystkiego
- bez monolitu agentowego w `backend/app/main.py`

Docelowy kierunek jest opisany w:

- [ARCHITECTURE_SPLIT.md](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/36_chambers/The_Buch/ARCHITECTURE_SPLIT.md)

## Co zostało odsunięte

Rzeczy niepotrzebne do obecnego runtime zostały przeniesione do:

- [NOT_in_USE](S:/BONZO_I_DO_SHELL_SHOP/the_CLEAN_east_WOOD/NOT_in_USE)

Są tam między innymi:

- stare szablony workspace
- stare artefakty `.omx`, `.astro`, `.wrangler`, `.vscode`
- stare UI i eksperymentalne launchery
- testowe logi i pliki po starych portach `4433/4444`

## Stan na teraz

- aplikacja jest przygotowana do pierwszego kontrolowanego uruchomienia
- dokumentacja została wyrównana do aktualnego układu
- nic nie było uruchamiane w ramach tego etapu porządków
