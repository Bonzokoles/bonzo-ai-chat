# -*- coding: utf-8 -*-
"""Small, separate loader for the_deal_BOYS strategic subsystem."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
import re


_APP_DIR = Path(__file__).resolve().parent
_BUCH_ROOT = _APP_DIR.parent.parent


def deal_root() -> Path:
    direct = _BUCH_ROOT / "the_deal_BOYS"
    if direct.exists():
        return direct
    return _BUCH_ROOT / "knowledge_mood" / "the_deal_BOYS"


_DEAL_ROOT = deal_root()
_MANIFEST = _DEAL_ROOT / "rag" / "manifest.md"
_CHUNKS_DIR = _DEAL_ROOT / "rag" / "chunks"


@dataclass
class DealChunkRoute:
    chunk: str
    title: str
    tags: List[str]
    workers: List[str]


def _split_csv(raw: str) -> List[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def load_manifest_routes() -> List[DealChunkRoute]:
    if not _MANIFEST.exists():
        return []
    routes: List[DealChunkRoute] = []
    for line in _MANIFEST.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line.startswith("| chunk_"):
            continue
        cols = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        routes.append(
            DealChunkRoute(
                chunk=cols[0],
                title=cols[1],
                tags=_split_csv(cols[2]),
                workers=_split_csv(cols[3]),
            )
        )
    return routes


def list_workers() -> List[str]:
    workers = set()
    for route in load_manifest_routes():
        for worker in route.workers:
            if worker.lower() != "orchestrator":
                workers.add(worker)
    return sorted(workers)


def suggest_workers(query: str, limit: int = 3) -> List[Dict]:
    query_lc = query.lower()
    query_tokens = set(re.findall(r"[a-zA-Z0-9ąćęłńóśźż_-]+", query_lc))
    scored = []
    for route in load_manifest_routes():
        score = 0
        hay = " ".join([route.title, " ".join(route.tags), " ".join(route.workers)]).lower()
        for token in query_tokens:
            if token and token in hay:
                score += 1
        if score:
            for worker in route.workers:
                scored.append(
                    {
                        "worker": worker,
                        "score": score,
                        "chunk": route.chunk,
                        "title": route.title,
                        "tags": route.tags,
                    }
                )
    # dedupe by worker, keep best match
    best: Dict[str, Dict] = {}
    for item in scored:
        worker = item["worker"]
        if worker not in best or item["score"] > best[worker]["score"]:
            best[worker] = item
    result = sorted(best.values(), key=lambda item: (-item["score"], item["worker"]))
    return result[:limit]


def subsystem_info() -> Dict:
    return {
        "name": "the_deal_BOYS",
        "root": str(_DEAL_ROOT),
        "manifest": str(_MANIFEST),
        "chunks_dir": str(_CHUNKS_DIR),
        "chunk_count": len(list(_CHUNKS_DIR.glob("chunk_*.md"))) if _CHUNKS_DIR.exists() else 0,
        "workers": list_workers(),
    }
