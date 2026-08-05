---
name: series-bible
description: Builds and maintains a Series Bible — the cross-book continuity reference (series-bible.md plus a light series.json registry) that sits above the individual book project folders and holds what spans an entire series: the overarching arc, reading order, in-world timeline, recurring cast across books, persistent world canon, a reveal/continuity ledger, and open setups and payoffs. Use whenever a story is or will become a series, sequel, trilogy, or multi-book saga; when the user wants to keep later books from contradicting earlier ones; to track what's been revealed in which book, age a recurring cast across volumes, or plant setups that pay off books later; or to capture a finished book's canon before starting the next. Complements the single-book story-bible (one book's world/voice/plot) and character-dossier (one book's cast) — it owns only the layer that crosses books.
---

# Series Bible

A Series Bible is the **single source of truth for a multi-book story** — the document
Claude re-reads so book three never contradicts book one. Where the **story-bible**
governs one book's world, voice, and plot, and the **character-dossier** holds one
book's cast, the Series Bible governs the layer *above* them: the arc that spans the
whole series, the shared timeline, the cast as it ages and changes across volumes, the
world canon every book must honor, and the running record of what has been revealed
when. It exists so a long-running series stays consistent with itself.

Build it when a project is, or is likely to become, a series, sequel, trilogy, or saga.
A standalone book doesn't need one.

## Where it lives, and how the machine uses it

A series spans several book project folders, so the Series Bible sits **one level above
them**, in a series folder that contains the per-book folders:

```
<series-folder>/
├── series-bible.md      # the cross-book canon (this skill owns it)
├── series.json          # light registry of the books (order, title, folder, status)
├── 01-<book-slug>/      # a normal book project folder: book.json, story-bible.md,
│   └── ...              #   characters.json, outline.json, chapters/, dist/ …
├── 02-<book-slug>/
└── …
```

`series.json` is the machine-readable book list:

```json
{
  "title": "string",
  "books": [
    { "order": 1, "title": "string", "slug": "string", "folder": "01-<slug>",
      "status": "planned | drafting | done", "logline": "one line" }
  ]
}
```

When `series-bible.md` exists, the per-book stages treat it as **higher canon**:
**outline-designer** and **chapter-writer** read it so a new book's structure and prose
honor the series arc, timeline, and established facts; **book-editor** checks a book
against it for cross-book contradictions; **story-bible** and **character-dossier** for
a new book defer upward to it for shared world rules and recurring cast rather than
re-deciding them; and **fidelity-review** audits a book against the Series Bible, so a
detail that breaks earlier-book canon is flagged like any other fidelity issue. The
book's own text remains the highest authority for that book — when a finished book and
the Series Bible disagree, reconcile the bible to the text (see Maintenance).

## The core sections

Write `series-bible.md` with this structure. Keep entries concrete and rule-shaped, the
way the story-bible states enforceable laws — a series bible is most useful when it says
exactly what later books may not contradict.

```markdown
# Series Bible — <Series Title>

## 1. Series Overview
The premise of the whole series, the throughline or arc that runs across the books,
the genre, and the intended length. State the central question the series is
answering and how it resolves (if known).

## 2. Books & Reading Order
The ordered list of books, each with a one-line logline and status. Mirrors
series.json. Note chronological vs. publication order if they differ.

## 3. Series Timeline
The in-world chronology spanning the books: key dated events, and how much in-world
time passes within and between books. This is what stops a later book from misdating
an earlier event or aging a character wrong.

## 4. Recurring Cast (cross-book layer)
Only what crosses books: each recurring character's series-long arc, how they age or
change, their status by book (alive, gone, estranged), and relationships that evolve
across volumes. Point at each book's characters.json for the per-book detail; do not
duplicate the dossier here.

## 5. Persistent World Canon
The rules, places, organizations, and established facts that EVERY book must honor —
the shared world. A single book's story-bible may hold book-local detail; this section
holds what binds the whole series. Write them as constraints that must hold.

## 6. Continuity & Reveal Ledger
What the reader knows by the end of each book, what is still secret, and the
established facts later books cannot contradict. Track reveals by book ("Book 1 end:
reader knows X; still hidden: Y"). Essential for mystery/suspense series.

## 7. Open Threads (setups & payoffs)
Things planted in one book to pay off in a later one: where each was set up, where it
is meant to land, and whether it is still open. Keeps a series from dropping a thread
or forgetting a promise.

## 8. Canon Change Log
When something is retconned, evolved, or decided, record it with the book/date so the
current canon is unambiguous.
```

Voice across the series usually defers to the **prose-style** house style plus each
book's own story-bible Voice & Style Guide; note here only conventions that must hold
series-wide (a consistent narrator, a recurring structural motif).

## Spoilers across books

A series often carries a secret from an early book to a reveal books later, so the
Series Bible adopts the suite's **spoiler-wall** discipline. Sections 6 and 7 in
particular will hold future-book spoilers — keep author-only material behind a clear
`## (author-only)` heading and **never** let it leak into prose, transitions, a blurb,
or a back-cover description. `chapter-writer`, `book-editor`, and `chapter-transition`
must honor future-book canon without exposing it; `review-panel` reads it only for its
informed reviewers. This mirrors the spoiler wall and `clues.md` ledger owned by
story-bible at the single-book level.

## How to build it — a guided interview

Like the story-bible, **draw this out of the user**; don't invent a series and present
it as theirs. Two entry points:

- **Planning a new series.** Run a relaxed conversation about the big picture: the
  premise and the arc across books, how many books are planned, what recurs (cast,
  world, themes), and which large beats are fixed versus open. Capture the spine; leave
  blanks where the future isn't decided yet.
- **Capturing a finished book before the next.** After a book is done, reconcile what it
  established into the bible: events and their dates, what was revealed, how the
  recurring cast changed, new world facts, and which threads it opened or closed. The
  **finished book's text is the highest authority** — read it (or its story-bible,
  characters.json, and chapters) and update the series canon to match, exactly as this
  suite treats a manuscript as the top source of truth.

Throughout:
- **Push for rules, not vibes** — "the city was rebuilt between books two and three" is
  enforceable; "things changed" is not.
- **Never block on a blank.** A partial series bible is useful immediately and fills in
  as books are written. Unknown future is expected.
- **Offer to draft, with approval** — propose an arc, a timeline entry, or a payoff for
  the user to accept, tweak, or reject. What the user confirms is canon.

After writing or updating `series-bible.md` (and `series.json`), show the user a short
recap so they can correct it. Support partial runs: "add book 3 to the registry," "what
threads are still open?", "update the timeline after this book," "who's alive by book
4?" → edit just that part.

## Relationship to the other skills

- **story-bible / `story-bible.md`.** Owns one book's world, voice, and plot. The Series
  Bible holds the shared world and arc above it; a per-book story-bible defers upward
  for series canon and keeps only book-local detail. No duplication.
- **character-dossier / `characters.json`.** The canonical per-book cast. The Series
  Bible tracks only the cross-book layer (arc, aging, status by book) and points at each
  dossier for the rest.
- **outline-designer, chapter-writer, book-editor.** Read the Series Bible as higher
  canon when the book belongs to a series.
- **fidelity-review.** Audits a book against the Series Bible too; a cross-book
  contradiction is a fidelity issue.
- **book-machine.** When orchestrating a book that is part of a series, consult the
  Series Bible during foundations and reconcile it into the bible once the book is done.
- **prose-style.** The always-on house style still governs all prose; the Series Bible
  doesn't restate it, only any series-wide voice convention.

## Maintenance

A series bible is only useful if it stays true. After each book, reconcile it to that
book's finished text: fold in new events, reveals, character changes, and world facts,
close the threads it paid off, and log anything that changed. Before starting the next
book, the bible is the guardrail every stage writes against.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill series-bible --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
