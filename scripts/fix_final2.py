import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', encoding='utf-8') as f:
    c = f.read()

before = len(c)

# Right arrow: â (U+00E2) + dagger (U+2020) + rsquo (U+2019) = mojibake for U+2192 →
arrow = '\u00e2\u2020\u2019'
if arrow in c:
    c = c.replace(arrow, '&rarr;')
    print("Fixed: right arrow")

# Checkmark: â (U+00E2) + oe (U+0153) + rdquo (U+201D) = mojibake for U+2713 ✓
check = '\u00e2\u0153\u201d'
if check in c:
    c = c.replace(check, '&#10003;')
    print("Fixed: checkmark")

# Catch any leftover lone â that precedes a space or tag (just strip it)
import re
remaining = re.findall(r'\u00e2[\u0080-\u00ff\u2000-\u27ff]{0,2}', c)
if remaining:
    seen = set()
    for r in remaining:
        if r not in seen:
            seen.add(r)
            idx = c.find(r)
            print(f"Still remaining: {repr(r)} at context: {repr(c[max(0,idx-30):idx+30])}")

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved.")
