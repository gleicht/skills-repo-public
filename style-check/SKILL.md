---
name: style-check
description: >-
  A deterministic, read-only prose-style linter for a manuscript — the scripted
  companion to prose-style and book-editor. It measures what a tired eye misses: crutch
  and filler words, perception "filter" verbs, adverb density, sentence-length monotony,
  word echoes within a paragraph, reading level per chapter against a target, and hard
  counts of em dashes and stock AI-ism phrases, writing the numbers to style-report.md.
  Use whenever the user wants a style check, prose diagnostics, a crutch-word /
  filler-word / adverb / cliché scan, a readability or reading-level check, to find
  overused or repeated words, or objective style metrics before editing. It reports and
  never edits — fixes go to book-editor or the author. A read-only diagnostic in the
  book-machine Edit stage, like the deduplicator; works standalone on any folder of
  chapters.
---

# Style Check

An objective, scripted style pass. The **book-editor** fixes prose and **prose-style**
defines the house voice, but both work by judgment. This skill adds the *measurement*:
it runs a deterministic scan over the chapters and reports the patterns that hide from a
reader who has read the book too many times — the word used four times on one page, the
adverbs piling up, the sentences that all run the same length. It is **read-only**: it
produces numbers and lists; the author or `book-editor` decides what to change.

## Run the script

```
scripts/style_check.py
```

Stdlib only. Point it at the book project folder:

```bash
python scripts/style_check.py <book-folder> [--grade N]
```

`--grade N` sets the target Flesch-Kincaid grade (from the story bible's reading-level
goal, e.g. `--grade 9`); chapters that drift above it are flagged. It is **advisory**
(always exits 0) — a style guide, not a gate.

## What it measures

- **Reading level & sentence length, per chapter** — Flesch-Kincaid grade, average
  sentence length, and a count of very long (40+ word) sentences. Wildly varying grades
  between chapters, or one chapter far above the target, signal a voice that drifts. Very
  uniform sentence lengths read as monotonous.
- **Adverb density** — the share of `-ly` adverbs, with the worst offenders. High density
  (over ~4%) usually means telling that the verbs should carry.
- **Crutch / filler words** — `just`, `really`, `very`, `suddenly`, `began to`, `sort of`,
  and the like: words that mostly add nothing and can be cut.
- **Filter words** — `saw`, `felt`, `noticed`, `realized`, `seemed`: perception verbs that
  put a pane of glass between the reader and the scene.
- **Word echoes** — a distinctive word repeated several times inside one paragraph (the
  unintentional kind, not a deliberate refrain).
- **AI-ism / stock phrases** — hard counts of catalogued tells (`a testament to`,
  `breath caught`, `a wave of … washed over`, `little did`) from the prose-style catalog.
- **Em dashes** — a straight count, since the prose-style house rule replaces them.

## How to use it

1. Run the script (pass `--grade` if the story bible sets a reading level).
2. Read the report as **signal, not law.** A number is a place to look, not an order to
   cut. Some repetition is a chosen refrain; some long sentences earn their length; a
   character may speak in filler. Use judgment — the point is to surface candidates.
3. Write the findings to `style-report.md` in the project folder and summarize the
   standouts for the user.
4. **Hand the fixes to book-editor** (or the author). This skill never edits the
   manuscript; like the deduplicator, it detects and reports.

## Relationship to the other skills

- **prose-style** — defines the rules (no em dashes, no AI-isms, show don't tell). This
  skill *counts* violations of the measurable ones; prose-style and book-editor apply
  the judgment ones.
- **book-editor** — the fixer. Run style-check first to aim the editing pass at the real
  hotspots.
- **deduplicator** — its sibling read-only scan: deduplicator finds *repeated content*,
  style-check finds *repeated and weak wording*. Run both before editing.
- **review-panel** — its line specialist also flags style by judgment; style-check gives
  the panel objective counts to corroborate.
- **book-machine** — offer it in the Edit stage, alongside the deduplicator, feeding the
  book-editor pass.

## What it is not

Not a fixer and not a grammar checker. It is a measuring tape for prose: it tells you
where to look, and leaves the cutting to the editor.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill style-check --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
