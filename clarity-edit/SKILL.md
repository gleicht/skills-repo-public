---
name: clarity-edit
description: A per-chapter clarity pass over a first draft. It reads a drafted chapter, finds prose that would confuse a reader — sentences that make no sense, wrong or awkward vocabulary, failed or mixed metaphors and similes, ambiguous pronouns and modifiers, and grammar so tangled it should be simplified — and produces both a report of every issue and a clarity-edited version of the chapter (written as a proposal in a clarity/ folder, never overwriting the draft). Use whenever the user wants a clarity pass or clarity edit, to fix confusing prose, simplify overly complex sentences, catch nonsensical or garbled lines, broken metaphors, or unclear wording in a chapter; it is meant to run right after a chapter is drafted. It honors the prose-style house rules and never invents meaning — where a sentence's intent is unclear it flags it for the author rather than guessing.
---

# Clarity Edit

The first cleanup a freshly drafted chapter gets: a focused line edit for **clarity** —
making sure a reader can actually follow every sentence. It is narrower and earlier than
the **book-editor** (which later polishes the whole manuscript for consistency, pacing,
and continuity). Run it per chapter, right after drafting, so the prose is comprehensible
before any of that.

Unlike the read-only diagnostics, this skill **edits**: it produces a report *and* a
clarity-edited version of the chapter. The edit is written as a **proposal** so the draft
is never lost.

## What it looks for

- **Sentences that make no sense** — lines that don't parse, contradict themselves, or
  state nothing. The hardest and most important category.
- **Wrong or awkward vocabulary** — a word used incorrectly (malapropism), a
  thesaurus-reach that misses the meaning, jargon a reader won't know, a register that
  clashes with the voice.
- **Failed metaphors & similes** — comparisons that don't illuminate, mixed metaphors
  ("a ticking time bomb waiting to explode into a snowball"), images that fight each
  other, or figures so clichéd they've gone invisible.
- **Overly complex grammar** — tangled, over-subordinated, or garden-path sentences and
  run-ons that can be split or restructured without losing meaning or rhythm.
- **Ambiguity** — pronouns with no clear antecedent ("it / they / this"), dangling or
  misplaced modifiers, who-did-what confusion.
- **Reader-stumble spots** — anywhere a first-time reader would have to stop and re-read
  to understand. The catch-all: if it trips the reader, flag it.
- *(Chapter-local only — cross-chapter continuity and facts are the book-editor's and
  fidelity-review's job.)*

## How to run it

1. **Get the complexity candidates first** (the deterministic half):
   ```bash
   python scripts/complexity_flags.py <chapter.md | book-folder>
   ```
   It lists the longest and most heavily subordinated sentences — split/simplify
   candidates. The script judges *complexity only*; it cannot judge sense, vocabulary,
   or metaphor.
2. **Read the chapter for the rest** — nonsense, vocabulary, failed figures, ambiguity.
   These need human/LLM judgment, line by line.
3. **Fix where intent is clear; flag where it isn't.** Simplify the tangled sentence,
   correct the wrong word, repair or cut the broken metaphor, resolve the ambiguous
   pronoun. **When a sentence is genuinely unintelligible and you cannot tell what it
   was meant to say, do NOT invent a meaning** — leave it and flag it for the author.
   Inventing sense is worse than a clear "this line needs you."
4. **Preserve voice, meaning, and house style.** Keep the author's voice and the scene's
   content; apply the **prose-style** rules (no em dashes, no AI-isms, no
   negation-correction antithesis, complete-sentence narration with jagged dialogue).
   Clarity is the goal, not flattening — a long sentence that *works* stays.

## What it writes

Non-destructive, in a `clarity/` folder beside `chapters/`:

```
clarity/
├── NN-slug.report.md   # every issue: location, category, original → revised, why
└── NN-slug.edited.md   # the clarity-edited chapter (a PROPOSAL)
```

- The **report** lists each finding with a short quote, its category, the change made (or
  "flagged for author" with the reason), so the author can scan and accept or revert.
- The **edited chapter** is a proposal. **Promote it only on the author's OK** — copy
  `clarity/NN-slug.edited.md` over `chapters/NN-slug.md` when approved (do not auto-
  overwrite the draft). Surface a short summary and the count of author-flagged lines.

## Running automatically after each chapter

This is meant to fire whenever a chapter is drafted. A skill can't trigger itself; the
automatic part is a Claude Code **`PostToolUse` hook** on `chapters/*.md` writes (the
same mechanism as the fidelity-review auto-fire hook). The hook injects a prompt to run
clarity-edit on the chapter that was just written. Because the edit is written to
`clarity/` (not `chapters/`), it does not re-trigger the hook — no loop. The hook lives
in `~/.claude/settings.json` + `~/.claude/hooks/`, machine-global config separate from
this repo.

## Relationship to the other skills

- **book-editor** — the later, whole-manuscript polish. clarity-edit front-loads the
  per-chapter comprehension fixes so the editor and author work on cleaner text. Promote
  clarity edits before the book-editor pass.
- **style-check** — measures prose metrics (adverbs, crutch words, reading level);
  clarity-edit fixes comprehension. Complementary.
- **prose-style** — the house style this edit obeys while clarifying.
- **fidelity-review** — truth and continuity; clarity-edit stays chapter-local and never
  changes facts or plot.
- **book-machine** — runs it in the Draft/Edit stage, per chapter, right after
  chapter-writer.

## What it is not

Not a developmental or continuity edit, and not a license to rewrite. It clarifies what's
confusing, preserves everything that works, and never invents meaning for a line it can't
parse — that one goes back to the author.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill clarity-edit --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
