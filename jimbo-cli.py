#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_BASE = "http://127.0.0.1:4149"


def _request(method: str, base_url: str, path: str, payload=None, expect_binary: bool = False):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(base_url.rstrip("/") + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            if expect_binary:
                return body
            txt = body.decode("utf-8", errors="replace")
            if not txt.strip():
                return {}
            return json.loads(txt)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {raw}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Brak połączenia z backendem: {e}") from e


def cmd_health(args):
    out = _request("GET", args.base_url, "/api/health")
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_research(args):
    out = _request("POST", args.base_url, "/api/knowledge/research_web", {"query": args.query, "max_results": args.max_results})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_tmdb(args):
    out = _request("POST", args.base_url, "/api/knowledge/ingest_tmdb", {"query": args.query, "limit": args.limit})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_decide(args):
    out = _request(
        "POST",
        args.base_url,
        "/api/decision/coach",
        {"topic": args.topic, "options": args.options or [], "constraints": args.constraints or []},
    )
    print(out.get("answer", "Brak odpowiedzi"))


def cmd_memory_show(args):
    out = _request("GET", args.base_url, "/api/diary")
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_memory_add_fact(args):
    out = _request("POST", args.base_url, "/api/diary/fact", {"fact": args.fact})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_memory_add_pref(args):
    out = _request("POST", args.base_url, "/api/diary/preference", {"preference": args.preference})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_memory_add_goal(args):
    out = _request("POST", args.base_url, "/api/diary/goal", {"goal": args.goal})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_memory_clear(args):
    out = _request("DELETE", args.base_url, "/api/diary")
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="EastWood Ops CLI - sterowanie lokalnym backendem")
    parser.add_argument("--base-url", default=DEFAULT_BASE, help="Adres backendu, np. http://127.0.0.1:4149")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_health = sub.add_parser("health", help="Status backendu")
    p_health.set_defaults(func=cmd_health)

    p_research = sub.add_parser("research", help="Wyszukaj web i zapisz do knowledge_mood/web_research")
    p_research.add_argument("query")
    p_research.add_argument("--max-results", type=int, default=5)
    p_research.set_defaults(func=cmd_research)

    p_tmdb = sub.add_parser("tmdb", help="Pobierz dane filmowe z TMDB do knowledge_mood/movies_api")
    p_tmdb.add_argument("query")
    p_tmdb.add_argument("--limit", type=int, default=5)
    p_tmdb.set_defaults(func=cmd_tmdb)

    p_decide = sub.add_parser("decide", help="Doradca decyzji (profil + ograniczenia)")
    p_decide.add_argument("topic")
    p_decide.add_argument("--option", dest="options", action="append", help="Opcja decyzji, możesz podać kilka")
    p_decide.add_argument("--constraint", dest="constraints", action="append", help="Ograniczenie, możesz podać kilka")
    p_decide.set_defaults(func=cmd_decide)

    p_memory = sub.add_parser("memory", help="Operacje na pamięci/dzienniku")
    memory_sub = p_memory.add_subparsers(dest="memory_cmd", required=True)

    p_m_show = memory_sub.add_parser("show", help="Pokaż pełną pamięć")
    p_m_show.set_defaults(func=cmd_memory_show)

    p_m_fact = memory_sub.add_parser("add-fact", help="Dodaj fakt")
    p_m_fact.add_argument("fact")
    p_m_fact.set_defaults(func=cmd_memory_add_fact)

    p_m_pref = memory_sub.add_parser("add-pref", help="Dodaj preferencję")
    p_m_pref.add_argument("preference")
    p_m_pref.set_defaults(func=cmd_memory_add_pref)

    p_m_goal = memory_sub.add_parser("add-goal", help="Dodaj cel")
    p_m_goal.add_argument("goal")
    p_m_goal.set_defaults(func=cmd_memory_add_goal)

    p_m_clear = memory_sub.add_parser("clear", help="Wyczyść pamięć")
    p_m_clear.set_defaults(func=cmd_memory_clear)

    args = parser.parse_args()
    try:
        args.func(args)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
