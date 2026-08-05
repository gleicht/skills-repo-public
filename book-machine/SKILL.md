---
name: book-machine
description: Orchestrates writing a complete book from an idea, end to end, by running its multi-stage suite of modular skills (project-research, story-bible, character-dossier, outline-designer, chapter-writer, book-editor, deduplicator, fidelity-review, and the epub-/docx-packagers) in sequence with review checkpoints. Use this whenever the user wants to create, write, generate, draft, or produce a whole book, manuscript, ebook, or EPUB from a topic, premise, notes, or outline — even if they don't name the stages. If the user only wants one stage (just an outline, just packaging, etc.), use that stage's skill directly instead.
---

# Book Machine

This skill turns an idea into a finished book by coordinating a set of
specialized skills. Each stage reads and writes plain files in a shared **book
project folder**, so the stages stay decoupled — the user can stop after any
stage, redo one, or run a single stage on its own later.

You are the conductor. You don't write prose or assemble EPUBs yourself here —
you set up the project, then hand each stage to its skill, pausing for the user
to review between stages.

## The shared project-folder contract

Every stage agrees on this layout. Read it once; the stage skills assume it.

```
<book-folder>/
├── book.json            # metadata + spec (title, author, audience, tone, topic, status)
├── research.md          # (optional) factual source material — see project-research skill
├── research/            # (optional) raw sources backing research.md
├── story-bible.md       # (stories) world rules, voice, plot beats — see story-bible skill
├── clues.md             # (stories, optional) spoiler-walled fair-play clue ledger — owned by story-bible
├── characters.json      # (stories) structured cast dossier — see character-dossier skill
├── outline.json         # { "title", "chapters": [{ "id", "title", "brief", "targetWords" }] }
├── chapters/
│   ├── 01-<slug>.md     # one file per chapter; starts with "# <Chapter Title>", then prose
│   └── 02-<slug>.md
├── consensus/           # (optional) best-of-N drafts + merged chapter — see chapter-consensus skill
│   └── NN-slug/         #   draft-K-<lens>.md, merged.md, consensus-report.md
├── clarity/             # (optional) per-chapter clarity report + edited proposal — see clarity-edit skill
│   ├── NN-slug.report.md
│   └── NN-slug.edited.md
├── ai-isms/             # (optional) per-chapter AI-ism report + edited proposal — see ai-ism-editor skill
│   ├── NN-slug.report.md
│   └── NN-slug.edited.md
├── front-matter/        # (optional) title-page metadata + front/back matter — see front-matter skill
│   ├── front-matter.json #   manifest: which pieces, front vs back, order
│   └── dedication.md     #   copyright.md, epigraph.md, about-author.md, …
├── transitions/         # (optional) connective passages between chapters — see chapter-transition skill
│   ├── transitions.json #   index: one entry per seam (decision, appearance, status, rationale)
│   └── 01-02.md         #   the bridge between chapter 01 and 02 (only when one is proposed)
├── dev-edit-report.md   # (optional) developmental edit / revision roadmap — see developmental-edit skill
├── style-report.md      # (optional) prose-style metrics — see style-check skill
├── dialogue-report.md   # (optional) dialogue craft review — see dialogue-pass skill
├── ai-detection-report.md # (optional) reads-as-AI heuristic scan — see ai-detection skill
├── fidelity-report.md   # (optional) latest verification report — see fidelity-review skill
├── review-report.md     # (optional) final panel review + READY/NOT-READY verdict — see review-panel skill
├── preflight-report.md  # (optional) pre-publish reconciliation + GO/HOLD verdict — see preflight-check skill
├── amazon-categories.md # (optional) KDP categories + keywords for publishing — see amazon-book-categorizer skill
├── audit-log.md         # every skill run, chronological (ran / result / items / outputs) — see lib/AUDIT-LOG.md
├── audit-log.jsonl      # the same run entries as JSON lines
└── dist/
    ├── <slug>.epub      # produced by epub-packager
    ├── <slug>.docx      # produced by docx-packager
    └── <slug>.pdf       # produced by pdf-packager
```

**`book.json`**
```json
{
  "title": "string",
  "subtitle": "string",
  "author": "string",
  "series": { "name": "string", "number": 1 },
  "topic": "string",
  "audience": "string",
  "tone": "string",
  "language": "en",
  "status": "outlined | drafting | edited | verified | reviewed | packaged",
  "formatting": { "justify": true, "dropCap": true, "docxJustify": false }
}
```

`title` and `author` are the spine. `subtitle`, `series`, and the copyright fields
(`publisher`, `copyrightYear`, `rights`, `edition`) are optional title-page/copyright
metadata owned by the **front-matter** skill — leave them out for sensible defaults.

**`formatting`** is optional and controls per-book output styling for the
packagers. The **EPUB** keys (`dropCap`, `justify`, `hyphenate`, `paragraphIndent`,
`chapterNumber`, `chapterTitleCase`, `bodyFont`) default to the classic justified
novel look; the **DOCX** key `docxJustify` defaults to `false` (left-aligned
manuscript format), kept separate so the EPUB can stay justified while the DOCX
stays ragged-right. See the **epub-packager** and **docx-packager** skills for the
full field lists. Omit `formatting` entirely for sensible defaults.

**`outline.json`** — the source of truth for chapter order and titles.
```json
{
  "title": "string",
  "chapters": [
    { "id": "01", "title": "string", "brief": "2-4 sentences on what this chapter covers", "targetWords": 1200 }
  ]
}
```

Chapter files are named `<id>-<slug>.md` so they sort correctly and map back to
outline entries by their `id` prefix.

## Workflow

1. **Set up the project.** Ask the user (or infer from the conversation) for the
   topic/premise and any optional spec: working title, author, audience, tone,
   notes/source material, how many chapters, and rough words per chapter. Pick a
   project folder — default to `./<slug-of-title-or-topic>/` in the current
   directory unless the user names one. Create the folder and write a first
   `book.json` with `status: "outlined"` pending. **If the user has research or
   source material** for the book, use the **project-research** skill to capture it
   into `research.md` now — at the start, when available and appropriate — so the
   book is grounded in it from the first chapter. This applies to fiction and
   non-fiction alike; skip it when there's nothing to ground.

2. **Foundations (stories only).** If the book is a story — fiction, a novel,
   anything character-driven — establish its reference material *before* outlining.
   Two complementary skills, each owning a distinct domain (no overlap):
   - **character-dossier** → `characters.json`: the cast — each character's name,
     description, role, want, fear, and secret. Build this for any story.
   - **story-bible** → `story-bible.md`: the world rules, voice & style guide, and
     plot beats. Add this for any serious or long-form project (optional for a light
     one). It becomes the governing world/voice/plot reference for drafting and
     editing.
   Skip both for non-fiction with no cast (a guide, a manual). If unsure how much
   scaffolding the book needs, ask.
   - **If the book is part of a series**, also consult the **series-bible** skill: its
     `series-bible.md` (one level up, above the book folders) is higher canon for the
     shared world, timeline, and recurring cast, so a new book honors earlier ones. Once
     the book is finished, reconcile what it established back into the series bible.

3. **Outline.** Use the **outline-designer** skill to produce `outline.json` (and
   finalize the title in `book.json`). For a story, build the arc to deliver the
   Plot Structure & Beats in `story-bible.md` (if present) and around the cast.
   Show the user the proposed title and chapter list.
   **Pause** — let them tweak chapters, reorder, rename, or change counts before
   writing prose. Editing `outline.json` by hand is fine and expected.

4. **Draft.** Use the **chapter-writer** skill to write each chapter into
   `chapters/`. It reads `characters.json` (if present) to keep the cast
   consistent. For a long book, write a couple of chapters, show the user a
   sample, and confirm the voice is right before drafting the rest — re-drafting
   one chapter is cheap; re-drafting twelve in the wrong tone is not. Set
   `status: "drafting"` then `"edited"`-pending.
   **For a chapter that's worth the extra cost** (an opener, a pivotal scene, a climax),
   use the **chapter-consensus** skill instead of a single draft: it fans out three
   lensed chapter-writers in parallel and merges the strongest into one chapter
   (`consensus/NN-slug/merged.md`), promoted to `chapters/` on your OK. Costs ~3× the
   drafting tokens, so reserve it for the chapters that earn it.
   **Right after each chapter is drafted, three light passes fire on it** (automatically, via
   the chapters-write hook), and they apply to **every** chapter: **clarity-edit**, then
   **propulsion-editor**, then **ai-ism-editor**. Clarity-edit flags confusing prose — nonsense,
   wrong vocabulary, failed metaphors, tangled syntax — and writes a clarity-edited proposal to
   `clarity/`; it never invents meaning, and lines it can't parse go back to the author. Then
   **propulsion-editor** rewrites the chapter so every sentence pulls: it enforces prose-style
   Part 4 (a dramatic question per scene; causal *therefore/but*, not additive *and then*;
   enter late and leave early; active verbs; an unresolved ending) and **earn the length**
   (every paragraph advances plot or character; padding is refocused into story, not cut, so
   the chapter keeps or grows its length). Finally **ai-ism-editor** strips the patterns that
   make prose read as machine-written — emotion labeling, vague abstraction, stock fiction
   phrases, clichéd metaphors, filler, reflexive reflective endings, the negation-correction
   antithesis — using the catalog it owns (`ai-ism-editor/references/ai-isms.md`), while
   preserving the idiosyncratic, human parts of the voice. Each pass edits from the one before
   it, so all three land in **one** `ai-isms/` proposal, promoted over the draft on the
   author's OK.

   Order matters: fix comprehension first, then add pull, then remove the machine tells last,
   so a de-AI-ing pass gets the final word on any phrasing the earlier rewrites introduced.

5. **Edit.** Work big-picture first, then line-level. This whole stage is optional but
   recommended; offer it and skip what the draft doesn't need.
   - **(optional, big-picture)** For a full draft with structural weaknesses, use the
     **developmental-edit** skill — it reads the book against the outline and story bible
     and writes a prioritized revision roadmap (`dev-edit-report.md`). Hand its moves to
     **chapter-writer** (rewrites/expansions) and **outline-designer** (restructure)
     *before* polishing sentences.
   - **Diagnostics (read-only, run before the editor to aim it):** the **deduplicator**
     skill (`scripts/check_duplication.py`) catches duplicated content — a chapter pasted
     in twice, a reused passage, near-identical chapters; the **style-check** skill
     (`scripts/style_check.py`) measures crutch/filler words, adverb density, word echoes,
     reading level, and em dashes into `style-report.md`; and the **ai-detection** skill
     (`scripts/ai_likelihood.py`) scores how much the prose reads as AI-generated
     (burstiness, AI-isms, transitions) into `ai-detection-report.md`. All earn their keep
     on books drafted across many sittings or with AI assistance.
   - **Line edit:** use the **book-editor** skill for a consistency-and-polish pass across
     the whole manuscript, checking the cast against `characters.json` and acting on what
     the scans surfaced (some repetition is a deliberate refrain, so the editor and the
     user judge each candidate).
   - **(optional, fiction)** the **dialogue-pass** skill for a focused review of how the
     characters talk (distinct voices, tags/beats, on-the-nose lines → `dialogue-report.md`).

6. **Transitions (optional, stories).** Use the **chapter-transition** skill to judge
   the seam between each adjacent pair of chapters and propose optional connective
   passages where a time jump, location change, POV switch, or tonal shift would
   otherwise jar. It defaults to *no* transition unless one earns its place, writes
   proposals to a `transitions/` folder without editing the chapters, and lets the user
   keep, edit, or remove each. Offer it for multi-chapter stories; skip it for tightly
   continuous or very short books.

7. **Verify.** Use the **fidelity-review** skill to confirm the manuscript stayed
   true to the task and the process and didn't diverge, pad, or hallucinate —
   checking it against the spec, outline, story bible, dossier, and research. It
   reports issues and the fixes it made and loops until the work is clean or the
   user overrides. Run it after editing, before packaging. On a clean pass, set
   `status: "verified"`.

8. **Final review (optional, the pre-publish gate).** Use the **review-panel** skill
   for a last sanity check: a panel of several independent reviewers reads the whole
   manuscript the way human editors and beta readers would, and the skill reports the
   problems they agree on (plot gaps, weak twists, continuity, pacing, spelling and
   grammar) with a READY / NOT-READY verdict. It is read-only; hand confirmed issues
   back to **book-editor** and re-run. Heavy (several full reads), so reserve it for
   when the book is believed finished. Offer it before packaging anything for release.
   When the panel returns READY, set `status: "reviewed"`.

9. **Preflight check (go/no-go gate).** Before any publishing work, run the
   **preflight-check** skill: a fast, read-only reconciliation (`scripts/preflight.py`
   plus a judgment pass) that confirms the book is complete and the earlier gates closed
   clean — every outline chapter has a real, non-empty file, no `TODO`/`TK`/placeholder
   markers remain, the title and **author** are filled, the `front-matter/` manifest
   resolves, and `review-report.md` / `fidelity-report.md` show no open items. It writes
   `preflight-report.md` with a **GO / HOLD** verdict. On HOLD, route each blocking item
   to the owning skill (book-editor, fidelity-review, review-panel, front-matter, or the
   author) and re-run; only a GO proceeds. Set `status: "verified"`/`"reviewed"` as
   appropriate.

10. **Package.** Build the finished deliverable into `dist/`. **First, if the book needs a
   proper title page or front/back matter** (and to fill the author and any
   subtitle/series/copyright metadata), use the **front-matter** skill — it sets the
   `book.json` fields and writes the `front-matter/` folder, which all three packagers
   then include. Ask which format(s)
   the user wants: use the **epub-packager** skill for an EPUB (e-readers), the
   **docx-packager** skill for a Microsoft Word `.docx` (editable), and/or the
   **pdf-packager** skill for a print-ready `.pdf` (it renders the `.docx` through an
   installed engine such as Microsoft Word or LibreOffice). All read the same folder,
   so you can produce any combination. Report the output path(s). Set
   `status: "packaged"`.

11. **Publishing prep (optional).** For a self-publishing run:
    - Use the **back-cover-blurb** skill to write the marketing copy (blurb, book
      description, tagline, hook) into `blurb.md`, in the book's voice and honoring the
      spoiler wall. Do this first — it can set `book.json`'s `description`, and the
      categorizer reads the blurb.
    - Use the **amazon-book-categorizer** skill to recommend KDP browse categories,
      subcategories, and the seven KDP search keywords from the book's metadata, written
      to `amazon-categories.md` for pasting into the KDP dashboard. It works from the
      book's own metadata, not live Amazon ranks, so present its picks as choices to
      confirm in the KDP category picker.
    - Use the **cover-designer** skill to write a cover brief and Midjourney prompts into
      `cover-brief.md`, then hand off to the **midjourney-images** skill to generate the
      art. Offer these once the book is settled.

## Principles

- **Checkpoints over autopilot.** The expensive, hard-to-undo steps are drafting
  and editing. Get sign-off on the outline before drafting and on the voice
  before drafting in bulk. This is where a book goes right or wrong.
- **Fewer, better passes.** Every subtractive edit pass regresses the prose a little toward
  a safe, rule-compliant mean, and voice is the first thing it costs. Run the minimum the
  draft actually needs, not the maximum the suite offers. The five-editor **editor-ensemble**
  is opt-in for the chapters that earn it, not an every-chapter default; a freshly drafted
  chapter gets the three light passes that apply to every chapter, **clarity-edit**,
  **propulsion-editor**, then **ai-ism-editor**. Reach for the full ensemble when a chapter is genuinely weak, not by
  reflex. A book run through every available pass comes out cleaner
  and flatter than one that got the few passes it needed.
- **Files are the interface.** Everything a stage needs is on disk. If the user
  comes back tomorrow, any stage can resume by reading the folder.
- **Stay modular.** If the user only wants to re-run one stage (e.g., "rewrite
  chapter 3" or "repackage after I edited the files"), invoke just that stage's
  skill against the existing folder.
- **Every run is logged.** Each skill records its run to `audit-log.md` (and
  `audit-log.jsonl`) in the book folder — that it ran, its result (pass/fail or
  verdict), the items it went through, and the outputs it wrote. The shared logger and
  format live in `lib/audit_log.py` / `lib/AUDIT-LOG.md`. Read `audit-log.md` to see
  everything that has happened to a book at a glance.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill book-machine --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
