# -*- coding: utf-8 -*-
"""Small, separate loader for the PINKY_one private-help subsystem."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import re


_APP_DIR = Path(__file__).resolve().parent
_BUCH_ROOT = _APP_DIR.parent.parent


def private_root() -> Path:
    direct = _BUCH_ROOT / "PINKY_one"
    if direct.exists():
        return direct
    return _BUCH_ROOT / "knowledge_mood" / "PINKY_one"


_PRIVATE_ROOT = private_root()


def list_docs() -> List[Dict]:
    docs = []
    root = private_root()
    for fp in sorted(root.glob("*.md")):
        if fp.name in {"README.md", "SOURCE_MAP.md", "TODO.md"}:
            continue
        docs.append(
            {
                "name": fp.name,
                "stem": fp.stem,
                "path": str(fp),
            }
        )
    return docs


def suggest_topics(query: str, limit: int = 4) -> List[Dict]:
    query_tokens = set(re.findall(r"[a-zA-Z0-9ąćęłńóśźż_-]+", query.lower()))
    scored = []
    for doc in list_docs():
        hay = f"{doc['name']} {doc['stem']}".lower()
        score = 0
        for token in query_tokens:
            if token and token in hay:
                score += 1
        if score:
            scored.append(
                {
                    "topic": doc["stem"],
                    "file": doc["name"],
                    "score": score,
                }
            )
    scored.sort(key=lambda item: (-item["score"], item["file"]))
    return scored[:limit]


def search_docs(query: str, limit: int = 5) -> List[Dict]:
    query_tokens = [t for t in re.findall(r"[a-zA-Z0-9ąćęłńóśźż_-]+", query.lower()) if len(t) >= 3]
    if not query_tokens:
        return []
    results = []
    for doc in list_docs():
        path = Path(doc["path"])
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lowered = text.lower()
        score = sum(1 for token in query_tokens if token in lowered)
        if not score:
            continue
        first_pos = min((lowered.find(token) for token in query_tokens if token in lowered), default=0)
        start = max(0, first_pos - 80)
        end = min(len(text), first_pos + 220)
        snippet = " ".join(text[start:end].split())
        results.append(
            {
                "source": f"PINKY_one/{doc['name']}",
                "score": float(score),
                "text": snippet,
                "match_type": "lexical",
            }
        )
    results.sort(key=lambda item: (-item["score"], item["source"]))
    return results[:limit]


def subsystem_info() -> Dict:
    docs = list_docs()
    return {
        "name": "PINKY_one",
        "root": str(_PRIVATE_ROOT),
        "doc_count": len(docs),
        "docs": docs,
    }
