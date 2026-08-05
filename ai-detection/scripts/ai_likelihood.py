#!/usr/bin/env python3
"""Heuristic 'reads-as-AI' scan for a manuscript.

A read-only diagnostic that scores how much the prose reads as machine-generated, from
the signals that correlate with AI writing: low sentence-length burstiness (AI is
uniform; humans vary), density of AI-ism phrases and signature words, sentence-initial
transition words, hedging, em dashes, and low lexical diversity. It reports a per-chapter
and overall risk band with the contributing factors, and never edits.

IMPORTANT — read the SKILL.md. This is a heuristic, NOT a real detector. It does not run,
replicate, or predict GPTZero / Originality.ai / Turnitin / Copyleaks or any commercial
tool, and a low score is not proof a text will "pass" one (those tools are themselves
unreliable and false-positive on human writing). Use it to find and remove AI tells so
the prose genuinely reads human; fixes go to prose-style / book-editor.

Usage:
    python ai_likelihood.py [book-folder]

Standard library only. Advisory: exits 0.
"""

import argparse
import os
import re
import sys
from collections import Counter
from statistics import mean, pstdev

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

AI_PHRASES = [
    "it's worth noting", "it is worth noting", "needless to say", "in conclusion",
    "a testament to", "navigate the complexities", "rich tapestry", "tapestry of",
    "when it comes to", "plays a crucial role", "plays a vital role", "in the realm of",
    "a wave of", "washed over", "in that moment", "little did", "breath caught",
    "heart pounded", "heart hammered", "sent shivers", "barely above a whisper",
    "couldn't help but", "a mix of", "a mixture of", "let out a breath",
    "stark reminder", "testament to the", "underscores the", "a beacon of",
]
SIGNATURE = ["delve", "leverage", "robust", "seamless", "nuanced", "tapestry",
             "landscape", "navigate", "foster", "synergy", "holistic", "intricate",
             "myriad", "realm", "underscore", "pivotal", "showcase", "elevate",
             "embark", "crucial", "vital", "vibrant", "bustling", "meticulous"]
TRANSITIONS = ["however", "moreover", "furthermore", "additionally", "consequently",
               "nevertheless", "nonetheless", "indeed", "ultimately", "overall",
               "in addition", "in conclusion", "that said", "importantly", "notably"]
HEDGES = ["perhaps", "arguably", "generally", "typically", "relatively", "essentially",
          "fundamentally", "somewhat", "often", "usually", "in general", "to some extent"]


def strip_title(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def count_terms(low, terms):
    n = 0
    for t in terms:
        n += len(re.findall(r"\b" + re.escape(t) + r"\b", low))
    return n


def count_initial(sents, terms):
    n = 0
    for s in sents:
        first = re.sub(r"^[^A-Za-z]+", "", s).lower()
        for t in terms:
            if first.startswith(t + " ") or first.startswith(t + ","):
                n += 1
                break
    return n


def score_chapter(body):
    low = body.lower()
    words = re.findall(r"[A-Za-z']+", body)
    n = len(words) or 1
    sents = sentences(body)
    lengths = [len(re.findall(r"[A-Za-z']+", s)) for s in sents] or [0]
    per1k = 1000.0 / n

    # burstiness: coefficient of variation of sentence length (humans vary more)
    cv = (pstdev(lengths) / mean(lengths)) if len(lengths) > 1 and mean(lengths) else 0.0
    # lexical diversity on first 600 words
    sample = [w.lower() for w in words[:600]]
    ttr = len(set(sample)) / len(sample) if sample else 1.0

    ai_ph = count_terms(low, AI_PHRASES)
    sig = count_terms(low, SIGNATURE)
    trans = count_initial(sents, TRANSITIONS)
    hedge = count_terms(low, HEDGES)
    emdash = low.count("—")

    pts = []
    if len(lengths) >= 5:
        if cv < 0.40:
            pts.append(("uniform sentence length (low burstiness)", 30))
        elif cv < 0.55:
            pts.append(("somewhat uniform sentence length", 15))
    p = round((ai_ph + sig) * per1k)
    if p:
        pts.append((f"AI-ism / signature words ({ai_ph + sig})", min(25, p * 4)))
    t = round(trans * per1k)
    if t:
        pts.append((f"sentence-initial transitions ({trans})", min(15, t * 4)))
    h = round(hedge * per1k)
    if h:
        pts.append((f"hedging words ({hedge})", min(10, h * 2)))
    e = round(emdash * per1k)
    if e:
        pts.append((f"em dashes ({emdash})", min(10, e * 2)))
    if ttr < 0.42 and len(sample) >= 200:
        pts.append(("low lexical diversity", 10))

    score = min(100, sum(p for _, p in pts))
    band = "reads as AI" if score >= 66 else "mixed" if score >= 33 else "reads as human"
    return {"score": score, "band": band, "cv": cv, "ttr": ttr, "words": n,
            "factors": sorted(pts, key=lambda x: -x[1])}


def main():
    ap = argparse.ArgumentParser(description="Heuristic reads-as-AI scan (not a real detector).")
    ap.add_argument("folder", nargs="?", default=".")
    args = ap.parse_args()
    ch_dir = os.path.join(os.path.abspath(args.folder), "chapters")
    if not os.path.isdir(ch_dir):
        print(f"No chapters/ folder in {args.folder}")
        return 0
    files = sorted(f for f in os.listdir(ch_dir) if f.endswith(".md"))
    if not files:
        print("No chapters to scan.")
        return 0

    print("AI-TELL SCAN  (heuristic — not a real detector; see SKILL.md)")
    print("=" * 64)
    rows = []
    agg = Counter()
    total_words = 0
    for f in files:
        body = strip_title(open(os.path.join(ch_dir, f), encoding="utf-8").read())
        r = score_chapter(body)
        rows.append((f, r))
        total_words += r["words"]
        for name, p in r["factors"]:
            key = re.sub(r"\s*\([^)]*\)", "", name)
            agg[key] += 1

    print(f"  {len(files)} chapter(s), {total_words:,} words\n")
    print(f"    {'chapter':<30}{'score':>6}{'burst':>7}{'TTR':>6}  band")
    worst = sorted(rows, key=lambda x: -x[1]["score"])
    for f, r in rows:
        print(f"    {f[:28]:<30}{r['score']:>6}{r['cv']:>7.2f}{r['ttr']:>6.2f}  {r['band']}")

    book = round(mean([r["score"] for _, r in rows]))
    band = "reads as AI" if book >= 66 else "mixed" if book >= 33 else "reads as human"
    print(f"\n  Book average: {book}/100 — {band}")

    flagged = [(f, r) for f, r in worst if r["score"] >= 33]
    if flagged:
        print("\n  Chapters to look at first (top factors):")
        for f, r in flagged[:6]:
            tops = "; ".join(name for name, _ in r["factors"][:3])
            print(f"    {f}  [{r['score']}] {tops}")

    print("\n" + "=" * 64)
    print("  Heuristic only. A low score is NOT proof a text passes any commercial")
    print("  detector. Fix flags by genuine humanizing via prose-style / book-editor,")
    print("  then re-scan. To check a real detector, run the text through one yourself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
