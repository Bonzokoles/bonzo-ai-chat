# -*- coding: utf-8 -*-
"""
Bonzo Addons Manager
====================
Centralny orkiestrator modułów dodatkowych dla czatbota.
Ładuje, rejestruje i udostępnia wszystkie dodatki bez ingerencji w kod rdzenia.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from .media_hub_addon import router as media_router, register_media_tools, MUSIC_DIR
from .radio_addon import router as radio_router, register_radio_tools
from .daily_fun_addon import router as fun_router, register_fun_tools
from .companion_addon import register_companion_profiles

main_addons_router = APIRouter(prefix="/api/addons", tags=["Bonzo Addons"])
main_addons_router.include_router(media_router)
main_addons_router.include_router(radio_router)
main_addons_router.include_router(fun_router)


@main_addons_router.get("/status")
async def get_addons_status():
    """Zwraca stan i metadane wszystkich aktywnych dodatków."""
    return {
        "status": "active",
        "addons": [
            {
                "id": "media_hub",
                "name": "Bonzo Media Hub",
                "description": "28 utworów muzycznych oraz katalog 105 filmów z trailerami YouTube",
                "endpoints": ["/api/addons/media/tracks", "/api/addons/media/films", "/api/addons/media/films/random"]
            },
            {
                "id": "radio_streams",
                "name": "Live Radio & Ambient",
                "description": "Niezawodne stacje radiowe online i przeszukiwanie globalnego katalogu Radio-Browser",
                "endpoints": ["/api/addons/radio/presets", "/api/addons/radio/search"]
            },
            {
                "id": "daily_fun",
                "name": "Daily Helpers & Fun",
                "description": "Pogoda na żywo, darmowe generowanie obrazów AI (Pollinations), szybkie fakty i myśli dnia",
                "endpoints": ["/api/addons/fun/weather", "/api/addons/fun/image", "/api/addons/fun/thought", "/api/addons/fun/search"]
            },
            {
                "id": "companion_modes",
                "name": "Companion Task Profiles",
                "description": "Profile Pogadać, Kino & Filmy oraz Muzyka & DJ",
                "profiles": ["bonzo_companion", "bonzo_cinema", "bonzo_dj"]
            }
        ]
    }


def init_addons(app: FastAPI, mcp_registry: Any, task_profiles: Dict[str, Any]):
    """Główna funkcja inicjalizująca system dodatków."""
    print("[ADDONS] Inicjalizacja pakietu dodatków Bonzo...")

    # 1. Podpięcie routera REST API
    app.include_router(main_addons_router)

    # 2. Montowanie plików audio dla bezpośredniego streamingu
    if MUSIC_DIR.exists():
        app.mount(
            "/api/addons/media/audio",
            StaticFiles(directory=str(MUSIC_DIR)),
            name="bonzo_music_audio"
        )
        print(f"[ADDONS] Zamontowano streaming audio z: {MUSIC_DIR}")
    else:
        print(f"[ADDONS] Ostrzeżenie: Katalog muzyki nie znaleziony: {MUSIC_DIR}")

    # 3. Rejestracja narzędzi MCP
    register_media_tools(mcp_registry)
    register_radio_tools(mcp_registry)
    register_fun_tools(mcp_registry)
    print(f"[ADDONS] Narzędzia MCP zarejestrowane (obecnie łącznie {len(mcp_registry.list_tools())} narzędzi)")

    # 4. Rejestracja nowych profili zadaniowych
    register_companion_profiles(task_profiles)
    print("[ADDONS] Profile konwersacyjne 'Pogadać', 'Kino' i 'Muzyka' aktywne.")

    print("[ADDONS] System dodatków gotowy!")
