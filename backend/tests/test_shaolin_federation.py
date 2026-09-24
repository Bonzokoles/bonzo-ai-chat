# -*- coding: utf-8 -*-
"""Tests for the 36 Chambers federation bridge wired into the chat retrieval.

Covers: enable flag, fail-soft behaviour, context/source injection, and a live
integration check against the canonical orchestrator (skipped if unavailable).
"""

import os
import sys
from pathlib import Path

import pytest

_TESTS_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _TESTS_DIR.parent
_APP_DIR = _BACKEND_DIR / "app"
_BUCH_ROOT = _BACKEND_DIR.parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))


def _load_buch_env():
    """Best-effort: load The_Buch .env chain so CHAMBERS_* resolve in the test env."""
    env_file = _BUCH_ROOT / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and val:
            os.environ.setdefault(key, val)


_load_buch_env()

import shaolin_bridge  # noqa: E402
import main as main_module  # noqa: E402


def _reset_bridge_cache(monkeypatch):
    monkeypatch.setattr(shaolin_bridge, "_ORCH_MODULE", None, raising=False)
    monkeypatch.setattr(shaolin_bridge, "_LOAD_ERROR", None, raising=False)


def test_enabled_default_true(monkeypatch):
    monkeypatch.delenv("SHAOLIN_FEDERATION", raising=False)
    assert shaolin_bridge.enabled() is True


def test_disabled_flag(monkeypatch):
    monkeypatch.setenv("SHAOLIN_FEDERATION", "0")
    assert shaolin_bridge.enabled() is False


def test_fail_soft_when_orchestrator_missing(monkeypatch, tmp_path):
    _reset_bridge_cache(monkeypatch)
    monkeypatch.setenv("CHAMBERS_ORCHESTRATOR", str(tmp_path / "nope.py"))
    monkeypatch.setenv("CHAMBERS_ROOT", str(tmp_path))
    assert shaolin_bridge.federated_context("co wiesz o sist2?") == ("", [])


def test_federated_context_disabled_returns_empty(monkeypatch):
    monkeypatch.setenv("SHAOLIN_FEDERATION", "0")
    assert shaolin_bridge.federated_context("anything") == ("", [])


def test_apply_federation_appends_context_and_sources(monkeypatch):
    fake_ctx = "--- KONTEKST Z FEDERACJI 36 CHAMBERS (read-only) ---\n[chamber:03] x\n---"
    fake_hits = [{"source": "chamber:03", "text": "", "score": 0.9, "chamber_id": 3, "record_id": "42"}]
    monkeypatch.setattr(shaolin_bridge, "federated_context", lambda q, limit=6: (fake_ctx, fake_hits))
    ctx, hits = main_module._apply_shaolin_federation(
        "q", "BAZA", [{"source": "PINKY_one/a", "text": "t", "score": 1.0}]
    )
    assert "FEDERACJI 36 CHAMBERS" in ctx and "BAZA" in ctx
    sources = [h["source"] for h in hits]
    assert "chamber:03" in sources and "PINKY_one/a" in sources


def test_apply_federation_noop_when_empty(monkeypatch):
    monkeypatch.setattr(shaolin_bridge, "federated_context", lambda q, limit=6: ("", []))
    ctx, hits = main_module._apply_shaolin_federation("q", "BAZA", [])
    assert ctx == "BAZA"
    assert hits == []


def test_apply_federation_is_fail_soft(monkeypatch):
    def _boom(q, limit=6):
        raise RuntimeError("adapter exploded")
    monkeypatch.setattr(shaolin_bridge, "federated_context", _boom)
    ctx, hits = main_module._apply_shaolin_federation("q", "BAZA", [])
    assert ctx == "BAZA" and hits == []


@pytest.mark.skipif(not shaolin_bridge.is_available(), reason="canonical orchestrator unavailable in test env")
def test_live_federation_returns_chamber_sources():
    ctx, hits = shaolin_bridge.federated_context("co wiesz o sist2?", limit=4)
    assert ctx, "live federation should return a context block"
    assert hits, "live federation should return at least one source"
    assert all(h["source"].startswith("chamber:") for h in hits)
