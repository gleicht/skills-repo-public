---
name: cover-designer
description: Turns a finished book's genre, tone, comps, and key imagery into a cover-design brief plus ready-to-run Midjourney prompts, saved to cover-brief.md, then hands off to the midjourney-images skill to generate the art. Use whenever the user wants a book cover, cover art, a cover concept or design brief, jacket or cover imagery, or Midjourney prompts for a cover; wants to design or brainstorm a cover; or is prepping cover art for KDP or print. It writes the brief and the prompts (focused on the art, at the 2:3 book-cover ratio, built for thumbnail legibility) but does not generate images itself — the midjourney-images skill drives Midjourney. Honors the spoiler wall and the book's real setting and era so the cover never misleads. Publishing-prep stage of the book-machine suite.
---

# Cover Designer

The bridge from a finished book to its cover art. This skill reads the book, decides a
visual direction that fits its genre and mood, writes a **cover-design brief**, and turns
that into **ready-to-run Midjourney prompts** — then hands off to the **midjourney-images**
skill, which actually drives Midjourney to generate the art.

It does **not** generate images itself, and it does **not** lay out the final cover (title
and author type go on in a design tool afterward). Its job is the *brief* and the
*prompts*, so the art that comes back is the right art.

## Where it lives

In the book project folder, beside `book.json`:

```
cover-brief.md   # the design direction, constraints, and the Midjourney prompts
cover/           # (optional) where generated/chosen art is saved by midjourney-images
```

## What it reads

- **`book.json`** — title, author, genre, tone, audience. The positioning the cover sells.
- **`story-bible.md`** — setting, era, mood, and any signature imagery the book leans on.
- **`back-cover blurb` / `blurb.md`** — the hook and emotional register the cover should match.
- **`amazon-categories.md`** (if present) — the chosen shelf, so the cover signals the
  right genre to browsers.
- **`research.md`** (when relevant) — period and place detail the art must get right.
- **`characters.json`** — only if a figure belongs on the cover; many covers avoid faces.
- Any **comps** the user admires and their own must-have or must-avoid imagery.

## Two rules the cover must obey

- **No spoilers on the cover.** Read the spoiler-walled material (the `story-bible`
  `SOLUTION`, `clues.md`, the **series-bible** reveal ledger) and never put the twist,
  the culprit, or the ending in the art. The cover sets mood and genre, not answers.
- **Stay true to the book.** Match the real setting, era, and tone. For a period book,
  no anachronisms (for a late-1980s small-town story, no smartphones, modern cars, or
  modern dress). A cover that misrepresents the book earns returns and bad reviews.

## The brief

Write `cover-brief.md` with these:

```markdown
# Cover brief — <Title>

## Book at a glance
Genre/shelf, audience, mood in a phrase, setting and era.

## Design direction
The one-line concept: what the cover should say at a glance, and the feeling it
should give a browser scrolling past.

## Visual elements
The focal image and key motifs to include; specific things to avoid. Decide
photographic vs. illustrated vs. typographic, and whether a figure appears.

## Colour & light
Palette and lighting that carry the mood (e.g., cold dusk blues and sodium-lamp
amber for small-town dread).

## Typography & layout (added in design, not Midjourney)
Title and author hierarchy, the type mood (a bold sans for thrillers, a quiet
serif for literary), and the reminder that it must read as a tiny Amazon thumbnail.

## Comps
Cover styles to echo or to avoid, and why.

## Midjourney prompts
3 distinct concept directions (see below), each ready to run.

## Next step
Generate with midjourney-images, choose a frame, then set title/author type in a
design tool.
```

## Writing the Midjourney prompts

- **Prompt the art, not the text.** Midjourney does not render legible titles reliably,
  so describe the *image*; the title and author go on later in a design tool. Do not ask
  it to write the book's title.
- **Use the book-cover ratio.** End each prompt with `--ar 2:3` (the standard ebook/print
  cover shape). Optionally suggest `--stylize` for more or less artistic licence; leave
  Midjourney version to the user's account default (the **midjourney-images** skill
  handles operational details).
- **Give 2-4 distinct directions, not variations of one.** For example: an atmospheric
  landscape, a lone figure in silhouette, and a symbolic object close-up — so the user
  can compare real alternatives.
- **Be concrete and sensory.** Name the subject, setting, era, time of day, light,
  weather, palette, composition (e.g., "negative space at the top for the title"), and an
  art style or medium. Leave room at top or bottom for type.
- **Signal the genre.** Lean into the visual language of the shelf the book sits on, so
  the cover reads as its genre at a glance.

Example shape (adapt to the book):
`a deserted small-town main street at dusk, late 1980s, wet asphalt reflecting sodium
streetlights, fair banners sagging overhead, a single distant figure, cold blue and amber
palette, cinematic, muted film grain, ominous quiet, negative space at top for a title
--ar 2:3`

## How to work

Offer 2-3 design directions for the user to react to before committing, then write the
brief and the prompts for the chosen direction (plus a couple of alternates). When the
prompts are ready, **hand off to the midjourney-images skill** to generate, upscale, and
download; save chosen art under `cover/`. Support partial runs: "just give me three
prompts," "make it more literary," "try a typographic direction."

## Relationship to the other skills

- **midjourney-images.** The executor — it drives Midjourney via the browser extension to
  generate, vary, upscale, and download from the prompts this skill writes. This skill
  produces the prompts; that one runs them.
- **back-cover-blurb.** The blurb's hook and mood guide the cover's; build it first when
  you can.
- **amazon-book-categorizer.** The chosen category is the shelf whose visual conventions
  the cover should match.
- **story-bible / clues.md / series-bible.** The spoiler and setting sources of truth —
  honor them; never spoil on the cover.
- **book-machine.** Offer this in publishing prep, alongside the blurb and categories.

## What this is not

It is not an image generator (that is **midjourney-images**) and not a layout tool. It
stops at the brief and the prompts, and at handing the prompts to the generator. Final
cover assembly — placing the title and author type over the art — happens in a design
tool afterward.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill cover-designer --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
