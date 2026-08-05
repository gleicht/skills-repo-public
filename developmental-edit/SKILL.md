---
name: developmental-edit
description: >-
  A big-picture structural edit of a drafted book that produces a prioritized revision
  roadmap — the "editorial letter" a developmental editor sends an author. It reads the
  whole manuscript against the outline and story bible and proposes structural changes:
  reorder, cut, merge, or split chapters; expand thin scenes and compress saggy ones;
  strengthen a weak act break, a soft midpoint, or an unearned ending; sharpen stakes,
  momentum, character arcs, and the central promise — written to dev-edit-report.md. Use
  whenever the user wants a developmental or structural edit, an editorial letter, a
  revision plan or roadmap, big-picture feedback on structure/pacing/arcs/stakes, or
  help deciding what to cut, move, or expand. Read-only: it proposes the plan;
  chapter-writer/outline-designer/book-editor execute it. Runs after a full draft,
  before line editing.
---

# Developmental Edit

The structural pass: not the sentences, the *shape*. A developmental edit steps back from
the prose and asks whether the book works as a book — whether the structure holds, the
pacing carries, the arcs land, and the promise of the premise is paid off. Its product is
an **editorial letter and a prioritized revision plan**: the changes worth making, in the
order worth making them. It is **read-only** — it proposes; the author and the writing
skills execute.

Run it on a complete (or near-complete) draft, **before** line editing — there is no
point polishing sentences in a chapter that the revision plan says to cut or move.

## Where it sits, and how it differs from the neighbors

- **review-panel** *diagnoses* by consensus: several readers report the problems they
  agree on. **developmental-edit** is one structural editor who turns problems into a
  **plan** — what to change, why, and in what order. (A panel's report is excellent raw
  material for this letter.)
- **book-editor** executes *line and consistency* fixes. **developmental-edit** works a
  level up, at structure and story, and hands the actual rewriting to **chapter-writer**
  and any restructure to **outline-designer**.
- **story-bible** holds the *intended* beats and arc; this pass judges the draft against
  that intent and proposes how to close the gap.

## What it reads

- **`chapters/*.md`** — the whole manuscript, as a structure.
- **`outline.json`** — the intended chapter plan, to compare against what got written.
- **`story-bible.md`** — plot beats, arc, voice, and (if a mystery) the spoiler-walled
  solution and `clues.md`, so structural advice respects the intended design.
- **`characters.json`** — arcs, wants, and motivations to track across the book.
- Existing **`review-report.md`** / **`fidelity-report.md`** — fold their findings in.

## The developmental lenses

Read the book against each, and turn what's weak into a concrete proposal:

- **Premise & promise.** What the opening promises the reader, and whether the book
  delivers it. The single most important question.
- **Structure & act shape.** Does the book have a clear beginning/middle/end; are the act
  breaks, inciting incident, midpoint, and climax in the right places and strong enough.
- **Pacing & momentum.** Where it drags (a saggy middle, repeated beats, a slow open) and
  where it rushes (a compressed climax, an unearned turn). Name the chapters.
- **Character arcs & motivation.** Does each major arc track and pay off; are motivations
  consistent and sufficient; does anyone go passive.
- **Stakes & tension.** Are the stakes clear, escalating, and personal; does tension build
  or flatten.
- **Scene economy.** Scenes that don't earn their place (cut/merge), scenes that are too
  thin for their weight (expand), and order (reorder for cause-and-effect or tension).
- **POV & tense.** Whether the chosen POV/tense serves the story, and whether it's handled
  consistently.
- **Theme & resonance.** What the book is *about* under the plot, and whether the ending
  lands it.
- **Opening & ending.** The first pages (do they hook on the right thing) and the last
  (is it earned, does it satisfy or cheat).

## The output: `dev-edit-report.md`

Write an **editorial letter**, then a **revision plan**:

```markdown
# Developmental Edit — <Title>

## Overall
A few paragraphs: what's working and must be protected, then the core structural
issue(s) in plain terms.

## Revision plan (prioritized)
1. [STRUCTURE] Move ch.14 before ch.11 so the reveal lands after the setup. — why — owner: outline-designer
2. [PACING]   Compress ch.5-7 (the middle drags); cut the second warehouse scene. — why — owner: chapter-writer
3. [ARC]      Give Tara an active choice in ch.9; she's passive through the act. — why — owner: chapter-writer
... ordered by impact; mark each [STRUCTURE|PACING|ARC|STAKES|SCENE|POV|THEME|OPEN|END]

## Chapter-by-chapter notes
Brief structural note per chapter (keep / cut / expand / move / fix), not line edits.

## What's working
Name the strengths the revision must not break.
```

Lead with the few changes that matter most; a good developmental edit is ruthless about
priority, not a wish list. Then summarize the top moves for the user.

## How it works with the rest

- Propose; **never rewrite the manuscript here.** Hand structural moves to
  **outline-designer**, scene rewrites/expansions to **chapter-writer**, and line work to
  **book-editor** — then, after the revision, the QA gates and **preflight-check** re-run.
- For a series, check the **series-bible** so structural changes keep cross-book setups
  and payoffs intact.

## What it is not

Not a line edit, not a proofread, and not a multi-reader panel. It is one structural
editor's revision roadmap — the plan that tells the author what to change before the
polishing begins.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill developmental-edit --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
