#!/usr/bin/env python3
"""
HuggingFace Dataset Downloader for EastWood Ops Knowledge
========================================================
Downloads coding Q&A datasets and saves them as readable Markdown
into knowledge_mood/coding/ so the semantic search can find them.

Datasets:
  1. iamtarun/python_code_instructions_18k_alpaca  (Python instructions)
  2. sahil2801/CodeAlpaca-20k                       (mixed language coding)

Usage:
  python download_hf_datasets.py
  python download_hf_datasets.py --limit 500 --skip-alpaca
"""

import argparse
import os
from pathlib import Path

KB_DIR = Path(os.getenv("KB_DIR", str(Path(__file__).parent.parent / "knowledge_mood"))) / "coding"
KB_DIR.mkdir(parents=True, exist_ok=True)


def save_markdown(entries: list[dict], out_path: Path, dataset_name: str):
    """Save list of {instruction, input, output} as readable Markdown."""
    lines = [f"# {dataset_name}\n", f"Total: {len(entries)} examples\n\n"]
    for i, entry in enumerate(entries, 1):
        instruction = entry.get("instruction", "").strip()
        inp = entry.get("input", "").strip()
        output = entry.get("output", "").strip()
        lines.append(f"## Q{i}: {instruction[:120]}\n")
        if inp:
            lines.append(f"**Input:**\n```\n{inp[:400]}\n```\n")
        lines.append(f"**Answer:**\n{output[:800]}\n\n---\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"  Saved {len(entries)} examples → {out_path.name} ({size_kb:.0f} KB)")


def download_python_alpaca(limit: int):
    print(f"\n[1/2] Downloading python_code_instructions_18k_alpaca (limit={limit})...")
    from datasets import load_dataset
    ds = load_dataset("iamtarun/python_code_instructions_18k_alpaca", split=f"train[:{limit}]")
    entries = [
        {
            "instruction": row.get("instruction", ""),
            "input": row.get("input", ""),
            "output": row.get("output", ""),
        }
        for row in ds
    ]
    save_markdown(entries, KB_DIR / "python_instructions.md", "Python Code Instructions (Alpaca)")


def download_code_alpaca(limit: int):
    print(f"\n[2/2] Downloading CodeAlpaca-20k (limit={limit})...")
    from datasets import load_dataset
    ds = load_dataset("sahil2801/CodeAlpaca-20k", split=f"train[:{limit}]")
    entries = [
        {
            "instruction": row.get("instruction", ""),
            "input": row.get("input", ""),
            "output": row.get("output", ""),
        }
        for row in ds
    ]
    save_markdown(entries, KB_DIR / "code_alpaca.md", "CodeAlpaca Mixed Languages")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download HF coding datasets to KB")
    parser.add_argument("--limit", type=int, default=300, help="Max examples per dataset (default: 300)")
    parser.add_argument("--skip-alpaca", action="store_true", help="Skip python alpaca")
    parser.add_argument("--skip-code", action="store_true", help="Skip CodeAlpaca-20k")
    args = parser.parse_args()

    print(f"KB target: {KB_DIR}")
    errors = []

    if not args.skip_alpaca:
        try:
            download_python_alpaca(args.limit)
        except Exception as e:
            print(f"  ❌ python_alpaca failed: {e}")
            errors.append("python_alpaca")

    if not args.skip_code:
        try:
            download_code_alpaca(args.limit)
        except Exception as e:
            print(f"  ❌ code_alpaca failed: {e}")
            errors.append("code_alpaca")

    print("\n✅ Done!" if not errors else f"\n⚠️ Completed with errors: {errors}")
    print(f"Files in {KB_DIR}:")
    for f in sorted(KB_DIR.iterdir()):
        print(f"  {f.name} ({f.stat().st_size // 1024} KB)")
