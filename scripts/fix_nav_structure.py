#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix nav: Services dropdown only, all other links standalone
"""

import os
import re
from pathlib import Path

# Simple nav HTML - Services dropdown only
NEW_NAV_HTML = """  <div class="nav-links" id="navLinks">
    <a href="/">Home</a>
    <div class="nav-item">
      <a href="/services.html">Services</a>
      <div class="nav-dropdown">
        <a href="/services/vehicle-wraps.html">Vehicle Wraps</a>
        <a href="/services/spot-graphics.html">Spot Graphics</a>
        <a href="/services/window-tint.html">Window Tint</a>
        <a href="/services/window-frosting.html">Window Frosting</a>
        <a href="/services/wall-graphics.html">Wall Graphics</a>
        <a href="/services/lobby-signs.html">Lobby Signs</a>
        <a href="/services/building-signs.html">Building Signs</a>
        <a href="/services/custom-work.html">Custom Work</a>
      </div>
    </div>
    <a href="/portfolio.html">Portfolio</a>
    <a href="/our-process.html">Process</a>
    <a href="/about-us.html">About</a>
    <a href="/get-a-quote.html">Get a Quote</a>
  </div>"""


def update_file(filepath):
    """Update nav in a single file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace nav links
    nav_pattern = r'<div class="nav-links"[^>]*>.*?</div>\s*<div class="mobile-toggle"'
    replacement = NEW_NAV_HTML + '\n  <div class="mobile-toggle"'
    content = re.sub(nav_pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Update all HTML files
    for file in base_path.glob("*.html"):
        update_file(file)
    
    # Update all service pages
    services_path = base_path / "services"
    for file in services_path.glob("*.html"):
        update_file(file)
    
    # Update all blog pages
    blog_path = base_path / "blog"
    for file in blog_path.glob("*.html"):
        update_file(file)
    
    print("\nNav fixed: Services dropdown only, other links standalone")


if __name__ == "__main__":
    main()
