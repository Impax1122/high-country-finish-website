#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add gold button CSS to portfolio page
"""

from pathlib import Path

portfolio_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/portfolio.html")

# Gold button CSS from homepage
BUTTON_CSS = """
/* ─── BUTTONS ─────────────────────────────── */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--gold);
  color: #000;
  padding: 16px 32px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  border-radius: 2px;
  transition: background .2s, transform .2s;
}

.btn-primary:hover { 
  background: var(--gold-light); 
  transform: translateY(-1px); 
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(255,255,255,.2);
  color: var(--text);
  padding: 16px 32px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  border-radius: 2px;
  transition: all .2s;
}

.btn-outline:hover { 
  border-color: var(--gold); 
  color: var(--gold); 
  transform: translateY(-1px); 
}
"""

# Read portfolio
with open(portfolio_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if button CSS already exists
if '.btn-primary' not in content:
    # Add button CSS before footer CSS section
    footer_marker = '/* ─── FOOTER'
    footer_idx = content.find(footer_marker)
    
    if footer_idx != -1:
        before = content[:footer_idx]
        after = content[footer_idx:]
        content = before + BUTTON_CSS + '\n\n' + after
        
        with open(portfolio_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Added gold button CSS to portfolio page")
        print("- .btn-primary (gold button)")
        print("- .btn-outline (outlined button)")
        print("- Hover effects included")
    else:
        print("Could not find footer marker")
else:
    print("Button CSS already exists on portfolio page")
