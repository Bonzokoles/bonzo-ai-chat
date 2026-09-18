# -*- coding: utf-8 -*-
"""
Multi-provider LLM wrapper
Priority: OpenRouter > OpenAI > Ollama (fallback)
"""
import os
import json
import re
import sqlite3
import requests
from pathlib import Path
from typing import Optional, Generator


# --- Load only local runtime .env files (backend -> app shell) ---
def _load_env():
    current = Path(__file__).resolve().parent
    discovered = []
    for _ in range(3):
        for filename in (".env.runtime", ".env"):
            env_path = current / filename
            if env_path.exists():
                discovered.append(env_path)
        current = current.parent
    if not discovered:
        print("[WARN] Nie znaleziono pliku .env")
        return
    for env_path in reversed(discovered):
        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_.-]*$", key):
                continue
            os.environ[key] = value
        print(f"[OK] Załadowano .env z: {env_path}")


_load_env()


def _bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _discover_9router_api_key() -> Optional[str]:
    appdata = os.getenv("APPDATA")
    if not appdata:
        return None
    db_path = Path(appdata) / "9router" / "db" / "data.sqlite"
    if not db_path.exists():
        return None
    try:
        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                "select key from apiKeys where isActive = 1 order by createdAt asc limit 1"
            ).fetchone()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception:
        return None
    return None

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:4149")
APP_NAME = os.getenv("APP_NAME", "EastWood Ops")
OPENROUTER_DEFAULT_MODEL = os.getenv("OPENROUTER_DEFAULT_MODEL", "x-ai/grok-4.3")
OPENROUTER_SECONDARY_MODEL = os.getenv("OPENROUTER_SECONDARY_MODEL", "z-ai/glm-5.1")
OPENROUTER_FALLBACK_MODEL = os.getenv("OPENROUTER_FALLBACK_MODEL", "moonshotai/kimi-k2.6")
AGENT_MODEL_PRIMARY = os.getenv("AGENT_MODEL_PRIMARY", "deepseek/deepseek-v4-pro")
AGENT_MODEL_SECONDARY = os.getenv("AGENT_MODEL_SECONDARY", "minimax/minimax-m2.7")
AGENT_MODEL_EXPERIMENTAL = os.getenv("AGENT_MODEL_EXPERIMENTAL", "tencent/hy3-preview")
MYBONZO_BASE_URL = os.getenv("MYBONZO_BASE_URL", "https://mybonzo-v3.stolarnia-ams.workers.dev/v1").rstrip("/")
MYBONZO_API_KEY = os.getenv("MYBONZO_API_KEY", "BonzoToken2026")
MYBONZO_MODELS = {
    "MyBonzo Llama 3.3 70B (Edge Free)": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    "MyBonzo Llama 3.2 3B (Edge Fast)": "@cf/meta/llama-3.2-3b-instruct",
    "MyBonzo Llama 3.1 8B (Edge)": "@cf/meta/llama-3.1-8b-instruct",
    "MyBonzo Smart Auto-Router": "auto",
}
MODEL_ROUTER_ENABLED = _bool_env("MODEL_ROUTER_ENABLED", False)
MODEL_ROUTER_BASE_URL = os.getenv("MODEL_ROUTER_BASE_URL", "http://127.0.0.1:20128/v1").rstrip("/")
MODEL_ROUTER_DEFAULT_MODEL = os.getenv("MODEL_ROUTER_DEFAULT_MODEL", "auto/best-chat")
MODEL_ROUTER_AUTO_DISCOVER_KEY = _bool_env("MODEL_ROUTER_AUTO_DISCOVER_KEY", False)
MODEL_ROUTER_API_KEY = os.getenv("MODEL_ROUTER_API_KEY")
if not MODEL_ROUTER_API_KEY and MODEL_ROUTER_AUTO_DISCOVER_KEY:
    MODEL_ROUTER_API_KEY = _discover_9router_api_key()
SPEECH_API_KEY = os.getenv("SPEECH_API_KEY") or OPENAI_API_KEY
SPEECH_API_BASE_URL = os.getenv("SPEECH_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")
STT_MODEL = os.getenv("STT_MODEL", "gpt-4o-mini-transcribe")
TTS_MODEL = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("TTS_VOICE", "alloy")

ROUTER_MODELS = {
    "BUCH Router Chat Chain": "auto/best-chat",
    "BUCH Router Agent Chain": "auto/best-coding",
    "BUCH Router Experimental Chain": "auto/best-fast",
}

# Display name → API model ID
OPENROUTER_MODELS = {
    "BUCH Primary — Grok 4.3": "x-ai/grok-4.3",
    "BUCH Secondary — GLM 5.1": "z-ai/glm-5.1",
    "BUCH Fallback — Kimi K2.6": "moonshotai/kimi-k2.6",
    "Agent Optional — MiniMax M3": "minimax/minimax-m3",
    "Agent Primary — DeepSeek V4 Pro": "deepseek/deepseek-v4-pro",
    "Agent Secondary — MiniMax M2.7": "minimax/minimax-m2.7",
    "Agent Experimental — Hy3 Preview": "tencent/hy3-preview",
    "DeepSeek Chat":         "deepseek/deepseek-chat",
    "Claude 3 Haiku":        "anthropic/claude-3-haiku",
    "Gemini Flash 1.5":      "google/gemini-flash-1.5",
    "Gemma 4 31B Free":      "google/gemma-4-31b-it:free",
    "Gemma 4 26B Free":      "google/gemma-4-26b-a4b-it:free",
    "Llama 3.3 70B Free":    "meta-llama/llama-3.3-70b-instruct:free",
    "Llama 3.2 3B Fast":     "meta-llama/llama-3.2-3b-instruct:free",
    "Qwen3 80B Free":        "qwen/qwen3-next-80b-a3b-instruct:free",
    "Qwen3 Coder Free":      "qwen/qwen3-coder:free",
    "Hermes 3 405B Free":    "nousresearch/hermes-3-llama-3.1-405b:free",
}

OPENAI_MODELS = {
    "GPT-4o mini":   "gpt-4o-mini",
    "GPT-3.5 Turbo": "gpt-3.5-turbo",
}

ALL_MODELS = {**OPENROUTER_MODELS, **OPENAI_MODELS}


class MultiProviderModel:
    """
    Wybiera provider automatycznie na podstawie dostępnych kluczy API.
    Priorytet: OpenRouter > OpenAI > Ollama
    """

    def __init__(self, model_name: str = None):
        self.router_enabled = bool(MODEL_ROUTER_ENABLED and MODEL_ROUTER_API_KEY)
        self.router_base_url = MODEL_ROUTER_BASE_URL
        if MYBONZO_BASE_URL:
            self.provider = "mybonzo"
            self.default_model_id = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
            self.default_model_name = "MyBonzo Llama 3.3 70B (Edge Free)"
            print(f"[OK] MyBonzo Edge aktywny ({MYBONZO_BASE_URL})")
        elif self.router_enabled:
            self.provider = "9router"
            self.default_model_id = MODEL_ROUTER_DEFAULT_MODEL
            self.default_model_name = self._display_name_for_id(self.default_model_id)
            print(f"[OK] 9router aktywny ({self.router_base_url})")
        elif OPENROUTER_API_KEY:
            self.provider = "openrouter"
            self.default_model_id = OPENROUTER_DEFAULT_MODEL
            self.default_model_name = self._display_name_for_id(self.default_model_id)
            print(f"[OK] OpenRouter aktywny (klucz: ...{OPENROUTER_API_KEY[-8:]})")
        elif OPENAI_API_KEY:
            self.provider = "openai"
            self.default_model_id = "gpt-4o-mini"
            self.default_model_name = "GPT-4o mini"
            print(f"[OK] OpenAI aktywny (klucz: ...{OPENAI_API_KEY[-8:]})")
        else:
            self.provider = "ollama"
            self.default_model_id = model_name or "llama3.2:latest"
            self.default_model_name = "Ollama local"
            print(f"[WARN] Brak kluczy API - próbuję Ollama: {self.default_model_id}")

    def _display_name_for_id(self, model_id: str) -> str:
        for display_name, mapped_id in MYBONZO_MODELS.items():
            if mapped_id == model_id:
                return display_name
        for display_name, mapped_id in ROUTER_MODELS.items():
            if mapped_id == model_id:
                return display_name
        for display_name, mapped_id in ALL_MODELS.items():
            if mapped_id == model_id:
                return display_name
        return model_id

    def _resolve_model(self, model_name: str | None):
        """Zwraca (provider, model_id) dla nazwy wyświetlanej lub raw ID."""
        if not model_name:
            return self.provider, self.default_model_id
        if model_name in MYBONZO_MODELS:
            return "mybonzo", MYBONZO_MODELS[model_name]
        if model_name in MYBONZO_MODELS.values() or model_name.startswith(("@cf/", "pollinations/")) or model_name == "auto":
            return "mybonzo", model_name
        if model_name in ROUTER_MODELS:
            return "9router", ROUTER_MODELS[model_name]
        if model_name in ROUTER_MODELS.values():
            return "9router", model_name
        if model_name in OPENROUTER_MODELS:
            return "openrouter", OPENROUTER_MODELS[model_name]
        if model_name in OPENAI_MODELS:
            return "openai", OPENAI_MODELS[model_name]
        if model_name.startswith(("gpt-", "o1-", "o3-")):
            return "openai", model_name
        if model_name.startswith("buch-"):
            return "9router", model_name
        # Default: raw routed/openrouter model ID
        if MYBONZO_BASE_URL and (not model_name or "/" not in model_name):
            return "mybonzo", model_name
        return ("9router" if self.router_enabled and "/" not in model_name else "openrouter"), model_name

    def get_small_model_name(self) -> str:
        """Zwraca tani/szybki model w zależności od aktywnego providera (np. do zadań w tle)."""
        if self.provider == "mybonzo":
            return "@cf/meta/llama-3.2-3b-instruct"
        elif self.provider == "9router":
            return "gpt-4o-mini"
        elif self.provider == "openrouter":
            return "meta-llama/llama-3.2-3b-instruct:free"
        elif self.provider == "openai":
            return "gpt-4o-mini"
        return self.default_model_id

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.6,
                 top_p: float = 0.9, model_name: str = None) -> str:
        provider, model_id = self._resolve_model(model_name)

        if provider == "mybonzo" and MYBONZO_BASE_URL:
            return self._call_mybonzo(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "9router" and MODEL_ROUTER_API_KEY:
            return self._call_9router(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "openrouter" and OPENROUTER_API_KEY:
            return self._call_openrouter(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "openai" and OPENAI_API_KEY:
            return self._call_openai(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "ollama":
            return self._call_ollama(prompt, model_id, max_tokens, temperature, top_p)
        else:
            return f"[ERR] Provider '{provider}' niedostępny — brak klucza API"

    def _call_mybonzo(self, prompt: str, model_id: str, max_tokens: int,
                      temperature: float, top_p: float) -> str:
        try:
            resp = requests.post(
                f"{MYBONZO_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MYBONZO_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": False,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                payload = resp.json()
                choices = payload.get("choices")
                if choices and len(choices) > 0:
                    msg = choices[0].get("message", {})
                    return msg.get("content", "")
                return payload.get("response", "") or payload.get("content", "")
            if OPENROUTER_API_KEY:
                return self._call_openrouter(prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p)
            return f"[ERR] MyBonzo Edge błąd {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            if OPENROUTER_API_KEY:
                return self._call_openrouter(prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p)
            return f"[ERR] MyBonzo Edge wyjątek: {str(e)}"


    def _call_9router(self, prompt: str, model_id: str, max_tokens: int,
                      temperature: float, top_p: float) -> str:
        try:
            resp = requests.post(
                f"{self.router_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MODEL_ROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": False,
                },
                timeout=90,
            )
            if resp.status_code == 200:
                body = resp.text.strip()
                if body.startswith("data:"):
                    # Defensive: provider ignored stream=false and sent SSE anyway.
                    lines = [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
                    lines = [ln for ln in lines if ln and ln != "[DONE]"]
                    chunks = [json.loads(ln) for ln in lines]
                    content_parts, reasoning_parts = [], []
                    for ch in chunks:
                        delta = ch.get("choices", [{}])[0].get("delta", {})
                        if delta.get("content"):
                            content_parts.append(delta["content"])
                        elif delta.get("reasoning"):
                            reasoning_parts.append(delta["reasoning"])
                    return (
                        "".join(content_parts)
                        or "".join(reasoning_parts)
                        or "[ERR] 9router zwrócił pustą odpowiedź"
                    )
                payload = json.loads(body)
                message = payload["choices"][0]["message"]
                return (
                    message.get("content")
                    or message.get("reasoning_content")
                    or message.get("reasoning")
                    or "[ERR] 9router zwrócił pustą odpowiedź"
                )
            if OPENROUTER_API_KEY:
                return self._call_openrouter(prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p)
            return f"[ERR] 9router błąd {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            if OPENROUTER_API_KEY:
                return self._call_openrouter(prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p)
            return f"[ERR] 9router wyjątek: {str(e)}"

    def _call_openrouter(self, prompt: str, model_id: str, max_tokens: int,
                         temperature: float, top_p: float) -> str:
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": UI_BASE_URL,
                    "X-Title": APP_NAME,
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            return f"[ERR] OpenRouter błąd {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            return f"[ERR] OpenRouter wyjątek: {str(e)}"

    def _call_openai(self, prompt: str, model_id: str, max_tokens: int,
                     temperature: float, top_p: float) -> str:
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            return f"[ERR] OpenAI błąd {resp.status_code}: {resp.text[:300]}"
        except Exception as e:
            return f"[ERR] OpenAI wyjątek: {str(e)}"

    def _call_ollama(self, prompt: str, model_id: str, max_tokens: int,
                     temperature: float, top_p: float) -> str:
        try:
            resp = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model_id,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                    },
                },
                timeout=90,
            )
            if resp.status_code == 200:
                return resp.json().get("response", "Brak odpowiedzi z Ollama")
            return f"[ERR] Ollama błąd {resp.status_code}"
        except requests.exceptions.ConnectionError:
            return "[ERR] Ollama niedostępna. Uruchom: ollama serve"
        except Exception as e:
            return f"[ERR] Ollama wyjątek: {str(e)}"

    def generate_stream(self, prompt: str, max_tokens: int = 512, temperature: float = 0.6,
                         top_p: float = 0.9, model_name: str = None) -> Generator[str, None, str]:
        """Streaming generation. Yields text chunks. Returns final full text."""
        provider, model_id = self._resolve_model(model_name)

        if provider == "mybonzo" and MYBONZO_BASE_URL:
            full = yield from self._stream_mybonzo(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "9router" and MODEL_ROUTER_API_KEY:
            full = yield from self._stream_9router(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "openrouter" and OPENROUTER_API_KEY:
            full = yield from self._stream_openrouter(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "openai" and OPENAI_API_KEY:
            full = yield from self._stream_openai(prompt, model_id, max_tokens, temperature, top_p)
        elif provider == "ollama":
            full = yield from self._stream_ollama(prompt, model_id, max_tokens, temperature, top_p)
        else:
            msg = f"[ERR] Provider '{provider}' niedostępny — brak klucza API"
            yield msg
            full = msg
        return full

    def _stream_mybonzo(self, prompt: str, model_id: str, max_tokens: int,
                        temperature: float, top_p: float) -> Generator[str, None, str]:
        full = ""
        try:
            resp = requests.post(
                f"{MYBONZO_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MYBONZO_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": True,
                },
                stream=True,
                timeout=60,
            )
            if resp.status_code != 200:
                msg = f"[ERR] MyBonzo Edge stream HTTP {resp.status_code}: {resp.text[:200]}"
                yield msg
                return msg

            for raw_line in resp.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                line = raw_line.strip()
                if line.startswith("data:"):
                    payload = line[5:].strip()
                    if payload == "[DONE]":
                        break
                    try:
                        chunk = json.loads(payload)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        token = delta.get("content", "")
                        if token:
                            full += token
                            yield token
                    except Exception:
                        continue
            return full
        except Exception as e:
            if OPENROUTER_API_KEY:
                full = yield from self._stream_openrouter(
                    prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p
                )
                return full
            msg = f"[ERR] MyBonzo Edge stream wyjątek: {str(e)}"
            yield msg
            return msg

    def _stream_openrouter(self, prompt: str, model_id: str, max_tokens: int,
                            temperature: float, top_p: float) -> Generator[str, None, str]:
        full = ""
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": UI_BASE_URL,
                    "X-Title": APP_NAME,
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": True,
                },
                timeout=120,
                stream=True,
            )
            if resp.status_code != 200:
                msg = f"[ERR] OpenRouter b\u0142\u0105d {resp.status_code}: {resp.text[:300]}"
                yield msg
                return msg
            for line in resp.iter_lines():
                if not line:
                    continue
                decoded = line.decode("utf-8", errors="replace")
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    try:
                        obj = json.loads(decoded[6:])
                        delta = obj.get("choices", [{}])[0].get("delta", {})
                        chunk = delta.get("content", "")
                        if chunk:
                            full += chunk
                            yield chunk
                    except json.JSONDecodeError:
                        pass
            if not full:
                msg = "[ERR] Brak odpowiedzi z OpenRouter (stream)"
                yield msg
                full = msg
        except Exception as e:
            msg = f"[ERR] OpenRouter stream wyj\u0105tek: {str(e)}"
            yield msg
            full = msg
        return full

    def _stream_openai(self, prompt: str, model_id: str, max_tokens: int,
                        temperature: float, top_p: float) -> Generator[str, None, str]:
        full = ""
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": True,
                },
                timeout=120,
                stream=True,
            )
            for line in resp.iter_lines():
                if not line:
                    continue
                decoded = line.decode("utf-8", errors="replace")
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    try:
                        obj = json.loads(decoded[6:])
                        delta = obj.get("choices", [{}])[0].get("delta", {})
                        chunk = delta.get("content", "")
                        if chunk:
                            full += chunk
                            yield chunk
                    except json.JSONDecodeError:
                        pass
            if not full:
                msg = "[ERR] Brak odpowiedzi z OpenAI (stream)"
                yield msg
                full = msg
        except Exception as e:
            msg = f"[ERR] OpenAI stream wyj\u0105tek: {str(e)}"
            yield msg
            full = msg
        return full

    def _stream_ollama(self, prompt: str, model_id: str, max_tokens: int,
                        temperature: float, top_p: float) -> Generator[str, None, str]:
        full = ""
        try:
            resp = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": model_id,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                    },
                },
                timeout=120,
                stream=True,
            )
            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    obj = json.loads(line.decode("utf-8", errors="replace"))
                    chunk = obj.get("response", "")
                    if chunk:
                        full += chunk
                        yield chunk
                    if obj.get("done"):
                        break
                except json.JSONDecodeError:
                    pass
            if not full:
                msg = "[ERR] Brak odpowiedzi z Ollama (stream)"
                yield msg
                full = msg
        except requests.exceptions.ConnectionError:
            msg = "[ERR] Ollama niedost\u0119pna. Uruchom: ollama serve"
            yield msg
            full = msg
        except Exception as e:
            msg = f"[ERR] Ollama stream wyj\u0105tek: {str(e)}"
            yield msg
            full = msg
        return full

    def _stream_9router(self, prompt: str, model_id: str, max_tokens: int,
                        temperature: float, top_p: float) -> Generator[str, None, str]:
        full = ""
        try:
            resp = requests.post(
                f"{self.router_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {MODEL_ROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "stream": True,
                },
                timeout=120,
                stream=True,
            )
            if resp.status_code != 200:
                if OPENROUTER_API_KEY:
                    full = yield from self._stream_openrouter(
                        prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p
                    )
                    return full
                msg = f"[ERR] 9router błąd {resp.status_code}: {resp.text[:300]}"
                yield msg
                return msg
            for line in resp.iter_lines():
                if not line:
                    continue
                decoded = line.decode("utf-8", errors="replace")
                if decoded.startswith("data: ") and decoded != "data: [DONE]":
                    try:
                        obj = json.loads(decoded[6:])
                        delta = obj.get("choices", [{}])[0].get("delta", {})
                        chunk = delta.get("content", "")
                        if chunk:
                            full += chunk
                            yield chunk
                    except json.JSONDecodeError:
                        pass
            if not full:
                if OPENROUTER_API_KEY:
                    full = yield from self._stream_openrouter(
                        prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p
                    )
                    return full
                msg = "[ERR] Brak odpowiedzi z 9router (stream)"
                yield msg
                full = msg
        except Exception as e:
            if OPENROUTER_API_KEY:
                full = yield from self._stream_openrouter(
                    prompt, OPENROUTER_FALLBACK_MODEL, max_tokens, temperature, top_p
                )
                return full
            msg = f"[ERR] 9router stream wyjątek: {str(e)}"
            yield msg
            full = msg
        return full

    def list_models(self) -> dict:
        groups = {}
        if MYBONZO_BASE_URL:
            groups["MyBonzo Edge (Workers AI Free)"] = [{"name": name, "id": model_id} for name, model_id in MYBONZO_MODELS.items()]
        if self.router_enabled:
            groups["9Router Chains"] = [{"name": name, "id": model_id} for name, model_id in ROUTER_MODELS.items()]
        groups["OpenRouter Direct"] = [{"name": name, "id": model_id} for name, model_id in OPENROUTER_MODELS.items()]
        groups["OpenAI Direct"] = [{"name": name, "id": model_id} for name, model_id in OPENAI_MODELS.items()]

        # Drop empty groups to keep UI clean when one provider is intentionally unavailable.
        groups = {k: v for k, v in groups.items() if v}
        return {
            "provider": self.provider,
            "default": self.default_model_name,
            "default_id": self.default_model_id,
            "router": {
                "enabled": self.router_enabled,
                "base_url": self.router_base_url,
                "default_model": MODEL_ROUTER_DEFAULT_MODEL,
            },
            "recommended": {
                "chat_chain": MYBONZO_MODELS["MyBonzo Llama 3.3 70B (Edge Free)"] if MYBONZO_BASE_URL else ROUTER_MODELS["BUCH Router Chat Chain"],
                "agent_chain": MYBONZO_MODELS["MyBonzo Llama 3.3 70B (Edge Free)"] if MYBONZO_BASE_URL else ROUTER_MODELS["BUCH Router Agent Chain"],
                "experimental_chain": MYBONZO_MODELS["MyBonzo Llama 3.2 3B (Edge Fast)"] if MYBONZO_BASE_URL else ROUTER_MODELS["BUCH Router Experimental Chain"],
                "chat_primary": "MyBonzo Llama 3.3 70B (Edge Free)" if MYBONZO_BASE_URL else OPENROUTER_DEFAULT_MODEL,
                "chat_secondary": OPENROUTER_SECONDARY_MODEL,
                "chat_fallback": OPENROUTER_FALLBACK_MODEL,
                "agent_primary": AGENT_MODEL_PRIMARY,
                "agent_secondary": AGENT_MODEL_SECONDARY,
                "agent_experimental": AGENT_MODEL_EXPERIMENTAL,
            },
            "groups": groups,
        }


class SpeechService:
    """
    Speech API service (OpenAI-compatible endpoint).
    Works with API keys only (no local models).
    """
    def __init__(self):
        self.api_key = SPEECH_API_KEY
        self.base_url = SPEECH_API_BASE_URL
        self.stt_model = STT_MODEL
        self.tts_model = TTS_MODEL
        self.tts_voice = TTS_VOICE

    def is_configured(self) -> bool:
        return bool(self.api_key and self.base_url)

    def transcribe(self, file_bytes: bytes, filename: str, language: str = "pl", prompt: Optional[str] = None) -> str:
        if not self.is_configured():
            raise RuntimeError("Speech API nie skonfigurowane (SPEECH_API_KEY / OPENAI_API_KEY)")
        files = {"file": (filename, file_bytes)}
        data = {"model": self.stt_model, "language": language}
        if prompt:
            data["prompt"] = prompt
        resp = requests.post(
            f"{self.base_url}/audio/transcriptions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            files=files,
            data=data,
            timeout=120,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"STT błąd {resp.status_code}: {resp.text[:400]}")
        body = resp.json()
        return body.get("text", "")

    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        audio_format: str = "mp3",
        instructions: Optional[str] = None,
    ) -> bytes:
        if not self.is_configured():
            raise RuntimeError("Speech API nie skonfigurowane (SPEECH_API_KEY / OPENAI_API_KEY)")
        payload = {
            "model": self.tts_model,
            "voice": voice or self.tts_voice,
            "input": text,
            "format": audio_format,
        }
        if instructions:
            payload["instructions"] = instructions
        resp = requests.post(
            f"{self.base_url}/audio/speech",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"TTS błąd {resp.status_code}: {resp.text[:400]}")
        return resp.content


# Backward compat alias
LocalModel = MultiProviderModel
