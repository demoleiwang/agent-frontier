"""Tag items with topics and a relevance score; fill an extractive tldr.

Stage 1 (now): keyword matching from config/topics.yaml.
Stage 2 (later): send only keyword hits to an LLM for scoring + one-line tldr.

Usage: python scripts/classify.py [--all]
"""
from __future__ import annotations

import argparse
import math
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


def reputation(it: dict, rep: dict) -> tuple[float, list[str]]:
    """0-1 reputation for papers from community, institution, author, venue and code signals, plus readable reasons."""
    w, reasons, parts = rep["weights"], [], {}
    up = it.get("upvotes") or 0
    if up:
        parts["upvotes"] = min(1.0, math.log1p(up) / math.log1p(rep.get("upvotes_full", 100)))
        reasons.append(f"HF {up}↑")
    inst = (it.get("institution") or "").lower()
    if inst:
        for tier, names in rep["institutions"].items():
            if tier == "tier_weight":
                continue
            if any(n.lower() in inst for n in names):
                parts["inst"] = max(parts.get("inst", 0), rep["institutions"]["tier_weight"][tier])
        reasons.append(it["institution"])
    hit = [a for a in it.get("authors", []) if a in rep["_authors"]]
    if hit:
        parts["author"] = 1.0
        reasons.append("作者: " + ", ".join(hit[:2]))
    comment = it.get("comment") or ""
    venue = next((v for v in rep["venues"] if re.search(rf"\b{re.escape(v)}\b", comment)), None)
    if venue and re.search(r"accept|published|to appear|camera", comment, re.I):
        parts["venue"] = 1.0
        reasons.append(f"{venue} 录用")
    if it.get("github_repo"):
        parts["code"] = 1.0
        reasons.append("code")
    return round(min(1.0, sum(w[k] * v for k, v in parts.items())), 2), reasons


def classify(it: dict, topics: dict, authors: set[str]) -> None:
    title = it.get("title", "")
    tags = " ".join(it.get("source_tags", []) + it.get("tags", []))
    body = it.get("excerpt", "")
    scores = {}
    for name, cfg in topics.items():
        req = cfg.get("requires_any")
        if req and not any(compile_kw(k).search(f"{title} {body}") for k in req):
            continue
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
    rep = load_yaml("reputation.yaml")
    rep["_authors"] = set(rep.get("authors") or [])
    items = load_items()
    n = 0
    for it in items.values():
        if args.all or "topics" not in it:
            classify(it, cfg, authors)
            n += 1
        if "paper" in it.get("tags", []):  # signals (upvotes, venue) can change on refetch: always recompute
            it["rep"], it["rep_reasons"] = reputation(it, rep)
    save_items(items)
    print(f"classified {n} items")


if __name__ == "__main__":
    main()
