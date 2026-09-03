#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standardize nav across ALL pages - same dropdown structure everywhere
"""

import os
import re
from pathlib import Path

# Standard nav HTML (same for all pages)
def get_nav_html(active_page=""):
    """Generate nav HTML with proper active state"""
    
    home_active = ' class="active"' if active_page == "home" else ""
    services_active = ' class="active"' if active_page == "services" else ""
    portfolio_active = ' class="active"' if active_page == "portfolio" else ""
    process_active = ' class="active"' if active_page == "process" else ""
    about_active = ' class="active"' if active_page == "about" else ""
    
    return f"""  <div class="nav-links" id="nav-links">
    <a onclick="closeNav()" href="/"{ home_active }>Home</a>
    <div class="nav-item">
      <a onclick="closeNav()" href="/services.html"{ services_active }>Services</a>
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
    <a onclick="closeNav()" href="/portfolio.html"{ portfolio_active }>Portfolio</a>
    <a onclick="closeNav()" href="/our-process.html"{ process_active }>Process</a>
    <a onclick="closeNav()" href="/about-us.html"{ about_active }>About</a>
    <a onclick="closeNav()" href="/get-a-quote.html" class="nav-cta">Get a Quote</a>
  </div>"""


def update_nav(filepath, active_page=""):
    """Replace nav in a file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find nav-links div
    pattern = r'<div class="nav-links"[^>]*>.*?</div>\s*<div class="mobile-toggle"'
    
    replacement = get_nav_html(active_page) + '\n  <div class="mobile-toggle"'
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Core pages
    update_nav(base_path / "index.html", "home")
    update_nav(base_path / "portfolio.html", "portfolio")
    update_nav(base_path / "about-us.html", "about")
    update_nav(base_path / "our-process.html", "process")
    update_nav(base_path / "service-area.html")
    update_nav(base_path / "get-a-quote.html")
    update_nav(base_path / "services.html", "services")
    update_nav(base_path / "blog.html")
    
    # All service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in services_path.glob("*.html"):
            update_nav(file, "services")
    
    # All blog pages
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in blog_path.glob("*.html"):
            update_nav(file)
    
    print("\nAll pages now have standardized nav with dropdown")


if __name__ == "__main__":
    main()
