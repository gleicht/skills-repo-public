---
name: voice-editor
description: An active per-chapter voice and style editor. It holds a single, consistent narrative voice across the chapter and true to the book's established voice — smoothing tonal wobble, register slips, POV-distance drift, and rhythm inconsistency back into the book's voice, and enforcing the prose-style house rules (no em dashes, no AI-isms, American spelling, complete-sentence narration, jagged dialogue). Use whenever the user wants a consistent voice, to fix tone or register that drifts, smooth the style, hold the prose at one reading level, or keep a chapter sounding like the rest of the book. It matches the established voice from the story bible and prior chapters and never flattens the prose or imposes a generic style.
---

# Voice Editor

The voice-and-style lens of the per-chapter editor panel. It makes the chapter read as
**one consistent voice**, and the *book's* voice — not a generic clean style. It is the
active, single-chapter application of the **prose-style** house rules plus the story
bible's Voice & Style Guide.

## What it holds steady

- **Constant narrative voice.** One diction, one sentence music, one level of irony or
  warmth across the chapter. Smooth a paragraph that drifts suddenly formal, casual, or
  purple back into the book's register.
- **POV distance.** Keep the chosen psychic distance steady (close-third stays close);
  don't drift toward or away from the character's head mid-scene.
- **Rhythm.** Maintain the book's sentence-length variety and cadence; fix a stretch that
  goes monotone or suddenly clipped against the established rhythm.
- **Established voice, not a new one.** Match the diction, motifs, and tone already set by
  `story-bible.md` — above all its **Voice Sample**, the concrete paragraphs the prose must
  sound like, plus the Voice & Style Guide, banned expressions, and micro-phrases — and the
  prior chapters. The standard is *this book's* voice; measure the chapter against the
  sample, not a description of it.
- **Prose-style house rules.** Enforce them: no em dashes (use the punctuation that names
  the relationship), no ellipses, straight quotes, American spelling, serial commas,
  complete-sentence narration with jagged dialogue, no AI-isms or stock fiction phrases,
  no negation-correction antithesis, questions take a question mark.

## How it runs

1. Read the chapter against `story-bible.md` (the Voice & Style Guide and any banned
   expressions), the previous chapter (the established voice in practice), `book.json`
   (tone, audience, reading level), and the **prose-style** baseline.
2. Edit lines that fall out of voice back into it — the drifting register, the AI-ism, the
   em dash, the tonal wobble, the rhythm that flattens. Keep the meaning and the scene.
3. Write the harmonized version and a change-note (what fell out of voice and how it was
   brought back).

## What it writes

Non-destructive. Inside **editor-ensemble**, write `editors/NN-slug/voice.md` and return the
change-note. Standalone, write the same file plus the note; promote on the author's OK
(copy over `chapters/NN-slug.md`).

## Constraints

- **Match the established voice; don't invent one.** The book's voice (story bible + prior
  chapters) is the target, not a house-neutral style. If the book's voice and prose-style
  ever conflict, the book's deliberate choices win (and you flag it).
- **Don't flatten.** Consistency is the goal, not homogenization. A distinctive sentence
  that *is* the voice stays; you remove the lines that break it, not the ones that make it.
- **Preserve plot, POV facts, and meaning.** Style only; defer to the other editors for
  story, continuity, dialogue substance, and pace.

## Relationship to the other skills

- **prose-style** — the house rules this lens applies line by line.
- **style-check** — the read-only metrics (adverbs, crutch words, reading level, echoes);
  voice-editor acts on what those numbers point at.
- **book-editor** — the later whole-manuscript voice smoothing; voice-editor front-loads it
  per chapter.
- **editor-ensemble** — runs this as one of five parallel editors.

## What it is not

Not a copyedit-for-grammar-only and not a generic polish. It keeps the chapter in the
book's own voice, consistent end to end, without sanding off what makes that voice itself.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill voice-editor --target <book-folder> --status DONE --item "<chapter>" --output "editors/NN-slug/voice.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
