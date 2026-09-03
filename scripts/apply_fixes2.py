#!/usr/bin/env python3
"""Apply remaining mobile/responsive fixes to vinyl-website/index.html (Fix 5 + Fix 6)"""

filepath = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# =============================================================
# Fix 5: Remove .gallery-grid standalone CSS block
# (file uses \n\n double-newline formatting in main style block)
# =============================================================
old_gallery_grid = """.gallery-grid {\n\n  display: grid;\n\n  grid-template-columns: repeat(3, 1fr);\n\n  gap: 12px;\n\n}\n\n.gallery-item {"""
new_gallery_grid = """.gallery-item {"""
if old_gallery_grid in content:
    content = content.replace(old_gallery_grid, new_gallery_grid, 1)
    print("Fix 5 (removed .gallery-grid standalone block): applied")
else:
    print("Fix 5 standalone: pattern not found — checking alt pattern")
    # Try alternative
    import re
    m = re.search(r'\.gallery-grid \{\s+display: grid;\s+grid-template-columns: repeat\(3, 1fr\);\s+gap: 12px;\s+\}\s+\.gallery-item', content)
    if m:
        content = content[:m.start()] + '.gallery-item' + content[m.end():]
        print("Fix 5 (removed .gallery-grid via regex): applied")
    else:
        print("Fix 5 FAIL: could not find .gallery-grid standalone block")

# Remove .gallery-grid from 900px media query (double-newline format)
old_900 = """@media(max-width:900px){\n\n  .gallery-grid{grid-template-columns:1fr 1fr;}\n\n  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}\n\n}\n\n@media(max-width:600px){\n\n  .gallery-grid{grid-template-columns:1fr;}\n\n}"""
new_900 = """@media(max-width:900px){\n\n  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}\n\n}"""
if old_900 in content:
    content = content.replace(old_900, new_900, 1)
    print("Fix 5 (removed .gallery-grid from media queries): applied")
else:
    print("Fix 5 media queries: trying regex approach")
    import re
    # Remove gallery-grid line from 900px block
    content = re.sub(r'\n\n  \.gallery-grid\{grid-template-columns:1fr 1fr;\}', '', content, count=1)
    # Remove the 600px block containing only gallery-grid
    content = re.sub(r'\n\n@media\(max-width:600px\)\{\n\n  \.gallery-grid\{grid-template-columns:1fr;\}\n\n\}', '', content, count=1)
    print("Fix 5 (removed .gallery-grid from media queries via regex): applied")

# =============================================================
# Fix 6: Add touch-friendly image heights for pf-photo-cell img
# The portfolio-full style block uses single newlines
# =============================================================
old_pf_cta = """/* CTA at bottom */
#portfolio-full .pf-cta {
  text-align: center;
  margin-top: 32px;
}"""
new_pf_cta = """/* CTA at bottom */
#portfolio-full .pf-cta {
  text-align: center;
  margin-top: 32px;
}
/* Fix 6: Touch-friendly portfolio card image heights */
@media(max-width: 600px) {
  #portfolio-full .pf-photo-cell img { height: 200px; }
}
@media(max-width: 480px) {
  #portfolio-full .pf-photo-cell img { height: 160px; }
}"""
if old_pf_cta in content:
    content = content.replace(old_pf_cta, new_pf_cta, 1)
    print("Fix 6 (pf-photo-cell responsive heights 200px/160px): applied")
else:
    print("Fix 6 FAIL: pattern not found")

# =============================================================
# Verify Fixes 1, 2, 3 already applied
# =============================================================
checks = [
    ('Fix 1 (mobile captions)', 'hero-gallery-overlay { opacity: 1; }'),
    ('Fix 2 (btn-portfolio mobile)', '.btn-portfolio {'),
    ('Fix 3 (280px desktop)', 'height: 280px;'),
    ('Fix 3 (220px tablet)', 'height: 220px;'),
    ('Fix 3 (180px mobile)', 'height: 180px;'),
    ('Fix 4 (portfolio padding >=60px)', 'padding: 70px 0'),
    ('Fix 7 (nav hamburger)', 'function toggleNav()'),
]
print()
for label, pattern in checks:
    status = "✓ present" if pattern in content else "✗ MISSING"
    print(f"  {label}: {status}")

# =============================================================
# Write output
# =============================================================
if content == original:
    print("\nWARNING: No changes were made!")
else:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\nSaved. Total size: {len(content)} bytes")
