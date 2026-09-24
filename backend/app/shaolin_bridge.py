# -*- coding: utf-8 -*-
"""36 Chambers federation bridge for The Buch chat (READ-ONLY, fail-soft).

Routes knowledge queries through the canonical 36 Chambers orchestrator so the main
chat uses the federated 9-chamber retrieval instead of only local loaders.

Path resolution (36 Chambers rule: no hardcoded absolute paths):
  1. $CHAMBERS_ORCHESTRATOR  (explicit path to shaolin_orchestrator.py)
  2. $CHAMBERS_ROOT/src/orchestrator/shaolin_orchestrator.py

Fail-soft: any error (missing orchestrator, missing deps, adapter failure) returns
empty context so the chat keeps working. Never writes to any chamber.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

_ORCH_MODULE = None
_LOAD_ERROR: str | None = None


def enabled() -> bool:
    """Federation is on unless SHAOLIN_FEDERATION is explicitly disabled."""
    return os.getenv("SHAOLIN_FEDERATION", "1").strip().lower() not in ("0", "false", "no", "off")


def _orchestrator_path() -> Path | None:
    explicit = os.getenv("CHAMBERS_ORCHESTRATOR")
    if explicit and Path(explicit).is_file():
        return Path(explicit)
    root = os.getenv("CHAMBERS_ROOT")
    if root:
        cand = Path(root) / "src" / "orchestrator" / "shaolin_orchestrator.py"
        if cand.is_file():
            return cand
    return None


def _load_orchestrator():
    """Import the canonical orchestrator by file path (named uniquely to avoid the
    stale duplicate that may exist on sys.path)."""
    global _ORCH_MODULE, _LOAD_ERROR
    if _ORCH_MODULE is not None:
        return _ORCH_MODULE
    if _LOAD_ERROR is not None:
        return None
    try:
        path = _orchestrator_path()
        if path is None:
            raise RuntimeError("CHAMBERS_ORCHESTRATOR / CHAMBERS_ROOT not set or file missing")
        # the orchestrator imports its sibling `config.py` via sys.path[parent]
        src_dir = str(path.parents[1])
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        spec = importlib.util.spec_from_file_location("shaolin_orchestrator_canonical", str(path))
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot build import spec for {path}")
        mod = importlib.util.module_from_spec(spec)
        # register BEFORE exec: dataclasses resolve annotations via sys.modules[cls.__module__]
        sys.modules[spec.name] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:
            sys.modules.pop(spec.name, None)
            raise
        _ORCH_MODULE = mod
        return mod
    except Exception as exc:  # fail-soft: remember and degrade
        _LOAD_ERROR = str(exc)
        return None


def is_available() -> bool:
    return enabled() and _load_orchestrator() is not None


def _snippet(text: str, n: int = 400) -> str:
    text = (text or "").strip().replace("\r", " ")
    text = " ".join(text.split())
    return text[:n] + ("..." if len(text) > n else "")


def federated_context(query: str, limit: int = 6):
    """Return (context_block, hits) for chat injection.

    hits are chat-compatible dicts: {"source": "chamber:03", "text": "",
    "score": <float|None>, "chamber_id": <int>, "record_id": <str|None>}.
    Empty ("", []) on any failure so callers need no special-casing.
    """
    if not query or not query.strip() or not enabled():
        return "", []
    mod = _load_orchestrator()
    if mod is None:
        return "", []
    try:
        result = mod.run(query)
    except Exception as exc:  # adapter/orchestrator failure must not break chat
        print(f"[36ch] orchestrator error: {exc}")
        return "", []

    evidence = result.get("sources") or []
    if not evidence:
        return "", []
    evidence = evidence[: max(1, int(limit))]

    lines = ["--- KONTEKST Z FEDERACJI 36 CHAMBERS (read-only) ---"]
    hits = []
    seen = set()
    for ev in evidence:
        cid = ev.get("chamber_id")
        rid = ev.get("record_id")
        src = f"chamber:{int(cid):02d}" if isinstance(cid, int) else f"chamber:{cid}"
        score = ev.get("score")
        lines.append(f"[{src} | record={rid} | score={score}] {_snippet(ev.get('content', ''))}")
        key = (src, rid)
        if key in seen:
            continue
        seen.add(key)
        hits.append({
            "source": src,
            "text": "",
            "score": score,
            "chamber_id": cid,
            "record_id": rid,
        })
    lines.append("---")
    return "\n".join(lines), hits
