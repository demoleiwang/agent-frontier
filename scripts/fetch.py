"""Fetch new items from enabled sources into data/items/YYYY/MM/YYYY-MM-DD.jsonl.

Usage: python scripts/fetch.py [--since YYYY-MM-DD] [--days N] [--source ID]
"""
from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
import yaml

from common import ROOT, load_items, load_yaml, merge_item, parse_date, save_items, today

import json

# url -> published date for scraped pages, so old pages discovered via sitemap are not re-opened every run
SCRAPE_CACHE = ROOT / "data" / "scrape_dates.json"


def load_scrape_cache() -> dict[str, str]:
    try:
        return json.loads(SCRAPE_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_scrape_cache(cache: dict[str, str]) -> None:
    SCRAPE_CACHE.write_text(json.dumps(dict(sorted(cache.items())), indent=0) + "\n", encoding="utf-8")

UA = {"User-Agent": "agent-frontier/0.1 (+https://github.com/demoleiwang/agent-frontier)"}
EXCERPT_CHARS = 1500


@functools.lru_cache(maxsize=64)
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
        cats = [t.get("term") for t in e.get("tags", []) if t.get("term")]
        if set(cats) & set(src.get("exclude_categories") or []):
            continue
        out.append({
            # id_prefix lets several feeds of one lab (e.g. OpenAI news + research) dedupe to one id
            "id": f"{src.get('id_prefix', src['id'])}:{slug}",
            "source": src["id"],
            "title": e.get("title", "").strip(),
            "url": link,
            "date": d.isoformat(),
            "authors": [a.get("name") for a in e.get("authors", []) if a.get("name")],
            "source_tags": cats,
            "tags": list(src.get("tags") or []),
            "excerpt": md_to_text(e.get("summary", ""))[:EXCERPT_CHARS],
        })
    return out


MONTH_DATE = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b")


# Site-wide boilerplate some pages fall back to; useless as an excerpt.
GENERIC_DESCRIPTIONS = {
    "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.",
}


def _meta(h: str, prop: str) -> str:
    m = re.search(rf'<meta[^>]+(?:property|name)="{prop}"[^>]+content="([^"]*)"', h) or \
        re.search(rf'<meta[^>]+content="([^"]*)"[^>]+(?:property|name)="{prop}"', h)
    return html.unescape(m.group(1)).strip() if m else ""


def parse_article(h: str) -> dict:
    """Title / published date / description / body excerpt from a server-rendered article page."""
    title = _meta(h, "og:title")
    if not title:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    d = None
    m = re.search(r'"datePublished":"(\d{4}-\d{2}-\d{2})', h) or \
        re.search(r'article:published_time" content="(\d{4}-\d{2}-\d{2})', h) or \
        re.search(r'<time[^>]+dateTime="(\d{4}-\d{2}-\d{2})', h, re.I)
    if m:
        d = parse_date(m.group(1))
    h1 = h.find("<h1")
    body = h[h1:] if h1 >= 0 else h
    paras = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
    paras = [re.sub(r"\s+", " ", p) for p in paras if len(p) > 40]
    desc = _meta(h, "og:description") or _meta(h, "description")
    if desc and desc in GENERIC_DESCRIPTIONS:
        desc = ""
    return {"title": title, "date": d, "description": desc, "text": " ".join(paras)}


def scrape_listing(src: dict) -> dict[str, dt.date | None]:
    """URL -> listing date (None if the listing shows none) for links matching src['link_pattern']."""
    pat = re.compile(src["link_pattern"])
    found: dict[str, dt.date | None] = {}
    for page in src.get("listing_urls", []):
        h = get(page)
        for m in re.finditer(r'<a\b[^>]*href="([^"#?]+)"[^>]*>(.*?)</a>', h, re.S):
            url = urljoin(page, m.group(1))
            if not pat.search(urlparse(url).path):
                continue
            dm = MONTH_DATE.search(re.sub(r"<[^>]+>", " ", m.group(2)))
            d = parse_date(dm.group(0)) if dm else None
            if found.get(url) is None:
                found[url] = d
    if src.get("sitemap"):  # discovery only: lastmod is when the page was touched, not published
        since_mod = src.get("_since")
        for loc, mod in re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?", get(src["sitemap"])):
            if pat.search(urlparse(loc).path) and (not since_mod or not mod or mod[:10] >= since_mod.isoformat()):
                found.setdefault(loc, None)
    return found


def fetch_scrape(src: dict, since: dt.date, known: set[str]) -> list[dict]:
    src = {**src, "_since": since}
    cache = load_scrape_cache()
    out = []
    for url, listed in scrape_listing(src).items():
        listed = listed or parse_date(cache.get(url, ""))
        if listed and listed < since:
            continue
        slug = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
        iid = f"{src['id']}:{slug}"
        if iid in known:  # already stored; re-scraping old posts every run is wasted requests
            continue
        try:
            art = parse_article(get(url))
            time.sleep(src.get("delay", 0.2))
        except requests.RequestException as ex:
            print(f"  ! {url}: {ex}", file=sys.stderr)
            continue
        d = art["date"] or listed
        if d:
            cache[url] = d.isoformat()
        if not d or d < since:
            continue
        excerpt = (art["description"] + " " + art["text"]).strip()
        out.append({
            "id": iid,
            "source": src["id"],
            "title": art["title"] or slug,
            "url": url,
            "date": d.isoformat(),
            "authors": [],
            "source_tags": [],
            "tags": list(src.get("tags") or []),
            "excerpt": excerpt[:EXCERPT_CHARS],
        })
    save_scrape_cache(cache)
    return out


FETCHERS = {"github_blog_index": fetch_github_blog_index, "rss": fetch_rss, "scrape": fetch_scrape}


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
