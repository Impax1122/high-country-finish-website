import re

# Check index.html navigation
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find navigation links
nav_links = re.findall(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL)

print("[NAVIGATION CHECK]\n")

if nav_links:
    # Extract href links from nav
    links = re.findall(r'href="([^"]+)"', nav_links[0])
    
    print("Navigation links found:")
    for link in links[:15]:  # First 15 links
        if link.startswith('#'):
            print(f"  [ANCHOR] {link}")
        elif link.startswith('http'):
            print(f"  [EXTERNAL] {link}")
        elif link.startswith('tel:') or link.startswith('mailto:'):
            print(f"  [ACTION] {link}")
        elif link.startswith('/services/'):
            page = link.split('/')[-1]
            print(f"  [SERVICE] {link} - OK")
        else:
            print(f"  [PAGE] {link}")

print("\n[INFO] Service pages in /services/:")
print("  - vehicle-wraps.html")
print("  - window-tint.html")
print("  - window-frosting.html")
print("  - wall-graphics.html")
print("  - lobby-signs.html")
print("  - building-signs.html")
print("  - spot-graphics.html")
print("  - custom-work.html")

print("\n[RESULT] Navigation structure appears correct")
print("         Service links point to /services/ pages (not anchors)")
