"""Build the dashboard: site/data.json (everything the page shows) and two HTML shells around site/template.html.

- site/index.html    full document, for GitHub Pages or any static host
- site/artifact.html body-only content, for publishing as a claude.ai Artifact

Both embed a snapshot of data.json, so they work offline; the Artifact can also pull the newest data.json from GitHub
through the viewer's GitHub connector. Run after render.py (the daily workflow does).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from collections import Counter

from common import ROOT, load_items, load_yaml, today
from render import (CORE_TOPICS, LABS, PAPER_TOPICS, direction_hits, is_paper, lab_of, paper_rank, rank,
                    review_title, topic_heat)

SITE = ROOT / "site"
REPO = "demoleiwang/agent-frontier"
BRANCH = "claude/inspiring-lovelace-umqw6v"
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/"
SCHEMA = "agent-frontier/site@1"
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def md(s: str | None) -> str:
    """Inline markdown (links, bold, code) -> safe HTML; relative links point at the repo on GitHub."""
    if not s:
        return ""
    out, pos = [], 0
    for m in MD_LINK.finditer(s):
        out.append(_inline(s[pos:m.start()]))
        url = m.group(2)
        if not url.startswith(("http://", "https://", "#")):
            url = BLOB + url.lstrip("./")
        out.append(f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{_inline(m.group(1))}</a>')
        pos = m.end()
    out.append(_inline(s[pos:]))
    return "".join(out)


def _inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", t)


def item_view(it: dict) -> dict:
    return {
        "id": it["id"], "title": it["title"], "url": it["url"], "date": it["date"],
        "source": it.get("source"), "lab": dict(LABS).get(lab_of(it) or "", ""),
        "topics": [t for t in it.get("topics", []) if t in CORE_TOPICS],
        "rep": round(it.get("rep", 0), 2) if is_paper(it) else None,
        "inst": (it.get("institution") or "")[:60], "upvotes": it.get("upvotes"),
        "tldr": it.get("tldr") or "", "status": it.get("status", "new"),
        "paper": is_paper(it),
    }


def weekly_counts(d: dict, items: list, weeks: int = 12) -> list[int]:
    """Hits per ISO week for the last `weeks` weeks (oldest first), same matcher as the README radar."""
    start = today() - dt.timedelta(days=7 * weeks)
    hits = direction_hits(d, items, start.isoformat())
    c = Counter((today() - dt.date.fromisoformat(i["date"])).days // 7 for i in hits)
    return [c.get(w, 0) for w in range(weeks - 1, -1, -1)]


def build() -> dict:
    compass = load_yaml("compass.yaml") or {}
    items = list(load_items().values())
    days = 14
    cutoff = (today() - dt.timedelta(days=days)).isoformat()
    week = (today() - dt.timedelta(days=7)).isoformat()

    directions = []
    for d in compass.get("directions") or []:
        hits = direction_hits(d, items, cutoff)
        directions.append({
            "name": d["name"], "status": d.get("status", ""), "why": md(d.get("why")), "next": md(d.get("next")),
            "evidence": [{"title": e["title"], "url": e["url"]} for e in d.get("evidence", [])],
            "hits14": len(hits), "weekly": weekly_counts(d, items),
            "recent": [item_view(i) for i in hits[:4]],
        })

    new_papers = sorted((i for i in items if is_paper(i) and i["date"] >= week and i.get("status") == "new"
                         and CORE_TOPICS & set(i.get("topics", [])) and i.get("rep", 0) >= 0.3),
                        key=paper_rank, reverse=True)[:16]
    read_papers = sorted((i for i in items if is_paper(i) and i.get("status") in ("skimmed", "read", "noted")
                          and i.get("tldr_source") == "manual"), key=lambda i: i["date"], reverse=True)[:30]
    lab_posts = rank([i for i in items if not is_paper(i) and i["date"] >= cutoff])[:24]

    heat = []
    for t in PAPER_TOPICS:
        cur, cs, prev, ps, arrow = topic_heat(items, t, days)
        heat.append({"topic": t, "cur": cur, "cur_share": round(cs, 4), "prev": prev, "prev_share": round(ps, 4),
                     "trend": arrow, "page": BLOB + f"topics/{t}.md" if (ROOT / "topics" / f"{t}.md").exists() else None})

    reports = [{"title": review_title(r), "url": BLOB + f"reviews/{r.name}", "date": r.name[:10]}
               for r in sorted((ROOT / "reviews").glob("*.md"), reverse=True)]

    def pin(p):
        if p.get("id"):
            it = next((i for i in items if i["id"] == p["id"]), None)
            if it:
                return {"title": it["title"], "url": it["url"], "why": p.get("why", ""), "status": it.get("status")}
            return None
        return {"title": p["title"], "url": p["url"], "why": p.get("why", ""), "status": None}

    papers = [i for i in items if is_paper(i)]
    return {
        "schema": SCHEMA,
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "data_date": today().isoformat(),
        "compass_updated": str(compass.get("updated", "")),
        "repo": {"name": REPO, "branch": BRANCH, "blob": BLOB},
        "stats": {"items": len(items), "papers": len(papers), "posts": len(items) - len(papers),
                  "papers_14d": sum(1 for i in papers if i["date"] >= cutoff),
                  "posts_14d": sum(1 for i in items if not is_paper(i) and i["date"] >= cutoff),
                  "skimmed": sum(1 for i in items if i.get("status") in ("skimmed", "read", "noted"))},
        "scope": md(compass.get("scope")),
        "thesis": md(compass.get("thesis")),
        "main_direction": md(compass.get("main_direction")),
        "why_this": [{"head": md(w.get("head")), "body": md(w.get("body"))} for w in compass.get("why_this") or []],
        "phases": [{"name": p["name"], "weeks": p["weeks"], "modules": p.get("modules", []), "goal": md(p.get("goal"))}
                   for p in compass.get("phases") or []],
        "modules": [{"id": m["id"], "name": m["name"], "status": m.get("status", ""), "what": md(m.get("what")),
                     "next": md(m.get("next")), "url": m.get("url")} for m in compass.get("modules") or []],
        "watch": [{"signal": md(w["signal"]), "action": md(w["action"])} for w in compass.get("watch") or []],
        "direction_log": [{"version": d["version"], "date": d["date"], "direction": md(d["direction"]), "why": md(d["why"])}
                          for d in compass.get("direction_log") or []],
        "directions": directions,
        "signals": [{"signal": s["signal"], "detail": md(s["detail"]),
                     "refs": s.get("refs") or ([{"title": "来源", "url": s["ref"]}] if s.get("ref") else [])}
                    for s in compass.get("signals") or []],
        "must_read": [p for p in (pin(p) for p in compass.get("must_read") or []) if p],
        "new_papers": [item_view(i) for i in new_papers],
        "read_papers": [item_view(i) for i in read_papers],
        "lab_posts": [item_view(i) for i in lab_posts],
        "heat": heat,
        "reports": reports,
    }


def main() -> None:
    data = build()
    SITE.mkdir(exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (SITE / "data.json").write_text(payload, encoding="utf-8")
    body = (SITE / "template.html").read_text(encoding="utf-8")
    # keep the embedded snapshot inert inside <script type="application/json">
    body = body.replace("__SNAPSHOT__", payload.replace("</", "<\\/"))
    (SITE / "artifact.html").write_text(body, encoding="utf-8")
    title = re.search(r"<title>.*?</title>", body, re.S)
    head = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n')
    (SITE / "index.html").write_text(head + (title.group(0) if title else "") + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n",
                                     encoding="utf-8")
    print(f"site: {len(payload) // 1024} KB data, {len(data['directions'])} directions, {len(data['new_papers'])} new papers")


if __name__ == "__main__":
    main()
