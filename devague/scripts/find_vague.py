#!/usr/bin/env python3
"""Find vague placeholder words for the devague skill.

Locates every occurrence of the three vague placeholder families the skill targets:
  - something
  - thing / things
  - shape / shapes / shaped (and "X-shaped" compounds)

It reports each occurrence with its sentence so devague can judge it. The script only
LOCATES candidates with a light idiom/dialogue heuristic; it cannot decide whether a
given instance should be replaced or kept (that needs meaning, per prose-style 2.4).

Whole-word matching: "\\bthings?\\b" does NOT match inside "something", "anything",
"nothing", or "everything"; "shape[sd]?" does NOT match "shapeless" or "landscape".

Usage:
    python find_vague.py <chapter.md | book-folder> [--show N]

Read-only. Stdlib only. Exits 0.
"""

import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# word families -> compiled pattern
FAMILIES = [
    ("something", re.compile(r"\bsomething\b", re.I)),
    ("thing/things", re.compile(r"\bthings?\b", re.I)),
    ("shape(s)", re.compile(r"\b(?:[\w]+-)?shape[sd]?\b", re.I)),
]

# light advisory heuristics — likely KEEP per prose-style 2.4 (idioms / set phrases)
IDIOM = re.compile(
    r"\b(?:the right thing|for one thing|first thing|sure thing|poor thing|"
    r"the whole thing|that (?:kind|sort) of thing|the only thing|a thing or two|"
    r"one thing|do(?:ing|es)? the right thing|something like|or something|"
    r"something(?:'s| is) wrong|something else|in (?:good|bad|better|worse|no) shape|"
    r"out of shape|bent out of shape|takes? shape|took shape|in the shape of)\b",
    re.I,
)


def split_sentences(text):
    """Rough sentence split for prose; skips markdown heading lines."""
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
    body = re.sub(r"\s+", " ", body).strip()
    # split after . ! ? (optionally followed by a closing quote)
    parts = re.split(r'(?<=[.!?])["”’]?\s+', body)
    return [p.strip() for p in parts if p.strip()]


def scan_file(path):
    text = open(path, encoding="utf-8").read()
    sentences = split_sentences(text)
    counts = {fam: 0 for fam, _ in FAMILIES}
    hits = []  # (sent_index, family, matched_word, sentence, flags)
    for i, sent in enumerate(sentences, 1):
        for fam, pat in FAMILIES:
            found = pat.findall(sent)
            if not found:
                continue
            counts[fam] += len(found)
            n = len(found)
            flags = []
            if IDIOM.search(sent):
                flags.append("likely idiom — verify")
            if '"' in sent or "“" in sent:
                flags.append("quote present — check if dialogue")
            word = pat.search(sent).group(0)
            hits.append((i, fam, word, sent, n, flags))
    return counts, hits, len(sentences)


def collect(target):
    if os.path.isdir(target):
        ch = os.path.join(target, "chapters")
        base = ch if os.path.isdir(ch) else target
        files = sorted(
            os.path.join(base, f) for f in os.listdir(base)
            if f.endswith(".md") and not f.startswith(".")
        )
    else:
        files = [target]
    return files


def trim(sent, limit=120):
    return sent if len(sent) <= limit else sent[:limit].rstrip() + " ..."


def main():
    ap = argparse.ArgumentParser(description="Find vague placeholder words (devague).")
    ap.add_argument("target", help="a chapter .md file or a book folder")
    ap.add_argument("--show", type=int, default=0,
                    help="cap displayed candidates per file (0 = all)")
    args = ap.parse_args()

    files = collect(args.target)
    if not files:
        print(f"no .md files found at {args.target}", file=sys.stderr)
        return 0

    print("DE-VAGUE CANDIDATES  (vague placeholder words — devague)")
    print("=" * 60)
    grand = {fam: 0 for fam, _ in FAMILIES}
    grand_total = 0
    for path in files:
        counts, hits, nsent = scan_file(path)
        total = sum(counts.values())
        grand_total += total
        for fam in grand:
            grand[fam] += counts[fam]
        rel = os.path.relpath(path)
        if total == 0:
            print(f"\n  {rel}: clean (0 candidates)")
            continue
        summary = " | ".join(f"{fam}: {counts[fam]}" for fam, _ in FAMILIES if counts[fam])
        print(f"\n  {rel}: {total} candidate(s)   [{summary}]")
        shown = hits if args.show == 0 else hits[: args.show]
        for i, fam, word, sent, n, flags in shown:
            tag = f"  ({n} in sentence)" if n > 1 else ""
            note = ("   [" + "; ".join(flags) + "]") if flags else ""
            print(f'    [s{i}] {word:<10} "{trim(sent)}"{tag}{note}')
        if args.show and len(hits) > args.show:
            print(f"    ... and {len(hits) - args.show} more")

    print("\n" + "=" * 60)
    gsum = " | ".join(f"{fam}: {grand[fam]}" for fam, _ in FAMILIES)
    print(f"  TOTAL candidates: {grand_total}   [{gsum}]")
    print("  Candidates only. devague decides each in context: replace with a precise")
    print("  word, or KEEP (idiom / deliberate mystery / dialogue) per prose-style 2.4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
