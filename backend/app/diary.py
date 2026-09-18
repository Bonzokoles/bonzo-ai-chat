# -*- coding: utf-8 -*-
"""
System dziennika użytkownika.
Zapisuje ważne momenty z rozmów i buduje profil użytkownika.
"""
import json
import threading
import os
from pathlib import Path
from datetime import datetime

_APP_DIR    = Path(__file__).resolve().parent
_BUCH_ROOT   = _APP_DIR.parent.parent
_KB_DIR      = Path(os.getenv("KB_DIR", str(_BUCH_ROOT / "knowledge_mood")))
_BRAIN_DIR   = _BUCH_ROOT / "The_brain"

def _get_diary_file() -> Path:
    brain_file = _BRAIN_DIR / "bonzo_diary.json"
    if brain_file.exists():
        return brain_file
    return _KB_DIR / "bonzo_diary.json"

def _get_diary_log() -> Path:
    brain_log = _BRAIN_DIR / "bonzo_diary_log.jsonl"
    if brain_log.exists():
        return brain_log
    return _KB_DIR / "bonzo_diary_log.jsonl"

_DIARY_FILE = _get_diary_file()
_DIARY_LOG  = _get_diary_log()
_USER_NAME = os.getenv("USER_NAME", "Bonzo")
_ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "EASTWOOD")

_EMPTY = {
    "facts": [],
    "moments": [],
    "preferences": [],
    "goals": [],
    "decisions": [],
    "last_updated": None,
}


class BonzoDiary:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = self._load()

    def _load(self) -> dict:
        if _DIARY_FILE.exists():
            try:
                with open(_DIARY_FILE, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return dict(_EMPTY)

    def _save(self):
        _KB_DIR.mkdir(parents=True, exist_ok=True)
        self._data["last_updated"] = datetime.now().isoformat()
        with open(_DIARY_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # ── public API ────────────────────────────────────────────────────────────

    def log_turn(self, user_msg: str, assistant_msg: str):
        """Zapisuje turę rozmowy do logu JSONL (raw)."""
        _KB_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts":        datetime.now().isoformat(),
            "user":      user_msg[:1000],
            "assistant": assistant_msg[:600],
        }
        with self._lock:
            with open(_DIARY_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def add_fact(self, fact: str):
        """Dodaje fakt o użytkowniku (deduplikuje, max 150)."""
        fact = fact.strip()
        if not fact or len(fact) < 6:
            return
        with self._lock:
            if fact not in self._data["facts"]:
                self._data["facts"].append(fact)
                self._data["facts"] = self._data["facts"][-150:]
                self._save()

    def add_moment(self, summary: str, tags: list = None):
        """Dodaje ważny moment do dziennika (max 60)."""
        with self._lock:
            self._data["moments"].append({
                "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
                "summary": summary.strip(),
                "tags":    tags or [],
            })
            self._data["moments"] = self._data["moments"][-60:]
            self._save()

    def add_preference(self, pref: str):
        pref = pref.strip()
        if not pref or len(pref) < 4:
            return
        with self._lock:
            if pref not in self._data["preferences"]:
                self._data["preferences"].append(pref)
                self._data["preferences"] = self._data["preferences"][-150:]
                self._save()

    def add_goal(self, goal: str):
        goal = goal.strip()
        if not goal or len(goal) < 6:
            return
        with self._lock:
            if goal not in self._data["goals"]:
                self._data["goals"].append(goal)
                self._data["goals"] = self._data["goals"][-120:]
                self._save()

    def add_decision(self, topic: str, recommendation: str, rationale: str = "", confidence: str = "medium"):
        with self._lock:
            self._data["decisions"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": topic.strip()[:300],
                "recommendation": recommendation.strip()[:1200],
                "rationale": rationale.strip()[:2000],
                "confidence": confidence,
            })
            self._data["decisions"] = self._data["decisions"][-200:]
            self._save()

    def get_facts(self) -> list:
        return list(self._data.get("facts", []))

    def get_moments(self) -> list:
        return list(self._data.get("moments", []))

    def get_preferences(self) -> list:
        return list(self._data.get("preferences", []))

    def get_goals(self) -> list:
        return list(self._data.get("goals", []))

    def get_decisions(self) -> list:
        return list(self._data.get("decisions", []))

    def get_summary(self, max_facts: int = 25, max_moments: int = 5) -> str:
        """Zwraca podsumowanie do wstrzyknięcia w system prompt."""
        facts = self._data.get("facts", [])[-max_facts:]
        moments = self._data.get("moments", [])[-max_moments:]
        prefs = self._data.get("preferences", [])[-10:]
        goals = self._data.get("goals", [])[-10:]
        decisions = self._data.get("decisions", [])[-5:]
        if not facts and not moments and not prefs and not goals and not decisions:
            return ""
        parts = [f"\n\n=== CO WIEM O {_USER_NAME.upper()} ==="]
        if facts:
            parts.append("Fakty:")
            parts.extend(f"  - {f}" for f in facts)
        if prefs:
            parts.append("Preferencje:")
            parts.extend(f"  - {p}" for p in prefs)
        if goals:
            parts.append("Cele:")
            parts.extend(f"  - {g}" for g in goals)
        if moments:
            parts.append("Kluczowe momenty:")
            for m in moments:
                tags = f" [{', '.join(m['tags'])}]" if m.get("tags") else ""
                parts.append(f"  - [{m['date']}]{tags} {m['summary']}")
        if decisions:
            parts.append("Ostatnie decyzje:")
            for d in decisions:
                parts.append(f"  - [{d['date']}] {d['topic']} -> {d['recommendation']} ({d.get('confidence','medium')})")
        parts.append("=========================")
        return "\n".join(parts)

    def clear(self):
        with self._lock:
            self._data = dict(_EMPTY)
            self._save()


# ── singleton ─────────────────────────────────────────────────────────────────

_diary_instance: "BonzoDiary | None" = None
_diary_lock = threading.Lock()


def get_diary() -> BonzoDiary:
    global _diary_instance
    if _diary_instance is None:
        with _diary_lock:
            if _diary_instance is None:
                _diary_instance = BonzoDiary()
    return _diary_instance


# ── async fact extraction ─────────────────────────────────────────────────────

def extract_facts_async(model, user_msg: str, assistant_msg: str):
    """
    W tle ekstrahuje fakty o użytkowniku z tury rozmowy.
    Wywołuje LLM z małym promptem ekstrakcyjnym (temperatura 0.2).
    """
    if len(user_msg.strip()) < 40:
        return  # za krótka wiadomość — nic ciekawego

    def _run():
        try:
            prompt = (
                "Jesteś ekstraherem faktów. Przeanalizuj tę wymianę i podaj TYLKO "
                f"konkretne fakty o użytkowniku '{_USER_NAME}' — jego projekty, zainteresowania, "
                "umiejętności, preferencje, ważne rzeczy które ujawnił o sobie. "
                "Każdy fakt w osobnej linii zaczynającej się od '-'. "
                f"Jeśli nie ma żadnych faktów o {_USER_NAME}, napisz tylko: BRAK\n\n"
                f"{_USER_NAME}: {user_msg[:600]}\n"
                f"{_ASSISTANT_NAME}: {assistant_msg[:400]}\n\n"
                f"Fakty o {_USER_NAME}:"
            )
            small_model = getattr(model, "get_small_model_name", lambda: None)()
            result = model.generate(prompt, max_tokens=200, temperature=0.2, model_name=small_model)
            if not result or result.strip().upper().startswith("BRAK"):
                return
            diary = get_diary()
            for line in result.splitlines():
                line = line.strip().lstrip("-•*").strip()
                if line and len(line) > 8:
                    diary.add_fact(line)
        except Exception as e:
            print(f"[Diary] Blad ekstrakcji faktow: {e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()


def extract_profile_async(model, user_msg: str, assistant_msg: str):
    """
    W tle: ekstrahuje preferencje i cele użytkownika.
    """
    if len(user_msg.strip()) < 40:
        return

    def _run():
        try:
            prompt = (
                f"Wyciągnij profil użytkownika {_USER_NAME} z wymiany.\n"
                "Zwróć JSON z polami: preferences (lista string), goals (lista string).\n"
                "Tylko JSON, bez komentarza.\n\n"
                f"{_USER_NAME}: {user_msg[:800]}\n"
                f"{_ASSISTANT_NAME}: {assistant_msg[:400]}\n"
            )
            small_model = getattr(model, "get_small_model_name", lambda: None)()
            raw = model.generate(prompt, max_tokens=220, temperature=0.1, model_name=small_model)
            start = raw.find("{")
            end = raw.rfind("}")
            if start == -1 or end == -1:
                return
            payload = json.loads(raw[start:end + 1])
            diary = get_diary()
            for p in payload.get("preferences", [])[:10]:
                if isinstance(p, str):
                    diary.add_preference(p)
            for g in payload.get("goals", [])[:10]:
                if isinstance(g, str):
                    diary.add_goal(g)
        except Exception as e:
            print(f"[Diary] Blad ekstrakcji profilu: {e}")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
