#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make all page navs match homepage exactly:
- Correct logo (High Country + subtitle)
- GET A QUOTE as gold button
"""

import os
import re
from pathlib import Path

# Correct nav HTML from homepage
CORRECT_NAV_HTML = """<nav id="nav">
  <a href="/" class="nav-logo">
    <span class="logo-main">High Country</span>
    <span class="logo-sub">Finish & Repair CO</span>
  </a>
  <div class="nav-links" id="nav-links">
    <a onclick="closeNav()" href="/">Home</a>
    <div class="nav-item">
      <a onclick="closeNav()" href="/services.html">Services</a>
      <div class="nav-dropdown">
        <a onclick="closeNav()" href="/services/vehicle-wraps.html">Vehicle Wraps</a>
        <a onclick="closeNav()" href="/services/spot-graphics.html">Spot Graphics</a>
        <a onclick="closeNav()" href="/services/window-tint.html">Window Tint</a>
        <a onclick="closeNav()" href="/services/window-frosting.html">Window Frosting</a>
        <a onclick="closeNav()" href="/services/wall-graphics.html">Wall Graphics</a>
        <a onclick="closeNav()" href="/services/lobby-signs.html">Lobby Signs</a>
        <a onclick="closeNav()" href="/services/building-signs.html">Building Signs</a>
        <a onclick="closeNav()" href="/services/custom-work.html">Custom Work</a>
      </div>
    </div>
    <a onclick="closeNav()" href="/portfolio.html">Portfolio</a>
    <a onclick="closeNav()" href="/our-process.html">Process</a>
    <a onclick="closeNav()" href="/about-us.html">About</a>
    <a onclick="closeNav()" href="/get-a-quote.html" class="nav-cta">Get a Quote</a>
  </div>
  <div class="nav-toggle" id="nav-toggle" onclick="toggleNav()">
    <span></span><span></span><span></span>
  </div>
</nav>"""


def update_nav(filepath):
    """Replace nav in a file to match homepage"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace <nav>...</nav>
    nav_pattern = r'<nav[^>]*>.*?</nav>'
    
    content = re.sub(nav_pattern, CORRECT_NAV_HTML, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated nav: {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    files_to_update = []
    
    # Skip index.html (it's already correct)
    for file in base_path.glob("*.html"):
        if file.name != "index.html":
            files_to_update.append(file)
    
    # Service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in services_path.glob("*.html"):
            files_to_update.append(file)
    
    # Blog pages
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in blog_path.glob("*.html"):
            files_to_update.append(file)
    
    for filepath in files_to_update:
        update_nav(filepath)
    
    print(f"\nUpdated {len(files_to_update)} pages to match homepage nav")
    print("- Correct logo: 'High Country' + 'Finish & Repair CO' subtitle")
    print("- Services dropdown with all 8 services")
    print("- GET A QUOTE styled as gold button")


if __name__ == "__main__":
    main()
