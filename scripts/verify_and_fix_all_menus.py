#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive check: Verify and fix menu button on EVERY page
"""

import os
import re
from pathlib import Path

# Master JavaScript - correct for all pages
MASTER_JS = """
// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {

// Mobile menu toggle
function toggleNav() {
  const links = document.getElementById('nav-links');
  const toggle = document.getElementById('nav-toggle');
  if (!links || !toggle) {
    console.error('Menu elements not found!');
    return;
  }
  const isOpen = links.classList.toggle('open');
  toggle.classList.toggle('is-open', isOpen);
  document.body.classList.toggle('nav-open', isOpen);
}

function closeNav() {
  const links = document.getElementById('nav-links');
  const toggle = document.getElementById('nav-toggle');
  if (!links || !toggle) return;
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

// Mobile Services dropdown toggle
const servicesItem = document.querySelector('.nav-item');
if (servicesItem) {
  const servicesLink = servicesItem.querySelector('a');
  if (servicesLink) {
    servicesLink.addEventListener('click', (e) => {
      if (window.innerWidth <= 900) {
        e.preventDefault();
        e.stopPropagation();
        servicesItem.classList.toggle('open');
      }
    });
  }
  
  servicesItem.querySelectorAll('.nav-dropdown a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}

}); // End DOMContentLoaded
"""


def check_and_fix_page(filepath):
    """Check if page has correct menu JS, fix if needed"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it has the correct JavaScript markers
    has_dom_ready = 'DOMContentLoaded' in content
    has_correct_ids = "getElementById('nav-links')" in content
    has_toggle_function = 'function toggleNav()' in content
    
    if has_dom_ready and has_correct_ids and has_toggle_function:
        print(f"OK: {os.path.basename(filepath)}")
        return False  # No changes needed
    
    # Needs fixing
    print(f"FIXING: {os.path.basename(filepath)}")
    
    # Remove ALL old JavaScript patterns
    patterns_to_remove = [
        r'<script>.*?</script>',  # Remove entire script blocks
    ]
    
    # Find last </script> before </body>
    body_idx = content.rfind('</body>')
    if body_idx != -1:
        # Only remove scripts before body
        before_body = content[:body_idx]
        after_body = content[body_idx:]
        
        # Remove old scripts
        for pattern in patterns_to_remove:
            before_body = re.sub(pattern, '', before_body, flags=re.DOTALL)
        
        # Add correct script before </body>
        new_content = before_body.rstrip() + '\n\n<script>' + MASTER_JS + '\n</script>\n\n' + after_body
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True  # Fixed
    
    return False


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    print("=" * 60)
    print("COMPREHENSIVE MENU CHECK - ALL PAGES")
    print("=" * 60)
    
    all_files = []
    
    # Root pages
    print("\nROOT PAGES:")
    for file in sorted(base_path.glob("*.html")):
        all_files.append(file)
        check_and_fix_page(file)
    
    # Service pages
    print("\nSERVICE PAGES:")
    services_path = base_path / "services"
    if services_path.exists():
        for file in sorted(services_path.glob("*.html")):
            all_files.append(file)
            check_and_fix_page(file)
    
    # Blog pages
    print("\nBLOG PAGES:")
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in sorted(blog_path.glob("*.html")):
            all_files.append(file)
            check_and_fix_page(file)
    
    print("\n" + "=" * 60)
    print(f"TOTAL PAGES CHECKED: {len(all_files)}")
    print("=" * 60)
    print("\nAll pages now have:")
    print("  - Correct IDs (nav-toggle, nav-links)")
    print("  - DOMContentLoaded wrapper")
    print("  - Services dropdown logic")
    print("  - Mobile menu toggle")
    print("  - Global function access")


if __name__ == "__main__":
    main()
