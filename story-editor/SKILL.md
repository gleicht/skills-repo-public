---
name: story-editor
description: An active per-chapter story-quality editor. It reads a drafted chapter and rewrites it stronger as a story beat — sharpening the scene's purpose, the stakes, tension and escalation, the turn, cause-and-effect logic, and emotional payoff — so the chapter does a real job and lands. Unlike the read-only diagnostics, it edits, writing a stronger version as a proposal. Use whenever the user wants to strengthen story quality, raise stakes or tension, fix a scene that does not do anything or feels flat, or sharpen a chapter's turn or emotional impact. One of the five editors in the editor-ensemble per-chapter polish; honors the outline, story bible, characters, and prose-style, and never invents new plot.
---

# Story Editor

The story-quality lens of the per-chapter editor panel. It reads one drafted chapter and
**rewrites it stronger as a story beat** — not new plot, but the existing beat made to do
its job and land. It is an *active* editor (it produces an improved chapter), the
strengthening cousin of the read-only **review-panel** and **developmental-edit**.

## What it strengthens

- **Scene purpose.** Every chapter must do a job: advance the plot, change a character,
  or (ideally) both. Find the job and sharpen it; if a scene only marks time, give it one.
- **Stakes.** Make clear what is at risk and why it matters to the POV character now.
  Raise or clarify stakes that are vague or absent.
- **Tension and escalation.** Locate the source of tension and make it build. The chapter
  should end in a more pressured place than it began.
- **The turn.** A scene should turn — a change in value or state from open to close
  (safe→threatened, hopeful→cornered, ignorant→knowing). Strengthen a weak or missing turn.
- **Cause and effect.** Events should follow causally, not as a list. Tie beats to the
  decisions and consequences that drive them; cut "and then" sequencing.
- **Emotional payoff.** Engage the POV character's want and fear (per characters.json) so
  the beat lands emotionally, not just informationally.
- **Entrance and exit.** Open near the friction and end on a beat that pulls the reader on.

## How it runs

1. Read the chapter, its `outline.json` entry (the beats it must hit), `story-bible.md`
   (plot beats, world, voice), `characters.json` (the POV character's want/fear/arc), the
   previous chapter (for setup carried in), and the **prose-style** baseline.
2. Edit the chapter to strengthen the axes above — deepen stakes, sharpen the turn, tie
   cause to effect, land the emotional beat — **without changing what happens.** The
   outline's beats, the canon, and the POV all stay; you make them hit harder.
3. Write the stronger version and a short change-note (what you strengthened and where).

## What it writes

Non-destructive. When run inside **editor-ensemble**, write to
`editors/NN-slug/story.md` and return the change-note for the merge. Run standalone, write
`editors/NN-slug/story.md` plus a one-paragraph note; promote only on the author's OK
(copy over `chapters/NN-slug.md`).

## Constraints

- **Never invent plot** beyond the outline brief, and never add a twist the book did not
  call for. Strengthen the existing beat; do not write a different one.
- **Defer to the sources of truth** on facts, canon, and POV (`outline.json`,
  `story-bible.md`, `characters.json`). If the chapter must contradict them to be stronger,
  that is a structural call for the author or **developmental-edit**, not a silent rewrite.
- **Keep the author's voice** and obey **prose-style**. Strengthen, do not flatten.

## Relationship to the other skills

- **editor-ensemble** — runs this as one of five parallel editors and merges its gains.
- **developmental-edit / review-panel** — diagnose structure across the whole book;
  story-editor applies the fix to one chapter.
- **momentum-editor** — its sibling: momentum cuts what drags and diverts; story-editor
  raises what the scene is *for*. They are complementary and the merge reconciles them.
- **outline-designer / story-bible** — own the plot; this lens never overrides them.

## What it is not

Not a developmental rewrite and not new-plot generation. It makes the chapter's own beat
stronger, on canon and in voice, and hands structural calls back to the author.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill story-editor --target <book-folder> --status DONE --item "<chapter>" --output "editors/NN-slug/story.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
