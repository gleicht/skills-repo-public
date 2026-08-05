---
name: outline-designer
description: Designs a book's structure — a strong title plus an ordered list of chapters, each with a short brief describing what it covers. Use whenever the user wants a book outline, chapter plan, table of contents, or overall structure for a manuscript, ebook, guide, or non-fiction/fiction book, or when starting a book from a topic, premise, or pile of notes. This is the first stage of the book-machine pipeline, but it works standalone too.
---

# Outline Designer

Turn an idea into a clear, well-paced book structure. A good outline is the
backbone of the whole book: it fixes the scope, the order of ideas, and the
promise of the title. Getting it right here saves expensive rewrites later.

## Inputs

Gather (ask, or infer from the conversation / existing `book.json`):

- **Topic / premise** — required. What the book is about.
- **Working title** — optional; you'll propose a stronger one if none is given.
- **Audience** — who it's for. Shapes vocabulary, depth, and examples.
- **Tone / style** — e.g. warm and practical, rigorous, playful.
- **Notes / source material** — any outline, bullet points, or research to follow.
- **`research.md`** — if it exists, the project's factual source material. Shape the
  structure to cover what the research supports, and don't plan chapters that depend
  on facts the research doesn't have. Built by the **project-research** skill.
- **`story-bible.md`** — for a story, if it exists, treat its **Plot Structure &
  Beats** as the spine the outline must deliver (in order), and respect its **World
  Brief**. The outline is how those beats become concrete chapters. Built by the
  **story-bible** skill. (The cast comes from `characters.json`, below.)
- **`characters.json`** — for a story, read the cast dossier if it exists, and
  build the chapter arc around those characters and their goals. If the book is
  clearly a story but no dossier exists yet, suggest building one with the
  **character-dossier** skill first.
- **Chapter count** — how many chapters (default 6 if unspecified).
- **Words per chapter** — rough target (default 1200), recorded per chapter as
  `targetWords`. Treat it as the intended length the chapter's *story* must fill, not a
  quota to pad toward, and pair every target with enough beats to earn it.

## What to produce

Write two files into the book project folder (create it if needed; default
`./<slug>/`):

**`outline.json`** — the authoritative chapter list:
```json
{
  "title": "Final, compelling title",
  "chapters": [
    { "id": "01", "title": "Chapter title", "brief": "2-4 sentences describing exactly what this chapter covers and why it sits here.", "targetWords": 1200 }
  ]
}
```

**`book.json`** — metadata/spec (create or update):
```json
{
  "title": "Final title",
  "author": "",
  "topic": "...",
  "audience": "...",
  "tone": "...",
  "language": "en",
  "status": "outlined"
}
```

Use zero-padded `id`s (`01`, `02`, …) so chapters sort correctly.

## How to design a good outline

- **Make the chapters tell a story in order.** Each should build on the last.
  For non-fiction: motivation → fundamentals → application → troubleshooting →
  next steps. For fiction: a coherent arc. Avoid chapters that overlap or could
  be swapped without anyone noticing — that's a sign the cut is wrong.
- **Write briefs the next stage can actually use.** A brief is an instruction to
  the chapter writer, not a teaser. Say what the chapter establishes, what
  examples or beats it includes, and what it deliberately leaves to other
  chapters. Specific beats vague.
- **Give every chapter a question, a turn, and enough story to fill its length.** In each
  brief, name the dramatic question the chapter runs on (what the reader reads it to find
  out) and the turn it makes (the change in value or state from open to close). Make sure
  the beats you assign carry enough story (a complication, a decision, a consequence) to
  reach `targetWords` with material that advances the plot or a character. If a chapter
  can't justify its length with real story, shorten it or fold in more story; never plan a
  chapter the writer will have to pad.
- **Earn the title.** Propose a title that promises something concrete to the
  stated audience. If the user gave a working title, you may keep it or offer a
  stronger alternative and let them choose.

## Finishing

Show the user the proposed title and the chapter list (titles + one-line gist).
Invite them to add, cut, reorder, or rename chapters — editing `outline.json`
directly is fine. Don't move on to drafting from here; that's the
chapter-writer stage.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill outline-designer --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
