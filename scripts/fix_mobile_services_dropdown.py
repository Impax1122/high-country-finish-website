#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix mobile Services dropdown:
- Tapping Services should expand dropdown (not navigate)
- Shows all 8 service pages
- Apply to all pages
"""

import os
import re
from pathlib import Path

# Fixed mobile JavaScript - prevents navigation, opens dropdown
FIXED_MOBILE_JS = """
// Mobile menu toggle
function toggleNav() {
  const links = document.getElementById('nav-links');
  const toggle = document.getElementById('nav-toggle');
  const isOpen = links.classList.toggle('open');
  toggle.classList.toggle('is-open', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
}

function closeNav() {
  const links = document.getElementById('nav-links');
  const toggle = document.getElementById('nav-toggle');
  links.classList.remove('open');
  toggle.classList.remove('is-open');
  document.body.classList.remove('nav-open');
  // Also close Services dropdown
  const servicesItem = document.querySelector('.nav-item');
  if (servicesItem) {
    servicesItem.classList.remove('open');
  }
}

// Close menu when clicking links (except Services parent)
document.querySelectorAll('.nav-links a').forEach(a => {
  if (!a.parentElement.classList.contains('nav-item')) {
    a.addEventListener('click', closeNav);
  }
});

// Mobile Services dropdown toggle - PREVENT NAVIGATION
const servicesItem = document.querySelector('.nav-item');
if (servicesItem) {
  const servicesLink = servicesItem.querySelector('a');
  if (servicesLink) {
    servicesLink.addEventListener('click', (e) => {
      // On mobile, prevent navigation and toggle dropdown
      if (window.innerWidth <= 900) {
        e.preventDefault();
        e.stopPropagation();
        servicesItem.classList.toggle('open');
      }
      // On desktop, allow normal dropdown hover (link still works)
    });
  }
  
  // Close menu when clicking dropdown links
  servicesItem.querySelectorAll('.nav-dropdown a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}
"""


def fix_mobile_js(filepath):
    """Replace mobile menu JavaScript in a file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all existing mobile menu JavaScript
    patterns_to_remove = [
        r'// Mobile menu toggle\nfunction toggleNav\(\).*?^\}',
        r'function closeNav\(\).*?^\}',
        r'// Close menu when clicking links.*?\}\);',
        r'// Mobile Services dropdown toggle.*?^\}',
        r'const servicesItem = document\.querySelector.*?^\}',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Find last </script> before </body> and insert fixed JS
    # Pattern: </script> followed by optional comments/whitespace, then </body>
    script_body_pattern = r'(</script>)\s*(<!--.*?-->)?\s*(.*?</body>)'
    
    if re.search(script_body_pattern, content, re.DOTALL):
        content = re.sub(
            script_body_pattern,
            FIXED_MOBILE_JS + '\n\\1\n\\2\n\\3',
            content,
            flags=re.DOTALL
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {os.path.basename(filepath)}")


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
        fix_mobile_js(filepath)
    
    print(f"\nFixed mobile Services dropdown on {len(files_to_update)} pages")
    print("Now on mobile:")
    print("- Tap 'Services' → dropdown opens (does NOT navigate)")
    print("- Shows all 8 service pages")
    print("- Tap any service → goes to page and closes menu")


if __name__ == "__main__":
    main()
