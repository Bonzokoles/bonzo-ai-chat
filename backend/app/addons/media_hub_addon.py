# -*- coding: utf-8 -*-
"""
Bonzo Media Hub Addon (Music & Films)
=====================================
Integracja z zasobami U:\\www_BONZO_media_HUB_inc:
- 28 utworów audio (Depeche Mode, Męskie Granie, Nosowska, Bowie, Podsiadło, Massive Attack)
- 105 wyselekcjonowanych filmów z TMDB w 7 kategoriach tematycznych
- Oficjalne trailery YouTube
"""

from __future__ import annotations

import os
import re
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/media", tags=["Bonzo Media Hub"])

# Base paths
MEDIA_HUB_DIR = Path("U:/www_BONZO_media_HUB_inc")
MUSIC_DIR = MEDIA_HUB_DIR / "public" / "music"
FILMS_CATALOG_PATH = MEDIA_HUB_DIR / "components" / "features" / "films" / "data" / "catalog" / "catalog_with_tmdb.json"

TMDB_READ_TOKEN = os.getenv("TMDB_READ_TOKEN", "")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

# In-memory caches
_CACHED_TRACKS: List[Dict[str, Any]] = []
_CACHED_FILMS: List[Dict[str, Any]] = []
_CACHED_CATEGORIES: List[Dict[str, Any]] = []


def _parse_track_filename(filename: str) -> Dict[str, str]:
    """Ekstrahuje wykonawcę i tytuł z nazwy pliku MP3."""
    stem = Path(filename).stem
    # Clean leading numbers like "01. ", "02 - "
    cleaned = re.sub(r"^\d+[\.\-_ ]*", "", stem).strip()

    artist = "Bonzo Media"
    title = cleaned

    if "Personal Jesus" in stem or "Tora!" in stem or "Depeche Mode" in stem:
        artist = "Depeche Mode"
        title = "Personal Jesus" if "Personal Jesus" in stem else "Tora! Tora! Tora!"
    elif "Nieznajomy" in stem:
        artist = "Dawid Podsiadło"
        title = "Nieznajomy"
    elif "Czy te oczy mogą kłamać" in stem:
        artist = "Raz Dwa Trzy"
        title = "Czy te oczy mogą kłamać"
    elif "Oczy tej małej" in stem:
        artist = "Raz Dwa Trzy"
        title = "Oczy tej małej"
    elif "Uciekaj moje serce" in stem:
        artist = "Seweryn Krajewski"
        title = "Uciekaj moje serce"
    elif "Kilka westchnień" in stem:
        artist = "Kortez"
        title = "Kilka westchnień"
    elif "Męskie Granie" in stem:
        artist = "Męskie Granie 2020"
        m = re.search(r"Męskie Granie 2020 - (.+)$", stem)
        if m:
            title = m.group(1).strip()
    elif "Nosowska" in stem:
        artist = "Nosowska"
        m = re.search(r"Nosowska - (.+)$", stem)
        if m:
            title = m.group(1).strip()
    elif "Daria Zawiałow" in stem:
        artist = "Daria Zawiałow"
        m = re.search(r"Daria Zawiałow.* - (.+)$", stem)
        if m:
            title = m.group(1).strip()
    elif "bowie" in stem.lower():
        artist = "David Bowie"
        title = "Life On Mars" if "Life On Mars" in stem else "The Man Who Sold The World"
    elif "gutek" in stem.lower():
        artist = "Gutek"
        title = "Nikt tak pięknie"
    elif "Massive Attack" in stem:
        artist = "Massive Attack"
        title = "Antistar"
    elif "Miuosh" in stem:
        artist = "Miuosh"
        title = "Neony"
    elif "Rozynek" in stem:
        artist = "Marcin Rozynek"
        title = "Siłacz"
    elif "Swiernalis" in stem or "Świernalis" in stem:
        artist = "Świernalis"
        title = "Blizny"
    elif " - " in cleaned:
        parts = cleaned.split(" - ", 1)
        artist = parts[0].strip()
        title = parts[1].strip()

    return {"title": title, "artist": artist}


def load_music_tracks() -> List[Dict[str, Any]]:
    """Ładuje i indeksuje wszystkie pliki muzyczne."""
    global _CACHED_TRACKS
    if not MUSIC_DIR.exists():
        return []

    tracks = []
    idx = 1
    for f in sorted(MUSIC_DIR.glob("*.mp3")):
        meta = _parse_track_filename(f.name)
        size_mb = round(f.stat().st_size / (1024 * 1024), 2)
        tracks.append({
            "id": f"track_{idx}",
            "filename": f.name,
            "title": meta["title"],
            "artist": meta["artist"],
            "size_mb": size_mb,
            "stream_url": f"/api/addons/media/audio/{f.name}",
            "full_path": str(f)
        })
        idx += 1

    _CACHED_TRACKS = tracks
    return tracks


def load_films_catalog() -> Dict[str, Any]:
    """Ładuje i indeksuje katalog 105 filmów."""
    global _CACHED_FILMS, _CACHED_CATEGORIES
    if not FILMS_CATALOG_PATH.exists():
        return {"films": [], "categories": []}

    try:
        data = json.loads(FILMS_CATALOG_PATH.read_text(encoding="utf-8"))
        categories = []
        all_films = []

        for cat in data.get("categories", []):
            cat_name = cat.get("category", "General")
            cat_mood = cat.get("mood", [])
            films_in_cat = cat.get("films", [])

            categories.append({
                "category": cat_name,
                "mood": cat_mood,
                "count": len(films_in_cat)
            })

            for film in films_in_cat:
                film_entry = dict(film)
                film_entry["category"] = cat_name
                film_entry["category_mood"] = cat_mood
                # Ensure tmdb poster fallback
                if not film_entry.get("poster"):
                    film_entry["poster"] = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=500&q=80"
                all_films.append(film_entry)

        _CACHED_FILMS = all_films
        _CACHED_CATEGORIES = categories
        return {"films": all_films, "categories": categories}
    except Exception as e:
        print(f"[ERROR] Failed to load film catalog: {e}")
        return {"films": [], "categories": []}


def get_youtube_trailer(tmdb_id: int, title: str) -> Dict[str, Any]:
    """Pobiera oficjalny trailer z TMDB API lub generuje fallback YouTube."""
    trailer_url = None
    trailer_embed = None
    key = None

    if TMDB_READ_TOKEN and tmdb_id:
        try:
            headers = {"Authorization": f"Bearer {TMDB_READ_TOKEN}", "Accept": "application/json"}
            res = requests.get(
                f"https://api.themoviedb.org/3/movie/{tmdb_id}/videos",
                headers=headers,
                timeout=4
            )
            if res.status_code == 200:
                vids = res.json().get("results", [])
                # Find official trailer
                for v in vids:
                    if v.get("site") == "YouTube" and v.get("type") in {"Trailer", "Teaser"}:
                        key = v.get("key")
                        break
                if not key and vids:
                    key = vids[0].get("key")
        except Exception:
            pass

    if key:
        trailer_url = f"https://www.youtube.com/watch?v={key}"
        trailer_embed = f"https://www.youtube-nocookie.com/embed/{key}?autoplay=1"
    else:
        # Fallback search URL
        query = f"{title} official trailer"
        trailer_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
        trailer_embed = ""

    return {
        "youtube_key": key,
        "trailer_url": trailer_url,
        "trailer_embed": trailer_embed
    }


# Initial warm-up
load_music_tracks()
load_films_catalog()


# --- REST API Endpoints ---

@router.get("/tracks")
async def list_tracks(query: Optional[str] = None):
    """Lista utworów muzycznych z opcją wyszukiwania."""
    tracks = _CACHED_TRACKS or load_music_tracks()
    if not query:
        return {"count": len(tracks), "tracks": tracks}

    q = query.lower()
    matched = [
        t for t in tracks
        if q in t["title"].lower() or q in t["artist"].lower() or q in t["filename"].lower()
    ]
    return {"count": len(matched), "query": query, "tracks": matched}


@router.get("/tracks/random")
async def random_track():
    """Zwraca losowy utwór z biblioteki."""
    tracks = _CACHED_TRACKS or load_music_tracks()
    if not tracks:
        raise HTTPException(status_code=404, detail="No tracks found")
    return random.choice(tracks)


@router.get("/films/categories")
async def list_categories():
    """Lista 7 kategorii filmowych."""
    if not _CACHED_CATEGORIES:
        load_films_catalog()
    return {"categories": _CACHED_CATEGORIES}


@router.get("/films")
async def list_films(
    category: Optional[str] = None,
    mood: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Przeglądanie i filtrowanie katalogu 105 filmów."""
    films = _CACHED_FILMS or load_films_catalog().get("films", [])

    filtered = films
    if category:
        cat_lower = category.lower()
        filtered = [f for f in filtered if cat_lower in f.get("category", "").lower()]

    if mood:
        mood_lower = mood.lower()
        filtered = [
            f for f in filtered
            if any(mood_lower in str(m).lower() for m in f.get("mood", []))
            or any(mood_lower in str(m).lower() for m in f.get("category_mood", []))
        ]

    if query:
        q = query.lower()
        filtered = [
            f for f in filtered
            if q in f.get("title", "").lower()
            or q in str(f.get("overview", "")).lower()
            or q in str(f.get("director", "")).lower()
        ]

    total = len(filtered)
    page_slice = filtered[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "films": page_slice
    }


@router.get("/films/random")
async def random_film(category: Optional[str] = None, mood: Optional[str] = None):
    """Zwraca losowy film z trailerem na wieczór."""
    res = await list_films(category=category, mood=mood, limit=1000)
    films = res["films"]
    if not films:
        raise HTTPException(status_code=404, detail="No films matching criteria")

    film = random.choice(films)
    trailer_info = get_youtube_trailer(film.get("tmdb_id"), film.get("title"))
    film_with_trailer = dict(film)
    film_with_trailer.update(trailer_info)
    return film_with_trailer


@router.get("/films/{tmdb_id}/trailer")
async def film_trailer(tmdb_id: int, title: Optional[str] = ""):
    """Pobiera informacje o trailerze filmu."""
    return get_youtube_trailer(tmdb_id, title or f"Movie {tmdb_id}")


# --- MCP Tools Registration ---

def register_media_tools(mcp_registry: Any):
    """Rejestruje narzędzia multimedialne w rejestrze MCP."""

    def tool_play_music(query: str = "", **kwargs) -> str:
        """Wyszukuje i zwraca utwór muzyczny do odtworzenia."""
        search_query = query or kwargs.get("song", "") or kwargs.get("track", "") or kwargs.get("title", "")
        tracks = _CACHED_TRACKS or load_music_tracks()
        if not tracks:
            return "Brak dostępnych utworów w Bonzo Media Hub."

        matched = None
        if search_query:
            tokens = [tok.strip().lower() for tok in re.split(r"[\s\-_,]+", search_query) if len(tok.strip()) >= 3]
            best_score = 0
            for t in tracks:
                hay = f"{t['title']} {t['artist']} {t['filename']}".lower()
                score = sum(1 for tok in tokens if tok in hay)
                if score > best_score:
                    best_score = score
                    matched = t

        if not matched:
            matched = random.choice(tracks)

        card_json = json.dumps({
            "type": "audio",
            "title": matched["title"],
            "artist": matched["artist"],
            "url": matched["stream_url"],
            "filename": matched["filename"]
        }, ensure_ascii=False)

        return (
            f"[AUDIO_PLAY: {matched['stream_url']} | {matched['title']} | {matched['artist']}]\n\n"
            f"Odtwarzam: **{matched['title']}** - {matched['artist']}\n"
            f"Plik: `{matched['filename']}` ({matched['size_mb']} MB)\n"
            f"<!-- CARD_JSON: {card_json} -->"
        )

    def tool_recommend_film(category_or_mood: str = "", query: str = "", **kwargs) -> str:
        """Poleca wyselekcjonowany film z Bonzo Media Hub wraz z trailerem."""
        films = _CACHED_FILMS or load_films_catalog().get("films", [])
        if not films:
            return "Brak filmów w katalogu Bonzo Media Hub."

        search_term = category_or_mood or query or kwargs.get("search", "")
        selected = None
        if search_term:
            term = search_term.lower()
            candidates = [
                f for f in films
                if term in f.get("category", "").lower()
                or any(term in str(m).lower() for m in f.get("mood", []))
                or term in f.get("title", "").lower()
            ]
            if candidates:
                selected = random.choice(candidates)

        if not selected:
            selected = random.choice(films)

        trailer = get_youtube_trailer(selected.get("tmdb_id"), selected.get("title"))
        card_data = {
            "type": "film",
            "title": selected.get("title"),
            "category": selected.get("category"),
            "director": selected.get("director", "N/A"),
            "rating": selected.get("rating"),
            "poster": selected.get("poster"),
            "overview": selected.get("overview", ""),
            "trailer_url": trailer.get("trailer_url"),
            "trailer_embed": trailer.get("trailer_embed")
        }

        trailer_btn = f"[Oglądaj Trailer]({trailer['trailer_url']})" if trailer.get("trailer_url") else ""

        return (
            f"[MOVIE_CARD: {selected.get('title')} | {selected.get('category')} | {trailer.get('trailer_url')}]\n\n"
            f"### {selected.get('title')} ({selected.get('category')})\n"
            f"**Reżyser:** {selected.get('director', 'Nieznany')} | **Ocena TMDB:** {selected.get('rating')}/10\n\n"
            f"{selected.get('overview', '')}\n\n"
            f"{trailer_btn}\n"
            f"<!-- CARD_JSON: {json.dumps(card_data, ensure_ascii=False)} -->"
        )

    def tool_search_films(query: str = "", **kwargs) -> str:
        """Wyszukuje filmy w katalogu 105 tytułów."""
        search_query = query or kwargs.get("search", "") or kwargs.get("term", "")
        films = _CACHED_FILMS or load_films_catalog().get("films", [])
        q = search_query.lower()
        matches = [
            f for f in films
            if q in f.get("title", "").lower()
            or q in str(f.get("overview", "")).lower()
            or q in str(f.get("director", "")).lower()
        ][:5]

        if not matches:
            return f"Brak wyników w katalogu Bonzo Media Hub dla: '{query}'."

        lines = [f"Znaleziono {len(matches)} filmów dla '{query}':"]
        for f in matches:
            lines.append(f"- **{f.get('title')}** ({f.get('category')}) — reż. {f.get('director')}, ocena {f.get('rating')}")

        return "\n".join(lines)

    # Register
    mcp_registry.register_tool(
        name="play_music",
        description="Wyszukuje i uruchamia odtwarzanie utworu muzycznego z Bonzo Media Hub. Args: query (str)",
        function=tool_play_music
    )
    mcp_registry.register_tool(
        name="recommend_film",
        description="Rekomenduje wyselekcjonowany film z katalogu 105 perełek Bonzo Media Hub wraz z trailerem. Args: category_or_mood (str)",
        function=tool_recommend_film
    )
    mcp_registry.register_tool(
        name="search_films",
        description="Przeszukuje 105 filmów w katalogu Bonzo Media Hub. Args: query (str)",
        function=tool_search_films
    )
