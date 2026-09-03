#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix service pages: they have OLD JavaScript with wrong IDs
Need to replace with correct mobile menu JavaScript
"""

import os
import re
from pathlib import Path

# Correct JavaScript for service pages
CORRECT_JS = """
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


def fix_service_page(filepath):
    """Fix JavaScript in a service page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace everything between <script> and </script>
    script_pattern = r'<script>.*?</script>'
    
    replacement = '<script>' + CORRECT_JS + '\n</script>'
    
    content = re.sub(script_pattern, replacement, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {os.path.basename(filepath)}")


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    # Fix all service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in services_path.glob("*.html"):
            fix_service_page(file)
    
    # Also fix blog pages (they might have the same issue)
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in blog_path.glob("*.html"):
            fix_service_page(file)
    
    print("\nFixed all service and blog pages")
    print("Mobile menu will now work on service pages")


if __name__ == "__main__":
    main()
