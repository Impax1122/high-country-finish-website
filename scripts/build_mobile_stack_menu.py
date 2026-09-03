#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build proper mobile stack menu:
- Fixed position, always same place
- Vertically stacked
- Services dropdown expands on tap
- Works across all pages
"""

import os
import re
from pathlib import Path

# Mobile nav CSS - replaces existing mobile section
MOBILE_NAV_CSS = """
@media(max-width:900px){
  nav { padding: 20px 24px; }
  nav.scrolled { padding: 14px 24px; }
  
  /* Mobile menu overlay - fixed, centered stack */
  .nav-links {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100vh;
    background: rgba(12, 12, 12, 0.98);
    backdrop-filter: blur(12px);
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 24px;
    z-index: 10001;
    padding: 100px 40px 80px;
    overflow-y: auto;
  }
  
  .nav-links.open {
    display: flex;
  }
  
  /* Lock body scroll */
  body.nav-open {
    overflow: hidden;
    position: fixed;
    width: 100%;
  }
  
  /* Vertically stacked menu items */
  .nav-links > a,
  .nav-links > .nav-item {
    width: 100%;
    max-width: 320px;
    text-align: center;
  }
  
  .nav-links > a {
    font-size: 22px !important;
    padding: 14px 24px;
    display: block;
    color: var(--text);
  }
  
  /* Services parent link */
  .nav-item > a {
    font-size: 22px !important;
    padding: 14px 24px;
    display: block;
    color: var(--text);
    cursor: pointer;
    position: relative;
  }
  
  /* Arrow indicator for Services */
  .nav-item > a::after {
    content: '▼';
    margin-left: 8px;
    font-size: 12px;
    transition: transform 0.3s;
  }
  
  .nav-item.open > a::after {
    transform: rotate(180deg);
  }
  
  /* Mobile dropdown - stacked below parent */
  .nav-dropdown {
    position: static !important;
    margin-top: 12px;
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
    display: none;
    width: 100%;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }
  
  .nav-item.open .nav-dropdown {
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 500px;
  }
  
  .nav-dropdown a {
    padding: 12px 24px !important;
    font-size: 16px !important;
    color: var(--muted) !important;
    background: rgba(28, 28, 28, 0.5);
    border-radius: 4px;
  }
  
  .nav-dropdown a:hover {
    background: var(--surface2) !important;
    color: var(--text) !important;
  }
  
  /* Gold button on mobile */
  .nav-cta {
    background: var(--gold) !important;
    color: #000 !important;
    padding: 16px 32px !important;
    font-size: 14px !important;
    border-radius: 4px;
    margin-top: 16px;
  }
  
  /* Hamburger toggle */
  .nav-toggle {
    display: flex;
    z-index: 10002;
  }
  
  /* Hamburger → X animation */
  .nav-toggle.is-open span:nth-child(1) {
    transform: translateY(6.5px) rotate(45deg);
  }
  .nav-toggle.is-open span:nth-child(2) {
    opacity: 0;
  }
  .nav-toggle.is-open span:nth-child(3) {
    transform: translateY(-6.5px) rotate(-45deg);
  }
}
"""

# Mobile menu JavaScript
MOBILE_NAV_JS = """
// Mobile menu toggle
function toggleNav() {
  const links = document.getElementById('nav-links');
  const toggle = document.getElementById('nav-toggle');
  const isOpen = links.classList.toggle('open');
  toggle.classList.toggle('is-open', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
}

function closeNav() {
  document.getElementById('nav-links').classList.remove('open');
  document.getElementById('nav-toggle').classList.remove('is-open');
  document.body.classList.remove('nav-open');
}

// Close menu when clicking links (except Services parent)
document.querySelectorAll('.nav-links a').forEach(a => {
  if (!a.parentElement.classList.contains('nav-item')) {
    a.addEventListener('click', closeNav);
  }
});

// Mobile Services dropdown toggle
const servicesItem = document.querySelector('.nav-item');
if (servicesItem && window.innerWidth <= 900) {
  const servicesLink = servicesItem.querySelector('a');
  if (servicesLink) {
    servicesLink.addEventListener('click', (e) => {
      e.preventDefault();
      servicesItem.classList.toggle('open');
    });
  }
  
  // Close menu when clicking dropdown links
  servicesItem.querySelectorAll('.nav-dropdown a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}
"""


def update_page(filepath):
    """Update mobile nav CSS and JS on a page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace mobile CSS section
    # Find @media(max-width:900px){ and replace until closing }
    mobile_css_pattern = r'@media\(max-width:900px\)\{.*?\n\}\n'
    
    if '@media(max-width:900px)' in content:
        content = re.sub(mobile_css_pattern, MOBILE_NAV_CSS + '\n', content, flags=re.DOTALL)
    else:
        # Add before </style> if not present
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + '\n' + MOBILE_NAV_CSS + '\n' + content[style_end:]
    
    # Replace mobile JavaScript
    # Remove old functions and add new ones
    js_patterns = [
        r'// Mobile menu toggle\nfunction toggleNav\(\).*?^\}',
        r'function closeNav\(\).*?^\}',
        r'// Close menu when clicking links.*?\}\);',
        r'// Mobile Services dropdown toggle.*?^\}',
        r'// Mobile dropdown toggle.*?^\}',
    ]
    
    for pattern in js_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Find last </script> before </body> and insert new JS
    # Look for </script> followed by optional whitespace and </body>
    script_marker = r'(</script>)\s*(<!--.*?-->)?\s*(.*?</body>)'
    
    if re.search(script_marker, content, re.DOTALL):
        content = re.sub(
            script_marker,
            MOBILE_NAV_JS + '\n\\1\n\\2\n\\3',
            content,
            flags=re.DOTALL
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    files_to_update = []
    
    # All root pages
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
        update_page(filepath)
    
    print(f"\nMobile stack menu built on {len(files_to_update)} pages")
    print("Features:")
    print("- Fixed position (always same place)")
    print("- Vertically stacked menu")
    print("- Services dropdown expands on tap")
    print("- All dropdown links work")
    print("- Closes after clicking any link")


if __name__ == "__main__":
    main()
