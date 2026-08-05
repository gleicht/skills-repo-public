# Welcome to the Book Machine: Onboarding Guide

A practical guide to writing a book with the Book Machine, a suite of modular
[Claude Code](https://claude.com/claude-code) skills that takes a project from a bare
idea (or a stack of your own chapters) all the way to a finished EPUB and Word file.

This guide is written so someone who has never touched the machine can sit down and
produce a book. Read it top to bottom the first time, then keep it as a reference. If
you already know Claude Code, skip to [Quick Start](#quick-start).

---

## 1. What the Book Machine is

The Book Machine is not a separate app. It is a set of **skills** that live inside
Claude Code. You talk to Claude in plain English, Claude recognizes which stage of
book-making you are asking for, and it runs the matching skill. There is no website to
log into, no server to start, and **no API key to configure**. Claude Code itself is
the engine.

Two ideas make the whole thing work:

1. **Files are the interface.** Every stage reads and writes plain files in one
   **project folder**. Nothing is hidden in a database. If you stop today and come back
   next month, any stage can pick up exactly where you left off by reading the folder.
2. **The stages are modular.** You can run the whole pipeline end to end, stop after any
   step, redo one step, or run a single step on its own. Want only an outline? Only a
   Word export of chapters you already wrote? That works.

It supports two ways of working, and you can mix them:

- **Generate from scratch:** you give a premise and answer a few interview questions, and
  the machine drafts the book.
- **Bring your own prose:** you write the chapters yourself, and the machine ingests,
  style-checks, fact-checks for continuity, and packages them.

---

## 2. What you need

1. **Claude Code**, installed and signed in (desktop app, CLI, or an IDE extension).
2. **The skill suite** installed in your personal skills folder:
   `~/.claude/skills/` (on Windows, `C:\Users\<you>\.claude\skills\`). Each skill is a
   folder with a `SKILL.md` inside. If you are setting up a new machine, clone the skill
   repository into that location.
3. **Python 3** on your PATH. The EPUB and Word packagers are plain Python with no extra
   libraries to install.
4. **Git (optional but recommended)** if you want to back your book up to GitHub.

That is the entire setup. Once the skills are in `~/.claude/skills/`, Claude finds them
automatically.

---

## 3. The pieces: the eleven skills

You rarely call these by name. You describe what you want, and Claude picks the right
one. But it helps to know the cast. Each skill owns one job and, where relevant, one
file in the project folder.

| Skill | What it does | Owns |
|-------|--------------|------|
| **book-machine** | The conductor. Runs the whole pipeline with review checkpoints. | the project folder |
| **project-research** | Captures your source material and facts so the book stays accurate. | `research.md`, `research/` |
| **story-bible** | World rules, narrative voice and style, and plot beats. | `story-bible.md` |
| **character-dossier** | Interviews you to build the cast: name, role, want, fear, secret. | `characters.json` |
| **outline-designer** | A strong title plus an ordered chapter list, each with a brief. | `outline.json` |
| **chapter-writer** | Writes full prose, one file per chapter, in your house style. | `chapters/NN-*.md` |
| **prose-style** | The always-on house style (see below). Applied to all prose. | (a baseline, no file) |
| **book-editor** | An editorial pass for consistency, flow, pacing, and continuity. | (edits `chapters/`) |
| **fidelity-review** | Audits the work against the sources of truth: no drift, no padding, no made-up facts. | `fidelity-report.md` |
| **epub-packager** | Builds a valid EPUB for e-readers. | `dist/…​.epub` |
| **docx-packager** | Builds an editable Microsoft Word file. | `dist/…​.docx` |

### Two of these run quietly in the background

- **prose-style** is the **always-on baseline** beneath everything the machine writes or
  edits. It keeps the writing human: it replaces em dashes with punctuation that names
  the relationship they signal, strips AI tells (words like "delve," fake balance,
  emotion-labeling, stock phrases like "her breath caught"), keeps narration in complete
  sentences, and shows rather than tells. You do not invoke it; it is simply how the
  machine writes.
- **fidelity-review** can fire **automatically** after any chapter is written, if you
  have the optional auto-review hook installed (see
  [Section 9](#9-optional-extras)). Otherwise, just ask for it.

---

## 4. The project folder

Everything about one book lives in one folder. Here is the full layout. You will not
create all of this by hand; the stages write most of it.

```
<book-folder>/
├── book.json            # metadata + spec (title, author, audience, tone, topic, status)
├── research.md          # (optional) factual source material
├── research/            # (optional) raw sources behind research.md
├── story-bible.md       # (stories) world rules, voice, plot beats
├── characters.json      # (stories) the cast dossier
├── outline.json         # the chapter order and titles (source of truth)
├── chapters/
│   ├── 01-<slug>.md     # one file per chapter; starts with "# Chapter Title", then prose
│   └── 02-<slug>.md
├── fidelity-report.md   # (optional) the latest verification report
├── dist/                # scratch output (safe to delete; regenerate any time)
└── approved/            # blessed, final deliverables you have signed off on
```

**`book.json`** holds the spec:

```json
{
  "title": "string",
  "author": "string",
  "topic": "string",
  "audience": "string",
  "tone": "string",
  "language": "en",
  "status": "outlined | drafting | edited | packaged"
}
```

**`outline.json`** is the source of truth for chapter order and titles:

```json
{
  "title": "string",
  "chapters": [
    { "id": "01", "title": "Chapter One: ...", "brief": "2-4 sentences on this chapter", "targetWords": 1200 }
  ]
}
```

Chapter files are named `<id>-<slug>.md` so they sort correctly and map back to their
outline entry by the `id` prefix. You can edit any of these files by hand at any time;
the machine expects that.

### `dist/` versus `approved/`

This is a convention worth understanding:

- **`dist/`** is **scratch**. The packagers write here while you are reviewing. It is
  disposable and is normally excluded from Git.
- **`approved/`** holds the **final files you have signed off on**. When you approve a
  chapter or a book, the machine builds the `.docx` and `.epub` into `approved/` and
  (if you use Git) commits and pushes them. This is your clean, trustworthy output.

---

## 5. Quick Start

The fastest way in is to open Claude Code **inside the folder where you keep your
books** and just say what you want. A few openers that work:

> "Let's write a book. It's a comedic sci-fi novella about a moon base."

> "Run this chapter through the book machine:" *(then paste your chapter)*

> "Make an outline for a beginner's guide to backyard stargazing, about 10 chapters."

> "Package the chapters in this folder as an EPUB and a Word doc."

Claude will set up a project folder, ask only the questions it actually needs, and pause
at the points that matter so you can steer. You do not have to memorize any commands.

---

## 6. Workflow A: Generate a book from scratch

Use this when you have an idea and want the machine to draft it.

**Step 1: Start the project.** Tell Claude the premise and any of the spec you already
know (working title, audience, tone, how many chapters, rough words per chapter).

> "I want to write a comedic sci-fi novella set on a lunar base, around 8 short
> chapters. Audience is adults who like light, funny sci-fi."

Claude creates the folder and a first `book.json`.

**Step 2: Add research (optional).** If the book should rest on real facts or notes,
hand them over now so every chapter is grounded from the start.

> "Here are my notes on how lunar bases actually work. Use them as background."

**Step 3: Build the foundations (for stories).** For anything character-driven, the
machine establishes its reference material *before* outlining:

- The **character dossier**: Claude interviews you about each character (name, role,
  what they want, what they fear, a secret) and writes `characters.json`.
- The **story bible** (for serious or long projects): world rules, the voice and style
  guide, and plot beats, written to `story-bible.md`.

> "Let's build the characters first." → answer the interview questions.

**Step 4: Outline.** The machine proposes a title and a chapter list, each with a brief.

> Review it. **This is a checkpoint.** Reorder, rename, split, merge, or change the
> count before any prose is written. Editing `outline.json` by hand is fine.

**Step 5: Draft.** The machine writes the chapters into `chapters/`. For a long book it
will write a couple first and show you a sample.

> Confirm the voice on the sample before it drafts the rest. Re-drafting one chapter is
> cheap; re-drafting twelve in the wrong tone is not.

**Step 6: Edit (optional, recommended).** A consistency-and-polish pass across the whole
manuscript, including checking the cast against `characters.json`.

**Step 7: Verify.** Fidelity review audits the manuscript against the spec, outline,
story bible, dossier, and research, then reports what it found and fixed. It loops until
clean or you tell it to stop.

**Step 8: Package.** Build the EPUB and/or Word file.

> "Build the EPUB and a Word doc."

---

## 7. Workflow B: Bring your own prose

Use this when **you** are the writer and you want the machine to ingest, refine, check,
and package your chapters.

**Step 1: Set up the project once.** If this is a new book, give Claude the basics so it
can create `book.json` and (for a story) the story bible and character dossier. If you
already have a first chapter, the machine can reverse-engineer a starting bible and cast
from it, flagging anything it had to guess.

**Step 2: Hand over a chapter.**

> "Run the next chapter through the book machine:" *(paste the chapter)*

The machine will:

1. **Save** it as `chapters/NN-slug.md`, faithfully. Your words are kept as written.
2. **Apply the house style** lightly: it fixes mechanical issues (for example, a title
   em dash becomes a colon) without bulldozing your voice or your deliberate choices.
3. **Fidelity-review** it against your sources of truth, checking continuity with
   earlier chapters and flagging anything that contradicts the bible or the cast.
4. **Reconcile the scaffolding to your text.** Your prose is the highest authority. If a
   chapter introduces a new character or a plot turn, the machine updates
   `characters.json`, `story-bible.md`, and `outline.json` to match what you wrote, and
   tells you what it changed.

**Step 3: Review.** Ask for a Word export and read it.

> "Export that chapter as a .docx so I can review it."

**Step 4: Revise or approve.**

- To revise: tell the machine the changes in plain language. It edits the chapter file,
  re-runs fidelity review, and rebuilds the export.
- To approve: say so. The machine builds the `.docx` and `.epub` into `approved/` and,
  if you use Git, commits and pushes them.

> "Approved. Push everything."

A note on **planning aids**: for a long or twisty book, the machine can keep extra
reference files such as a spoiler-walled clue ledger for a mystery, so later chapters
stay consistent with a reveal you have not written yet. Ask for whatever tracking you
need; it is just another file in the folder.

---

## 8. Packaging and formatting

Both packagers read the same folder, so you can produce either or both at any time.

### EPUB (the book-form deliverable)

The EPUB is styled like a finished book and is configurable per book. Add a
`"formatting"` block to `book.json` to override any of these defaults:

| Key | Default | Meaning |
|-----|---------|---------|
| `dropCap` | `true` | Ornamental large initial on each chapter's first paragraph |
| `justify` | `true` | Justified body text (vs. left-aligned) |
| `hyphenate` | `true` | Allow hyphenation (pairs well with justify) |
| `paragraphIndent` | `true` | First-line indent, no blank line between paragraphs |
| `chapterNumber` | `true` | Centered chapter number with a rule above the title |
| `chapterTitleCase` | `"small-caps"` | `"small-caps"`, `"uppercase"`, or `"normal"` |
| `bodyFont` | `"serif"` | `"serif"` or `"sans"` |

Example, for a plainer EPUB:

```json
"formatting": { "dropCap": false, "chapterTitleCase": "normal" }
```

### Word `.docx` (the editable/manuscript deliverable)

The Word file defaults to **left-aligned** body text (ragged right), which is standard
manuscript format. It uses a serif body, page-break-per-chapter, and page numbers. If
you want a fully justified Word file instead, set this in `book.json`:

```json
"formatting": { "docxJustify": true }
```

This is kept separate from the EPUB's `justify` setting, so your EPUB can stay justified
(book-like) while your Word file stays left-aligned (manuscript-like). Both can coexist
in the same `book.json`.

---

## 9. Optional extras

- **Auto fidelity review.** You can install a Claude Code hook so that fidelity review
  fires automatically every time a chapter file is written. With it, you never forget to
  verify a chapter. Without it, just ask for a review when you want one. This is a
  machine-wide setting, configured once in `~/.claude/settings.json`.
- **Git backup.** Make each book folder a Git repo and push it to GitHub. Keep `dist/`
  in `.gitignore` (it is regenerable scratch) and track `approved/` (your final files).
  The machine can do the commits and pushes for you when you approve work.
- **Hands-off permissions.** If you do not want to approve each file action, set Claude
  Code's permission mode so the machine can write files and run the packagers without
  stopping to ask each time.

---

## 10. Common single-stage commands

The machine is modular, so any of these work on their own against an existing folder:

- "Make an outline for ..." → outline only.
- "Write chapter 5." / "Rewrite chapter 3 in a tenser voice." → draft one chapter.
- "Do an editing pass on the whole manuscript." → editor only.
- "Fact-check these chapters against the story bible." → fidelity review only.
- "Build an EPUB." / "Export the book to Word." → packaging only.
- "Add this to the research." → research only.
- "Add a new character." / "Update the story bible with this rule." → foundations only.

---

## 11. Tips and gotchas

- **Checkpoints beat autopilot.** The expensive, hard-to-undo steps are drafting and
  editing. Approve the outline before drafting, and the voice before drafting in bulk.
  This is where a book goes right or wrong.
- **Your text wins.** In the bring-your-own-prose workflow, your words are the source of
  truth. The machine reconciles its notes to your chapters, never the other way around.
- **The machine reads the folder, not its memory.** To resume after a break, just point
  Claude at the folder. Everything it needs is on disk.
- **No API key needed.** Claude Code is the engine. If something asks for an
  `ANTHROPIC_API_KEY`, you are looking at a different tool, not the skill suite.
- **Windows note:** use native paths (`C:\Users\you\...`). The packagers force UTF-8
  output so accented characters and curly quotes do not crash on Windows consoles.

---

## 12. Where to go next

Every skill is self-documenting: open its folder and read `SKILL.md`. For a one-page
description of all of them, plus what each skill folder contains, see
[`SKILLS.md`](SKILLS.md). Section 4 above describes the project-folder layout the whole
suite reads and writes.

---

*Happy writing. When in doubt, just tell Claude what you want in plain English and let
the machine handle the stages.*
