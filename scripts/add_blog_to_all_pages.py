#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Blog to navigation and footer on all pages
Per brand guidelines
"""

import os
import re
from pathlib import Path

def add_blog_to_page(filepath):
    """Add Blog to nav and footer"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changed = False
    
    # 1. Add Blog to navigation (before Get a Quote)
    # Pattern: </a> before <a...Get a Quote
    nav_pattern = r'(</div>\s*<a onclick="closeNav\(\)" href="/portfolio\.html">Portfolio</a>\s*<a onclick="closeNav\(\)" href="/our-process\.html">Process</a>\s*<a onclick="closeNav\(\)" href="/about-us\.html">About</a>)\s*(<a onclick="closeNav\(\)" href="/get-a-quote\.html" class="nav-cta">Get a Quote</a>)'
    
    if re.search(nav_pattern, content):
        replacement = r'\1\n    <a onclick="closeNav()" href="/blog.html">Blog</a>\n    \2'
        content = re.sub(nav_pattern, replacement, content)
        changed = True
    
    # 2. Add Blog to footer Company column (after Service Area, before Get a Quote)
    footer_pattern = r'(<li><a href="/service-area\.html">Service Area</a></li>)\s*(<li><a href="/get-a-quote\.html">Get a Quote</a></li>)'
    
    if re.search(footer_pattern, content):
        replacement = r'\1\n          <li><a href="/blog.html">Blog</a></li>\n          \2'
        content = re.sub(footer_pattern, replacement, content)
        changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added Blog to: {os.path.basename(filepath)}")
        return True
    else:
        print(f"Skipped (already has Blog or different structure): {os.path.basename(filepath)}")
        return False


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    print("=" * 60)
    print("ADDING BLOG TO NAVIGATION AND FOOTER")
    print("=" * 60)
    
    updated_count = 0
    
    # Root pages
    print("\nROOT PAGES:")
    for file in sorted(base_path.glob("*.html")):
        if add_blog_to_page(file):
            updated_count += 1
    
    # Service pages
    print("\nSERVICE PAGES:")
    services_path = base_path / "services"
    if services_path.exists():
        for file in sorted(services_path.glob("*.html")):
            if add_blog_to_page(file):
                updated_count += 1
    
    # Blog pages
    print("\nBLOG PAGES:")
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in sorted(blog_path.glob("*.html")):
            if add_blog_to_page(file):
                updated_count += 1
    
    print("\n" + "=" * 60)
    print(f"UPDATED {updated_count} PAGES")
    print("=" * 60)
    print("\nBlog now appears in:")
    print("  - Navigation (between About and Get a Quote)")
    print("  - Footer Company column (after Service Area)")


if __name__ == "__main__":
    main()
