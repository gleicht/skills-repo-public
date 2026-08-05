#!/usr/bin/env python3
"""
check_duplication.py - scan a book project's chapters for duplicated content.

Pure standard library (no installs). Run pointed at a book project folder:

    python check_duplication.py <book-folder> [--threshold 0.25] [--json]

If <book-folder> is omitted, the current directory is used. The script reads
`chapters/*.md` (ordered/titled by `outline.json` when present, otherwise by
filename) and reports five kinds of duplication, from hardest to softest:

  1. Exact duplicate chapters   - identical body text (a copy-paste accident).
  2. Near-duplicate chapter pairs - high word-overlap (paraphrased or partially
                                    pasted content) via 5-word-shingle Jaccard
                                    similarity and containment.
  3. Identical paragraphs        - the same paragraph appearing in two chapters.
  4. Repeated sentences          - an 8+ word sentence appearing in 2+ places.
  5. Word-count table            - with identical counts flagged (a copy hint).

It is READ-ONLY: it never edits the manuscript. Removing or consolidating
anything it finds is a judgment call for the author or the book-editor skill.

Exit code is 0 when nothing notable is found, 1 when any exact duplicate,
identical paragraph, or near-duplicate pair (>= threshold) is detected, so the
script can also gate a pipeline.
"""
import sys, os, re, json, glob, hashlib, argparse
from collections import defaultdict


def load_chapters(folder):
    """Return an ordered list of {id,title,file,body} for the book's chapters."""
    chap_dir = os.path.join(folder, "chapters")
    if not os.path.isdir(chap_dir):
        # tolerate being pointed straight at a chapters/ folder
        chap_dir = folder if os.path.basename(folder.rstrip("/\\")) == "chapters" else chap_dir
    files = sorted(glob.glob(os.path.join(chap_dir, "*.md")))
    if not files:
        return []

    # order/titles from outline.json when available
    order = None
    outline_path = os.path.join(folder, "outline.json")
    if os.path.isfile(outline_path):
        try:
            outline = json.load(open(outline_path, encoding="utf-8"))
            order = [c.get("id") for c in outline.get("chapters", [])]
        except Exception:
            order = None

    def file_for_id(cid):
        for f in files:
            if os.path.basename(f).startswith(str(cid)):
                return f
        return None

    chapters = []
    used = set()
    seq = order if order else [os.path.basename(f).split("-")[0] for f in files]
    for cid in seq:
        f = file_for_id(cid)
        if not f or f in used:
            continue
        used.add(f)
        chapters.append(_read_chapter(f))
    # append any files not referenced by the outline
    for f in files:
        if f not in used:
            chapters.append(_read_chapter(f))
    return chapters


def _read_chapter(path):
    raw = open(path, encoding="utf-8").read()
    lines = raw.splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else os.path.basename(path)
    body = "\n".join(l for l in lines if not l.startswith("# "))
    return {"file": os.path.basename(path), "title": title, "body": body}


def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def shingles(text, k=5):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return set(tuple(words[i:i + k]) for i in range(max(0, len(words) - k + 1)))


def paragraphs(body, min_chars=40):
    return [p.strip() for p in re.split(r"\n\s*\n", body) if len(p.strip()) >= min_chars]


def sentences(body, min_words=8):
    flat = re.sub(r"\s+", " ", body)
    return [s.strip() for s in re.split(r'(?<=[.!?"”])\s+', flat) if len(s.split()) >= min_words]


def analyze(chapters, threshold=0.25):
    n = len(chapters)
    report = {"chapter_count": n, "exact": [], "near": [], "shared_paragraphs": [],
              "repeated_sentences": [], "word_counts": [], "identical_word_counts": []}

    # word counts
    for c in chapters:
        c["words"] = len(c["body"].split())
        report["word_counts"].append({"file": c["file"], "title": c["title"], "words": c["words"]})
    wc_index = defaultdict(list)
    for c in chapters:
        wc_index[c["words"]].append(c["file"])
    report["identical_word_counts"] = [v for v in wc_index.values() if len(v) > 1]

    # precompute
    for c in chapters:
        c["hash"] = hashlib.md5(normalize(c["body"]).encode()).hexdigest()
        c["shingles"] = shingles(c["body"])
        c["paras"] = set(paragraphs(c["body"]))

    # 1. exact duplicate chapters
    seen = {}
    for c in chapters:
        if c["hash"] in seen:
            report["exact"].append([seen[c["hash"]], c["file"]])
        else:
            seen[c["hash"]] = c["file"]

    # 2. near-duplicate pairs (Jaccard + containment over 5-word shingles)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = chapters[i], chapters[j]
            if not a["shingles"] or not b["shingles"]:
                continue
            inter = len(a["shingles"] & b["shingles"])
            if inter == 0:
                continue
            union = len(a["shingles"] | b["shingles"])
            jacc = inter / union
            contain = inter / min(len(a["shingles"]), len(b["shingles"]))
            if jacc >= threshold or contain >= max(threshold * 1.5, 0.4):
                report["near"].append({"a": a["file"], "b": b["file"],
                                       "similarity": round(jacc, 3), "containment": round(contain, 3)})
    report["near"].sort(key=lambda x: -max(x["similarity"], x["containment"]))

    # 3. identical paragraphs across chapters
    para_index = defaultdict(list)
    for c in chapters:
        for p in c["paras"]:
            para_index[p].append(c["file"])
    for p, locs in para_index.items():
        if len(set(locs)) > 1:
            report["shared_paragraphs"].append({"where": sorted(set(locs)), "text": p[:160]})

    # 4. repeated sentences (8+ words) anywhere in the book
    sent_index = defaultdict(list)
    for c in chapters:
        for s in sentences(c["body"]):
            sent_index[normalize(s)].append(c["file"])
    for s, locs in sent_index.items():
        if len(locs) > 1:
            report["repeated_sentences"].append({"count": len(locs), "where": locs, "text": s[:160]})
    report["repeated_sentences"].sort(key=lambda x: -x["count"])
    return report


def render(report, threshold):
    out = []
    n = report["chapter_count"]
    out.append(f"DUPLICATION REPORT - {n} chapters  (near-dup threshold = {threshold})")
    out.append("=" * 64)

    out.append("\n[1] EXACT DUPLICATE CHAPTERS (identical body text)")
    if report["exact"]:
        for pair in report["exact"]:
            out.append(f"    DUPLICATE: {pair[0]}  ==  {pair[1]}")
    else:
        out.append("    none")

    out.append("\n[2] NEAR-DUPLICATE CHAPTER PAIRS (paraphrased / partly pasted)")
    if report["near"]:
        for pr in report["near"]:
            out.append(f"    {pr['a']}  <>  {pr['b']}   similarity {pr['similarity']}  containment {pr['containment']}")
    else:
        out.append(f"    none above threshold {threshold}")

    out.append("\n[3] IDENTICAL PARAGRAPHS shared across chapters")
    if report["shared_paragraphs"]:
        for sp in report["shared_paragraphs"]:
            out.append(f"    in {', '.join(sp['where'])}:")
            out.append(f"        \"{sp['text']}...\"")
    else:
        out.append("    none")

    out.append("\n[4] REPEATED SENTENCES (8+ words appearing in 2+ places)")
    if report["repeated_sentences"]:
        for rs in report["repeated_sentences"][:25]:
            out.append(f"    x{rs['count']}  ({', '.join(rs['where'])}):")
            out.append(f"        \"{rs['text']}...\"")
        if len(report["repeated_sentences"]) > 25:
            out.append(f"    ... and {len(report['repeated_sentences']) - 25} more")
    else:
        out.append("    none")

    out.append("\n[5] WORD COUNTS")
    for w in report["word_counts"]:
        out.append(f"    {w['file'][:44]:46} {w['words']:>6}w")
    if report["identical_word_counts"]:
        out.append("    NOTE - chapters with identical word counts (possible copy):")
        for grp in report["identical_word_counts"]:
            out.append(f"        {', '.join(grp)}")

    flagged = bool(report["exact"] or report["near"] or report["shared_paragraphs"])
    out.append("\n" + "=" * 64)
    if flagged:
        out.append("VERDICT: DUPLICATION FOUND - review sections above. Removal is the")
        out.append("author's / book-editor's call (this scan never edits the manuscript).")
    elif report["repeated_sentences"]:
        out.append("VERDICT: CLEAN on chapters/paragraphs. Some repeated sentences exist")
        out.append("(often intentional refrains) - skim section [4] to confirm.")
    else:
        out.append("VERDICT: CLEAN - no duplicated chapters, passages, or sentences.")
    return "\n".join(out), flagged


def main():
    ap = argparse.ArgumentParser(description="Scan a book's chapters for duplicated content.")
    ap.add_argument("folder", nargs="?", default=".", help="book project folder (default: current dir)")
    ap.add_argument("--threshold", type=float, default=0.25,
                    help="near-duplicate Jaccard threshold (0-1, default 0.25)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of a report")
    args = ap.parse_args()

    chapters = load_chapters(args.folder)
    if not chapters:
        print("No chapters found. Point this at a book folder containing chapters/*.md "
              "(or run the chapter-writer skill first).", file=sys.stderr)
        sys.exit(2)

    report = analyze(chapters, args.threshold)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        flagged = bool(report["exact"] or report["near"] or report["shared_paragraphs"])
    else:
        text, flagged = render(report, args.threshold)
        print(text)
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
