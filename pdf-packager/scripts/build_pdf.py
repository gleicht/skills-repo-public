#!/usr/bin/env python3
"""Build a PDF of a book project by rendering the packaged .docx to PDF.

A faithful PDF needs a real layout/pagination engine (page numbers, a populated
table of contents, justified text, fonts). Rather than re-implement one, this
skill reuses the docx-packager output and hands it to whatever document engine is
installed, in order of fidelity:

  1. Microsoft Word (COM automation, Windows) - best fidelity; updates the TOC
     field and page numbers, then exports PDF.
  2. LibreOffice (soffice --headless --convert-to pdf) - cross-platform.
  3. (documented fallback) pandoc + a LaTeX engine, if you prefer that pipeline.

It first builds the .docx with the sibling docx-packager (so author, TOC, and
formatting all come through), then converts that .docx to .pdf.

Project-folder contract is identical to the epub-/docx-packagers:

    <book-folder>/
      book.json        (optional)  title, author, formatting
      outline.json     (optional)  chapter order + titles
      chapters/*.md    one markdown file per chapter

Usage:
    python build_pdf.py [book-folder] [--out PATH] [--docx PATH]
                        [--engine auto|word|libreoffice] [--toc | --no-toc]
                        [--keep-docx]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:60] or "book"


def docx_builder_path() -> Path:
    """The sibling docx-packager build script, resolved within the skills suite
    (skills/pdf-packager/scripts/build_pdf.py -> skills/docx-packager/scripts/...)."""
    return Path(__file__).resolve().parents[2] / "docx-packager" / "scripts" / "build_docx.py"


def build_docx(folder: Path, out_docx: Path, toc) -> None:
    builder = docx_builder_path()
    if not builder.is_file():
        raise FileNotFoundError(
            f"Could not find docx-packager build script at {builder}. "
            "Pass an already-built file with --docx instead.")
    cmd = [sys.executable, str(builder), str(folder), "--out", str(out_docx)]
    if toc is True:
        cmd.append("--toc")
    elif toc is False:
        cmd.append("--no-toc")
    subprocess.run(cmd, check=True)


# ---------- converters ----------

def find_soffice():
    for name in ("soffice", "libreoffice"):
        p = shutil.which(name)
        if p:
            return p
    for cand in (
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
    ):
        if Path(cand).exists():
            return cand
    return None


def word_available() -> bool:
    if sys.platform != "win32":
        return False
    ps = "try { $w = New-Object -ComObject Word.Application; $w.Quit(); 'yes' } catch { 'no' }"
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=60)
        return "yes" in r.stdout
    except Exception:
        return False


def convert_with_word(in_path: Path, out_path: Path) -> None:
    """Open in Word, refresh the TOC + fields, export PDF (wdExportFormatPDF = 17)."""
    ip = str(in_path.resolve())
    op = str(out_path.resolve())
    ps = f"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open("{ip}", $false, $true)
try {{ foreach ($t in $doc.TablesOfContents) {{ $t.Update() }} }} catch {{}}
try {{ $doc.Fields.Update() | Out-Null }} catch {{}}
$doc.ExportAsFixedFormat("{op}", 17)
$doc.Close($false)
$word.Quit()
"""
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], check=True)


def convert_with_libreoffice(soffice: str, in_path: Path, out_path: Path) -> None:
    outdir = out_path.parent
    outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                    "--outdir", str(outdir), str(in_path)], check=True)
    produced = outdir / (in_path.stem + ".pdf")
    if produced.resolve() != out_path.resolve():
        if produced.exists():
            produced.replace(out_path)


def main():
    ap = argparse.ArgumentParser(description="Build a PDF from a book project folder.")
    ap.add_argument("folder", nargs="?", default=".", help="Book project folder (default: current dir)")
    ap.add_argument("--out", help="Output .pdf path (default: <folder>/dist/<slug>.pdf)")
    ap.add_argument("--docx", help="Use this existing .docx instead of building one")
    ap.add_argument("--engine", choices=("auto", "word", "libreoffice"), default="auto",
                    help="Conversion engine (default: auto - Word, then LibreOffice)")
    ap.add_argument("--toc", dest="toc", action="store_true", default=None,
                    help="Force a table of contents in the built .docx")
    ap.add_argument("--no-toc", dest="toc", action="store_false",
                    help="Omit the table of contents in the built .docx")
    ap.add_argument("--keep-docx", action="store_true",
                    help="Keep the intermediate .docx (when this script builds it)")
    args = ap.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Not a directory: {folder}", file=sys.stderr)
        return 1

    # Output path
    if args.out:
        out_pdf = Path(args.out).resolve()
    else:
        title = folder.name
        try:
            import json
            if (folder / "book.json").is_file():
                title = json.loads((folder / "book.json").read_text(encoding="utf-8")).get("title") or title
        except Exception:
            pass
        out_pdf = folder / "dist" / f"{slugify(title)}.pdf"
    out_pdf.parent.mkdir(parents=True, exist_ok=True)

    # Resolve the .docx (reuse or build)
    built_here = False
    if args.docx:
        docx = Path(args.docx).resolve()
        if not docx.is_file():
            print(f"--docx not found: {docx}", file=sys.stderr)
            return 1
    else:
        docx = out_pdf.with_suffix(".docx")
        print("Building intermediate .docx ...")
        build_docx(folder, docx, args.toc)
        built_here = True

    # Choose engine
    engine = args.engine
    soffice = find_soffice()
    if engine == "auto":
        engine = "word" if word_available() else ("libreoffice" if soffice else None)
    elif engine == "word" and not word_available():
        print("Microsoft Word COM is not available on this machine.", file=sys.stderr)
        return 1
    elif engine == "libreoffice" and not soffice:
        print("LibreOffice (soffice) was not found.", file=sys.stderr)
        return 1

    if engine is None:
        print("No PDF engine found. Install Microsoft Word or LibreOffice, or convert\n"
              f"the already-built .docx manually:\n  {docx}\n"
              "(e.g. pandoc with a LaTeX engine, or any 'Print to PDF').", file=sys.stderr)
        return 1

    print(f"Converting to PDF with {engine} ...")
    try:
        if engine == "word":
            convert_with_word(docx, out_pdf)
        else:
            convert_with_libreoffice(soffice, docx, out_pdf)
    except subprocess.CalledProcessError as e:
        print(f"PDF conversion failed ({engine}): {e}", file=sys.stderr)
        return 1

    if built_here and not args.keep_docx:
        try:
            docx.unlink()
        except OSError:
            pass

    if not out_pdf.is_file():
        print("Conversion reported success but no PDF was produced.", file=sys.stderr)
        return 1
    size = out_pdf.stat().st_size
    print(f"Built PDF: {out_pdf}")
    print(f"  {size:,} bytes  (engine: {engine})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
