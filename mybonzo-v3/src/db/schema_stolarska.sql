-- Schemat D1 dla modulu Stolarnia AMS / PRO100 Hub
-- Kompatybilny z Cloudflare D1 (SQLite)

CREATE TABLE IF NOT EXISTS stolar_projekty (
  id              TEXT PRIMARY KEY,
  nazwa           TEXT NOT NULL,
  klient          TEXT,
  status          TEXT DEFAULT 'nowy',
  data_utworzenia TEXT NOT NULL,
  data_start      TEXT,
  data_koniec     TEXT,
  termin_klienta  TEXT,
  pro100_plik     TEXT,
  pro100_data     TEXT,
  wycena_klienta  REAL DEFAULT 0,
  zaliczka        REAL DEFAULT 0,
  notatki         TEXT,
  created_at      TEXT DEFAULT (datetime('now')),
  updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stolar_koszty (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  projekt_id    TEXT NOT NULL REFERENCES stolar_projekty(id),
  kategoria     TEXT NOT NULL,
  nazwa         TEXT NOT NULL,
  jednostka     TEXT,
  ilosc         REAL DEFAULT 1,
  cena_jedn     REAL DEFAULT 0,
  wartosc       REAL GENERATED ALWAYS AS (ilosc * cena_jedn) STORED,
  faktura_nr    TEXT,
  data_kosztu   TEXT,
  notatki       TEXT,
  created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stolar_faktury_sprzedaz (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  projekt_id       TEXT NOT NULL REFERENCES stolar_projekty(id),
  numer            TEXT,
  typ              TEXT,
  kwota_netto      REAL DEFAULT 0,
  kwota_brutto     REAL DEFAULT 0,
  vat_proc         REAL DEFAULT 23,
  data_wystawienia TEXT,
  data_platnosci   TEXT,
  data_oplacenia   TEXT,
  status           TEXT DEFAULT 'oczekuje',
  created_at       TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stolar_czas_pracy (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  projekt_id    TEXT NOT NULL REFERENCES stolar_projekty(id),
  pracownik     TEXT,
  data          TEXT NOT NULL,
  godziny       REAL NOT NULL,
  stawka_godz   REAL DEFAULT 80,
  opis          TEXT,
  created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stolar_insights (
  id                   INTEGER PRIMARY KEY AUTOINCREMENT,
  projekt_id           TEXT REFERENCES stolar_projekty(id),
  task_id              TEXT UNIQUE,
  package_type         TEXT DEFAULT '_04',
  domain               TEXT DEFAULT 'stolarska',
  confidence           REAL,
  insights_json        TEXT,
  recommendations_json TEXT,
  dashboard_hints_json TEXT,
  created_at           TEXT DEFAULT (datetime('now'))
);

CREATE VIEW IF NOT EXISTS v_stolar_projekt_kpis AS
SELECT
  p.id,
  p.nazwa,
  p.klient,
  p.status,
  p.wycena_klienta,
  p.zaliczka,
  p.termin_klienta,
  p.pro100_plik,
  COALESCE((SELECT SUM(k.wartosc) FROM stolar_koszty k WHERE k.projekt_id = p.id), 0) AS koszty_materialow,
  COALESCE((SELECT SUM(cp.godziny * cp.stawka_godz) FROM stolar_czas_pracy cp WHERE cp.projekt_id = p.id), 0) AS koszty_robocizny,
  COALESCE((SELECT SUM(fs.kwota_netto) FROM stolar_faktury_sprzedaz fs WHERE fs.projekt_id = p.id AND fs.status = 'oplacona'), 0) AS wplywy,
  p.wycena_klienta
    - COALESCE((SELECT SUM(k.wartosc) FROM stolar_koszty k WHERE k.projekt_id = p.id), 0)
    - COALESCE((SELECT SUM(cp.godziny * cp.stawka_godz) FROM stolar_czas_pracy cp WHERE cp.projekt_id = p.id), 0)
    AS zysk_brutto,
  CASE
    WHEN p.wycena_klienta > 0 THEN ROUND(
      (p.wycena_klienta
        - COALESCE((SELECT SUM(k.wartosc) FROM stolar_koszty k WHERE k.projekt_id = p.id), 0)
        - COALESCE((SELECT SUM(cp.godziny * cp.stawka_godz) FROM stolar_czas_pracy cp WHERE cp.projekt_id = p.id), 0)
      ) / p.wycena_klienta * 100, 1)
    ELSE 0
  END AS marza_proc
FROM stolar_projekty p;
