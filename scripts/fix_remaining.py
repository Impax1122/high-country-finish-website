import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', encoding='utf-8') as f:
    c = f.read()

# Fix the mangled placeholder
old_ph = 'placeholder="Tell us about your project &rdquo;\u201d vehicle type, dimensions, timeline, any specific requirements..."'
new_ph = 'placeholder="Tell us about your project &mdash; vehicle type, dimensions, timeline, any specific requirements..."'
if old_ph in c:
    c = c.replace(old_ph, new_ph)
    print("Fixed placeholder em dash (v1)")

# Try alternate form
old_ph2 = '&rdquo;" vehicle type'
new_ph2 = '&mdash; vehicle type'
if old_ph2 in c:
    c = c.replace(old_ph2, new_ph2)
    print("Fixed placeholder em dash (v2)")

# Find remaining mojibake - scan for multi-byte Latin-1 sequences
# Right arrow: U+2192 = E2 86 92 -> in latin1 = chr(0xe2)+chr(0x86)+chr(0x92)
arrow_bad = '\xe2\x86\x92'  # these are the actual chars if file was double-encoded
if arrow_bad in c:
    c = c.replace(arrow_bad, '&rarr;')
    print("Fixed arrow (byte method)")

# Also try the string pattern
for bad, good, name in [
    ('\u00e2\u0080\x93', '&ndash;', 'en dash'),
    ('\u00e2\u0080\x94', '&mdash;', 'em dash'),
    ('\u00e2\u0086\x92', '&rarr;',  'right arrow'),
    ('\u00e2\u0086\x90', '&larr;',  'left arrow'),
]:
    if bad in c:
        count = c.count(bad)
        c = c.replace(bad, good)
        print(f"Fixed {count}x {name}")

# Report any remaining â-prefixed sequences
remaining = set(re.findall(r'\xe2[^\s<"]{0,3}', c))
if remaining:
    print(f"Still remaining: {[repr(r) for r in remaining]}")
else:
    print("No remaining mojibake found")

# Verify textarea
idx = c.find('textarea')
while idx != -1:
    snippet = c[idx:idx+200]
    if 'placeholder' in snippet:
        print("Textarea now:", repr(snippet[:150]))
        break
    idx = c.find('textarea', idx+1)

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved.")
