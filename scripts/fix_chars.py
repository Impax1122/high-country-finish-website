import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', encoding='utf-8') as f:
    c = f.read()

fixes = {
    'â€"':  '&mdash;',
    'â€"':  '&ndash;',
    'Â©':   '&copy;',
    'Â·':   '&middot;',
    'â€™':  '&rsquo;',
    'â€˜':  '&lsquo;',
    'â€':   '&rdquo;',
    'â€œ':  '&ldquo;',
    'â€¦':  '&hellip;',
    'Â ':   '&nbsp;',
    'Â®':   '&reg;',
    'â„¢':  '&trade;',
    'â€¢':  '&bull;',
    'Â':    '',
}

total = 0
for bad, good in fixes.items():
    count = c.count(bad)
    if count:
        c = c.replace(bad, good)
        print(f"Fixed {count}x {repr(bad)[:20]} -> {good}")
        total += count

print(f"Total fixes: {total}")

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved.")
