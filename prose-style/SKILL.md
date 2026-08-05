---
name: prose-style
description: The user's house writing style — write natural, specific, human prose and strip out AI tells. Replace em dashes with punctuation that names the relationship they signal; avoid AI-ism phrases, vocabulary, and structures ("delve," "it's worth noting," fake balance, emotion-labeling, stock fiction phrases like "her breath caught"); write narration in complete sentences at a grade 9–12 reading level with serial commas; and show rather than tell. Use whenever writing or editing prose for the user — drafting or revising chapters, stories, essays, or any narrative/expository text; cleaning up a passage; removing em dashes; or making writing read less like AI and more like a person. Apply it to prose you generate and to text the user asks you to edit. The full AI-ism catalog with before/after examples is in references/ai-isms.md.
---

# Prose Style (house style)

The user's standing style for prose. Apply it to anything you write for them and to
any passage they ask you to clean up. Produce natural, specific, alive prose: don't
perform helpfulness, don't announce your intentions, don't summarize what you're
about to do — just do it. Before finalizing, scan for the patterns below and rewrite
any that appear.

Three jobs: (1) replace em dashes with precise punctuation, (2) keep narration in
clear, complete sentences, and (3) strip out AI-isms so the writing reads like a
person wrote it.

**When the task is fiction or detailed revision, read `references/ai-isms.md`** for
the complete flag lists, the diagnostic codes, and before/after examples. This file
is the operative summary; the reference is the full catalog.

---

## Part 1 — Em dashes

Every em dash (—) signals a relationship between ideas. Identify the relationship and
use the punctuation that names it. Don't swap every em dash for the same mark — read
for meaning first. Five patterns:

| Pattern | Signal | Replacement |
|---------|--------|-------------|
| **Paired** (parenthetical) | Two em dashes wrapping an aside | comma … comma |
| **Sentence break** | Both sides are complete sentences | period + capitalize next word |
| **Introduction / payoff** | First half builds to a conclusion | colon |
| **Contrast / pivot** | Followed by *but, yet, still, though* | comma |
| **Loose connection** (default) | No clear pattern | comma (or semicolon if both sides are independent clauses) |

Examples:
- Paired: *The report — which nobody had read — was cited anyway.* → *…, which nobody had read, …*
- Break: *She opened the letter — her hands were shaking.* → *She opened the letter. Her hands were shaking.*
- Payoff: *He wanted only one thing — control.* → *He wanted only one thing: control.*
- Contrast: *I tried my best — but it wasn't enough.* → *I tried my best, but it wasn't enough.*
- Loose: *It was late — I was tired.* → *It was late; I was tired.*

**Decision order** (stop at the first yes): paired? → commas. Both sides complete
sentences? → period. Second half a payoff? → colon. Contrast word after it? → comma.
Otherwise → comma (or semicolon).

**Edge cases:**
- Parenthetical that already contains commas → use **parentheses**, not commas.
- Attribution lines → colon or restructure.
- **Interrupted / cut-off dialogue → KEEP the em dash.** No other mark replicates it. *"I never said that I—"*
- Em dash for bare dramatic emphasis → remove it and restructure. *This is — important.* → *This is important.*

---

## Part 2 — Sentences and readability

Improve flow, pacing, clarity, and emotional impact while preserving the original
meaning, tone, scene content, and **voice**. Make the writing cleaner without
flattening it.

- **Complete sentences in narration.** No one- or two-word fragments in narrative or
  exposition; every sentence needs a subject and a verb. Convert one-word sentences
  into full ones, and combine adjacent fragments into a single grammatical sentence.
  **This governs narration — not dialogue** (see the dialogue note below).
  **Exception — deliberate fragments stay.** A fragment used for clear comedic or
  dramatic punch is a voice choice; keep it (e.g., "The Kirk jaw." or "Three days, no
  word."). The rule targets *accidental* fragments, not crafted ones. **But the
  negation–correction antithesis is not a protected fragment** — cut "Not X. Y." and
  "It wasn't X. It was Y." by default (see Part 3 and `references/ai-isms.md` §4.15).
  When in doubt about an ordinary fragment, leave it and flag it rather than flattening
  the beat.
- **Statements, not rhetorical questions** — except in character dialogue.
- **Questions take a question mark.** A sentence that asks something ends with a
  question mark, in dialogue and in tag questions (*How are you holding up?*, *Bills
  don't grieve, do they?*). Never put a period on a question for flat or numb affect;
  it reads as a typo. Imperatives (*Don't say it.*) keep the period.
- **Clear paragraphs** in logical order; vary sentence length and rhythm to build
  momentum (mechanical uniformity is itself an AI tell).
- **Compound sentences, handled with care.** Join independent clauses correctly — a
  comma plus a coordinating conjunction, or a semicolon — and make sure each clause
  can stand alone. Don't comma-splice; don't let them sprawl.
- **Break run-ons, and cap the clause count.** Split overlong, multi-clause sentences,
  chains of and-clauses especially, into two or more shorter ones. **Hard cap: two
  clauses per sentence, three at the absolute most.** A sentence carrying more than three
  clauses gets split, with no exception for "it flows." **Default to breaking.** Keep a
  longer sentence only when its length does work that splitting would destroy, mainly a
  character's speech rhythm or one genuinely breathless action beat, and even then stay
  within the cap. Do NOT excuse an and-chain as a "closing cadence," a "build," or because
  "it flows" — break it. With the fragment rule above, the target is varied sentence
  length, neither run-on nor choppy.
- **Plain over purple. Cut overwriting.** Default to plain, direct prose. **Purple prose
  is a primary failure mode here** — ornate or overwrought diction, stacked adjectives and
  adverbs, straining metaphors and similes, lofty abstractions (*soul, fate, void,
  unbearable*), and sentences reaching for a poetic effect they have not earned. Cut it.
  Prefer plainer language and lower literary density wherever it improves clarity; when a
  simpler word or a shorter sentence carries the meaning just as well, use it. Keep the
  voice, the tension, and the one idiosyncratic word that is exactly right, but avoid both
  purple prose *and* lifeless, dumbed-down prose, and when in doubt, err plainer. (See
  Part 3 vocabulary and `references/ai-isms.md` §2.3, §4.3, §4.7.)
- **Kill vague placeholder nouns, especially "something," "thing," and "shape."** First
  choice: name the actual noun the sentence is about. *She grabbed something* → *She grabbed
  the tire iron.* *He did the thing* → say what he did. The vague **"shape"** is its own
  habit to break: *it took on a shape, the shape of it, a name-shaped hole, a pattern still
  looking for the shape that would hold it* — name the real form, pattern, or realization,
  or cut the line. Only when no specific noun is right, pick a precise stand-in by register:
  concrete → *object, item, article, piece*; abstract → *matter, detail, element, aspect,
  point*; informal/comic voice → *contraption, gadget, doohickey, whatchamacallit*. Applies
  to the whole empty-placeholder family (*stuff, something, do that, took on a shape*).
  **Keep it when the vagueness is the point:** deliberate mystery, where not-naming is the
  effect (*something moved in the dark* — don't touch this in suspense); idioms and set
  phrases (*the right thing to do, for one thing, out of shape, in good shape*); dialogue
  and comedic setups that pay off. The target is lazy vagueness, not intentional phrasing.
  Full lists and examples in `references/ai-isms.md` §2.4.
- **Reading level: grades 9–12.**
- **Spelling: American.** Use US spellings: *gray* not *grey*, *color* not *colour*, *toward* not *towards*, *traveled* not *travelled*.
- **Serial (Oxford) comma:** "fried sugar, livestock, and diesel smoke" — not
  repeated *ands*.
- **Don't pile sensory lists.** Keep "X smelled of Y and Z and W" to a minimum; one or
  two items usually land harder than three (*The cab smelled of coffee and wet wool*,
  not *…coffee and wet wool and cigarettes and rain*). Applies to stacked sights and
  sounds too. A deliberate triad for rhythm is fine; a reflexive one is filler.
- **`and` vs. `with` vs. `but`:** pick the connector that fits the relationship.
  Combined? *with* is often truer than *and*. Contrasting? *but*. Don't default
  everything to *and*.
- **Speech and thought formatting.** Discrete spoken lines take quotation marks.
  Generalized or habitual reported speech (the kind of thing people *would* say) stays
  plain, no quotes and no italics, as free indirect speech. Reserve italics for a
  specific phrase intruding on the point-of-view character, or a single verbatim thought
  that earns the emphasis; overusing them spends their force. Internal thought stays
  mostly in plain close third.
- **Avoid em dashes** in your own prose; apply Part 1 to text you're editing.
- **Avoid the colon (:).** Do not use a colon in prose unless it is absolutely
  necessary. Replace it with a period, a comma, or a restructure, and use *including*
  or *namely* to lead into a list. Reserve the colon for the rare case where nothing
  else works, such as a clock time.

> **Narration vs. dialogue.** The complete-sentence / no-fragment rule is for narration.
> **Dialogue is looser than narration, but should still read smoothly** — natural
> contractions, the occasional short or unfinished reply, real rhythm. Don't over-fragment
> it: go easy on interruptions, trailing-offs, and clipped one-word volleys. Aim for speech
> that sounds like a real person talking in mostly complete, easy sentences, not staccato.
> Don't go the other way and stiffen it into formal, grammatically perfect lines either
> (that's an AI tell, §4.9). The target is natural, not jagged.
>
> **Fiction default:** third-person past tense, unless the project's Voice & Style
> Guide (story bible) specifies otherwise.

---

## Part 3 — Avoid AI-isms

Patterns that make writing read as machine-generated. Scan and rewrite them. The
**full flag lists and before/after rewrites are in `references/ai-isms.md`** —
consult it when drafting or revising, especially fiction. Summary of the categories:

**Conversational** — overused openers ("Certainly!", "Great question!", "Let's dive
in"); hollow filler ("It's worth noting that…", "When it comes to…"); restating the
question; automated closings ("I hope this helps!", "Let me know if…"); hedging
overload; reflexive fake enthusiasm ("fascinating," "remarkable").

**Vocabulary** — signature AI words (delve, leverage, robust, seamless, nuanced,
tapestry, landscape, navigate, foster, synergy, holistic…) — name the specific thing
instead. In fiction, watch recycled mood words (flicker, ache, hollow, shatter,
fragile…) and inflated diction (soul, fate, void, unbearable).

**Structural** — over-formatting (bullets/headers where prose serves better); fake
balance ("on one hand… on the other…"); the summary sandwich (tell them, tell them,
tell them you told them).

**Fiction** (the big one — see reference §4): vague abstraction ("a sense of dread
filled the room"); emotion labeling ("she was angry"); generic poetic phrasing ("the
silence was deafening"); high-frequency stock phrases ("her breath caught," "his jaw
tightened," "their eyes met"); clichéd sensory metaphors ("heart hammered," "ice in
her veins"); atmosphere as decoration; metaphor stacking; false profundity; dialogue
that's too clean; emotional overstatement in dialogue; reflective endings by default;
theme stated too directly; too many -ing participial openings; backstory inserted too
smoothly; the **negation–correction antithesis** ("it wasn't X, it was Y" — cut it).

**The core fix is always the same:** show, don't tell; choose the concrete, specific
detail that belongs only to this scene; trust the reader.

### Revision moves
Replace abstraction with visible behavior · replace cliché with a specific
sound/object/gesture · let action carry emotion · swap tidy insight for a partial
thought · break rhythmic sameness · loosen dialogue toward natural speech (not staccato) ·
cut the reflective last sentence (the scene already did the work).

### Preserve the human stuff
While removing AI-isms, don't sand off what makes writing alive: idiosyncratic
phrasing, real subtext, asymmetric dialogue, emotional contradiction, surprising-but-
precise detail, voice shaped by character, tension that doesn't resolve on cue.

---

## Part 4 — Propulsion (make every sentence pull)

Parts 1 through 3 remove what's wrong. This part adds what's missing: forward motion.
Clean prose that doesn't pull is still a failure. Every scene, paragraph, and line should
make the reader need the next one. Apply this to fiction and to any narrative nonfiction.
The active **propulsion-editor** skill enforces these rules on every chapter in the drafting
loop; the rules below are what it applies.

- **Every scene runs on a question.** Name the dramatic question the scene exists to
  answer (will she reach the car first? does he already know?), open it early, and keep it
  open as long as it can hold. When it closes, the scene is over, so cut to the next. A
  scene with no open question is why a passage reads as filler even when nothing in it is
  technically wrong.
- **Dole out information; never dump it.** Withhold. End paragraphs a half-step unresolved
  so the next one is necessary. Delay the consequence, hold back the name, let the reader
  lean in. If a reader could set the book down comfortably at a paragraph break mid-scene,
  the tension has leaked; tighten until they can't.
- **Causal, not additive.** Beats connect with *therefore* and *but*, not *and then*. "She
  found the letter, and then she went downstairs" is a list. "She found the letter, so she
  went down to burn it, but he was already in the kitchen" is a story. If two paragraphs
  can be reordered without breaking anything, the scene isn't building.
- **Enter late, leave early.** Start each scene as deep into it as the meaning survives,
  and cut out the moment its question closes. Drop the throat-clearing opening (waking,
  arriving, crossing a room, settling in) and the wind-down after the point has landed.
- **Active verbs carry motion; stative verbs stall it.** Hunt *was, were, had been, there
  was/were, began to, started to, could feel*. They hold the prose still. Recast into a
  subject doing something: "There was fear in the room" stalls; "Nobody moved" pulls.
- **End every chapter unresolved.** Close on a turn, a reversal, a new threat, a decision
  not yet acted on, or a question the next chapter must answer. Never end on a tidy
  reflective summary that gives the reader permission to stop.

---

### Quick self-check before returning prose
- No stray em dashes (except interrupted dialogue); each one replaced by the right mark.
- Narration in complete sentences; dialogue natural and a little looser, but not over-fragmented.
- No AI-ism openers, filler, or closings; no fake balance or summary sandwich.
- Emotions shown through behavior, not labeled; no stock fiction phrases or clichéd metaphors.
- No "it wasn't X, it was Y" negation-correction antithesis (cut by default; see §4.15).
- No vague placeholder nouns ("something," "thing," "stuff," "shape") where a specific word fits (deliberate vagueness/idioms/voice excepted).
- Series use the Oxford comma; connectors (`and`/`with`/`but`) fit the meaning.
- No piled sensory lists (one or two items, not three-plus); run-ons broken into shorter sentences, two clauses (three max) per sentence, except where length is the deliberate effect.
- No purple prose or overwriting; the plainer word or shorter sentence chosen wherever it reads as well.
- Reported speech plain (free indirect); italics rare and reserved; discrete spoken lines in quotes.
- Reads at grade 9–12 with the original voice and tension intact.
- Could any sentence appear in *any* novel unchanged? If so, make it specific.
- Propulsion (Part 4): every scene runs on an open question; paragraphs end pulling forward; beats connect by *therefore*/*but*, not *and then*; no comfortable mid-scene stopping point; the chapter ends unresolved.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill prose-style --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
