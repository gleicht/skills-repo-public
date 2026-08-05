---
name: dialogue-pass
description: A focused craft review of a book's dialogue — deeper on speech than book-editor's holistic pass. It reads the conversations across the manuscript and reports where character voices blur together, where speech sounds stiff or on-the-nose, where dialogue tags and action beats are mishandled (said-bookisms, adverb-laden tags, tag/beat imbalance), where exposition is dumped into talk, and where formatting or dialect is inconsistent — writing the findings to dialogue-report.md. Use whenever the user wants a dialogue pass, to review or sharpen dialogue, check that characters sound distinct, fix stilted or expository conversation, or clean up dialogue tags and beats. Read-only: it diagnoses and suggests; book-editor or the author makes the changes. A focused craft review in the book-machine Edit stage; works standalone on any folder of chapters.
---

# Dialogue Pass

A single-lens craft review aimed only at how the characters talk. The **book-editor**
edits the whole manuscript and the **review-panel** reads it as beta readers; this pass
goes *deep on dialogue specifically* — the layer that most often separates flat fiction
from sharp fiction, and the one a broad pass skims. It is **read-only**: it reports
problems and concrete suggestions; the author or `book-editor` rewrites.

Run it on a drafted manuscript, after the cast is settled (it leans on
`characters.json` for each voice), as part of editing.

## What it reads

- **`chapters/*.md`** — the dialogue in context.
- **`characters.json`** — each character's voice, background, and education, so the pass
  can judge whether they actually *sound* like themselves and unlike each other.
- **`story-bible.md`** — the voice & style guide and any era/register constraints
  (period diction, formality).

## What it reviews

- **Distinct voices.** The core test: cover the dialogue tags and can you still tell who
  is speaking? Flag characters whose speech is interchangeable — same vocabulary,
  rhythm, and verbal habits. Note who *should* differ (age, region, class, era) but
  doesn't.
- **Naturalness.** Stilted, overly grammatical, or stagey lines; speeches no one would
  actually say aloud; contractions missing where a voice would use them.
- **On-the-nose & exposition.** Characters stating feelings outright, or explaining plot
  and backstory to each other purely for the reader ("As you know, Bob…"). Flag
  info-dumps disguised as conversation.
- **Tags & beats.** Said-bookisms (`he expostulated`, `she ejaculated`) and
  adverb-laden tags (`"No," he said angrily`) where `said`/`asked` plus an action beat
  would carry it; over-tagging in a clear two-person exchange; or long stretches with no
  attribution where the reader loses the thread. Aim for the right *balance* of tag,
  beat, and clean line.
- **Subtext & conflict.** Exchanges where everyone simply agrees and says what they
  mean; note where a scene's dialogue could carry tension or be doing two things at once.
- **Formatting & dialect.** Consistent quote style and paragraphing (a new speaker = a
  new paragraph); dialect rendered readably and consistently, not as a wall of
  apostrophes.

## How to run it

1. Read the dialogue across the book with the cast voices from `characters.json` in mind.
   For a long book, work chapter by chapter and note cross-book voice drift.
2. Record each finding **located and concrete**: chapter, the quoted line, the problem,
   and a suggested direction (not a full rewrite). For voice-blur, name *which* characters
   and *why* they read alike.
3. Write `dialogue-report.md` to the project folder, grouped by the categories above,
   plus a short per-character note on how distinct each voice currently reads.
4. Hand the fixes to **book-editor** or the author. *(For the mechanical counts — adverb-
   laden tags, said-bookism frequency — the **style-check** script can corroborate.)*

## Relationship to the other skills

- **book-editor** — the fixer; this pass aims its dialogue work.
- **character-dossier / `characters.json`** — the source of each intended voice; flag
  speech that contradicts a character's profile.
- **review-panel** — its generalists judge dialogue among everything else; this is the
  deeper, dedicated pass when dialogue is the priority.
- **style-check** — objective counts (tag adverbs, repeated words) that back up the
  craft findings.
- **prose-style** — the house rule that *dialogue stays jagged* (real speech is
  fragmentary) while narration is complete-sentence; honor that split here.

## What it is not

Not a rewrite of the manuscript and not a whole-book review — it is the focused dialogue
lens. It reports; the editor or author revises.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill dialogue-pass --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
