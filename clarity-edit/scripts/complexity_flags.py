#!/usr/bin/env python3
"""Flag over-complex sentences in a chapter — the deterministic half of clarity-edit.

Lists the sentences most likely to need simplifying: very long ones, and heavily
subordinated ones (many clauses, commas, semicolons, relative pronouns). It does NOT
judge sense, vocabulary, or metaphor — that is the skill's LLM pass. This just gives
that pass objective candidates to look at first. Read-only; advisory (exits 0).

Usage:
    python complexity_flags.py <chapter.md | book-folder>

Standard library only.
"""

import argparse
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

LONG_WORDS = 45          # a sentence this long is a split candidate
COMPLEX_SCORE = 6        # subordination score at/above which a sentence is flagged

SUBORDINATORS = r"\b(?:which|that|who|whom|whose|although|though|because|since|while|" \
                r"whereas|unless|until|before|after|when|where|if|as|so that|in order to|" \
                r"despite|however|moreover|therefore|thereby|wherein)\b"


def strip_title(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def sentences(text):
    # keep dialogue intact-ish; split on sentence-final punctuation + space
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def score(sent):
    low = sent.lower()
    words = len(re.findall(r"[A-Za-z']+", sent))
    commas = sent.count(",")
    semis = sent.count(";")
    subs = len(re.findall(SUBORDINATORS, low))
    s = commas + 2 * semis + subs
    reasons = []
    if words >= LONG_WORDS:
        reasons.append(f"long ({words}w)")
    if s >= COMPLEX_SCORE:
        reasons.append(f"heavily subordinated (commas {commas}, semicolons {semis}, "
                       f"clause words {subs})")
    return words, s, reasons


def scan_file(path):
    body = strip_title(open(path, encoding="utf-8").read())
    flagged = []
    for i, sent in enumerate(sentences(body), 1):
        words, s, reasons = score(sent)
        if reasons:
            flagged.append((words + s, i, reasons, sent))
    return flagged


def chapter_files(target):
    if os.path.isfile(target):
        return [target]
    ch = os.path.join(target, "chapters")
    base = ch if os.path.isdir(ch) else target
    return [os.path.join(base, f) for f in sorted(os.listdir(base)) if f.endswith(".md")]


def main():
    ap = argparse.ArgumentParser(description="Flag over-complex sentences (split candidates).")
    ap.add_argument("target", help="a chapter .md file or a book folder")
    ap.add_argument("--top", type=int, default=12, help="max sentences to list per chapter")
    args = ap.parse_args()

    files = chapter_files(os.path.abspath(args.target))
    if not files:
        print("No chapter files found.")
        return 0

    print("COMPLEXITY FLAGS  (split/simplify candidates — clarity-edit)")
    print("=" * 64)
    for path in files:
        flagged = scan_file(path)
        name = os.path.basename(path)
        print(f"\n  {name}: {len(flagged)} sentence(s) flagged")
        for _, idx, reasons, sent in sorted(flagged, reverse=True)[:args.top]:
            snippet = (sent[:96] + "…") if len(sent) > 96 else sent
            print(f"    [s{idx}] {', '.join(reasons)}")
            print(f"          {snippet}")
    print("\n" + "=" * 64)
    print("  Candidates only. The clarity-edit pass judges which to simplify, and also")
    print("  checks sense, vocabulary, and metaphor — which a script cannot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
