#!/usr/bin/env python3
"""Apply mobile/responsive fixes to vinyl-website/index.html"""
import re

filepath = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# =============================================================
# Fix 3 (desktop): Change hero-gallery-item img height 260px -> 280px
# =============================================================
old = '.hero-gallery-item img {\n  width: 100%;\n  height: 260px;'
new = '.hero-gallery-item img {\n  width: 100%;\n  height: 280px;'
assert old in content, "FAIL Fix3-desktop: pattern not found"
content = content.replace(old, new, 1)
print("Fix 3 (desktop 280px): applied")

# =============================================================
# Fixes 1, 2, 3 (tablet/mobile): Inject after .btn-portfolio:hover block
# inside the hero gallery <style> tag
# =============================================================
old_btn_hover = """.btn-portfolio:hover {
  background: var(--gold);
  color: #000;
}
</style>"""

new_btn_hover = """.btn-portfolio:hover {
  background: var(--gold);
  color: #000;
}
/* ── Mobile responsive fixes (Fix 1 + Fix 2 + Fix 3) ───────────── */
@media(max-width: 768px) {
  /* Fix 3: Tablet image height */
  .hero-gallery-item img { height: 220px; }
  /* Fix 1: Always show captions on touch/mobile (hover doesn't work) */
  .hero-gallery-item .hero-gallery-overlay { opacity: 1; }
}
@media(max-width: 480px) {
  /* Fix 3: Mobile image height */
  .hero-gallery-item img { height: 180px; }
}
@media(max-width: 600px) {
  /* Fix 2: Full-width "View Full Portfolio" button on mobile */
  .btn-portfolio {
    display: block;
    width: 100%;
    padding: 16px 24px;
    text-align: center;
    box-sizing: border-box;
  }
}
</style>"""

assert old_btn_hover in content, "FAIL Fix1+2+3-mobile: pattern not found"
content = content.replace(old_btn_hover, new_btn_hover, 1)
print("Fix 1 (mobile captions always visible): applied")
print("Fix 2 (btn-portfolio full-width mobile): applied")
print("Fix 3 (tablet 220px, mobile 180px): applied")

# =============================================================
# Fix 5: Remove .gallery-grid standalone CSS block (unused — no HTML uses it)
# =============================================================
old_gallery_grid = """.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.gallery-item {"""
new_gallery_grid = """.gallery-item {"""
assert old_gallery_grid in content, "FAIL Fix5-standalone: pattern not found"
content = content.replace(old_gallery_grid, new_gallery_grid, 1)
print("Fix 5 (removed .gallery-grid standalone block): applied")

# Remove .gallery-grid from 900px media query (keep .gallery-item rule)
old_900 = """@media(max-width:900px){
  .gallery-grid{grid-template-columns:1fr 1fr;}
  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}
}
@media(max-width:600px){
  .gallery-grid{grid-template-columns:1fr;}
}"""
new_900 = """@media(max-width:900px){
  .gallery-item{grid-column:span 1!important;grid-row:span 1!important;}
}"""
assert old_900 in content, "FAIL Fix5-media-queries: pattern not found"
content = content.replace(old_900, new_900, 1)
print("Fix 5 (removed .gallery-grid from media queries): applied")

# =============================================================
# Fix 6: Add touch-friendly image heights for pf-photo-cell img
# Inject after the pf-cta block inside portfolio-full <style>
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
assert old_pf_cta in content, "FAIL Fix6: pattern not found"
content = content.replace(old_pf_cta, new_pf_cta, 1)
print("Fix 6 (pf-photo-cell responsive heights 200px/160px): applied")

# =============================================================
# Fix 4: Verify #portfolio-full mobile padding
# =============================================================
if '#portfolio-full { padding: 70px 0; }' in content or '#portfolio-full { padding: 60px 0' in content:
    print("Fix 4 (portfolio-full mobile padding): already ≥60px — no change needed ✓")
else:
    print("Fix 4 WARNING: Could not verify mobile padding — manual check needed")

# =============================================================
# Fix 7: Verify nav hamburger
# =============================================================
if '.nav-toggle{display:flex;z-index:1000;}' in content and 'function toggleNav()' in content:
    print("Fix 7 (nav hamburger at 900px): verified working — no change needed ✓")
else:
    print("Fix 7 WARNING: Could not verify nav hamburger")

# =============================================================
# Write output
# =============================================================
if content == original:
    print("\nWARNING: No changes were made!")
else:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\nSaved. Total size: {len(content)} bytes")
