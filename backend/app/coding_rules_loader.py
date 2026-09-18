# -*- coding: utf-8 -*-
"""
Loader for software engineering rules & books from The_brain/coding/agent-rules-books.
Provides instant access to full, mini, and nano architectural rule sets.
"""

from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_APP_DIR = Path(__file__).resolve().parent
_BUCH_ROOT = _APP_DIR.parent.parent

_CANDIDATE_ROOTS = [
    _BUCH_ROOT / "The_brain" / "coding" / "agent-rules-books",
    _BUCH_ROOT / "The_brain" / "coding" / "agent-rules-books" / "_rule-workbench",
]

BOOK_METADATA = {
    "clean-code": {
        "title": "Clean Code (Robert C. Martin)",
        "keywords": ["clean", "naming", "function", "refactor", "comment", "smell", "readable", "mutation", "dry"],
    },
    "clean-architecture": {
        "title": "Clean Architecture (Robert C. Martin)",
        "keywords": ["architecture", "boundaries", "entities", "use-case", "controller", "dependency-rule", "port", "adapter"],
    },
    "a-philosophy-of-software-design": {
        "title": "A Philosophy of Software Design (John Ousterhout)",
        "keywords": ["complexity", "deep module", "interface", "information hiding", "exception", "abstraction"],
    },
    "code-complete": {
        "title": "Code Complete (Steve McConnell)",
        "keywords": ["routine", "variable", "quality", "construction", "defensive", "pseudocode", "checklist"],
    },
    "designing-data-intensive-applications": {
        "title": "Designing Data-Intensive Applications (Martin Kleppmann)",
        "keywords": ["data", "replication", "partition", "consistency", "transaction", "consensus", "batch", "stream", "database", "distributed"],
    },
    "domain-driven-design": {
        "title": "Domain-Driven Design (Eric Evans)",
        "keywords": ["ddd", "domain", "ubiquitous language", "aggregate", "entity", "value object", "repository", "bounded context"],
    },
    "domain-driven-design-distilled": {
        "title": "Domain-Driven Design Distilled (Vaughn Vernon)",
        "keywords": ["ddd", "context map", "core domain", "subdomain", "event storming", "aggregate", "domain event"],
    },
    "implementing-domain-driven-design": {
        "title": "Implementing Domain-Driven Design (Vaughn Vernon)",
        "keywords": ["iddd", "aggregate root", "domain service", "application service", "event sourcing", "cqrs", "repository"],
    },
    "patterns-of-enterprise-application-architecture": {
        "title": "Patterns of Enterprise Application Architecture (Martin Fowler)",
        "keywords": ["poeaa", "pattern", "data mapper", "active record", "unit of work", "table module", "service layer"],
    },
    "refactoring": {
        "title": "Refactoring (Martin Fowler)",
        "keywords": ["refactoring", "extract", "inline", "code smell", "primitive obsession", "switch statements", "temporary field"],
    },
    "refactoring-guru": {
        "title": "Refactoring Guru Patterns",
        "keywords": ["creational", "structural", "behavioral", "design patterns", "factory", "singleton", "strategy", "observer", "adapter"],
    },
    "release-it": {
        "title": "Release It! (Michael Nygard)",
        "keywords": ["circuit breaker", "bulkhead", "timeout", "fail-safe", "stability", "production", "resilience", "capacity"],
    },
    "the-pragmatic-programmer": {
        "title": "The Pragmatic Programmer (Thomas & Hunt)",
        "keywords": ["pragmatic", "dry", "orthogonality", "tracer bullets", "prototyping", "broken windows", "good-enough"],
    },
    "working-effectively-with-legacy-code": {
        "title": "Working Effectively with Legacy Code (Michael Feathers)",
        "keywords": ["legacy", "characterization test", "seam", "sensing", "dependency breaking", "sprout method", "wrap method"],
    },
}


def coding_rules_root() -> Path:
    for candidate in _CANDIDATE_ROOTS:
        if candidate.exists() and any(candidate.iterdir()):
            return candidate
    return _CANDIDATE_ROOTS[0]


def list_books() -> List[Dict]:
    root = coding_rules_root()
    if not root.exists():
        return []

    books = []
    for item in sorted(root.iterdir()):
        if not item.is_dir() or item.name.startswith((".", "_")):
            continue
        slug = item.name
        meta = BOOK_METADATA.get(slug, {"title": slug.replace("-", " ").title(), "keywords": []})
        nano_file = item / f"{slug}.nano.md"
        mini_file = item / f"{slug}.mini.md"
        full_file = item / f"{slug}.md"

        books.append({
            "slug": slug,
            "title": meta["title"],
            "has_nano": nano_file.exists(),
            "has_mini": mini_file.exists(),
            "has_full": full_file.exists(),
            "keywords": meta["keywords"],
        })
    return books


def get_book_rule(slug: str, tier: str = "nano") -> Optional[str]:
    root = coding_rules_root()
    book_dir = root / slug
    if not book_dir.exists():
        return None

    filename = f"{slug}.nano.md" if tier == "nano" else (f"{slug}.mini.md" if tier == "mini" else f"{slug}.md")
    target = book_dir / filename
    if not target.exists():
        target = book_dir / f"{slug}.nano.md"
    if not target.exists():
        target = book_dir / f"{slug}.md"

    if target.exists():
        return target.read_text(encoding="utf-8", errors="ignore")
    return None


def suggest_rules(query: str, limit: int = 3) -> List[Dict]:
    query_tokens = set(re.findall(r"[a-zA-Z0-9_-]+", query.lower()))
    if not query_tokens:
        return []

    scored = []
    for book in list_books():
        slug = book["slug"]
        meta = BOOK_METADATA.get(slug, {})
        keywords = meta.get("keywords", [])
        title = meta.get("title", slug).lower()

        score = 0
        for token in query_tokens:
            if len(token) < 3:
                continue
            if token in slug:
                score += 3
            if token in title:
                score += 2
            for kw in keywords:
                if token in kw or kw in token:
                    score += 2

        if score > 0:
            scored.append({
                "slug": slug,
                "title": book["title"],
                "score": score,
            })

    scored.sort(key=lambda x: -x["score"])
    return scored[:limit]


def build_coding_context(query: str, tier: str = "nano", limit: int = 2) -> Tuple[str, List[str]]:
    suggestions = suggest_rules(query, limit=limit)
    if not suggestions:
        # Fallback to general clean code & pragmatic programmer if explicit coding prompt
        coding_markers = {"code", "funkcja", "klasa", "refactor", "architektura", "błąd", "debug", "test"}
        q_lower = query.lower()
        if any(m in q_lower for m in coding_markers):
            suggestions = [
                {"slug": "clean-code", "title": BOOK_METADATA["clean-code"]["title"]},
                {"slug": "the-pragmatic-programmer", "title": BOOK_METADATA["the-pragmatic-programmer"]["title"]}
            ]
        else:
            return "", []

    blocks = []
    sources = []
    for sug in suggestions:
        slug = sug["slug"]
        rule_content = get_book_rule(slug, tier=tier)
        if rule_content:
            blocks.append(f"--- ENGINEERING RULE: {sug['title']} ({tier.upper()}) ---\n{rule_content.strip()}")
            sources.append(f"rule:{slug}:{tier}")

    if not blocks:
        return "", []

    context = "\n\n--- INŻYNIERSKIE ZASADY JAKOŚCI KODU (The_brain/coding/agent-rules-books) ---\n" + "\n\n".join(blocks) + "\n---\n"
    return context, sources
