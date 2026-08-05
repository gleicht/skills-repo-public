---
name: fidelity-review
description: A self-verification pass that audits written work to confirm it stayed true to the task and the process and did not diverge, pad, or hallucinate. It checks the output against the project's sources of truth (book.json spec, outline.json, story-bible.md, characters.json, research.md) and the user's original request, produces a report of every issue found and the corrective measure taken, then re-runs until no issues remain — or until the user overrides it. Use whenever the user wants to verify, audit, fact-check, or quality-check written work; confirm it stuck to the plan; check for drift, scope creep, made-up facts, or contradictions; or as the final verification gate before a book is finished or packaged.
---

# Fidelity Review

A verification gate. After work has been written, this pass confirms it is **true to
the task, true to the process, and free of invention**. It is not a craft edit (that
is the book-editor's job) — it is a QA audit that catches divergence and hallucination,
fixes what it can, reports honestly, and keeps going until the work is clean or the
user calls it.

## The sources of truth

"True" means consistent with the established record. Read these first; they are the
yardstick. Never change them to match the prose — if the prose disagrees, the prose
is what's wrong (unless the user says a source is out of date).

- **The user's original request / task** — what was actually asked for, including scope.
- **`book.json`** — topic, audience, tone, language, intended length.
- **`outline.json`** — the chapters that should exist and what each should cover.
- **`story-bible.md`** — world rules, voice & style, plot beats (no violations, no off-plot invention).
- **`characters.json`** — character facts, motivation, and secrets (no drift, no early reveals).
- **`research.md`** — factual ground truth (no contradictions, nothing invented beyond it).
- **The prior written content itself** — internal consistency across chapters/sections.

For non-book work, the yardstick is the stated task, the agreed process, and any
provided source material.

## What to look for — the four issue types

1. **Divergence from the task / scope.** Content that wasn't asked for, topic drift,
   padding, tangents, or quietly expanded scope. Did it stick to *this* task?
2. **Process deviation.** A pipeline step skipped or run out of order; a review
   checkpoint ignored; a stage's source of truth not actually consulted.
3. **Hallucination / unsupported content.** Facts not in `research.md`; world details
   that contradict `story-bible.md`; character actions that contradict
   `characters.json`; plot events not in the beats; invented sources, names, figures,
   or citations; claims stated with confidence that nothing supports.
4. **Spec mismatch.** Tone, audience, reading level, length, POV/tense, or format that
   doesn't match `book.json`, the Voice & Style Guide, or the request.

## How to run the audit

1. Load the sources of truth above.
2. Go through the written work systematically — chapter by chapter, section by section.
   For each, compare against the relevant source: does it cover what the outline
   promised, obey the bible, match the dossier, stay within the research, fit the spec?
3. Check the **run as a whole** against the original task: was the process followed,
   was the scope honored, did anything drift.
4. Record every issue with its location, type, and severity.

## Corrective measures

For each issue, take the smallest fix that restores fidelity, and record it:

- **Divergence** → cut or refocus the off-task material; restore the intended scope.
- **Process deviation** → run the missed step (or flag that it must be run).
- **Hallucination** → remove or correct the unsupported content. If the book genuinely
  needs the fact, do **not** invent it — flag it as a gap for the user (or hand to
  project-research / deep-research).
- **Spec mismatch** → bring the prose back to the spec.

**Never "resolve" an issue by fabricating, by deleting required content, or by editing
a source of truth to match a mistake.** A fix must make the work *actually* faithful,
not just make the warning disappear. If the source of truth itself looks wrong or
outdated, surface that to the user rather than deciding unilaterally.

## The report

After each pass, produce a report (present it to the user and save the latest to
`fidelity-report.md` in the project folder):

```markdown
# Fidelity Review — <Project> — pass <N>

## Verdict: PASS  |  ISSUES FOUND (<count> open)  |  HALTED (user override)

## Findings
| # | Type | Location | Severity | Issue | Corrective measure | Status |
|---|------|----------|----------|-------|--------------------|--------|
| 1 | Hallucination | ch.3 ¶2 | high | States the base has 40 crew; research says 12 | Corrected to 12 | Fixed |
| 2 | Divergence | ch.5 | med | Subplot not in the outline | Flagged — needs user call | Open |

## Summary
- Checked: <what against what>
- Fixed this pass: <n>   ·   Still open: <n>
- Next: re-run / done / awaiting user decision on items [..]
```

Keep the report concrete: name the issue, where it is, and exactly what you changed.

## The loop, and the stop conditions

Repeat **audit → fix → re-audit** until one of these is true:

- **Clean** — a full pass finds zero open issues. Report PASS and stop.
- **User override** — the user says "accept as is," "override," "stop the review,"
  "ship it," or similar. Stop immediately, report HALTED, and list any issues left
  open so the decision is on the record. The user can override at any time.
- **No progress (safeguard)** — if an issue survives two or three passes, or fixing
  one issue keeps spawning others, **stop looping**. Don't thrash or burn the budget.
  Report the specific blocker and ask the user how to proceed.

Each pass must either resolve issues or make clear progress. Some issues (a subplot
that may or may not belong, a fact the research doesn't cover) are **judgment calls
that belong to the user** — flag those rather than "fixing" them yourself.

## Relationships and notes

- **book-editor** handles craft (flow, tone, repetition, prose style). **fidelity-review**
  handles truth and process. Run the editor for quality; run this to verify honesty.
  Order: usually edit first, then verify.
- It reads, but never rewrites, the source-of-truth files.
- **Automation:** this skill loops to resolution *within* an invocation. To make it
  fire automatically after every drafting stage (rather than when invoked), that's a
  Claude Code **hook** in settings.json — a separate setup the user can request.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill fidelity-review --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
