---
name: amazon-book-categorizer
description: Recommends Amazon US (KDP) browse categories, subcategories, and the seven KDP search keywords for a finished book from its own metadata — title, topic, audience, tone, blurb, and outline. Writes the picks plus reasoning and alternates to amazon-categories.md in the book project folder, ready to paste into the KDP dashboard. Use whenever the user wants to categorize a book for Amazon or KDP publication, choose categories or subcategories, find or optimize KDP keywords, or prep an existing listing's metadata. It works from the book's metadata and does not browse live Amazon ranks, so treat its picks as a starting point to verify in the KDP category picker. Publishing-prep stage of the book-machine suite; works standalone on any book folder with a book.json.
---

# Amazon Book Categorizer

A publishing-prep stage. Given a finished (or near-finished) book, this skill
recommends the **Amazon US / KDP categories** and the **seven KDP search keywords**
that put the book in front of the right readers, and saves them so the user can paste
them straight into the KDP dashboard.

It works from the book's own metadata — `book.json`, the outline, the blurb, the
story bible — plus what is plainly true about the genre. It does **not** browse live
Amazon, so it cannot read current bestseller ranks or guarantee a category still
exists under that exact name. Its job is strong, well-reasoned picks the user then
confirms in the live KDP category picker, not invented competitive data.

## Reference and tooling

- **`references/kdp-categories-us.md`** — **real** Amazon US category data imported from
  Publisher Rocket, with exact node names and **sales-to-rank** numbers (`→#1`, `→#10`),
  `Pub%`, and `KU%`. **When the book's genre is covered here, this is the source of
  truth** — prefer it over the curated map, and use the sales columns to steer the user
  toward niches they can realistically rank in (low `→#1`/`→#10`) rather than just
  plausible-sounding ones. Covers Science Fiction & Fantasy so far; more genres get
  added as the user pastes Rocket exports.
- **`references/kdp-category-paths-us.md`** — a broader catalog of real Amazon US
  **browse paths** (print and Kindle), imported from a Publisher Rocket export but
  **without** sales data. Covers Mystery, Thriller & Suspense; Literature & Fiction;
  Comics & Graphic Novels; and Children's Books. Use it for exact, current node names in
  those genres; it has no competition numbers, so reason about rank from the live store
  or a Rocket lookup. Prefer `kdp-categories-us.md` wherever the two overlap.
- **`references/category-map.md`** — the curated Amazon US category tree (drilled into
  the genres this suite writes), KDP's rules (category limit, the seven 50-character
  keyword fields, the banned-terms list), the keyword-research method, and worked
  examples. **Reason from it; don't invent categories.** It is a snapshot to verify
  against the live KDP picker, not live truth — the fallback for genres not yet in
  `kdp-categories-us.md`.
- **`scripts/lint_keywords.py`** — a deterministic check on the seven keywords (length
  ≤ 50, count ≤ 7, banned terms, title/author echo). Run it on the finished
  `amazon-categories.md` so a miscounted slot or a stray "bestseller" never ships:
  ```bash
  python scripts/lint_keywords.py <book-folder>     # or --kw "phrase" --kw "phrase" ...
  ```
  It exits non-zero on any hard violation and prints each field's character count.

## Where it lives

In the book project folder, beside `book.json` and `dist/`:

```
amazon-categories.md   # the KDP categories + keywords digest, with reasoning and alternates
```

It is the only file this skill writes. Like `fidelity-report.md` and
`review-report.md`, it is a human-facing digest, not something a packager script
consumes.

## What it reads

Pull every genre and positioning signal the folder already holds:

- **`book.json`** — title, author, topic, audience, tone, language. The spine of the
  recommendation.
- **`outline.json`** — chapter titles and briefs, for subject matter and structure.
- **`story-bible.md`** (stories) — genre, setting, voice, and the kind of read it is.
- **`research.md`** (non-fiction) — the subject domain and angle.
- **A back-cover blurb / description**, if one exists, and any comps ("for readers of
  …") the user offers. If there is no blurb yet, ask the user for a one-line pitch and
  any comparable titles; those sharpen both categories and keywords.

If `book.json` is missing, ask the user for title, genre/topic, audience, and tone, and
proceed from that — the skill works standalone.

## `amazon-categories.md` structure

```markdown
# Amazon categories & keywords — <Title>

## How to use this
Paste these into the KDP "Categories" and "Keywords" fields. Confirm each category
name against the live KDP category picker before publishing — availability and exact
wording change by marketplace and over time, and these were chosen from the book's
metadata, not live Amazon ranks.

## Book at a glance
- Genre / shelf: ...
- Audience: ...
- Tone & comps: ...

## Recommended categories (pick up to 3 in KDP)
1. Books › <Top> › <Sub> › <Specific>  — one line on why this fits
2. Books › ...                          — ...
3. Books › ...                          — ...

### Alternates (if a pick is unavailable or too broad)
- Books › ... — when to reach for it

## Keywords (7 slots, up to 50 characters each)
1. `keyword phrase`   — the reader search it targets
2. `keyword phrase`   — ...
... through 7

## Notes & cautions
- Anything to verify in KDP, trademark flags, or gaps in the metadata.
```

## How to do it

1. **Fix the genre and shelf.** From the metadata, name the single shelf a browser
   would find this on (e.g. "domestic thriller," "cozy mystery," "epic fantasy,"
   "personal-finance how-to"). Everything else follows from this. State your read of
   the audience and tone too; a YA and an adult version of the same premise categorize
   differently.

2. **Pick the categories — specific over broad.** Pick your source in this order: if the
   genre is in `references/kdp-categories-us.md`, work from there and let the `→#1` /
   `→#10` sales numbers break ties toward niches the book can actually rank in; else if
   it is in `references/kdp-category-paths-us.md` (Mystery/Thriller, Literature &
   Fiction, Comics, Children's), use those exact node names; otherwise fall back to the
   curated tree in `references/category-map.md`. Recommend categories as real Amazon
   browse paths (`Books › … › … › …`), choosing the **most specific** node that
   genuinely fits. A book ranks far more easily in a precise subcategory than in a
   giant top-level one. Amazon's KDP dashboard currently lets you select **up to three**
   categories per book — but that limit has changed before and can differ by
   marketplace, so say "up to three" and tell the user to confirm the current number in
   KDP. Offer a couple of **alternates** in case a pick is unavailable in the picker or
   reads as too broad. Give a one-line reason for each so the user can judge the fit.

3. **Write the seven keywords like a reader's search box.** KDP gives seven keyword
   fields, each **up to 50 characters**, and every field is a *phrase*, so pack related
   words together to cover more of a real search. Aim across these angles, without
   repeating: genre and form, tropes and themes, setting and era, tone and mood, and
   read-alike framing ("books like …" as a descriptive phrase, never another author's
   actual name). Seven distinct, high-intent phrases beats seven near-duplicates. The
   full keyword-research method (Amazon autocomplete, turning comps into phrases, the
   seven angles) is in `references/category-map.md`.

4. **Obey KDP's keyword rules.** Do not use: the book's own title, subtitle, series, or
   author name (already indexed); other authors', characters', or brands' **trademarked
   names**; subjective or unverifiable claims ("best," "bestseller," "award-winning");
   time-bound or promotional terms ("new," "free," "on sale," "available now");
   category names the user can already select directly; or anything inaccurate or
   misleading about the book. KDP can suppress a listing that breaks these, so flag any
   borderline pick instead of slipping it in.

5. **Lint, then write the file and show the user.** Run
   `python scripts/lint_keywords.py --kw "…" …` (or against the saved
   `amazon-categories.md`) to confirm all seven slots fit 50 characters and carry no
   banned terms or title/author echo; fix anything it flags. Then save
   `amazon-categories.md` and summarize the picks in chat, noting explicitly which
   choices are confident and which need a look in the live KDP picker.

## What it does not do

- It does **not** read live Amazon bestseller ranks, sales, or competition. If asked
  "what category has the least competition," say plainly that this needs the live KDP
  data and offer the most-specific-fit reasoning instead. Never fabricate ranks, sales
  figures, or "this category has N books."
- It does **not** invent categories. If unsure a node exists under that exact name, say
  so and mark it to verify.
- It does **not** edit the manuscript or any other source of truth — it only writes
  `amazon-categories.md`.

## How the rest of the machine uses it

This is publishing prep, so it runs **after packaging**, once the book and its blurb
are settled — or standalone for an existing listing the user wants to re-categorize.
The **book-machine** orchestrator offers it as the final, optional step. It reads the
same project folder as every other stage and adds one file; nothing downstream depends
on it.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill amazon-book-categorizer --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
