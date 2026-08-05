---
name: story-bible
description: Builds and maintains a Story Bible — a single Markdown reference document (story-bible.md) capturing a project's world rules, narrative voice & style, and plot beats — so Claude keeps continuity and consistent prose across a long book or series. Use whenever the user wants a story bible, world/series bible, or central continuity reference; wants to define worldbuilding rules, a voice & style guide, or plot guardrails; is starting a serious or long-form fiction project; or wants to stop the writing from drifting off-plot, breaking its own rules, or losing its voice. (Characters are handled by the companion character-dossier skill.)
---

# Story Bible

A Story Bible is the **single source of truth** for a long narrative project — the
document Claude re-reads to stay consistent over dozens of chapters written across
many sittings. Worlds contradict themselves, voices drift, and plots sprout twists
nobody asked for. The bible exists to prevent that by writing the project's *laws*
down in one place.

This skill owns three domains — **world, voice, and plot**. The **cast lives in the
companion `character-dossier` skill** (`characters.json`); the bible deliberately
does not duplicate character entries — it points at the dossier instead.

## Where it lives, and how the machine uses it

Write the bible to **`story-bible.md`** in the book project folder, beside
`book.json`, `characters.json`, `outline.json`, and `chapters/`. It's plain Markdown
on purpose: it's meant to be loaded into context as the governing reference for the
writing and editing stages.

When `story-bible.md` exists, **chapter-writer treats it as canon** (world rules,
voice, plot beats) and **book-editor checks every chapter against it** (rule
violations, voice/style drift, off-plot inventions). Character consistency is
checked separately against `characters.json`.

## The core sections

Write the document using this structure. Keep entries concrete and rule-shaped —
the bible is most useful when it states things the writer can be held to.

```markdown
# Story Bible — <Project Title>

## 1. The World Brief
The container for the setting: the rules of the world, the magic/technology
system, history, and geographical lore. Write these as **constraints that must
hold**, not flavor text.
- e.g. "Magic requires physical exhaustion — every spell has a bodily cost."
- e.g. "No faster-than-light travel exists; journeys take in-world months."

## 2. The Voice & Style Guide
How the prose should read, so Claude writes like you:
- **Narrative distance / POV / tense** — e.g. "Third-person limited, past tense."
- **Pacing** — e.g. "Short, punchy sentences during action; longer in reflection."
- **Banned expressions** — words/phrases to never use. e.g. "He sighed," "Suddenly."
- Any diction, motifs, or formatting rules that define the voice.
- **Voice Sample (the most important field).** Two or three paragraphs of prose in
  exactly the voice the book should have, pasted in: the author's own writing, or a
  passage they've approved. The writer and the voice-editor match this sample directly. A
  real sample teaches the voice far better than any description of it; without one, the
  prose drifts toward a generic clean style.
- **Voice fingerprint** — a few concrete notes on what the sample is doing: typical
  sentence length and rhythm, characteristic moves, signature diction, and what the voice
  refuses to do. e.g. "Plain, short declaratives. Dry understatement. No metaphor unless
  it belongs to a character. Never names the emotion."

## 3. Plot Structure & Beats
The major milestones, acts, or beats the story **must** hit, in order. This is the
*law* that keeps the writing from drifting into unintended plotlines or inventing
unnecessary twists. List each beat plainly; mark which are fixed vs. flexible.

## (Extensible) Other sections
Add whatever a given book needs — a timeline, factions/organizations, a glossary or
language notes, key locations, themes, a list of established facts. The bible grows
with the project.

## Cast
Characters are tracked in `characters.json` via the **character-dossier** skill —
see it for names, descriptions, wants, fears, and secrets. (Don't restate the roster
here; just reference it so there's one source of truth.)
```

## Spoilers and the clue ledger (mystery / suspense)

For a mystery, thriller, or any book built on a withheld twist, this skill also owns
two spoiler-sensitive artifacts, kept behind a clear **spoiler wall** so the drafting
stages don't leak the ending:

- **The solution**, recorded in a spoiler-walled section of `story-bible.md` (e.g.
  a `## SOLUTION (author-only)` heading): who did it, the real sequence of events,
  and what every earlier chapter must *not* confirm.
- **`clues.md`** — a fair-play **clue ledger** beside `story-bible.md`. It tracks the
  deniable clues planted for the true answer, the decoy/red-herring trail, and a
  "fairness watch" so every reveal is earned and seeded. Give each clue an id, the
  chapter it lands in, what it really means, and how it stays deniable until the
  reveal.

Both are **author-only**: never surface them in prose, transitions, or a blurb.
`chapter-writer`, `book-editor`, and `chapter-transition` must obey them without
exposing them; **review-panel** reads them for its *informed* reviewers only and
keeps them away from the blind reviewers. Build these only when the book has a twist
to protect; skip them otherwise.

## How to build it — a guided interview

Your job is to **draw this out of the user**, section by section, not to invent a
world and present it as theirs. Run it like a relaxed worldbuilding conversation:

- **Go one section at a time**, and within a section ask grouped, natural questions
  rather than reciting fields. Start with whichever the user has most clearly in
  mind (often the voice or the premise) — order doesn't matter, completeness does.
- **Push for rules, not vibes.** "Magic is mysterious" can't be enforced; "magic
  costs the caster a memory" can. For each world/voice/plot item, nudge toward a
  concrete, checkable statement.
- **Pin down the Voice & Style Guide explicitly** — POV, tense, pacing, and a real
  banned-expressions list. Above all, **get a Voice Sample**: ask the user for two or
  three paragraphs in the target voice (their own writing or an approved passage), and if
  they have none, draft a short sample, get it approved, and record that. Then note its
  fingerprint. The sample is what actually makes the prose sound like the user's; a
  described voice with no sample is the main reason generated prose comes out generic.
- **Treat the Plot Beats as the spine** the outline will later have to deliver.
- **Never block on a blank.** Unknown is fine; leave it and move on. A partial bible
  is useful immediately and fills in as the project develops.
- **Offer to draft, with approval.** It's welcome to *propose* a world rule, a voice
  guideline, or a plot beat for the user to accept, tweak, or reject — suggest,
  don't impose. What the user confirms is canon.

If the project clearly has characters and there's no `characters.json` yet, point
the user to the **character-dossier** skill to build the cast — don't capture
characters here.

After writing (or updating) `story-bible.md`, show the user a short recap of each
section so they can correct it. Support partial runs: "tighten the voice guide,"
"add a faction," "what are the plot beats again?" → edit just that part of the file.

## Relationship to the other skills

- **character-dossier / `characters.json`.** The canonical home for the cast,
  including each character's want, fear, and secret. The Story Bible references it
  and never duplicates character entries.
- **outline-designer / `outline.json`.** The Plot Structure & Beats section is the
  *intent and rules*; `outline.json` is the concrete chapter breakdown. Build the
  outline to satisfy the beats.
- **book.json `tone`.** The Voice & Style Guide is the detailed expansion of it.
- **prose-style skill.** The user's house style (no em dashes, no AI-isms,
  show-don't-tell, complete-sentence narration, grade 9–12) is the always-on
  baseline for *all* their prose. This book's Voice & Style Guide layers
  project-specific flavor on top of it; it doesn't replace it.

## Maintenance

A bible is only useful if it stays true. As the story develops, keep it current —
new world rules, refined voice notes, adjusted beats. When the plot changes, update
the beats so the writer and editor are held to the *current* plan, not the old one.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill story-bible --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
