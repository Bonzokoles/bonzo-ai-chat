# -*- coding: utf-8 -*-
"""
Daily Helpers & Fun Addon
=========================
- Pogoda na żywo (Open-Meteo: bez klucza API, z geokodowaniem i prognozą)
- Generowanie obrazów AI (Pollinations.ai / FLUX: bez klucza, bezpośredni URL)
- Szybkie wyszukiwanie faktów (DuckDuckGo & Wikipedia)
- Złota myśl dnia i ciekawostki
"""

from __future__ import annotations

import json
import random
import requests
from typing import Dict, Any, Optional
from fastapi import APIRouter, Query

router = APIRouter(prefix="/fun", tags=["Daily Helpers & Fun"])

WMO_WEATHER_CODES = {
    0: "Bezchmurnie (Czyste niebo)",
    1: "Przeważnie bezchmurnie",
    2: "Częściowe zachmurzenie",
    3: "Pochmurno",
    45: "Mgła",
    48: "Oszroniona mgła",
    51: "Lekka mżawka",
    53: "Umiarkowana mżawka",
    55: "Gęsta mżawka",
    61: "Słaby deszcz",
    63: "Umiarkowany deszcz",
    65: "Ulewny deszcz",
    71: "Lekkie opady śniegu",
    73: "Umiarkowane opady śniegu",
    75: "Intensywny śnieg",
    77: "Ziarna śniegu",
    80: "Przelotne opady deszczu",
    81: "Umiarkowane przelotne opady",
    82: "Gwałtowne opady deszczu",
    95: "Burza z piorunami",
    96: "Burza z lekkim gradem",
    99: "Burza z gwałtownym gradem"
}

DAILY_THOUGHTS = [
    {"quote": "Prostota to najwyższa forma wyrafinowania.", "author": "Leonardo da Vinci", "tag": "ARCHITEKTURA"},
    {"quote": "Nie tłumacz kodu komentarzami — pisz kod tak, by tłumaczył się sam.", "author": "Martin Fowler", "tag": "CZYSTY KOD"},
    {"quote": "Spokój ducha to owoc panowania nad tym, co od nas zależy, i obojętności wobec reszty.", "author": "Marek Aureliusz", "tag": "STOICYZM"},
    {"quote": "Najlepszym sposobem na przewidzenie przyszłości jest jej stworzenie.", "author": "Alan Kay", "tag": "INNOWACJA"},
    {"quote": "W chaosie kryje się okazja, o ile zachowasz zimną krew i jasny cel.", "author": "Sun Tzu", "tag": "STRATEGIA"},
    {"quote": "Rzeczywistość to to, co nie znika, kiedy przestajesz w to wierzyć.", "author": "Philip K. Dick", "tag": "CYBERPUNK"},
    {"quote": "Zrób to raz, a dobrze. Automatyzuj wszystko, co powtarzasz więcej niż dwa razy.", "author": "Zasada Dev", "tag": "AUTOMATYZACJA"}
]


def fetch_weather(city: str = "Warszawa") -> Dict[str, Any]:
    """Pobiera dane pogodowe z Open-Meteo bez kluczy API."""
    try:
        # 1. Geokodowanie
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(city)}&count=1&language=pl&format=json"
        geo_res = requests.get(geo_url, timeout=4)
        if geo_res.status_code != 200 or not geo_res.json().get("results"):
            return {"error": f"Nie znaleziono lokalizacji: {city}"}

        loc = geo_res.json()["results"][0]
        lat = loc["latitude"]
        lon = loc["longitude"]
        name = loc.get("name", city)
        country = loc.get("country", "")

        # 2. Pogoda
        meteo_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
            f"&timezone=auto"
        )
        meteo_res = requests.get(meteo_url, timeout=4)
        if meteo_res.status_code != 200:
            return {"error": "Błąd pobierania prognozy pogody"}

        data = meteo_res.json()
        current = data.get("current", {})
        daily = data.get("daily", {})

        wcode = current.get("weather_code", 0)
        condition = WMO_WEATHER_CODES.get(wcode, "Zmienne warunki")

        return {
            "city": name,
            "country": country,
            "temperature": current.get("temperature_2m"),
            "apparent_temperature": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "condition": condition,
            "is_day": bool(current.get("is_day", 1)),
            "temp_max": daily.get("temperature_2m_max", [None])[0],
            "temp_min": daily.get("temperature_2m_min", [None])[0],
            "sunrise": daily.get("sunrise", [""])[0].split("T")[-1],
            "sunset": daily.get("sunset", [""])[0].split("T")[-1]
        }
    except Exception as e:
        return {"error": str(e)}


def generate_pollinations_image_url(prompt: str, width: int = 1024, height: int = 768) -> str:
    """Generuje bezpośredni adres URL do wyrenderowania obrazu przez Pollinations AI."""
    clean_prompt = requests.utils.quote(prompt.strip())
    seed = random.randint(1000, 999999)
    return f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model=flux"


def quick_web_summary(query: str) -> Dict[str, Any]:
    """Szybkie podsumowanie hasła z Wikipedii i DuckDuckGo."""
    summary = ""
    source = ""

    # 1. Wikipedia PL
    try:
        wiki_url = f"https://pl.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        res = requests.get(wiki_url, timeout=3, headers={"User-Agent": "EastWoodOps/1.0"})
        if res.status_code == 200:
            data = res.json()
            if data.get("extract"):
                return {
                    "title": data.get("title"),
                    "extract": data.get("extract"),
                    "thumbnail": data.get("thumbnail", {}).get("source"),
                    "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                    "source": "Wikipedia"
                }
    except Exception:
        pass

    # 2. DuckDuckGo Instant Answer
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1&skip_disambig=1"
        res = requests.get(ddg_url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            abstract = data.get("AbstractText")
            if abstract:
                return {
                    "title": data.get("Heading") or query,
                    "extract": abstract,
                    "thumbnail": data.get("Image"),
                    "url": data.get("AbstractURL"),
                    "source": "DuckDuckGo"
                }
    except Exception:
        pass

    return {"title": query, "extract": f"Brak natychmiastowej definicji encyklopedycznej dla '{query}'.", "source": "None"}


# --- Endpoints ---

@router.get("/weather")
async def get_weather(city: str = "Warszawa"):
    """Zwraca aktualną pogodę dla wybranego miasta."""
    return fetch_weather(city)


@router.get("/image")
async def get_image(prompt: str, width: int = 1024, height: int = 768):
    """Zwraca URL wygenerowanego obrazu z Pollinations AI."""
    url = generate_pollinations_image_url(prompt, width, height)
    return {"prompt": prompt, "image_url": url}


@router.get("/thought")
async def get_thought():
    """Zwraca losową myśl lub cytat dnia."""
    return random.choice(DAILY_THOUGHTS)


@router.get("/search")
async def search_quick(query: str):
    """Szybkie wyszukanie wiedzy ogólnej."""
    return quick_web_summary(query)


# --- MCP Tools ---

def register_fun_tools(mcp_registry: Any):
    """Rejestruje narzędzia codzienne i rozrywkowe w MCP."""

    def tool_live_weather(city: str = "Warszawa", query: str = "", location: str = "", **kwargs) -> str:
        """Pobiera aktualną pogodę na żywo dla miasta."""
        target_city = city or location or query or kwargs.get("name", "Warszawa")
        w = fetch_weather(target_city)
        if "error" in w:
            return f"Błąd pogody: {w['error']}"

        card_json = json.dumps({"type": "weather", **w}, ensure_ascii=False)

        return (
            f"**Pogoda: {w['city']}, {w['country']}**\n"
            f"- Warunki: **{w['condition']}**\n"
            f"- Temperatura: **{w['temperature']}°C** (odczuwalna: {w['apparent_temperature']}°C)\n"
            f"- Zakres dzisiejszy: {w['temp_min']}°C do {w['temp_max']}°C\n"
            f"- Wilgotność: {w['humidity']}% | Wiatr: {w['wind_speed']} km/h\n"
            f"- Wschód słońca: {w['sunrise']} | Zachód: {w['sunset']}\n"
            f"<!-- CARD_JSON: {card_json} -->"
        )

    def tool_generate_image(prompt: str = "", query: str = "", description: str = "", **kwargs) -> str:
        """Generuje obraz AI na podstawie promptu za pomocą Pollinations AI."""
        target_prompt = prompt or query or description or kwargs.get("text", "cyberpunk neon landscape")
        img_url = generate_pollinations_image_url(target_prompt)
        card_json = json.dumps({"type": "image", "prompt": target_prompt, "url": img_url}, ensure_ascii=False)

        return (
            f"[IMAGE: {img_url}]\n\n"
            f"![{target_prompt}]({img_url})\n\n"
            f"*Wygenerowano dla promptu: `{target_prompt}`*\n"
            f"<!-- CARD_JSON: {card_json} -->"
        )

    def tool_quick_search(query: str = "", **kwargs) -> str:
        """Szybkie wyszukiwanie faktów w encyklopedii (Wikipedia/DuckDuckGo)."""
        target_query = query or kwargs.get("term", "") or kwargs.get("search", "")
        res = quick_web_summary(target_query)
        return (
            f"**{res['title']}** ({res['source']})\n\n"
            f"{res['extract']}\n"
            + (f"\nLink: {res['url']}" if res.get("url") else "")
        )

    def tool_daily_thought() -> str:
        """Zwraca inspirujący cytat lub złotą myśl dnia."""
        t = random.choice(DAILY_THOUGHTS)
        return f"> \"{t['quote']}\"\n> — **{t['author']}** [{t['tag']}]"

    mcp_registry.register_tool(
        name="get_live_weather",
        description="Sprawdza aktualną pogodę na żywo dla dowolnego miasta na świecie. Args: city (str)",
        function=tool_live_weather
    )
    mcp_registry.register_tool(
        name="generate_image",
        description="Generuje natychmiastowy obraz AI na podstawie opisu tekstowego. Args: prompt (str)",
        function=tool_generate_image
    )
    mcp_registry.register_tool(
        name="quick_search",
        description="Błyskawicznie sprawdza definicję, osobę lub pojęcie w Wikipedii i DuckDuckGo. Args: query (str)",
        function=tool_quick_search
    )
    mcp_registry.register_tool(
        name="daily_thought",
        description="Zwraca refleksję, cytat lub stoicką myśl dnia. Brak argumentów.",
        function=tool_daily_thought
    )
