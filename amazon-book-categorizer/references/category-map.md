# Amazon / KDP category & keyword reference

A working map of the Amazon US book category system plus the KDP rules and methods
this skill applies. **Treat it as a curated snapshot, not live truth.** Amazon
restructures categories, renames nodes, and changes limits; the live KDP category
picker is the final authority. Use this to reason from, then confirm exact names and
availability in KDP before the user publishes. Never present a node from this file as
guaranteed to exist under that exact wording today.

**When real, imported data exists, prefer it.** [`kdp-categories-us.md`](kdp-categories-us.md)
holds Amazon US category trees pasted from Publisher Rocket, with real node names and
**sales-to-rank** numbers. For any genre covered there, use *that* file as the source
of truth and pick rankable niches by its `→#1` / `→#10` columns; fall back to the
curated tree below only for genres not yet imported.

## How KDP categorization works

- A book is sold under **browse categories** (the "Books ›" and "Kindle Store ›"
  paths a reader clicks down) that map to **BISAC** subject codes behind the scenes.
  Print books are chosen by BISAC code; Kindle eBooks are chosen from KDP's own
  category list, which mirrors the Kindle Store browse tree.
- KDP currently lets an author select **up to three categories** per book in the
  dashboard. This limit has changed before (it was two for years, and Amazon has run
  promotions allowing more), and it can differ by marketplace. Say "up to three" and
  have the user confirm the current number in KDP.
- **Specific beats broad.** A book ranks, and earns an "Amazon Best Seller" or "New
  Release" flag, within the *smallest* category it charts in. A precise niche
  (`Domestic Thrillers`) is far easier to rank in than its giant parent
  (`Mystery, Thriller & Suspense`). Prefer the deepest node that genuinely fits over a
  broad one that technically fits.
- Pick categories that **honestly match the book.** Miscategorizing to chase an easy
  rank gets books re-filed or suppressed and earns angry reviews from mismatched
  readers.

## The Kindle eBook category tree (US) — top level

Kindle Store › Kindle eBooks › …

Arts & Photography · Biographies & Memoirs · Business & Money · Children's eBooks ·
Comics & Graphic Novels · Computers & Technology · Cookbooks, Food & Wine · Crafts,
Hobbies & Home · Education & Teaching · Engineering & Transportation · Health, Fitness
& Dieting · History · Humor & Entertainment · Law · LGBTQ+ eBooks · Literature &
Fiction · Medical eBooks · Mystery, Thriller & Suspense · Nonfiction · Parenting &
Relationships · Politics & Social Sciences · Reference · Religion & Spirituality ·
Romance · Science & Math · Science Fiction & Fantasy · Self-Help · Sports & Outdoors ·
Teen & Young Adult · Travel

## Key fiction branches (where the book-machine writes most)

Drill into these; verify the leaf names in KDP.

**Literature & Fiction** — *exact node names imported in
[`kdp-category-paths-us.md`](kdp-category-paths-us.md); use that list (no sales data).*
- › Genre Fiction › { Action & Adventure · Coming of Age · Family Life · Historical ·
  Literary Fiction · Psychological · Sagas · Short Stories · War · Women's Fiction }
- › Literary Fiction
- › Women's Fiction
- › Contemporary Fiction
- › Historical Fiction

**Mystery, Thriller & Suspense** — *exact node names imported in
[`kdp-category-paths-us.md`](kdp-category-paths-us.md); use that list (no sales data).*
- › Mystery › { Cozy · Police Procedurals · Private Investigators · Women Sleuths ·
  Amateur Sleuths · Historical Mystery · International Mystery & Crime }
- › Thrillers & Suspense › { Crime · Domestic · Psychological · Suspense · Legal ·
  Medical · Military · Spy · Technothrillers · Serial Killers · Financial }

**Romance**
- › { Contemporary · Historical · Paranormal · Romantic Suspense · Clean & Wholesome ·
  New Adult & College · Western · Holiday · LGBTQ+ }

**Science Fiction & Fantasy** — *imported with sales data; use
[`kdp-categories-us.md`](kdp-categories-us.md) as the source of truth for this genre.*
The full Fantasy / Science Fiction / Gaming trees (print and Kindle, which differ in
naming) live there. Quick orientation:
- › Science Fiction › { Space Opera · Hard Science Fiction · Dystopian · Time Travel ·
  Post-Apocalyptic · Military (Space Fleet / Space Marine) · Cyberpunk · Alien Invasion ·
  First Contact · Galactic Empire · Colonization · Humorous }
- › Fantasy › { Epic · Sword & Sorcery · Dark (print) / Dark Fantasy (Kindle) ·
  Historical · Paranormal & Urban (Contemporary / Paranormal / Urban) · Coming of Age ·
  Cozy · Dragons & Mythical Creatures · Myths & Legends · Humorous }
- Note the print/Kindle name splits (e.g. `Alternate` vs `Alternative History`,
  `Superheroes` vs `Superhero`) — pick from the tree matching your format.

**Teen & Young Adult**
- › Literature & Fiction › { Social & Family Issues · Coming of Age · Romance ·
  Mysteries & Thrillers · Science Fiction · Fantasy · Historical }

## Key nonfiction branches

- **Self-Help** › { Personal Transformation · Happiness · Motivational · Success ·
  Anxieties & Phobias · Relationships }
- **Business & Money** › { Entrepreneurship · Personal Finance · Marketing & Sales ·
  Management & Leadership · Small Business }
- **Health, Fitness & Dieting** › { Diets & Weight Loss · Exercise & Fitness · Mental
  Health · Nutrition }
- **Biographies & Memoirs** › { Memoirs · Specific Groups · Historical · Arts &
  Literature }
- **History** › { by region/era — United States, Europe, Military, Ancient, World }
- **Cookbooks, Food & Wine** › { by cuisine, method, or diet }
- **Religion & Spirituality** · **Parenting & Relationships** · **Reference** ·
  **Education & Teaching**

For any nonfiction book, anchor on the one true subject node, then add a second
category for the angle (e.g. a budgeting book: `Personal Finance` plus
`Self-Help › Success`).

## Keyword rules (the seven KDP fields)

- **Seven fields, up to 50 characters each.** Each field is a *phrase*; every word in
  every field is independently searchable, so combine related words to cover more of a
  real query (`small town murder mystery`, not just `mystery`).
- Word **order inside a field doesn't matter** for search, and you don't need to
  repeat a word that already appears in your title, subtitle, or another field.
- **Do not use:**
  - your own title, subtitle, series name, or author name (already indexed);
  - other authors', characters', or brands' **trademarked names** (e.g. naming a
    famous author or a series to ride their traffic) — KDP prohibits this;
  - subjective or unverifiable claims: `best`, `bestseller`, `bestselling`,
    `award-winning`, `#1`, `top`;
  - temporary or promotional terms: `free`, `on sale`, `new`, `available now`,
    `discount`, `sale`;
  - category names you can already pick directly as a category;
  - anything inaccurate or irrelevant to the book.
- Misleading or trademark-violating keywords can get a listing **suppressed**, so flag
  any borderline choice rather than slipping it in.

## Keyword research method

1. **Mine Amazon's own autocomplete.** In the Amazon (or Kindle Store) search bar,
   type a seed phrase for the book and read the dropdown suggestions — those are real,
   high-volume queries readers actually type. Note the ones that fit. (This is a step
   the *user* can do live; the skill suggests strong candidates from the metadata when
   it can't browse.)
2. **Translate comps into descriptive phrases.** "For readers of <Author>" becomes a
   *describing* phrase, never the author's name: a Gillian Flynn comp →
   `unreliable narrator thriller`, `dark domestic suspense`.
3. **Cover seven different angles, no near-duplicates:**
   genre/form · trope or theme · setting and era · protagonist or character type ·
   mood and tone · read-alike framing · reader intent ("books for fans of …").
4. **Keep every phrase honest and specific.** Concrete beats generic;
   `1980s small town disappearance` outperforms `good book`.

## Worked examples

**Literary domestic suspense (1980s small-town, missing teen, multi-POV)**
- Categories:
  1. `Mystery, Thriller & Suspense › Thrillers & Suspense › Domestic`
  2. `Mystery, Thriller & Suspense › Thrillers & Suspense › Psychological`
  3. `Literature & Fiction › Women's Fiction` (or `Literary Fiction`)
- Keywords: `small town disappearance` · `1980s coming of age` ·
  `multiple points of view` · `missing girl mystery` · `slow burn suspense` ·
  `survivor guilt drama` · `unsolved crime literary`

**Nonfiction personal-finance how-to (budgeting for new grads)**
- Categories:
  1. `Business & Money › Personal Finance › Budgeting & Money Management`
  2. `Self-Help › Personal Transformation`
  3. `Business & Money › Personal Finance › Money Management` (alt)
- Keywords: `budgeting for beginners` · `pay off debt fast` · `money habits guide` ·
  `personal finance for grads` · `save money in your 20s` · `build an emergency fund` ·
  `financial freedom plan`
