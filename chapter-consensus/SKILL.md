---
name: chapter-consensus
description: >-
  Drafts one chapter several ways in parallel, then merges the best of each into a
  single chapter. By default it fans out SIX chapter-writers at once, one per lens
  (interiority, pacing, dialogue, sensory, restraint, hook), all obeying the same
  outline, story bible, characters, and prose-style; then it synthesizes one coherent
  chapter in the book's voice and hands it to clarity-edit. Use whenever the user wants
  best-of-N or ensemble drafting, multiple parallel drafts of a chapter, to write a
  chapter a few ways and combine the strongest parts, a consensus or merge of drafts, or
  a higher-effort pass on an important chapter. Non-destructive: drafts and the merge go
  in a consensus/ folder; the merge is promoted to chapters/ only on approval.
---

# Chapter Consensus

A higher-effort way to draft a chapter that matters: write it **N ways in parallel**
(default **6 — all six lenses at once**), each draft pushed toward a different strength,
then **merge the best of each** into one chapter that is stronger on every axis than any
single draft. The merged chapter then goes to **clarity-edit** like any freshly drafted
chapter.

It is an alternative to the single **chapter-writer** pass — use it when a chapter is
worth 6× the drafting cost (an opener, a pivotal scene, a climax), not for every chapter.

## Why lenses (the whole point)

If all N writers get the identical prompt, the drafts converge and the merge has nothing
to choose between. So each parallel writer gets the **same brief plus one lens** — a
deliberate emphasis — so the drafts come back with genuinely different strengths.

**A lens changes *how* the chapter is rendered, never *what happens*.** Every draft obeys
the same outline beats, the story bible, the characters, the POV, and the prose-style
house rules. The lens is emphasis only; it never alters plot, canon, or POV (that would
make the drafts impossible to merge).

### Lens library
- **interiority** — the POV character's inner experience, emotional logic, what they notice.
- **pacing** — scene structure and momentum; compress the slow, build the tension.
- **dialogue** — distinct character voices and subtext; what's left unsaid.
- **sensory** — concrete physical grounding, true to the world and era; no anachronisms.
- **restraint** — spare, show-don't-tell, trust the reader; let image and silence carry.
- **hook** — the strongest possible chapter opening and closing.

**Default (N=6):** run **all six lenses at once** — the full sweep, maximum coverage and
the richest merge. This is the standard run.

To spend less on a routine higher-effort pass, narrow to a three-lens subset chosen for
the scene:
- action / suspense → `pacing`, `sensory`, `dialogue`
- quiet / interior → `interiority`, `restraint`, `dialogue`
- chapter opener or finale → `hook`, `interiority`, `pacing`

Tell the skill the lenses you want, or let it run all six; it states which it used.

## How it runs

1. **Gather the brief** the writers share: the `outline.json` entry for the chapter, the
   `story-bible.md`, `characters.json`, the previous chapter (for continuity), and the
   `prose-style` baseline. Identical for all N.
2. **Fan out N=6 chapter-writers in parallel.** Spawn them as **parallel subagents in a
   single message** so they run concurrently — each is told to write the chapter with the
   chapter-writer skill, given the shared brief plus **one lens** (one writer per lens in
   the set). (Concurrency is capped around `min(16, CPU cores − 2)`; on a typical
   multi-core machine all six run at once, and on a small machine the extra writers queue
   and start as slots free. For guaranteed parallel fan-out, run it via the **Workflow**
   tool instead.)
3. **Collect the drafts** into `consensus/NN-slug/draft-K-<lens>.md`.
4. **Merge — synthesize, don't staple.** Read all N against the brief. Take the strongest
   opening, structure, beats, dialogue, and lines, and **rewrite them into one coherent
   chapter in the book's voice** — harmonize the seams so it reads as one author, not a
   patchwork. Obey prose-style. Where drafts conflict on facts, defer to
   `outline.json` / `story-bible.md` / `characters.json` (and flag a real conflict rather
   than guessing). Never invent plot beyond the brief.
5. **Write the result and a report**, then hand off (see below).

## What it writes

Non-destructive, in a `consensus/` folder beside `chapters/`:

```
consensus/
└── NN-slug/
    ├── draft-1-interiority.md
    ├── draft-2-pacing.md
    ├── draft-3-dialogue.md
    ├── draft-4-sensory.md
    ├── draft-5-restraint.md
    ├── draft-6-hook.md
    ├── merged.md            # the consensus chapter (the deliverable)
    └── consensus-report.md  # lenses used + what each draft contributed
```

- **`consensus-report.md`** notes the lenses, a one-line strength of each draft, and which
  draft each major element of the merge came from, so the choices are on the record.
- **`merged.md` is a proposal.** On the author's OK, **promote it to `chapters/NN-slug.md`**
  (which triggers the per-chapter pipeline — clarity-edit then fidelity-review — via the
  chapters-write hook). Do not overwrite an existing chapter without that OK.

## Cost and when to use it

It costs about **N× the drafting tokens** (6× by default — one full draft per lens), so
reserve it for chapters that earn it: openers, pivotal scenes, climaxes. N=6 is the
maximum-coverage setting; the six lenses are deliberately distinct, so the merge has
genuinely different strengths to choose from rather than near-duplicate drafts. For a
cheaper higher-effort pass, drop to a three-lens subset (above).

## Relationship to the other skills

- **chapter-writer** — the drafter this runs N copies of, one per lens. For ordinary
  chapters, use chapter-writer alone; use chapter-consensus for the ones that matter.
- **clarity-edit** — receives the promoted merge as the chapter's first cleanup.
- **prose-style / story-bible / character-dossier** — the canon and voice every draft and
  the merge obey; lenses never override them.
- **book-machine** — an optional, higher-effort substitute for the single chapter-writer
  step in the Draft stage.

## What it is not

Not a way to generate ten near-identical drafts and bolt them together. The value is
*diverse* drafts and a *harmonized* merge, in voice and on canon — not a patchwork, and
never new plot the brief didn't call for.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill chapter-consensus --target <book-folder> --status <DONE|verdict> --item "<chapter + the N lenses>" --output "consensus/NN-slug/merged.md" --note "<one-line summary>"`

Use `DONE` for a completed merge. `--item` is the chapter and the lenses used; `--output`
is the merge and report written. Full convention: `lib/AUDIT-LOG.md`.
