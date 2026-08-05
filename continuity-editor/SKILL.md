---
name: continuity-editor
description: An active per-chapter continuity editor. It reads a drafted chapter and fixes consistency drift in place — names and spellings, ages, tells, relationships, the timeline and day-count, objects and evidence, world rules, POV and tense, and secrets revealed too early — correcting the prose to match the story bible, characters.json, prior chapters, and book.json. It is the active, single-chapter cousin of fidelity-review (which audits the whole book read-only). Use whenever the user wants to fix continuity errors, consistency problems, canon drift, or contradictions within a chapter. It treats the sources of truth as authoritative and never changes canon to match a mistake; genuine gaps are flagged, not invented.
---

# Continuity Editor

The continuity lens of the per-chapter editor panel. It reads one drafted chapter and
**corrects consistency drift in place** so the chapter agrees with the book's canon and
everything written before it. It is the *active*, single-chapter counterpart of
**fidelity-review** (the read-only whole-book auditor).

## What it checks and fixes

- **Names and spellings.** Every character and place spelled one canonical way
  (per `characters.json` and `story-bible.md`); no variant or renamed character.
- **Character facts.** Ages, appearance, tells, manner of speaking, relationships, and the
  `continuityNotes` that must never drift.
- **Timeline.** The day-count and elapsed-time phrases progress consistently and match the
  story bible's timeline; no scene out of order, no overshoot.
- **Objects and evidence.** Items, their locations, and who holds what stay consistent
  across chapters (and any do-not-lose / chain-of-custody rules hold).
- **World rules.** Nothing contradicts the story bible's world rules or motif system.
- **POV and tense.** The chapter uses the POV character and tense the roster assigns; no
  head-hopping; no character given interiority they should not have.
- **Reveal timing.** A character's `secret`, or a plot reveal, is not exposed earlier than
  the plan allows.

## How it runs

1. Read the chapter against `story-bible.md`, `characters.json`, `outline.json`, `book.json`,
   `research.md` (if present), and the previous chapter(s) for carried-in facts.
2. **Fix the prose to match canon.** Correct the wrong age, the misspelled name, the
   timeline slip, the moved object, the early reveal, the POV break — the smallest change
   that restores consistency.
3. Where the prose and the sources genuinely disagree and you cannot tell which is right,
   **flag it for the author**; do not guess and do not invent a fact to paper over the gap.
4. Write the corrected version and a change-note (each fix: what was wrong, what it now is).

## What it writes

Non-destructive. Inside **editor-ensemble**, write `editors/NN-slug/continuity.md` and
return the change-note. Standalone, write the same file plus the note; promote on the
author's OK (copy over `chapters/NN-slug.md`).

## Constraints

- **The sources of truth win.** Never edit `story-bible.md` / `characters.json` /
  `outline.json` to match a mistake in the prose, and never "resolve" a contradiction by
  inventing a fact. If a source is actually wrong or out of date, surface it.
- **Stay chapter-local.** Fix this chapter; whole-book reconciliation is fidelity-review's
  job. Do not change plot or voice beyond what consistency requires.

## Relationship to the other skills

- **fidelity-review** — the read-only whole-book truth/continuity audit; continuity-editor
  applies the per-chapter fixes so fidelity-review finds less to flag.
- **editor-ensemble** — runs this as one of five parallel editors.
- **story-bible / character-dossier** — the canon this lens enforces and never overrides.

## What it is not

Not a craft or quality edit and not a whole-book pass. It makes one chapter consistent with
the established record, and flags real gaps rather than inventing answers.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill continuity-editor --target <book-folder> --status DONE --item "<chapter>" --output "editors/NN-slug/continuity.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
