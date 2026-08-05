---
name: docx-packager
description: Assembles a folder of finished chapter files into a Microsoft Word (.docx) document using a bundled, dependency-free Python script. Use whenever the user wants a Word version of a book or manuscript, to export, package, or convert chapters to .docx or Word format, or to produce an editable Word deliverable alongside (or instead of) the EPUB. This is an output stage of the book-machine pipeline; it works standalone on any folder following the book project layout.
---

# DOCX Packager

Assemble written chapters into a Microsoft Word document. Like EPUB, a `.docx`
is a ZIP with a required internal XML layout (OOXML) — fiddly and easy to get
subtly wrong by hand — so this skill ships a deterministic builder rather than
improvising the format each time.

## Don't hand-build the .docx — run the script

Use the bundled builder:

```
scripts/build_docx.py
```

It needs only Python 3 (standard library — **no python-docx, no Node, no
installs**). Run it pointed at the book project folder:

```bash
python scripts/build_docx.py <book-folder>
```

If `<book-folder>` is omitted it uses the current directory. Useful flags:

- `--out <path>` — write to a specific file (default `<book-folder>/dist/<slug>.docx`).
- `--title`, `--author` — override what's in `book.json` (handy for filling in a
  blank author without editing the file).
- `--toc` / `--no-toc` — add or omit a table of contents page (otherwise taken from
  `book.json` `formatting.docxToc`; default off).

Run it from the skill directory or pass the script's absolute path — e.g.
`python ~/.claude/skills/docx-packager/scripts/build_docx.py ./my-book`.

## What the script expects (the project-folder contract)

Identical to the EPUB packager, so the two are interchangeable outputs:

```
<book-folder>/
├── book.json        # { title, author, ... }  (optional but recommended)
├── outline.json     # { title, chapters: [{ id, title, ... }] }  → source of order & titles
└── chapters/
    ├── 01-*.md      # one markdown file per chapter
    └── 02-*.md
```

- **Order and titles** come from `outline.json` when present (each entry matched
  to the chapter file whose name starts with its `id`); otherwise every
  `chapters/*.md` sorted by filename, titled from its leading `# ` heading.
- **Chapter bodies** are markdown: blank-line-separated paragraphs, `## `
  subheadings, and `**bold**` / `*italic*`. A leading `# Title` line is treated
  as the chapter title and not duplicated in the body.

## What it produces

A Word document with a **title page** (title + author), an **optional table of
contents** page (see below), **each chapter starting on its own page**, serif body
text (Georgia) with first-line indents, and **page numbers** in the footer. Body text
is **left-aligned (ragged right) by default** — standard manuscript format. It opens
in Microsoft Word, Google Docs, LibreOffice, and Pages, and stays fully editable.

The table of contents is a real Word **TOC field** over the chapter headings, with
clickable links and page numbers. The builder also writes a `settings.xml` that tells
the word processor to refresh fields on open, so the TOC populates itself (no manual
F9 needed in Word/LibreOffice). Until refreshed, it shows a one-line placeholder.

## Front and back matter (optional)

If the book project folder has a `front-matter/` folder with a `front-matter.json`
manifest (written by the **front-matter** skill), this builder renders those pieces:
**front** matter (copyright, dedication, epigraph, …) after the title page and before
the chapters, **back** matter (about-the-author, acknowledgments, …) after the last
chapter, each on its own page and kept out of the table of contents. It also reads
`subtitle` and `series` from `book.json` for the title page. With no `front-matter/`
folder the document builds exactly as before — the feature is purely additive.

## Formatting (configurable per book)

The DOCX reads one key from the optional `formatting` object in `book.json`:

| Field | Values | Default | Effect |
|-------|--------|---------|--------|
| `docxJustify` | `true` / `false` | `false` | Full justification vs. left-aligned (ragged right, manuscript format) |
| `docxToc` | `true` / `false` | `false` | Insert a table of contents page after the title page |

```json
{ "title": "...", "author": "...", "formatting": { "docxJustify": true, "docxToc": true } }
```

This is kept **separate** from the EPUB's `formatting.justify` (which defaults to
`true`) on purpose, so the book-form EPUB can stay justified while the manuscript
DOCX stays left-aligned. The script reports the applied alignment in its summary.

## After running

The script prints the output path and a summary (chapter count, byte size).
Relay that and point the user at the `.docx`. Note that the page-number field in
the footer displays correctly in Word/LibreOffice; some lightweight viewers show
it only after the document recalculates fields on open.

## If something's missing

- No chapters found → the book hasn't been drafted; use the **chapter-writer**
  skill first.
- A chapter referenced by the outline has no matching file → the script warns and
  skips it; tell the user which chapter is missing.
- The TOC shows placeholder text instead of entries → the viewer hasn't refreshed
  fields; open in Word/LibreOffice (which refresh on open), or press F9. For a PDF
  with the TOC already baked in, use the **pdf-packager** skill, which refreshes the
  field before exporting.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill docx-packager --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
