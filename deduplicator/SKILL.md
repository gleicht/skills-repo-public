---
name: deduplicator
description: Scans a drafted manuscript for duplicated content - chapters that are exact or near-duplicates of one another, paragraphs or passages pasted into two places, and sentences repeated across the book - and reports them without touching the files. Use whenever the user wants to check a book or its chapters for duplication, repeated or copy-pasted content, accidental duplicate or near-identical chapters, or wants to "de-dupe", "find duplicates", "check for repeated passages", or confirm every chapter is unique. Also use it as a routine QA gate before editing, verifying, or packaging a manuscript, even if the user does not name it. A read-only diagnostic stage in the book-machine pipeline (like fidelity-review and review-panel); it detects and reports, and leaves actual removal to the book-editor skill or the author. This is for prose manuscripts (books, novels, chapter folders), NOT for de-duplicating spreadsheet rows, database records, file lists, contacts, or code. Works standalone on any folder of chapter files.
---

# Deduplicator

A QA gate that answers one question precisely: **does this manuscript repeat
itself?** Long books drafted in many sittings (or assembled from notes, or
regenerated chapter by chapter) are prone to silent duplication - a chapter
pasted in twice under two titles, a vivid paragraph reused in two places, a
backstory beat re-explained almost word for word. A reader notices, and it reads
as carelessness. This skill finds that duplication mechanically so it does not
survive to print.

It is **read-only**, like fidelity-review and review-panel. It produces a report;
it never edits the chapters. Deciding what to cut or merge is a judgment call that
belongs to the author or to the **book-editor** skill - some repetition is an
accident, and some (a refrain, a deliberate motif, a parallel structure) is the
point. The detector's job is to surface every candidate and let a human judge.

## When to run it

- The user asks to check for duplicate chapters, repeated passages, or copy-paste.
- A book was drafted across many sessions, merged from drafts, or regenerated in
  pieces - exactly the conditions that produce accidental duplication.
- As a routine pass before the **book-editor**, **fidelity-review**, or packaging
  stages, so duplication is caught while it is still cheap to fix.

## Inputs (the book project-folder contract)

Identical to the rest of the suite, so it drops into any book project:

```
<book-folder>/
├── outline.json     # (optional) chapter order + titles; used to label the report
└── chapters/
    ├── 01-*.md
    └── 02-*.md
```

Order and titles come from `outline.json` when present; otherwise the chapters are
read in filename order. Only `chapters/*.md` are analyzed.

## How to run it - use the bundled script

Do not eyeball 40 chapters for repetition by hand; that is what the script is for,
and it is deterministic and fast. Run it pointed at the book folder:

```bash
python scripts/check_duplication.py <book-folder>
```

Standard-library Python 3 only - **no installs**. Run it from the skill directory
or pass the script's absolute path. Useful flags:

- `--threshold <0-1>` - the near-duplicate sensitivity (default `0.25`). Lower it
  (e.g. `0.15`) to surface looser echoes; raise it to report only heavy overlap.
- `--json` - emit machine-readable JSON instead of the text report (for piping into
  another stage). The script's **exit code is 1** when any exact duplicate,
  near-duplicate pair, or shared paragraph is found, and 0 otherwise, so it can gate
  a pipeline.

## What it checks (hardest duplication to softest)

1. **Exact duplicate chapters** - two chapter files with identical body text. Almost
   always a copy-paste accident; the strongest signal.
2. **Near-duplicate chapter pairs** - paraphrased or partially pasted chapters,
   found by comparing 5-word-shingle sets and reporting **similarity** (Jaccard
   overlap) and **containment** (how much of the smaller chapter sits inside the
   larger). This catches the cases exact matching misses: a chapter lightly reworded,
   or one chapter's scene dropped into another.
3. **Identical paragraphs across chapters** - the same paragraph appearing in two
   different chapters.
4. **Repeated sentences** - any 8-plus-word sentence that appears in two or more
   places in the book (across or within chapters). Many of these are intentional
   refrains; the report lists them so a human can confirm.
5. **Word-count table** - every chapter's length, with any chapters sharing an
   identical word count flagged (a weak but real hint that one is a copy of another).

The report ends with a one-line **VERDICT**: clean, clean-but-with-refrains, or
duplication-found.

## Reading and reporting the results

Relay the report to the user and interpret it, do not just dump it:

- **Exact duplicates or shared paragraphs** are almost certainly real problems -
  name the chapters and recommend the fix (usually: keep one, cut the other, or hand
  the merge to **book-editor**).
- **Near-duplicate pairs** need a look: open both and decide whether it is true
  duplication, a deliberately parallel structure (e.g. a "then vs. now" comparison),
  or two distinct scenes that merely share vocabulary. Report which.
- **Repeated sentences** are usually fine (a motif, a callback). Skim them and flag
  only the ones that read as accidental restatement.
- A **clean** result is a real result worth stating plainly, so the author knows the
  book was checked and is unique.

## Principles

- **Non-destructive, always.** The script and this skill never modify a chapter.
  Detection and removal are deliberately separate jobs.
- **Detect, then let a human judge.** Flag every candidate; do not decide unilaterally
  that a refrain is a defect. Repetition can be craft or accident, and only a reader
  in context can tell which.
- **Hand fixes off.** When real duplication is confirmed, the cut or merge is the
  **book-editor**'s job (or the author's). Say so and hand it over.

## Relationship to the other skills

- **book-editor** owns the actual removal/merge once duplication is confirmed.
- **fidelity-review** checks a book against its plan and sources of truth;
  **review-panel** judges whether the story works for a reader. This skill is the
  narrow, mechanical complement: it answers only "does the text repeat itself."
- **prose-style** governs overused *phrasing* (AI-isms, stock metaphors, tics) at the
  sentence level; this skill targets duplicated *content* at the passage and chapter
  level. They are complementary - run both for a thorough cleanup.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill deduplicator --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
