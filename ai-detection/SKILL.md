---
name: ai-detection
description: Checks whether a manuscript reads as AI-generated and helps make it read human. A read-only heuristic scan (scripts/ai_likelihood.py) scores each chapter on the signals that correlate with machine writing — uniform sentence length (low burstiness), AI-ism and signature-word density, sentence-initial transitions, hedging, em dashes, low lexical diversity — and reports a reads-as-AI / mixed / reads-as-human band with the worst passages, written to ai-detection-report.md; fixes loop back through prose-style and book-editor. Use whenever the user wants an AI-detection check, to confirm content reads as human (not AI), to humanize or de-AI prose, lower an AI score, or check writing before submitting it somewhere that screens for AI. It is a heuristic, not a real detector, and cannot run or guarantee GPTZero/Originality.ai/Turnitin — it documents how to run one yourself.
---

# AI Detection

A check that drafted prose reads as written by a person, not a machine, and a loop to
fix it where it doesn't. It pairs with **prose-style**: that skill *removes* AI tells,
this one *measures* whether they're gone and points at what's left. It is **read-only**:
it scores and reports; `prose-style` and `book-editor` do the rewriting.

## What this can and can't do — read first

- It is a **heuristic**, not a detector. It scores the *tells* that make writing read as
  AI (see below). It does **not** run, replicate, or predict **GPTZero, Originality.ai,
  Turnitin, Copyleaks**, or any commercial tool, and there is no network or API key in
  this environment to call one.
- **A low score is not proof.** Those tools are themselves statistically unreliable and
  routinely false-positive on genuinely human writing (including classic literature and
  non-native-English authors). Never tell the user a text is "confirmed to pass" — say it
  *reads as human by these signals*, and that any real-world check is the detector's call.
- **The fix is genuine humanizing, never gaming.** Do not insert typos, gibberish,
  invisible characters, or unicode tricks to fool a detector. Make the prose actually more
  human (specific detail, varied rhythm, real voice); that is what both serves the reader
  and lowers detector flags.

## Run the script

```
scripts/ai_likelihood.py
```

Stdlib only, read-only, advisory (exits 0):

```bash
python scripts/ai_likelihood.py <book-folder>
```

It prints, per chapter and as a book average, a **0–100 risk score**, the sentence-length
**burstiness** (humans vary; AI is uniform), lexical diversity, and a band:
**reads as human (<33) / mixed (33–66) / reads as AI (>66)** — plus the chapters to look
at first with their top contributing factors.

## What it measures

- **Burstiness** — variation in sentence length. The strongest single tell: AI writes
  uniformly; human writing mixes long and short.
- **AI-ism & signature-word density** — catalogued phrases (`a testament to`,
  `navigate the complexities`, `rich tapestry`) and words (`delve, leverage, robust,
  seamless, myriad`) per 1,000 words, drawn from the prose-style catalog.
- **Sentence-initial transitions** — `However, Moreover, Furthermore, Additionally,
  In conclusion` openings, an essay-AI habit.
- **Hedging density**, **em dashes per 1,000 words**, and **lexical diversity**.

## The loop

1. **Scan** the manuscript with the script.
2. **Read the flags as direction, not verdict.** A high score points at chapters to work;
   a single tell isn't damning, and some uniformity is genre-appropriate.
3. **Fix by humanizing** — hand the flagged passages to **prose-style** (strip the AI
   tells, vary the rhythm, choose concrete detail) and **book-editor** (apply across the
   manuscript). Never "fix" by degrading the text.
4. **Re-scan** until it reads as human or the user accepts the result. Record the run in
   `ai-detection-report.md` (per-chapter scores, the factors, what was changed).

## Checking a real detector (optional, user-driven)

When the user genuinely needs a commercial score (a publisher, school, or platform that
screens), they run the text through the detector themselves — it can't be done from here:

- Paste the chapter into a tool (e.g. GPTZero, Originality.ai), or use its API with their
  own key if they have one.
- Bring the result back and record it in `ai-detection-report.md` alongside the heuristic
  score. Treat a flag as a prompt to humanize further, not as ground truth — and warn the
  user about false positives before they act on any single number.

## `ai-detection-report.md`

Write the report to the project folder: the per-chapter heuristic scores and bands, the
top factors per flagged chapter, any external-detector results the user supplied, what was
changed, and a one-line summary. Keep it honest about the heuristic's limits.

## Relationship to the other skills

- **prose-style** — the fixer of AI tells (em dashes, AI-isms, show-don't-tell, vague
  placeholders). This skill measures whether the prose still reads as AI and routes the
  work; prose-style does it.
- **style-check** — overlaps on the granular metrics (adverbs, echoes, sentence length);
  this skill combines the AI-specific signals into a single reads-as-AI verdict and adds
  the external-detector workflow. Run either or both before editing.
- **book-editor** — applies the humanizing fixes across the manuscript.
- **book-machine** — offer it in the Edit/verify stage, after drafting, alongside
  style-check; re-run after the editor.

## What it is not

Not a real AI detector, not a guarantee, and not a fixer. It is a read-only humanness
check that finds the machine tells and sends them to the skills that remove them.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill ai-detection --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
