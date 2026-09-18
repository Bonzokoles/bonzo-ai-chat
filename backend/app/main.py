# -*- coding: utf-8 -*-
import sys
import io
import os

# Force UTF-8 encoding for Windows console (skip under pytest)
if sys.platform == 'win32' and 'pytest' not in sys.modules and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

from dotenv import load_dotenv
from pathlib import Path

# Load local .env from the root of The_Buch
app_dir = Path(__file__).resolve().parent
buch_dir = app_dir.parent.parent
local_env = buch_dir / ".env"
if local_env.exists():
    load_dotenv(local_env)

# Load master .env from the workspace root (S:\BONZO_I_DO_SHELL_SHOP)
master_env = Path("S:/BONZO_I_DO_SHELL_SHOP/.env")
if master_env.exists():
    load_dotenv(master_env)
else:
    alt_master = buch_dir.parent.parent / ".env"
    if alt_master.exists():
        load_dotenv(alt_master)

from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import json
import shutil
import asyncio
import shutil as _shutil
import re
import requests
from bs4 import BeautifulSoup
import boto3
from pathlib import Path as _Path
from datetime import datetime
from sqlalchemy import func
from model import LocalModel, SpeechService
from db import SessionLocal, init_db, Conversation, Message
from mcp_tools import mcp_registry, parse_tool_call_from_text
from typing import List, Optional
import deal_ops_loader as deal_ops_module
import private_help_loader as private_help_module
import coding_rules_loader as coding_rules_module

APP_NAME = os.getenv("APP_NAME", "EastWood Ops")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "EASTWOOD")
USER_NAME = os.getenv("USER_NAME", "Bonzo")
KB_LABEL = os.getenv("KB_LABEL", "KNOWLEDGE MOOD")
RERANK_PROVIDER = os.getenv("RERANK_PROVIDER", "cohere")
RERANK_MODEL = os.getenv("RERANK_MODEL", "rerank-v4.0-fast")
MODEL_ROUTER_BASE_URL = os.getenv("MODEL_ROUTER_BASE_URL", "http://127.0.0.1:20128/v1")
MODEL_ROUTER_ENABLED = os.getenv("MODEL_ROUTER_ENABLED", "false").strip().lower() in {"1", "true", "yes", "on"}
KB_DIR_DEFAULT = _shutil.os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "knowledge_mood")
ACTIVE_CHAT_REQUESTS = 0
ACTIVE_TERMINAL_WS = 0
TASK_PROFILES = {
    "default": {
        "label": "Default",
        "description": "Ogólny tryb BUCH do pracy operacyjnej.",
        "model_name": None,
        "tools": True,
        "kb_scope": [],
        "char_scope": [],
        "use_character_examples": True,
        "system_append": "",
    },
    "shop_help": {
        "label": "Shop Help",
        "description": "Pomoc przy sklepie, katalogu, produktach i wdrożeniu.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": ["PINKY_one"],
        "char_scope": [],
        "use_character_examples": True,
        "system_append": (
            "\n\nTRYB ZADANIA: SHOP HELP\n"
            "- skupiasz się na sklepie, produktach, katalogu, opisach, Shopify i operacji sklepu\n"
            "- jeśli pytanie dotyczy wdrożenia, dajesz kolejność działań i ryzyka\n"
            "- jeśli pytanie dotyczy panelu lub produktu, mówisz konkretnie co sprawdzić i gdzie kliknąć"
        ),
    },
    "shopify": {
        "label": "Shopify",
        "description": "Tryb pod Shopify Admin, katalog, warianty, kolekcje i synchronizację.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": ["PINKY_one"],
        "char_scope": [],
        "use_character_examples": True,
        "system_append": (
            "\n\nTRYB ZADANIA: SHOPIFY\n"
            "- skupiasz się na Shopify Admin, produktach, wariantach, kolekcjach, tagach i synchronizacji danych\n"
            "- rozróżniasz storefront od panelu admina i mówisz jasno, którego obszaru dotyczy odpowiedź\n"
            "- jeśli temat dotyczy wdrożenia albo syncu, dajesz kolejność działań, zależności i test końcowy\n"
            "- jeśli ryzyko dotyczy scope'ów, tokenów albo zapisu danych, mówisz to wprost"
        ),
    },
    "private_help": {
        "label": "Private Help",
        "description": "Prywatna pomoc operacyjna: sklep, platforma, konfiguracja i codzienna obsługa.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": ["PINKY_one"],
        "char_scope": [],
        "use_character_examples": True,
        "system_append": (
            "\n\nTRYB ZADANIA: PRIVATE HELP\n"
            "- pracujesz na prywatnej wiedzy operacyjnej sklepu i platformy\n"
            "- priorytet mają ustawienia, konfiguracja, panel, checklisty i codzienna obsługa\n"
            "- najpierw opierasz się na lokalnych plikach PINKY_one i prywatnym kontekście tego workspace\n"
            "- jeśli pytanie dotyczy panelu lub wdrożenia, odpowiadasz w układzie: gdzie to jest, co sprawdzić, co kliknąć, jakie zmienne/env są ważne\n"
            "- nie odsyłasz odruchowo do ogólnej dokumentacji Shopify, jeśli odpowiedź jest już w lokalnych plikach\n"
            "- nie mieszasz tego trybu z agentami handlowymi ani strategią deali, chyba że użytkownik wyraźnie tego chce"
        ),
    },
    "agent_ops": {
        "label": "Agent Ops",
        "description": "Tryb do agentów, workflow i automatyzacji.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": ["the_deal_BOYS"],
        "char_scope": ["agent_ops", "deal_ops", "strategy"],
        "use_character_examples": False,
        "system_append": (
            "\n\nTRYB ZADANIA: AGENT OPS\n"
            "- rozbijasz zadania na kroki, wejścia, wyjścia i warunki błędu\n"
            "- priorytetem jest niezawodność przepływu, nie efektowność\n"
            "- gdy czegoś brakuje, wskazujesz brakujący kontrakt lub integrację"
        ),
    },
    "research": {
        "label": "Research",
        "description": "Tryb do researchu, porównań i zbierania materiałów.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": [],
        "char_scope": [],
        "use_character_examples": False,
        "system_append": (
            "\n\nTRYB ZADANIA: RESEARCH\n"
            "- rozdzielasz fakty, hipotezy i decyzje\n"
            "- jeśli porównujesz opcje, kończysz krótkim werdyktem i jednym zaleceniem\n"
            "- bez nadmuchanego języka i bez zgadywania"
        ),
    },
    "deal_ops": {
        "label": "Deal Ops",
        "description": "Strategia deali, sourcing, marże, B2B i logika przyszłych Polaczków.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": ["the_deal_BOYS"],
        "char_scope": ["deal_ops", "strategy", "b2b"],
        "use_character_examples": False,
        "system_append": (
            "\n\nTRYB ZADANIA: DEAL OPS\n"
            "- pracujesz na strategicznej wiedzy dealowej: sourcing, marże, B2B, lejki i ryzyka handlowe\n"
            "- traktujesz Polaczki i orkiestrator jako osobny subsystem, nie jako domyślną część BUCH\n"
            "- nie mieszasz prywatnej pomocy operacyjnej sklepu z logiką dealową, jeśli nie ma takiej potrzeby\n"
            "- odpowiedzi mają kończyć się werdyktem operacyjnym: kup/odpuść/sprawdź/eskaluj"
        ),
    },
    "content": {
        "label": "Content",
        "description": "Tryb do opisów i treści sprzedażowych bez papki.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": False,
        "kb_scope": ["PINKY_one"],
        "char_scope": ["content", "sales"],
        "use_character_examples": True,
        "system_append": (
            "\n\nTRYB ZADANIA: CONTENT\n"
            "- piszesz jasno, konkretnie i po ludzku\n"
            "- zero korpo-sloganu i sztucznego zachwytu\n"
            "- jeśli tworzysz tekst sprzedażowy, ma być wiarygodny i użyteczny"
        ),
    },
    "debug": {
        "label": "Debug",
        "description": "Tryb do szukania błędów, przyczyn i fixów.",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": [],
        "char_scope": ["debug", "technical"],
        "use_character_examples": False,
        "system_append": (
            "\n\nTRYB ZADANIA: DEBUG\n"
            "- najpierw ustalasz objaw, potem przyczynę, potem fix\n"
            "- nie zgadujesz; jeśli czegoś nie widać, mówisz czego brakuje\n"
            "- kończysz krótkim testem potwierdzającym"
        ),
    },
    "coding": {
        "label": "Coding & Architecture",
        "description": "Zasady czystego kodu, architektury i wzorców (14 książek z The_brain/coding/agent-rules-books).",
        "model_name": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "tools": True,
        "kb_scope": [],
        "char_scope": ["coding", "technical", "architecture"],
        "use_character_examples": False,
        "system_append": (
            "\n\nTRYB ZADANIA: CODING & ARCHITECTURE\n"
            "- rygorystycznie stosujesz reguły Clean Code, Clean Architecture, DDD, Refactoring oraz Pragmatic Programmer\n"
            "- eliminujesz ukryte mutacje, flagi w argumentach i mieszanie poziomów abstrakcji\n"
            "- kod musi być testowalny, modularny i pozbawiony długu technologicznego\n"
            "- przy każdej propozycji podajesz komendę lub test weryfikacyjny"
        ),
    },
}

# Inicjalizacja
app = FastAPI(title=APP_NAME)

# CORS Configuration - umoĹĽliwia poĹ‚Ä…czenia z frontendu
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import embeddings as embed_module
import diary as diary_module

print(f"[START] Inicjalizacja {APP_NAME} Backend...")
model = LocalModel()  # auto-wykrywa OpenRouter / OpenAI / Ollama
speech = SpeechService()
init_db()
embed_module.start_background_build()  # semantic index buduje się w tle
print("[OK] Backend gotowy! (embeddings budują się w tle)")

class ChatRequest(BaseModel):
    messages: List[dict]  # [{role: "user"|'assistant'|'system', text: "..."}]
    max_tokens: int = 512
    use_tools: bool = True  # Czy uĹĽywaÄ‡ MCP tools
    temperature: float = 0.6
    top_p: float = 0.9
    model_name: Optional[str] = None  # JeĹ›li None, uĹĽywa domyĹ›lnego
    task_profile: Optional[str] = None


class ChatWebhookRequest(BaseModel):
    text: str
    task_profile: Optional[str] = "shop_help"
    model_name: Optional[str] = None
    use_tools: bool = True
    max_tokens: int = 700
    temperature: float = 0.5
    top_p: float = 0.9
    custom_system_prompt: Optional[str] = None
    meta: dict = {}


class DealOpsContextRequest(BaseModel):
    query: str
    top_k: int = 5


class PrivateHelpContextRequest(BaseModel):
    query: str
    top_k: int = 5


class WebIngestRequest(BaseModel):
    url: str
    title: Optional[str] = None
    tags: List[str] = []
    max_chars: int = 20000


class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    format: str = "mp3"
    style_preset: Optional[str] = None


class TMDBIngestRequest(BaseModel):
    query: str
    limit: int = 5


class WebResearchRequest(BaseModel):
    query: str
    max_results: int = 5


class R2PushRequest(BaseModel):
    prefix: str = "knowledge_mood"
    only_ext: List[str] = [".md", ".txt", ".json", ".csv", ".py"]


class DecisionRequest(BaseModel):
    topic: str
    options: List[str] = []
    constraints: List[str] = []


def _kb_dir() -> _Path:
    d = _Path(os.getenv("KB_DIR", KB_DIR_DEFAULT))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _excerpt(text: str, limit: int = 140) -> str:
    text = " ".join((text or "").split())
    return text[:limit] + ("…" if len(text) > limit else "")


def _file_count(path: _Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for p in path.rglob("*") if p.is_file())


def _db_overview(db) -> dict:
    conversation_count = db.query(func.count(Conversation.id)).scalar() or 0
    message_count = db.query(func.count(Message.id)).scalar() or 0
    messages_by_role = {
        role or "unknown": count
        for role, count in db.query(Message.role, func.count(Message.id)).group_by(Message.role).all()
    }
    recent_conversations = []
    for conv in db.query(Conversation).order_by(Conversation.created_at.desc()).limit(5).all():
        msg_count = db.query(func.count(Message.id)).filter(Message.conversation_id == conv.id).scalar() or 0
        last_msg = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.created_at.desc(), Message.id.desc())
            .first()
        )
        recent_conversations.append({
            "id": conv.id,
            "created_at": conv.created_at.isoformat() if conv.created_at else None,
            "message_count": msg_count,
            "last_role": last_msg.role if last_msg else None,
            "last_excerpt": _excerpt(last_msg.content, 180) if last_msg else "",
        })
    recent_messages = [
        {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "role": msg.role,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
            "excerpt": _excerpt(msg.content, 180),
        }
        for msg in db.query(Message).order_by(Message.created_at.desc(), Message.id.desc()).limit(8).all()
    ]
    return {
        "conversation_count": conversation_count,
        "message_count": message_count,
        "messages_by_role": messages_by_role,
        "recent_conversations": recent_conversations,
        "recent_messages": recent_messages,
    }


def _diagnostics_snapshot() -> dict:
    db = SessionLocal()
    try:
        diary = diary_module.get_diary()
        kb_dir = _kb_dir()
        kb_files = []
        for p in sorted(kb_dir.rglob("*")):
            if p.is_file():
                kb_files.append(str(p.relative_to(kb_dir)))
        db_overview = _db_overview(db)
        return {
            "generated_at": datetime.now().isoformat(),
            "app_name": APP_NAME,
            "assistant_name": ASSISTANT_NAME,
            "user_name": USER_NAME,
            "health": {
                "status": "ok",
                "provider": model.provider,
                "default_model": model.default_model_name,
                "embeddings_ready": embed_module.is_ready(),
                "speech_api_configured": speech.is_configured(),
                "terminal_available": _HAS_WINPTY,
                "model_router_enabled": MODEL_ROUTER_ENABLED,
                "model_router_base_url": MODEL_ROUTER_BASE_URL,
            },
            "runtime": {
                "active_chat_requests": ACTIVE_CHAT_REQUESTS,
                "active_terminal_connections": ACTIVE_TERMINAL_WS,
                "python_executable": sys.executable,
            },
            "database": db_overview,
            "diary": {
                "facts": diary.get_facts(),
                "moments": diary.get_moments(),
                "preferences": diary.get_preferences(),
                "goals": diary.get_goals(),
                "decisions": diary.get_decisions(),
                "summary": diary.get_summary(),
            },
            "knowledge": {
                "dir": str(kb_dir),
                "file_count": len(kb_files),
                "sample_files": kb_files[:12],
            },
            "task_profiles": [
                {
                    "key": key,
                    "label": value["label"],
                    "description": value["description"],
                    "model_name": value["model_name"],
                    "kb_scope": value["kb_scope"],
                    "char_scope": value["char_scope"],
                }
                for key, value in TASK_PROFILES.items()
            ],
            "tools": mcp_registry.list_tools(),
            "recent_activity": db_overview["recent_messages"][:5],
        }
    finally:
        db.close()


def _build_default_system_prompt(
    diary_summary: str = "",
    tools_rules: str = "",
    char_inject: str = "",
    kb_context: str = "",
    files_context: str = "",
):
    return f"""Jesteś {ASSISTANT_NAME} (BUCH / JIMBO) – Senior Software Architect & Automation Guru operujący w ekosystemie Bonzo (standard K.R.A.F.T. v3).

ROLA I ARCHITEKTURA STANOWISKA:
- Pracujesz w centrum dowodzenia The Buch (EastWood Ops, port 4149).
- Twoim partnerem i zleceniodawcą jest {USER_NAME}.
- Masz zintegrowane dwa okna operacyjne: Chat AI (po lewej) oraz interaktywny terminal PowerShell 7 Core (pwsh.exe po prawej z obsługą PTY).
- Ignorujesz uprzejmości i marketingowy bełkot. Działasz z chirurgiczną precyzją techniczną.
- Używaj tagów statusu: [OK], [RUN], [WARN], [ERR]. Kategoryczny zakaz używania emoji.
- Odpowiedzi formułujesz konkretnie: wskazujesz dokładny plik, logikę i gotową komendę CLI.

INTEGRACJA Z TERMINALEM POWERSHELL (PRAWE OKNO):
- Prawy panel to natywna sesja PowerShell 7 Core (pwsh.exe) w katalogu roboczym.
- Gdy proponujesz uruchomienie skryptu, testu, komendy diagnostycznej lub polecenia CLI, ZAWSZE umieszczaj je w bloku kodu ```powershell.
- Interfejs The Buch wyposażony jest w przycisk [run] przy każdym bloku kodu powłoki – {USER_NAME} może jednym kliknięciem wysłać polecenie bezpośrednio do terminala.
- Zawsze podawaj kompletne ścieżki i parametry, aby polecenie było natychmiast wykonywalne bez poprawek.

MAPA EKOSYSTEMU, DYSKÓW I NARZĘDZI:
1. Z:\\.Goose_agent\\ — Centrum Skryptów i Launcherów:
   - START_THE_BUCH.ps1: Uruchamia lub weryfikuje serwer The Buch (port 4149).
   - START_AGENT_PI_MYBONZO.ps1: Uruchamia Agenta Pi zintegrowanego z bramą Cloudflare Workers AI.
   - START_GOOSE_MYBONZO.ps1: Uruchamia Agenta Goose zintegrowanego z MyBonzo.
   - LAUNCH_GOOSE_AGENT_CENTER.ps1: Interaktywne menu launcherów.
   - check_env.ps1: Diagnostyka środowiska (PowerShell 7, Node v24, Python 3.13, Git).
   - test_gateway.ps1: Test latencji i statusu bramy MyBonzo Cloudflare AI.

2. Z:\\36_chambers\\The_Buch\\ — Baza The Buch:
   - Port 4149: FastAPI backend + xterm.js terminal + Chat AI.
   - Brama modeli: MyBonzo Cloudflare AI (@cf/meta/llama-3.3-70b-instruct-fp8-fast).

3. U:\\WWW_Zen_BRo_wser_tool\\ — Hub Narzędziowy i Silnik ETL (JIMBO_KIT, port 4111):
   - meblepumo.db: Baza SQLite (36 MB) zawierająca produkty, marże, kategorie, break-even.
   - AGENT_Pi_TOOLS\\CAY_FEED_conventer\\: Konwerter feedów produktowych XML/YAML/CSV do JSON.
   - AGENT_Pi_TOOLS\\I_Do_INDexer\\: Asynchroniczny indekser metadanych katalogów do SQLite.
   - AGENT_Pi_TOOLS\\Tabularis_Importer\\: Streamingowy importer JSON/CSV do SQLite.
   - database\\etl\\diff_processor.py: Codzienny procesor diffów i snapshotów bazy meblepumo.db.
   - database\\stolarska\\adapter.js: Adapter domenowy stolarki (normalizacja projektów, KPI, koszty).
   - JIMBOKIT_COMMS\\: Kolejki zadań i komunikacja plikowa IPC między agentami.

4. U:\\WWW_Zen_BRo_wser_org3\\ — ZENO Browser (Dual-Target Desktop & Cloud):
   - Desktop: Electron 27 z 33 narzędziami MCP (stdio + SSE).
   - Cloudflare Pages: zeno-browser-web (zenbrowsers.org).
   - D1 Database: zeno-browser-db (ddac77ec-fe9e-4b5b-b3f5-ba0793152917).
   - R2 Storage: zen-static-assets (7f490d58a478c6baccb0ae01ea1d87c3.r2.cloudflarestorage.com).

5. F:\\GENINI_ANTGRAV\\workspace\\ — Główny obszar roboczy projektów.
   - Kategoryczny zakaz tworzenia plików projektowych na dysku C:.
   - Kopie zapasowe: F:\\GENINI_ANTGRAV\\backup\\.

6. R:\\repos\\active\\ — Repozytoria Git.
   - Pamięć długoterminowa: R:\\mempalace\\ (wing_bonzo, wing_yutro, wing_devz).

WYTYCZNE OPERACYJNE DLA ODPOWIEDZI:
- Komunikacja z {USER_NAME} w języku polskim. Kod, nazwy zmiennych, ścieżki i zapytania SQL po angielsku.
- Zero pustych pytań na końcu typu \"Co o tym sądzisz?\". Kończ konkretnym werdyktem, gotową komendą PowerShell do uruchomienia lub kolejnym krokiem wdrożeniowym.
- Gdy {USER_NAME} pyta co zrobić w projekcie, podaj plan w punktach z gotowymi komendami do wklejenia w terminal.{diary_summary}{tools_rules}{char_inject}{kb_context}{files_context}"""


def _resolve_task_profile(task_profile: Optional[str]):
    key = (task_profile or "default").strip().lower()
    return key, TASK_PROFILES.get(key, TASK_PROFILES["default"])


def _apply_task_profile(
    task_profile: Optional[str],
    model_name: Optional[str],
    use_tools: bool,
    custom_system_prompt: Optional[str],
):
    profile_key, profile = _resolve_task_profile(task_profile)
    selected_model = model_name or profile.get("model_name")
    selected_tools = use_tools if use_tools is not None else bool(profile.get("tools", True))
    prompt_tail = profile.get("system_append", "")
    merged_prompt = (custom_system_prompt or "").strip()
    if prompt_tail:
        merged_prompt = f"{merged_prompt}\n\n{prompt_tail}".strip() if merged_prompt else prompt_tail.strip()
    return profile_key, profile, selected_model, selected_tools, (merged_prompt or None)


def _resolve_response_meta(selected_model_name: Optional[str]):
    provider_used, model_id_used = model._resolve_model(selected_model_name)
    return {
        "provider": provider_used,
        "model_id": model_id_used,
        "model_display": model._display_name_for_id(model_id_used),
        "model_requested": selected_model_name or model.default_model_id,
    }


def _profile_kb_scope(profile: dict) -> List[str]:
    raw_scope = profile.get("kb_scope") or []
    return [str(item).strip() for item in raw_scope if str(item).strip()]


def _profile_char_scope(profile: dict) -> List[str]:
    raw_scope = profile.get("char_scope") or []
    return [str(item).strip() for item in raw_scope if str(item).strip()]


def _webhook_tools_rules(use_tools: bool) -> str:
    if not use_tools:
        return ""
    tool_names = ", ".join(mcp_registry.list_tools())
    return f"""
NARZĘDZIA MCP — ZASADY:
- Masz dostęp TYLKO do: {tool_names}
- Użyj formatu: [TOOL:nazwa]argument[/TOOL]
- NIE WYMYŚLAJ danych (CPU%, RAM%, procesy, IP, sieć) — powiedz że brak narzędzia
  - Jeśli pytanie wymaga czegoś czego nie masz — przyznaj to wprost"""


def _format_kb_hits_block(title: str, hits: List[dict]) -> str:
    if not hits:
        return ""
    parts = []
    for hit in hits:
        source = hit.get("source", "unknown")
        score = hit.get("score")
        match_type = hit.get("match_type")
        suffix = []
        if score is not None:
            try:
                suffix.append(f"score={float(score):.2f}")
            except (TypeError, ValueError):
                pass
        if match_type:
            suffix.append(f"mode={match_type}")
        header = f"--- {source}"
        if suffix:
            header += " (" + ", ".join(suffix) + ")"
        header += " ---"
        parts.append(f"{header}\n{hit.get('text', '')}")
    return f"\n\n--- {title} ---\n" + "\n\n".join(parts) + "\n---"


def _build_private_help_context(query: str, top_k: int = 3):
    if not query.strip():
        return "", []
    hits = []
    if embed_module.is_ready():
        hits = embed_module.get_index().semantic_search_kb(
            query,
            top_k=max(1, min(top_k, 10)),
            include_prefixes=["PINKY_one"],
        )
    if not hits:
        hits = private_help_module.search_docs(
            query,
            limit=max(1, min(top_k, 10)),
        )
    if not hits:
        return "", []
    context = _format_kb_hits_block("KONTEKST PRIVATE HELP Z PINKY_one", hits)
    return context, hits


def _hit_sources(hits: List[dict]) -> List[str]:
    return list(dict.fromkeys(hit.get("source", "") for hit in hits if hit.get("source")))


def _profile_context(query: str, task_profile_key: str, task_profile_def: dict):
    kb_scope = _profile_kb_scope(task_profile_def)
    char_scope = _profile_char_scope(task_profile_def)
    use_character_examples = bool(task_profile_def.get("use_character_examples", True))
    char_inject = ""
    kb_context = ""
    kb_hits = []
    if not query.strip() or not embed_module.is_ready():
        if task_profile_key == "private_help":
            kb_context, kb_hits = _build_private_help_context(query, top_k=3)
        elif task_profile_key in {"coding", "debug"}:
            coding_ctx, rule_sources = coding_rules_module.build_coding_context(query, tier="nano", limit=2)
            if coding_ctx:
                kb_context = coding_ctx
                kb_hits = [{"source": src, "text": "", "score": 1.0} for src in rule_sources]
        return {
            "kb_scope": kb_scope,
            "char_scope": char_scope,
            "use_character_examples": use_character_examples,
            "char_inject": char_inject,
            "kb_context": kb_context,
            "kb_hits": kb_hits,
        }

    examples = []
    if use_character_examples:
        examples = embed_module.get_index().find_character_examples(
            query,
            top_k=3,
            allowed_styles=char_scope,
        )
    if examples:
        char_inject = f"\n\nPrzykłady jak {ASSISTANT_NAME} odpowiada (dobrane do tematu):\n---\n"
        char_inject += "\n\n".join([e["text"] for e in examples])
        char_inject += "\n---"

    kb_hits = embed_module.get_index().semantic_search_kb(
        query,
        top_k=3,
        include_prefixes=kb_scope,
    )
    if kb_hits:
        kb_context = _format_kb_hits_block("KONTEKST Z BAZY WIEDZY (dobrany semantycznie)", kb_hits)
    elif task_profile_key == "private_help":
        kb_context, kb_hits = _build_private_help_context(query, top_k=3)

    if task_profile_key in {"coding", "debug"}:
        coding_ctx, rule_sources = coding_rules_module.build_coding_context(query, tier="nano", limit=2)
        if coding_ctx:
            kb_context = (kb_context + "\n\n" + coding_ctx).strip() if kb_context else coding_ctx
            kb_hits.extend([{"source": src, "text": "", "score": 1.0} for src in rule_sources])

    return {
        "kb_scope": kb_scope,
        "char_scope": char_scope,
        "use_character_examples": use_character_examples,
        "char_inject": char_inject,
        "kb_context": kb_context,
        "kb_hits": kb_hits,
    }


def _run_profiled_webhook_chat(
    text: str,
    task_profile: Optional[str],
    model_name: Optional[str],
    use_tools: bool,
    max_tokens: int,
    temperature: float,
    top_p: float,
    custom_system_prompt: Optional[str],
    meta: Optional[dict] = None,
    subsystem: Optional[str] = None,
):
    task_profile_key, task_profile_def, model_name, use_tools, custom_system_prompt = _apply_task_profile(
        task_profile, model_name, use_tools, custom_system_prompt
    )
    response_meta = _resolve_response_meta(model_name)
    meta_payload = dict(meta or {})
    if subsystem:
        meta_payload.setdefault("subsystem", subsystem)
    profile_context = _profile_context(text, task_profile_key, task_profile_def)
    kb_hits = profile_context["kb_hits"]
    if kb_hits:
        meta_payload.setdefault(
            "kb_sources",
            ", ".join(_hit_sources(kb_hits)),
        )
    meta_lines = [f"- {key}: {value}" for key, value in meta_payload.items()]
    meta_block = f"\n\nMETA:\n" + "\n".join(meta_lines) if meta_lines else ""
    request_messages = [{"role": "user", "text": text + meta_block}]
    tools_rules = _webhook_tools_rules(use_tools)
    if custom_system_prompt:
        system_prompt = custom_system_prompt
    else:
        system_prompt = _build_default_system_prompt(
            tools_rules=tools_rules,
            char_inject=profile_context["char_inject"],
            kb_context=profile_context["kb_context"],
            files_context="",
        )
    prompt = f"{system_prompt}\n\n" + "\n".join([f"{m['role']}: {m['text']}" for m in request_messages])
    out = model.generate(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        model_name=model_name,
    )
    payload = {
        "status": "ok",
        "task_profile": task_profile_key,
        "task_profile_label": task_profile_def["label"],
        "model_name": model_name or model.default_model_id,
        "provider": response_meta["provider"],
        "model_id": response_meta["model_id"],
        "model_display": response_meta["model_display"],
        "kb_scope": _profile_kb_scope(task_profile_def),
        "kb_sources": _hit_sources(kb_hits),
        "char_scope": _profile_char_scope(task_profile_def),
        "use_character_examples": bool(task_profile_def.get("use_character_examples", True)),
        "text": out,
    }
    if subsystem:
        payload["subsystem"] = subsystem
    if meta_payload:
        payload["meta"] = meta_payload
    return payload

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "provider": model.provider,
        "default_model": model.default_model_name,
        "database": "connected",
        "mcp_tools": len(mcp_registry.list_tools()),
        "available_tools": mcp_registry.list_tools(),
        "embeddings_ready": embed_module.is_ready(),
        "speech_api_configured": speech.is_configured(),
        "python_executable": sys.executable,
        "terminal_pty": _HAS_WINPTY,
        "app_name": APP_NAME,
        "assistant_name": ASSISTANT_NAME,
        "user_name": USER_NAME,
        "kb_dir": str(_kb_dir()),
        "rerank_provider": RERANK_PROVIDER,
        "rerank_model": RERANK_MODEL,
        "model_router_enabled": MODEL_ROUTER_ENABLED,
        "model_router_base_url": MODEL_ROUTER_BASE_URL,
        "task_profiles": list(TASK_PROFILES.keys()),
    }


@app.get("/api/diagnostics")
async def diagnostics():
    """Real-time dashboard data with no synthetic counters."""
    return _diagnostics_snapshot()


@app.get("/api/ui-config")
async def ui_config():
    return {
        "app_name": APP_NAME,
        "assistant_name": ASSISTANT_NAME,
        "user_name": USER_NAME,
        "kb_label": KB_LABEL,
        "rerank_provider": RERANK_PROVIDER,
        "rerank_model": RERANK_MODEL,
        "model_router_enabled": MODEL_ROUTER_ENABLED,
        "model_router_base_url": MODEL_ROUTER_BASE_URL,
        "task_profiles": TASK_PROFILES,
        "default_system_prompt": _build_default_system_prompt().strip(),
    }


@app.get("/api/task-profiles")
async def task_profiles():
    return {"default": "shop_help", "profiles": TASK_PROFILES}

@app.get("/api/models")
async def list_models():
    """Lista dostępnych modeli pogrupowana według providera"""
    return model.list_models()

@app.get("/api/tools")
async def list_tools():
    """Lista dostÄ™pnych narzÄ™dzi MCP"""
    tools_info = []
    for tool_name in mcp_registry.list_tools():
        tool = mcp_registry.get_tool(tool_name)
        tools_info.append({
            "name": tool["name"],
            "description": tool["description"]
        })
    return {"tools": tools_info}


# ── KNOWLEDGE BASE ENDPOINTS ──────────────────────────────────────────────────

@app.get("/api/knowledge")
async def list_knowledge():
    """Lista plików w bazie wiedzy"""
    kb = _kb_dir()
    files = []
    for f in sorted(kb.rglob("*")):
        if f.is_file():
            files.append({
                "name": f.name,
                "path": str(f.relative_to(kb)),
                "size": f.stat().st_size,
            })
    return {"files": files, "kb_dir": str(kb), "count": len(files)}

@app.post("/api/knowledge/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    """Przesyła plik do bazy wiedzy"""
    kb = _kb_dir()
    safe_name = os.path.basename(file.filename)
    dest = kb / safe_name
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "ok", "file": safe_name, "size": dest.stat().st_size}

@app.delete("/api/knowledge/{filename}")
async def delete_knowledge(filename: str):
    """Usuwa plik z bazy wiedzy"""
    kb = _kb_dir()
    target = (kb / filename).resolve()
    if not str(target).startswith(str(kb.resolve())):
        raise HTTPException(status_code=400, detail="Niedozwolona sciezka")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    target.unlink()
    return {"status": "ok", "deleted": filename}


def _safe_slug(s: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", s).strip("-")
    return slug[:120] or "entry"


def _extract_page_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
    title = (soup.title.string or "").strip() if soup.title else ""
    text = "\n".join([ln.strip() for ln in soup.get_text("\n").splitlines() if ln.strip()])
    return title, text


def _web_search_candidates(query: str, max_results: int = 5):
    out = []
    tavily_key = os.getenv("TAVILY_API_KEY", "").strip()
    if tavily_key:
        try:
            rr = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": tavily_key, "query": query, "max_results": max_results},
                timeout=20,
            )
            if rr.ok:
                for it in rr.json().get("results", [])[:max_results]:
                    out.append({"title": it.get("title", ""), "url": it.get("url", ""), "snippet": it.get("content", "")})
            if out:
                return out
        except Exception:
            pass
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    if serper_key:
        try:
            rr = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": query, "num": max_results},
                timeout=20,
            )
            if rr.ok:
                for it in rr.json().get("organic", [])[:max_results]:
                    out.append({"title": it.get("title", ""), "url": it.get("link", ""), "snippet": it.get("snippet", "")})
            if out:
                return out
        except Exception:
            pass
    # fallback: DDG instant
    try:
        url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1"
        rr = requests.get(url, timeout=10)
        if rr.ok:
            dd = rr.json()
            for rt in dd.get("RelatedTopics", [])[:max_results]:
                if isinstance(rt, dict) and rt.get("FirstURL"):
                    out.append({"title": rt.get("Text", "").split(" - ")[0], "url": rt.get("FirstURL"), "snippet": rt.get("Text", "")})
    except Exception:
        pass
    return out[:max_results]


@app.post("/api/knowledge/ingest_web")
async def ingest_web(body: WebIngestRequest):
    kb = _kb_dir()
    web_dir = kb / "web"
    web_dir.mkdir(parents=True, exist_ok=True)
    try:
        resp = requests.get(body.url, timeout=20, headers={"User-Agent": f"{APP_NAME}/1.0"})
        resp.raise_for_status()
        page_title, text = _extract_page_text(resp.text)
        text = text[: max(1000, min(body.max_chars, 100000))]
        title = body.title or page_title or body.url
        slug = _safe_slug(title)
        filename = f"{slug}.md"
        target = web_dir / filename
        header = [
            f"# {title}",
            "",
            f"Source: {body.url}",
            f"Tags: {', '.join(body.tags) if body.tags else 'web,import'}",
            "",
            "## Content",
            "",
        ]
        target.write_text("\n".join(header) + text, encoding="utf-8")
        return {"status": "ok", "file": str(target.relative_to(kb)), "chars": len(text), "title": title}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Nie udało się pobrać strony: {e}")


@app.post("/api/knowledge/ingest_tmdb")
async def ingest_tmdb(body: TMDBIngestRequest):
    tmdb_key = os.getenv("TMDB_API_KEY", "").strip()
    if not tmdb_key:
        raise HTTPException(status_code=400, detail="Brak TMDB_API_KEY w .env")
    kb = _kb_dir()
    movies_dir = kb / "movies_api"
    movies_dir.mkdir(parents=True, exist_ok=True)
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        r = requests.get(url, params={"api_key": tmdb_key, "query": body.query, "language": "pl-PL", "page": 1}, timeout=20)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])[: max(1, min(body.limit, 20))]
        saved = []
        for item in results:
            title = item.get("title") or item.get("original_title") or "untitled"
            slug = _safe_slug(f"{title}-{item.get('id', '')}")
            target = movies_dir / f"{slug}.json"
            target.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
            saved.append(str(target.relative_to(kb)))
        return {"status": "ok", "count": len(saved), "files": saved}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"TMDB fetch failed: {e}")


@app.post("/api/knowledge/research_web")
async def research_web(body: WebResearchRequest):
    kb = _kb_dir()
    web_dir = kb / "web_research"
    web_dir.mkdir(parents=True, exist_ok=True)
    hits = _web_search_candidates(body.query, max_results=max(1, min(body.max_results, 10)))
    saved = []
    for idx, h in enumerate(hits, start=1):
        u = (h.get("url") or "").strip()
        if not u:
            continue
        try:
            resp = requests.get(u, timeout=20, headers={"User-Agent": f"{APP_NAME}/1.0"})
            resp.raise_for_status()
            title, text = _extract_page_text(resp.text)
            final_title = title or h.get("title") or u
            fname = _safe_slug(f"{body.query}-{idx}-{final_title}") + ".md"
            target = web_dir / fname
            target.write_text(
                f"# {final_title}\n\nSource: {u}\nQuery: {body.query}\n\n## Snippet\n{h.get('snippet','')}\n\n## Content\n\n{text[:20000]}\n",
                encoding="utf-8",
            )
            saved.append(str(target.relative_to(kb)))
        except Exception:
            continue
    return {"status": "ok", "query": body.query, "saved": saved, "count": len(saved)}


@app.post("/api/knowledge/push_r2")
async def push_knowledge_to_r2(body: R2PushRequest):
    account_id = os.getenv("CF_R2_ACCOUNT_ID", "").strip()
    access_key = os.getenv("CF_R2_ACCESS_KEY_ID", "").strip()
    secret_key = os.getenv("CF_R2_SECRET_ACCESS_KEY", "").strip()
    bucket = os.getenv("CF_R2_BUCKET", "").strip()
    if not (account_id and access_key and secret_key and bucket):
        raise HTTPException(status_code=400, detail="Brak konfiguracji R2 (CF_R2_ACCOUNT_ID/CF_R2_ACCESS_KEY_ID/CF_R2_SECRET_ACCESS_KEY/CF_R2_BUCKET)")
    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )
    kb = _kb_dir()
    uploaded = []
    only = {e.lower() for e in body.only_ext}
    for f in sorted(kb.rglob("*")):
        if not f.is_file():
            continue
        if only and f.suffix.lower() not in only:
            continue
        key = f"{body.prefix.strip('/')}/{str(f.relative_to(kb)).replace(os.sep, '/')}"
        s3.upload_file(str(f), bucket, key)
        uploaded.append(key)
    return {"status": "ok", "bucket": bucket, "uploaded": len(uploaded), "keys": uploaded[:100]}


@app.post("/api/speech/transcribe")
async def speech_transcribe(
    file: UploadFile = File(...),
    language: str = Form("pl"),
    prompt: Optional[str] = Form(None),
):
    try:
        content = await file.read()
        text = speech.transcribe(content, file.filename or "audio.wav", language=language, prompt=prompt)
        return {"status": "ok", "text": text, "language": language}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/speech/synthesize")
async def speech_synthesize(body: TTSRequest):
    try:
        preset_map = {
            "neo-noir": "Deep, restrained, cinematic delivery. Subtle tension, low-key noir atmosphere.",
            "dry-sarcasm": "Controlled, dry delivery with understated ironic edge. Keep clarity high.",
            "philosophy-dark": "Reflective, analytical, serious tone. Slow cadence with confident articulation.",
            "code-mentor": "Precise technical narration, neutral and focused, crisp pacing for clarity.",
        }
        instructions = preset_map.get((body.style_preset or "").strip().lower())
        audio = speech.synthesize(body.text, voice=body.voice, audio_format=body.format, instructions=instructions)
        media = "audio/mpeg" if body.format == "mp3" else "audio/wav"
        filename = f"{ASSISTANT_NAME.lower()}-tts.{body.format}"
        return StreamingResponse(
            iter([audio]),
            media_type=media,
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── DIARY ENDPOINTS ───────────────────────────────────────────────────────────

@app.get("/api/diary")
async def get_diary_data():
    """Zwraca dziennik użytkownika — fakty i kluczowe momenty"""
    d = diary_module.get_diary()
    return {
        "facts":   d.get_facts(),
        "moments": d.get_moments(),
        "preferences": d.get_preferences(),
        "goals": d.get_goals(),
        "decisions": d.get_decisions(),
        "summary": d.get_summary(),
    }

@app.post("/api/diary/fact")
async def add_diary_fact(body: dict):
    """Ręcznie dodaje fakt o użytkowniku"""
    fact = body.get("fact", "").strip()
    if not fact:
        raise HTTPException(status_code=400, detail="Brak faktu")
    diary_module.get_diary().add_fact(fact)
    return {"status": "ok", "fact": fact}

@app.post("/api/diary/moment")
async def add_diary_moment(body: dict):
    """Ręcznie dodaje ważny moment"""
    summary = body.get("summary", "").strip()
    tags    = body.get("tags", [])
    if not summary:
        raise HTTPException(status_code=400, detail="Brak podsumowania")
    diary_module.get_diary().add_moment(summary, tags)
    return {"status": "ok"}

@app.delete("/api/diary")
async def clear_diary():
    """Czyści dziennik użytkownika"""
    diary_module.get_diary().clear()
    return {"status": "ok", "message": "Dziennik wyczyszczony"}


@app.post("/api/diary/preference")
async def add_diary_preference(body: dict):
    pref = body.get("preference", "").strip()
    if not pref:
        raise HTTPException(status_code=400, detail="Brak preference")
    diary_module.get_diary().add_preference(pref)
    return {"status": "ok", "preference": pref}


@app.post("/api/diary/goal")
async def add_diary_goal(body: dict):
    goal = body.get("goal", "").strip()
    if not goal:
        raise HTTPException(status_code=400, detail="Brak goal")
    diary_module.get_diary().add_goal(goal)
    return {"status": "ok", "goal": goal}


@app.post("/api/decision/coach")
async def decision_coach(body: DecisionRequest):
    topic = body.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Brak topic")
    diary = diary_module.get_diary()
    profile = diary.get_summary(max_facts=25, max_moments=6)
    options = "\n".join([f"- {o}" for o in body.options]) if body.options else "- (brak listy opcji)"
    constraints = "\n".join([f"- {c}" for c in body.constraints]) if body.constraints else "- (brak)"
    prompt = (
        f"Jesteś doradcą decyzyjnym {USER_NAME}. Daj konkretną rekomendację.\n"
        "Format odpowiedzi:\n"
        "1) REKOMENDACJA (1 zdanie)\n"
        "2) DLACZEGO (max 5 punktów)\n"
        "3) RYZYKA (max 3)\n"
        "4) NASTĘPNY KROK (1 bardzo konkretny krok dziś)\n\n"
        f"Temat: {topic}\n"
        f"Opcje:\n{options}\n"
        f"Ograniczenia:\n{constraints}\n"
        f"Profil użytkownika:\n{profile}\n"
    )
    answer = model.generate(prompt, max_tokens=600, temperature=0.4, top_p=0.9)
    diary.add_decision(topic=topic, recommendation=answer[:1200], rationale=answer, confidence="medium")
    return {"status": "ok", "topic": topic, "answer": answer}


@app.get("/api/mood-advisor")
async def mood_advisor(query: str):
    """Filozofia + film z Cinema Vault dopasowany do sytuacji/nastroju, z cytatem recenzji."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Brak query")
    result = mcp_registry.execute_tool("mood_prescription", query=query.strip())
    return {"query": query, "prescription": result}


@app.post("/api/chat")
async def chat(
    messages: str = Form(...),
    use_tools: bool = Form(True),
    max_tokens: int = Form(512),
    temperature: float = Form(0.6),
    top_p: float = Form(0.9),
    model_name: Optional[str] = Form(None),
    task_profile: Optional[str] = Form(None),
    custom_system_prompt: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[])
):
    """
    GĹ‚Ăłwny endpoint czatu z obsĹ‚ugÄ… MCP tools, plikĂłw i Ollama
    
    FormData: messages (JSON string), files (opcjonalnie), temperature, top_p
    """
    global ACTIVE_CHAT_REQUESTS
    db = None
    ACTIVE_CHAT_REQUESTS += 1
    try:
        # Parse JSON messages
        request_messages = json.loads(messages)
        task_profile_key, task_profile_def, model_name, use_tools, custom_system_prompt = _apply_task_profile(
            task_profile, model_name, use_tools, custom_system_prompt
        )
        
        # ObsĹ‚uga przesĹ‚anych plikĂłw
        uploaded_files_info = []
        if files:
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            for file in files:
                file_path = os.path.join(upload_dir, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Przeczytaj zawartoĹ›Ä‡ (tylko txt/kod, max 10KB)
                file_content = ""
                if file.filename.endswith((".txt", ".py", ".js", ".md", ".json")):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read(10000)  # max 10KB
                    except:
                        file_content = "[nie moĹĽna odczytaÄ‡ pliku]"
                
                uploaded_files_info.append({
                    "name": file.filename,
                    "path": file_path,
                    "content": file_content[:500]  # max 500 znakĂłw w odpowiedzi
                })

        db = SessionLocal()
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)

        # Zapisz wiadomoĹ›ci uĹĽytkownika
        for m in request_messages:
            db.add(Message(conversation_id=conv.id, role=m.get("role"), content=m.get("text")))
        db.commit()

        # Przygotuj prompt z informacjÄ… o plikach
        files_context = ""
        if uploaded_files_info:
            files_context = "\n\nđź“Ž ZaĹ‚Ä…czone pliki:\n" + "\n".join([
                f"- {f['name']}: {f['content'][:200]}..." for f in uploaded_files_info
            ])

        user_text = request_messages[-1].get("text", "") if request_messages else ""
        profile_context = _profile_context(user_text, task_profile_key, task_profile_def)
        char_inject = profile_context["char_inject"]
        kb_context = profile_context["kb_context"]
        kb_scope = profile_context["kb_scope"]
        kb_sources = _hit_sources(profile_context["kb_hits"])
        char_scope = profile_context["char_scope"]
        use_character_examples = profile_context["use_character_examples"]

        # Dziennik użytkownika — podsumowanie do system promptu
        diary_summary = diary_module.get_diary().get_summary()

        # Zasady narzędzi: zawsze dołączane gdy use_tools=True (także z custom prompt)
        tool_names = ", ".join(mcp_registry.list_tools())
        tools_rules = f"""
NARZĘDZIA MCP — ZASADY:
- Masz dostęp TYLKO do: {tool_names}
- Użyj formatu: [TOOL:nazwa]argument[/TOOL]
- NIE WYMYŚLAJ danych (CPU%, RAM%, procesy, IP, sieć) — powiedz że brak narzędzia
- Jeśli pytanie wymaga czegoś czego nie masz — przyznaj to wprost"""

        # Przygotuj prompt - użyj custom prompt jeśli podany, inaczej domyślny
        if custom_system_prompt:
            system_prompt = f"{custom_system_prompt}{(tools_rules if use_tools else '')}{char_inject}{kb_context}{files_context}"
        else:
            system_prompt = _build_default_system_prompt(
                diary_summary=diary_summary,
                tools_rules=tools_rules if use_tools else "",
                char_inject=char_inject,
                kb_context=kb_context,
                files_context=files_context,
            )
        prompt = f"{system_prompt}\n\n" + "\n".join([f"{m['role']}: {m['text']}" for m in request_messages])

        # Generuj odpowiedź
        print(f"[OUT] Wysyłam do {model.provider} model={model_name or 'default'} temp={temperature}: {prompt[:100]}...")
        response_meta = _resolve_response_meta(model_name)
        out = model.generate(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p, model_name=model_name)
        print(f"[IN] Odpowiedź ({len(out)} znaków): {out[:100]}...")

        # Dziennik użytkownika — zaloguj turę i wyekstrahuj fakty w tle
        diary_module.get_diary().log_turn(user_text, out)
        diary_module.extract_facts_async(model, user_text, out)
        diary_module.extract_profile_async(model, user_text, out)

        # Sprawdź czy są wywołania narzędzi
        tool_calls = []
        if use_tools:
            tool_calls_parsed = parse_tool_call_from_text(out)

            for tc in tool_calls_parsed:
                result = mcp_registry.execute_tool(tc["tool"], **tc["args"])
                tool_calls.append({
                    "tool": tc["tool"],
                    "args": tc["args"],
                    "result": result
                })

            # Jeśli były wywołania narzędzi, dodaj ich wyniki do odpowiedzi
            if tool_calls:
                out = re.sub(r'\[TOOL:\w+\].*?\[/TOOL\]', '', out, flags=re.DOTALL)
                out = re.sub(r'<tool_call>.*?</tool_call>', '', out, flags=re.DOTALL).strip()
                tools_summary = "\n\n[TOOL] Użyte narzędzia:\n" + "\n".join([
                    f"- {tc['tool']}: {tc['result']}" for tc in tool_calls
                ])
                out = out + tools_summary

        # Zapisz odpowiedĹş asystenta
        db.add(Message(conversation_id=conv.id, role="assistant", content=out))
        db.commit()

        return JSONResponse(
            content={
                "text": out,
                "task_profile": task_profile_key,
                "task_profile_label": task_profile_def["label"],
                "kb_scope": kb_scope,
                "kb_sources": kb_sources,
                "char_scope": char_scope,
                "use_character_examples": use_character_examples,
                "provider": response_meta["provider"],
                "model_id": response_meta["model_id"],
                "model_display": response_meta["model_display"],
                "model_requested": response_meta["model_requested"],
                "tool_calls": tool_calls if tool_calls else [],
                "uploaded_files": [f["name"] for f in uploaded_files_info]
            },
            media_type="application/json; charset=utf-8"
        )

    except Exception as e:
        import traceback
        print(f"âťŚ BĹ‚Ä…d /api/chat: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db:
            db.close()


@app.post("/api/chat/stream")
def chat_stream(
    messages: str = Form(...),
    use_tools: bool = Form(True),
    max_tokens: int = Form(512),
    temperature: float = Form(0.6),
    top_p: float = Form(0.9),
    model_name: Optional[str] = Form(None),
    task_profile: Optional[str] = Form(None),
    custom_system_prompt: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[])
):
    """
    Streaming chat endpoint (SSE).
    Accepts same FormData as /api/chat, returns text/event-stream with 'chunk' and 'done' events.
    """
    global ACTIVE_CHAT_REQUESTS
    db = None
    streaming_response_created = False
    ACTIVE_CHAT_REQUESTS += 1
    try:
        request_messages = json.loads(messages)
        task_profile_key, task_profile_def, model_name, use_tools, custom_system_prompt = _apply_task_profile(
            task_profile, model_name, use_tools, custom_system_prompt
        )

        # Handle uploaded files
        uploaded_files_info = []
        if files:
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            for file in files:
                file_path = os.path.join(upload_dir, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                file_content = ""
                if file.filename.endswith((".txt", ".py", ".js", ".md", ".json")):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_content = f.read(10000)
                    except:
                        file_content = "[nie mo\u017cna odczyta\u0107 pliku]"
                uploaded_files_info.append({
                    "name": file.filename,
                    "path": file_path,
                    "content": file_content[:500]
                })

        db = SessionLocal()
        conv = Conversation()
        db.add(conv)
        db.commit()
        db.refresh(conv)

        for m in request_messages:
            db.add(Message(conversation_id=conv.id, role=m.get("role"), content=m.get("text")))
        db.commit()

        # Build context (same logic as /api/chat)
        files_context = ""
        if uploaded_files_info:
            files_context = "\n\n\U0001f4ce Za\u0142\u0105czone pliki:\n" + "\n".join([
                f"- {f['name']}: {f['content'][:200]}..." for f in uploaded_files_info
            ])

        user_text = request_messages[-1].get("text", "") if request_messages else ""
        profile_context = _profile_context(user_text, task_profile_key, task_profile_def)
        char_inject = profile_context["char_inject"]
        kb_context = profile_context["kb_context"]
        kb_scope = profile_context["kb_scope"]
        kb_sources = _hit_sources(profile_context["kb_hits"])
        char_scope = profile_context["char_scope"]
        use_character_examples = profile_context["use_character_examples"]

        diary_summary = diary_module.get_diary().get_summary()

        tool_names = ", ".join(mcp_registry.list_tools())
        tools_rules = f"""
NARZ\u0118DZIA MCP \u2014 ZASADY:
- Masz dost\u0119p TYLKO do: {tool_names}
- U\u017cyj formatu: [TOOL:nazwa]argument[/TOOL]
- NIE WYMY\u015aLAJ danych (CPU%, RAM%, procesy, IP, sie\u0107) \u2014 powiedz \u017ce brak narz\u0119dzia
- Je\u015bli pytanie wymaga czego\u015b czego nie masz \u2014 przyznaj to wprost"""

        if custom_system_prompt:
            system_prompt = f"{custom_system_prompt}{(tools_rules if use_tools else '')}{char_inject}{kb_context}{files_context}"
        else:
            system_prompt = _build_default_system_prompt(
                diary_summary=diary_summary,
                tools_rules=tools_rules if use_tools else "",
                char_inject=char_inject,
                kb_context=kb_context,
                files_context=files_context,
            )
        prompt = f"{system_prompt}\n\n" + "\n".join([f"{m['role']}: {m['text']}" for m in request_messages])

        print(f"\U0001f4e4 Stream do {model.provider} model={model_name or 'default'} temp={temperature}: {prompt[:100]}...")
        response_meta = _resolve_response_meta(model_name)

        def generate():
            global ACTIVE_CHAT_REQUESTS
            full_text = ""
            try:
                for chunk in model.generate_stream(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p, model_name=model_name):
                    full_text += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"

                print(f"\U0001f4e5 Stream response ({len(full_text)} chars)")

                # Tool calls
                tool_calls = []
                if use_tools:
                    tool_calls_parsed = parse_tool_call_from_text(full_text)
                    for tc in tool_calls_parsed:
                        result = mcp_registry.execute_tool(tc["tool"], **tc["args"])
                        tool_calls.append({
                            "tool": tc["tool"],
                            "args": tc["args"],
                            "result": result
                        })
                    if tool_calls:
                        tools_summary = "\n\n\U0001f527 U\u017cyte narz\u0119dzia:\n" + "\n".join([
                            f"- {tc['tool']}: {tc['result']}" for tc in tool_calls
                        ])
                        full_text += tools_summary
                        yield f"data: {json.dumps({'type': 'chunk', 'text': tools_summary})}\n\n"

                # Save to DB
                db.add(Message(conversation_id=conv.id, role="assistant", content=full_text))
                db.commit()

                # Diary
                diary_module.get_diary().log_turn(user_text, full_text)
                diary_module.extract_facts_async(model, user_text, full_text)
                diary_module.extract_profile_async(model, user_text, full_text)

                yield f"data: {json.dumps({'type': 'done', 'text': full_text, 'tool_calls': tool_calls, 'uploaded_files': [f['name'] for f in uploaded_files_info], 'task_profile': task_profile_key, 'task_profile_label': task_profile_def['label'], 'kb_scope': kb_scope, 'kb_sources': kb_sources, 'char_scope': char_scope, 'use_character_examples': use_character_examples, 'provider': response_meta['provider'], 'model_id': response_meta['model_id'], 'model_display': response_meta['model_display'], 'model_requested': response_meta['model_requested']})}\n\n"

            except Exception as e:
                import traceback
                print(f"\u274c Stream error: {e}")
                print(traceback.format_exc())
                yield f"data: {json.dumps({'type': 'done', 'text': full_text, 'tool_calls': [], 'uploaded_files': [f['name'] for f in uploaded_files_info], 'task_profile': task_profile_key, 'task_profile_label': task_profile_def['label'], 'kb_scope': kb_scope, 'kb_sources': kb_sources, 'char_scope': char_scope, 'use_character_examples': use_character_examples, 'provider': response_meta['provider'], 'model_id': response_meta['model_id'], 'model_display': response_meta['model_display'], 'model_requested': response_meta['model_requested']})}\n\n"
            finally:
                if db:
                    db.close()
                ACTIVE_CHAT_REQUESTS = max(0, ACTIVE_CHAT_REQUESTS - 1)

        streaming_response_created = True
        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        import traceback
        print(f"\u274c B\u0142\u0105d /api/chat/stream: {e}")
        print(traceback.format_exc())

        def error_gen():
            yield f"data: {json.dumps({'type': 'chunk', 'text': f'B\u0142\u0105d: {str(e)}'})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'text': '', 'tool_calls': [], 'task_profile': task_profile or 'default'})}\n\n"

        return StreamingResponse(error_gen(), media_type="text/event-stream")
    finally:
        if not streaming_response_created:
            if db:
                db.close()
            ACTIVE_CHAT_REQUESTS = max(0, ACTIVE_CHAT_REQUESTS - 1)


@app.post("/api/chat/webhook")
async def chat_webhook(body: ChatWebhookRequest):
    return _run_profiled_webhook_chat(
        text=body.text,
        task_profile=body.task_profile,
        model_name=body.model_name,
        use_tools=body.use_tools,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        custom_system_prompt=body.custom_system_prompt,
        meta=body.meta,
    )


@app.get("/api/deal-ops/info")
async def deal_ops_info():
    info = deal_ops_module.subsystem_info()
    info["task_profile"] = "deal_ops"
    info["model_chain"] = TASK_PROFILES["deal_ops"]["model_name"]
    return info


@app.post("/api/deal-ops/context")
async def deal_ops_context(body: DealOpsContextRequest):
    hits = []
    if embed_module.is_ready() and body.query.strip():
        hits = embed_module.get_index().semantic_search_kb(
            body.query,
            top_k=max(1, min(body.top_k, 10)),
            include_prefixes=["the_deal_BOYS"],
        )
    return {
        "subsystem": "the_deal_BOYS",
        "query": body.query,
        "workers": deal_ops_module.suggest_workers(body.query),
        "hits": hits,
        "count": len(hits),
    }


@app.post("/api/deal-ops/chat")
async def deal_ops_chat(body: ChatWebhookRequest):
    worker_suggestions = deal_ops_module.suggest_workers(body.text)
    meta = dict(body.meta or {})
    if worker_suggestions:
        meta["worker_suggestions"] = ", ".join(item["worker"] for item in worker_suggestions)
    return _run_profiled_webhook_chat(
        text=body.text,
        task_profile="deal_ops",
        model_name=body.model_name,
        use_tools=body.use_tools,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        custom_system_prompt=body.custom_system_prompt,
        meta=meta,
        subsystem="the_deal_BOYS",
    )


@app.get("/api/private-help/info")
async def private_help_info():
    info = private_help_module.subsystem_info()
    info["task_profile"] = "private_help"
    info["model_chain"] = TASK_PROFILES["private_help"]["model_name"]
    return info


@app.post("/api/private-help/context")
async def private_help_context(body: PrivateHelpContextRequest):
    hits = []
    if embed_module.is_ready() and body.query.strip():
        hits = embed_module.get_index().semantic_search_kb(
            body.query,
            top_k=max(1, min(body.top_k, 10)),
            include_prefixes=["PINKY_one"],
        )
    if not hits and body.query.strip():
        hits = private_help_module.search_docs(
            body.query,
            limit=max(1, min(body.top_k, 10)),
        )
    return {
        "subsystem": "PINKY_one",
        "query": body.query,
        "topics": private_help_module.suggest_topics(body.query),
        "hits": hits,
        "count": len(hits),
        "hit_mode": "semantic" if hits and "match_type" not in hits[0] else "lexical",
    }


@app.post("/api/private-help/chat")
async def private_help_chat(body: ChatWebhookRequest):
    topic_suggestions = private_help_module.suggest_topics(body.text)
    meta = dict(body.meta or {})
    if topic_suggestions:
        meta["topic_suggestions"] = ", ".join(item["topic"] for item in topic_suggestions)
    return _run_profiled_webhook_chat(
        text=body.text,
        task_profile="private_help",
        model_name=body.model_name,
        use_tools=body.use_tools,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        top_p=body.top_p,
        custom_system_prompt=body.custom_system_prompt,
        meta=meta,
        subsystem="PINKY_one",
    )


class CodingRuleMatchRequest(BaseModel):
    query: str
    tier: Optional[str] = "nano"
    limit: Optional[int] = 3


@app.get("/api/coding-rules/list")
async def coding_rules_list():
    books = coding_rules_module.list_books()
    return {
        "count": len(books),
        "books": books,
        "root": str(coding_rules_module.coding_rules_root()),
    }


@app.get("/api/coding-rules/{slug}")
async def coding_rules_get(slug: str, tier: str = "nano"):
    rule = coding_rules_module.get_book_rule(slug, tier=tier)
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule '{slug}' not found")
    return {
        "slug": slug,
        "tier": tier,
        "content": rule,
    }


@app.post("/api/coding-rules/match")
async def coding_rules_match(body: CodingRuleMatchRequest):
    suggestions = coding_rules_module.suggest_rules(body.query, limit=body.limit or 3)
    context, sources = coding_rules_module.build_coding_context(body.query, tier=body.tier or "nano", limit=body.limit or 3)
    return {
        "query": body.query,
        "suggestions": suggestions,
        "sources": sources,
        "context": context,
    }


class SmolAgentRunRequest(BaseModel):
    task: str
    model_name: Optional[str] = None


@app.post("/api/smolagent/run")
async def api_smolagent_run(body: SmolAgentRunRequest):
    if not body.task.strip():
        raise HTTPException(status_code=400, detail="Task description is required.")
    
    agent_dir = buch_dir / "The_brain" / "agents"
    if str(agent_dir) not in sys.path:
        sys.path.insert(0, str(agent_dir))
    
    import smol_runner
    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, smol_runner.run_task, body.task, body.model_name)
        return {
            "status": "ok",
            "task": body.task,
            "result": result,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "task": body.task, "detail": str(e)},
        )

# ── TERMINAL WEBSOCKET ────────────────────────────────────────────────────────

# Próbuje zaimportować pywinpty — daje prawdziwy PTY (obsługuje codex, python -i itd.)
try:
    import winpty as _winpty
    _HAS_WINPTY = True
except ImportError:
    try:
        import pywinpty as _winpty  # fallback for environments exposing this module name
        _HAS_WINPTY = True
    except ImportError:
        _HAS_WINPTY = False

def _find_powershell() -> str | None:
    """Znajduje ścieżkę do PowerShell 7 (pwsh) lub powershell.exe."""
    for candidate in ("pwsh.exe", "pwsh", "powershell.exe", "powershell"):
        found = _shutil.which(candidate)
        if found:
            return found
    return None

@app.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket):
    """WebSocket bridge: przeglądarka ↔ PowerShell.
    Używa pywinpty (prawdziwy PTY) jeśli dostępny — wymagane dla interactive CLI
    jak 'codex', 'python -i', 'node' itp. Fallback na pipe subprocess."""
    global ACTIVE_TERMINAL_WS
    await websocket.accept()
    ACTIVE_TERMINAL_WS += 1

    try:
        ps_path = _find_powershell()
        if not ps_path:
            await websocket.send_text(json.dumps({"type": "error", "data": "PowerShell not found on this system."}))
            await websocket.close()
            return

        if _HAS_WINPTY:
            await _terminal_ws_pty(websocket, ps_path)
        else:
            await websocket.send_text(json.dumps({"type": "output", "data":
                "[UWAGA] pywinpty nie jest zainstalowany — tryb pipe (bez TTY).\n"
                "Aby uruchamiać 'codex' i inne interaktywne CLI, zainstaluj: pip install pywinpty\n\n"
            }))
            await _terminal_ws_pipe(websocket, ps_path)
    finally:
        ACTIVE_TERMINAL_WS = max(0, ACTIVE_TERMINAL_WS - 1)


async def _terminal_ws_pty(websocket: WebSocket, ps_path: str):
    """PTY-based terminal — solidny wzorzec z Queue.
    Dedykowany wątek czyta PTY i wkłada dane do asyncio.Queue.
    Brak wait_for(run_in_executor) — żadnych zombie threads.
    """
    import threading
    import queue as _queue

    loop = asyncio.get_event_loop()
    out_queue: asyncio.Queue = asyncio.Queue(maxsize=200)
    alive = threading.Event()
    alive.set()

    try:
        proc = _winpty.PtyProcess.spawn(
            [ps_path, "-NoLogo", "-NoProfile"],
            cwd=str(_FRONTEND_DIR),
            dimensions=(50, 220),
        )
    except Exception as e:
        await websocket.send_text(json.dumps({"type": "error", "data": f"PTY spawn failed: {e}"}))
        return

    def _reader_thread():
        """Blokujący wątek czytający z PTY — odkłada dane do thread-safe queue."""
        thread_q: _queue.SimpleQueue = _queue.SimpleQueue()
        # Przekazujemy przez thread_q → loop.call_soon_threadsafe do asyncio.Queue
        while alive.is_set():
            try:
                data = proc.read(4096)
                if data:
                    text = data if isinstance(data, str) else data.decode("utf-8", errors="replace")
                    loop.call_soon_threadsafe(out_queue.put_nowait, text)
            except EOFError:
                break
            except Exception:
                if not proc.isalive():
                    break
        loop.call_soon_threadsafe(out_queue.put_nowait, None)  # sentinel

    reader = threading.Thread(target=_reader_thread, daemon=True)
    reader.start()

    async def send_output():
        while True:
            chunk = await out_queue.get()
            if chunk is None:
                break
            try:
                await websocket.send_text(json.dumps({"type": "output", "data": chunk}))
            except Exception:
                break

    async def recv_input():
        try:
            while True:
                msg = await websocket.receive_text()
                try:
                    data = json.loads(msg)
                except json.JSONDecodeError:
                    data = {"type": "input", "data": msg}
                if data.get("type") == "input":
                    payload = data.get("data", "")
                    try:
                        proc.write(payload)
                    except Exception:
                        break
                elif data.get("type") == "resize":
                    rows = max(1, int(data.get("rows", 24)))
                    cols = max(1, int(data.get("cols", 80)))
                    try:
                        proc.setwinsize(rows, cols)
                    except Exception:
                        pass
        except (WebSocketDisconnect, Exception):
            pass

    try:
        await asyncio.gather(send_output(), recv_input())
    finally:
        alive.clear()
        try:
            proc.terminate()
        except Exception:
            pass


async def _terminal_ws_pipe(websocket: WebSocket, ps_path: str):
    """Pipe-based terminal — fallback bez PTY (nie obsługuje interactive CLI)."""
    import subprocess as _subprocess
    process = await asyncio.create_subprocess_exec(
        ps_path, "-NoLogo", "-NoProfile",
        cwd=str(_FRONTEND_DIR),
        stdin=asyncio.subprocess.PIPE,
        creationflags=_subprocess.CREATE_NEW_PROCESS_GROUP,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    async def read_stream(stream):
        try:
            while True:
                chunk = await stream.read(1024)
                if not chunk:
                    break
                text = chunk.decode("utf-8", errors="replace")
                await websocket.send_text(json.dumps({"type": "output", "data": text}))
        except Exception:
            pass

    async def read_ws():
        try:
            while True:
                msg = await websocket.receive_text()
                try:
                    data = json.loads(msg)
                except json.JSONDecodeError:
                    data = {"type": "input", "data": msg}
                if data.get("type") == "input":
                    payload = data.get("data", "")
                    if process.stdin and not process.stdin.is_closing():
                        process.stdin.write(payload.encode("utf-8"))
                        await process.stdin.drain()
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    try:
        await asyncio.gather(
            read_ws(),
            read_stream(process.stdout),
            read_stream(process.stderr),
        )
    finally:
        try:
            process.kill()
        except Exception:
            pass
        try:
            await process.wait()
        except Exception:
            pass


# ── Frontend static serving ────────────────────────────────────────────────
from fastapi.responses import FileResponse as _FileResponse

_FRONTEND_DIR = _Path(__file__).parent.parent.parent

@app.get("/", include_in_schema=False)
async def _serve_index():
    return _FileResponse(str(_FRONTEND_DIR / "index.html"))

@app.get("/app.js", include_in_schema=False)
async def _serve_appjs():
    return _FileResponse(str(_FRONTEND_DIR / "app.js"), media_type="application/javascript")

@app.get("/favicon.ico", include_in_schema=False)
async def _serve_favicon():
    return _FileResponse(str(_FRONTEND_DIR / "Icons33eeewwee" / "445334.webFavicons" / "favicon.ico"))

@app.get("/ui-icon.png", include_in_schema=False)
async def _serve_ui_icon():
    return _FileResponse(str(_FRONTEND_DIR / "Icons33eeewwee" / "445334.windows" / "icon_32x32.png"), media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4149, reload=False)
