#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix portfolio.html nav structure
"""

from pathlib import Path

portfolio_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/portfolio.html")

with open(portfolio_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Old nav structure
old_nav = """  <ul class="nav-links" id="nav-links">
    <li><a onclick="closeNav()" href="index.html#services">Services</a></li>
    <li><a onclick="closeNav()" href="portfolio.html" class="active">Portfolio</a></li>
    <li><a onclick="closeNav()" href="index.html#process">Process</a></li>
    <li><a onclick="closeNav()" href="index.html#about">About</a></li>
    <li><a onclick="closeNav()" href="index.html#contact" class="nav-cta">Get a Quote</a></li>
  </ul>"""

# New nav structure with dropdown
new_nav = """  <div class="nav-links" id="nav-links">
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
    <a onclick="closeNav()" href="/portfolio.html" class="active">Portfolio</a>
    <a onclick="closeNav()" href="/our-process.html">Process</a>
    <a onclick="closeNav()" href="/about-us.html">About</a>
    <a onclick="closeNav()" href="/get-a-quote.html" class="nav-cta">Get a Quote</a>
  </div>"""

# Replace
content = content.replace(old_nav, new_nav)

# Add mobile dropdown CSS if not present
mobile_dropdown = """
  .nav-item.open .nav-dropdown {
    display: block;
  }
"""

if '.nav-item.open .nav-dropdown' not in content:
    marker = '.nav-links.open{display:flex;}'
    if marker in content:
        content = content.replace(marker, marker + mobile_dropdown)

# Write back
with open(portfolio_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed portfolio.html nav structure with dropdown")
