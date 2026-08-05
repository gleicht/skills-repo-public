#!/usr/bin/env python3
"""Pre-publish preflight: reconcile a finished book and confirm it is ready.

A read-only sanity check meant to run AFTER the editing and review gates and BEFORE
the publishing workflow (front-matter, packaging, publishing prep). It does the
mechanical reconciliation a human would do on a final walk-through:

  - every outline chapter has a real, non-empty file, in order, no orphans/gaps
  - no leftover placeholder / TODO / TK markers in the prose
  - the metadata is complete (title and author filled — no unsigned book)
  - the front-matter manifest, if present, resolves to real files
  - the prior QA gates closed out (review-panel READY, fidelity-review PASS/no open)

It prints a checklist and a GO / HOLD verdict and exits non-zero on any FAIL. It never
edits anything; remediation is handed back to the right skill (see SKILL.md). The
cross-file judgment checks (cast in prose vs dossier, fair-play clues, series threads)
are the SKILL.md's job — this script covers what can be checked deterministically.

Usage:
    python preflight.py [book-folder]      # default: current directory

Standard library only.
"""

import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

MIN_CHAPTER_WORDS = 40   # below this a chapter reads as a stub, not finished prose

# Hard placeholder tokens (uppercase, word-bounded) — leftover author markers.
RX_HARD = re.compile(r"\b(?:TODO|FIXME|TBD|XXX|TK)\b")
# Softer signals — bracketed editorial notes and filler text.
RX_SOFT = re.compile(r"lorem ipsum|\[(?:TK|TODO|INSERT|PLACEHOLDER|NOTE)[^\]]{0,40}\]"
                     r"|\bplaceholder\b", re.I)

results = []  # (level, name, detail) ; level in {"PASS","WARN","FAIL"}


def add(level, name, detail=""):
    results.append((level, name, detail))


def strip_title(text):
    """Drop a leading '# Title' line; return the remaining body."""
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def chapter_prefix(name):
    m = re.match(r"^(\d+)", name)
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description="Pre-publish preflight reconciliation.")
    ap.add_argument("folder", nargs="?", default=".", help="book project folder")
    args = ap.parse_args()
    folder = os.path.abspath(args.folder)

    # ---- book.json metadata ----
    book = {}
    bj = os.path.join(folder, "book.json")
    if os.path.isfile(bj):
        try:
            book = json.loads(open(bj, encoding="utf-8").read())
        except ValueError:
            add("FAIL", "book.json", "present but is not valid JSON")
    else:
        add("WARN", "book.json", "missing — no spec to reconcile against")
    if book:
        if (book.get("title") or "").strip():
            add("PASS", "title", book["title"])
        else:
            add("FAIL", "title", "book.json has no title")
        if (book.get("author") or "").strip():
            add("PASS", "author", book["author"])
        else:
            add("FAIL", "author", "book.json author is blank — the book would publish unsigned")

    # ---- chapters present ----
    ch_dir = os.path.join(folder, "chapters")
    files = sorted(f for f in os.listdir(ch_dir)) if os.path.isdir(ch_dir) else []
    files = [f for f in files if f.endswith(".md")]
    if not files:
        add("FAIL", "chapters", "no chapters/*.md found — nothing to publish")
        return finish()
    add("PASS", "chapters present", f"{len(files)} file(s)")

    # ---- numbering: duplicates / gaps ----
    prefixes = [chapter_prefix(f) for f in files]
    nums = [p for p in prefixes if p is not None]
    dups = sorted({n for n in nums if nums.count(n) > 1})
    if dups:
        add("FAIL", "chapter numbering", f"duplicate number prefix(es): {dups}")
    if nums:
        missing = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
        if missing:
            add("WARN", "chapter numbering", f"gap(s) in sequence: {missing}")
    if not dups and not (nums and [n for n in range(min(nums), max(nums) + 1) if n not in nums]):
        add("PASS", "chapter numbering", "sequential, no duplicates")

    # ---- empty / stub chapters + placeholder scan ----
    bodies = {}
    empty, stub = [], []
    hard_hits, soft_hits = [], []
    for f in files:
        raw = open(os.path.join(ch_dir, f), encoding="utf-8").read()
        body = strip_title(raw)
        bodies[f] = body
        wc = len(body.split())
        if wc == 0:
            empty.append(f)
        elif wc < MIN_CHAPTER_WORDS:
            stub.append(f"{f} ({wc}w)")
        for i, line in enumerate(raw.replace("\r\n", "\n").split("\n"), 1):
            for m in RX_HARD.finditer(line):
                hard_hits.append(f"{f}:{i}  {m.group(0)}  — {line.strip()[:60]}")
            for m in RX_SOFT.finditer(line):
                soft_hits.append(f"{f}:{i}  {line.strip()[:60]}")
    add("FAIL" if empty else "PASS", "no empty chapters",
        ("empty: " + ", ".join(empty)) if empty else "all chapters have prose")
    if stub:
        add("WARN", "very short chapters", "; ".join(stub))
    if hard_hits:
        add("FAIL", "placeholder markers",
            f"{len(hard_hits)} found:\n      " + "\n      ".join(hard_hits[:12]))
    else:
        add("PASS", "placeholder markers", "none (TODO/FIXME/TBD/XXX/TK)")
    if soft_hits:
        add("WARN", "editorial notes / filler",
            f"{len(soft_hits)} found:\n      " + "\n      ".join(soft_hits[:8]))

    # ---- outline <-> chapters reconciliation ----
    op = os.path.join(folder, "outline.json")
    if os.path.isfile(op):
        try:
            outline = json.loads(open(op, encoding="utf-8").read())
        except ValueError:
            outline = None
            add("FAIL", "outline.json", "present but is not valid JSON")
        if outline:
            entries = outline.get("chapters", [])
            matched = set()
            missing_files = []
            for e in entries:
                cid = str(e.get("id", "")).strip()
                hit = next((f for f in files if f == cid or f.startswith(cid + "-")), None)
                if hit:
                    matched.add(hit)
                else:
                    missing_files.append(f"{cid} ('{e.get('title','')}')")
            orphans = [f for f in files if f not in matched]
            if missing_files:
                add("FAIL", "outline reconciliation",
                    "outline chapter(s) with no file: " + "; ".join(missing_files))
            if orphans:
                add("WARN", "outline reconciliation",
                    "chapter file(s) not in outline: " + ", ".join(orphans))
            if not missing_files and not orphans:
                add("PASS", "outline reconciliation",
                    f"{len(entries)} outline chapters all map to files")
    else:
        add("WARN", "outline.json", "missing — chapter order/coverage not reconciled")

    # ---- front-matter manifest ----
    fm = os.path.join(folder, "front-matter", "front-matter.json")
    if os.path.isfile(fm):
        try:
            data = json.loads(open(fm, encoding="utf-8").read())
            miss = []
            for key in ("front", "back"):
                for entry in data.get(key, []) or []:
                    fn = entry.get("file")
                    if not fn or not os.path.isfile(os.path.join(folder, "front-matter", fn)):
                        miss.append(str(fn))
            if miss:
                add("FAIL", "front-matter manifest", "missing file(s): " + ", ".join(miss))
            else:
                add("PASS", "front-matter manifest", "all referenced pieces exist")
        except ValueError:
            add("FAIL", "front-matter manifest", "front-matter.json is not valid JSON")

    # ---- prior QA gates closed out ----
    rr = os.path.join(folder, "review-report.md")
    if os.path.isfile(rr):
        txt = open(rr, encoding="utf-8").read()
        if re.search(r"NOT[\s-]*READY", txt, re.I):
            add("FAIL", "review-panel gate", "review-report.md verdict is NOT READY")
        else:
            add("PASS", "review-panel gate", "review-report.md present, no NOT-READY verdict")
    else:
        add("WARN", "review-panel gate", "no review-report.md — panel may not have run")

    fr = os.path.join(folder, "fidelity-report.md")
    if os.path.isfile(fr):
        txt = open(fr, encoding="utf-8").read()
        open_rows = len(re.findall(r"\|\s*Open\s*\|", txt))
        if re.search(r"ISSUES FOUND|HALTED", txt) or open_rows:
            add("FAIL", "fidelity-review gate",
                f"fidelity-report.md has unresolved items ({open_rows} 'Open' row(s))")
        else:
            add("PASS", "fidelity-review gate", "fidelity-report.md present, no open items")
    else:
        add("WARN", "fidelity-review gate", "no fidelity-report.md — verify it was run")

    return finish()


def finish():
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    fails = sum(1 for r in results if r[0] == "FAIL")
    warns = sum(1 for r in results if r[0] == "WARN")
    passes = sum(1 for r in results if r[0] == "PASS")
    print("PREFLIGHT CHECK")
    print("=" * 60)
    for level, name, detail in sorted(results, key=lambda r: order[r[0]]):
        line = f"[{level}] {name}"
        if detail:
            line += f": {detail}"
        print("  " + line)
    print("=" * 60)
    print(f"  {passes} pass · {warns} warn · {fails} fail")
    if fails:
        print(f"VERDICT: HOLD — {fails} blocking item(s) to address before publishing.")
        return 1
    if warns:
        print("VERDICT: GO (with warnings) — review the warnings, then publish.")
        return 0
    print("VERDICT: GO — the book reconciles; clear for the publishing workflow.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
