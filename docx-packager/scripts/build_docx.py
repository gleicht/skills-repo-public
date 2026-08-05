#!/usr/bin/env python3
"""Build a Word (.docx) document from a book project folder.

Standard library only — no python-docx, no Node. A .docx is a ZIP of XML parts
(OOXML / WordprocessingML); this writes the minimal valid set of parts directly.

Expects the book-machine project layout:

    <book-folder>/
      book.json        (optional)  title, author, language
      outline.json     (optional)  authoritative chapter order + titles
      chapters/*.md    one markdown file per chapter

Order/titles come from outline.json when present (each entry matched to the
chapter file whose name starts with its `id`); otherwise every chapters/*.md
is used, sorted by filename, titled from its leading "# " heading.

Output mirrors the rest of the machine: title page, each chapter on its own
page, serif body with first-line indents, page numbers in the footer.

A table of contents (Word TOC field over the chapter headings, with clickable
links and page numbers Word/LibreOffice fill in on open) can be added with --toc,
or per-book via book.json "formatting": { "docxToc": true }.

Usage:
    python build_docx.py [book-folder] [--out PATH] [--title T] [--author A]
                         [--toc | --no-toc]
"""

import argparse
import html
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles default to cp1252 and crash on non-ASCII (accented titles).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# ---------- markdown-ish parsing ----------

def parse_inline(text: str):
    """Return a list of (text, bold, italic) runs from **bold**/*italic* markup."""
    runs = []
    for tok in re.findall(r"\*\*[^*]+\*\*|\*[^*]+\*|[^*]+", text):
        if tok.startswith("**") and tok.endswith("**"):
            runs.append((tok[2:-2], True, False))
        elif tok.startswith("*") and tok.endswith("*"):
            runs.append((tok[1:-1], False, True))
        else:
            runs.append((tok, False, False))
    return runs or [(text, False, False)]


def strip_leading_h1(body: str):
    lines = body.replace("\r\n", "\n").lstrip("\n").split("\n")
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return body


def run_xml(text: str, bold=False, italic=False) -> str:
    rpr = ""
    if bold or italic:
        rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def runs_xml(text: str) -> str:
    return "".join(run_xml(t, b, i) for t, b, i in parse_inline(text))


def para(text, style=None, page_break=False, justify=False, indent=False):
    """One <w:p>. pPr children must follow schema order: pStyle, pageBreakBefore,
    spacing, ind, jc."""
    ppr = ""
    if style:
        ppr += f'<w:pStyle w:val="{style}"/>'
    if page_break:
        ppr += "<w:pageBreakBefore/>"
    if indent:
        ppr += '<w:ind w:firstLine="360"/>'
    if justify:
        ppr += '<w:jc w:val="both"/>'
    ppr = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr}{runs_xml(text)}</w:p>"


def body_paragraphs(body: str, justify: bool = False):
    out = []
    blocks = [b.strip() for b in re.split(r"\n{2,}", body.replace("\r\n", "\n"))]
    for block in [b for b in blocks if b]:
        m = re.match(r"^(#{1,6})\s+(.*)$", block)
        if m:
            out.append(para(m.group(2), style="Heading2"))
        elif len(block) <= 12 and re.fullmatch(r"[\*·• ]+", block) and re.search(r"[\*·•]", block):
            # A scene-break / time-demarcation line: centered, literal "* * *".
            out.append('<w:p><w:pPr><w:spacing w:before="240" w:after="240"/>'
                       '<w:jc w:val="center"/></w:pPr>'
                       '<w:r><w:t xml:space="preserve">* * *</w:t></w:r></w:p>')
        else:
            out.append(para(block.replace("\n", " "), justify=justify, indent=True))
    return out


# ---------- front / back matter (optional front-matter/ folder) ----------

def front_matter_paragraphs(piece, justify=False):
    """Render one front/back-matter piece to a list of <w:p>. The piece starts on a
    fresh page (the first paragraph carries the page break) and is styled by its `type`.
    Titles are bold-centered, NOT a Heading style, so the matter stays out of the
    chapter table of contents."""
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

    out, pb_used = [], False
    if title is not None:
        out.append('<w:p><w:pPr><w:pageBreakBefore/>'
                   '<w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/></w:pPr>'
                   f'<w:r><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>'
                   f'<w:t xml:space="preserve">{esc(title)}</w:t></w:r></w:p>')
        pb_used = True

    for blk in blocks:
        flat = blk.replace("\n", " ")
        lead_pb = ""
        if not pb_used:
            lead_pb, pb_used = "<w:pageBreakBefore/>", True
        if ptype in ("dedication", "epigraph"):
            before = "2400" if (ptype == "dedication" and lead_pb) else "160"
            out.append(f'<w:p><w:pPr>{lead_pb}'
                       f'<w:spacing w:before="{before}" w:after="160"/><w:jc w:val="center"/></w:pPr>'
                       f'<w:r><w:rPr><w:i/></w:rPr>'
                       f'<w:t xml:space="preserve">{esc(flat)}</w:t></w:r></w:p>')
        elif ptype == "copyright":
            out.append(f'<w:p><w:pPr>{lead_pb}<w:spacing w:after="80"/></w:pPr>'
                       f'<w:r><w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                       f'<w:t xml:space="preserve">{esc(flat)}</w:t></w:r></w:p>')
        elif ptype == "also-by":
            out.append(f'<w:p><w:pPr>{lead_pb}<w:spacing w:after="80"/>'
                       f'<w:jc w:val="center"/></w:pPr>{runs_xml(flat)}</w:p>')
        else:
            ppr = lead_pb + '<w:ind w:firstLine="360"/>'
            if justify:
                ppr += '<w:jc w:val="both"/>'
            out.append(f'<w:p><w:pPr>{ppr}</w:pPr>{runs_xml(flat)}</w:p>')
    return out


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


# ---------- static parts ----------

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="240" w:after="360"/><w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>
</w:styles>"""

FOOTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="{W}">
  <w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:fldSimple w:instr=" PAGE "><w:r><w:t>1</w:t></w:r></w:fldSimple></w:p>
</w:ftr>"""

APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Book Machine</Application>
</Properties>"""


def settings_xml(update_fields: bool) -> str:
    # updateFields tells Word/LibreOffice to recalculate fields (the TOC, page
    # numbers) when the document is opened, so the TOC populates without the reader
    # having to press F9.
    upd = '<w:updateFields w:val="true"/>' if update_fields else ""
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<w:settings xmlns:w="{W}">{upd}</w:settings>')


def toc_paragraphs():
    """A 'Contents' heading (deliberately not a Heading style, so it is not itself a
    TOC entry) followed by a Word TOC field spanning the chapter Heading1s. The field
    carries placeholder text until the reader's word processor updates fields on open
    (see settings_xml). \\o "1-1" = outline level 1 only, \\h = clickable links,
    \\z = suppress page numbers in web view, \\u = use outline levels."""
    heading = ('<w:p><w:pPr><w:pageBreakBefore/>'
               '<w:spacing w:before="240" w:after="240"/><w:jc w:val="center"/></w:pPr>'
               '<w:r><w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>'
               '<w:t xml:space="preserve">Contents</w:t></w:r></w:p>')
    field = ('<w:p>'
             '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
             '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-1" \\h \\z \\u </w:instrText></w:r>'
             '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
             '<w:r><w:t xml:space="preserve">Right-click and choose Update Field '
             '(or press F9) to build the table of contents.</w:t></w:r>'
             '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
             '</w:p>')
    return [heading, field]


def core_xml(title, author):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{esc(title)}</dc:title>
  <dc:creator>{esc(author or "Book Machine")}</dc:creator>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>"""


def document_xml(title, author, chapters, justify=False, transitions=None, toc=False,
                 subtitle="", series=None, front_matter=None):
    parts = []
    # Title page
    parts.append('<w:p><w:pPr><w:spacing w:before="3200"/></w:pPr></w:p>')
    parts.append(para(title, style="Title"))
    if subtitle:
        parts.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="200"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(subtitle)}</w:t></w:r></w:p>'
        )
    if author:
        parts.append(
            f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(author)}</w:t></w:r></w:p>'
        )
    if series and series.get("name"):
        num = series.get("number")
        line = series["name"] + (f", Book {num}" if num else "")
        parts.append(
            f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="200"/></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(line)}</w:t></w:r></w:p>'
        )
    # Front matter (after the title page, before the TOC/chapters)
    if front_matter:
        for piece in front_matter.get("front", []):
            parts.extend(front_matter_paragraphs(piece, justify))
    # Table of contents (its own page, after the title page, before chapter 1)
    if toc:
        parts.extend(toc_paragraphs())
    # Chapters
    for idx, ch in enumerate(chapters):
        parts.append(para(ch["title"], style="Heading1", page_break=True))
        parts.extend(body_paragraphs(ch["body"], justify=justify))
        # A transition renders after its `after` chapter, only when a later chapter follows.
        if transitions and idx < len(chapters) - 1:
            trans = transitions.get(ch.get("id"))
            if trans:
                parts.extend(transition_paragraphs(trans["prose"], trans["appearance"], justify))
    # Back matter (after the last chapter)
    if front_matter:
        for piece in front_matter.get("back", []):
            parts.extend(front_matter_paragraphs(piece, justify))
    sect = (
        "<w:sectPr>"
        '<w:footerReference w:type="default" r:id="rId2"/>'
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0"/>'
        "</w:sectPr>"
    )
    return (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>'
        + "".join(parts)
        + sect
        + "</w:body></w:document>"
    )


# ---------- chapter collection (same contract as the EPUB packager) ----------

def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:60] or "book"


def collect_chapters(folder: Path):
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
            match = next(
                (f for f in md_files if f.stem == cid or f.name.startswith(cid + "-")),
                None,
            )
            if not match:
                print(f"  ! warning: no file for chapter id '{cid}' "
                      f"('{entry.get('title', '')}') - skipping", file=sys.stderr)
                continue
            result.append({"id": cid, "title": entry.get("title") or cid,
                            "body": strip_leading_h1(match.read_text(encoding="utf-8"))})
        if result:
            return result
    for f in md_files:
        raw = f.read_text(encoding="utf-8")
        heading, body = (raw.splitlines()[0][2:].strip(), strip_leading_h1(raw)) \
            if raw.lstrip().startswith("# ") else (f.stem, raw)
        result.append({"id": f.stem.split("-")[0], "title": heading, "body": body})
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


def para_setoff(text: str, justify: bool) -> str:
    """A set-off transition paragraph: italic by default, with inline *emphasis*
    toggled back to roman (correct typography inside an italic block)."""
    ppr = '<w:ind w:firstLine="360"/>'
    if justify:
        ppr += '<w:jc w:val="both"/>'
    runs = "".join(run_xml(t, b, not i) for t, b, i in parse_inline(text))
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p>"


def transition_paragraphs(prose: str, appearance: str, justify: bool):
    blocks = [b.strip() for b in re.split(r"\n{2,}", prose.replace("\r\n", "\n")) if b.strip()]
    out = []
    if appearance == "set-off":
        out.append('<w:p><w:pPr><w:spacing w:before="240" w:after="200"/>'
                   '<w:jc w:val="center"/></w:pPr>'
                   '<w:r><w:t xml:space="preserve">· · ·</w:t></w:r></w:p>')
        out.extend(para_setoff(b.replace(chr(10), " "), justify) for b in blocks)
    else:
        out.extend(para(b.replace(chr(10), " "), justify=justify, indent=True) for b in blocks)
    return out


def build(folder: Path, out: Path, title_override, author_override, toc_override=None):
    book = {}
    if (folder / "book.json").is_file():
        book = json.loads((folder / "book.json").read_text(encoding="utf-8"))
    chapters = collect_chapters(folder)
    if not chapters:
        print("No chapters found. Draft the book first (chapter-writer skill).",
              file=sys.stderr)
        return 1

    transitions = load_transitions(folder)

    title = title_override or book.get("title") or "Untitled Book"
    author = author_override or book.get("author") or ""

    # Table of contents: --toc/--no-toc wins; otherwise book.json formatting.docxToc.
    toc = toc_override if toc_override is not None \
        else bool(book.get("formatting", {}).get("docxToc", False))

    # Body alignment. Default is LEFT-aligned (ragged right) — standard manuscript
    # format. Opt into full justification per-book with formatting.docxJustify=true.
    # Kept separate from the EPUB's formatting.justify so the book-form EPUB can stay
    # justified while the manuscript DOCX is left-aligned.
    justify = bool(book.get("formatting", {}).get("docxJustify", False))

    subtitle = book.get("subtitle") or ""
    series = book.get("series") or None
    # `series` may be a plain string (with a separate `seriesOrder`) or an
    # object {name, number}. Normalize the string form into the object shape.
    if isinstance(series, str):
        series = {"name": series, "number": book.get("seriesOrder")}
    front_matter = load_front_matter(folder)

    if out is None:
        out = folder / "dist" / f"{slugify(title)}.docx"
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml",
                   document_xml(title, author, chapters, justify, transitions, toc,
                                subtitle, series, front_matter))
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/footer1.xml", FOOTER)
        z.writestr("word/settings.xml", settings_xml(toc))
        z.writestr("docProps/core.xml", core_xml(title, author))
        z.writestr("docProps/app.xml", APP_XML)

    size = out.stat().st_size
    print(f"Built DOCX: {out}")
    print(f"  {len(chapters)} chapter(s), {size:,} bytes")
    print(f"  Title: {title}" + (f"  by {author}" if author else ""))
    print(f"  Body alignment: {'justified' if justify else 'left-aligned (ragged right)'}")
    print(f"  Table of contents: {'yes (update fields on open)' if toc else 'no'}")
    if front_matter:
        print(f"  Front/back matter: {len(front_matter.get('front', []))} front, "
              f"{len(front_matter.get('back', []))} back piece(s)")
    rendered = sum(1 for i, ch in enumerate(chapters)
                   if i < len(chapters) - 1 and transitions.get(ch.get("id")))
    if rendered:
        print(f"  Transitions: {rendered} rendered between chapters")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Build a .docx from a book project folder.")
    ap.add_argument("folder", nargs="?", default=".", help="Book project folder (default: current dir)")
    ap.add_argument("--out", help="Output .docx path (default: <folder>/dist/<slug>.docx)")
    ap.add_argument("--title", help="Override the book title")
    ap.add_argument("--author", help="Override the author")
    ap.add_argument("--toc", dest="toc", action="store_true", default=None,
                    help="Insert a table of contents page (after the title page)")
    ap.add_argument("--no-toc", dest="toc", action="store_false",
                    help="Omit the table of contents (overrides book.json)")
    args = ap.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Not a directory: {folder}", file=sys.stderr)
        return 1
    out = Path(args.out).resolve() if args.out else None
    return build(folder, out, args.title, args.author, args.toc)


if __name__ == "__main__":
    raise SystemExit(main())
