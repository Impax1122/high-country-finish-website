#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add logo image to navigation on all pages
Replace text logo with actual logo.png
"""

import os
import re
from pathlib import Path

def add_logo_to_page(filepath):
    """Replace text logo with image logo"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Old text logo HTML
    old_logo_pattern = r'<a href="/" class="nav-logo">\s*<span class="logo-main">High Country</span>\s*<span class="logo-sub">Finish & Repair CO</span>\s*</a>'
    
    # New image logo HTML
    new_logo = '''<a href="/" class="nav-logo">
    <img src="/images/logo.png" alt="High Country Finish & Repair CO" class="nav-logo-img"/>
  </a>'''
    
    if re.search(old_logo_pattern, content, re.DOTALL):
        content = re.sub(old_logo_pattern, new_logo, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added logo to: {os.path.basename(filepath)}")
        return True
    else:
        print(f"Skipped (already has logo or different structure): {os.path.basename(filepath)}")
        return False


def add_logo_css(filepath):
    """Add CSS for logo image"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if logo CSS already exists
    if '.nav-logo-img' in content:
        return False
    
    # Logo CSS
    logo_css = """
.nav-logo-img {
  height: 40px;
  width: auto;
  display: block;
  transition: opacity 0.2s;
}

.nav-logo-img:hover {
  opacity: 0.8;
}

@media(max-width:900px) {
  .nav-logo-img {
    height: 32px;
  }
}
"""
    
    # Add after .nav-logo styling
    nav_logo_marker = '.nav-logo .logo-sub'
    if nav_logo_marker in content:
        # Find the closing brace after logo-sub
        idx = content.find('}', content.find(nav_logo_marker))
        if idx != -1:
            content = content[:idx+1] + '\n' + logo_css + content[idx+1:]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    
    return False


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    print("=" * 60)
    print("ADDING LOGO TO ALL PAGES")
    print("=" * 60)
    
    html_updated = 0
    css_updated = 0
    
    all_files = []
    
    # Root pages
    print("\nROOT PAGES:")
    for file in sorted(base_path.glob("*.html")):
        all_files.append(file)
    
    # Service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in sorted(services_path.glob("*.html")):
            all_files.append(file)
    
    # Blog pages
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in sorted(blog_path.glob("*.html")):
            all_files.append(file)
    
    # Update all files
    for filepath in all_files:
        if add_logo_to_page(filepath):
            html_updated += 1
        if add_logo_css(filepath):
            css_updated += 1
    
    print("\n" + "=" * 60)
    print(f"HTML UPDATED: {html_updated} pages")
    print(f"CSS UPDATED: {css_updated} pages")
    print("=" * 60)
    print("\nLogo now appears:")
    print("  - In navigation on all pages")
    print("  - At /images/logo.png")
    print("  - 40px height on desktop, 32px on mobile")
    print("  - Hover effect (slight fade)")


if __name__ == "__main__":
    main()
