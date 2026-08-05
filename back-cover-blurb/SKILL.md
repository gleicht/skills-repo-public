---
name: back-cover-blurb
description: Writes a finished book's marketing copy — the back-cover blurb and Amazon/KDP book description, a tagline and one-line hook, and short and long variants — into blurb.md (and optionally book.json's description). Works from the book's own metadata, outline, story bible, and prose, in the book's voice, and honors the spoiler wall so the blurb never gives away the twist. Use whenever the user wants a blurb, book description, back-cover or jacket copy, a tagline, logline, elevator pitch, or marketing/sales copy for a book or listing; wants to pitch or describe a book to readers; or is prepping a KDP/Amazon description. Publishing-prep stage of the book-machine suite; pairs with amazon-book-categorizer (which reads the blurb) and front-matter; works standalone on any book project folder.
---

# Back-Cover Blurb

The selling copy: the back-cover blurb and the Amazon/KDP book description, plus a
tagline, a one-line hook, and short and long variants. The blurb's job is not to
summarize the book; it is to make the right reader want it. It promises the *experience*
of the book without spending the book's secrets.

This runs as publishing prep, once the manuscript is settled. It works from the actual
book, never inventing plot or overselling claims the pages don't earn.

## Where it lives

In the book project folder, beside `book.json`:

```
blurb.md   # tagline, hook, short blurb, full description, comps, notes
```

Optionally also set `book.json`'s `description` to the full blurb, so the EPUB metadata
and the **amazon-book-categorizer** pick it up automatically.

## What it reads

- **`book.json`** — title, author, audience, tone. The positioning.
- **`outline.json`** and a **chapter or two** — the actual hook, the protagonist, the
  central conflict, and the *voice* (a blurb should sound like the book).
- **`story-bible.md`** — genre, stakes, the kind of read it is.
- **`characters.json`** — the protagonist's want and what stands in the way.
- **`research.md`** (non-fiction) — the subject and the promise (what the reader gains).
- Any **comps** the user offers ("for readers of …") and an existing description to revise.

If there's no metadata, ask for the genre, the protagonist or subject, the central
conflict or promise, and the audience, and work from that.

## Spoilers — the rule that matters most

A blurb that gives away the twist is the worst failure this skill can produce. **Read
the spoiler-walled material and obey it without exposing it:** the author-only
`SOLUTION` section of `story-bible.md`, the `clues.md` ledger, and the **series-bible**
reveal ledger for a series. The blurb may *raise* the central question and lean into a
decoy the book itself plants, but it must never confirm the answer, name the culprit, or
reveal a late-book reversal, a death, or an ending. When in doubt, withhold — intrigue
sells better than a spoiler. (For a missing-person suspense novel, for example: tighten
the dread and the question of what happened to her; never hint at who is responsible.)

## The pieces

Write `blurb.md` with these, longest-useful first:

```markdown
# Blurb — <Title>

## Tagline
One line, ~10 words, the mood in a breath.

## Hook
A single sentence that states who wants what against what — the logline.

## Short blurb (~50 words)
For ads, social, and a newsletter. The hook plus stakes, ending on tension.

## Back-cover / Amazon description (~150-200 words)
The full pitch: open on a hook, introduce the protagonist and their ordinary
world, turn on the inciting trouble, raise the central question and the stakes,
and end on a hook or question — not a resolution. Short paragraphs.

## Comps & positioning
"For readers of <Author> and <Author>" / "<Book> meets <Book>." Naming other
authors is fine *here* (unlike KDP keywords, where trademarked names are banned).

## Notes
Anything to confirm, claims to verify, or a spoiler risk avoided.
```

## How to write it — craft

- **Lead with a hook, not a setup.** Open on the line that creates tension or curiosity.
  Never open with throat-clearing ("In a world where…", "Meet Jane, a…").
- **Protagonist, want, obstacle, stakes.** Name who the reader follows, what they want,
  what blocks it, and what it costs to fail. Concrete beats abstract.
- **Raise the question; don't answer it.** End on the dramatic question or a hook line,
  so the only way to learn the answer is to read.
- **Match the genre's register.** Thriller and suspense: short, punchy paragraphs and a
  ticking pressure. Literary: let the voice carry it. Romance: the couple and the barrier.
  Non-fiction: the problem, the promise, and why this book delivers it.
- **Sound like the book.** Pull the blurb's diction from the prose so the reader gets a
  true sample of the voice.
- **Don't oversell.** No "the best thriller ever," no claims the pages don't earn; that
  reads as hype and disappoints the reader who buys on it.
- **House style still applies.** The **prose-style** rules hold (no em dashes, no
  AI-isms, human and specific). Marketing copy may use punchy fragments for rhythm, the
  way dialogue can run jagged.

Offer drafts for the user to accept, tweak, or reject; iterate on the ones they like.
Support partial runs: "just the tagline," "make the description punchier," "give me
three hook options."

## Relationship to the other skills

- **amazon-book-categorizer.** It reads a blurb when one exists; writing this first makes
  its category and keyword picks sharper. (Note the rule difference: comparing to named
  authors is good in *this* description but banned in KDP *keywords*.)
- **front-matter.** That skill writes the short in-book *about-the-author* bio; this skill
  writes the *book's* selling copy (and can draft a longer marketing author bio if asked).
- **story-bible / clues.md / series-bible.** The spoiler sources of truth — read, never
  leak.
- **book.json.** Optionally set its `description` to the full blurb for the EPUB metadata
  and the categorizer.
- **prose-style.** The always-on house style governs the copy.
- **book-machine.** Offer this in publishing prep, once the book is done.

## A note on what this is not

It is sales copy, so it is allowed to be persuasive — but not dishonest. It must not
promise what the book does not deliver, and it must not spend the secrets the book is
built to protect.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill back-cover-blurb --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
