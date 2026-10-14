"""Tag items with topics and a relevance score; fill an extractive tldr.

Stage 1 (now): keyword matching from config/topics.yaml.
Stage 2 (later): send only keyword hits to an LLM for scoring + one-line tldr.

Usage: python scripts/classify.py [--all]
"""
from __future__ import annotations

import argparse
import re

from common import load_items, load_yaml, save_items

TITLE_W, TAG_W, BODY_W = 3.0, 2.0, 1.0
SATURATION = 6.0        # raw points at which a topic scores 1.0
MIN_TOPIC_SCORE = 0.15


def compile_kw(kw: str) -> re.Pattern:
    esc = re.escape(kw.lower()).replace(r"\ ", r"[\s\-_]+")
    if len(kw) <= 4 or kw.isupper():
        return re.compile(rf"(?<![a-z0-9]){esc}(?![a-z0-9])", re.I)
    return re.compile(rf"(?<![a-z0-9]){esc}", re.I)


def extract_tldr(text: str, limit: int = 220) -> str:
    out = ""
    for s in re.split(r"(?<=[.!?。])\s+", text):
        if out and len(out) + len(s) > limit:
            break
        out = f"{out} {s}".strip()
    return out[:limit].rstrip() + ("…" if len(out) > limit else "")


def classify(it: dict, topics: dict, authors: set[str]) -> None:
    title = it.get("title", "")
    tags = " ".join(it.get("source_tags", []) + it.get("tags", []))
    body = it.get("excerpt", "")
    scores = {}
    for name, cfg in topics.items():
        raw = 0.0
        for kw in cfg.get("keywords", []):
            p = compile_kw(kw)
            if p.search(title):
                raw += TITLE_W
            elif p.search(tags):
                raw += TAG_W
            elif p.search(body):
                raw += BODY_W
        s = min(1.0, raw / SATURATION) * cfg.get("weight", 1.0)
        if s >= MIN_TOPIC_SCORE:
            scores[name] = round(s, 2)
    it["topics"] = sorted(scores, key=scores.get, reverse=True)
    it["score"] = max(scores.values(), default=0.0)
    if authors & set(it.get("authors", [])):
        it["pinned"] = True
        it["score"] = 1.0
    if it.get("tldr_source") not in ("llm", "manual"):
        it["tldr"] = extract_tldr(body)
        it["tldr_source"] = "extract"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="re-classify every item, not only unclassified ones")
    args = ap.parse_args()
    cfg = load_yaml("topics.yaml")
    authors = set(cfg.pop("authors", None) or [])
    items = load_items()
    n = 0
    for it in items.values():
        if args.all or "topics" not in it:
            classify(it, cfg, authors)
            n += 1
    save_items(items)
    print(f"classified {n} items")


if __name__ == "__main__":
    main()
