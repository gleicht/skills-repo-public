#!/usr/bin/env python3
"""Deterministic prose-style diagnostics for a manuscript.

A read-only style linter — the scripted companion to the prose-style and book-editor
skills. It measures the things a tired eye misses: crutch and filler words, perception
"filter" verbs, adverb density, sentence-length monotony, word echoes within a
paragraph, reading level per chapter, and hard counts of em dashes and stock AI-ism
phrases. It reports; it never edits. Fixing is book-editor's / the author's job.

Usage:
    python style_check.py [book-folder] [--grade N]

--grade sets the target Flesch-Kincaid grade (from the story bible's reading-level
goal) so chapters that drift above it are flagged. Standard library only; advisory
(always exits 0).
"""

import argparse
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

CRUTCH = ["just", "really", "very", "quite", "rather", "somewhat", "somehow",
          "suddenly", "actually", "basically", "literally", "simply", "even",
          "only", "perhaps", "maybe", "almost", "nearly", "began to", "started to",
          "sort of", "kind of", "a bit", "a little"]
FILTER = ["saw", "watched", "noticed", "realized", "realised", "felt", "heard",
          "knew", "wondered", "thought", "seemed", "looked", "decided", "remembered"]
# Stock phrases / AI-isms (a subset of the prose-style catalog) — literal, lowercased.
AI_ISMS = [
    "it's worth noting", "needless to say", "in conclusion", "a testament to",
    "navigate the complexities", "tapestry", "delve", "little did", "breath caught",
    "heart pounded", "heart hammered", "sent shivers", "barely above a whisper",
    "a mix of", "a mixture of", "couldn't help but", "let out a breath",
    "didn't know she was holding", "didn't know he was holding", "visibly",
    "a wave of", "washed over", "in that moment", "time seemed to",
]
COMMON_LONG = {"another", "because", "before", "between", "should", "through",
               "around", "though", "without", "nothing", "something", "anything",
               "himself", "herself", "always", "really", "little", "thought",
               "looked", "behind", "toward", "against", "almost", "people",
               "morning", "moment"}


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    n = len(groups)
    if word.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def count_phrases(text_lower, phrases):
    out = Counter()
    for p in phrases:
        pat = r"\b" + re.escape(p) + r"\b" if p.isalpha() or " " in p else re.escape(p)
        c = len(re.findall(pat, text_lower))
        if c:
            out[p] = c
    return out


def strip_title(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def analyze(body):
    low = body.lower()
    words = re.findall(r"[A-Za-z']+", body)
    wl = [w.lower() for w in words]
    sents = sentences(body)
    n_words = len(words) or 1
    n_sents = len(sents) or 1
    syl = sum(syllables(w) for w in words)
    fk = 0.39 * (n_words / n_sents) + 11.8 * (syl / n_words) - 15.59
    fre = 206.835 - 1.015 * (n_words / n_sents) - 84.6 * (syl / n_words)
    adverbs = [w for w in wl if w.endswith("ly") and len(w) > 4]
    lengths = [len(re.findall(r"[A-Za-z']+", s)) for s in sents]
    # echoes: distinctive word repeated within a paragraph
    echoes = Counter()
    for para in re.split(r"\n{2,}", body):
        pw = [w.lower() for w in re.findall(r"[A-Za-z']+", para)]
        c = Counter(w for w in pw if len(w) >= 6 and w not in COMMON_LONG)
        for w, k in c.items():
            if k >= 3:
                echoes[w] += k
    return {
        "words": n_words, "sents": n_sents,
        "fk": fk, "fre": fre,
        "avg_len": n_words / n_sents,
        "long_sents": sum(1 for L in lengths if L > 40),
        "adverbs": Counter(adverbs), "adverb_pct": 100 * len(adverbs) / n_words,
        "crutch": count_phrases(low, CRUTCH),
        "filter": count_phrases(low, FILTER),
        "aiisms": count_phrases(low, AI_ISMS),
        "emdash": low.count("—") + len(re.findall(r"\s-\s", body)),
        "echoes": echoes,
    }


def main():
    ap = argparse.ArgumentParser(description="Deterministic prose-style diagnostics.")
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--grade", type=float, default=None,
                    help="target Flesch-Kincaid grade; chapters above it are flagged")
    args = ap.parse_args()
    ch_dir = os.path.join(os.path.abspath(args.folder), "chapters")
    if not os.path.isdir(ch_dir):
        print(f"No chapters/ folder in {args.folder}")
        return 0
    files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".md"))
    if not files:
        print("No chapters to analyze.")
        return 0

    book = Counter()
    book_adv = Counter(); book_cr = Counter(); book_fi = Counter()
    book_ai = Counter(); book_echo = Counter()
    per_chapter = []
    total_words = total_adv = emdash = 0
    for f in files:
        body = strip_title(open(os.path.join(ch_dir, f), encoding="utf-8").read())
        a = analyze(body)
        per_chapter.append((f, a))
        total_words += a["words"]
        total_adv += sum(a["adverbs"].values())
        emdash += a["emdash"]
        book_adv += a["adverbs"]; book_cr += a["crutch"]; book_fi += a["filter"]
        book_ai += a["aiisms"]; book_echo += a["echoes"]

    print("STYLE CHECK")
    print("=" * 64)
    print(f"  {len(files)} chapter(s), {total_words:,} words\n")

    print("  Reading level & sentence length (per chapter)")
    print(f"    {'chapter':<32}{'FK grade':>9}{'avg sent':>10}{'long>40':>9}")
    for f, a in per_chapter:
        flag = "  <-- above target" if (args.grade is not None and a["fk"] > args.grade) else ""
        print(f"    {f[:30]:<32}{a['fk']:>9.1f}{a['avg_len']:>10.1f}{a['long_sents']:>9}{flag}")
    if args.grade is not None:
        print(f"    (target grade: {args.grade})")

    pct = 100 * total_adv / (total_words or 1)
    print(f"\n  Adverbs (-ly): {total_adv} ({pct:.1f}% of words)"
          + ("  <-- high, aim < 4%" if pct > 4 else ""))
    top = ", ".join(f"{w}×{n}" for w, n in book_adv.most_common(8))
    if top:
        print(f"    top: {top}")

    def section(title, counter, note=""):
        if not counter:
            return
        total = sum(counter.values())
        print(f"\n  {title}: {total} total{note}")
        print("    " + ", ".join(f"{w}×{n}" for w, n in counter.most_common(12)))

    section("Crutch / filler words", book_cr, " (trim the ones that add nothing)")
    section("Filter words (distance the reader)", book_fi)
    section("Word echoes (repeated in a paragraph)", book_echo)
    section("AI-ism / stock phrases", book_ai, " (see prose-style)")
    print(f"\n  Em dashes: {emdash}" + ("  <-- prose-style replaces these" if emdash else ""))

    print("\n" + "=" * 64)
    print("  Advisory only. Hand fixes to book-editor / the author; nothing was changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
