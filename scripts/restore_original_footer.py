#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore original footer structure from first build
Match BRAND.md exactly
"""

import os
import re
from pathlib import Path

# Original footer HTML (from commit 9fb0082)
ORIGINAL_FOOTER_HTML = """<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo-main">High Country</div>
        <div class="logo-sub">Finish & Repair CO</div>
        <p>Denver's premier vinyl wrap, sign, and window tint specialists. Precision installs, every time.</p>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="/services/vehicle-wraps.html">Vehicle Wraps</a></li>
          <li><a href="/services/spot-graphics.html">Spot Graphics</a></li>
          <li><a href="/services/window-tint.html">Window Tint</a></li>
          <li><a href="/services/window-frosting.html">Window Frosting</a></li>
          <li><a href="/services/wall-graphics.html">Wall Graphics</a></li>
          <li><a href="/services/lobby-signs.html">Lobby Signs</a></li>
          <li><a href="/services/building-signs.html">Building Signs</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about-us.html">About Us</a></li>
          <li><a href="/portfolio.html">Portfolio</a></li>
          <li><a href="/our-process.html">Our Process</a></li>
          <li><a href="/service-area.html">Service Area</a></li>
          <li><a href="/get-a-quote.html">Get a Quote</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:3038824656">303-882-4656</a></li>
          <li><a href="mailto:highcountryfinishandrepairco@gmail.com" style="word-break:break-word;font-size:12px">highcountryfinishandrepairco<br/>@gmail.com</a></li>
          <li style="margin-top:8px">Denver, CO & Surrounding Areas</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 High Country Finish and Repair CO. All rights reserved.</p>
      <p>Denver, CO &middot; 303-882-4656</p>
    </div>
  </div>
</footer>"""

# Original footer CSS (from commit 9fb0082)
ORIGINAL_FOOTER_CSS = """
/* ─── FOOTER ──────────────────────────────── */
footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 60px 0 32px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-brand .logo-main { font-family: 'Cormorant Garamond', serif; font-size: 22px; font-weight: 600; margin-bottom: 4px; }
.footer-brand .logo-sub  { font-size: 9px; text-transform: uppercase; letter-spacing: 3px; color: var(--gold); }
.footer-brand p { font-size: 13px; color: var(--muted); margin-top: 16px; max-width: 260px; line-height: 1.7; }

.footer-col h4 { font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); margin-bottom: 16px; }
.footer-col ul { list-style: none; }
.footer-col ul li { font-size: 13px; color: var(--muted); padding: 5px 0; }
.footer-col ul li a:hover { color: var(--gold); }

.footer-bottom { border-top: 1px solid var(--border); padding-top: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.footer-bottom p { font-size: 12px; color: var(--muted); }

@media(max-width:900px){
  .footer-grid{grid-template-columns:1fr 1fr;gap:36px;}
}

@media(max-width:600px){
  .footer-grid{grid-template-columns:1fr;}
}
"""


def restore_footer(filepath):
    """Replace footer HTML and CSS in a file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace footer HTML
    footer_pattern = r'<footer>.*?</footer>'
    content = re.sub(footer_pattern, ORIGINAL_FOOTER_HTML, content, flags=re.DOTALL)
    
    # Replace footer CSS
    # Find existing footer CSS and replace it
    footer_css_pattern = r'/\* ─── FOOTER ──────────────────────────────── \*/.*?(?=/\* ─── |@media\(max-width:768px\)|</style>)'
    
    # Check if footer CSS exists
    if '/* ─── FOOTER' in content:
        content = re.sub(footer_css_pattern, ORIGINAL_FOOTER_CSS + '\n', content, flags=re.DOTALL)
    else:
        # Add footer CSS before </style>
        style_end = content.rfind('</style>')
        if style_end != -1:
            content = content[:style_end] + ORIGINAL_FOOTER_CSS + '\n' + content[style_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Restored original footer in {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Update all pages
    files_to_update = []
    
    # Root pages
    for file in base_path.glob("*.html"):
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
        restore_footer(filepath)
    
    print(f"\nRestored original footer across {len(files_to_update)} pages")


if __name__ == "__main__":
    main()
