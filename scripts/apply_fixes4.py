#!/usr/bin/env python3
"""Apply Fix 1, Fix 2, Fix 3 to vinyl-website/index.html"""

filepath = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Fix 3 desktop: 260px -> 280px for .hero-gallery-item img
old_h = "hero-gallery-item img {\n  width: 100%;\n  height: 260px;"
new_h = "hero-gallery-item img {\n  width: 100%;\n  height: 280px;"
if old_h in content:
    content = content.replace(old_h, new_h, 1)
    print("Fix3 desktop (280px): applied")
else:
    print("Fix3 desktop: pattern not found")

# Fix 1 + Fix 2 + Fix 3 tablet/mobile: inject after .btn-portfolio:hover block
old_inject = ".btn-portfolio:hover {\n  background: var(--gold);\n  color: #000;\n}\n</style>"
new_inject = """.btn-portfolio:hover {
  background: var(--gold);
  color: #000;
}
/* Fix 1+2+3: Mobile responsive rules */
@media(max-width: 768px) {
  .hero-gallery-item img { height: 220px; }
  .hero-gallery-item .hero-gallery-overlay { opacity: 1; }
}
@media(max-width: 480px) {
  .hero-gallery-item img { height: 180px; }
}
@media(max-width: 600px) {
  .btn-portfolio {
    display: block;
    width: 100%;
    padding: 16px 24px;
    text-align: center;
    box-sizing: border-box;
  }
}
</style>"""

if old_inject in content:
    content = content.replace(old_inject, new_inject, 1)
    print("Fix1+2+3 mobile: applied")
else:
    print("Fix1+2+3 mobile: pattern not found")

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved ok. Size: " + str(len(content)) + " bytes")
else:
    print("No changes made")

# Verify
checks = [
    ("Fix1 mobile captions @media", "@media(max-width: 768px)"),
    ("Fix1 overlay opacity 1 in media", "hero-gallery-overlay { opacity: 1; }\n}"),
    ("Fix2 btn full-width", "width: 100%;\n    padding: 16px 24px;"),
    ("Fix3 280px", "height: 280px;"),
    ("Fix3 220px", "height: 220px;"),
    ("Fix3 180px", "height: 180px;"),
    ("Fix5 gallery-grid removed", ".gallery-grid {\n\n  display: grid;"),
    ("Fix6 200px", "pf-photo-cell img { height: 200px; }"),
    ("Fix6 160px", "pf-photo-cell img { height: 160px; }"),
    ("Fix4 padding ok", "padding: 70px 0"),
    ("Fix7 hamburger", "function toggleNav()"),
]
print("\nVerification:")
for label, pattern in checks:
    found = pattern in content
    if "removed" in label.lower():
        status = "REMOVED OK" if not found else "STILL PRESENT"
    else:
        status = "OK" if found else "MISSING"
    print("  " + label + ": " + status)
