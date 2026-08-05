---
name: devague
description: >-
  A surgical de-vaguing pass over a chapter. It finds every vague placeholder word —
  "something," "thing"/"things," and "shape"/"shapes"/"shaped" — and replaces each with
  a precise, concrete word so the prose says what it means, then writes a before/after
  report of every change (the sentence, the word removed, and the word used). It honors
  prose-style 2.4: it keeps the vague word where vagueness is the point (deliberate
  mystery or suspense, fixed idioms like "the right thing" or "out of shape," and
  dialogue), and flags the uncertain rather than guessing. Non-destructive: the edited
  chapter and the report go to a devague/ folder, promoted only on approval. Use
  whenever the user wants to remove or replace vague words, cut "something/thing/shape,"
  reduce vagueness, make prose more specific, or run a de-vague or specificity pass on a
  chapter or book.
---

# Devague

A narrow, mechanical pass with one job: hunt the three vague placeholder words and
replace each with the precise word the sentence actually wants. It is the automated
enforcer of **prose-style §2.4** ("kill vague placeholder nouns"), run as its own focused
sweep rather than folded into a broader edit. It produces a **before/after report** of
every swap and a **de-vagued chapter** as a proposal.

It is narrower than **clarity-edit** (which fixes all confusing prose) and than the
**book-editor** (which polishes the whole manuscript). devague touches only three words.

## What it targets

- **something**
- **thing / things**
- **shape / shapes / shaped** (and "X-shaped" compounds, e.g. *name-shaped hole*)

Whole-word only: it never fires inside *anything, nothing, everything, shapeless,
landscape*.

## The rule it enforces (prose-style §2.4)

1. **First choice: name the actual noun.** *She grabbed something* → *She grabbed the tire
   iron.* *He did the thing* → say what he did. *It took on a shape* → name the form,
   pattern, or realization.
2. **Only if no specific noun fits, use a precise stand-in by register** — concrete:
   *object, item, article, piece*; abstract: *matter, detail, element, aspect, point*;
   comic/voice: *contraption, gadget, doohickey*.
3. **KEEP the vague word when the vagueness is the point** (do not force a swap):
   - **Deliberate mystery / suspense** — not-naming is the effect: *something moved in the
     dark*. Replacing it would kill the dread.
   - **Idioms and set phrases** — *the right thing to do, for one thing, out of shape, in
     good shape, take shape*.
   - **Dialogue and voice beats** — people say "thing" and "something"; let them.
4. **Never invent meaning.** If you cannot tell what a vague word stands for, **flag it for
   the author** rather than guessing a replacement.

Every replacement must itself obey prose-style: American spelling, no new vague word, no
purple substitute, the clause cap intact.

## How to run it

1. **Find the candidates (the deterministic half):**
   ```bash
   python scripts/find_vague.py <chapter.md | book-folder>
   ```
   It lists every occurrence with its sentence and a light advisory flag
   (`likely idiom — verify`, `quote present — check if dialogue`). The script only
   *locates*; it cannot judge whether to replace or keep.
2. **Judge each occurrence in context.** Replace where a precise word fits; keep idioms,
   deliberate mystery, and dialogue; flag the genuinely unclear.
3. **Write the de-vagued chapter and the report** (see below). The edit is a proposal;
   the draft is never overwritten.

## What it writes

Non-destructive, in a `devague/` folder beside `chapters/`:

```
devague/
├── NN-slug.report.md   # every change (before → after) + every KEPT word with its reason
└── NN-slug.edited.md   # the de-vagued chapter (a PROPOSAL)
```

### The report (the deliverable)

A **Replaced** table — one row per swap — and a **Kept** list with reasons:

```markdown
# Devague report — Chapter 11: The Looks

Source: consensus/11-the-looks/merged.md · candidates: 18 · replaced: 12 · kept: 6

## Replaced
| # | Sentence (excerpt) | Removed | Used |
|---|--------------------|---------|------|
| 1 | "It had only taken on a **shape**, and Faith knew the **shape**." | shape | a weight / the lean of it |
| 2 | "She made the help feel like **nothing**… filed it, before she had any**thing** to file it against." | thing | a fact |
| 3 | "a pattern still looking for the **shape** that would hold it" | shape | the rule |

## Kept (vagueness intentional — prose-style §2.4)
- "the right **thing** to do" — idiom
- "**something** moved in the dark" — deliberate mystery
- "some **things** you are better off leaving be" (Nora) — dialogue

## Flagged for author (intent unclear)
- (none) — or: "…the **thing** about the river" — can't tell what noun; please specify.
```

Lead with the counts (candidates / replaced / kept / flagged), then the tables. Show
enough of each sentence that the change is unambiguous; **bold** the word in question.

## Promotion

The edited chapter is a proposal. **Promote it only on the author's OK** — copy
`devague/NN-slug.edited.md` over `chapters/NN-slug.md` when approved. Surface the counts
and any author-flagged lines first.

## Where it sits

Run it per chapter in the **Draft / Edit** stage, **after chapter-writer or
chapter-consensus**, alongside **clarity-edit**. Order does not matter much, but running
devague before the whole-manuscript **book-editor** pass means the editor works on
already-specific text. It can also run standalone any time the prose has gone vague.

## Relationship to the other skills

- **prose-style §2.4** — the rule. devague is its mechanical, report-producing enforcer.
- **clarity-edit** — the broad per-chapter comprehension pass; devague is the narrow
  three-word lexical pass. Complementary; run either order.
- **style-check** — measures crutch-word and adverb frequency; devague fixes the specific
  vague-noun crutch and rewrites it.
- **book-editor** — applies fixes across the manuscript; devague front-loads the per-chapter
  de-vaguing so the editor starts from concrete prose.

## What it is not

Not a general line edit, not a thesaurus that swaps in fancier vague words, and not a
license to flatten deliberate mystery or natural dialogue. It removes lazy vagueness in
three words, keeps the intentional uses, and never invents a meaning it cannot read.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill devague --target <book-folder> --status <DONE|verdict> --item "<each chapter processed>" --output "<each file written>" --note "<one-line summary, e.g. '12 replaced, 6 kept, 0 flagged'>"`

Use `DONE` for a completed pass. `--item` is the chapter(s) processed; `--output` is each
file written (the edited chapter and the report). Full convention: `lib/AUDIT-LOG.md`.
