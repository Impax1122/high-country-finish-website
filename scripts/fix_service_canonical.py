import os
import re

# Service page list with correct canonical URLs
service_pages = {
    'vehicle-wraps.html': 'https://highcountryfinish.com/services/vehicle-wraps.html',
    'window-tint.html': 'https://highcountryfinish.com/services/window-tint.html',
    'window-frosting.html': 'https://highcountryfinish.com/services/window-frosting.html',
    'wall-graphics.html': 'https://highcountryfinish.com/services/wall-graphics.html',
    'lobby-signs.html': 'https://highcountryfinish.com/services/lobby-signs.html',
    'building-signs.html': 'https://highcountryfinish.com/services/building-signs.html',
    'spot-graphics.html': 'https://highcountryfinish.com/services/spot-graphics.html',
    'custom-work.html': 'https://highcountryfinish.com/services/custom-work.html',
}

services_dir = 'services'

for filename, correct_url in service_pages.items():
    filepath = os.path.join(services_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️  Skipping {filename} (not found)")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix canonical tag
    content = re.sub(
        r'<link rel="canonical" href="https://highcountryfinish\.com/"\s*/?>',
        f'<link rel="canonical" href="{correct_url}"/>',
        content
    )
    
    # Fix og:url
    content = re.sub(
        r'<meta property="og:url" content="https://highcountryfinish\.com/"\s*/?>',
        f'<meta property="og:url" content="{correct_url}"/>',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Fixed {filename}")

print("\n[OK] All service page canonical tags updated!")
