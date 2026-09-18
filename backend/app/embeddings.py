"""
Semantic Embedding Index for EastWood Ops
========================================
- Model: paraphrase-multilingual-MiniLM-L12-v2 (supports Polish + EN)
- KB index: semantic search over knowledge_mood/ files
- Character index: few-shot assistant examples from DATASETNO2_clean.jsonl
- Builds in background thread — non-blocking startup
"""

import os
import json
import threading
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple

KB_DIR = Path(os.getenv("KB_DIR", str(Path(__file__).parent.parent.parent / "knowledge_mood")))
SKIP_DIR_NAMES = {
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
}

_index_instance: Optional["EmbeddingIndex"] = None
_ready = False
_building = False


class EmbeddingIndex:
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    CHUNK_SIZE = 400     # chars per chunk
    MAX_JSONL = 500      # max lines from .jsonl files

    def __init__(self):
        self.model = None
        self.kb_chunks: List[Tuple[str, str]] = []   # (text, source_name)
        self.kb_embeddings: Optional[np.ndarray] = None
        self.char_examples: List[Tuple[str, str]] = []  # (text, style)
        self.char_embeddings: Optional[np.ndarray] = None

    def _load_model(self):
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            print(f"[Embeddings] Loading {self.MODEL_NAME}...")
            self.model = SentenceTransformer(self.MODEL_NAME)
            print("[Embeddings] Model loaded [OK]")
        return self.model

    def _chunk(self, text: str, source: str) -> List[Tuple[str, str]]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.CHUNK_SIZE
            if end < len(text):
                space = text.rfind(" ", start, end)
                if space > start:
                    end = space
            chunk = text[start:end].strip()
            if len(chunk) > 30:  # skip tiny fragments
                chunks.append((chunk, source))
            start = end
        return chunks

    def build_kb_index(self, kb_dir: Path = KB_DIR):
        model = self._load_model()
        self.kb_chunks = []
        text_exts = {".txt", ".md", ".py"}
        max_chunks = 5000

        for fp in sorted(kb_dir.rglob("*")):
            if not fp.is_file():
                continue
            if any(part in SKIP_DIR_NAMES for part in fp.parts):
                continue
            if len(self.kb_chunks) >= max_chunks:
                break
            ext = fp.suffix.lower()
            src = str(fp.relative_to(kb_dir))
            try:
                if ext in text_exts:
                    # Skip huge files — limit chars per file
                    stat = fp.stat()
                    if stat.st_size > 200_000:
                        print(f"[Embeddings] Skip large file: {src} ({stat.st_size//1000}KB)")
                        continue
                    text = fp.read_text(encoding="utf-8", errors="ignore")
                    self.kb_chunks.extend(self._chunk(text, src))
                elif ext == ".jsonl":
                    lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
                    for line in lines[: self.MAX_JSONL]:
                        if len(self.kb_chunks) >= max_chunks:
                            break
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            d = json.loads(line)
                            t = d.get("text") or d.get("content") or d.get("output") or ""
                            if t and isinstance(t, str):
                                self.kb_chunks.extend(self._chunk(t[:600], src))
                        except (json.JSONDecodeError, TypeError):
                            pass
            except Exception as e:
                print(f"[Embeddings] Skip {fp.name}: {e}")

        if self.kb_chunks:
            texts = [c[0] for c in self.kb_chunks]
            print(f"[Embeddings] Encoding {len(texts)} KB chunks...")
            self.kb_embeddings = model.encode(texts, batch_size=64, show_progress_bar=False)
            print(f"[Embeddings] KB index ready: {len(texts)} chunks")

    def build_character_index(self, kb_dir: Path = KB_DIR):
        model = self._load_model()
        self.char_examples = []
        dataset_file = kb_dir / "DATASETNO2_clean.jsonl"
        if not dataset_file.exists():
            brain_dataset = kb_dir.parent / "The_brain" / "DATASETNO2_clean.jsonl"
            if brain_dataset.exists():
                dataset_file = brain_dataset
            else:
                print(f"[Embeddings] Character dataset not found: {dataset_file}")
                return
        with open(dataset_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    text = d.get("text", "")
                    style = d.get("style", "jimbo_core")
                    if text:
                        self.char_examples.append((text, style))
                except json.JSONDecodeError:
                    pass
        if self.char_examples:
            texts = [e[0] for e in self.char_examples]
            self.char_embeddings = model.encode(texts, show_progress_bar=False)
            print(f"[Embeddings] Character index ready: {len(texts)} examples")

    def _cosine(self, q: np.ndarray, corpus: np.ndarray) -> np.ndarray:
        q = q / (np.linalg.norm(q) + 1e-9)
        norms = np.linalg.norm(corpus, axis=1, keepdims=True) + 1e-9
        return (corpus / norms) @ q

    def semantic_search_kb(
        self,
        query: str,
        top_k: int = 5,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> List[Dict]:
        if self.kb_embeddings is None or not self.kb_chunks:
            return []
        q_emb = self._load_model().encode([query])[0]
        scores = self._cosine(q_emb, self.kb_embeddings)
        ranked_idxs = np.argsort(scores)[::-1]
        include_prefixes = [p.replace("\\", "/").strip("/") for p in (include_prefixes or []) if p]
        exclude_prefixes = [p.replace("\\", "/").strip("/") for p in (exclude_prefixes or []) if p]
        top_idxs = []
        for idx in ranked_idxs:
            source = self.kb_chunks[idx][1].replace("\\", "/")
            if include_prefixes and not any(
                source == prefix or source.startswith(prefix + "/") for prefix in include_prefixes
            ):
                continue
            if exclude_prefixes and any(
                source == prefix or source.startswith(prefix + "/") for prefix in exclude_prefixes
            ):
                continue
            top_idxs.append(idx)
            if len(top_idxs) >= top_k:
                break
        return [
            {"text": self.kb_chunks[i][0], "source": self.kb_chunks[i][1], "score": float(scores[i])}
            for i in top_idxs
        ]

    def find_character_examples(
        self,
        query: str,
        top_k: int = 3,
        allowed_styles: Optional[List[str]] = None,
    ) -> List[Dict]:
        if self.char_embeddings is None or not self.char_examples:
            return []
        q_emb = self._load_model().encode([query])[0]
        scores = self._cosine(q_emb, self.char_embeddings)
        ranked_idxs = np.argsort(scores)[::-1]
        allowed = {s.strip().lower() for s in (allowed_styles or []) if s and s.strip()}
        top_idxs = []
        for idx in ranked_idxs:
            style = str(self.char_examples[idx][1]).strip().lower()
            if allowed and style not in allowed:
                continue
            top_idxs.append(idx)
            if len(top_idxs) >= top_k:
                break
        return [
            {"text": self.char_examples[i][0], "style": self.char_examples[i][1], "score": float(scores[i])}
            for i in top_idxs
        ]


def _build_all():
    global _index_instance, _ready, _building
    if _building:
        return
    _building = True
    try:
        idx = EmbeddingIndex()
        idx.build_character_index()
        idx.build_kb_index()
        _index_instance = idx
        _ready = True
        print("[Embeddings] All indexes ready [OK]")
    except Exception as e:
        print(f"[Embeddings] Index build failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        _building = False


def start_background_build():
    """Start embedding index build in daemon thread (non-blocking)."""
    t = threading.Thread(target=_build_all, daemon=True, name="embeddings-build")
    t.start()
    return t


def get_index() -> Optional[EmbeddingIndex]:
    return _index_instance


def is_ready() -> bool:
    return _ready
