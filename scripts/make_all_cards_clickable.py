#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make all cards/boxes fully clickable
Not just the "Read More" link - the entire card
"""

import os
import re
from pathlib import Path

# JavaScript to make cards clickable
CLICKABLE_CARDS_JS = """
// Make all cards fully clickable
document.addEventListener('DOMContentLoaded', function() {
  // Find all cards with links inside
  const cards = document.querySelectorAll('.service-card, .blog-card, .service-card-link');
  
  cards.forEach(card => {
    // Find the first link inside the card
    const link = card.querySelector('a');
    if (link) {
      // Make entire card clickable
      card.style.cursor = 'pointer';
      
      card.addEventListener('click', function(e) {
        // Don't double-click if user clicks the actual link
        if (e.target.tagName === 'A') return;
        
        // Navigate to the link's href
        window.location.href = link.href;
      });
      
      // Add visual feedback on hover
      card.addEventListener('mouseenter', function() {
        if (!card.classList.contains('hovering')) {
          card.classList.add('hovering');
        }
      });
      
      card.addEventListener('mouseleave', function() {
        card.classList.remove('hovering');
      });
    }
  });
});
"""

# CSS to improve hover state
CLICKABLE_CARDS_CSS = """
/* Enhanced clickable cards */
.service-card,
.blog-card {
  cursor: pointer;
  user-select: none;
}

.service-card.hovering,
.blog-card.hovering {
  transform: translateY(-4px);
}

.service-card:active,
.blog-card:active {
  transform: translateY(-2px);
}
"""


def add_clickable_cards(filepath):
    """Add clickable card JavaScript to a page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changed = False
    
    # Check if already has clickable cards JS
    if 'Make all cards fully clickable' not in content:
        # Find last </script> before </body>
        body_idx = content.rfind('</body>')
        if body_idx != -1:
            # Find last </script> before body
            script_idx = content.rfind('</script>', 0, body_idx)
            if script_idx != -1:
                # Insert before </script>
                before = content[:script_idx]
                after = content[script_idx:]
                content = before + '\n' + CLICKABLE_CARDS_JS + '\n' + after
                changed = True
    
    # Add CSS if cards exist and CSS not present
    if ('service-card' in content or 'blog-card' in content) and 'Enhanced clickable cards' not in content:
        # Find last style block
        style_end = content.rfind('</style>')
        if style_end != -1:
            before = content[:style_end]
            after = content[style_end:]
            content = before + '\n' + CLICKABLE_CARDS_CSS + '\n' + after
            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Made cards clickable: {os.path.basename(filepath)}")
        return True
    else:
        print(f"Skipped (no cards or already clickable): {os.path.basename(filepath)}")
        return False


def main():
    base_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website")
    
    print("=" * 60)
    print("MAKING ALL CARDS FULLY CLICKABLE")
    print("=" * 60)
    
    updated = 0
    
    all_files = []
    
    # Root pages
    print("\nROOT PAGES:")
    for file in sorted(base_path.glob("*.html")):
        all_files.append(file)
    
    # Service pages
    services_path = base_path / "services"
    if services_path.exists():
        for file in sorted(services_path.glob("*.html")):
            all_files.append(file)
    
    # Blog pages
    blog_path = base_path / "blog"
    if blog_path.exists():
        for file in sorted(blog_path.glob("*.html")):
            all_files.append(file)
    
    for filepath in all_files:
        if add_clickable_cards(filepath):
            updated += 1
    
    print("\n" + "=" * 60)
    print(f"UPDATED {updated} PAGES")
    print("=" * 60)
    print("\nNow all cards are fully clickable:")
    print("  - Service cards on services.html")
    print("  - Blog cards on blog.html")
    print("  - Homepage service cards (if any)")
    print("  - Click anywhere on card to navigate")


if __name__ == "__main__":
    main()
