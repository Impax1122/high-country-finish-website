#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make homepage service cards clickable
"""

from pathlib import Path

index_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define service card replacements
replacements = [
    # Vehicle Graphics & Wraps
    (
        '      <div class="service-card reveal">',
        '      <a href="/services/vehicle-wraps.html" class="service-card-link">\n      <div class="service-card reveal">'
    ),
    # Window Frosting & Tinting (after first service card)
    (
        '      <div class="service-card reveal reveal-delay-1">',
        '      <a href="/services/window-frosting.html" class="service-card-link">\n      <div class="service-card reveal reveal-delay-1">'
    ),
    # Lobby Signs & Building Signs
    (
        '      <div class="service-card reveal reveal-delay-2">',
        '      <a href="/services/lobby-signs.html" class="service-card-link">\n      <div class="service-card reveal reveal-delay-2">'
    ),
    # Wall Murals & Graphics
    (
        '      <div class="service-card reveal reveal-delay-3">',
        '      <a href="/services/wall-graphics.html" class="service-card-link">\n      <div class="service-card reveal reveal-delay-3">'
    ),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new, 1)  # Replace only first occurrence of each

# Now need to close the </a> tags after each service card
# Find each </div> that closes a service-card and add </a> after it
# We need to be careful - each service card has nested divs

# The pattern is: <div class="service-card...">...[content]...</div>
# We need to add </a> after the closing </div> of each service-card

# Simpler approach: find the pattern and replace
service_card_closes = [
    ('        <h3>Vehicle Graphics &amp; Wraps</h3>\n\n        <p>Full wraps, partial wraps, and spot graphics for personal and commercial vehicles. Premium cast vinyl, precision-cut.</p>\n\n      </div>',
     '        <h3>Vehicle Graphics &amp; Wraps</h3>\n\n        <p>Full wraps, partial wraps, and spot graphics for personal and commercial vehicles. Premium cast vinyl, precision-cut.</p>\n\n      </div>\n      </a>'),
    
    ('        <h3>Window Frosting &amp; Tinting</h3>\n\n        <p>Privacy, UV protection, and aesthetic enhancement for residential and commercial properties.</p>\n\n      </div>',
     '        <h3>Window Frosting &amp; Tinting</h3>\n\n        <p>Privacy, UV protection, and aesthetic enhancement for residential and commercial properties.</p>\n\n      </div>\n      </a>'),
    
    ('        <h3>Lobby Signs &amp; Building Signs</h3>\n\n        <p>Make a powerful first impression with professional interior and exterior signage that reflects your brand.</p>\n\n      </div>',
     '        <h3>Lobby Signs &amp; Building Signs</h3>\n\n        <p>Make a powerful first impression with professional interior and exterior signage that reflects your brand.</p>\n\n      </div>\n      </a>'),
    
    ('        <h3>Wall Murals &amp; Graphics</h3>\n\n        <p>Transform interior spaces with bold, high-resolution wall graphics. Perfect for offices, retail, and hospitality.</p>\n\n      </div>',
     '        <h3>Wall Murals &amp; Graphics</h3>\n\n        <p>Transform interior spaces with bold, high-resolution wall graphics. Perfect for offices, retail, and hospitality.</p>\n\n      </div>\n      </a>'),
]

for old, new in service_card_closes:
    content = content.replace(old, new, 1)

# Add CSS for clickable service cards
css_addition = """
.service-card-link {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s;
}
.service-card-link:hover {
  transform: translateY(-4px);
}
.service-card-link .service-card {
  cursor: pointer;
}
"""

# Find .service-card { and insert before it
marker = '.service-card {'
if marker in content:
    content = content.replace(marker, css_addition + '\n' + marker)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Homepage service cards are now clickable")
print("- Vehicle Graphics → /services/vehicle-wraps.html")
print("- Window Frosting → /services/window-frosting.html")
print("- Lobby Signs → /services/lobby-signs.html")
print("- Wall Murals → /services/wall-graphics.html")
