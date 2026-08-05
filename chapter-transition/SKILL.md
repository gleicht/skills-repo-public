---
name: chapter-transition
description: Proposes optional, non-destructive connective passages between adjacent chapters — a "bridge" that smooths a time jump, location change, POV switch, tonal shift, or dangling thread, anywhere from a one-line dateline to roughly 1000 words, or nothing at all when a hard cut serves the book better. Writes each proposal into a transitions/ folder for the user to keep, edit, or remove, and never edits the chapter files themselves. Use whenever the user wants transitions, bridges, interstitials, or connective tissue between chapters, wants to ease the seams between chapters without rewriting them, or asks whether the gap between two chapters needs a bridge. Defaults to no transition unless one genuinely earns its place. (For smoothing a chapter's own opening or closing in place, use the book-editor skill instead.)
---

# Chapter Transition

Decide, seam by seam, whether the move from one chapter to the next needs help,
and when it does, write a short connective passage that carries the reader across.
The work is **additive and non-destructive**: you never touch the chapter files.
Each transition lives in its own file in a `transitions/` folder, clearly marked,
so the user can keep it, edit it, or delete it without disturbing the manuscript.

## The first rule: default to silence

Most chapter breaks need nothing. A hard cut is a deliberate, powerful device,
especially in suspense, comedy, and any book with momentum. A transition at every
seam turns a book into mush. So your **default decision is "none."** Propose a
bridge only when there is a real continuity problem the reader would otherwise
stumble over. When in doubt, leave the gap alone and say so.

A transition has to *earn its place* by solving one of these seam problems:

- **Time jump** — hours, days, or years pass between chapters and the next chapter
  doesn't orient the reader on its own.
- **Location change** — the story moves somewhere new without a handhold.
- **POV / narrator switch** — the next chapter changes whose head we're in, and the
  shift would jar without a beat to reset.
- **Dangling thread** — chapter N ends mid-tension and chapter N+1 leaves the reader
  wondering what happened in between, in a way that confuses rather than intrigues.
- **Tonal whiplash** — a hard swing in register (a death, then a farce) that needs a
  breath.

If the next chapter already orients the reader in its first lines (a dateline, "By
eight o'clock…", a clear new scene), it usually needs **no** transition. Say so.

## Inputs

Read from the book project folder (default: current directory, or ask):

- **`chapters/*.md`** — the drafted chapters, in order. Required. You judge the
  **seam** between each adjacent pair: the last beats of chapter N and the opening
  of chapter N+1.
- **`outline.json`** — chapter order, titles, and briefs. The authority for which
  chapters are adjacent and what each is meant to do.
- **`book.json`** — title, author, audience, tone. Transitions must match this tone.
- **`story-bible.md`** — if present, the governing reference for world rules, the
  Voice & Style Guide, and plot beats. A transition must obey the bible and must
  never reveal a beat earlier than the plot intends.
- **`characters.json`** — if present, the cast dossier. Keep names, voice, and
  `continuityNotes` consistent; never let a transition expose a character's `secret`
  ahead of the plot.
- **`fidelity-report.md`** / any spoiler-walled notes — respect them. A transition
  must not leak anything the manuscript is deliberately withholding.

## How to run the pass

1. **Read the whole book in order first.** You can only judge a seam with both
   chapters in your head, and only judge the set with the whole arc in mind.
2. **For each adjacent pair, decide the seam.** One of three calls:
   - **none** — the cut works; nothing to add.
   - **brief** — one or two paragraphs (or a non-prose marker: a dateline like
     "Three weeks later." or a section ornament) is enough.
   - **bridge** — a fuller passage, up to roughly 800–1000 words, when a real gap of
     time, place, or knowledge needs to be crossed with actual scene or summary.
   Never pad to reach a length. The right length is the shortest that solves the
   problem.
3. **Choose how it should appear** (record it; the packager will honor it later):
   - **seamless** — reads as connective prose flowing straight into the next
     chapter, with no visible marker.
   - **set-off** — visibly distinct from chapter prose (a scene-break ornament or
     italics) so the reader registers it as a bridge.
   Pick per transition based on what the moment wants, and mark which.
4. **Write it in the book's voice.** Draft every transition to match the `book.json`
   tone, the story bible's Voice & Style Guide, and the surrounding chapters, under
   the house **prose-style** baseline (no em dashes, complete-sentence narration,
   no AI-isms, show don't tell). Write in-voice drafts even for manuscripts the user
   wrote themselves; the user keeps, edits, or deletes each one.
5. **Write the files** (see contract below) and **report for approval** (see below).
   Nothing is final until the user says so.

## The `transitions/` contract

Additive only. The chapter files are never modified.

```
<book-folder>/
└── transitions/
    ├── transitions.json    # the index: one entry per seam, with the decision + rationale
    ├── 01-02.md            # the transition prose between chapter 01 and chapter 02 (omit if "none")
    └── 03-04.md
```

Transition prose files are named `<afterId>-<beforeId>.md` and contain only the
passage itself (plain paragraphs, `*italics*` allowed). A file exists only when the
decision is `brief` or `bridge`; a `none` decision is recorded in the index with no
file.

**`transitions.json`**
```json
{
  "transitions": [
    {
      "gap": "01-02",
      "after": "01",
      "before": "02",
      "decision": "none | brief | bridge",
      "appearance": "seamless | set-off | n/a",
      "words": 0,
      "status": "proposed | approved | declined",
      "rationale": "the seam problem this solves (time jump, POV switch, ...) — or why none is needed"
    }
  ]
}
```

## Reporting for approval

After the pass, give the user a single compact table covering **every** seam, so
they see your judgment on the whole book at once:

| Seam | Decision | Length | Appearance | Why |
|------|----------|--------|------------|-----|
| Ch1 → Ch2 | none | — | — | Ch2 self-orients at the blue gate; a hard cut is cleaner. |
| Ch3 → Ch4 | brief | ~2 paras | set-off | POV shifts to Kelsey; a beat resets the reader. |

Then, for each proposed transition, show the draft prose so the user can read it in
place. Make the three options explicit and easy:

- **Keep** it as written (set `status` to `approved`).
- **Edit** it — they tell you the change, you revise the file.
- **Remove** it entirely — delete the file and set `status` to `declined` (or back to
  `none`). Removing a transition never touches the chapters.

## Principles

- **Non-destructive, always.** Transitions are separate files. The manuscript is
  never edited by this skill. (If a seam's real fix is editing a chapter's own
  opening or closing, that is the **book-editor**'s job, not this one. Say so and
  hand it off.)
- **Earn every word.** Bias hard toward "none." A book is not improved by connective
  tissue it didn't need.
- **Match the voice, don't invent the story.** A transition summarizes or bridges
  what the chapters imply; it never introduces new plot, new facts, or a reveal the
  book is saving. Obey the story bible, the dossier, and any spoiler-walled notes.
- **The user decides.** You propose and draft; the user keeps, edits, or removes.
  Default state is `proposed`, never silently `approved`.
- **Rendering (wired into the packagers).** This skill produces and maintains the
  `transitions/` folder for review. The **epub-packager** and **docx-packager** read
  `transitions/transitions.json` and render every transition whose `status` is
  `approved` after its `after` chapter: **seamless** as plain connective prose closing
  out that chapter, **set-off** with a centered `· · ·` ornament and italics. Anything
  still `proposed`, `declined`, or `none` renders nothing. So **approving a transition
  is what makes it appear in the next build**; until then it is review-only.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill chapter-transition --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
