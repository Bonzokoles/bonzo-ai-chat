# -*- coding: utf-8 -*-
"""
Automated unit and integration tests for The Buch (EastWood Ops) core backend.
Validates architecture loaders, knowledge routing, and API contracts.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add app directory to sys.path
_TESTS_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _TESTS_DIR.parent
_APP_DIR = _BACKEND_DIR / "app"
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

import coding_rules_loader as crl
import deal_ops_loader as dol
import private_help_loader as phl
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_coding_rules_books_inventory():
    """Verify that all 14 canonical engineering books are discovered and indexed."""
    books = crl.list_books()
    assert len(books) >= 14
    slugs = {b["slug"] for b in books}
    expected = {
        "clean-code",
        "clean-architecture",
        "designing-data-intensive-applications",
        "domain-driven-design",
        "refactoring",
        "the-pragmatic-programmer",
    }
    assert expected.issubset(slugs)


def test_coding_rules_nano_tier():
    """Verify that nano-tier rules exist and contain actionable decision rules."""
    rule = crl.get_book_rule("clean-code", tier="nano")
    assert rule is not None
    assert "Decision rules" in rule or "OBEY" in rule


def test_coding_rules_matching():
    """Verify semantic keyword matching for engineering rules."""
    suggestions = crl.suggest_rules("refactoring legacy architecture", limit=3)
    assert len(suggestions) > 0
    matched_slugs = [s["slug"] for s in suggestions]
    assert any(s in matched_slugs for s in ["refactoring", "working-effectively-with-legacy-code", "clean-architecture"])


def test_private_help_loader():
    """Verify PINKY_one store documentation loader."""
    docs = phl.list_docs()
    assert len(docs) >= 5
    stems = {d["stem"] for d in docs}
    assert any("produkty" in s or "platforma" in s for s in stems)


def test_deal_ops_loader():
    """Verify the_deal_BOYS sourcing workers and manifest chunks."""
    info = dol.subsystem_info()
    assert info["name"] == "the_deal_BOYS"
    assert info["chunk_count"] >= 14
    assert len(info["workers"]) == 5
    assert "Polaczek_Bohdan_01" in info["workers"]


def test_api_health(client):
    """Verify /api/health endpoint response structure."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "provider" in data


def test_api_task_profiles(client):
    """Verify task profiles include the new coding profile."""
    res = client.get("/api/task-profiles")
    assert res.status_code == 200
    data = res.json()
    assert "coding" in data["profiles"]
    assert data["profiles"]["coding"]["label"] == "Coding & Architecture"


def test_api_coding_rules_match_endpoint(client):
    """Verify /api/coding-rules/match endpoint."""
    res = client.post("/api/coding-rules/match", json={"query": "ddd aggregate root"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["suggestions"]) > 0
    assert "context" in data
