"""
MCP (Model Context Protocol) Tools for Local AI Chatbot
========================================================

Implementacja narzędzi MCP umożliwiających lokalnym modelom AI dostęp do:
- Operacji na plikach (czytanie, pisanie, listowanie)
- Wyszukiwania w internecie
- Kalkulatora matematycznego
- Wykonywania kodu Python
- Operacji systemowych

Każde narzędzie ma:
- Nazwę (name)
- Opis (description)
- Funkcję wykonującą (function)
"""

import os
import json
import subprocess
import requests
import inspect
from bs4 import BeautifulSoup
import boto3
from pathlib import Path
from typing import Dict, Any, List, Callable
import math
import re
import sys
from datetime import datetime, timezone

# Knowledge base directory (folder z plikami wiedzy dla modelu)
KB_DIR = Path(os.getenv("KB_DIR", str(Path(__file__).parent.parent.parent / "knowledge_mood")))
KB_DIR.mkdir(parents=True, exist_ok=True)

# Semantic embeddings (loaded in background after startup)
try:
    import embeddings as _embed
    _HAS_EMBEDDINGS = True
except ImportError:
    _HAS_EMBEDDINGS = False


class MCPToolRegistry:
    """Rejestr wszystkich dostępnych narzędzi MCP"""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def register_tool(self, name: str, description: str, function: Callable):
        """Rejestruje nowe narzędzie"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function
        }

    def get_tool(self, name: str) -> Dict[str, Any]:
        """Pobiera narzędzie po nazwie"""
        return self.tools.get(name)

    def list_tools(self) -> List[str]:
        """Lista wszystkich dostępnych narzędzi"""
        return list(self.tools.keys())

    def execute_tool(self, name: str, **kwargs) -> str:
        """Wykonuje narzędzie z podanymi argumentami"""
        tool = self.get_tool(name)
        if not tool:
            return f"❌ Narzędzie '{name}' nie istnieje"

        try:
            result = tool["function"](**kwargs)
            return str(result)
        except Exception as e:
            return f"❌ Błąd wykonania narzędzia '{name}': {str(e)}"

    def _register_default_tools(self):
        """Rejestruje domyślny zestaw narzędzi"""

        # 1. FILE OPERATIONS
        self.register_tool(
            name="read_file",
            description="Czyta zawartość pliku. Args: path (str)",
            function=self._read_file
        )

        self.register_tool(
            name="write_file",
            description="Zapisuje tekst do pliku. Args: path (str), content (str)",
            function=self._write_file
        )

        self.register_tool(
            name="list_directory",
            description="Listuje pliki w katalogu. Args: path (str, default='.')",
            function=self._list_directory
        )

        # 2. WEB SEARCH
        self.register_tool(
            name="web_search",
            description="Wyszukuje informacje w internecie. Args: query (str)",
            function=self._web_search
        )
        self.register_tool(
            name="research_and_fill_kb",
            description="Wyszukuje źródła i zapisuje treści do knowledge_mood/web_research. Args: query (str), max_results (int, optional)",
            function=self._research_and_fill_kb
        )
        self.register_tool(
            name="scrape_to_knowledge_base",
            description="Pobiera URL i zapisuje do knowledge_mood/web. Args: url (str), title (str, optional)",
            function=self._scrape_to_knowledge_base
        )
        self.register_tool(
            name="scrape_to_knowledge_mood",
            description="Pobiera URL i zapisuje do knowledge_mood/web. Args: url (str), title (str, optional)",
            function=self._scrape_to_knowledge_base
        )
        self.register_tool(
            name="tmdb_search_movie",
            description="Wyszukuje filmy w TMDB. Args: query (str), limit (int, optional)",
            function=self._tmdb_search_movie
        )
        self.register_tool(
            name="push_knowledge_to_r2",
            description="Wysyła knowledge_mood do Cloudflare R2. Args: prefix (str, optional)",
            function=self._push_knowledge_to_r2
        )

        # 3. CALCULATOR
        self.register_tool(
            name="calculator",
            description="Wykonuje obliczenia matematyczne. Args: expression (str)",
            function=self._calculator
        )

        # 4. CODE EXECUTION (SANDBOXED)
        self.register_tool(
            name="execute_python",
            description="Wykonuje kod Python w sandboxie. Args: code (str)",
            function=self._execute_python
        )

        # 5. WEATHER
        self.register_tool(
            name="get_weather",
            description="Sprawdza pogodę dla podanej lokalizacji. Args: location (str), lat (float, optional), lon (float, optional)",
            function=self._get_weather
        )

        # 6. NOTES
        self.register_tool(
            name="note_save",
            description="Zapisuje notatkę. Args: title (str), content (str)",
            function=self._note_save
        )
        self.register_tool(
            name="note_read",
            description="Czyta notatkę po tytule. Args: title (str)",
            function=self._note_read
        )
        self.register_tool(
            name="note_list",
            description="Listuje wszystkie notatki",
            function=self._note_list
        )
        self.register_tool(
            name="note_search",
            description="Szuka w notatkach. Args: query (str)",
            function=self._note_search
        )

        # 7. SYSTEM INFO
        self.register_tool(
            name="system_info",
            description="Zwraca informacje systemowe",
            function=self._system_info
        )

        # 8. DATE/TIME
        self.register_tool(
            name="get_datetime",
            description="Zwraca aktualną datę i czas",
            function=self._get_datetime
        )

        # 9. TEXT PROCESSING
        self.register_tool(
            name="count_words",
            description="Liczy słowa w tekście. Args: text (str)",
            function=self._count_words
        )

        # 10. KNOWLEDGE BASE
        self.register_tool(
            name="search_knowledge_base",
            description="Przeszukuje baze wiedzy (folder knowledge_mood). Args: query (str)",
            function=self._search_knowledge_base
        )
        self.register_tool(
            name="search_knowledge_mood",
            description="Przeszukuje baze wiedzy (folder knowledge_mood). Args: query (str)",
            function=self._search_knowledge_base
        )

        self.register_tool(
            name="list_knowledge_base",
            description="Listuje pliki w bazie wiedzy",
            function=self._list_knowledge_base
        )
        self.register_tool(
            name="list_knowledge_mood",
            description="Listuje pliki w bazie wiedzy",
            function=self._list_knowledge_base
        )

        self.register_tool(
            name="read_knowledge_file",
            description="Czyta konkretny plik z bazy wiedzy. Args: filename (str)",
            function=self._read_knowledge_file
        )

    # ========== IMPLEMENTACJE NARZĘDZI ==========

    def _read_file(self, path: str) -> str:
        """Czyta plik"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"📄 Zawartość pliku '{path}':\n{content[:500]}..." if len(content) > 500 else f"📄 Zawartość pliku '{path}':\n{content}"
        except FileNotFoundError:
            return f"❌ Plik '{path}' nie istnieje"
        except Exception as e:
            return f"❌ Błąd czytania pliku: {str(e)}"

    def _write_file(self, path: str, content: str) -> str:
        """Zapisuje do pliku"""
        try:
            from pathlib import Path
            safe_dir = Path(os.getenv("MCP_SAFE_DIR", "./mcp_workspace")).resolve()
            safe_dir.mkdir(parents=True, exist_ok=True)

            # Prevent Path Traversal by resolving and validating target path
            target_path = Path(safe_dir / path).resolve()
            if not str(target_path).startswith(str(safe_dir)):
                return "❌ Błąd bezpieczeństwa: Próba wyjścia poza dozwolony katalog (Path Traversal)"

            # Ensure subdirectories exist
            target_path.parent.mkdir(parents=True, exist_ok=True)

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)

            rel_path = target_path.relative_to(safe_dir)
            return f"✅ Zapisano {len(content)} znaków do '{safe_dir.name}/{rel_path}'"
        except Exception as e:
            return f"❌ Błąd zapisu: {str(e)}"

    def _list_directory(self, path: str = ".") -> str:
        """Listuje zawartość katalogu"""
        try:
            items = os.listdir(path)
            files = [f"📄 {item}" if os.path.isfile(os.path.join(path, item)) else f"📁 {item}" for item in items]
            return f"📂 Zawartość '{path}':\n" + "\n".join(files[:20])
        except Exception as e:
            return f"❌ Błąd listowania: {str(e)}"

    def _web_search(self, query: str) -> str:
        """Wyszukuje w internecie z fallbackiem po providerach API."""
        try:
            lines = []
            tavily_key = os.getenv("TAVILY_API_KEY", "").strip()
            if tavily_key:
                rr = requests.post(
                    "https://api.tavily.com/search",
                    json={"api_key": tavily_key, "query": query, "max_results": 5},
                    timeout=20,
                )
                if rr.ok:
                    for it in rr.json().get("results", [])[:5]:
                        lines.append(f"- {it.get('title','(no title)')}\n  {it.get('url','')}\n  {it.get('content','')[:220]}")
                    if lines:
                        return "🔍 [Tavily] Wyniki:\n" + "\n".join(lines)

            serper_key = os.getenv("SERPER_API_KEY", "").strip()
            if serper_key:
                rr = requests.post(
                    "https://google.serper.dev/search",
                    headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                    json={"q": query, "num": 5},
                    timeout=20,
                )
                if rr.ok:
                    for it in rr.json().get("organic", [])[:5]:
                        lines.append(f"- {it.get('title','(no title)')}\n  {it.get('link','')}\n  {it.get('snippet','')[:220]}")
                    if lines:
                        return "🔍 [Serper] Wyniki:\n" + "\n".join(lines)

            # DuckDuckGo fallback
            url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            if data.get("AbstractText"):
                lines.append(f"- {data['AbstractText']}")
            for rt in data.get("RelatedTopics", [])[:5]:
                if isinstance(rt, dict) and rt.get("Text"):
                    lines.append(f"- {rt.get('Text')}\n  {rt.get('FirstURL','')}")
            if lines:
                return "🔍 [DuckDuckGo] Wyniki:\n" + "\n".join(lines)
            return f"🔍 Brak wyników dla '{query}'."
        except Exception as e:
            return f"❌ Błąd wyszukiwania: {str(e)}"

    def _research_and_fill_kb(self, query: str, max_results: int = 5) -> str:
        """Wyszukuje i zapisuje treści stron do KB/web_research."""
        try:
            max_results = max(1, min(int(max_results), 10))
            search_text = self._web_search(query)
            urls = re.findall(r"https?://\S+", search_text)
            urls = urls[:max_results]
            if not urls:
                return "ℹ️ Brak URL-i do scrapingu."
            out_dir = KB_DIR / "web_research"
            out_dir.mkdir(parents=True, exist_ok=True)
            saved = []
            for idx, url in enumerate(urls, start=1):
                try:
                    resp = requests.get(url, timeout=20, headers={"User-Agent": "EastWood-Ops/1.0"})
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for tag in soup(["script", "style", "noscript"]):
                        tag.extract()
                    title = (soup.title.string or "").strip() if soup.title else url
                    text = "\n".join([ln.strip() for ln in soup.get_text("\n").splitlines() if ln.strip()])[:20000]
                    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", f"{query}-{idx}-{title}").strip("-")[:120] or f"entry-{idx}"
                    target = out_dir / f"{safe}.md"
                    target.write_text(f"# {title}\n\nSource: {url}\nQuery: {query}\n\n## Content\n\n{text}\n", encoding="utf-8")
                    saved.append(str(target.relative_to(KB_DIR)))
                except Exception:
                    continue
            return f"✅ Research zapisany do KB ({len(saved)}):\n" + "\n".join(f"- {p}" for p in saved)
        except Exception as e:
            return f"❌ Research błąd: {e}"

    def _scrape_to_knowledge_base(self, url: str, title: str = "") -> str:
        """Pobiera stronę WWW, wyciąga tekst i zapisuje do KB."""
        try:
            resp = requests.get(url, timeout=20, headers={"User-Agent": "EastWood-Ops/1.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.extract()
            page_title = (soup.title.string or "").strip() if soup.title else ""
            final_title = title.strip() or page_title or url
            body = "\n".join([ln.strip() for ln in soup.get_text("\n").splitlines() if ln.strip()])[:20000]
            safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", final_title).strip("-")[:120] or "web-entry"
            out_dir = KB_DIR / "web"
            out_dir.mkdir(parents=True, exist_ok=True)
            target = out_dir / f"{safe}.md"
            content = f"# {final_title}\n\nSource: {url}\n\n## Content\n\n{body}\n"
            target.write_text(content, encoding="utf-8")
            return f"✅ Zapisano stronę do KB: {target.relative_to(KB_DIR)} ({len(body)} znaków)"
        except Exception as e:
            return f"❌ Błąd scrape: {e}"

    def _tmdb_search_movie(self, query: str, limit: int = 5) -> str:
        """Wyszukuje filmy przez TMDB API i zapisuje JSON-y do KB/movies_api."""
        tmdb_key = os.getenv("TMDB_API_KEY", "").strip()
        if not tmdb_key:
            return "❌ Brak TMDB_API_KEY w środowisku"
        try:
            r = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={
                    "api_key": tmdb_key,
                    "query": query,
                    "language": "pl-PL",
                    "page": 1
                },
                timeout=20,
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])[: max(1, min(int(limit), 20))]
            out_dir = KB_DIR / "movies_api"
            out_dir.mkdir(parents=True, exist_ok=True)
            lines = []
            for mv in results:
                title = mv.get("title") or mv.get("original_title") or "untitled"
                safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", f"{title}-{mv.get('id','')}").strip("-")[:120]
                p = out_dir / f"{safe}.json"
                p.write_text(json.dumps(mv, ensure_ascii=False, indent=2), encoding="utf-8")
                lines.append(f"- {title} ({mv.get('release_date', 'brak daty')}) -> {p.relative_to(KB_DIR)}")
            if not lines:
                return f"ℹ️ Brak wyników TMDB dla: {query}"
            return "✅ TMDB import zakończony:\n" + "\n".join(lines)
        except Exception as e:
            return f"❌ TMDB błąd: {e}"

    def _push_knowledge_to_r2(self, prefix: str = "knowledge_mood") -> str:
        """Wysyła pliki z KB do Cloudflare R2 (S3 API)."""
        account_id = os.getenv("CF_R2_ACCOUNT_ID", "").strip()
        access_key = os.getenv("CF_R2_ACCESS_KEY_ID", "").strip()
        secret_key = os.getenv("CF_R2_SECRET_ACCESS_KEY", "").strip()
        bucket = os.getenv("CF_R2_BUCKET", "").strip()
        if not (account_id and access_key and secret_key and bucket):
            return "❌ Brak konfiguracji CF_R2_*"
        try:
            endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
            s3 = boto3.client(
                "s3",
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="auto",
            )
            uploaded = []
            for f in sorted(KB_DIR.rglob("*")):
                if not f.is_file():
                    continue
                if f.suffix.lower() not in {".md", ".txt", ".json", ".csv", ".py"}:
                    continue
                key = f"{prefix.strip('/')}/{str(f.relative_to(KB_DIR)).replace(os.sep, '/')}"
                s3.upload_file(str(f), bucket, key)
                uploaded.append(key)
            return f"✅ R2 upload OK: {len(uploaded)} plików do bucket={bucket}"
        except Exception as e:
            return f"❌ R2 upload błąd: {e}"

    def _calculator(self, expression: str) -> str:
        """Kalkulator matematyczny"""
        try:
            # Bezpieczne parsowanie - tylko matematyka
            allowed_chars = set("0123456789+-*/().^ ")
            if not all(c in allowed_chars or c.isspace() for c in expression):
                return "❌ Niedozwolone znaki w wyrażeniu"

            # Zamień ^ na **
            expression = expression.replace("^", "**")

            # Bezpieczna ewaluacja
            result = eval(expression, {"__builtins__": {}}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
                "log": math.log, "abs": abs, "pow": pow
            })

            return f"🔢 {expression} = {result}"
        except Exception as e:
            return f"❌ Błąd obliczeń: {str(e)}"

    def _execute_python(self, code: str) -> str:
        """Wykonuje kod Python w sandboxie (ulepszony — stdout/stderr osobno, timeout, auto python)."""
        blocks = ["import os", "import sys", "import subprocess", "import shutil"]
        for b in blocks:
            if b in code:
                return f"❌ Niebezpieczny kod \u2014 '{b}' niedozwolone"
        try:
            python = sys.executable
            result = subprocess.run(
                [python, "-c", code],
                capture_output=True,
                text=True,
                timeout=10
            )
            parts = []
            if result.stdout:
                parts.append(f"stdout:\n{result.stdout[:2000]}")
            if result.stderr:
                parts.append(f"stderr:\n{result.stderr[:1000]}")
            if not parts:
                return "\U0001f40d Kod wykonany, brak outputu."
            return "\U0001f40d Wynik:\n" + "\n---\n".join(parts)
        except subprocess.TimeoutExpired:
            return "\u274c Timeout (10s) \u2014 kod wykonywa\u0142 si\u0119 za d\u0142ugo"
        except Exception as e:
            return f"\u274c B\u0142\u0105d: {str(e)}"

    def _get_weather(self, location: str, lat: float = None, lon: float = None) -> str:
        """Pogoda dla lokalizacji przez open-meteo.com (bez API key)."""
        try:
            if lat is None or lon is None:
                geo = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": location, "count": 1, "language": "pl", "format": "json"},
                    timeout=10
                )
                if not geo.ok:
                    return f"\u2753 Nie znaleziono lokalizacji: {location}"
                geo_data = geo.json()
                if not geo_data.get("results"):
                    return f"\u2753 Nie znaleziono lokalizacji: {location}"
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                loc_name = geo_data["results"][0].get("name", location)
                country = geo_data["results"][0].get("country", "")
                location = f"{loc_name}, {country}"

            w = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature",
                               "weather_code", "wind_speed_10m", "pressure_msl"],
                    "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code",
                              "precipitation_sum", "wind_speed_10m_max"],
                    "timezone": "auto", "forecast_days": 3
                },
                timeout=10
            )
            if not w.ok:
                return f"\u2753 B\u0142\u0105d pobierania pogody: HTTP {w.status_code}"
            d = w.json()
            cur = d.get("current", {})
            code_map = {
                0: "\u2600\ufe0f bezchmurnie", 1: "\ud83c\udf24 g\u0142\u00f3wnie bezchmurnie", 2: "\u26c5 cz\u0119\u015bciowo pochmurno",
                3: "\u2601\ufe0f pochmurno", 45: "\ud83c\udf2b mg\u0142a", 48: "\ud83c\udf2b szron", 51: "\ud83c\udf26 lekka m\u017cawka",
                53: "\ud83c\udf26 umiarkowana m\u017cawka", 55: "\ud83c\udfe7 g\u0119sta m\u017cawka", 61: "\ud83c\udf26 lekki deszcz",
                63: "\ud83c\udfe7 umiarkowany deszcz", 65: "\ud83c\udfe7\ud83c\udfe7 silny deszcz", 71: "\ud83c\udf28 lekki \u015bnieg",
                73: "\ud83c\udf28 umiarkowany \u015bnieg", 75: "\ud83c\udf28\ud83c\udf28 silny \u015bnieg",
                80: "\ud83c\udf27 przelotne opady", 81: "\ud83c\udf27\ud83c\udf27 umiarkowane przelotne",
                82: "\ud83c\udf27\ud83c\udf27\ud83c\udf27 silne przelotne", 85: "\ud83c\udf28 przelotny \u015bnieg",
                86: "\ud83c\udf28\ud83c\udf28 silny przelotny \u015bnieg", 95: "\u26c8 burza",
                96: "\u26c8\u26a1 burza z gradem", 99: "\u26c8\u26a1\u26a1 silna burza z gradem"
            }
            wcode = cur.get("weather_code", 0)
            desc = code_map.get(wcode, f"kod {wcode}")
            temp = cur.get("temperature_2m", "?")
            feels = cur.get("apparent_temperature", "?")
            hum = cur.get("relative_humidity_2m", "?")
            wind = cur.get("wind_speed_10m", "?")
            pressure = cur.get("pressure_msl", "?")

            lines = [
                f"\ud83c\udf24 Pogoda dla: {location}",
                f"{desc}, {temp}\u00b0C (odczuwalna {feels}\u00b0C)",
                f"\ud83d\udca7 Wilgotno\u015b\u0107: {hum}% | \ud83d\udca8 Wiatr: {wind} km/h",
                f"\ud83d\udccf Ci\u015bnienie: {pressure} hPa",
            ]

            daily = d.get("daily", {})
            if daily:
                dates = daily.get("time", [])
                tmax = daily.get("temperature_2m_max", [])
                tmin = daily.get("temperature_2m_min", [])
                wcodes = daily.get("weather_code", [])
                precip = daily.get("precipitation_sum", [])
                lines.append("")
                lines.append("\ud83d\udcc5 Prognoza na 3 dni:")
                for i in range(min(len(dates), 3)):
                    cd = code_map.get(wcodes[i], f"kod {wcodes[i]}") if i < len(wcodes) else ""
                    p = precip[i] if i < len(precip) else "?"
                    lines.append(f"  {dates[i]}: {tmax[i]}\u00b0C / {tmin[i]}\u00b0C, {cd}, opady {p}mm")

            return "\n".join(lines)

        except Exception as e:
            return f"\u274c B\u0142\u0105d pogody: {str(e)}"

    def _note_save(self, title: str, content: str) -> str:
        """Zapisuje notatk\u0119."""
        try:
            notes_dir = KB_DIR / "notes"
            notes_dir.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", title).strip("-")[:80] or "note"
            target = notes_dir / f"{safe}.md"
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            text = f"# {title}\n\n**Utworzono:** {ts}\n\n{content}\n"
            target.write_text(text, encoding="utf-8")
            return f"\u2705 Notatka zapisana: notes/{safe}.md"
        except Exception as e:
            return f"\u274c B\u0142\u0105d zapisu notatki: {str(e)}"

    def _note_read(self, title: str) -> str:
        """Czyta notatk\u0119 po tytule (szuka po plikach .md w notes/)."""
        try:
            notes_dir = KB_DIR / "notes"
            if not notes_dir.exists():
                return "\u2139\ufe0f Brak notatek."
            query = title.lower().strip()
            for f in sorted(notes_dir.glob("*.md")):
                if query in f.stem.lower():
                    content = f.read_text(encoding="utf-8")[:3000]
                    return f"\ud83d\udcdd {f.stem}:\n\n{content}"
            return f"\u2753 Nie znaleziono notatki: {title}. U\u017cyj note_list."
        except Exception as e:
            return f"\u274c B\u0142\u0105d: {str(e)}"

    def _note_list(self) -> str:
        """Listuje wszystkie notatki."""
        try:
            notes_dir = KB_DIR / "notes"
            if not notes_dir.exists():
                return "\u2139\ufe0f Brak notatek."
            files = sorted(notes_dir.glob("*.md"))
            if not files:
                return "\u2139\ufe0f Brak notatek."
            lines = ["\ud83d\udcdd Notatki:"]
            for f in files:
                size = len(f.read_text(encoding="utf-8"))
                lines.append(f"  \ud83d\udcc4 {f.stem} ({size} znak\u00f3w)")
            return "\n".join(lines)
        except Exception as e:
            return f"\u274c B\u0142\u0105d: {str(e)}"

    def _note_search(self, query: str) -> str:
        """Szuka w tre\u015bci notatek."""
        try:
            notes_dir = KB_DIR / "notes"
            if not notes_dir.exists():
                return "\u2139\ufe0f Brak notatek."
            q = query.lower().strip()
            results = []
            for f in sorted(notes_dir.glob("*.md")):
                content = f.read_text(encoding="utf-8")
                if q in content.lower():
                    lines = [l.strip() for l in content.split("\n") if l.strip() and q in l.lower()]
                    snippet = "\n".join(lines[:3])[:400]
                    results.append(f"  \ud83d\udcc4 {f.stem}:\n    {snippet}")
            if not results:
                return f"\u2139\ufe0f Brak wynik\u00f3w dla '{query}' w notatkach."
            return f"\ud83d\udd0e Wyniki w notatkach dla '{query}':\n\n" + "\n\n".join(results[:10])
        except Exception as e:
            return f"\u274c B\u0142\u0105d: {str(e)}"

    def _system_info(self) -> str:
        """Informacje systemowe"""
        import platform
        info = {
            "System": platform.system(),
            "Release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor() or "Unknown",
            "Python": platform.python_version()
        }
        return "💻 Informacje systemowe:\n" + "\n".join(f"- {k}: {v}" for k, v in info.items())

    def _get_datetime(self) -> str:
        """Aktualna data i czas"""
        from datetime import datetime
        now = datetime.now()
        return f"🕐 {now.strftime('%Y-%m-%d %H:%M:%S')} ({now.strftime('%A')})"

    def _count_words(self, text: str) -> str:
        """Liczy słowa w tekście"""
        words = len(text.split())
        chars = len(text)
        lines = len(text.split("\n"))
        return f"📊 Statystyki tekstu:\n- Słowa: {words}\n- Znaki: {chars}\n- Linie: {lines}"

    def _search_knowledge_base(self, query: str) -> str:
        """Przeszukuje baze wiedzy — semantic search (sentence-transformers) lub grep fallback."""
        # Semantic search (if embeddings ready)
        if _HAS_EMBEDDINGS and _embed.is_ready():
            try:
                idx = _embed.get_index()
                hits = idx.semantic_search_kb(query, top_k=5)
                if hits:
                    parts = [f"📄 {h['source']} (score={h['score']:.2f}):\n{h['text']}" for h in hits]
                    return f"🔎 Semantic wyniki dla '{query}':\n\n" + "\n\n".join(parts)
                return f"🔎 Brak semantycznych wyników dla '{query}' w KB."
            except Exception as e:
                print(f"[KB search] Semantic error, falling back to grep: {e}")

        # Grep fallback (embeddings not ready yet)
        query_lower = query.lower()
        results = []
        try:
            for file_path in sorted(KB_DIR.rglob("*")):
                if file_path.is_file() and file_path.suffix in {".txt", ".md", ".json", ".py", ".csv"}:
                    try:
                        text = file_path.read_text(encoding="utf-8")
                        if query_lower in text.lower():
                            lines = text.split("\n")
                            matching = [l.strip() for l in lines if query_lower in l.lower()]
                            snippet = "\n".join(matching[:3])
                            results.append(f"📄 {file_path.name}:\n{snippet}")
                    except Exception:
                        pass
            if results:
                return f"🔎 Wyniki grep '{query}' w KB (embeddings nie gotowe):\n\n" + "\n\n".join(results[:5])
            return f"🔎 Brak wyników dla '{query}' w KB."
        except Exception as e:
            return f"❌ Błąd wyszukiwania KB: {str(e)}"


    def _list_knowledge_base(self) -> str:
        """Listuje pliki w bazie wiedzy"""
        try:
            files = sorted([f for f in KB_DIR.rglob("*") if f.is_file()])
            if not files:
                return f"📂 Baza wiedzy jest pusta. Dodaj pliki .txt lub .md do folderu: {KB_DIR}"
            items = [f"📄 {f.relative_to(KB_DIR)} ({f.stat().st_size} B)" for f in files]
            return f"📂 Baza wiedzy ({len(files)} plik(ów)) w {KB_DIR}:\n" + "\n".join(items)
        except Exception as e:
            return f"❌ Błąd listowania KB: {str(e)}"

    def _read_knowledge_file(self, filename: str) -> str:
        """Czyta konkretny plik z bazy wiedzy"""
        try:
            target = (KB_DIR / filename).resolve()
            if not str(target).startswith(str(KB_DIR.resolve())):
                return "❌ Dostęp zabroniony - plik poza bazą wiedzy"
            if not target.exists():
                return f"❌ Plik '{filename}' nie istnieje w bazie wiedzy. Użyj list_knowledge_mood."
            content = target.read_text(encoding="utf-8")
            truncated = len(content) > 3000
            return f"📄 {filename}:\n{content[:3000]}" + ("\n...[plik skrócony]" if truncated else "")
        except Exception as e:
            return f"❌ Błąd czytania z KB: {str(e)}"


def parse_tool_call_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Parsuje wywołania narzędzi z tekstu generowanego przez model.

    Format: [TOOL:nazwa_narzędzia]argument1|argument2[/TOOL]
    Przykład: [TOOL:calculator]2+2[/TOOL]
    """
    pattern = r'\[TOOL:(\w+)\](.*?)\[/TOOL\]'
    matches = re.findall(pattern, text, re.DOTALL)

    tool_calls = []
    for tool_name, args_text in matches:
        # Parse arguments (simple key=value or positional)
        kwargs = {}

        # Try JSON first (model sometimes sends {"key": "val", ...})
        stripped = args_text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                kwargs = json.loads(stripped)
            except json.JSONDecodeError:
                pass

        if not kwargs:
            # Sprawdź czy to key=value format (key=val|key=val)
            if "=" in args_text and "|" in args_text:
                for pair in args_text.split("|"):
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        kwargs[key.strip()] = value.strip()

        if not kwargs and stripped:
            # NarzÄ™dzia bezargumentowe
            no_arg_tools = {"note_list", "system_info", "get_datetime", "list_knowledge_base", "list_knowledge_mood"}
            if tool_name in no_arg_tools:
                pass  # kwargs stays empty
            else:
                # Pozycyjny argument — mapa tool_name -> pierwszy parametr
                pos_map = {
                    "read_file": "path",
                    "write_file": None,
                    "read_knowledge_file": "filename",
                    "execute_python": "code",
                    "web_search": "query",
                    "calculator": "expression",
                    "count_words": "text",
                    "search_knowledge_base": "query",
                    "search_knowledge_mood": "query",
                    "get_weather": "location",
                    "list_directory": "path",
                    "note_save": None,
                    "note_read": "title",
                    "note_search": "query",
                }
                mapping = pos_map.get(tool_name, "query")
                if mapping is None and tool_name in ("write_file", "note_save"):
                    parts = stripped.split("|", 1)
                    key1 = "path" if tool_name == "write_file" else "title"
                    key2 = "content"
                    kwargs[key1] = parts[0].strip()
                    kwargs[key2] = parts[1].strip() if len(parts) > 1 else ""
                else:
                    kwargs[mapping] = stripped

        tool_calls.append({
            "tool": tool_name,
            "args": kwargs
        })

    return tool_calls


# Global registry instance
mcp_registry = MCPToolRegistry()
