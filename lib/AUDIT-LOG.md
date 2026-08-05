# Audit log — shared convention

Every book-machine skill records each run to an **audit log** in the book project folder,
so there is a trail of what happened: that the skill ran, when, whether it passed or
failed (or its verdict), the items it ran through, and the outputs it wrote.

Two files, both in the book folder, both append-only:
- **`audit-log.md`** — human-readable, one entry per run, oldest first.
- **`audit-log.jsonl`** — the same entries as JSON lines, for tooling.

## How a skill logs a run

At the **end** of a run, call the shared logger (`lib/audit_log.py`) once:

```bash
python <skills-dir>/lib/audit_log.py \
  --skill <this-skill-name> \
  --target <book-folder> \
  --status <PASS | FAIL | DONE | GO | HOLD | READY | NOT-READY | verdict> \
  --item "<each thing processed>"   # repeat --item per item, or --items "a, b, c"
  --output "<each file written>"    # repeat --output, or --outputs "x, y"; omit if read-only
  --note "<one-line summary>"
```

`<skills-dir>` is the personal skills directory, e.g. `~/.claude/skills` (on Windows,
`C:/Users/<you>/.claude/skills`). The logger stamps the real local time itself.

Pick `--status` to match the skill:
- gates/checks → their verdict: `PASS`/`FAIL` (fidelity-review), `GO`/`HOLD`
  (preflight-check), `READY`/`NOT-READY` (review-panel), or the band (ai-detection).
- builders/editors with no pass/fail → `DONE`.

`--item` is the list of things the run went through — usually the chapters scanned or the
file(s) operated on (e.g. each `chapters/NN-*.md`). `--output` is each file the run wrote
(reports, edited proposals, packaged files); omit for a read-only run that wrote nothing.

## Example

```bash
python ~/.claude/skills/lib/audit_log.py --skill style-check --target ./my-book \
  --status DONE --item 01-intro.md --item 02-rising.md --output style-report.md \
  --note "2 chapters; adverb density 5.1% flagged"
```

## If the logger isn't reachable

If `lib/audit_log.py` can't be run (a skill copied out on its own), append the same
entry to `audit-log.md` by hand in the format above. The point is the trail, not the tool.

## Reading it

Open `audit-log.md` for the chronological history of every skill run on the book; parse
`audit-log.jsonl` if you want to filter or summarize runs programmatically.

## Emailing the log (on demand)

`lib/email_audit_log.py` emails a book's `audit-log.md` over SMTP, on demand:

```bash
python <skills-dir>/lib/email_audit_log.py --book <book-folder> [--to addr] [--latest] [--dry-run]
```

- `--dry-run` composes and prints the email without sending (no credentials needed).
- `--latest` sends only the most recent run entry instead of the whole log.

**Setup (one time):** copy `lib/email_config.example.json` to `lib/email_config.json`
(gitignored — never committed) and fill in SMTP details. Easiest is a personal Gmail with
2-Step Verification + an **App Password** as `smtp_pass`. Any SMTP provider works; or set
the `AUDIT_SMTP_*` env vars instead of the file. Emailing sends the log (which can include
manuscript file names and snippets) out through your provider — intentional, but worth knowing.

