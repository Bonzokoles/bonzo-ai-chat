# -*- coding: utf-8 -*-
"""
Radio & Ambient Streams Addon
=============================
- Gotowe, niezawodne stacje radiowe online (Synthwave, Lofi, Rock, Jazz, Ambient)
- Wyszukiwarka stacji ze świata poprzez darmowe Radio-Browser API
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional, Any
import requests
from fastapi import APIRouter, Query

router = APIRouter(prefix="/radio", tags=["Live Radio & Ambient"])

# Curated high-uptime streams
PRESET_STATIONS = [
    {
        "id": "synthwave",
        "name": "Nightride FM (Cyberpunk / Synthwave)",
        "genre": "Synthwave",
        "stream_url": "https://stream.nightride.fm/nightride.m4a",
        "bitrate": "128k",
        "tag": "CYBERPUNK"
    },
    {
        "id": "chillsynth",
        "name": "Chillsynth FM (Dreamwave / Chill)",
        "genre": "Chillwave",
        "stream_url": "https://stream.nightride.fm/chillsynth.m4a",
        "bitrate": "128k",
        "tag": "CHILL"
    },
    {
        "id": "lofi",
        "name": "Lofi Chillhop Radio (Focus / Code)",
        "genre": "Lofi",
        "stream_url": "https://stream.zeno.fm/f3wvbbqmdg8uv",
        "bitrate": "128k",
        "tag": "LOFI"
    },
    {
        "id": "jazz",
        "name": "Smooth Jazz 24/7 (Late Night Vibes)",
        "genre": "Jazz",
        "stream_url": "https://streaming.exclusive.radio/er/smoothjazz/icecast.audio",
        "bitrate": "128k",
        "tag": "JAZZ"
    },
    {
        "id": "rock",
        "name": "Classic Rock Global (Hits & Anthems)",
        "genre": "Rock",
        "stream_url": "https://streaming.exclusive.radio/er/classicrock/icecast.audio",
        "bitrate": "128k",
        "tag": "ROCK"
    },
    {
        "id": "ambient",
        "name": "Space & Deep Ambient (Deep Work)",
        "genre": "Ambient",
        "stream_url": "https://ice1.somafm.com/spacestation-128-mp3",
        "bitrate": "128k",
        "tag": "AMBIENT"
    }
]


@router.get("/presets")
async def list_presets():
    """Zwraca listę prekonfigurowanych stacji radiowych."""
    return {"stations": PRESET_STATIONS}


@router.get("/search")
async def search_radio_stations(query: str, limit: int = 10):
    """Wyszukuje stacje radiowe na całym świecie przez Radio-Browser API."""
    mirrors = [
        "https://de1.api.radio-browser.info",
        "https://nl1.api.radio-browser.info",
        "https://at1.api.radio-browser.info"
    ]
    results = []
    headers = {"User-Agent": "EastWoodOps/1.0"}

    for mirror in mirrors:
        try:
            url = f"{mirror}/json/stations/byname/{requests.utils.quote(query)}"
            res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 200:
                raw = res.json()
                for s in raw[:limit]:
                    stream = s.get("url_resolved") or s.get("url")
                    if stream and stream.startswith("http"):
                        results.append({
                            "id": s.get("stationuuid"),
                            "name": s.get("name"),
                            "country": s.get("country"),
                            "tags": s.get("tags"),
                            "stream_url": stream,
                            "bitrate": s.get("bitrate", 128)
                        })
                if results:
                    break
        except Exception:
            continue

    return {"query": query, "count": len(results), "stations": results}


def register_radio_tools(mcp_registry: Any):
    """Rejestruje narzędzia radia w MCP."""

    def tool_play_radio(genre_or_station: str = "", query: str = "", **kwargs) -> str:
        """Uruchamia strumień radiowy (synthwave, lofi, rock, jazz, ambient)."""
        search_term = genre_or_station or query or kwargs.get("genre", "") or kwargs.get("station", "")
        term = search_term.lower().strip()
        matched = None

        if term:
            for s in PRESET_STATIONS:
                if term in s["genre"].lower() or term in s["id"].lower() or term in s["name"].lower():
                    matched = s
                    break

        if not matched:
            matched = PRESET_STATIONS[0]  # default Synthwave

        card_json = json.dumps({
            "type": "radio",
            "name": matched["name"],
            "genre": matched["genre"],
            "stream_url": matched["stream_url"]
        }, ensure_ascii=False)

        return (
            f"[RADIO_PLAY: {matched['stream_url']} | {matched['name']}]\n\n"
            f"Uruchomiono radio na żywo: **{matched['name']}** ({matched['genre']})\n"
            f"Strumień: `{matched['stream_url']}`\n"
            f"<!-- CARD_JSON: {card_json} -->"
        )

    mcp_registry.register_tool(
        name="play_radio",
        description="Włącza stację radiową online (gatunki: synthwave, lofi, rock, jazz, ambient). Args: genre_or_station (str)",
        function=tool_play_radio
    )
