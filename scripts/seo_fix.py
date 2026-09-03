"""Fix remaining SEO issues: H1, OG title, meta description."""

from pathlib import Path
import re

HTML_FILE = Path(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html')
content = HTML_FILE.read_text(encoding='utf-8')

# ── FIX 1: H1 — file uses \n\n double newlines ──────────────────────────────
old_h1 = '<h1 class="hero-title">\n\n        Precision craft.<br/>\n\n        <em>Elevated finish.</em>\n\n      </h1>'
new_h1 = '<h1 class="hero-title">\n\n        Commercial Vinyl Graphics &amp; Sign Installation<br/>\n\n        <em>in Denver</em>\n\n      </h1>'
if old_h1 in content:
    content = content.replace(old_h1, new_h1)
    print("H1 replaced OK")
else:
    print("H1 NOT FOUND — trying regex fallback")
    content = re.sub(
        r'(<h1 class="hero-title">)(.*?)(</h1>)',
        r'\1\n\n        Commercial Vinyl Graphics &amp; Sign Installation<br/>\n\n        <em>in Denver</em>\n\n      \3',
        content, flags=re.DOTALL
    )
    print("H1 regex fallback applied")

# ── FIX 2: OG title — file has & not &amp; ───────────────────────────────────
old_og = '<meta property="og:title" content="High Country Finish and Repair CO | Denver Vinyl & Sign Specialists"/>'
new_og = '<meta property="og:title" content="Sign Installation Denver | High Country Finish CO"/>'
if old_og in content:
    content = content.replace(old_og, new_og)
    print("OG title replaced OK")
else:
    print("OG title NOT FOUND — trying regex fallback")
    content = re.sub(
        r'<meta property="og:title" content="[^"]*"/>',
        new_og,
        content
    )
    print("OG title regex fallback applied")

# ── FIX 3: Shorten meta description to under 155 rendered chars ──────────────
# Current (too long): Expert sign installation &amp; commercial vinyl graphics in Denver.
#   Lobby signs, vehicle graphics, storefront wraps &amp; window frosting. Call 303-882-4656 for a free quote.
# New (139 rendered chars):
new_desc = '<meta name="description" content="Denver sign installation &amp; commercial vinyl graphics — lobby signs, vehicle graphics, window frosting &amp; storefront wraps. Call 303-882-4656."/>'
content = re.sub(
    r'<meta name="description" content="[^"]*"/>',
    new_desc,
    content
)
print("Meta description updated OK")

# ── WRITE ─────────────────────────────────────────────────────────────────────
HTML_FILE.write_text(content, encoding='utf-8')
print("Fix script complete.")
