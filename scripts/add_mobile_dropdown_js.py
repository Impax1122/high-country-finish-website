#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add mobile dropdown toggle JS to index and portfolio
"""

from pathlib import Path

mobile_js = """
// Mobile dropdown toggle for Services
if (window.innerWidth <= 768) {
  const servicesLink = document.querySelector('.nav-item > a');
  if (servicesLink) {
    servicesLink.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      e.target.parentElement.classList.toggle('open');
    });
  }
}
"""

def add_mobile_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has mobile dropdown JS
    if 'Mobile dropdown toggle for Services' in content:
        print(f"Skipping {filepath.name} - already has mobile dropdown JS")
        return
    
    # Add before the closing </script> tag at the end
    # Try different markers
    markers = [
        ('</script>\n\n</body>', mobile_js + '\n</script>\n\n</body>'),
        ('</script>\n\n  <!-- Mobile sticky call button -->', mobile_js + '\n</script>\n\n  <!-- Mobile sticky call button -->'),
    ]
    
    updated = False
    for old_marker, new_marker in markers:
        if old_marker in content:
            content = content.replace(old_marker, new_marker, 1)  # Only replace the last occurrence
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added mobile dropdown JS to {filepath.name}")
            updated = True
            break
    
    if not updated:
        print(f"WARNING: Could not find marker in {filepath.name}")

# Update index and portfolio
base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
add_mobile_js(base_path / "index.html")
add_mobile_js(base_path / "portfolio.html")

print("\nMobile dropdown JS added")
