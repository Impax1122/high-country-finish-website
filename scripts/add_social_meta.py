#!/usr/bin/env python3
"""
Add Social Media Meta Tags (Open Graph + Twitter Cards)
Adds OG and Twitter meta tags to all HTML pages
"""

import os
import glob
import re
from pathlib import Path

# Page-specific metadata
PAGE_META = {
    "index.html": {
        "title": "High Country Finish and Repair CO - Denver Commercial Vinyl Graphics & Signage",
        "description": "Premier commercial vinyl graphics and sign installation in Denver. Vehicle wraps, window tinting, lobby signs, building signs, and custom installations. Call 303-882-4656."
    },
    "about-us.html": {
        "title": "About Us - High Country Finish and Repair CO",
        "description": "Meet the team behind Denver's trusted commercial vinyl and signage installation experts. Quality craftsmanship and attention to detail since day one."
    },
    "services.html": {
        "title": "Our Services - High Country Finish and Repair CO",
        "description": "Complete commercial vinyl and signage services in Denver: vehicle wraps, window tint & frosting, wall graphics, lobby signs, building signs, and custom installations."
    },
    "portfolio.html": {
        "title": "Portfolio - High Country Finish and Repair CO",
        "description": "View our work: vehicle wraps, window graphics, lobby signs, building signage, and custom vinyl installations for Denver businesses."
    },
    "blog.html": {
        "title": "Blog - High Country Finish and Repair CO",
        "description": "Expert tips and insights on commercial vinyl graphics, signage, and installation best practices in Denver, Colorado."
    },
    "get-a-quote.html": {
        "title": "Get a Quote - High Country Finish and Repair CO",
        "description": "Request a free quote for your commercial vinyl graphics or signage project in Denver. Fast response, competitive pricing, professional installation."
    },
    "our-process.html": {
        "title": "Our Process - High Country Finish and Repair CO",
        "description": "From consultation to installation: learn how we deliver high-quality commercial vinyl graphics and signage for Denver businesses."
    },
    "service-area.html": {
        "title": "Service Area - High Country Finish and Repair CO",
        "description": "Serving Denver, Arvada, Aurora, Lakewood, Westminster, and surrounding areas with commercial vinyl graphics and professional sign installation."
    },
    "vehicle-wraps.html": {
        "title": "Vehicle Wraps - High Country Finish and Repair CO",
        "description": "Professional vehicle wrap installation in Denver. Full wraps, partial wraps, and fleet graphics that turn your vehicles into mobile billboards."
    },
    "window-tint.html": {
        "title": "Window Tinting - High Country Finish and Repair CO",
        "description": "Commercial window tinting in Denver. UV protection, privacy, energy efficiency, and professional installation for businesses."
    },
    "window-frosting.html": {
        "title": "Window Frosting - High Country Finish and Repair CO",
        "description": "Decorative window frosting and etched glass effects for Denver businesses. Privacy, branding, and elegant aesthetics."
    },
    "wall-graphics.html": {
        "title": "Wall Graphics & Murals - High Country Finish and Repair CO",
        "description": "Custom wall graphics and murals for Denver businesses. Transform your space with vibrant, durable vinyl wall installations."
    },
    "lobby-signs.html": {
        "title": "Lobby Signs - High Country Finish and Repair CO",
        "description": "Professional lobby signage installation in Denver. Dimensional letters, acrylic signs, and custom designs that make a lasting impression."
    },
    "building-signs.html": {
        "title": "Building Signs - High Country Finish and Repair CO",
        "description": "Exterior building signage installation in Denver. Channel letters, monument signs, and façade graphics for maximum visibility."
    },
    "spot-graphics.html": {
        "title": "Spot Graphics - High Country Finish and Repair CO",
        "description": "Vehicle spot graphics and decals in Denver. Cost-effective mobile advertising for your business with professional installation."
    },
    "custom-work.html": {
        "title": "Custom Installations - High Country Finish and Repair CO",
        "description": "Custom vinyl graphics and specialty installations in Denver. If you can dream it, we can install it with precision and expertise."
    },
    # Blog posts
    "choosing-the-right-building-sign-for-your-denver-business.html": {
        "title": "Choosing the Right Building Sign for Your Denver Business",
        "description": "Expert guide to selecting the perfect building sign for your Denver business. Types, materials, and considerations for maximum impact."
    },
    "frosted-glass-vs-window-tint-for-offices.html": {
        "title": "Frosted Glass vs Window Tint for Offices",
        "description": "Compare frosted glass and window tint for Denver offices. Privacy, aesthetics, cost, and functionality explained by installation experts."
    },
    "how-long-do-vehicle-wraps-last-in-colorado.html": {
        "title": "How Long Do Vehicle Wraps Last in Colorado?",
        "description": "Learn about vehicle wrap lifespan in Colorado's climate. Factors affecting durability, maintenance tips, and what to expect from your investment."
    },
    "how-to-prepare-a-wall-for-wall-graphics-and-murals.html": {
        "title": "How to Prepare a Wall for Wall Graphics and Murals",
        "description": "Professional wall preparation guide for vinyl graphics and murals. Surface requirements, cleaning, and best practices for perfect installation."
    },
    "what-makes-a-lobby-sign-look-expensive.html": {
        "title": "What Makes a Lobby Sign Look Expensive?",
        "description": "Design secrets for premium lobby signage. Materials, lighting, mounting techniques, and details that create high-end commercial appeal."
    }
}

def get_relative_path(filepath):
    """Get URL-relative path for og:url."""
    filename = os.path.basename(filepath)
    
    if "services\\" in filepath or "services/" in filepath:
        return f"services/{filename}"
    elif "blog\\" in filepath or "blog/" in filepath:
        return f"blog/{filename}"
    else:
        return filename

def add_social_meta(filepath):
    """Add social media meta tags to HTML file."""
    try:
        filename = os.path.basename(filepath)
        
        # Get metadata for this page
        meta = PAGE_META.get(filename)
        if not meta:
            print(f"[SKIP] {filename}: No metadata defined")
            return 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if OG tags already exist
        if 'property="og:title"' in content:
            print(f"[SKIP] {filename}: Social meta already present")
            return 0
        
        # Find the </head> tag
        head_end = content.find('</head>')
        if head_end == -1:
            print(f"[ERROR] {filename}: No </head> tag found")
            return -1
        
        # Build the social media meta tags
        rel_path = get_relative_path(filepath)
        social_meta = f'''
    <!-- Open Graph -->
    <meta property="og:title" content="{meta['title']}">
    <meta property="og:description" content="{meta['description']}">
    <meta property="og:image" content="https://highcountryfinish.com/images/og-image.jpg">
    <meta property="og:url" content="https://highcountryfinish.com/{rel_path}">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{meta['title']}">
    <meta name="twitter:description" content="{meta['description']}">
    <meta name="twitter:image" content="https://highcountryfinish.com/images/twitter-card.jpg">
'''
        
        # Insert before </head>
        new_content = content[:head_end] + social_meta + '  ' + content[head_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 1
        
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return -1

def main():
    """Process all HTML files."""
    base_dir = Path(__file__).parent
    
    html_files = []
    html_files.extend(glob.glob(str(base_dir / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "blog" / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "services" / "*.html")))
    
    print(f"SOCIAL MEDIA META TAG INSERTION")
    print(f"Found {len(html_files)} HTML files\n")
    
    files_modified = 0
    files_skipped = 0
    errors = 0
    
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        result = add_social_meta(filepath)
        
        if result > 0:
            print(f"[OK] {filename}: Social meta added")
            files_modified += 1
        elif result == 0:
            files_skipped += 1
        else:
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Files skipped: {files_skipped}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")
    
    return errors == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
