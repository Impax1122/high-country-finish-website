#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply all 4 tasks to the High Country Finish website files."""

import re

INDEX = r"C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html"
PORTFOLIO = r"C:\Users\Spaceship\.openclaw\workspace\vinyl-website\portfolio.html"

# ── helpers ─────────────────────────────────────────────────────────────────

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

# ═══════════════════════════════════════════════════════════════════════════
# TASK 1 — GSC verification meta tag in index.html
# ═══════════════════════════════════════════════════════════════════════════
print("=== TASK 1: GSC meta tag ===")
index_html = read_file(INDEX)

gsc_tag = '<meta name="google-site-verification" content="aNM9J4vS_h7rcjrL5kSvPEpy9PVS_u4ivNYltlOWwbk" />'

if gsc_tag in index_html:
    print("  SKIP: GSC tag already present.")
else:
    target = '<meta charset="UTF-8"/>'
    if target not in index_html:
        target = '<meta charset="UTF-8">'
    if target in index_html:
        replacement = target + "\n\n" + gsc_tag
        index_html = index_html.replace(target, replacement, 1)
        print(f"  DONE: inserted GSC tag immediately after '{target}'")
    else:
        print("  ERROR: could not find charset meta tag!")

# ═══════════════════════════════════════════════════════════════════════════
# TASK 3 — Update business address in index.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== TASK 3: Address update ===")

# The JSON-LD currently has parts split across fields. Find any plain-text or
# combined address occurrences and replace. Also check for old street numbers.
new_address = "9563 Joyce Way, Arvada, Colorado 80007"

# Pattern: any variation of the address that might appear as combined text
old_address_patterns = [
    # Common old patterns that might exist
    r"\d{4}\s+Joyce\s+Way[,\s]+Arvada[,\s]+Colorado\s+\d{5}",
    r"\d{4}\s+Joyce\s+Way[,\s]+Arvada[,\s]+CO\s+\d{5}",
    r"9563 Joyce Way, Arvada, CO 80007",
]

found_address = False
for pat in old_address_patterns:
    matches = re.findall(pat, index_html)
    if matches:
        for m in matches:
            if m != new_address:
                index_html = index_html.replace(m, new_address)
                print(f"  REPLACED: '{m}' → '{new_address}'")
                found_address = True
            else:
                print(f"  SKIP: address already correct: '{m}'")
                found_address = True

# Check if address appears in "CO" abbreviated form separate from JSON-LD
co_variant = "9563 Joyce Way, Arvada, CO 80007"
if co_variant in index_html:
    index_html = index_html.replace(co_variant, new_address)
    print(f"  REPLACED: '{co_variant}' → '{new_address}'")
    found_address = True

if not found_address:
    print("  INFO: No combined plain-text address found. JSON-LD uses split fields (already correct).")
    # Show what JSON-LD currently has for confirmation
    jld_match = re.search(r'"streetAddress":\s*"([^"]+)"', index_html)
    if jld_match:
        print(f"  JSON-LD streetAddress: {jld_match.group(1)}")

# ═══════════════════════════════════════════════════════════════════════════
# TASK 4 — Add logo to site header nav in index.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== TASK 4: Logo in nav ===")

logo_img = '<img src="images/logo.png" alt="High Country Finish logo" style="height:40px;width:auto;margin-right:8px;vertical-align:middle;" />'

# Check if a logo img already exists in the nav-logo anchor
nav_section_match = re.search(
    r'(<a[^>]+class="nav-logo"[^>]*>)(.*?)(</a>)',
    index_html, re.DOTALL
)

if nav_section_match:
    full_anchor = nav_section_match.group(0)
    anchor_open = nav_section_match.group(1)
    anchor_content = nav_section_match.group(2)
    anchor_close = nav_section_match.group(3)

    # Check if there's already a logo img (either path variant)
    if "logo.png" in anchor_content:
        print(f"  INFO: nav-logo anchor already contains a logo image.")
        print(f"  Content: {anchor_content.strip()[:120]}")
        # Check if the logo img uses absolute vs relative path
        if 'src="/images/logo.png"' in anchor_content:
            print("  NOTE: existing logo uses absolute path '/images/logo.png' — leaving as-is.")
        else:
            print("  NOTE: logo img present, no change needed.")
    else:
        # Need to add the logo before any text
        # Find text nodes in the anchor that look like brand names
        brand_patterns = [
            r'(High Country)',
            r'(<span[^>]*class="logo-main"[^>]*>)',
            r'(<div[^>]*class="logo-main"[^>]*>)',
        ]
        inserted = False
        for bp in brand_patterns:
            if re.search(bp, anchor_content):
                new_content = re.sub(bp, logo_img + r'\1', anchor_content, count=1)
                new_anchor = anchor_open + new_content + anchor_close
                index_html = index_html.replace(full_anchor, new_anchor, 1)
                print(f"  DONE: inserted logo img before brand text (pattern: {bp})")
                inserted = True
                break
        if not inserted:
            # Just prepend inside the anchor
            new_anchor = anchor_open + "\n    " + logo_img + anchor_content + anchor_close
            index_html = index_html.replace(full_anchor, new_anchor, 1)
            print("  DONE: prepended logo img inside nav-logo anchor.")
else:
    print("  ERROR: could not find nav-logo anchor!")

write_file(INDEX, index_html)
print("\nindex.html saved.")

# ═══════════════════════════════════════════════════════════════════════════
# TASK 2 — Fix weak alt texts in portfolio.html
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== TASK 2: Portfolio alt text fixes ===")
portfolio_html = read_file(PORTFOLIO)

alt_fixes = [
    ("novara-lobby.jpg",  "Novara lobby vinyl wall graphics installation Denver CO"),
    ("gym-wall-mural.jpg","Commercial gym wall mural vinyl installation Front Range Colorado"),
    ("kpa-lobby-sign.jpg","KPA lobby acrylic sign installation Arvada Colorado"),
    ("sea-lobby-wide.jpg","SEA lobby wide-angle vinyl wall graphics Denver Colorado"),
    ("sea-lobby-sign.jpg","SEA lobby dimensional sign installation Denver Colorado"),
]

for filename, new_alt in alt_fixes:
    # Match <img ... src="...filename..." ... alt="..."> in any attribute order
    pattern = re.compile(
        r'(<img\b[^>]*\bsrc="[^"]*' + re.escape(filename) + r'"[^>]*\balt=)"([^"]*)"',
        re.IGNORECASE
    )
    match = pattern.search(portfolio_html)
    if match:
        old_alt = match.group(2)
        if old_alt == new_alt:
            print(f"  SKIP {filename}: alt already correct.")
        else:
            portfolio_html = pattern.sub(r'\1"' + new_alt + '"', portfolio_html)
            print(f"  FIXED {filename}:")
            print(f"    OLD: {old_alt}")
            print(f"    NEW: {new_alt}")
    else:
        # Try reversed attribute order: alt before src
        pattern2 = re.compile(
            r'(<img\b[^>]*\balt=)"([^"]*)"([^>]*\bsrc="[^"]*' + re.escape(filename) + r'")',
            re.IGNORECASE
        )
        match2 = pattern2.search(portfolio_html)
        if match2:
            old_alt = match2.group(2)
            portfolio_html = pattern2.sub(r'\1"' + new_alt + r'"\3', portfolio_html)
            print(f"  FIXED {filename} (alt-before-src):")
            print(f"    OLD: {old_alt}")
            print(f"    NEW: {new_alt}")
        else:
            print(f"  WARNING: could not find img tag for {filename}")

# Fix any <img> tags with empty or missing src
empty_src_pattern = re.compile(r'<img\b[^>]*\bsrc=""[^>]*/>', re.IGNORECASE)
empty_src_matches = empty_src_pattern.findall(portfolio_html)
if empty_src_matches:
    for bad_img in empty_src_matches:
        portfolio_html = portfolio_html.replace(bad_img, "")
        print(f"  REMOVED empty-src img: {bad_img[:80]}")
else:
    print("  No empty-src img tags found.")

# Also check for <img> missing src entirely
no_src_pattern = re.compile(r'<img\b(?![^>]*\bsrc=)[^>]*/>', re.IGNORECASE)
no_src_matches = no_src_pattern.findall(portfolio_html)
if no_src_matches:
    for bad_img in no_src_matches:
        portfolio_html = portfolio_html.replace(bad_img, "")
        print(f"  REMOVED no-src img: {bad_img[:80]}")
else:
    print("  No missing-src img tags found.")

write_file(PORTFOLIO, portfolio_html)
print("\nportfolio.html saved.")
print("\nAll tasks complete.")
