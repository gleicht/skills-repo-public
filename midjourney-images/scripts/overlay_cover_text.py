#!/usr/bin/env python3
"""Overlay clean, correctly-spelled text onto Midjourney cover art.

Midjourney renders text as gibberish, so the usual workflow is: generate the
artwork only, then lay real text on top with this script. It paints feathered
banners over the (often garbled) top/bottom strips of the image so the baked-in
gibberish is hidden, then draws a title, an optional series/subtitle line, and
an optional author line — with optional outline and drop shadow.

Everything is parameterized; nothing is hard-coded to a particular book.

Dependencies: Pillow  (pip install Pillow)

Examples
--------
Basic title + author:
  python overlay_cover_text.py --image art.png --output cover.png \\
      --title "Rocketship Rampart" --author "Jane Doe"

Full styling (series line, colors, author outline + shadow):
  python overlay_cover_text.py --image art.png --output cover.png \\
      --title "Rocketship Rampart" --series "BOOK TWO OF THREE" --author "Jane Doe" \\
      --title-color "#D46837" --accent-color "#D6B254" --author-color "#E0C9B5" \\
      --author-outline "#2E66C4" --author-outline-width 3 --author-shadow "#28160A"
"""
import argparse
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required. Install with: pip install Pillow")


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_font(path, size):
    """Load a TrueType font, falling back through common bold faces."""
    candidates = [path] if path else []
    candidates += ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf",
                   "arial.ttf", "DejaVuSans.ttf"]
    for name in candidates:
        if not name:
            continue
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_line(draw, text, font, cx, cy, fill, W, tracking=0,
              shadow=None, shadow_off=8, stroke_w=0, stroke_fill=None):
    """Draw horizontally-centered text with optional letter tracking,
    drop shadow, and outline."""
    widths = [draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0]
              for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    asc, desc = font.getmetrics()
    x = cx - total / 2
    y = cy - (asc + desc) / 2
    for ch, w in zip(text, widths):
        if shadow is not None:
            draw.text((x + shadow_off, y + shadow_off), ch, font=font,
                      fill=shadow, stroke_width=stroke_w, stroke_fill=shadow)
        draw.text((x, y), ch, font=font, fill=fill,
                  stroke_width=stroke_w, stroke_fill=stroke_fill)
        x += w + tracking


def fit_font(path, text, max_width, start_size):
    """Shrink the font until the text fits within max_width."""
    size = start_size
    while size > 24:
        f = load_font(path, size)
        w = f.getbbox(text)[2] - f.getbbox(text)[0]
        if w <= max_width:
            return f, size
        size -= 6
    return load_font(path, size), size


def gradient_banner(overlay_draw, W, y0, y1, color, max_alpha, fade_from_top):
    """Draw a vertical alpha gradient band between y0 and y1.
    fade_from_top=True: opaque at y0 fading to transparent at y1 (top banner).
    fade_from_top=False: transparent at y0 fading to opaque at y1 (bottom banner)."""
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / span
        a = int(max_alpha * (1 - t)) if fade_from_top else int(max_alpha * t)
        overlay_draw.line([(0, y), (W, y)], fill=color + (a,))


def main():
    p = argparse.ArgumentParser(description="Overlay clean text on cover art.")
    p.add_argument("--image", required=True, help="Input artwork (PNG/JPG)")
    p.add_argument("--output", required=True, help="Output path (PNG)")
    p.add_argument("--title", default=None, help="Title text (auto-wrapped/centered, top)")
    p.add_argument("--series", default=None, help="Optional series/subtitle line under the title")
    p.add_argument("--author", default=None, help="Author line (bottom by default)")
    p.add_argument("--author-pos", choices=["top", "bottom"], default="bottom")
    p.add_argument("--uppercase", action="store_true", help="Force title/series/author to UPPERCASE")
    p.add_argument("--font", default=None, help="Path to a .ttf font (optional)")
    p.add_argument("--title-color", default="#F5F5FA")
    p.add_argument("--series-color", default="#D6B254")
    p.add_argument("--accent-color", default="#D6B254", help="Color of the rule under the title")
    p.add_argument("--author-color", default="#F5F5FA")
    p.add_argument("--author-outline", default=None, help="Hex color for an outline around the author")
    p.add_argument("--author-outline-width", type=int, default=0)
    p.add_argument("--author-shadow", default=None, help="Hex color for an author drop shadow")
    p.add_argument("--banner-color", default="#08101E", help="Color of the cover-up banners")
    p.add_argument("--no-top-banner", action="store_true")
    p.add_argument("--no-bottom-banner", action="store_true")
    p.add_argument("--bottom-opaque", action="store_true",
                   help="Make the very bottom fully opaque (hides garbled baked-in text)")
    args = p.parse_args()

    img = Image.open(args.image).convert("RGBA")
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    banner = hex_to_rgb(args.banner_color)

    title_top = args.author_pos == "bottom"  # title at top unless author is on top

    # Banners over the strips where Midjourney's gibberish usually sits
    if not args.no_top_banner:
        solid = int(H * 0.205)
        od.rectangle([0, 0, W, solid], fill=banner + (255,))
        gradient_banner(od, W, solid, solid + int(H * 0.14), banner, 255, fade_from_top=True)
    if not args.no_bottom_banner:
        bot_max = 255 if args.bottom_opaque else 220
        gradient_banner(od, W, int(H * 0.78), int(H * 0.90), banner, bot_max, fade_from_top=False)
        od.rectangle([0, int(H * 0.90), W, H], fill=banner + (bot_max,))

    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    def cased(s):
        return s.upper() if args.uppercase else s

    # ---- Title block (top) ----
    title_y = int(H * 0.06)
    if args.title:
        words = cased(args.title).split()
        # split long titles into up to two balanced lines
        if len(words) > 2:
            mid = (len(words) + 1) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        else:
            lines = words if len(words) == 2 else [cased(args.title)]
        max_w = int(W * 0.86)
        longest = max(lines, key=len)
        tfont, tsize = fit_font(args.font, longest, max_w, int(W * 0.16))
        gap = int(tsize * 0.9)
        for i, line in enumerate(lines):
            draw_line(d, line, tfont, W / 2, title_y + gap // 2 + i * gap,
                      hex_to_rgb(args.title_color), W, tracking=int(tsize * 0.05),
                      shadow=(0, 0, 0))
        rule_y = title_y + gap * len(lines) + 10
        d.rectangle([(W / 2 - W * 0.16, rule_y), (W / 2 + W * 0.16, rule_y + max(5, int(H * 0.003)))],
                    fill=hex_to_rgb(args.accent_color))
        if args.series:
            sfont = load_font(args.font, int(W * 0.05))
            draw_line(d, cased(args.series), sfont, W / 2, rule_y + int(H * 0.03),
                      hex_to_rgb(args.series_color), W, tracking=int(W * 0.012), shadow=(0, 0, 0))

    # ---- Author block ----
    if args.author:
        ay = int(H * 0.935) if args.author_pos == "bottom" else int(H * 0.07)
        afont = load_font(args.font, int(W * 0.078))
        draw_line(d, cased(args.author), afont, W / 2, ay,
                  hex_to_rgb(args.author_color), W, tracking=int(W * 0.006),
                  shadow=hex_to_rgb(args.author_shadow) if args.author_shadow else (0, 0, 0),
                  shadow_off=10,
                  stroke_w=args.author_outline_width,
                  stroke_fill=hex_to_rgb(args.author_outline) if args.author_outline else None)

    img.convert("RGB").save(args.output)
    print(f"Saved {args.output} ({W}x{H})")


if __name__ == "__main__":
    main()
