#!/usr/bin/env python3
"""Deterministic AI-ism candidates for one chapter or a whole book folder.

The scripted half of the ai-ism-editor skill. It matches surface strings only, so every
hit is a CANDIDATE, not a verdict: a stock phrase used once in a character's own register
is not an AI-ism, and repetition is what marks the pattern. The judgment pass is the
skill's job, against references/ai-isms.md.

Usage:
    python ai_ism_flags.py <chapter.md>
    python ai_ism_flags.py <book-folder>        # scans chapters/*.md

Always exits 0 (advisory). ASCII output, UTF-8 stdin/stdout, safe on Windows consoles.
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- flag lists, keyed to references/ai-isms.md sections -------------------------------

SIGNATURE = [  # 2.1 signature AI words
    "delve", "leverage", "robust", "seamless", "nuanced", "tapestry", "landscape",
    "navigate", "foster", "synergy", "holistic", "myriad", "underscore", "pivotal",
    "realm", "testament", "intricate", "multifaceted", "paradigm", "elevate",
    "unlock", "harness", "embark", "resonate", "profound", "vibrant", "crucial",
]
RECYCLED = [  # 2.2 fiction-specific recycled words
    "flicker", "flickered", "ache", "ached", "hollow", "shatter", "shattered",
    "fragile", "shiver", "shivered", "tremble", "trembled", "linger", "lingered",
    "pulse", "pulsed", "thrum", "thrummed", "gaze", "raw",
]
INFLATED = ["soul", "fate", "void", "unbearable", "eternity", "abyss", "oblivion"]  # 2.3
PLACEHOLDER = ["something", "things", "stuff"]  # 2.4 (devague owns the full pass)

FILLER = [  # 1.2 hollow filler, 1.5 hedging
    "it's worth noting", "it is worth noting", "when it comes to", "in order to",
    "the fact that", "needless to say", "it's important to", "it is important to",
    "at the end of the day", "that being said", "in today's world",
    "arguably", "perhaps somewhat", "it could be argued", "one might say",
]
OPENERS = [  # sentence-initial filler transitions
    "however", "moreover", "furthermore", "additionally", "indeed", "notably",
    "ultimately", "essentially", "importantly", "consequently", "nevertheless",
]
STOCK = [  # 4.4 high-frequency fiction phrases, 4.5 cliched sensory metaphors
    "breath caught", "jaw tightened", "jaw clenched", "eyes met", "heart hammered",
    "heart pounded", "heart raced", "blood ran cold", "ice in her veins",
    "ice in his veins", "let out a breath", "held her breath", "held his breath",
    "the silence was deafening", "a sense of", "washed over", "a chill ran",
    "barely a whisper", "trailed off", "swallowed hard", "let out a sigh",
    "couldn't help but", "a beat passed", "time seemed to slow",
]
EMOTION = [  # 4.2 emotion labeling
    "angry", "sad", "afraid", "scared", "nervous", "happy", "furious", "anxious",
    "terrified", "relieved", "confused", "excited", "devastated", "ashamed",
]


def sentences(text):
    """Rough sentence split, good enough for surface flags."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def scan(path):
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    # strip fenced code and the "# Title" heading line
    body = re.sub(r"```.*?```", "", raw, flags=re.S)
    body = re.sub(r"^#.*$", "", body, flags=re.M)
    lines = body.split("\n")
    # Phrases and sentences must match across line wraps, so search a flattened copy.
    flat = re.sub(r"\s+", " ", body)
    low = flat.lower()
    hits = {}

    def add(label, item, count, examples):
        if count:
            hits.setdefault(label, []).append((item, count, examples))

    def line_of(term):
        out = []
        for i, ln in enumerate(lines, 1):
            if re.search(r"\b" + re.escape(term) + r"\b", ln, re.I):
                out.append(i)
        return out[:4]

    for label, words in (
        ("2.1 signature AI vocabulary", SIGNATURE),
        ("2.2 recycled fiction mood words", RECYCLED),
        ("2.3 inflated diction", INFLATED),
        ("2.4 vague placeholders (see devague)", PLACEHOLDER),
    ):
        for w in words:
            n = len(re.findall(r"\b" + re.escape(w) + r"\b", low))
            add(label, w, n, line_of(w))

    for label, phrases in (
        ("1.2/1.5 filler and hedging", FILLER),
        ("4.4/4.5 stock phrases and cliched metaphors", STOCK),
    ):
        for p in phrases:
            n = low.count(p)
            # Line numbers are best-effort: a phrase broken across a wrap still counts,
            # it just cannot be pinned to one line.
            add(label, p, n, [i for i, ln in enumerate(lines, 1) if p in ln.lower()][:4])

    sents = sentences(flat)

    # sentence-initial filler transitions
    for w in OPENERS:
        n = sum(1 for s in sents if s.lower().startswith(w + ",") or s.lower().startswith(w + " "))
        add("sentence-initial filler transitions", w, n, [])

    # 4.2 emotion labeling: "was/felt/seemed <emotion>"
    for w in EMOTION:
        n = len(re.findall(r"\b(?:was|were|felt|seemed|looked)\s+(?:very\s+|so\s+)?" + w + r"\b", low))
        add("4.2 emotion labeling", "was/felt " + w, n, [])

    # 4.13 participial openings: sentence starts with an -ing verb + comma clause
    part = [s for s in sents if re.match(r"^[A-Z][a-z]+ing\b[^,.]{0,60},", s)]
    # 4.15 negation-correction antithesis. The two-sentence form ("It wasn't grief. It was
    # something else.") spans a sentence break, so match on the flattened text.
    neg = []
    for pat in (
        # "It wasn't X. It was Y." / "She wasn't tired. She was furious."
        r"\b(?:it|that|this|he|she|they)\s+(?:wasn't|weren't|isn't|aren't|was not|were not)\b[^.!?]*[.!?]\s*"
        r"(?:it|that|this|he|she|they)\s+(?:was|were|is|are)\b[^.!?]*[.!?]",
        # "not X, but Y" within one sentence
        r"\bit\s+(?:was|is)\s+not\b[^.!?]*\bbut\b[^.!?]*[.!?]",
        # bare "Not X." fragment
        r"(?:^|(?<=[.!?]\s))Not\s+\w+[^.!?]{0,60}[.!?]",
    ):
        neg += [m.group(0).strip() for m in re.finditer(pat, flat, re.I)]

    emdash = body.count("—")
    last = sents[-1] if sents else ""

    return hits, part, neg, emdash, last, len(body.split())


def report(path, root=None):
    rel = os.path.relpath(path, root) if root else os.path.basename(path)
    hits, part, neg, emdash, last, words = scan(path)
    print("=" * 72)
    print("%s  (%d words)" % (rel, words))
    print("=" * 72)
    total = 0
    for label in sorted(hits):
        rows = [r for r in hits[label] if r[1]]
        if not rows:
            continue
        rows.sort(key=lambda r: -r[1])
        n = sum(r[1] for r in rows)
        total += n
        print("\n[%s]  %d hit(s)" % (label, n))
        for item, count, ex in rows[:12]:
            where = ("  lines %s" % ", ".join(str(e) for e in ex)) if ex else ""
            print("   %-42s x%d%s" % (item, count, where))
    if part:
        total += len(part)
        print("\n[4.13 participial openings]  %d" % len(part))
        for s in part[:5]:
            print("   %s" % s[:88])
    if neg:
        total += len(neg)
        print("\n[4.15 negation-correction antithesis -- cut by default]  %d" % len(neg))
        for s in neg[:5]:
            print("   %s" % s[:88])
    print("\n[em dashes]  %d  (prose-style Part 1: replace all but interrupted dialogue)" % emdash)
    print("\n[last sentence -- check for a reflective ending, 4.11]")
    print("   %s" % last[:200])
    print("\nTOTAL surface candidates: %d  (candidates, not verdicts -- read each one)\n" % total)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    target = sys.argv[1]
    if os.path.isdir(target):
        chapters = os.path.join(target, "chapters")
        root = target if os.path.isdir(chapters) else None
        folder = chapters if os.path.isdir(chapters) else target
        files = sorted(f for f in os.listdir(folder) if f.endswith(".md"))
        if not files:
            print("No .md files found in %s" % folder)
            return 0
        for f in files:
            report(os.path.join(folder, f), root)
    else:
        report(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
