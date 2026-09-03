#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix portfolio footer CSS to match homepage
"""

from pathlib import Path
import re

portfolio_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/portfolio.html")

# Correct footer CSS from homepage (from BRAND.md)
CORRECT_FOOTER_CSS = """
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

# Read portfolio page
with open(portfolio_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove bad footer CSS line
# Look for the line with "footer { padding-bottom: 5rem !important; }"
content = re.sub(r'footer \{ padding-bottom: 5rem !important; \}', '', content)

# Find where footer CSS should be (after GOLD LINE section)
# Look for the pattern before /* ─── NAV
nav_marker = '/* ─── NAV'
nav_idx = content.find(nav_marker)

if nav_idx != -1:
    # Insert footer CSS before NAV section
    before = content[:nav_idx]
    after = content[nav_idx:]
    
    # Remove any existing footer CSS blocks
    before = re.sub(r'/\* ─── FOOTER.*?(?=/\* ─── )', '', before, flags=re.DOTALL)
    
    # Add correct footer CSS
    new_content = before.rstrip() + '\n\n' + CORRECT_FOOTER_CSS + '\n\n' + after
    
    with open(portfolio_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Fixed portfolio footer CSS")
    print("- Removed bad padding-bottom rule")
    print("- Applied correct footer CSS from BRAND.md")
    print("- Footer now matches homepage")
else:
    print("Could not find NAV marker")
