---
name: epub-packager
description: Assembles a folder of finished chapter files into a valid, downloadable EPUB ebook using a bundled Python script. Use whenever the user wants to package, build, export, compile, or generate an EPUB or ebook file from written chapters, turn a manuscript into a readable .epub, or produce the final deliverable of a book. This is the final stage of the book-machine pipeline; it works standalone on any folder following the book project layout.
---

# EPUB Packager

Assemble written chapters into a standards-compliant EPUB 3 file. EPUB assembly
is a fixed, fiddly format problem (a ZIP with a required internal layout, an
uncompressed `mimetype` entry first, a package manifest, and a navigation
document). It should be done by a deterministic script, not improvised — so this
skill ships one.

## Don't hand-build the EPUB — run the script

Use the bundled builder:

```
scripts/build_epub.py
```

It needs only Python 3 (standard library — no pip installs). Run it pointed at
the book project folder:

```bash
python scripts/build_epub.py <book-folder>
```

If `<book-folder>` is omitted it uses the current directory. Useful flags:

- `--out <path>` — write the EPUB to a specific file (default
  `<book-folder>/dist/<slug>.epub`).
- `--title`, `--author` — override what's in `book.json`.

Run it from the skill directory, or pass the script's absolute path — e.g.
`python ~/.claude/skills/epub-packager/scripts/build_epub.py ./my-book`.

## What the script expects (the project-folder contract)

```
<book-folder>/
├── book.json        # { title, author, language, ... }  (optional but recommended)
├── outline.json     # { title, chapters: [{ id, title, ... }] }  → source of order & titles
└── chapters/
    ├── 01-*.md      # one markdown file per chapter
    └── 02-*.md
```

- **Order and titles** come from `outline.json` when present; each outline entry
  is matched to the chapter file whose name starts with its `id`. If there's no
  `outline.json`, the script falls back to every `chapters/*.md` sorted by
  filename, taking each chapter's title from its leading `# ` heading.
- **Chapter bodies** are markdown: blank-line-separated paragraphs, `## `
  subheadings, and `**bold**` / `*italic*`. A leading `# Title` line is treated
  as the chapter title and not duplicated in the body.

## Formatting (configurable per book)

The look of the EPUB is controlled by an optional `formatting` object in
`book.json`. Omit it and you get the classic novel look — a drop cap on each
chapter's first paragraph, justified + hyphenated text, indented paragraphs with
no blank line between them, and a centered chapter number + rule above a
small-caps title. Override any field per book:

```json
{
  "title": "...",
  "author": "...",
  "formatting": {
    "dropCap": true,
    "justify": true,
    "hyphenate": true,
    "paragraphIndent": true,
    "chapterNumber": true,
    "chapterTitleCase": "small-caps",
    "bodyFont": "serif"
  }
}
```

| Field | Values | Default | Effect |
|-------|--------|---------|--------|
| `dropCap` | `true` / `false` | `true` | Large decorative initial on each chapter's first paragraph (that paragraph isn't indented) |
| `justify` | `true` / `false` | `true` | Justified body text vs. left-aligned |
| `hyphenate` | `true` / `false` | `true` | Allow hyphenation (best paired with `justify`) |
| `paragraphIndent` | `true` / `false` | `true` | `true` = first-line indent, no blank line between paragraphs (classic prose); `false` = block paragraphs with spacing |
| `chapterNumber` | `true` / `false` | `true` | Centered chapter number + short rule above the title |
| `chapterTitleCase` | `"small-caps"` / `"uppercase"` / `"normal"` | `"small-caps"` | Case styling of the chapter title |
| `bodyFont` | `"serif"` / `"sans"` | `"serif"` | Body typeface family |

The script reports which options were applied in its summary line.

**Drop caps** are rendered as a large serif initial via a `<span class="dropcap">`
plus a CSS float — the portable, reliable approach across readers. A true
*ornamental / swash* drop cap (a decorative display face) would require **embedding
a font** in the EPUB, which this script does not do yet — mention it if you want
font embedding added.

**Reader caveat:** EPUB readers ultimately control rendering and can override
fonts, justification, and hyphenation in their own settings, so the exact look
varies by device. The CSS sets the intent; most readers honor it.

## Front and back matter (optional)

If the book project folder has a `front-matter/` folder with a `front-matter.json`
manifest (written by the **front-matter** skill), the builder adds each piece as its
own XHTML page in the spine: **front** matter (copyright, dedication, epigraph, …)
between the title page and the contents, **back** matter (about-the-author,
acknowledgments, …) after the last chapter. They are styled by type and stay out of the
nav/TOC. The title page also picks up `subtitle` and `series` from `book.json`. With no
`front-matter/` folder the EPUB builds exactly as before — the feature is additive.

## After running

The script prints the output path and a summary (chapter count, byte size).
Relay that to the user and point them at the `.epub` — it opens in Apple Books,
Calibre, Kindle (via conversion), and other readers. If `book.json` exists,
update its `status` to `"packaged"`.

## If something's missing

- No chapters found → the book hasn't been drafted; use the **chapter-writer**
  skill first.
- A chapter referenced by the outline has no matching file → the script warns and
  skips it; tell the user which chapter is missing so they can draft it.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill epub-packager --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
