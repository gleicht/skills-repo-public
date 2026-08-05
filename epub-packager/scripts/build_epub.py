#!/usr/bin/env python3
"""Build a valid EPUB 3 from a book project folder.

Standard library only. The book folder is expected to follow the
book-machine project layout:

    <book-folder>/
      book.json        (optional)  metadata: title, author, language, ...
      outline.json     (optional)  authoritative chapter order + titles
      chapters/*.md    one markdown file per chapter

Order/titles come from outline.json when present (each entry matched to the
chapter file whose name starts with its `id`); otherwise every chapters/*.md
is used, sorted by filename, titled from its leading "# " heading.

Usage:
    python build_epub.py [book-folder] [--out PATH] [--title T] [--author A]
"""

import argparse
import html
import json
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# On Windows the console defaults to cp1252, which crashes on non-ASCII output
# (book titles with accents, etc.). Force UTF-8 and never hard-fail on a glyph.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ---------- per-book formatting (book.json "formatting" object) ----------

# Defaults give the classic novel look: drop cap on the chapter's first
# paragraph, justified + hyphenated body, indented paragraphs with no blank line
# between them, and a centered chapter number + rule + small-caps title. Any of
# these can be overridden per book via a "formatting" object in book.json.
DEFAULT_FMT = {
    "dropCap": True,            # ornamental large initial on each chapter's first paragraph
    "justify": True,           # justified body text (vs. left-aligned)
    "hyphenate": True,         # allow hyphenation (pairs well with justify)
    "paragraphIndent": True,   # first-line indent + no blank line between paragraphs
    "chapterNumber": True,     # centered chapter number with a rule above the title
    "chapterTitleCase": "small-caps",  # "small-caps" | "uppercase" | "normal"
    "bodyFont": "serif",       # "serif" | "sans"
}


def load_formatting(book: dict) -> dict:
    """Merge the book.json 'formatting' object over the defaults."""
    fmt = dict(DEFAULT_FMT)
    user = book.get("formatting")
    if isinstance(user, dict):
        fmt.update({k: v for k, v in user.items() if k in DEFAULT_FMT})
    return fmt


# ---------- markdown-ish -> XHTML ----------

def escape(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    """Escape, then re-introduce the small set of inline tags we allow."""
    out = escape(text)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(^|[^*])\*([^*]+)\*", r"\1<em>\2</em>", out)
    return out


def body_to_xhtml(body: str, drop_cap: bool = False) -> str:
    """Blank-line-separated blocks -> <p>; '#'-prefixed lines -> headings.

    The chapter's first paragraph gets class="first" (no indent), and — when
    drop_cap is on and it begins with a letter — its initial is wrapped in a
    <span class="dropcap"> for the large decorative initial.
    """
    blocks = [b.strip() for b in re.split(r"\n{2,}", body.replace("\r\n", "\n"))]
    blocks = [b for b in blocks if b]
    parts = []
    first_para = True
    for block in blocks:
        m = re.match(r"^(#{1,6})\s+(.*)$", block)
        if m:
            level = min(len(m.group(1)) + 1, 6)  # '#' -> h2, so chapter H1s don't clash
            parts.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue
        sb = block.strip()
        if len(sb) <= 12 and re.fullmatch(r"[\*·• ]+", sb) and re.search(r"[\*·•]", sb):
            # A scene-break / time-demarcation line (e.g. "* * *" or "·  ·  ·").
            # Render it centered, literal, never through the italic parser.
            parts.append('<p class="scene-break">* * *</p>')
            continue
        text = block.replace(chr(10), " ")
        if first_para:
            first_para = False
            dm = re.match(r"^(\s*)(\w)(.*)$", text, re.S)
            if drop_cap and dm and dm.group(2).isalpha():
                initial, rest = dm.group(2), dm.group(3)
                parts.append(
                    f'<p class="first"><span class="dropcap">{escape(initial)}</span>'
                    f"{inline(rest)}</p>"
                )
            else:
                parts.append(f'<p class="first">{inline(text)}</p>')
        else:
            parts.append(f"<p>{inline(text)}</p>")
    return "\n".join(parts)


def strip_leading_h1(body: str):
    """Pull a leading '# Title' line off the body; return (title_or_None, rest)."""
    lines = body.replace("\r\n", "\n").lstrip("\n").split("\n")
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).lstrip("\n")
    return None, body


# ---------- document templates ----------

def chapter_xhtml(title: str, body: str, number: int, fmt: dict, transition=None) -> str:
    bits = []
    if fmt.get("chapterNumber", True):
        bits.append(f'<p class="chapter-number">{number}</p>')
        bits.append('<hr class="chapter-rule" />')
    bits.append(f'<h1 class="chapter-title">{escape(title)}</h1>')
    bits.append(body_to_xhtml(body, drop_cap=fmt.get("dropCap", True)))
    if transition:
        bits.append(transition_to_xhtml(transition["prose"], transition["appearance"]))
    inner = "\n    ".join(bits)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <section class="chapter">
    {inner}
  </section>
</body>
</html>"""


def title_xhtml(title: str, author: str, subtitle: str = "", series=None) -> str:
    author_line = f'<p class="book-author">{escape(author)}</p>' if author else ""
    subtitle_line = f'<p class="book-subtitle">{escape(subtitle)}</p>' if subtitle else ""
    series_line = ""
    if series and series.get("name"):
        num = series.get("number")
        s = series["name"] + (", Book %d" % num if num else "")
        series_line = f'<p class="book-series">{escape(s)}</p>'
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <section class="titlepage">
    <h1 class="book-title">{escape(title)}</h1>
    {subtitle_line}
    {author_line}
    {series_line}
  </section>
</body>
</html>"""


def frontmatter_xhtml(piece) -> str:
    """One front/back-matter piece as its own XHTML page. Styled by `type` via CSS
    classes; uses <h2>, never <h1>, so it stays out of the chapter nav/TOC."""
    ptype = piece.get("type", "")
    body = piece.get("body", "").replace("\r\n", "\n")
    blocks = [b.strip() for b in re.split(r"\n{2,}", body) if b.strip()]
    title = None
    if blocks and re.match(r"^#{1,6}\s+", blocks[0]):
        title = re.sub(r"^#{1,6}\s+", "", blocks[0]).strip()
        blocks = blocks[1:]
    if title is None:
        title = {"acknowledgments": "Acknowledgments",
                 "about-author": "About the Author"}.get(ptype)
    cls = {"dedication": "fm-dedication", "epigraph": "fm-epigraph",
           "copyright": "fm-copyright", "also-by": "fm-also-by"}.get(ptype, "fm-generic")
    bits = []
    if title is not None:
        bits.append(f'<h2 class="fm-title">{escape(title)}</h2>')
    bits.extend(f"<p>{inline(b.replace(chr(10), ' '))}</p>" for b in blocks)
    inner = "\n    ".join(bits)
    page_title = title or (ptype.replace("-", " ").title() if ptype else "Front Matter")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(page_title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <section class="frontmatter {cls}">
    {inner}
  </section>
</body>
</html>"""


def load_front_matter(folder: Path):
    """Read the optional front-matter/front-matter.json manifest and its files.
    Returns {"front": [...], "back": [...]} of {type, body}, or None if absent."""
    fm_dir = folder / "front-matter"
    manifest = fm_dir / "front-matter.json"
    if not manifest.is_file():
        return None
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None

    def load_list(key):
        items = []
        for entry in data.get(key, []) or []:
            fn = entry.get("file")
            f = fm_dir / fn if fn else None
            if not f or not f.is_file():
                print(f"  front-matter: missing '{fn}' - skipping", file=sys.stderr)
                continue
            items.append({"type": entry.get("type", ""),
                          "body": f.read_text(encoding="utf-8")})
        return items

    return {"front": load_list("front"), "back": load_list("back")}


def nav_xhtml(title: str, chapters) -> str:
    items = "\n".join(
        f'      <li><a href="chapter-{i + 1}.xhtml">{escape(ch["title"])}</a></li>'
        for i, ch in enumerate(chapters)
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <meta charset="utf-8" />
  <title>{escape(title)} — Contents</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Contents</h1>
    <ol>
{items}
    </ol>
  </nav>
</body>
</html>"""


def content_opf(meta, chapters, front=None, back=None) -> str:
    front = front or []
    back = back or []
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    desc = (
        f"<dc:description>{escape(meta['description'])}</dc:description>"
        if meta.get("description")
        else ""
    )
    xh = "application/xhtml+xml"
    manifest = "\n".join(
        [
            '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
            '    <item id="css" href="style.css" media-type="text/css" />',
            '    <item id="titlepage" href="title.xhtml" media-type="application/xhtml+xml" />',
            *[f'    <item id="front-{i + 1}" href="front-{i + 1}.xhtml" media-type="{xh}" />'
              for i in range(len(front))],
            *[
                f'    <item id="chapter-{i + 1}" href="chapter-{i + 1}.xhtml" media-type="application/xhtml+xml" />'
                for i in range(len(chapters))
            ],
            *[f'    <item id="back-{i + 1}" href="back-{i + 1}.xhtml" media-type="{xh}" />'
              for i in range(len(back))],
        ]
    )
    # Reading order: title page, front matter, contents, chapters, back matter.
    spine = "\n".join(
        [
            '    <itemref idref="titlepage" />',
            *[f'    <itemref idref="front-{i + 1}" />' for i in range(len(front))],
            '    <itemref idref="nav" />',
            *[f'    <itemref idref="chapter-{i + 1}" />' for i in range(len(chapters))],
            *[f'    <itemref idref="back-{i + 1}" />' for i in range(len(back))],
        ]
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{escape(meta['identifier'])}</dc:identifier>
    <dc:title>{escape(meta['title'])}</dc:title>
    <dc:language>{escape(meta['language'])}</dc:language>
    <dc:creator>{escape(meta.get('author') or 'Anonymous')}</dc:creator>
    {desc}
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
{manifest}
  </manifest>
  <spine>
{spine}
  </spine>
</package>"""


CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>"""

SERIF = '"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif'
SANS = 'system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'


def build_css(fmt: dict) -> str:
    """Generate OEBPS/style.css from the per-book formatting options."""
    body_font = SANS if fmt.get("bodyFont") == "sans" else SERIF
    align = "justify" if fmt.get("justify", True) else "left"
    indent = "1.4em" if fmt.get("paragraphIndent", True) else "0"
    # Indented style = no blank line between paragraphs; block style = spaced.
    p_margin = "0" if fmt.get("paragraphIndent", True) else "0 0 0.9em"
    hyph = (
        "hyphens: auto; -webkit-hyphens: auto; -epub-hyphens: auto; adobe-hyphenate: auto;"
        if fmt.get("hyphenate", True)
        else "hyphens: manual;"
    )
    title_case = {
        "small-caps": "font-variant: small-caps; letter-spacing: 0.04em;",
        "uppercase": "text-transform: uppercase; letter-spacing: 0.08em;",
    }.get(fmt.get("chapterTitleCase", "small-caps"), "")

    lines = [
        f"body {{ font-family: {body_font}; line-height: 1.5; margin: 6% 7%; color: #1a1a1a; }}",
        f"h1, h2, h3 {{ font-family: {body_font}; line-height: 1.3; }}",
        ".titlepage { text-align: center; margin-top: 30%; }",
        ".book-title { font-size: 2.2em; margin-bottom: 0.4em; }",
        ".book-subtitle { font-size: 1.3em; font-style: italic; color: #555; margin: 0 0 0.8em; }",
        ".book-author { font-size: 1.2em; font-style: italic; color: #555; }",
        ".book-series { font-size: 1em; color: #777; margin-top: 1.2em; }",
        ".frontmatter p { text-indent: 0; margin: 0 0 0.8em; }",
        ".fm-title { text-align: center; font-size: 1.4em; margin: 1.4em 0 1.6em; }",
        ".fm-dedication { text-align: center; font-style: italic; margin-top: 30%; }",
        ".fm-epigraph { text-align: center; font-style: italic; margin-top: 16%; }",
        ".fm-copyright { font-size: 0.85em; color: #444; }",
        ".fm-copyright p { text-align: left; }",
        ".fm-also-by { text-align: center; }",
        ".chapter-number { text-align: center; font-size: 1em; color: #444; margin: 2.5em 0 0.4em; }",
        ".chapter-rule { width: 2em; margin: 0 auto 1.6em; border: 0; border-top: 1px solid #888; }",
        f".chapter-title {{ text-align: center; font-weight: bold; font-size: 1.3em; margin: 0 0 2.4em; {title_case} }}",
        f"p {{ margin: {p_margin}; text-align: {align}; text-indent: {indent}; {hyph} }}",
        "p.first { text-indent: 0; }",
        ".scene-break { text-align: center; text-indent: 0; margin: 1.6em 0; }",
        ".transition { margin: 2em 0 0; }",
        ".transition.setoff p { font-style: italic; }",
        ".transition-break { text-align: center; text-indent: 0; letter-spacing: 0.4em; "
        "color: #666; margin: 1.5em 0; font-style: normal; }",
    ]
    if fmt.get("dropCap", True):
        lines.append(
            f".dropcap {{ float: left; font-size: 3.4em; line-height: 0.78; "
            f"padding: 0.02em 0.08em 0 0; font-family: {body_font}; font-weight: normal; }}"
        )
    lines.append("nav ol { line-height: 2; }")
    return "\n".join(lines) + "\n"


# ---------- collecting chapters ----------

def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:60] or "book"


def collect_chapters(folder: Path):
    """Return an ordered list of {title, body}. Prefer outline.json for order."""
    chapters_dir = folder / "chapters"
    if not chapters_dir.is_dir():
        return []

    md_files = sorted(chapters_dir.glob("*.md"))
    outline_path = folder / "outline.json"
    result = []

    if outline_path.is_file():
        outline = json.loads(outline_path.read_text(encoding="utf-8"))
        for entry in outline.get("chapters", []):
            cid = str(entry.get("id", "")).strip()
            # Match a chapter file whose name starts with the id (e.g. "03-...").
            match = next(
                (f for f in md_files if f.stem == cid or f.name.startswith(cid + "-")),
                None,
            )
            if not match:
                print(f"  ! warning: no file for chapter id '{cid}' "
                      f"('{entry.get('title', '')}') - skipping", file=sys.stderr)
                continue
            raw = match.read_text(encoding="utf-8")
            _, body = strip_leading_h1(raw)
            result.append({"id": cid, "title": entry.get("title") or cid, "body": body})
        if result:
            return result
        # outline produced nothing usable; fall through to filename scan.

    for f in md_files:
        raw = f.read_text(encoding="utf-8")
        heading, body = strip_leading_h1(raw)
        title = heading or f.stem
        result.append({"id": f.stem.split("-")[0], "title": title, "body": body})
    return result


# ---------- transitions (optional transitions/ folder) ----------

def load_transitions(folder: Path):
    """Map of after-chapter-id -> {appearance, prose} for APPROVED brief/bridge
    transitions. Empty when there is no transitions/ folder."""
    tpath = folder / "transitions" / "transitions.json"
    if not tpath.is_file():
        return {}
    try:
        data = json.loads(tpath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out = {}
    for e in data.get("transitions", []):
        if e.get("status") != "approved" or e.get("decision") not in ("brief", "bridge"):
            continue
        gap = str(e.get("gap", "")).strip()
        after = str(e.get("after", "")).strip()
        prose_file = folder / "transitions" / f"{gap}.md"
        if not prose_file.is_file():
            print(f"  ! warning: approved transition '{gap}' has no {prose_file.name}; skipping",
                  file=sys.stderr)
            continue
        prose = prose_file.read_text(encoding="utf-8").strip()
        if prose:
            out[after] = {"appearance": e.get("appearance") or "seamless", "prose": prose}
    return out


def transition_to_xhtml(prose: str, appearance: str) -> str:
    blocks = [b.strip() for b in re.split(r"\n{2,}", prose.replace("\r\n", "\n")) if b.strip()]
    paras = "\n    ".join(f"<p>{inline(b.replace(chr(10), ' '))}</p>" for b in blocks)
    if appearance == "set-off":
        return ('<div class="transition setoff">\n'
                '    <p class="transition-break">· · ·</p>\n'
                f"    {paras}\n"
                "    </div>")
    return f'<div class="transition seamless">\n    {paras}\n    </div>'


# ---------- main ----------

def build(folder: Path, out: Path, title_override, author_override):
    book = {}
    book_json = folder / "book.json"
    if book_json.is_file():
        book = json.loads(book_json.read_text(encoding="utf-8"))

    fmt = load_formatting(book)

    chapters = collect_chapters(folder)
    if not chapters:
        print("No chapters found. Draft the book first (chapter-writer skill).",
              file=sys.stderr)
        return 1

    transitions = load_transitions(folder)

    title = title_override or book.get("title") or "Untitled Book"
    author = author_override or book.get("author") or ""
    language = book.get("language") or "en"
    description = book.get("topic") or book.get("description") or ""
    identifier = f"urn:uuid:{uuid.uuid4()}"

    subtitle = book.get("subtitle") or ""
    series = book.get("series") or None
    front_matter = load_front_matter(folder)
    front = front_matter.get("front", []) if front_matter else []
    back = front_matter.get("back", []) if front_matter else []

    meta = {
        "title": title,
        "author": author,
        "language": language,
        "identifier": identifier,
        "description": description,
    }

    if out is None:
        out = folder / "dist" / f"{slugify(title)}.epub"
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        # mimetype MUST be first and stored uncompressed.
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", CONTAINER_XML)
        z.writestr("OEBPS/content.opf", content_opf(meta, chapters, front, back))
        z.writestr("OEBPS/nav.xhtml", nav_xhtml(title, chapters))
        z.writestr("OEBPS/style.css", build_css(fmt))
        z.writestr("OEBPS/title.xhtml", title_xhtml(title, author, subtitle, series))
        for i, piece in enumerate(front):
            z.writestr(f"OEBPS/front-{i + 1}.xhtml", frontmatter_xhtml(piece))
        for i, piece in enumerate(back):
            z.writestr(f"OEBPS/back-{i + 1}.xhtml", frontmatter_xhtml(piece))
        rendered_transitions = 0
        for i, ch in enumerate(chapters):
            # A transition renders after its `after` chapter, only when a later
            # chapter follows it in this build.
            trans = transitions.get(ch.get("id")) if i < len(chapters) - 1 else None
            if trans:
                rendered_transitions += 1
            z.writestr(f"OEBPS/chapter-{i + 1}.xhtml",
                       chapter_xhtml(ch["title"], ch["body"], i + 1, fmt, trans))

    size = out.stat().st_size
    on = [name for name, key in (
        ("drop cap", "dropCap"), ("justified", "justify"), ("hyphenation", "hyphenate"),
        ("indented paragraphs", "paragraphIndent"), ("chapter numbers", "chapterNumber"),
    ) if fmt.get(key)]
    print(f"Built EPUB: {out}")
    print(f"  {len(chapters)} chapter(s), {size:,} bytes")
    print(f"  Title: {title}" + (f"  by {author}" if author else ""))
    print(f"  Formatting: {', '.join(on) or 'plain'}; "
          f"titles: {fmt.get('chapterTitleCase')}; font: {fmt.get('bodyFont')}")
    if rendered_transitions:
        print(f"  Transitions: {rendered_transitions} rendered between chapters")
    if front or back:
        print(f"  Front/back matter: {len(front)} front, {len(back)} back piece(s)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build an EPUB from a book project folder.")
    ap.add_argument("folder", nargs="?", default=".", help="Book project folder (default: current dir)")
    ap.add_argument("--out", help="Output .epub path (default: <folder>/dist/<slug>.epub)")
    ap.add_argument("--title", help="Override the book title")
    ap.add_argument("--author", help="Override the author")
    args = ap.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Not a directory: {folder}", file=sys.stderr)
        return 1
    out = Path(args.out).resolve() if args.out else None
    return build(folder, out, args.title, args.author)


if __name__ == "__main__":
    raise SystemExit(main())
