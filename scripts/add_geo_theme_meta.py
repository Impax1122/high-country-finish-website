#!/usr/bin/env python3
"""
Add Geo & Theme Meta Tags
Adds geographic and theme-related meta tags to all HTML pages
"""

import os
import glob
from pathlib import Path

GEO_THEME_META = '''    <meta name="geo.region" content="US-CO">
    <meta name="geo.placename" content="Denver">
    <meta name="theme-color" content="#0c0c0c">
    <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
'''

def add_geo_theme_meta(filepath):
    """Add geo and theme meta tags to HTML file."""
    try:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if geo meta already exists
        if 'name="geo.region"' in content:
            print(f"[SKIP] {filename}: Geo/theme meta already present")
            return 0
        
        # Find the </head> tag
        head_end = content.find('</head>')
        if head_end == -1:
            print(f"[ERROR] {filename}: No </head> tag found")
            return -1
        
        # Insert before </head>
        new_content = content[:head_end] + GEO_THEME_META + '  ' + content[head_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 1
        
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return -1

def main():
    """Process all HTML files."""
    base_dir = Path(__file__).parent
    
    html_files = []
    html_files.extend(glob.glob(str(base_dir / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "blog" / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "services" / "*.html")))
    
    print(f"GEO & THEME META TAG INSERTION")
    print(f"Found {len(html_files)} HTML files\n")
    
    files_modified = 0
    files_skipped = 0
    errors = 0
    
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        result = add_geo_theme_meta(filepath)
        
        if result > 0:
            print(f"[OK] {filename}: Geo/theme meta added")
            files_modified += 1
        elif result == 0:
            files_skipped += 1
        else:
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Files skipped: {files_skipped}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")
    
    return errors == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
