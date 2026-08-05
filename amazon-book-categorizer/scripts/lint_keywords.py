#!/usr/bin/env python3
"""Validate KDP keywords against Amazon's mechanical rules.

Checks the seven keyword slots a book lists for Amazon KDP: field length
(<= 50 characters), slot count (<= 7), banned terms (subjective claims,
promotional words), and echoes of the book's own title or author. It is a
safety net for the amazon-book-categorizer skill, which an LLM can miscount.

Reads keywords from a book project's amazon-categories.md by default, or from
--kw flags. Exits non-zero if any hard rule is broken, so it can gate a build.

Usage:
    python lint_keywords.py [path]            # path = book folder or .md file (default .)
    python lint_keywords.py --kw "a" --kw "b" # check keywords passed directly
    python lint_keywords.py ./my-book --book-json ./my-book/book.json

Standard library only.
"""

import argparse
import json
import os
import re
import sys

# Force UTF-8 so the report doesn't crash on Windows cp1252 consoles.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

MAX_LEN = 50
MAX_SLOTS = 7

# Word-boundary patterns for terms KDP disallows or discourages in keywords.
BANNED = [
    r"best[\s-]?seller(?:s|ing)?", r"\bbest\b", r"award[\s-]?winning",
    r"#\s?1", r"\bnumber\s?one\b", r"\btop\b",
    r"\bfree\b", r"\bon sale\b", r"\bsale\b", r"\bdiscount\b", r"\bcheap\b",
    r"\bnew\b", r"\bavailable now\b", r"\bnewest\b",
]


def parse_md_keywords(text):
    """Pull keywords from the '## Keywords' section of amazon-categories.md.

    Expects numbered entries, ideally backtick-wrapped:
        1. `keyword phrase`  - optional note
    Falls back to the text after the number when no backticks are present.
    """
    lines = text.splitlines()
    out, in_section = [], False
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            in_section = bool(re.match(r"^#{1,6}\s*keywords\b", line, re.I))
            continue
        if not in_section:
            continue
        m = re.match(r"^\s*\d+[.)]\s*(.+)$", line)
        if not m:
            continue
        body = m.group(1).strip()
        tick = re.search(r"`([^`]+)`", body)
        if tick:
            out.append(tick.group(1).strip())
        else:
            # strip a trailing " - note" / " — note" annotation
            out.append(re.split(r"\s+[-–—]\s+", body)[0].strip())
    return out


def load_book_meta(path):
    if path and os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("title", ""), data.get("author", "")
        except (OSError, ValueError):
            pass
    return "", ""


def significant_words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 3}


def main():
    ap = argparse.ArgumentParser(description="Lint KDP keywords.")
    ap.add_argument("path", nargs="?", default=".",
                    help="book folder or amazon-categories.md (default: .)")
    ap.add_argument("--kw", action="append", default=[],
                    help="a keyword to check (repeatable); overrides the file")
    ap.add_argument("--book-json", default=None,
                    help="path to book.json for title/author echo checks")
    args = ap.parse_args()

    keywords, source = list(args.kw), "--kw flags"
    book_json = args.book_json

    if not keywords:
        md_path = args.path
        if os.path.isdir(md_path):
            book_json = book_json or os.path.join(md_path, "book.json")
            md_path = os.path.join(md_path, "amazon-categories.md")
        if not os.path.isfile(md_path):
            print(f"error: no keywords given and no file at {md_path}")
            return 2
        with open(md_path, encoding="utf-8") as f:
            keywords = parse_md_keywords(f.read())
        source = md_path
        if not keywords:
            print(f"error: found no '## Keywords' entries in {md_path}")
            return 2

    title, author = load_book_meta(book_json)
    errors, warnings = [], []

    # Slot count.
    if len(keywords) > MAX_SLOTS:
        errors.append(f"{len(keywords)} keywords given; KDP allows at most {MAX_SLOTS}.")
    elif len(keywords) < MAX_SLOTS:
        warnings.append(f"only {len(keywords)} of {MAX_SLOTS} slots used; unused slots are wasted reach.")

    seen = {}
    for i, kw in enumerate(keywords, 1):
        n = len(kw)
        flag = "OK " if n <= MAX_LEN else "LEN"
        print(f"  {flag} [{n:>2}/50] {i}. {kw}")
        if n > MAX_LEN:
            errors.append(f"#{i} is {n} chars (max {MAX_LEN}): {kw!r}")
        for pat in BANNED:
            if re.search(pat, kw, re.I):
                errors.append(f"#{i} contains a banned term ({pat}): {kw!r}")
        key = kw.strip().lower()
        if key in seen:
            errors.append(f"#{i} duplicates #{seen[key]}: {kw!r}")
        else:
            seen[key] = i
        if author and author.strip() and author.lower() in key:
            errors.append(f"#{i} echoes the author name: {kw!r}")
        if title and significant_words(title) and significant_words(title) <= significant_words(kw):
            warnings.append(f"#{i} repeats the whole title (already indexed): {kw!r}")

    print()
    for w in warnings:
        print(f"  warning: {w}")
    for e in errors:
        print(f"  ERROR:   {e}")

    print()
    print(f"source: {source}")
    if errors:
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"PASS — 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
