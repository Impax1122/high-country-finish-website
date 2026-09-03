#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync ALL nav CSS from homepage to every other page
This ensures every page has the exact same nav styling
"""

import os
import re
from pathlib import Path

# Complete nav CSS from homepage (lines 187-363 approximately)
COMPLETE_NAV_CSS = """
/* ─── NAV ──────────────────────────────────── */
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 24px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background .3s, padding .3s, border-color .3s;
  border-bottom: 1px solid transparent;
}

nav.scrolled {
  background: rgba(12,12,12,.97);
  backdrop-filter: blur(12px);
  padding: 16px 40px;
  border-color: var(--border);
}

.nav-logo {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.nav-logo .logo-main {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.5px;
}

.nav-logo .logo-sub {
  font-size: 9px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
  margin-top: 3px;
}

.nav-links {
  display: flex;
  gap: 36px;
  list-style: none;
  align-items: center;
}

.nav-links a {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: .5px;
  color: #aaa;
  transition: color .2s;
}

.nav-links a:hover { color: var(--text); }

/* Dropdown menu */
.nav-item {
  position: relative;
}

.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 20px;
  background: rgba(20, 20, 20, 0.98);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 0;
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  z-index: 2000;
}

.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.nav-dropdown a {
  display: block;
  padding: 10px 24px;
  font-size: 13px;
  color: var(--muted);
  transition: all 0.2s;
}

.nav-dropdown a:hover {
  background: var(--surface2);
  color: var(--text);
  padding-left: 28px;
}

.nav-cta {
  background: var(--gold);
  color: #000 !important;
  padding: 10px 22px;
  border-radius: 2px;
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background .2s !important;
}

.nav-cta:hover { background: var(--gold-light) !important; }

.nav-toggle { display: none; flex-direction: column; gap: 5px; cursor: pointer; padding: 4px; }
.nav-toggle span { width: 24px; height: 1.5px; background: var(--text); transition: all .3s; }

@media(max-width:900px){
  nav{padding:20px 24px;}
  nav.scrolled{padding:14px 24px;}
  .nav-links{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(12,12,12,.98);
    flex-direction:column;justify-content:center;gap:32px;z-index:10001;overflow-y:auto;}
  .nav-links.open{display:flex;}
  .nav-item.open .nav-dropdown {
    display: block;
  }
  body.nav-open{overflow:hidden;position:fixed;width:100%;}
  .nav-links a{font-size:18px!important;}
  .nav-toggle{display:flex;z-index:1000;}
  /* Hamburger → X animation */
  .nav-toggle.is-open span:nth-child(1){transform:translateY(6.5px) rotate(45deg);}
  .nav-toggle.is-open span:nth-child(2){opacity:0;}
  .nav-toggle.is-open span:nth-child(3){transform:translateY(-6.5px) rotate(-45deg);}
}
"""


def update_nav_css(filepath):
    """Replace ALL nav CSS in a file with homepage version"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and remove existing nav CSS section
    # Pattern: from /* ─── NAV to the next major section marker
    nav_css_patterns = [
        (r'/\* ─── NAV.*?(?=/\* ─── [A-Z])', ''),  # Until next major section
        (r'nav \{.*?@media\(max-width:900px\)\{.*?\}.*?\}', ''),  # Catch-all nav section
    ]
    
    # Try to find where nav CSS should be (after GOLD LINE or LAYOUT section)
    insertion_markers = [
        '/* ─── GOLD LINE',
        '/* ─── LAYOUT',
    ]
    
    # Remove old nav CSS
    for pattern, _ in nav_css_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Find insertion point (after gold-line section)
    gold_line_end = content.find('.gold-line {')
    if gold_line_end != -1:
        # Find the closing brace of gold-line
        closing_brace = content.find('}', gold_line_end)
        if closing_brace != -1:
            # Insert nav CSS after gold-line section
            before = content[:closing_brace + 1]
            after = content[closing_brace + 1:]
            content = before + '\n' + COMPLETE_NAV_CSS + '\n' + after
    else:
        # Fallback: insert before </style>
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + COMPLETE_NAV_CSS + '\n' + content[style_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Synced nav CSS: {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    files_to_update = []
    
    # Skip index.html (it's the source)
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
        update_nav_css(filepath)
    
    print(f"\nSynced complete nav CSS to {len(files_to_update)} pages")
    print("All pages now have:")
    print("- Correct logo styles")
    print("- Dropdown menu styles")
    print("- GET A QUOTE button styles")
    print("- Mobile nav styles")
    print("- Hamburger menu animation")


if __name__ == "__main__":
    main()
