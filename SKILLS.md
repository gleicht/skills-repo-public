# The Skills

Every skill in this repository, what it does, when it fires, and what lives inside its
folder. Each skill is a directory containing a `SKILL.md` (the instructions Claude Code
reads) and, where the work benefits from being deterministic, a `scripts/` or
`references/` folder alongside it.

Thirty-six skills, grouped by the stage of the book they serve.

| Stage | Skills |
|---|---|
| [Orchestration](#orchestration) | book-machine |
| [Plan and set up](#plan-and-set-up) | project-research, story-bible, character-dossier, series-bible, outline-designer |
| [Draft](#draft) | chapter-writer, chapter-consensus, chapter-transition, propulsion-editor, clarity-edit, devague |
| [Edit, active](#edit-active) | editor-ensemble, story-editor, continuity-editor, dialogue-editor, momentum-editor, voice-editor, book-editor |
| [Diagnose and gate, read-only](#diagnose-and-gate-read-only) | style-check, dialogue-pass, deduplicator, developmental-edit, ai-detection, fidelity-review, review-panel, preflight-check |
| [Prepare to publish](#prepare-to-publish) | front-matter, back-cover-blurb, cover-designer, amazon-book-categorizer |
| [Package](#package) | epub-packager, docx-packager, pdf-packager |
| [House style](#house-style) | prose-style |
| [Art](#art) | midjourney-images |
| [Shared internals](#shared-internals) | lib/, docs/ |

A convention runs through the whole suite. **Active** skills change your prose, and they
write their work as a proposal in a side folder that gets promoted only when you approve
it. **Read-only** skills never touch a file, they write a report and hand the fixes back
to an active skill or to you.

---

## Orchestration

### `book-machine`

The conductor. It runs the whole suite end to end, from a bare idea to a packaged book,
calling each stage in order and stopping at review checkpoints so you can steer. Use it
when you want a complete book, manuscript, or ebook produced from a topic, premise, pile
of notes, or an outline, even if you never name the individual stages. If you only want
one stage, call that stage's skill directly instead.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The full pipeline, the stage order, the review checkpoints, and the shared project-folder contract every other skill reads and writes |

---

## Plan and set up

### `project-research`

Captures source material into the book project so the writing and editing stages can draw
on it and stay accurate. It builds `research.md` plus a `research/` folder. Use it when
you paste in material to base a book on, add notes, facts, sources, or background, or say
"use my research when you write." Works for fiction, where it grounds real-world detail,
and for non-fiction, where it is the substance. For gathering new research off the web, it
hands off to a deep-research skill and stores the results here.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | How research is captured, filed, and cited back during drafting |

### `story-bible`

Builds and maintains `story-bible.md`, the single reference holding a project's world
rules, narrative voice and style, and plot beats, so continuity and prose hold steady
across a long book. Use it when starting serious long-form fiction, defining worldbuilding
rules or a voice guide, or when the writing has started drifting off-plot, breaking its
own rules, or losing its voice. Characters live in the companion `character-dossier`.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The bible's sections, including the Voice Sample and the spoiler-walled author-only material |

### `character-dossier`

Interviews you to build the cast roster, each character's name, description, role, want,
fear, and a secret, saved as `characters.json`. Chapters then stay consistent in names,
voice, appearance, motivation, and arc. Use it when a new story is starting, or to create,
edit, or review characters. When a story is being set up, the skill offers to build the
dossier before any chapter is drafted.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The interview, the dossier schema, and how the cast is kept current as the book grows |

### `series-bible`

The cross-book layer that sits above the individual book folders, holding the overarching
arc, reading order, in-world timeline, recurring cast across books, persistent canon, a
reveal ledger, and open setups awaiting payoff. It writes `series-bible.md` plus a light
`series.json` registry. Use it for any sequel, trilogy, or multi-book saga, to keep later
books from contradicting earlier ones, to age a recurring cast across volumes, or to
capture a finished book's canon before starting the next.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The series-level schema and the rules for what belongs here rather than in a single book's bible |

### `outline-designer`

Designs the book's structure, a strong title plus an ordered list of chapters each with a
short brief saying what it covers, written to `outline.json`. Use it for a book outline,
chapter plan, table of contents, or overall structure, or when starting from a topic or a
premise. First stage of the pipeline, and it works standalone.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | Structural patterns, act shaping, and the per-chapter brief format the drafting stage consumes |

---

## Draft

### `chapter-writer`

Writes full, publication-quality prose from the outline and the per-chapter briefs, one
markdown file per chapter. Use it to draft, write, or flesh out chapters, expand an outline
into real prose, or continue and rewrite specific chapters. Works standalone on any folder
that has an `outline.json`.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The drafting loop, the sources of truth it must obey, and the per-chapter quality bar |

### `chapter-consensus`

Best-of-N drafting. It fans out six chapter-writers at once, one per lens (interiority,
pacing, dialogue, sensory, restraint, hook), all obeying the same outline, bible,
characters, and house style, then synthesizes one coherent chapter in the book's voice and
hands it to `clarity-edit`. Use it for ensemble drafting, several parallel drafts merged
into the strongest single chapter, or a higher-effort pass on a chapter that earns it.
Non-destructive, drafts and the merge sit in a `consensus/` folder until promoted.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The six lenses, the fan-out, and the synthesis rules for merging without seams |

### `chapter-transition`

Proposes optional connective passages between adjacent chapters, a bridge that smooths a
time jump, location change, POV switch, tonal shift, or dangling thread. Anywhere from a
one-line dateline to roughly a thousand words, or nothing at all when a hard cut serves
the book better, which is the default. Proposals go in a `transitions/` folder and the
chapter files are never touched.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | When a bridge earns its place, the length ladder, and the proposal format |

### `propulsion-editor`

Rewrites a drafted chapter so every sentence pulls the reader to the next. It enforces
forward motion line by line, a dramatic question in every scene, causal progression rather
than additive, entering scenes late and leaving early, withheld information, active verbs
over stative, and an unresolved chapter ending. It also enforces "earn the length," so
padding is refocused into story rather than simply cut and the chapter keeps or grows its
size while every word works. The generative counterpart to `momentum-editor`, which
removes drag.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The propulsion rules, the earn-the-length contract, and the rewrite procedure |
| `scripts/propulsion_flags.py` | 132 | Deterministic propulsion candidates for one chapter or a whole book folder, flagging stative verbs, additive progression, and resolved endings |

### `clarity-edit`

A per-chapter clarity pass over a first draft. It finds prose that would confuse a reader,
sentences that make no sense, wrong or awkward vocabulary, failed or mixed metaphors,
ambiguous pronouns and modifiers, and grammar tangled enough that it should be simplified.
It produces both a report of every issue and a clarity-edited chapter in a `clarity/`
folder, never overwriting the draft. Where a sentence's intent is genuinely unclear it
flags it for you rather than guessing at meaning.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The clarity checklist, the report format, and the rule against inventing meaning |
| `scripts/complexity_flags.py` | 84 | Flags over-complex sentences, the deterministic half of the pass |

### `devague`

A surgical de-vaguing pass. It finds every vague placeholder word, "something," "thing"
and "things," "shape" and its forms, and replaces each with a precise, concrete word, then
writes a before-and-after report naming the sentence, the word removed, and the word used.
It keeps the vague word where vagueness is the point, deliberate mystery, fixed idioms
like "the right thing" or "out of shape," and dialogue. Non-destructive, output goes to a
`devague/` folder.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The replacement policy, the keep-it cases, and the report format |
| `scripts/find_vague.py` | 119 | Locates every vague placeholder occurrence with its surrounding sentence |

---

## Edit, active

These change the prose. Each writes its version as a proposal you promote.

### `editor-ensemble`

Runs five active editors over one chapter in parallel, story, continuity, dialogue,
momentum, and voice, each producing its own improved version of the same chapter, then
merges the strongest change from each into one final chapter in the book's voice and on
canon. Every version and the merge live in an `editors/` folder until promoted. It is the
editing counterpart of `chapter-consensus`. Opt-in rather than automatic, meant for the
chapters that justify the cost, openers, pivotal scenes, and climaxes.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The five-editor fan-out and the merge rules for taking the best of each without collision |

### `story-editor`

Rewrites a chapter stronger as a story beat, sharpening the scene's purpose, the stakes,
tension and escalation, the turn, cause-and-effect logic, and emotional payoff, so the
chapter does a real job and lands. Use it when a scene feels flat or does not seem to do
anything. Honors the outline and never invents new plot.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The story-beat test, the escalation checklist, and the rewrite bounds |

### `continuity-editor`

Fixes consistency drift in place, names and spellings, ages, tells, relationships, the
timeline and day-count, objects and evidence, world rules, POV and tense, and secrets
revealed too early, correcting the prose to match the bible, the cast, prior chapters, and
`book.json`. The active single-chapter cousin of the read-only `fidelity-review`. It
treats canon as authoritative and never edits canon to match a mistake. Genuine gaps get
flagged, not invented.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The drift categories, the precedence of sources, and the flag-do-not-invent rule |

### `dialogue-editor`

Rewrites a chapter's dialogue to be sharp and propulsive, distinct character voices,
subtext, real conflict, natural rhythm, cutting on-the-nose lines, exposition dumped into
talk, dead back-and-forth, and weak tags. The active counterpart to the read-only
`dialogue-pass`. It never changes the plot a conversation carries.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | Voice differentiation, subtext technique, and tag and beat handling |

### `momentum-editor`

Finds and fixes the two things that kill forward motion, slow saggy spots, which it
tightens and energizes, and diversions that neither advance the plot nor develop a
character, which it cuts or refocuses. The test for every passage is whether it moves the
story or deepens a character. If it does neither, it goes or it earns its place. Honors
the outline so required beats survive.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The two-part test, the compression technique, and what is protected from cutting |

### `voice-editor`

Holds one consistent narrative voice across the chapter and true to the book's established
voice, smoothing tonal wobble, register slips, POV-distance drift, and rhythm
inconsistency, and enforcing the house rules. It matches the voice already set by the bible
and the prior chapters, and never flattens the prose into something generic.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The voice-matching procedure and the drift categories it corrects |

### `book-editor`

The holistic pass over a whole drafted book, improving consistency, tone, flow, and pacing
across chapters, removing repetition, and fixing rough transitions. Use it to edit, revise,
polish, tighten, or proofread a manuscript, or to smooth the voice across the book. This
is where the fixes recommended by the read-only diagnostics get applied.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The whole-book editorial pass and its order of operations |

---

## Diagnose and gate, read-only

These never touch a file. They measure, report, and hand the work back.

### `style-check`

A deterministic prose-style linter, the scripted companion to `prose-style` and
`book-editor`. It measures what a tired eye misses, crutch and filler words, perception
filter verbs, adverb density, sentence-length monotony, word echoes inside a paragraph,
reading level per chapter against a target, and hard counts of em dashes and stock AI-ism
phrases, writing the numbers to `style-report.md`.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | How to read the metrics and which ones justify a rewrite |
| `scripts/style_check.py` | 158 | The diagnostics themselves, run over a folder of chapters |

### `dialogue-pass`

A focused craft review of the book's dialogue, deeper on speech than the book-editor's
holistic pass. It reports where character voices blur together, where speech is stiff or
on-the-nose, where tags and action beats are mishandled, where exposition is dumped into
talk, and where formatting or dialect drifts, writing to `dialogue-report.md`.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The dialogue review checklist and report format |

### `deduplicator`

Scans a drafted manuscript for duplicated content, chapters that are exact or near
duplicates, paragraphs pasted into two places, and sentences repeated across the book, and
reports them without touching the files. Worth running as a routine QA gate before
editing, verifying, or packaging, even unprompted. This is for prose manuscripts, not for
de-duplicating spreadsheet rows, records, or code.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | Thresholds, what counts as a near-duplicate, and how to triage the findings |
| `scripts/check_duplication.py` | 207 | Chapter, paragraph, and sentence-level duplication scan across a project |

### `developmental-edit`

The big-picture structural edit, the editorial letter a developmental editor sends an
author. It reads the whole manuscript against the outline and the bible and proposes
structural change, reorder, cut, merge, or split chapters, expand thin scenes, compress
saggy ones, strengthen a weak act break, a soft midpoint, or an unearned ending, and
sharpen stakes, momentum, arcs, and the central promise, written to `dev-edit-report.md`.
It proposes the plan, the drafting and editing skills execute it.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The structural diagnosis and the prioritized revision roadmap format |

### `ai-detection`

Checks whether a manuscript reads as machine-written, and helps make it read human. It
scores each chapter on the signals that correlate with AI prose, uniform sentence length,
AI-ism and signature-word density, sentence-initial transitions, hedging, em dashes, and
low lexical diversity, then reports a reads-as-AI, mixed, or reads-as-human band with the
worst passages, written to `ai-detection-report.md`. Fixes loop back through `prose-style`
and `book-editor`. It is a heuristic, not a real detector. It cannot run or guarantee any
commercial detector, though it documents how to run one yourself.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The signals, the banding, and the honest limits of the heuristic |
| `scripts/ai_likelihood.py` | 152 | The scan that produces the per-chapter scores |

### `fidelity-review`

A self-verification pass that audits written work to confirm it stayed true to the task and
did not diverge, pad, or hallucinate. It checks the output against the project's sources of
truth, the `book.json` spec, the outline, the bible, the cast, the research, and against
your original request, reports every issue with the corrective measure taken, then re-runs
until nothing is left open or you override it.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The audit procedure, the report schema, and the re-run-until-clean loop |

### `review-panel`

Several independent reviewers each read the whole manuscript the way human editors and beta
readers would. The skill reports the problems they agree on, ranked by how many reviewers
raised each, with a READY or NOT-READY verdict in `review-report.md`. Reviewers flag plot
gaps, logic holes, weak or unfair twists, continuity errors, character inconsistencies,
pacing problems, and spelling and grammar. Distinct from `fidelity-review`, which audits
against the plan, and `book-editor`, which fixes.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The panel setup, the independence rules, and the agreement ranking |

### `preflight-check`

The last gate before publishing. A fast reconciliation confirming every outline chapter has
a real, non-empty file in order with no orphans or gaps, that no placeholder or TODO
markers remain, that the metadata is complete so no book goes out unsigned, that the
front-matter manifest resolves, and that the earlier gates closed out, review-panel READY
and fidelity-review PASS with nothing open. Writes `preflight-report.md` with a GO or HOLD
verdict.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The checklist, the verdict rules, and which skill owns each possible failure |
| `scripts/preflight.py` | 213 | The reconciliation itself |

---

## Prepare to publish

### `front-matter`

Builds the front matter and title-page metadata. It fills the author, subtitle, series,
publisher, copyright year, and rights in `book.json`, and authors the copyright page,
dedication, epigraph, "also by," acknowledgments, and about-the-author into a
`front-matter/` folder that all three packagers render into the finished book.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | Each front-matter piece, its conventions, and the manifest the packagers read |

### `back-cover-blurb`

Writes the marketing copy, the back-cover blurb and Amazon description, a tagline and
one-line hook, and short and long variants, into `blurb.md` and optionally into
`book.json`. It works from the book's own metadata, outline, bible, and prose, in the
book's voice, and it honors the spoiler wall, so it may raise the central question and
lean into a decoy the book itself plants, but it never confirms the answer, names the
culprit, or reveals a late reversal, a death, or the ending.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The blurb pieces, the voice-matching rules, and the spoiler wall |

### `cover-designer`

Turns genre, tone, comps, and key imagery into a cover-design brief plus ready-to-run
Midjourney prompts in `cover-brief.md`, then hands off to `midjourney-images` to generate
the art. The prompts are built for the 2:3 book-cover ratio and for thumbnail legibility.
It honors the spoiler wall and the book's real setting and era, so the cover never
misleads about what is inside.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The brief format, prompt construction, and the handoff to the image skill |

### `amazon-book-categorizer`

Recommends Amazon US browse categories, subcategories, and the seven KDP search keywords
for a finished book, from the book's own metadata, title, topic, audience, tone, blurb,
and outline. Picks, reasoning, and alternates go to `amazon-categories.md`, ready to paste
into the KDP dashboard. It does not browse live Amazon ranks, so treat the picks as a
starting point to confirm in the category picker.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The selection method and how to use the output in KDP |
| `references/category-map.md` | 138 | Category and keyword reference |
| `references/kdp-categories-us.md` | 181 | US KDP category data |
| `references/kdp-category-paths-us.md` | 339 | The full US browse-path catalog |
| `scripts/lint_keywords.py` | 134 | Validates keywords against Amazon's mechanical rules |

---

## Package

### `epub-packager`

Assembles a folder of finished chapters into a valid, downloadable EPUB 3 using a bundled
Python script. Use it to package, build, export, or compile an ebook, or to produce the
final deliverable. Works standalone on any folder following the project layout.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The build invocation, the layout it expects, and the front-matter integration |
| `scripts/build_epub.py` | 498 | Builds a valid EPUB 3 from a book project folder |

### `docx-packager`

Assembles finished chapters into a Microsoft Word document using a bundled,
dependency-free Python script. Use it for an editable Word deliverable alongside or instead
of the EPUB.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The build invocation and the Word styling it applies |
| `scripts/build_docx.py` | 454 | Builds a `.docx` from a book project folder, no third-party dependencies |

### `pdf-packager`

Builds a print-ready PDF by rendering the packaged `.docx` through an installed document
engine, Microsoft Word or LibreOffice. Use it alongside the other two packagers when a PDF
is wanted.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | Engine detection, prerequisites, and the render step |
| `scripts/build_pdf.py` | 186 | Renders the packaged `.docx` to PDF |

---

## House style

### `prose-style`

The always-on writing style the whole suite obeys. Write natural, specific, human prose and
strip out AI tells. Replace em dashes with punctuation that names the relationship they
were standing in for. Avoid AI-ism phrases, vocabulary, and structures, "delve," "it's
worth noting," fake balance, emotion-labeling, and stock fiction phrases. Write narration
in complete sentences at a grade 9 to 12 reading level with serial commas. Show rather than
tell. It applies both to prose the skills generate and to text you hand over for editing.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The house rules in full |
| `references/ai-isms.md` | 344 | The complete AI-ism catalog with before-and-after examples |

---

## Art

### `midjourney-images`

Generates images in your own Midjourney account by driving the Claude for Chrome browser
extension, which is the only way to operate Midjourney since it has no public API or MCP
server. Use it to create images, art, illustrations, concept art, posters, or covers with
Midjourney, or to upscale, vary, or download a render. It requires that you are logged in
yourself. It never enters passwords, creates accounts, handles payments, or solves
CAPTCHAs.

| File | Lines | What it is |
|---|---|---|
| `SKILL.md` | — | The browser-driving procedure, prompt handling, and the hard safety limits |
| `README.md` | 74 | Standalone setup and usage notes, including the Chrome extension prerequisite |
| `scripts/overlay_cover_text.py` | 159 | Overlays clean, correctly spelled text onto cover art, since image models cannot be trusted with lettering |

---

## Shared internals

Not skills. Support files the skills call.

### `lib/`

| File | Lines | What it is |
|---|---|---|
| `AUDIT-LOG.md` | 51 | The shared audit-log convention. Every skill records each run to `audit-log.md` and `audit-log.jsonl` in the book folder, noting that it ran, when, its verdict, the items processed, and the outputs written |
| `audit_log.py` | 85 | Appends a run entry to a project's audit log |
| `email_audit_log.py` | 107 | Emails a book's audit log on demand |
| `email_config.example.json` | 9 | Template for the SMTP settings. Copy to `email_config.json` and fill it in. The real config is git-ignored and never committed |

### `docs/`

| File | What it is |
|---|---|
| `skill-map.png` | The suite diagram, showing every skill grouped by stage and the handoffs between them |
| `skill-map.svg` | The same diagram in vector form |

---

## Installing

Copy the skill folders you want into your personal skills directory.

- macOS and Linux: `~/.claude/skills/`
- Windows: `C:\Users\<you>\.claude\skills\`

Each skill is a folder with a `SKILL.md` inside. Claude Code discovers them on start and
fires each one from its description, so there is nothing to register and no configuration
file to edit. Take the whole suite or take a single skill, they work standalone.

The Python scripts need Python 3 and no third-party packages. The PDF packager is the one
exception, it needs Microsoft Word or LibreOffice installed to do the rendering.
