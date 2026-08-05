---
name: review-panel
description: >-
  A final pre-publish sanity check: a panel of several independent reviewers each reads
  the WHOLE manuscript the way human editors and beta readers would, and the skill
  reports the problems they agree on, ranked by how many reviewers raised each, with a
  READY / NOT-READY verdict. Reviewers flag plot gaps, logic holes, weak or unfair
  twists, continuity errors, character inconsistencies, pacing problems, and
  spelling/grammar. Read-only — it writes review-report.md and never edits the
  manuscript. Use whenever the user wants a final review, a whole-book or beta-reader or
  editorial-panel pass, a pre-publish gate, or to find plot holes and proofread before
  publishing. Distinct from fidelity-review (audits against the plan) and book-editor
  (which fixes).
---

# Review Panel

The last gate before a book is published. You convene a panel of independent
reviewers, each of whom reads the **whole manuscript** the way a sharp human editor
or beta reader would, and you report back the problems the panel **agrees** on. The
core idea: when several readers who never compared notes all flag the same spot, that
spot is almost certainly a real problem. A lone flag is "worth a look."

This skill is **read-only**. It produces a report and a verdict; it never edits the
manuscript. Fixing is the **book-editor**'s job; checking the book against its own
plan is **fidelity-review**'s job. This skill answers a different question: *does the
story actually work for a reader, and is it clean enough to publish?*

## Inputs

Read from the book project folder (default: current directory, or ask):

- **`chapters/*.md`** — the whole manuscript, in order. Required.
- **`book.json`** — title, audience, tone. The bar the book is judged against.
- **`story-bible.md`**, **`characters.json`**, **`research.md`** — reference for the
  *informed* reviewers and the continuity/fact checks.
- **`clues.md`** and any spoiler-walled sections (e.g. story-bible "SOLUTION") — the
  **intended twists and their planned setups**. These go ONLY to the *informed*
  reviewers. **Blind reviewers must never see them** (see the split below).
- **`transitions/`** — if present, include approved transitions in the read.

## The panel (hybrid: 5–6 reviewers, run concurrently)

Compose a panel of generalists (for the consensus signal) plus a couple of
specialists (for depth). Default panel of six; drop one generalist for a short book.

**Generalists — the consensus cohort (4).** Each does the *same* comprehensive read,
independently, and reports across every category below. Their overlap is the signal.
Split them by knowledge:
- **2 blind generalists** — given only the manuscript and the neutral spec (tone,
  audience). No `clues.md`, no solution, no spoiler-walled beats. They report the
  *cold-reader experience*: where it confuses, drags, or feels cheap; whether twists
  land or come from nowhere.
- **2 informed generalists** — given the manuscript **plus** the intended twists and
  their planned setups (`clues.md`, the solution). They judge *construction and
  fair-play*: is each reveal earned, are the clues fairly seeded, does anything
  contradict the intended design.

**Specialists — coverage, not consensus (2).**
- **Line specialist** — a close spelling/grammar/usage/punctuation/typo pass over the
  whole book. Reports a line-level list (chapter + quote + fix). Applies the
  **prose-style** baseline (flag em dashes, AI-isms, stock phrases) but does not
  rewrite.
- **Continuity specialist** — timeline, names, ages, objects, geography, and
  who-knows-what-when across the whole book, checked against `story-bible.md`,
  `characters.json`, and `clues.md`. Informed.

**Independence is the point.** Each reviewer works without seeing any other's
findings, so agreement actually means something. Launch them as **parallel
subagents — issue all reviewer calls in a single message** so they run at once, each
given only the inputs it is allowed to see. Wait for all, then synthesize. (For a
very long book, run the panel via the Workflow tool for robust fan-out, and/or have
each reviewer chunk the manuscript; say so in the report if you do.)

## What each generalist looks for (the human-reviewer lens)

- **Plot gaps & logic holes** — unanswered questions, events that don't follow,
  characters knowing things they couldn't, conveniences that strain belief.
- **Twists, setups & payoffs** — does each turn land? Informed reviewers judge whether
  it's fairly seeded; blind reviewers report whether it feels earned or cheap.
- **Continuity & consistency** — facts, timeline, objects, places that disagree across
  chapters.
- **Character** — consistent voice and behavior; motivations that hold; arcs that track.
- **Pacing & structure** — drag, rushed beats, weak chapter openings/closings, a
  saggy middle, an unearned ending.
- **Voice & prose** — clichés, AI-isms, tonal slips, repetition (against `book.json`
  tone and the prose-style baseline).
- **Spelling & grammar** — anything that would embarrass the book in print.
- **The reader's verdict** — anywhere a reader would feel confused, bored, or cheated.

## Each reviewer returns structured findings

Have every reviewer return, for the whole book:
- A list of **findings**, each: `{ chapter, anchor (a short quote or location),
  category, severity (blocker | major | minor | nit), issue, suggestion }`. The
  `suggestion` is a direction, not a rewrite.
- A one-line **overall impression** and that reviewer's **verdict** (ready /
  not-ready) with the reason.

Keep findings concrete and located (a quote or chapter:beat), so the synthesis can
tell when two reviewers are pointing at the same thing.

## Synthesis — the consensus step

You (or a final synthesis agent) collect every reviewer's findings and:

1. **Cluster** findings that point at the same problem (same location/topic), counting
   how many **generalists** independently raised each. (Specialist findings add
   coverage; the consensus count is among the 4 generalists, the comparable cohort.)
2. **Rank by agreement:**
   - **Consensus issues** — raised by a majority of generalists (≥3 of 4). High
     confidence; lead with these.
   - **Corroborated** — raised by 2. Likely real.
   - **Singletons** — one reviewer, but kept if severe or specific.
3. **Read the blind/informed split:** when **blind** reviewers report confusion at a
   spot the **informed** reviewers know is an intentional setup, that is not a false
   positive — it means the setup may be too obscure or mistimed. Flag it as "setup
   needs tuning," not "plot hole." When informed reviewers find an unfair or
   unseeded reveal that blind reviewers didn't notice, that is a construction problem
   to fix before publishing.
4. **Fold in the specialists:** the continuity list and the line-level
   spelling/grammar list as their own sections.

## The report: `review-report.md`

Write a single report to the project folder:

- **Verdict** — **READY** or **NOT READY** to publish, in one line, with the blocking
  issues named. NOT READY if any *blocker* survives (a real plot hole, an unfair/
  unseeded twist, a hard continuity contradiction), especially by consensus.
- **Consensus issues** — ranked, each with: the problem, where, severity, and **how
  many reviewers flagged it** (and which kinds — blind/informed).
- **By category** — plot/logic, twists & fair-play, continuity, character, pacing,
  voice/prose.
- **Line-level pass** — the spelling/grammar/usage list from the line specialist.
- **Per-reviewer verdicts & impressions** — so the author can see the spread, not just
  the merge.
- **What the panel agreed is working** — a short note on strengths (a good review names
  what not to break).

Then summarize the verdict and the top issues to the user. **Never edit the
chapters.** Hand confirmed issues to **book-editor** (craft fixes) or back to the
author; re-run the panel after fixes for a clean final gate.

## Principles

- **Agreement is the signal.** The value is independent reviewers converging. Protect
  their independence; never let one reviewer's findings leak into another's read.
- **Keep blind reviewers blind.** The cold-reader experience is only meaningful if they
  truly don't know the twists. Guard the spoiler inputs.
- **Diagnose, don't fix.** Read-only. Produce the report; let the editor or author act.
- **Concrete and located.** Every finding needs a place and a quote, or it can't be
  clustered or acted on.
- **Scale to the book and say so.** Six full reads is heavy; this is an occasional
  final gate, not a per-chapter step. For a long book, note in the report if reviewers
  chunked or if the panel was run via a workflow, and never silently sample without
  saying so.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill review-panel --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
