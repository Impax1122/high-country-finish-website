"""Verification script for SEO pass on index.html"""

import re
from pathlib import Path

content = Path(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html').read_text(encoding='utf-8')

# Title
m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
title = m.group(1).strip() if m else "NOT FOUND"
print(f"TITLE ({len(title)} chars): {title}")

# Meta description
m = re.search(r'<meta name="description" content="(.*?)"', content)
desc = m.group(1) if m else "NOT FOUND"
print(f"META DESC ({len(desc)} chars): {desc}")

# Canonical
m = re.search(r'<link rel="canonical" href="(.*?)"', content)
print(f"CANONICAL: {m.group(1) if m else 'NOT FOUND'}")

# OG tags
for tag in ['og:title', 'og:description', 'og:url', 'og:image']:
    m = re.search(rf'<meta property="{tag}" content="(.*?)"', content)
    print(f"OG {tag}: {m.group(1) if m else 'NOT FOUND'}")

# Schema
has_schema = '"@type": "LocalBusiness"' in content
print(f"SCHEMA LocalBusiness: {'PRESENT' if has_schema else 'MISSING'}")

# H1 count
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
print(f"H1 COUNT: {len(h1s)}")
for h in h1s:
    print(f"  H1: {re.sub('<[^>]+>', '', h).strip()}")

# H2 count
h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
print(f"H2 COUNT: {len(h2s)}")
for h in h2s:
    print(f"  H2: {re.sub('<[^>]+>', '', h).strip()}")

# H3 count
h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
print(f"H3 COUNT: {len(h3s)}")
for h in h3s:
    print(f"  H3: {re.sub('<[^>]+>', '', h).strip()}")

# IMG tags — check for missing/empty alt
imgs = re.findall(r'<img[^>]+>', content)
no_alt = [img for img in imgs if 'alt=""' in img or 'alt= ' in img or ' alt' not in img]
print(f"\nTOTAL IMG TAGS: {len(imgs)}")
print(f"IMG TAGS WITH MISSING/EMPTY ALT: {len(no_alt)}")
for img in no_alt:
    # Print truncated version
    print(f"  {img[:120]}")

# Footer NAP check
has_address = '9563 Joyce Way' in content
has_phone_footer = '303-882-4656' in content
print(f"\nFOOTER HAS ADDRESS: {has_address}")
print(f"FOOTER HAS PHONE: {has_phone_footer}")
