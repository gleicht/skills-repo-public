---
name: editor-ensemble
description: Runs a panel of active story editors over one chapter in parallel, then merges the best edit from each into a single stronger chapter. It fans out five editors at once — story, continuity, dialogue, momentum, and voice — each producing its own improved version of the same chapter, then synthesizes one final chapter that takes the strongest change from each, in the book's voice and on canon. Non-destructive: every editor's version and the merge go in an editors/ folder, and the merge is promoted to chapters/ only on approval. It is the editing counterpart of chapter-consensus (which is for drafting). Use whenever the user wants an ensemble or best-of edit of a chapter, to run all the story editors at once and combine their work, or a high-effort polish that needs little manual cleanup. Run it deliberately on the chapters that earn the extra cost (openers, pivotal scenes, climaxes); it is opt-in, not automatic.
---

# Editor Ensemble

A high-effort way to edit a chapter so it needs little manual cleanup: run **five active
editors over the same chapter in parallel**, each making it stronger on one axis, then
**merge the best change from each** into one chapter that is stronger on every axis than any
single editor's version.

It is the editing counterpart of **chapter-consensus** (which drafts a chapter N ways and
merges). Chapter-consensus fans out *writers*; editor-ensemble fans out *editors* over an
already-drafted chapter.

## The five editors

Each is its own skill, run as a parallel subagent over the same chapter and the same
sources of truth:

- **story-editor** — scene purpose, stakes, tension, the turn, cause-and-effect, payoff.
- **continuity-editor** — fixes drift vs the bible, characters, prior chapters, book.json.
- **dialogue-editor** — distinct voices, subtext, conflict; cuts boring or on-the-nose talk.
- **momentum-editor** — tightens slow spots; cuts or refocuses diversions that go nowhere.
- **voice-editor** — holds the book's constant voice and the prose-style house rules.

They overlap by design at the edges; the merge is where their gains are combined and any
conflicts resolved.

## How it runs

1. **Gather the shared inputs**, identical for all five: the chapter file, its
   `outline.json` entry (the beats it must hit), `story-bible.md`, `characters.json`, the
   previous chapter (continuity and established voice), and the **prose-style** baseline.
2. **Fan out the five editors in parallel** — spawn them as **subagents in a single
   message** so they run concurrently. Each is told to apply its editor skill to the
   chapter, write its improved version to `editors/NN-slug/<editor>.md`, and return a
   concise **change-note** (what it changed and where). (Concurrency is capped near
   `min(16, cores − 2)`; for guaranteed fan-out, run via the **Workflow** tool.)
3. **Collect** the five versions and their change-notes.
4. **Synthesize — merge, don't staple.** Read the **original** chapter plus all five edited
   versions and their change-notes, against the sources of truth. Build **one** final
   chapter that takes the strongest change from each editor: story-editor's sharper stakes
   and turn, dialogue-editor's better lines, momentum-editor's cuts and tightening,
   continuity-editor's fixes, voice-editor's consistency. **Resolve conflicts** where two
   editors touched the same text (for example, if momentum cut a line dialogue sharpened,
   keep it only if it earns its place). Harmonize the seams so it reads as one author in the
   **book's voice**, obey prose-style, defer to `outline.json` / `story-bible.md` /
   `characters.json` on any fact, and **never invent plot** the brief did not call for.
   **Voice discipline (this is where merges go wrong).** A merge averages unless you stop
   it. Hold one dominant voice — the draft's, as tuned by voice-editor against the story
   bible's Voice Sample — and take a change from another editor only when it fixes something
   clearly broken (a flat stake, a dead line, a real drag, a continuity error), never a
   lateral rephrase that only swaps one set of words for another. When in doubt, keep the
   original line. The result should read like the author's own tighter draft, not like five
   editors voting on every sentence.
5. **Write the merge and the report**, then hand off (below).

## What it writes

Non-destructive, in an `editors/` folder beside `chapters/`:

```
editors/
└── NN-slug/
    ├── story.md
    ├── continuity.md
    ├── dialogue.md
    ├── momentum.md
    ├── voice.md
    ├── merged.md          # the ensemble chapter (the deliverable)
    └── editor-report.md   # what each editor changed + which gains the merge took, conflicts resolved
```

- **`editor-report.md`** lists each editor's headline changes, which of them the merge kept,
  and how conflicts were resolved, so every choice is on the record.
- **`merged.md` is a proposal.** On the author's OK, **promote it to `chapters/NN-slug.md`
  by copying the file with a shell command** (`cp` / `Copy-Item`), not the Write/Edit tools,
  so promotion does not re-trigger the per-chapter hook. Do not overwrite a chapter without
  that OK. Surface a short summary and any author-flagged items (continuity gaps,
  load-bearing passages momentum was unsure about).

## When to run it (opt-in, not automatic)

Run this **by hand on the chapters that earn it** — openers, pivotal scenes, climaxes — not
on every chapter. It used to auto-fire on every fresh draft via the `PostToolUse` hook, but
running a five-editor merge on every chapter averaged the prose toward a flat, slightly-off
voice, so the hook now fires the lighter **clarity-edit** on a draft instead. Invoke
editor-ensemble deliberately when a chapter is worth the 5× cost and the hand-cleanup it
saves. Because the editors write to `editors/` (not `chapters/`) and promotion is a shell
copy, a run never re-triggers the hook.

## Cost and when to use it

It costs about **5× an edit pass per chapter** (one full edit per editor) plus the merge.
Because it is opt-in rather than automatic, that spend lands only on the chapters you
choose, which is the point: pay 5× only where it buys a chapter that needs little
hand-editing. To spend less on a chapter you do run it on, use a subset
(for example story + momentum + voice) and say so in the report.

## Relationship to the other skills

- **chapter-consensus** — the drafting analogue (N writers → merge); editor-ensemble is the
  editing analogue (N editors → merge). Consensus drafts a chapter, ensemble polishes it.
- **chapter-writer** — drafts the chapter the ensemble then edits; run the ensemble by hand
  on a finished draft when the chapter is worth it (the draft hook fires only the lighter
  clarity-edit).
- **clarity-edit / fidelity-review** — the lighter per-tweak checks the ensemble subsumes on
  a full draft (continuity-editor covers continuity; the merge clarifies).
- **book-editor / review-panel** — the later whole-book polish and gate; the ensemble makes
  each chapter strong first so they find less to do.
- **prose-style / story-bible / character-dossier / outline-designer** — the voice and canon
  every editor and the merge obey; the editors never override them.

## What it is not

Not a way to run five near-identical edits and bolt them together, and not new-plot
generation. The value is *diverse* editorial gains and a *harmonized* merge, in the book's
voice and on canon. Promotion is always the author's call.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill editor-ensemble --target <book-folder> --status DONE --item "<chapter + the five editors>" --output "editors/NN-slug/merged.md" --note "<one-line summary>"`

Use `DONE` for a completed merge. Full convention: `lib/AUDIT-LOG.md`.
