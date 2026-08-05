---
name: chapter-writer
description: Writes full, publication-quality prose for book chapters from an outline and per-chapter briefs, saving one markdown file per chapter. Use whenever the user wants to draft, write, or flesh out chapters of a book or manuscript, expand an outline into actual prose, or continue/rewrite specific chapters. This is the drafting stage of the book-machine pipeline, but it works standalone on any folder that has an outline.json.
---

# Chapter Writer

Expand a book's outline into real chapters — rich, coherent, finished prose, not
notes or bullet points. You are ghostwriting a book that a person will actually
read end to end, so voice, continuity, and pacing matter as much as content.

## Inputs

Read from the book project folder (default: current directory, or ask):

- **`outline.json`** — the chapter list (order, titles, briefs, `targetWords`).
  This is your spec. Required.
- **`book.json`** — title, author, audience, tone, language. Use it to keep the
  voice consistent.
- **`research.md`** — if it exists, the project's factual source material. Treat it
  as ground truth: get the details it covers right, and never contradict it. If the
  chapter needs a fact the research doesn't have, write around the gap rather than
  inventing one, and flag it. Maintained by the **project-research** skill.
- **`story-bible.md`** — the project's world/voice/plot reference, if present. Read
  it first and treat it as **law**: obey the World Brief's rules, write to the Voice
  & Style Guide (including its banned expressions), and serve the Plot Structure &
  Beats for this point in the story — don't break a world rule, drift from the voice,
  or invent plot the beats don't call for. Built by the **story-bible** skill.
- **`characters.json`** — the cast dossier, if the book is a story. Read it before
  writing and treat it as canon: names and their spelling, aliases, appearance, how
  each character speaks, relationships, the `continuityNotes` (hard facts that must
  never drift), and what drives them — their `motivation` (want/need) and `fear`.
  Keep each character's `secret` hidden in the prose until the plot reveals it. If
  it's missing and the story clearly has characters, offer to build it with the
  **character-dossier** skill first.

If there's no `outline.json`, the book hasn't been structured yet — use the
**outline-designer** skill first (or offer to).

## What to produce

One markdown file per chapter in `chapters/`, named `<id>-<slug>.md` where `id`
matches the outline entry (e.g. `03-finding-your-footing.md`). Each file:

```markdown
# <Chapter Title>

<the chapter prose>
```

- Begin with the chapter title as a single `# ` H1, then the prose. (The
  packager treats `outline.json` as the source of truth for titles, so this H1
  is for human readability and is fine to include.)
- Separate paragraphs with blank lines.
- For section breaks **within** a chapter, use `## Subheading` lines.
- Light inline formatting only: `**bold**` and `*italic*`, used sparingly.
- Don't invent front-matter keys, footnote syntax, or HTML — keep it clean
  markdown so the packager renders it predictably.

## How to write well

- **Honor the brief, serve the arc.** Cover what the brief asks, but write with
  the whole book in mind — pick up threads from earlier chapters and set up later
  ones. You have the full outline; use it for continuity and don't repeat what
  another chapter owns.
- **Match the audience and tone** from `book.json`. A chapter for beginners
  explains its terms; a rigorous one earns its claims. Keep the narrating voice
  steady across chapters — a reader should not feel the seams between files.
- **Write in the house style.** Follow the **prose-style** skill: no em dashes (use
  the punctuation that names the relationship), no AI-isms (no emotion-labeling,
  stock phrases like "her breath caught," clichéd metaphors, or generic poetic
  filler), complete-sentence narration paired with realistic, jagged dialogue,
  grade 9–12 readability, and Oxford commas. Show, don't tell. For fiction, scan
  against its `references/ai-isms.md` before finalizing.
- **Obey the Story Bible.** When `story-bible.md` exists, it's law: honor the
  world's rules, write to the Voice & Style Guide (and never use its banned
  expressions), and serve the Plot Structure & Beats for this point in the story
  rather than inventing new turns. If the guide includes a **Voice Sample**, match its
  rhythm, diction, and narrative distance directly, line by line; imitate the sample, don't
  just read its description. Your previous chapter is the other live exemplar, so the new
  one must read like it came from the same hand.
- **Keep characters true to the dossier.** When `characters.json` exists, every
  character must match it — name spelling, appearance, voice, relationships, and
  `continuityNotes` — and behave consistently with their `arc` at this point. Let
  each character's `motivation` (want) and `fear` drive them from underneath, and
  keep their `secret` hidden in the prose until the plot reveals it. If the story
  reveals something new a character's entry doesn't capture, mention it so the
  dossier can be updated; don't silently contradict it.
- **Earn the length.** `targetWords` is the floor for *story*, not a quota for *words*.
  Reach it, even exceed it, but only with material that advances the plot or deepens a
  character. Never pad to a number with stage business, restated interiority, sensory
  lists, or reflection that explains what the scene already showed. If you can't reach the
  length with advancing material, the scene is under-plotted, so add real story (a
  complication, an escalation, a consequence, a turn), not more words about the same beat.
  A long chapter where every paragraph pulls is the goal; a long chapter padded to a number
  is the failure mode this book is trying to escape.
- **Propel the reader, sentence by sentence.** The book lives or dies on forward motion, so
  build it in as you draft (see prose-style Part 4). Give every scene a dramatic question
  and hold it open; start in motion and enter each scene late, with no throat-clearing
  windup; dole out information instead of dumping it, ending paragraphs a half-step
  unresolved; connect beats by *therefore* and *but*, not *and then*; favor active verbs
  over *was, were, there was*. End the chapter unresolved, on a turn or a question that
  makes the next chapter necessary, never on a tidy reflective summary.

## Working through the book

- For a fresh draft, write chapters in order so continuity compounds. For a long
  book, it's good practice to write the first chapter or two, show the user, and
  confirm the voice before drafting the rest — re-drafting one chapter is cheap.
- Support partial runs: if the user says "rewrite chapter 4" or "draft chapters
  5–8," write only those files and leave the rest untouched.
- After drafting, update `book.json` `status` to `"drafting"` (or `"edited"` once
  an editing pass is done), and tell the user which files you wrote.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill chapter-writer --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
