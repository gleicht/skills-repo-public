---
name: ai-ism-editor
description: >-
  An active per-chapter AI-ism editor, and the owner of the full AI-ism catalog
  (references/ai-isms.md). It rewrites a drafted chapter to strip the patterns that make
  prose read as machine-generated, including hollow filler and hedging, signature AI
  vocabulary (delve, tapestry, robust), emotion labeling, vague abstraction, stock fiction
  phrases (her breath caught, his jaw tightened), clichéd metaphors, false profundity,
  reflexive reflective endings, and the negation-correction antithesis. Use whenever the
  user wants to remove AI-isms, de-AI or humanize prose, make writing sound like a person
  wrote it, cut cliché or stock phrasing, fix prose that reads as generated, or lower an
  AI-detection score. The active counterpart to the read-only ai-detection scan; runs on
  every chapter in the drafting loop and standalone. Never flattens the voice, never
  invents plot.
---

# AI-ism Editor

The de-machining pass. It reads one drafted chapter and rewrites the patterns that make
prose read as generated, then hands back a proposal. It is the **active counterpart to
ai-detection**: ai-detection scores how machine-written a manuscript reads, this fixes it.

This skill **owns the AI-ism catalog**. The complete flag lists, before/after rewrites, and
diagnostic codes live in **`references/ai-isms.md`** (nine sections). Every other skill in
the suite, prose-style included, points here rather than keeping its own copy.

**Read `references/ai-isms.md` before rewriting.** This file is the operative summary; the
reference is the full catalog and the authority on any specific flag.

## What it strips

Grouped as the catalog groups them.

- **Conversational** (§1) — overused openers ("Certainly!", "Let's dive in"), hollow filler
  ("It's worth noting that", "When it comes to"), question-restating, automated closings,
  hedging overload, reflexive fake enthusiasm.
- **Vocabulary** (§2) — signature AI words (delve, leverage, robust, seamless, nuanced,
  tapestry, landscape, navigate, foster, holistic). Name the specific thing instead. In
  fiction, recycled mood words (flicker, ache, hollow, shatter, fragile), inflated diction
  (soul, fate, void, unbearable), and vague placeholder nouns (§2.4).
- **Structural** (§3) — over-formatting where prose serves better, fake balance ("on one
  hand, on the other"), the summary sandwich.
- **Fiction** (§4, the big one) — vague abstraction ("a sense of dread filled the room"),
  emotion labeling ("she was angry"), generic poetic phrasing ("the silence was
  deafening"), high-frequency stock phrases ("her breath caught," "their eyes met"),
  clichéd sensory metaphors ("heart hammered," "ice in her veins"), atmosphere as
  decoration, metaphor stacking, false profundity, dialogue too clean or too jagged,
  emotional overstatement in dialogue, reflective endings by default, theme stated too
  directly, participial-opening pileups, backstory inserted too smoothly, and the
  **negation-correction antithesis** ("it wasn't X, it was Y"), which is cut by default.

**The core fix is always the same:** show rather than tell, choose the concrete detail that
belongs only to this scene, and trust the reader.

## How it runs

1. **Deterministic flags first** (the scripted half):
   ```bash
   python scripts/ai_ism_flags.py <chapter.md | book-folder>
   ```
   It lists signature vocabulary, stock fiction phrases, filler and hedging, sentence-initial
   filler transitions, participial openings, negation-correction constructions, em dashes,
   and the chapter's last sentence (the usual site of a reflective ending). These are
   *candidates*, not verdicts. The script matches surface strings; it cannot tell a cliché
   from a deliberate echo, so every hit gets a human read.
2. **Read for the rest** against `references/ai-isms.md`, the chapter's `story-bible.md`
   (the plot beats and the **Voice Sample**), `characters.json` (the POV character's voice,
   want, and fear), the previous chapter (the live voice), and the **prose-style** baseline.
   The worst AI-isms are not string-matchable: abstraction standing in for a specific image,
   atmosphere doing no work, a tidy insight the scene did not earn.
3. **Rewrite, using the revision moves** (§8): replace abstraction with visible behavior;
   replace cliché with a specific sound, object, or gesture; let action carry emotion; swap
   tidy insight for a partial thought; break rhythmic sameness; loosen dialogue toward
   natural speech, not staccato; cut the reflective last sentence, since the scene already
   did the work.
4. **Preserve the human stuff** (§7). This is the constraint that makes the pass worth
   running rather than damaging. See Constraints below.
5. **Write the stronger version and a change-note** naming each pattern removed, with the
   line before and after, and anything deliberately left alone with the reason.

## What it writes

Non-destructive. Run standalone or auto-fired in the loop, write
`ai-isms/NN-slug.report.md` and `ai-isms/NN-slug.edited.md`.

It runs **third in the per-draft loop**, so it edits from whatever the passes before it
produced: **from `propulsion/NN-slug.edited.md` if it exists, else `clarity/NN-slug.edited.md`,
else the chapter itself.** That keeps clarity, propulsion, and de-AI-ing in a single
promotable proposal. Inside **editor-ensemble**, write `editors/NN-slug/ai-ism.md` and return
the change-note instead.

The edit is a **proposal**: promote it over `chapters/NN-slug.md` only on the author's OK, by
**copying** the file with a shell command (`cp` / `Copy-Item`), not the Write/Edit tools, so
promotion does not re-trigger the per-chapter hook.

## Constraints

- **Don't sand off the human stuff.** Removing AI-isms can flatten prose into something
  correct and dead, which is the failure mode to fear here. Keep idiosyncratic phrasing, real
  subtext, asymmetric dialogue, emotional contradiction, surprising-but-precise detail, voice
  shaped by character, and tension that does not resolve on cue. A line that *is* the voice
  stays even if it trips a flag.
- **A flag is not a verdict.** A stock phrase used once, deliberately, in a character's own
  register is not an AI-ism. Repetition and reflexiveness are what mark the pattern. When a
  hit is defensible, leave it and say so in the report.
- **Never invent plot.** Rewrite how the existing beat is rendered, never what happens.
  Defer to `outline.json`, `story-bible.md`, and `characters.json` on canon and POV.
- **Keep the length honest.** De-AI-ing usually cuts a little, since it removes filler and
  reflective wind-downs. Where cutting a padded passage would drop the chapter below its
  weight, refocus it into story the way propulsion-editor does rather than leaving a hole.
- **Don't game a detector.** The goal is prose that genuinely reads as human. Never
  introduce typos, odd unicode, or artificial variation to move a score. See ai-detection.

## Relationship to the other skills

- **prose-style** — the house style; its Part 3 is the short summary of this skill's rules
  and points here for the catalog. This skill owns the catalog and does the active removal.
- **ai-detection** — the read-only scan that *scores* how machine-written the prose reads.
  It diagnoses, this fixes. The natural loop is detect, then run this on the worst chapters,
  then re-scan.
- **style-check** — reports hard counts of stock AI-ism phrases and em dashes as part of its
  broader linting. Another way to find the chapters that need this pass.
- **clarity-edit / propulsion-editor** — the two passes that run before it in the per-draft
  loop. This edits from their output so all three land in one proposal.
- **voice-editor** — holds the book's voice across the chapter and also enforces prose-style.
  Complementary: voice-editor keeps the prose sounding like *this book*, this keeps it
  sounding like *a person*.
- **book-editor** — the whole-manuscript pass; it uses this skill's flag lists and diagnostic
  codes to mark passages across the book.
- **chapter-writer** — writes against the catalog up front; this enforces it right after.
- **editor-ensemble** — can run it as an additional editor on a high-effort chapter.

## What it is not

Not a style flattener, not a rewrite of what happens, and not a detector-score optimizer. It
removes the machine tells and leaves the writing more specific, more concrete, and more the
author's own than it found it.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill ai-ism-editor --target <book-folder> --status DONE --item "<chapter>" --output "ai-isms/NN-slug.edited.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
