#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix mobile Services dropdown - wrap in DOMContentLoaded
The JavaScript was running before DOM was ready
"""

import os
import re
from pathlib import Path

# Fixed JavaScript - wrapped in DOMContentLoaded
FIXED_JS = """
// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {

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

// Make toggleNav and closeNav available globally for onclick handlers
window.toggleNav = toggleNav;
window.closeNav = closeNav;

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
        console.log('Services dropdown toggled:', servicesItem.classList.contains('open'));
      }
      // On desktop, allow normal dropdown hover (link still works)
    });
  }
  
  // Close menu when clicking dropdown links
  servicesItem.querySelectorAll('.nav-dropdown a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}

}); // End DOMContentLoaded
"""


def fix_js(filepath):
    """Fix JavaScript by wrapping in DOMContentLoaded"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove old mobile menu JavaScript
    patterns = [
        r'// Mobile menu toggle\nfunction toggleNav\(\).*?^\}',
        r'function closeNav\(\).*?^\}',
        r'// Close menu when clicking links.*?\}\);',
        r'// Mobile Services dropdown toggle.*?^\}',
        r'const servicesItem = document\.querySelector.*?^\}',
        r'document\.addEventListener\(\'DOMContentLoaded\',.*?^\}\); // End DOMContentLoaded',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Find where to insert - before closing </script> tag
    # Look for </script> that's in the head section (before </head>)
    head_end = content.find('</head>')
    if head_end != -1:
        # Find last </script> before </head>
        script_end = content.rfind('</script>', 0, head_end)
        if script_end != -1:
            # Insert before </script>
            content = content[:script_end] + '\n' + FIXED_JS + '\n' + content[script_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    files_to_update = []
    
    # All pages
    for file in base_path.glob("*.html"):
        files_to_update.append(file)
    
    services_path = base_path / "services"
    if services_path.exists():
        for file in services_path.glob("*.html"):
            files_to_update.append(file)
    
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in blog_path.glob("*.html"):
            files_to_update.append(file)
    
    for filepath in files_to_update:
        fix_js(filepath)
    
    print(f"\nFixed {len(files_to_update)} pages")
    print("JavaScript now runs AFTER DOM is loaded")
    print("Services dropdown will work on mobile")


if __name__ == "__main__":
    main()
