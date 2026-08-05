---
name: dialogue-editor
description: An active per-chapter dialogue editor. It rewrites a chapter's dialogue to be sharp and propulsive and never boring or dragging — distinct character voices, subtext, real conflict, natural rhythm — and it cuts on-the-nose lines, exposition dumped into talk, dead back-and-forth, and weak tags (said-bookisms, adverb-laden tags). It is the active counterpart to the read-only dialogue-pass. Use whenever the user wants to sharpen or fix dialogue, make conversations interesting, give characters distinct voices, add subtext, tighten talky scenes, or cut stilted, boring, or expository dialogue. Honors the characters.json voices and prose-style (dialogue stays jagged) and never changes the plot a conversation carries.
---

# Dialogue Editor

The dialogue lens of the per-chapter editor panel. It rewrites the chapter's spoken lines
so the talk is **always interesting and never drags** — the layer that most separates flat
fiction from sharp fiction. It is the *active* counterpart of the read-only
**dialogue-pass**: it does not just flag, it fixes.

## What it sharpens

- **Distinct voices.** Cover the tags — can you still tell who is speaking? Make each
  character's vocabulary, rhythm, and verbal habits their own, per `characters.json`. No
  two characters interchangeable.
- **Subtext.** People rarely say exactly what they mean. Replace on-the-nose declarations
  with lines that imply, deflect, or do two things at once.
- **Conflict.** A scene where everyone agrees and states their feelings is dead. Give
  exchanges friction, cross-purpose, something withheld.
- **Cut the drag.** Remove dead back-and-forth, throat-clearing greetings, repetition, and
  lines that add nothing. Every line should earn its place or go.
- **No exposition dumps.** Strip "As you know" backstory and plot recited for the reader's
  benefit; let needed information arrive under pressure, not in a lecture.
- **Tags and beats.** Prefer `said`/`asked` plus a telling action beat; kill said-bookisms
  ("he expostulated") and adverb tags ("she said angrily"); fix over-tagging in a clear
  two-hander and add attribution where the reader loses the thread.
- **Rhythm.** Real speech is jagged — contractions, fragments, interruptions. Keep dialogue
  un-smoothed (prose-style: narration is complete sentences, dialogue stays jagged).

## How it runs

1. Read the chapter with the cast voices from `characters.json` and the story bible's
   voice/era constraints in mind, plus the **prose-style** baseline.
2. Edit the dialogue and its tags/beats to hit the axes above. Cut what drags; sharpen what
   stays; build in subtext and conflict where the talk is flat.
3. Write the stronger version and a change-note (which exchanges changed and why).

## What it writes

Non-destructive. Inside **editor-ensemble**, write `editors/NN-slug/dialogue.md` and return
the change-note. Standalone, write the same file plus the note; promote on the author's OK
(copy over `chapters/NN-slug.md`).

## Constraints

- **Keep what is said true to character and canon.** Don't change a plot point a line
  carries, a fact revealed, or a character's established voice; defer to `characters.json`
  and `story-bible.md`.
- **Don't touch narration** beyond what a dialogue fix requires (beats around the lines are
  fair game; the surrounding prose is the other editors' work).
- **Preserve POV and meaning.** Sharper, not different.

## Relationship to the other skills

- **dialogue-pass** — the read-only diagnostic; dialogue-editor applies the fixes.
- **editor-ensemble** — runs this as one of five parallel editors.
- **character-dossier / prose-style** — the voices and the jagged-dialogue rule this obeys.

## What it is not

Not a whole-book pass and not a license to rewrite narration. It makes the talk sharp,
distinct, and propulsive, and leaves the plot the conversation carries intact.

## Audit log
When a run finishes, record it with the shared logger:

`python <skills-dir>/lib/audit_log.py --skill dialogue-editor --target <book-folder> --status DONE --item "<chapter>" --output "editors/NN-slug/dialogue.md" --note "<one-line summary>"`

Full convention: `lib/AUDIT-LOG.md`.
