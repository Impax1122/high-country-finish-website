from pathlib import Path
c = Path(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html').read_text(encoding='utf-8')

# Find H1 tag in body
idx = c.find('<h1 class')
print("H1 TAG:")
print(repr(c[idx:idx+300]))

print("\n---OG title---")
idx2 = c.find('og:title')
print(repr(c[idx2:idx2+150]))

print("\n---meta desc---")
idx3 = c.find('name="description"')
print(repr(c[idx3:idx3+250]))
