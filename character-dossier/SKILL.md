---
name: character-dossier
description: Interviews the user to build a per-book character dossier — the cast roster with each character's name, description, role, want, fear, and a secret — and saves it as characters.json in the book project folder, so chapters stay consistent in names, voice, appearance, motivation, and arcs. Use this whenever a new story, novel, or fiction book is being started, or when the user wants to create, define, add, edit, or review characters, build a character roster/profiles/dossier, or keep characters consistent across a manuscript. (For world rules, voice, and plot beats, see the companion story-bible skill.) When a story is being set up, proactively offer to build the dossier before chapters are drafted.
---

# Character Dossier

A story lives or dies on its characters staying *themselves* — same name spelling,
same eye color, same way of talking, the same wound driving them — across dozens
of pages written in different sittings. This skill captures that information once,
by interviewing the user, and stores it where the writing and editing stages can
consult it.

## Where the dossier lives (important)

The dossier is **unique to each book**, so it is **not** stored in this skill. It
is written to **`characters.json` in the book's project folder**, next to
`book.json`, `outline.json`, and `chapters/`. One book, one cast, one file.

If there's no project folder yet (the user is just starting a story), pick the
same default the book-machine uses — `./<slug-of-title-or-topic>/` — or ask where
the book lives, then write `characters.json` there.

## The data model

`characters.json`:
```json
{
  "characters": [
    {
      "id": "kebab-case-slug",
      "name": "Full name as it appears in prose",
      "aliases": ["nickname", "title", "what others call them"],
      "role": "protagonist | antagonist | supporting | minor",
      "summary": "One sentence: who they are in this story.",
      "appearance": "Physical details that recur and must stay consistent.",
      "personality": "Temperament, traits, how they come across.",
      "voice": "How they speak — diction, rhythm, verbal tics, what they never say.",
      "background": "Relevant backstory the writer should know.",
      "motivation": "Core WANT (the goal they chase) and core NEED (the deeper drive).",
      "fear": "Core fear — what they're running from. Drives them from underneath.",
      "secret": "One thing true about them that NOBODY else in the story knows yet. Drives hidden motivation; reveal only when the plot does.",
      "relationships": "Ties to other characters, by name.",
      "arc": "How they change from beginning to end.",
      "continuityNotes": "Hard facts that must NEVER drift: age, eye/hair color, scars, accent, left-handed, etc."
    }
  ]
}
```

Every field except `id` and `name` is optional — capture what the user knows and
leave the rest blank. `continuityNotes` is the highest-value field for keeping a
book consistent, so make a point of filling it.

## How to run the interview

Your job is to **prompt the user** for this information, not to invent a cast and
present it as fact. Be a helpful collaborator running a relaxed interview, not a
form to be filled in 13 fields at a time.

1. **Get the cast first, lightly.** Ask who the main characters are — just names
   and rough roles (e.g., "Who's the story about, and who's standing in their
   way?"). This gives you the list before you go deep on anyone.

2. **Go deeper, one character at a time, in small batches.** For each important
   character, ask grouped, natural questions rather than reciting the schema:
   - "Tell me about **{name}** — what do they want, and what's actually driving
     them underneath that?" (→ `motivation`)
   - "What are they most afraid of — what are they running from?" (→ `fear`)
   - "What's one thing true about them that **nobody else in the story knows yet**?"
     (→ `secret` — the engine of their hidden motivation; it gets revealed only when
     the plot calls for it, so flag it as spoiler-sensitive)
   - "How do they come across to people? How do they talk?"
   - "Anything about how they look, or any fixed details I should keep straight
     across the whole book?" (→ `continuityNotes`)
   - "Who matters to them, and how do those relationships change?"

3. **Never block on a blank.** If the user doesn't know a field yet, leave it
   empty and move on. A partial dossier is useful; an interrogation is not.

4. **Offer to fill gaps, with approval.** It's fine — often welcome — to *propose*
   a backstory, a voice, or a name and let the user accept, tweak, or reject it:
   "Want me to suggest a backstory that fits?" Suggest; don't impose. What the
   user confirms is canon.

5. **Minor characters get a light touch.** A name, a role, and one defining note
   is plenty. Spend the depth on the people the book actually follows.

## Saving and updating

Write the collected cast to `characters.json` (create or merge — don't clobber
existing characters when adding new ones; match by `id`). After saving, show the
user a short roster (name — role — one-line summary) so they can confirm or
correct it.

Support partial runs on an existing book:
- "Add a character" → interview just the new one and append.
- "Update {name}" / "she's actually got a sister" → edit that entry.
- "Who's in this story?" → read `characters.json` and summarize the cast.

## How the rest of the machine uses this

The **chapter-writer** and **book-editor** skills read `characters.json` when it
exists — the writer to keep every character true to the dossier, the editor to
catch drift (a name spelled two ways, eyes that change color, a voice that
wanders). That's the payoff for building the dossier up front: consistency you
don't have to police by hand. Keep the file current as the story evolves so those
stages stay accurate.

## Audit log
When a run finishes, record it so there's a trail of what happened — that the skill ran,
its result, the items it went through, and the outputs it wrote. Append one entry with the
shared logger:

`python <skills-dir>/lib/audit_log.py --skill character-dossier --target <book-folder> --status <PASS|FAIL|DONE|verdict> --item "<each item processed>" --output "<each file written>" --note "<one-line summary>"`

Use `DONE` when the skill has no pass/fail; otherwise its verdict (PASS/FAIL, GO/HOLD,
READY/NOT-READY, or the band). `--item` is what the run went through (usually the chapters);
`--output` is each file written (omit if read-only). Full convention: `lib/AUDIT-LOG.md`.
