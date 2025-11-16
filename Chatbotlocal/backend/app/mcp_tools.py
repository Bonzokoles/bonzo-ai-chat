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
from pathlib import Path
from typing import Dict, Any, List, Callable
import math
import re


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

        # 3. CALCULATOR
        self.register_tool(
            name="calculator",
            description="Wykonuje obliczenia matematyczne. Args: expression (str)",
            function=self._calculator
        )

        # 4. CODE EXECUTION (SANDBOXED)
        self.register_tool(
            name="execute_python",
            description="Wykonuje kod Python (bezpiecznie). Args: code (str)",
            function=self._execute_python
        )

        # 5. SYSTEM INFO
        self.register_tool(
            name="system_info",
            description="Zwraca informacje systemowe",
            function=self._system_info
        )

        # 6. DATE/TIME
        self.register_tool(
            name="get_datetime",
            description="Zwraca aktualną datę i czas",
            function=self._get_datetime
        )

        # 7. TEXT PROCESSING
        self.register_tool(
            name="count_words",
            description="Liczy słowa w tekście. Args: text (str)",
            function=self._count_words
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
            # Bezpieczeństwo: tylko w dozwolonych katalogach
            safe_dir = os.getenv("MCP_SAFE_DIR", "./mcp_workspace")
            os.makedirs(safe_dir, exist_ok=True)

            safe_path = os.path.join(safe_dir, os.path.basename(path))
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Zapisano {len(content)} znaków do '{safe_path}'"
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
        """Wyszukuje w internecie (używa DuckDuckGo HTML)"""
        try:
            # Prosty search przez DuckDuckGo Instant Answer API
            url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&pretty=1"
            response = requests.get(url, timeout=5)
            data = response.json()

            if data.get("AbstractText"):
                return f"🔍 Wynik dla '{query}':\n{data['AbstractText']}"
            elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                first = data["RelatedTopics"][0]
                if "Text" in first:
                    return f"🔍 Wynik dla '{query}':\n{first['Text']}"

            return f"🔍 Brak bezpośrednich wyników dla '{query}'. Spróbuj innego zapytania."
        except Exception as e:
            return f"❌ Błąd wyszukiwania: {str(e)}"

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
        """Wykonuje kod Python w sandboxie"""
        try:
            # Bezpieczeństwo: timeout, ograniczenia
            if any(dangerous in code for dangerous in ["import os", "import sys", "exec", "eval", "__"]):
                return "❌ Niebezpieczny kod - zabronione importy"

            # Wykonaj z timeoutem
            result = subprocess.run(
                ["python3", "-c", code],
                capture_output=True,
                text=True,
                timeout=5
            )

            output = result.stdout or result.stderr
            return f"🐍 Wynik:\n{output[:500]}"
        except subprocess.TimeoutExpired:
            return "❌ Timeout - kod wykonywał się za długo"
        except Exception as e:
            return f"❌ Błąd wykonania: {str(e)}"

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

        # Sprawdź czy to key=value format
        if "=" in args_text:
            for pair in args_text.split("|"):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    kwargs[key.strip()] = value.strip()
        else:
            # Pozycyjny argument (domyślnie pierwszy parametr)
            # Dla większości narzędzi pierwszy parametr jest główny
            if tool_name == "read_file":
                kwargs["path"] = args_text.strip()
            elif tool_name == "write_file":
                parts = args_text.split("|", 1)
                kwargs["path"] = parts[0].strip()
                kwargs["content"] = parts[1].strip() if len(parts) > 1 else ""
            elif tool_name in ["web_search", "calculator", "count_words"]:
                kwargs[list(inspect.signature(MCPToolRegistry.__dict__[f"__{tool_name}"]).parameters.keys())[1]] = args_text.strip()
            else:
                # Domyślnie pierwszy argument
                kwargs["query"] = args_text.strip()

        tool_calls.append({
            "tool": tool_name,
            "args": kwargs
        })

    return tool_calls


# Global registry instance
mcp_registry = MCPToolRegistry()
