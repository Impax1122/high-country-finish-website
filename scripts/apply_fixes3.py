#!/usr/bin/env python3
"""Apply remaining mobile/responsive fixes - Fix 5 + Fix 6 only"""
import re

filepath = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Fix 5: Remove .gallery-grid standalone block (double-newline format in main style)
old_gallery_grid = ".gallery-grid {\n\n  display: grid;\n\n  grid-template-columns: repeat(3, 1fr);\n\n  gap: 12px;\n\n}\n\n.gallery-item {"
new_gallery_grid = ".gallery-item {"
if old_gallery_grid in content:
    content = content.replace(old_gallery_grid, new_gallery_grid, 1)
    print("Fix5-standalone: applied")
else:
    m = re.search(r'\.gallery-grid \{\s+display: grid;\s+grid-template-columns: repeat\(3, 1fr\);\s+gap: 12px;\s+\}\s+\.gallery-item', content)
    if m:
        content = content[:m.start()] + '.gallery-item' + content[m.end():]
        print("Fix5-standalone (regex): applied")
    else:
        print("Fix5-standalone: ALREADY REMOVED or not found")

# Fix 5: Remove .gallery-grid from 900px and 600px media queries
old_900 = "@media(max-width:900px){\n\n  .gallery-grid{grid-template-columns:1fr 1fr;}\n\n  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}\n\n}\n\n@media(max-width:600px){\n\n  .gallery-grid{grid-template-columns:1fr;}\n\n}"
new_900 = "@media(max-width:900px){\n\n  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}\n\n}"
if old_900 in content:
    content = content.replace(old_900, new_900, 1)
    print("Fix5-media: applied")
else:
    # Try removing just the lines with gallery-grid
    content = re.sub(r'\n\n  \.gallery-grid\{grid-template-columns:1fr 1fr;\}', '', content, count=1)
    content = re.sub(r'\n\n@media\(max-width:600px\)\{\n\n  \.gallery-grid\{grid-template-columns:1fr;\}\n\n\}', '', content, count=1)
    print("Fix5-media (regex): applied")

# Fix 6: Add touch-friendly heights for pf-photo-cell img
old_pf_cta = "/* CTA at bottom */\n#portfolio-full .pf-cta {\n  text-align: center;\n  margin-top: 32px;\n}"
new_pf_cta = "/* CTA at bottom */\n#portfolio-full .pf-cta {\n  text-align: center;\n  margin-top: 32px;\n}\n/* Fix 6: Touch-friendly portfolio card image heights */\n@media(max-width: 600px) {\n  #portfolio-full .pf-photo-cell img { height: 200px; }\n}\n@media(max-width: 480px) {\n  #portfolio-full .pf-photo-cell img { height: 160px; }\n}"
if old_pf_cta in content:
    content = content.replace(old_pf_cta, new_pf_cta, 1)
    print("Fix6: applied")
else:
    print("Fix6: pattern not found - may already be applied")

# Save
if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File saved ok. Size: " + str(len(content)) + " bytes")
else:
    print("No changes (may already be applied)")

# Verify key patterns
checks = [
    ("Fix1 mobile captions", "hero-gallery-overlay { opacity: 1; }"),
    ("Fix2 btn-portfolio mobile", "width: 100%;\n    padding: 16px 24px;"),
    ("Fix3 280px desktop", "height: 280px;"),
    ("Fix3 220px tablet", "height: 220px;"),
    ("Fix3 180px mobile", "height: 180px;"),
    ("Fix5 gallery-grid gone", ".gallery-grid {\n\n  display: grid;"),
    ("Fix6 200px", "pf-photo-cell img { height: 200px; }"),
    ("Fix6 160px", "pf-photo-cell img { height: 160px; }"),
    ("Fix4 padding>=60", "padding: 70px 0"),
    ("Fix7 hamburger JS", "function toggleNav()"),
]
print("\nVerification:")
for label, pattern in checks:
    found = pattern in content
    if label == "Fix5 gallery-grid gone":
        status = "REMOVED OK" if not found else "STILL PRESENT - PROBLEM"
    else:
        status = "OK" if found else "MISSING - PROBLEM"
    print("  " + label + ": " + status)
