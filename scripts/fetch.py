"""Fetch new items from enabled sources into data/items/YYYY/MM/YYYY-MM-DD.jsonl.

Usage: python scripts/fetch.py [--since YYYY-MM-DD] [--days N] [--source ID]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys

import requests
import yaml

from common import load_items, load_yaml, merge_item, parse_date, save_items, today

UA = {"User-Agent": "agent-frontier/0.1 (+https://github.com/demoleiwang/agent-frontier)"}
EXCERPT_CHARS = 1500


def get(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    return r.text


def split_frontmatter(md: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", md, re.S)
    if not m:
        return {}, md
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, md[m.end():]


def md_to_text(md: str) -> str:
    """Rough markdown/HTML -> plain prose, good enough for excerpts and keyword matching."""
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"<(figure|svg|script|style|table)\b.*?</\1>", " ", md, flags=re.S | re.I)
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    lines = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", ">", "[[")):
            continue
        s = re.sub(r"[*_`]+", "", s)
        lines.append(s)
    return html.unescape(re.sub(r"\s+", " ", " ".join(lines))).strip()


def authors_of(meta: dict) -> list[str]:
    out = []
    for a in meta.get("authors") or []:
        if isinstance(a, dict) and a.get("user"):
            out.append(a["user"])
        elif isinstance(a, str):
            out.append(a)
    return out


def fetch_github_blog_index(src: dict, since: dt.date, known: set[str]) -> list[dict]:
    raw = f"https://raw.githubusercontent.com/{src['repo']}/{src.get('branch', 'main')}"
    index = yaml.safe_load(get(f"{raw}/{src['index']}"))
    out = []
    for e in index:
        d = parse_date(e.get("date"))
        if not d or d < since or not e.get("local"):
            continue
        local = e["local"]
        iid = f"{src['id']}:{local}"
        try:
            meta, body = split_frontmatter(get(f"{raw}/{local}.md"))
        except requests.RequestException as ex:
            print(f"  ! {local}: {ex}", file=sys.stderr)
            if iid in known:
                continue
            meta, body = {}, ""
        text = md_to_text(body)
        out.append({
            "id": iid,
            "source": src["id"],
            "title": str(meta.get("title") or local).strip(),
            "url": src["url_template"].format(local=local),
            "date": d.isoformat(),
            "authors": authors_of(meta),
            "source_tags": list(e.get("tags") or []),
            "tags": list(src.get("tags") or []),
            "excerpt": text[:EXCERPT_CHARS],
        })
    return out


def fetch_rss(src: dict, since: dt.date, known: set[str]) -> list[dict]:
    import feedparser

    feed = feedparser.parse(get(src["url"]))
    out = []
    for e in feed.entries:
        t = e.get("published_parsed") or e.get("updated_parsed")
        if not t:
            continue
        d = dt.date(t.tm_year, t.tm_mon, t.tm_mday)
        if d < since:
            continue
        link = e.get("link", "")
        slug = link.rstrip("/").rsplit("/", 1)[-1] or link
        out.append({
            "id": f"{src['id']}:{slug}",
            "source": src["id"],
            "title": e.get("title", "").strip(),
            "url": link,
            "date": d.isoformat(),
            "authors": [a.get("name") for a in e.get("authors", []) if a.get("name")],
            "source_tags": [t.get("term") for t in e.get("tags", []) if t.get("term")],
            "tags": list(src.get("tags") or []),
            "excerpt": md_to_text(e.get("summary", ""))[:EXCERPT_CHARS],
        })
    return out


FETCHERS = {"github_blog_index": fetch_github_blog_index, "rss": fetch_rss}


def run_source(src: dict, since: dt.date, known: set[str]) -> list[dict]:
    try:
        return FETCHERS[src["type"]](src, since, known)
    except Exception as ex:  # noqa: BLE001 - one broken source must not kill the daily run
        fb = src.get("fallback")
        if not fb:
            raise
        print(f"  ! {src['id']} ({src['type']}) failed: {ex}; trying fallback {fb['type']}", file=sys.stderr)
        return FETCHERS[fb["type"]]({**src, **fb}, since, known)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD, inclusive")
    ap.add_argument("--days", type=int, default=14, help="lookback when --since is not given")
    ap.add_argument("--source", help="only this source id")
    args = ap.parse_args()
    since = parse_date(args.since) if args.since else today() - dt.timedelta(days=args.days)

    items = load_items()
    total_new = 0
    for src in load_yaml("sources.yaml"):
        if args.source and src["id"] != args.source:
            continue
        if not src.get("enabled", True):
            continue
        if src["type"] not in FETCHERS:
            print(f"- {src['id']}: type {src['type']} not implemented yet, skipped")
            continue
        try:
            rows = run_source(src, since, set(items))
        except Exception as ex:  # noqa: BLE001
            print(f"- {src['id']}: FAILED {ex}", file=sys.stderr)
            continue
        n = sum(merge_item(items, r) for r in rows)
        total_new += n
        print(f"- {src['id']}: {len(rows)} items since {since}, {n} new")
    save_items(items)
    print(f"total new: {total_new}")


if __name__ == "__main__":
    main()
