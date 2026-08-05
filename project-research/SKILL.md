---
name: project-research
description: Captures and organizes per-book research and source material into the book project folder (research.md plus a research/ folder), so the writing and editing stages can draw on it and stay accurate. Use whenever the user wants to add research, notes, facts, sources, references, background, or source documents to a book project; says "use my research when you write," pastes material to base the book on, or starts a project that has supporting research. Applies to fiction (grounding real-world detail) and non-fiction (the source material itself). For actively gathering new research from the web, hand off to the deep-research skill, then store the results here.
---

# Project Research

A per-book research library. The user supplies research — pasted notes, facts, links,
or source files — and this skill organizes it into the project folder so the
**chapter-writer, outline-designer, and book-editor can read it and get the details
right.** Research is the factual ground the book stands on: real history, technical
specifics, geography, domain background, interview notes, source quotes.

This is distinct from the **story-bible** (which holds the *invented* rules of a
fictional world). Research is *real* source material. A historical novel might have
both: a Story Bible for its invented characters and plot, and Research for how a
1890s telegraph office actually worked.

## Where it lives

In the book project folder, beside `book.json`, `outline.json`, and `chapters/`:

```
research.md      # the writer-facing digest — organized facts the writing treats as ground truth
research/        # (optional) raw source material: clippings, notes, reference docs, transcripts
  <source>.md
```

`research.md` is the canonical, curated file the writing stages read first. The
`research/` folder holds bulkier raw sources to consult for depth.

## `research.md` structure

```markdown
# Research — <Project Title>

## How to use this
Factual material this book draws on. Treat the claims here as ground truth: don't
contradict them, and when a scene or section touches one of these topics, get the
specifics right.

## <Topic / theme>
- Concrete fact, detail, or figure. (source: <where it came from>)
- ...

## <Another topic>
- ...

## Open questions / to verify
- Things still unconfirmed — flag these so the writing hedges or the user resolves them.

## Sources
- <label> — link, citation, or the file under research/ it lives in.
```

## How to capture research

The user brings the material; your job is to organize it into something the writing
can actually use.

1. **Take it in whatever form it arrives** — pasted text, a list of facts, URLs, or
   a pointer to files. Drop substantial raw sources into `research/` as their own
   files; distill the usable facts into `research.md` under clear topic headings.
2. **Distill to usable specifics.** The writer needs concrete, checkable details
   (dates, names, figures, how-a-thing-works), not walls of text. Summarize long
   sources into the key facts and keep the raw source in `research/` for reference.
3. **Attribute and flag confidence.** Note where each fact came from in the Sources
   list. Put anything uncertain under "Open questions / to verify" so the writing
   doesn't state a guess as fact.
4. **Never invent facts.** If the user's research doesn't cover something the book
   needs, say so — list it under open questions rather than filling the gap. If they
   want it researched, hand off to the **deep-research** skill and store what it
   returns here (with sources).
5. **Keep it current.** Support adding more over time: "add this to the research,"
   "what do we know about X?", "log this source." Append and reorganize; don't
   clobber existing notes.

## How the rest of the machine uses it

When `research.md` exists, the writing stages treat it as factual ground truth:
- **outline-designer** shapes the structure to cover what the research supports.
- **chapter-writer** draws on it for accurate detail and does not contradict it; if
  a needed fact is missing, it writes around the gap rather than inventing, and flags
  it.
- **book-editor** checks factual claims in the prose against it.

Best added **at the start of a project, when research is available and appropriate** —
before outlining — so the book is built on it from the first chapter. Not every book
needs it; skip when there's nothing to ground.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill project-research --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
