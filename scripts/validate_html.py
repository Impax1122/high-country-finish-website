import os
import re

def check_html_file(filepath):
    """Basic HTML validation - check for common issues"""
    errors = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for unclosed tags (basic check)
    open_tags = re.findall(r'<(div|section|article|header|footer|nav|main|aside|ul|ol|form)[^>]*>', content)
    close_tags = re.findall(r'</(div|section|article|header|footer|nav|main|aside|ul|ol|form)>', content)
    
    if len(open_tags) != len(close_tags):
        errors.append(f"Possible unclosed tags: {len(open_tags)} open vs {len(close_tags)} close")
    
    # Check for required head elements
    if '<meta charset=' not in content and '<meta charset="' not in content:
        errors.append("Missing charset meta tag")
    
    if '<title>' not in content:
        errors.append("Missing title tag")
    
    if 'name="description"' not in content:
        errors.append("Missing meta description")
    
    if 'rel="canonical"' not in content:
        errors.append("Missing canonical link")
    
    # Check for broken image references (basic)
    img_tags = re.findall(r'<img[^>]+src="([^"]+)"', content)
    for img_src in img_tags:
        if img_src.startswith('http'):
            continue  # Skip external images
        # Check if local file exists (basic check for images/)
        if img_src.startswith('/images/'):
            img_path = img_src[1:]  # Remove leading /
        elif img_src.startswith('images/'):
            img_path = img_src
        else:
            continue
        
        if not os.path.exists(img_path):
            errors.append(f"Image not found: {img_src}")
    
    return errors

# Check main HTML files
html_files = [
    'index.html',
    'about-us.html',
    'portfolio.html',
    'services.html',
    'service-area.html',
    'our-process.html',
    'get-a-quote.html',
    'blog.html'
]

print("[VALIDATION REPORT]\n")

all_good = True
for filename in html_files:
    if not os.path.exists(filename):
        print(f"[SKIP] {filename} - not found")
        continue
    
    errors = check_html_file(filename)
    if errors:
        print(f"[WARN] {filename}:")
        for err in errors:
            print(f"  - {err}")
        all_good = False
    else:
        print(f"[OK] {filename}")

print("\n" + "="*50)
if all_good:
    print("[RESULT] All files passed basic validation!")
else:
    print("[RESULT] Some warnings found (see above)")
