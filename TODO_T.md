# The_Buch - TODO

## Zrobione

- odseparowano pliki nieaktywne do `the_CLEAN_east_WOOD/NOT_in_USE`
- zostawiono aktywne `themes/`
- zostawiono aktywny terminal `xterm.js` + backend PTY
- wyrównano porty robocze do `4149`
- ustawiono aktywny kierunek wiedzy na `knowledge_mood/`
- uporządkowano README do realnego stanu projektu
- rozdzielono kierunki runtime na `private_help` i `deal_ops` jako osobne profile BUCH

## Przed pierwszym uruchomieniem

- przejrzeć `.env` w katalogu głównym i w `backend/`
- sprawdzić, czy `backend/venv` ma komplet zależności
- potwierdzić, czy `The_brain/` ma zostać w całości czy wymaga późniejszego cięcia
- zdecydować, czy `knowledge_mood/the_deal_BOYS` ma być tylko RAG, czy też bazą pod osobny tryb orkiestratora

## Kierunek architektury

- `BUCH` zostaje głównym lokalnym operatorem
- `PINKY_one` zostaje torem prywatnej pomocy operacyjnej
- `the_deal_BOYS` idzie w osobny subsystem strategii i agentów
- zero mieszania wszystkiego do jednego promptu i jednego wielkiego runtime
- osobny opis granic i kolejności wdrożenia jest w `ARCHITECTURE_SPLIT.md`

## Po pierwszym uruchomieniu

- potwierdzić, że `GET /api/health` odpowiada
- potwierdzić, że terminal działa przez `/ws/terminal`
- sprawdzić ładowanie modeli i KB
- sprawdzić TTS i memory

## Nie ruszać bez potrzeby

- `start.bat`
- `backend/venv`
- `backend/app/main.py`
- `themes/`
- `Icons33eeewwee/`
