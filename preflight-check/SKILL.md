---
name: preflight-check
description: A final pre-publish sanity check — a fast, read-only reconciliation pass that confirms a finished book is actually ready before the publishing workflow runs. It checks that every outline chapter has a real, non-empty file in order with no orphans or gaps, that no placeholder or TODO/TK markers remain in the prose, that the metadata is complete (title and author filled — no unsigned book), that the front-matter manifest resolves, and that the prior QA gates closed out — review-panel READY, fidelity-review PASS with no open items — then writes preflight-report.md with a GO / HOLD verdict. Read-only: it reports and hands fixes back to the right skill. Use whenever the user wants a sanity check, a pre-flight or pre-publish check, a final reconciliation or readiness pass, a go/no-go gate, or wants to confirm nothing is left unaddressed before packaging or publishing. Runs after the editing and review gates, just before front-matter, packaging, and publishing prep.
---

# Preflight Check

The last walk-through before a book enters the publishing workflow. Where the other
gates each hunt for a specific class of problem, this one confirms the book is **whole,
internally reconciled, and that every prior finding has been closed** — the checklist a
careful author runs before committing to produce files. It answers one question: *is
there anything left unaddressed before we publish?*

It is **read-only**: it produces a report and a **GO / HOLD** verdict and never edits
the book. Remediation goes back to the skill that owns it.

## Where it sits, and how it differs from the other gates

Run it **after** editing and the review gates, **before** front-matter, packaging, and
publishing prep. It is a meta-gate that *consumes* the others' results rather than
repeating their work:

- **deduplicator** finds duplicated content. **fidelity-review** checks the prose
  against its sources of truth (and fixes/loops). **review-panel** judges craft and the
  reader experience.
- **preflight-check** confirms the book is **complete and reconciled** and that those
  gates **closed clean** — it does not re-audit truth or re-review craft. If a gate was
  never run, or left an open item, preflight is what catches it.

## Run the script — the deterministic checklist

```
scripts/preflight.py
```

Stdlib only. Point it at the book project folder:

```bash
python scripts/preflight.py <book-folder>
```

It prints a checklist of `[PASS] / [WARN] / [FAIL]` items and a final **GO / HOLD**
line, and **exits non-zero on any FAIL** so it can gate a build. It covers what can be
checked mechanically:

- **Chapters** — `chapters/*.md` exist; numbering is sequential with no duplicates or
  gaps; no empty chapters; very short (stub) chapters flagged.
- **Placeholders** — no leftover `TODO / FIXME / TBD / XXX / TK` markers in the prose
  (FAIL), and bracketed editorial notes or `lorem ipsum` flagged (WARN).
- **Metadata** — `book.json` has a title and a non-blank **author** (a blank author is a
  FAIL — the book would publish unsigned).
- **Outline reconciliation** — every `outline.json` chapter maps to a file; orphan files
  not in the outline are flagged.
- **Front-matter** — if a `front-matter/` manifest exists, every referenced piece file
  is present.
- **Prior gates** — `review-report.md` is present and not `NOT READY`; `fidelity-report.md`
  is present with no `Open` rows and no `ISSUES FOUND` / `HALTED` verdict. A missing
  report is a WARN ("verify it was run").

## The judgment layer — what the script can't see

After the script is clean, do the reconciliation a script can't:

- **Cast vs dossier.** Spot-check that characters named in the prose match
  `characters.json` (names, spellings, relationships); no stragglers or renamed
  characters.
- **Fair-play & twists.** If the book has a `clues.md` ledger or a spoiler-walled
  `SOLUTION`, confirm every intended reveal is actually seeded by the chapter it claims,
  and the "fairness watch" items are resolved — the panel checks this too, but preflight
  confirms it's *closed*.
- **Series threads.** For a book in a series, check the **series-bible** open-threads
  list: anything that was meant to pay off in *this* book actually did, and the series
  bible has been reconciled to the finished text.
- **Spec match.** Title/subtitle/series in `book.json` match the title page and the
  outline; the status reflects reality.
- **Open items from the reports.** Read `review-report.md` and `fidelity-report.md` and
  confirm each listed issue is genuinely addressed, not just marked done.

## The report and the verdict

Write `preflight-report.md` to the project folder: the checklist, the items still open
with the skill that should fix each, and the one-line verdict.

- **GO** — everything reconciles and the prior gates closed clean. Clear for front-matter,
  packaging, and publishing prep.
- **HOLD** — one or more blocking items remain. Name each and route it: prose
  duplication or craft → **book-editor**; truth/spec drift → **fidelity-review**;
  reader/plot problems → **review-panel**; missing title page or author → **front-matter**;
  a missing chapter or placeholder text → the author / **chapter-writer**.

Then summarize the verdict and the blocking items to the user. **Never edit the book** —
hand each issue to the owning skill and re-run preflight after the fixes for a clean gate.

## Relationship to the other skills

- **book-machine.** Offer this as the gate between the review stage and the publishing
  workflow; a GO is the green light to start front-matter and packaging.
- **fidelity-review / review-panel / deduplicator.** Preflight reads their outputs and
  confirms closure; it does not duplicate their analysis.
- **front-matter.** A common HOLD is a blank author or absent front matter — fix there,
  then re-run.
- It reads, but never writes, the manuscript and the source-of-truth files.

## What this is not

Not a craft review (that's **review-panel**), not a truth audit (that's
**fidelity-review**), and not a fixer. It is the final reconciliation checklist that
confirms nothing was left undone before the book goes to print.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill preflight-check --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
