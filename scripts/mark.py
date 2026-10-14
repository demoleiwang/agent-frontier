"""Move an item through the reading queue: new -> skimmed -> read -> noted.

Usage: python scripts/mark.py <id-or-substring> <status> [--note "..."] [--tldr "..."]
"""
from __future__ import annotations

import argparse
import sys

from common import STATUSES, load_items, save_items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("status", choices=STATUSES)
    ap.add_argument("--note")
    ap.add_argument("--tldr", help="hand-written tldr; classify.py will no longer overwrite it")
    args = ap.parse_args()
    items = load_items()
    hits = [i for i in items.values() if i["id"] == args.query] or \
           [i for i in items.values() if args.query.lower() in (i["id"] + " " + i["title"]).lower()]
    if len(hits) != 1:
        print(f"{len(hits)} matches: " + ", ".join(i["id"] for i in hits[:10]), file=sys.stderr)
        sys.exit(1)
    hits[0]["status"] = args.status
    if args.note:
        hits[0]["note"] = args.note
    if args.tldr:
        hits[0]["tldr"] = args.tldr
        hits[0]["tldr_source"] = "manual"
    save_items(items)
    print(f"{hits[0]['id']} -> {args.status}")


if __name__ == "__main__":
    main()
