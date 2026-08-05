# Midjourney Images — a Claude Code skill

Generate images in **your own Midjourney account** straight from Claude Code.

Midjourney has **no public API and no MCP server**, so there's no key-based
integration to install. This skill instead lets Claude drive your **logged-in
browser** (via the "Claude for Chrome" extension) to operate the Midjourney web
app the same way you would — composing prompts, reading the result grid,
upscaling, and downloading.

---

## What it does

- Connects to your Midjourney session through the Claude for Chrome extension
- Submits prompts (with `--ar`, `--stylize`, `--chaos`, etc.)
- Reads and describes the 4-image grid so you can pick a favorite
- Upscales (Subtle/Creative), varies, and downloads the result
- Adds **clean, correctly-spelled text** to cover art afterward, via a bundled
  helper script (Midjourney itself renders text as gibberish)

## Requirements

- **Claude Code** (this skill lives in `~/.claude/skills/`)
- The **"Claude for Chrome" extension**, installed and signed into the same
  Claude account
- A **Midjourney account** that you are already **logged into** in that Chrome
- **Python 3** with **Pillow** (`pip install Pillow`) — only needed for the
  text-overlay helper script

> You must be logged into Midjourney yourself. The skill never enters passwords,
> creates accounts, or solves CAPTCHAs.

## Install

**From the packaged file:** place `midjourney-images.skill` (or the unzipped
`midjourney-images/` folder) into your skills directory:

```
~/.claude/skills/midjourney-images/
├── SKILL.md
├── README.md
└── scripts/
    └── overlay_cover_text.py
```

On Windows that's `C:\Users\<you>\.claude\skills\`. Restart Claude Code (or open
`/skills`) so it picks up the new skill.

## Use it

Just ask in plain language — the skill triggers on Midjourney image requests:

- "Generate a Midjourney image of a neon cyberpunk alley, 16:9."
- "Connect to Midjourney and make 4 book-cover options for my sci-fi novel."
- "Upscale that render and download the full-res version."

Claude will confirm the prompt with you **before** submitting (it spends your
Midjourney credits), show you the grid, and walk through upscaling/downloading.

### Adding real text to cover art

Because Midjourney can't render text, generate the **artwork only**, then overlay
the title/author with the bundled script:

```bash
python scripts/overlay_cover_text.py \
  --image downloaded_art.png --output finished_cover.png \
  --title "Book Title" --series "BOOK TWO OF THREE" --author "Author Name" \
  --uppercase --title-color "#D46837" --accent-color "#D6B254" \
  --author-color "#E0C9B5" --author-outline "#2E66C4" --author-outline-width 3 \
  --author-shadow "#28160A" --bottom-opaque
```

Run `python scripts/overlay_cover_text.py -h` for all options (colors, fonts,
banner controls, author placement, etc.).

## Guardrails

- Confirms before **spending credits** (generate/upscale/vary) and before
  **downloading**.
- Never handles passwords, account creation, payments, or CAPTCHAs.
- The first action on `midjourney.com` triggers an "Allow once" browser-
  permission prompt — that's expected.

## Limitations

- It's **UI automation**, not an API — slower and more fragile; Midjourney site
  changes can break steps.
- You must stay **logged in** to Midjourney in the controlled browser.
- **Text in images comes out garbled** — always add real text afterward.
- Every generation/upscale uses your **Midjourney plan credits**.

## Privacy

This skill contains **no account credentials or personal data**. It operates
only through your own logged-in browser session and your local files.

---

*If Midjourney ever ships a public API or MCP server, a proper key-based
integration would replace this browser-driven approach.*
