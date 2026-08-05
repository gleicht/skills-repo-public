---
name: propulsion-editor
description: >-
  An active per-chapter propulsion editor. It rewrites a drafted chapter so every
  sentence pulls the reader to the next, enforcing forward motion line by line: a
  dramatic question in every scene, causal (therefore/but) progression instead of
  additive (and then), entering scenes late and leaving early, withheld information,
  active verbs over stative (was/were/there was/began to), and an unresolved chapter
  ending. It also enforces "earn the length" — every paragraph must advance the plot or
  deepen a character, and padding is refocused into story rather than cut, so the
  chapter keeps or grows its length while every word works. Use whenever the user wants
  prose that propels, to fix flat or inert writing, make every sentence excite and pull
  the reader onward, kill filler, or strengthen a chapter's hooks and momentum at the
  line level. Runs on every chapter in the drafting loop and standalone; the generative
  counterpart to momentum-editor (which removes drag). Honors the outline, story bible
  (including the Voice Sample), characters, and prose-style, and never invents plot.
---

# Propulsion Editor

The forward-motion lens that makes a chapter *pull*. It reads one drafted chapter and
rewrites it so every sentence makes the reader need the next, applying the **prose-style
Part 4** propulsion rules line by line. It is the active, generative counterpart to
**momentum-editor**: momentum *removes* what drags, propulsion *adds* the pull. It is built
to run on **every chapter** in the drafting loop, not only the ones that earn a heavy pass.

## What it strengthens

- **A dramatic question in every scene.** Name the question the scene exists to answer,
  open it early, hold it open, and end the scene the moment it closes.
- **Causal, not additive.** Beats connect by *therefore* and *but*, not *and then*. Convert
  and-then chains into cause and effect so each beat is caused by the last.
- **Enter late, leave early.** Cut the throat-clearing opening (waking, arriving, crossing a
  room) and the wind-down after the point lands.
- **Withholding.** Dole out information instead of dumping it; end paragraphs a half-step
  unresolved so the next one is necessary.
- **Active over stative verbs.** Recast *was, were, there was, had been, began to, could
  feel* into a subject doing something.
- **An unresolved chapter ending.** Close on a turn, a reversal, a new threat, a decision
  not yet acted on, or a question, never a tidy reflective summary.
- **Earn the length.** Every paragraph must advance the plot or deepen a character. Padding
  is **refocused into story** (given a job tied to the plot or a character's want/fear), not
  cut to shrink the chapter, so the word count holds or grows while every word works.
- **Sentence-to-sentence pull.** Each line sets up the next; no comfortable mid-scene
  stopping point.

## How it runs

1. **Deterministic flags first** (the scripted half):
   ```bash
   python scripts/propulsion_flags.py <chapter.md | book-folder>
   ```
   It lists stalling/stative constructions, additive "and then" sequencing, sentence-initial
   filler transitions, filter verbs, and the chapter's last sentence. These are *candidates*,
   not verdicts; the script judges surface signals, not whether a passage pulls.
2. **Read for the rest** against the chapter's `outline.json` brief (its dramatic question
   and turn, if named), `story-bible.md` (the plot beats and the **Voice Sample**),
   `characters.json` (the POV character's want and fear), the previous chapter (the live
   voice), and the **prose-style** Part 4 baseline.
3. **Rewrite for pull:** open and hold the dramatic question; convert additive chains to
   causal; cut the windup and the wind-down; recast stative constructions; withhold and dole
   out; end the chapter unresolved. For a paragraph that does not advance, **give it a job**
   rather than deleting it, so the length holds; cut only dead weight that cannot be saved.
4. **Keep the voice and the canon.** Match the Voice Sample, obey prose-style, defer to the
   sources of truth, and never invent plot or a new beat.
5. **Write the stronger version and a change-note** (what pulls harder, what got refocused,
   the rough words added or moved).

## What it writes

Non-destructive. Run standalone or auto-fired in the loop, write
`propulsion/NN-slug.report.md` and `propulsion/NN-slug.edited.md`. **If a clarity-edited
proposal exists** (`clarity/NN-slug.edited.md`), edit *from that* so the clarity fixes carry
through and there is a single proposal to promote. Inside **editor-ensemble**, write
`editors/NN-slug/propulsion.md` and return the change-note instead.

The edit is a **proposal**: promote it over `chapters/NN-slug.md` only on the author's OK, by
**copying** the file with a shell command (`cp` / `Copy-Item`), not the Write/Edit tools, so
promotion does not re-trigger the per-chapter hook.

## Constraints

- **Earn the length, don't cut it.** Preserve or grow the word count (the author's standing
  rule). Refocus padding into story; cut only what is truly irredeemable. Never pad either:
  any added words must advance the story or deepen a character.
- **Never invent plot.** Strengthen the pull of the existing beat; defer to `outline.json` /
  `story-bible.md` / `characters.json` on canon and POV. A structural problem goes to the
  author or **developmental-edit**, not a silent rewrite.
- **Keep the book's voice.** Match the story bible's Voice Sample and obey prose-style;
  strengthen, don't flatten. A distinctive line that *is* the voice stays.
- **Don't sacrifice clarity for speed.** If a propulsion rewrite would muddy meaning, keep it
  clear; clarity and pull are not in tension when the rewrite is done well.

## Relationship to the other skills

- **prose-style (Part 4)** — the propulsion rules this enforces line by line.
- **momentum-editor** — its subtractive sibling: momentum cuts drag and diversions;
  propulsion adds pull and refocuses filler into story. Run both on a heavy chapter;
  propulsion runs on every chapter in the loop.
- **story-editor** — raises what the scene is *for* (purpose, stakes, the turn); propulsion
  makes the prose pull moment to moment. Complementary.
- **chapter-writer** — builds propulsion in at the draft; this enforces and strengthens it
  right after, on every chapter.
- **clarity-edit** — the comprehension pass that runs first in the per-draft loop; propulsion
  edits from its output so both land in one proposal.
- **voice-editor / story-bible Voice Sample** — the voice this preserves while tightening for
  pull.
- **editor-ensemble** — can run it as an additional editor on a high-effort chapter.

## What it is not

Not new-plot generation, not a developmental rewrite, and not a word-count cut. It makes the
chapter's existing beat pull harder, at the same or greater length and in the book's own
voice, and hands structural calls back to the author.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill propulsion-editor --target <book-folder> --status DONE --item "<chapter>" --output "propulsion/NN-slug.edited.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
