#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dropdown navigation to all pages + update footer headings to be links
"""

import os
import re
from pathlib import Path

# New nav HTML with dropdowns
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
    <div class="nav-item">
      <a href="/about-us.html">Company</a>
      <div class="nav-dropdown">
        <a href="/about-us.html">About Us</a>
        <a href="/our-process.html">Our Process</a>
        <a href="/service-area.html">Service Area</a>
      </div>
    </div>
    <a href="/blog.html">Blog</a>
    <a href="/get-a-quote.html">Get a Quote</a>
  </div>"""

# Dropdown CSS to inject
DROPDOWN_CSS = """
/* ─── NAV WITH DROPDOWN ───────────────────── */
.nav-item {
  position: relative;
}
.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 16px 0;
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.nav-dropdown a {
  display: block;
  padding: 10px 20px;
  font-size: 14px;
  color: var(--muted);
  transition: all 0.2s;
}
.nav-dropdown a:hover {
  background: var(--surface2);
  color: var(--text);
  padding-left: 24px;
}
"""

# Mobile dropdown CSS
MOBILE_DROPDOWN_CSS = """
  .nav-dropdown {
    position: static;
    margin-top: 8px;
    opacity: 1;
    visibility: visible;
    transform: none;
    box-shadow: none;
    border: none;
    padding-left: 16px;
    display: none;
  }
  .nav-item.open .nav-dropdown {
    display: block;
  }
"""

# Mobile dropdown JS
MOBILE_DROPDOWN_JS = """
// Mobile dropdown toggles
if (window.innerWidth <= 768) {
  document.querySelectorAll('.nav-item > a').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      e.target.parentElement.classList.toggle('open');
    });
  });
}
"""

# Update footer headings to be links
NEW_FOOTER_HTML = """    <div class="footer-grid">
      <div class="footer-col">
        <h4><a href="/services.html">Services</a></h4>
        <a href="/services/vehicle-wraps.html">Vehicle Wraps</a>
        <a href="/services/spot-graphics.html">Spot Graphics</a>
        <a href="/services/window-tint.html">Window Tint</a>
        <a href="/services/window-frosting.html">Window Frosting</a>
        <a href="/services/wall-graphics.html">Wall Graphics</a>
        <a href="/services/lobby-signs.html">Lobby Signs</a>
        <a href="/services/building-signs.html">Building Signs</a>
        <a href="/services/custom-work.html">Custom Work</a>
      </div>
      <div class="footer-col">
        <h4><a href="/about-us.html">Company</a></h4>
        <a href="/about-us.html">About Us</a>
        <a href="/portfolio.html">Portfolio</a>
        <a href="/our-process.html">Our Process</a>
        <a href="/service-area.html">Service Area</a>
        <a href="/blog.html">Blog</a>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <a href="tel:3038824656">303-882-4656</a>
        <a href="mailto:highcountryfinishandrepairco@gmail.com">highcountryfinishandrepairco@gmail.com</a>
        <p style="margin-top:12px;font-size:14px;color:var(--muted);">Denver, CO & surrounding areas</p>
      </div>
    </div>"""

# Footer H4 link CSS
FOOTER_H4_CSS = """
.footer-col h4 a {
  color: var(--gold);
  transition: color 0.2s;
}
.footer-col h4 a:hover {
  color: var(--gold-light);
}
"""


def update_file(filepath):
    """Update a single HTML file with dropdown nav"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace nav links
    nav_pattern = r'<div class="nav-links"[^>]*>.*?</div>\s*<div class="mobile-toggle"'
    replacement = NEW_NAV_HTML + '\n  <div class="mobile-toggle"'
    content = re.sub(nav_pattern, replacement, content, flags=re.DOTALL)
    
    # Add dropdown CSS after /* ─── NAV ─────────────────────────────────── */
    if 'nav-dropdown' not in content:
        nav_css_marker = '/* ─── NAV ─────────────────────────────────── */'
        if nav_css_marker in content:
            content = content.replace(nav_css_marker, nav_css_marker + '\n' + DROPDOWN_CSS)
    
    # Add mobile dropdown CSS in mobile section
    if '.nav-item.open .nav-dropdown' not in content:
        mobile_marker = '  .nav-links.open { transform: translateX(0); }'
        if mobile_marker in content:
            content = content.replace(mobile_marker, mobile_marker + '\n' + MOBILE_DROPDOWN_CSS)
    
    # Add mobile dropdown JS
    if 'Mobile dropdown toggles' not in content:
        js_marker = '  });'
        # Find the last occurrence (end of mobile menu close script)
        last_idx = content.rfind(js_marker)
        if last_idx != -1:
            insert_pos = last_idx + len(js_marker)
            content = content[:insert_pos] + '\n\n' + MOBILE_DROPDOWN_JS + content[insert_pos:]
    
    # Update footer
    footer_pattern = r'<div class="footer-grid">.*?</div>\s*<div class="footer-bottom"'
    content = re.sub(footer_pattern, NEW_FOOTER_HTML + '\n    <div class="footer-bottom"', content, flags=re.DOTALL)
    
    # Add footer h4 link CSS
    if '.footer-col h4 a' not in content:
        footer_css_marker = '.footer-col h4 {'
        if footer_css_marker in content:
            content = content.replace(footer_css_marker, FOOTER_H4_CSS + '\n' + footer_css_marker)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Update all HTML files in root
    for file in base_path.glob("*.html"):
        if file.name not in ['services.html']:  # Skip services.html, it already has dropdown
            update_file(file)
    
    # Update all service pages
    services_path = base_path / "services"
    for file in services_path.glob("*.html"):
        update_file(file)
    
    # Update all blog pages
    blog_path = base_path / "blog"
    for file in blog_path.glob("*.html"):
        update_file(file)
    
    print("\nAll pages updated with dropdown navigation")


if __name__ == "__main__":
    main()
