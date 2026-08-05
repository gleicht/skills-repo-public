---
name: book-editor
description: Performs an editorial pass over a drafted book — improving consistency, tone, flow, and pacing across chapters, removing repetition, and fixing rough transitions. Use whenever the user wants to edit, revise, polish, tighten, or proofread a manuscript or its chapters, smooth the voice across a book, or do a consistency/continuity pass. This is the editing stage of the book-machine pipeline; it works standalone on any folder of chapter files.
---

# Book Editor

Take a drafted manuscript from "written" to "polished." Individual chapters are
often fine on their own but drift as a set — terminology shifts, the voice
wobbles, ideas get re-explained, transitions clunk. Your job is to make the book
read as one coherent work.

## Inputs

Read from the book project folder (default: current directory, or ask):

- **`chapters/*.md`** — the drafted chapters. Required.
- **`outline.json`** — intended structure, titles, and order.
- **`book.json`** — title, author, audience, tone. The tone here is the standard
  you're editing toward.
- **`story-bible.md`** — the project's central reference, if present. The governing
  standard for world rules, narrative voice/style (including banned expressions),
  plot beats, and character truths. Check the manuscript against it.
- **`characters.json`** — the cast dossier, if present. This is the canonical
  reference for character consistency; check the chapters against it.

## How to run the pass

Read the **whole book first**, in order, before changing anything. You can only
judge consistency and repetition with the full manuscript in your head — editing
chapter 1 in isolation is how inconsistencies survive.

Then edit the chapter files in place, against this checklist:

- **Consistency.** One spelling of recurring terms, names, and capitalization.
  One narrating voice and tense. Facts, numbers, and examples that agree across
  chapters.
- **Factual accuracy (research).** If `research.md` exists, check the manuscript's
  factual claims against it: flag anything that contradicts the research or states
  as fact something the research lists as unconfirmed. Don't silently "correct"
  toward invented facts — surface the discrepancy.
- **Story-bible adherence (stories).** If `story-bible.md` exists, audit the
  manuscript against it: no broken **world rules**, prose that matches the **Voice
  & Style Guide** (flag any **banned expressions**), and events that follow the
  **Plot Structure & Beats** without invented twists. This is the highest-authority
  reference for world/voice/plot; if a chapter contradicts it, the chapter is what's
  wrong (unless the user says the bible is out of date).
- **Character continuity (stories).** If `characters.json` exists, check every
  character against it: name and alias spelling, appearance, manner of speaking,
  relationships, and the `continuityNotes` (age, eye color, scars, accent — the
  facts that must never drift). Flag any place a character acts against their
  established personality, `arc`, `motivation`, or `fear` — and any place a
  character's `secret` is revealed earlier than the plot intends. If a chapter and
  the dossier genuinely disagree, surface it rather than guessing which is right.
- **Non-repetition.** If two chapters explain the same concept, keep the best
  explanation where it belongs and replace the other with a brief callback. Cut
  sentences that restate what the reader just read.
- **Flow and transitions.** Each chapter should land where the next can pick up.
  Smooth abrupt openings/closings. Fix paragraph-to-paragraph jumps.
- **Tone and clarity.** Bring every chapter to the `book.json` tone. Tighten
  padding, untangle convoluted sentences, replace vague claims with concrete
  ones — without flattening the author's character.
- **House style (prose-style skill).** Apply the user's standing style: replace
  em dashes with the right punctuation, strip AI-isms (emotion-labeling, stock
  fiction phrases, clichéd sensory metaphors, fake balance, filler, reflexive
  reflective endings), and convert telling into showing. Keep narration in
  complete sentences while leaving dialogue realistically jagged. Use the
  `ai-ism-editor/references/ai-isms.md` flag lists and diagnostic codes to mark
  passages; for a chapter that needs the patterns actively rewritten out, run the
  **ai-ism-editor** skill.
- **Pacing.** Flag chapters that are markedly longer or thinner than their peers;
  balance them if it serves the book.

Preserve the file format: keep the leading `# <Chapter Title>` H1, plain
paragraphs, `## ` subheads, and light `**bold**`/`*italic*` only. Don't
introduce new markup the packager won't understand.

## Be a careful editor, not a rewriter

- **Edit, don't replace.** Improve the draft; don't regenerate it from scratch
  and lose what was working. Make the smallest changes that fix the real problem.
- **Surface the big calls.** If a chapter needs structural surgery, a section
  should move between chapters, or two chapters should merge, don't silently do
  it — tell the user and let them decide. Within-chapter line and paragraph
  editing you can just do.
- **Report what changed.** After the pass, give the user a short editorial
  summary: the consistency issues you fixed, repetition you removed, and any
  larger changes you're recommending. Update `book.json` `status` to `"edited"`.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill book-editor --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
