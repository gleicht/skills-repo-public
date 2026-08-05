---
name: pdf-packager
description: Build a print-ready PDF of a finished book from the book project folder, by rendering the packaged .docx through an installed document engine (Microsoft Word or LibreOffice). Use alongside epub-packager and docx-packager when the user wants a PDF deliverable.
---

# PDF Packager

Assemble a finished book into a PDF. A faithful PDF needs real pagination, page
numbers, a populated table of contents, and font layout, so this skill does **not**
hand-roll a PDF. Instead it builds the book's `.docx` with the **docx-packager** and
converts that to PDF with whatever document engine is installed, in order of
fidelity. This keeps a single source of truth: the same title page, author, TOC, and
formatting you get in the `.docx` carry straight into the PDF.

## Don't hand-build the PDF — run the script

```
scripts/build_pdf.py
```

Needs only Python 3 plus one of the conversion engines below. Run it pointed at the
book project folder:

```bash
python scripts/build_pdf.py <book-folder>
```

If `<book-folder>` is omitted it uses the current directory. Useful flags:

- `--out <path>` — write to a specific file (default `<book-folder>/dist/<slug>.pdf`).
- `--docx <path>` — convert an already-built `.docx` instead of building a fresh one.
- `--engine auto|word|libreoffice` — force an engine (default `auto`).
- `--toc` / `--no-toc` — force the table of contents on/off in the built `.docx`
  (otherwise inherited from `book.json` `formatting.docxToc`).
- `--keep-docx` — keep the intermediate `.docx` the script builds (default: deleted
  when this script built it; never deletes a `--docx` you passed in).

Run from the skill directory or pass the script's absolute path, e.g.
`python ~/.claude/skills/pdf-packager/scripts/build_pdf.py ./my-book --out ./my-book/dist/my-book.pdf`.

## Conversion engines (auto-detected, best first)

1. **Microsoft Word (COM automation, Windows)** — highest fidelity. The script opens
   the `.docx` headless, updates the table-of-contents field and all page-number
   fields, and exports a PDF. This is what makes the TOC show real page numbers.
2. **LibreOffice** (`soffice --headless --convert-to pdf`) — cross-platform. Found on
   `PATH` or at the usual install locations.
3. **Fallback (manual):** if neither is installed, the script stops after building the
   `.docx` and tells you where it is. Convert it yourself with pandoc + a LaTeX engine,
   or any "Print to PDF" / "Save as PDF" in a word processor.

`auto` picks Word on Windows when available, else LibreOffice.

## What it produces

A PDF mirroring the `.docx`: a title page (title + author, plus subtitle/series when
set), any front and back matter (see the **front-matter** skill — it flows in through
the `.docx`), each chapter starting on its own page, a table of contents with working
page numbers (when one is enabled), serif body text, and page numbers in the footer.

## After running

The script prints the output path, byte size, and which engine it used. Relay that and
point the user at the `.pdf`. If the engine was Word or LibreOffice, the TOC page
numbers are already baked in; if a reader opens the source `.docx` instead, those
fields update on open.

## If something's missing

- No chapters found → the book hasn't been drafted; use **chapter-writer** first.
- No engine found → install Microsoft Word or LibreOffice, or convert the `.docx` the
  script leaves behind (it prints the path).
- TOC shows placeholder text in the PDF → the conversion engine didn't refresh fields;
  re-run with `--engine word` on Windows, or open the `.docx` in Word and export.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill pdf-packager --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
