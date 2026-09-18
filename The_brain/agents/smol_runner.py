# -*- coding: utf-8 -*-
"""
EastWood Ops / The Buch - Smolagents Cognitive Bridge
=====================================================
Uses Hugging Face smolagents (CodeAgent) to execute Python code actions,
query SQLite databases, inspect agent rules, and automate complex workflows
using MyBonzo Cloudflare Workers AI edge.
"""

from __future__ import annotations

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Path resolution
_CURRENT_DIR = Path(__file__).resolve().parent
_BRAIN_DIR = _CURRENT_DIR.parent
_BUCH_ROOT = _BRAIN_DIR.parent
_BACKEND_APP = _BUCH_ROOT / "backend" / "app"

# Add backend app to sys.path for direct access to loaders
if str(_BACKEND_APP) not in sys.path:
    sys.path.insert(0, str(_BACKEND_APP))

# Load .env
for env_candidate in [_BUCH_ROOT / ".env", _BUCH_ROOT / ".env.runtime", _BUCH_ROOT / "backend" / ".env"]:
    if env_candidate.exists():
        load_dotenv(env_candidate)

from smolagents import CodeAgent, OpenAIServerModel, tool
import coding_rules_loader as crl
import deal_ops_loader as dol
import private_help_loader as phl

# Configuration
CF_API_BASE = os.getenv("CLOUDFLARE_BASE_URL", "https://mybonzo-v3.stolarnia-ams.workers.dev/v1")
CF_API_KEY = os.getenv("CLOUDFLARE_API_KEY", "BonzoToken2026")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "@cf/meta/llama-3.3-70b-instruct-fp8-fast")


@tool
def search_agent_rules(query: str, tier: str = "nano") -> str:
    """Searches and returns engineering rules from The_brain/coding/agent-rules-books.
    
    Args:
        query: The technical topic (e.g. 'clean code', 'refactoring', 'legacy', 'ddd', 'architecture').
        tier: Detail level ('nano', 'mini', 'full'). Defaults to 'nano'.
    """
    context, sources = crl.build_coding_context(query, tier=tier, limit=2)
    if not context:
        return f"No matching rules found for '{query}'."
    return f"Matched sources: {sources}\n\n{context}"


@tool
def search_shop_knowledge(query: str) -> str:
    """Searches PINKY_one e-commerce and store operations knowledge base.
    
    Args:
        query: Topic to search (e.g. 'shopify', 'produkty', 'kolekcje', 'wdrożenie').
    """
    hits = phl.search_docs(query, limit=3)
    if not hits:
        return f"No store knowledge found for '{query}'."
    results = []
    for h in hits:
        results.append(f"[{h.get('source', 'doc')}]\n{h.get('text', '')}")
    return "\n---\n".join(results)


@tool
def search_deal_ops(query: str) -> str:
    """Searches the_deal_BOYS wholesale, sourcing, arbitrage and Polaczki worker operations.
    
    Args:
        query: Deal or sourcing topic (e.g. 'marża', 'b2b', 'hurt', 'hurtownie').
    """
    workers = dol.suggest_workers(query, limit=3)
    return f"Workers for '{query}':\n" + json.dumps(workers, indent=2, ensure_ascii=False)


@tool
def query_sqlite(db_name: str, query: str) -> str:
    """Runs a read-only SQL SELECT query against a local SQLite database in The Buch.
    
    Args:
        db_name: Name of the database file (e.g. 'chat.db' or 'meblepumo.db').
        query: The SQL SELECT query to execute.
    """
    if not query.strip().lower().startswith("select") and not query.strip().lower().startswith("pragma"):
        return "[ERR] Only read-only SELECT or PRAGMA statements are permitted."

    db_path = _BUCH_ROOT / "backend" / db_name
    if not db_path.exists():
        db_path = _BUCH_ROOT / db_name
    if not db_path.exists():
        return f"[ERR] Database '{db_name}' not found."

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(50)
        col_names = [d[0] for d in cursor.description] if cursor.description else []
        conn.close()
        return json.dumps({"columns": col_names, "rows": rows, "count": len(rows)}, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"[ERR] SQLite error: {e}"


def create_smol_agent(model_id: Optional[str] = None) -> CodeAgent:
    """Creates a configured CodeAgent connected to MyBonzo Cloudflare Workers AI."""
    model_name = model_id or DEFAULT_MODEL
    llm = OpenAIServerModel(
        model_id=model_name,
        api_base=CF_API_BASE,
        api_key=CF_API_KEY,
    )
    tools = [
        search_agent_rules,
        search_shop_knowledge,
        search_deal_ops,
        query_sqlite,
    ]
    agent = CodeAgent(
        tools=tools,
        model=llm,
        additional_authorized_imports=["re", "json", "math", "datetime", "pathlib", "collections", "sqlite3"],
        max_steps=6,
    )
    return agent


def run_task(task_prompt: str, model_id: Optional[str] = None) -> str:
    """Runs a task prompt through the smolagent and returns the result."""
    agent = create_smol_agent(model_id=model_id)
    result = agent.run(task_prompt)
    return str(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        print(f"[RUN] SmolAgent Task: {task}")
        output = run_task(task)
        print("\n[RESULT]")
        print(output)
    else:
        print("[INFO] Usage: python smol_runner.py <task description>")
