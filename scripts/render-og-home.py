#!/usr/bin/env python3
"""Render the home-page social share image, images/og-home.jpg.

Brand colors, type, and wording follow docs/BRAND.md (Brand Guide v2.3).
The mark is images/logo.png. Its flat brown field is dropped so the gold
artwork sits on the brand black; the drawing itself is not redrawn.

Size is 1200x630, the size of images/og-home.jpg and of the og:image
width/height tags in index.html. A 1024x538 preview is the same artwork
scaled down (1024/1200).

Requires Pillow:
    pip install pillow
    python3 scripts/render-og-home.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOGO_PATH = ROOT / "images" / "logo.png"
OUT_PATH = ROOT / "images" / "og-home.jpg"
FONT_DIR = Path(__file__).resolve().parent / "fonts"

WIDTH = 1200
HEIGHT = 630
SCALE = 2

# docs/BRAND.md
BLACK = (0x0C, 0x0C, 0x0C)
GOLD = (0xC9, 0xA8, 0x4C)
TEXT = (0xF0, 0xEC, 0xE4)
MUTED = (0x88, 0x88, 0x80)

BUSINESS_NAME = "High Country Finish & Repair Co."
LOCATION = "Arvada, CO"
DESCRIPTION = "Sign installation, vehicle wraps, and wall graphics."
URL = "highcountryfinish.com"

# Strings this image is allowed to show, besides the artwork already in logo.png.
COPY = (BUSINESS_NAME, LOCATION, DESCRIPTION, URL)

BANNED = (
    "premier",
    "denver metro",
    "flawless",
    "guarantee",
    "free site survey",
    "3m certified graphics installer",
    "window tint",
    "ada sign",
    "contract cutting",
)


def load_font(filename, size):
    return ImageFont.truetype(str(FONT_DIR / filename), size)


def text_width(font, text):
    return font.getlength(text)


def text_height(font):
    ascent, descent = font.getmetrics()
    return ascent + descent


def draw_centered(draw, text, font, top, fill, canvas_w):
    """Draw the whole line on one baseline. top is the top of the em box."""
    ascent, _descent = font.getmetrics()
    baseline = top + ascent
    draw.text((canvas_w / 2, baseline), text, font=font, fill=fill, anchor="ms")


def key_logo(logo):
    """Drop the logo file's flat brown field. Keep the gold artwork."""
    src = logo.convert("RGB")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    src_px = src.load()
    out_px = out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            r, g, b = src_px[x, y]
            # The field sits near rgb(32, 24, 19). Gold climbs well above that in red.
            alpha = max(0, min(255, int((r - 40) * 255 / 70)))
            out_px[x, y] = (r, g, b, alpha)
    cropped = out.crop(out.getbbox())
    return cropped


def assert_copy_is_allowed():
    for line in COPY:
        lowered = line.lower()
        for phrase in BANNED:
            if phrase in lowered:
                raise SystemExit(f"banned wording {phrase!r} in {line!r}")
    if "\n" in DESCRIPTION:
        raise SystemExit("description must stay one line")


def render():
    assert_copy_is_allowed()

    canvas_w = WIDTH * SCALE
    canvas_h = HEIGHT * SCALE
    image = Image.new("RGB", (canvas_w, canvas_h), BLACK)
    draw = ImageDraw.Draw(image)

    name_font = load_font("CormorantGaramond-SemiBold.ttf", 52 * SCALE)
    location_font = load_font("Inter-Medium.ttf", 18 * SCALE)
    body_font = load_font("Inter-Regular.ttf", 22 * SCALE)
    url_font = load_font("Inter-Medium.ttf", 18 * SCALE)

    logo = key_logo(Image.open(LOGO_PATH))
    logo_w = 280 * SCALE
    logo_h = round(logo.size[1] * logo_w / logo.size[0])
    logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

    gap_after_logo = 26 * SCALE
    gap_after_name = 10 * SCALE
    gap_after_location = 18 * SCALE
    rule_h = 2 * SCALE
    gap_after_rule = 18 * SCALE
    gap_after_body = 16 * SCALE

    name_h = text_height(name_font)
    location_h = text_height(location_font)
    body_h = text_height(body_font)
    url_h = text_height(url_font)

    block_h = (
        logo_h
        + gap_after_logo
        + name_h
        + gap_after_name
        + location_h
        + gap_after_location
        + rule_h
        + gap_after_rule
        + body_h
        + gap_after_body
        + url_h
    )
    y = (canvas_h - block_h) / 2

    image.paste(logo, ((canvas_w - logo_w) // 2, round(y)), logo)
    y += logo_h + gap_after_logo

    margin = 48 * SCALE
    for label, font in (
        (BUSINESS_NAME, name_font),
        (LOCATION, location_font),
        (DESCRIPTION, body_font),
        (URL, url_font),
    ):
        width = text_width(font, label)
        if width > canvas_w - margin * 2:
            raise SystemExit(f"{label!r} is {width:.0f}px wide; canvas allows {canvas_w - margin * 2:.0f}px")

    draw_centered(draw, BUSINESS_NAME, name_font, y, TEXT, canvas_w)
    y += name_h + gap_after_name

    draw_centered(draw, LOCATION, location_font, y, GOLD, canvas_w)
    y += location_h + gap_after_location

    rule_y = y
    y += rule_h + gap_after_rule

    draw_centered(draw, DESCRIPTION, body_font, y, MUTED, canvas_w)
    y += body_h + gap_after_body

    draw_centered(draw, URL, url_font, y, GOLD, canvas_w)

    final = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    final_draw = ImageDraw.Draw(final)
    # Bars and the short rule are painted at 1x so the downscale does not blur them.
    bar_h = 6
    final_draw.rectangle((0, 0, WIDTH, bar_h), fill=GOLD)
    final_draw.rectangle((0, HEIGHT - bar_h, WIDTH, HEIGHT), fill=GOLD)
    rule_top = round(rule_y / SCALE)
    rule_w = 48
    final_draw.rectangle(
        ((WIDTH - rule_w) / 2, rule_top, (WIDTH + rule_w) / 2, rule_top + 2),
        fill=GOLD,
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final.save(
        OUT_PATH,
        format="JPEG",
        quality=92,
        optimize=True,
        subsampling=0,
    )
    if final.size != (WIDTH, HEIGHT):
        raise SystemExit(f"unexpected size {final.size}")
    print(f"wrote {OUT_PATH.relative_to(ROOT)} {WIDTH}x{HEIGHT}")
    for line in COPY:
        print(f"  {line}")


if __name__ == "__main__":
    render()
