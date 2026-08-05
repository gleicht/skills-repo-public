---
name: momentum-editor
description: An active per-chapter momentum editor. It finds and fixes the two things that kill forward motion — slow, boring, saggy spots (it tightens, compresses, and energizes them) and diversions that do not advance the plot or develop a character (it cuts or refocuses them). The test for every passage is whether it moves the story or deepens a character; if it does neither, it goes or earns its place. Use whenever the user wants to fix pacing, cut boring or slow or draggy parts, remove tangents, filler, or scenes that go nowhere, tighten a chapter, or keep the story moving. Honors the outline so required beats stay, obeys prose-style, and cuts dead weight rather than essential plot.
---

# Momentum Editor

The forward-motion lens of the per-chapter editor panel. It hunts the two things that make
a reader skim or set the book down, and fixes both **in place**:

1. **Slow / boring / saggy spots** — passages that drag, over-described setting, repetition,
   throat-clearing openings, a scene that idles before it starts, a beat held too long.
2. **Diversions** — tangents, asides, or mini-scenes that do not advance the plot or develop
   a character. The interesting-but-pointless detour is still a detour.

## The one test

For every paragraph: **does it move the story or deepen a character?** If it does neither,
it gets tightened, refocused, or cut. Nothing rides along for free.

## What it does

- **Tighten the slow.** Compress over-long description and stage business; cut repetition and
  filler; trim the windup so the scene starts where the friction is; speed a passage that
  lingers past its point. Energize flat stretches with concrete, moving detail.
- **Cut or refocus diversions.** Remove a passage that goes nowhere; or, if it is worth
  keeping, give it a job — tie it to the plot or to a character's want/fear so it earns its
  place. Refocus a wandering scene back onto its through-line.
- **Protect the spine.** Keep the chapter's required beats and necessary setup; momentum is
  about removing what does *not* belong, never the load-bearing parts.

## How it runs

1. Read the chapter against its `outline.json` brief (the beats that must stay),
   `story-bible.md`, `characters.json`, and the **prose-style** baseline.
2. Edit for motion: tighten saggy prose, cut dead weight, remove or refocus diversions,
   strengthen the through-line so the chapter keeps pulling forward.
3. Write the tightened version and a change-note (what was cut/compressed/refocused, and the
   rough words removed), so the author can see exactly what left and why.

## What it writes

Non-destructive. Inside **editor-ensemble**, write `editors/NN-slug/momentum.md` and return
the change-note. Standalone, write the same file plus the note; promote on the author's OK
(copy over `chapters/NN-slug.md`).

## Constraints

- **Never cut a required beat or necessary setup.** If a passage feels slow but the outline
  or story bible needs it, keep it and make it move instead of removing it. When unsure
  whether something is load-bearing, flag it rather than cutting blind.
- **Cutting removes non-advancing material, not plot.** Don't change what happens; remove
  what doesn't matter and tighten the rest.
- **Keep the voice.** Tighter, not flatter; obey prose-style.

## Relationship to the other skills

- **developmental-edit** — diagnoses saggy or rushed structure across the whole book;
  momentum-editor fixes pace and cuts diversions inside one chapter.
- **story-editor** — its sibling: story-editor raises what a scene is *for*; momentum-editor
  removes what drags or wanders. The merge reconciles a cut against a strengthened beat.
- **propulsion-editor** — its generative opposite: momentum *removes* what drags; propulsion
  *adds* pull and refocuses filler into story rather than cutting it. Momentum subtracts,
  propulsion adds; together they own forward motion, and propulsion runs on every chapter in
  the loop.
- **editor-ensemble** — runs this as one of five parallel editors.
- **outline-designer / story-bible** — define which beats are required; this lens obeys them.

## What it is not

Not a structural reorder and not a quality-of-prose rewrite. It keeps the chapter moving by
tightening the slow and cutting the pointless, and leaves the required story intact.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill momentum-editor --target <book-folder> --status DONE --item "<chapter>" --output "editors/NN-slug/momentum.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
