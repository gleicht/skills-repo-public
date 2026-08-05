#!/usr/bin/env python3
"""propulsion_flags.py -- deterministic propulsion candidates for one chapter or a book folder.

The scripted half of the propulsion-editor skill. It surfaces the surface signals that
correlate with prose that stalls instead of pulls, so the editor knows where to look:

  - stalling / stative constructions  (was/were, there was, had been, began to, could feel,
    seemed to, past progressive) -- verbs that hold the prose still
  - additive sequencing               (and then, and so) -- "list" connectives instead of causal
  - sentence-initial filler           (However, Meanwhile, Suddenly, Then, Eventually, ...)
  - filter verbs                      (saw, heard, felt, noticed, realized, ...) -- distance the reader
  - the chapter's last sentence       (is it an unresolved hook, or a tidy summary?)

These are CANDIDATES, not verdicts: the script judges surface form, never whether a passage
actually pulls. The editor (and the author) make that call. Advisory only -- always exits 0.

Usage:
  python propulsion_flags.py <chapter.md>
  python propulsion_flags.py <book-folder>        # scans chapters/*.md, else *.md
"""
import sys, os, re, glob

# Make stdout UTF-8 so Windows cp1252 can't crash the run; output stays ASCII regardless.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MAX_SHOWN = 8  # cap per-category flag lists

STALLING = [
    (re.compile(r"\bthere (?:was|were|had been)\b", re.I), "there was/were"),
    (re.compile(r"\b(?:began|started|proceeded) to\b", re.I), "began/started to"),
    (re.compile(r"\b(?:could|would) (?:feel|hear|see|sense|smell|taste|tell|make out)\b", re.I), "could feel/see/..."),
    (re.compile(r"\bseemed to\b", re.I), "seemed to"),
    (re.compile(r"\b(?:was|were) able to\b", re.I), "was able to"),
    (re.compile(r"\bhad been\b", re.I), "had been"),
    (re.compile(r"\b(?:was|were) \w+ing\b", re.I), "past progressive (was -ing)"),
]
ADDITIVE = [
    (re.compile(r"\band then\b", re.I), "and then"),
    (re.compile(r"\band so\b", re.I), "and so"),
]
# Sentence-initial only (start of line, or after . ! ?) -- case-sensitive so mid-sentence
# "then" is not flagged.
TRANSITIONS = re.compile(
    r"(?:^|[.!?]\s+|\"\s*)"
    r"(However|Moreover|Furthermore|Meanwhile|Suddenly|Then|Afterwards?|Eventually|"
    r"Finally|Subsequently|Nevertheless|Nonetheless|Indeed|Additionally|Soon)\b"
)
FILTER = re.compile(
    r"\b(saw|watched|heard|felt|noticed|realized|realised|wondered|thought|sensed|"
    r"observed|knew|seemed)\b", re.I
)


def is_heading(line):
    return line.lstrip().startswith("#")


def clip(s, n=70):
    s = s.strip()
    return s if len(s) <= n else s[: n - 3] + "..."


def analyze(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    prose_lines = [(i + 1, ln.rstrip("\n")) for i, ln in enumerate(lines) if not is_heading(ln)]
    text = " ".join(ln for _, ln in prose_lines)
    words = len(text.split())
    sentences = max(1, len(re.findall(r"[.!?]+(?:\s|$)", text)))
    per_k = (lambda c: round(c * 1000.0 / words, 1) if words else 0.0)

    stalling, additive, filters = [], [], []
    transitions = []
    for lineno, ln in prose_lines:
        for rx, label in STALLING:
            for m in rx.finditer(ln):
                stalling.append((lineno, label, clip(ln)))
        for rx, label in ADDITIVE:
            if rx.search(ln):
                additive.append((lineno, label, clip(ln)))
        for m in TRANSITIONS.finditer(ln):
            transitions.append((lineno, m.group(1), clip(ln)))
        filters.extend((lineno,) for _ in FILTER.finditer(ln))

    last_sentence = ""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    if parts:
        last_sentence = clip(parts[-1].strip(), 200)

    name = os.path.basename(path)
    print("=== propulsion flags: %s ===" % name)
    print("words: %d   sentences: %d   avg words/sentence: %.1f"
          % (words, sentences, words / sentences))
    print("")

    def section(title, items, with_label=True):
        print("%s: %d  (%.1f per 1000 words)" % (title, len(items), per_k(len(items))))
        for row in items[:MAX_SHOWN]:
            if with_label:
                lineno, label, snip = row
                print("  L%-4d [%s]  %s" % (lineno, label, snip))
            else:
                lineno, word, snip = row
                print("  L%-4d [%s]  %s" % (lineno, word, snip))
        if len(items) > MAX_SHOWN:
            print("  (+%d more)" % (len(items) - MAX_SHOWN))
        print("")

    section("stalling / stative constructions", stalling)
    section("additive sequencing (and then / and so)", additive)
    section("sentence-initial filler transitions", transitions, with_label=False)
    print("filter verbs (perception that distances): %d  (%.1f per 1000 words)"
          % (len(filters), per_k(len(filters))))
    print("")
    print("last sentence (an unresolved hook, or a tidy summary?):")
    print("  \"%s\"" % last_sentence)
    print("")
    return {"words": words, "stalling": len(stalling), "additive": len(additive),
            "transitions": len(transitions), "filters": len(filters)}


def targets(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        ch = sorted(glob.glob(os.path.join(path, "chapters", "*.md")))
        if ch:
            return ch
        return sorted(glob.glob(os.path.join(path, "*.md")))
    return []


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    files = targets(path)
    if not files:
        print("no .md chapter files found at: %s" % path)
        return 0
    totals = []
    for f in files:
        totals.append((os.path.basename(f), analyze(f)))
    if len(totals) > 1:
        print("=== book summary (per 1000 words) ===")
        for name, t in totals:
            w = t["words"] or 1
            print("  %-32s stall %4.1f  add %4.1f  trans %4.1f  filter %4.1f"
                  % (name, t["stalling"] * 1000.0 / w, t["additive"] * 1000.0 / w,
                     t["transitions"] * 1000.0 / w, t["filters"] * 1000.0 / w))
    return 0


if __name__ == "__main__":
    sys.exit(main())
