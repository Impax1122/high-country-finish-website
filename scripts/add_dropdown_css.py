#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add dropdown CSS to make Services menu appear on hover
"""

import os
from pathlib import Path

# Dropdown CSS to insert after .nav-links a:hover
DROPDOWN_CSS = """
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
"""

def add_dropdown_css(filepath):
    """Add dropdown CSS after .nav-links a:hover"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has dropdown CSS
    if '.nav-dropdown' in content:
        print(f"Skipping {os.path.basename(filepath)} - already has dropdown CSS")
        return
    
    # Find .nav-links a:hover and insert dropdown CSS after it
    marker = '.nav-links a:hover { color: var(--text); }'
    
    if marker in content:
        content = content.replace(marker, marker + '\n' + DROPDOWN_CSS)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"WARNING: Could not find nav-links a:hover in {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Update all HTML files
    for file in base_path.glob("*.html"):
        add_dropdown_css(file)
    
    # Update all service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in services_path.glob("*.html"):
            add_dropdown_css(file)
    
    # Update all blog pages
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in blog_path.glob("*.html"):
            add_dropdown_css(file)
    
    print("\nDropdown CSS added to all pages")


if __name__ == "__main__":
    main()
