"""Shared helpers: paths, config loading, and the append-only jsonl item store."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
ITEMS = ROOT / "data" / "items"
DIGESTS = ROOT / "digests"

STATUSES = ["new", "skimmed", "read", "noted"]
# Fields a human may edit by hand; fetch/classify never overwrite them.
MANUAL_FIELDS = {"status", "note"}  # plus tldr when tldr_source == "manual"


def load_yaml(name: str):
    with open(CONFIG / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def today() -> dt.date:
    return dt.datetime.now(dt.timezone.utc).date()


def parse_date(s) -> dt.date | None:
    if isinstance(s, dt.date):
        return s
    s = str(s).strip()
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%b %d %Y", "%B, %Y", "%B %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def item_path(date: str) -> Path:
    y, m, _ = date.split("-")
    return ITEMS / y / m / f"{date}.jsonl"


def load_items() -> dict[str, dict]:
    """All items keyed by id. Later files win on duplicate ids."""
    items: dict[str, dict] = {}
    for p in sorted(ITEMS.rglob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                it = json.loads(line)
                items[it["id"]] = it
    return items


def save_items(items: dict[str, dict]) -> None:
    """Rewrite the store, one file per item date, items sorted by id for stable diffs."""
    by_date: dict[str, list[dict]] = {}
    for it in items.values():
        by_date.setdefault(it["date"], []).append(it)
    for p in ITEMS.rglob("*.jsonl"):
        if p.stem not in by_date:
            p.unlink()
    for date, rows in by_date.items():
        p = item_path(date)
        p.parent.mkdir(parents=True, exist_ok=True)
        rows.sort(key=lambda r: r["id"])
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def merge_item(items: dict[str, dict], new: dict) -> bool:
    """Insert or refresh an item, keeping manual fields. Returns True if it was new."""
    old = items.get(new["id"])
    if old is None:
        new.setdefault("status", "new")
        items[new["id"]] = new
        return True
    for k in MANUAL_FIELDS:
        if k in old:
            new[k] = old[k]
    if old.get("tldr_source") in ("manual", "llm"):
        new["tldr"], new["tldr_source"] = old["tldr"], old["tldr_source"]
    for k in ("topics", "score", "tldr", "tldr_source"):  # keep classification unless refetched text changed
        if k in old and k not in new and old.get("excerpt") == new.get("excerpt"):
            new[k] = old[k]
    items[new["id"]] = {**old, **new}
    return False
