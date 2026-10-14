"""Check that every claim in hand-written markdown carries a source URL.

A "claim block" is a list item, a table body row, or a prose paragraph. It passes if it contains an http(s) link.
Per-paper / per-post appendix notes (files under a reviews/<name>/ folder) may instead inherit the URL given at the
top of their card (the nearest ### or #### heading section that lists a URL before its first bullet).
Synthesis files (reviews/*.md, topics/*.md) must cite inline.

Blocks explicitly marked 「无出处，待核」 are reported separately as acknowledged gaps.

Usage: python scripts/check_evidence.py [paths...] [--verbose]
Exit code 1 if any unsourced claim is found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = re.compile(r"https?://")
GAP = "无出处，待核"
MIN_CHARS = 12  # shorter blocks are labels, not claims

# Sections that describe our own method / navigation rather than making claims about the world.
META_HEADINGS = re.compile(r"怎么做的|怎么筛|来源说明|How this|Method and source|方法与来源|阅读顺序|Coverage list|维护|目录|附录|Appendix|"
                           r"筛选说明|可信度|Scope|范围|缺口|Gaps|待跟进|下一步|For each|Screening|筛查|对研究的启示|研究的启示|可做的问题|"
                           r"热度|报告与入口|本周待分拣|一步一步的顺序|路线图")  # README: computed stats / navigation, not claims


def default_paths() -> list[Path]:
    out = sorted((ROOT / "reviews").rglob("*.md")) + sorted((ROOT / "topics").glob("*.md"))
    out += [p for p in sorted((ROOT / "notes").glob("*.md")) if not p.name.startswith("_")]
    return out + [ROOT / "README.md"]  # rendered from config/compass.yaml: fix claims there


def blocks(lines: list[str]):
    """Yield (line_no, kind, text, heading_stack) for claim-bearing blocks."""
    in_code = False
    heading: list[tuple[int, str, int]] = []  # (level, text, line_no)
    para: list[str] = []
    para_start = 0

    def flush():
        nonlocal para
        if para:
            yield_items.append((para_start, "para", " ".join(para), list(heading)))
            para = []

    yield_items: list = []
    for n, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            flush()
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", s)
        if m:
            flush()
            lvl = len(m.group(1))
            heading = [h for h in heading if h[0] < lvl] + [(lvl, m.group(2), n)]
            continue
        if not s or s == "---" or s.startswith("<!--") or s.startswith("<details") or s.startswith("</details"):
            flush()
            continue
        if s.startswith("|"):
            flush()
            if re.match(r"^\|[\s:|-]+\|$", s):
                continue
            yield_items.append((n, "row", s, list(heading)))
            continue
        if re.match(r"^([-*+]|\d+\.)\s+", s):
            flush()
            yield_items.append((n, "item", s, list(heading)))
            continue
        if raw.startswith(("  ", "\t")) and yield_items and yield_items[-1][1] == "item" and not para:
            # continuation of the previous list item
            ln, k, t, h = yield_items[-1]
            yield_items[-1] = (ln, k, t + " " + s, h)
            continue
        if not para:
            para_start = n
        para.append(s)
    flush()
    return yield_items


def card_has_url(lines: list[str], heading_line: int) -> bool:
    """True if the card under a heading states a URL before its first substantive bullet ends (first ~6 lines)."""
    for raw in lines[heading_line: heading_line + 8]:
        if raw.startswith("#"):
            break
        if URL.search(raw):
            return True
    return False


PLAN_LABEL = re.compile(r"^(\d+\.\s*|[-*+]\s*)?(\*\*)?(做什么|完成标准|第一步|统计|来源深度图例|阅读说明)")


def under_plan_label(lines: list[str], n: int) -> bool:
    """Proposal content ("what we will do", "done when", "first step") states our plan, not a claim about the world.
    A list item is exempt when it, or an item it is nested under, starts with such a label."""
    cur = len(lines[n - 1]) - len(lines[n - 1].lstrip())
    if PLAN_LABEL.match(lines[n - 1].strip()):
        return True
    for raw in reversed(lines[: n - 1]):
        if not raw.strip():
            return False
        ind = len(raw) - len(raw.lstrip())
        if ind < cur and re.match(r"^\s*([-*+]|\d+\.)\s+", raw):
            if PLAN_LABEL.match(raw.strip()):
                return True
            cur = ind
            if ind == 0:
                return False
    return False


def is_label(plain: str) -> bool:
    """Short headings-in-prose such as '架构共识：在 LLM 边界捕获' or '**Benchmark 现状**' carry no claim of their own."""
    return (len(plain) <= 25 and not re.search(r"[。；]", plain)) or (len(plain) <= 40 and not re.search(r"[0-9。；]", plain))


def children_sourced(lines: list[str], n: int) -> bool:
    """A lead-in item/paragraph passes if every indented child list item below it cites a URL."""
    base = len(lines[n - 1]) - len(lines[n - 1].lstrip())
    kids = []
    for raw in lines[n:]:
        if not raw.strip():
            if kids:
                break
            continue
        ind = len(raw) - len(raw.lstrip())
        if re.match(r"^\s*([-*+]|\d+\.)\s+", raw) and ind > base:
            kids.append(raw)
        elif ind > base and kids:
            kids[-1] += raw  # continuation line
        else:
            break
    return bool(kids) and all(URL.search(k) for k in kids)


def table_header_sourced(lines: list[str], n: int) -> bool:
    """Body rows of a comparison table inherit evidence when the header row links every compared source."""
    i = n - 1
    while i > 0 and lines[i - 1].strip().startswith("|"):
        i -= 1
    return bool(URL.search(lines[i]))


def check(path: Path, verbose: bool) -> tuple[int, int, int]:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    appendix = path.parent.name != "reviews" and path.parent.parent.name == "reviews"
    missing = gaps = total = 0
    header_rows_seen: set[int] = set()
    for n, kind, text, heads in blocks(lines):
        if kind == "row":
            # the first row of each table is its header
            prev = lines[n - 2].strip() if n >= 2 else ""
            if not prev.startswith("|"):
                header_rows_seen.add(n)
                continue
        plain = re.sub(r"[`*_>#|]", "", text).strip()
        if len(plain) < MIN_CHARS:
            continue
        if any(META_HEADINGS.search(h[1]) for h in heads):
            continue
        if is_label(plain):
            continue
        if PLAN_LABEL.match(text.strip()) or PLAN_LABEL.match(plain) or (kind == "item" and under_plan_label(lines, n)):  # our own plan / stats / legends
            continue
        if text.startswith(">") and n <= 12:  # file preamble
            continue
        if not heads or (path.name == "README.md" and all(h[0] == 1 for h in heads)):  # title block / README intro
            continue
        total += 1
        if URL.search(text):
            continue
        if GAP in text:
            gaps += 1
            continue
        if kind in ("item", "para") and children_sourced(lines, n):
            continue
        if kind == "row" and table_header_sourced(lines, n):
            continue
        # a card whose heading itself links the source (any file), or, in appendices, lists it right under the heading
        if any(h[0] >= 3 and URL.search(h[1]) for h in heads):
            continue
        if appendix and any(h[0] >= 2 and card_has_url(lines, h[2]) for h in heads):
            continue
        missing += 1
        if verbose:
            print(f"{path.relative_to(ROOT)}:{n}: {plain[:110]}")
    return total, missing, gaps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()
    paths = [Path(p).resolve() for p in args.paths] or default_paths()
    bad = 0
    for p in paths:
        total, missing, gaps = check(p, args.verbose)
        flag = "OK " if missing == 0 else "!! "
        print(f"{flag}{p.relative_to(ROOT)}: {total} claims, {missing} without URL, {gaps} marked 待核")
        bad += missing
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
