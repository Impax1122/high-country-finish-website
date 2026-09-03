#!/usr/bin/env python3
"""
Add Service Schema to Service Pages
Adds JSON-LD Service schema to each service page
"""

import os
import json
from pathlib import Path

# Service schema mapping
SERVICE_SCHEMAS = {
    "vehicle-wraps.html": {
        "serviceType": "Vehicle Wrap Installation",
        "description": "Professional vehicle wrap installation services in Denver, including full wraps, partial wraps, and fleet graphics for commercial vehicles."
    },
    "window-tint.html": {
        "serviceType": "Commercial Window Tinting Service",
        "description": "Commercial window tinting services in Denver providing UV protection, privacy, energy efficiency, and professional installation."
    },
    "window-frosting.html": {
        "serviceType": "Decorative Window Frosting Service",
        "description": "Decorative window frosting and etched glass effects for Denver businesses, offering privacy, branding, and elegant aesthetics."
    },
    "wall-graphics.html": {
        "serviceType": "Wall Graphics and Murals Installation",
        "description": "Custom wall graphics and mural installation services for Denver businesses, transforming spaces with vibrant, durable vinyl installations."
    },
    "lobby-signs.html": {
        "serviceType": "Lobby Sign Installation",
        "description": "Professional lobby signage installation in Denver, including dimensional letters, acrylic signs, and custom designs for lasting impressions."
    },
    "building-signs.html": {
        "serviceType": "Building Sign Installation",
        "description": "Exterior building signage installation in Denver, including channel letters, monument signs, and facade graphics for maximum business visibility."
    },
    "spot-graphics.html": {
        "serviceType": "Vehicle Spot Graphics and Decals",
        "description": "Vehicle spot graphics and decal installation services in Denver, providing cost-effective mobile advertising with professional installation."
    },
    "custom-work.html": {
        "serviceType": "Custom Vinyl Graphics Installation",
        "description": "Custom vinyl graphics and specialty installation services in Denver. Expert craftsmanship for unique projects with precision and attention to detail."
    }
}

def create_service_schema(service_data):
    """Create Service schema JSON-LD structure."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": service_data["serviceType"],
        "provider": {
            "@type": "LocalBusiness",
            "name": "High Country Finish and Repair CO",
            "telephone": "303-882-4656",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Denver",
                "addressRegion": "CO"
            }
        },
        "areaServed": {
            "@type": "City",
            "name": "Denver"
        },
        "description": service_data["description"]
    }
    return schema

def add_service_schema(filepath):
    """Add Service schema to a service page."""
    try:
        filename = os.path.basename(filepath)
        
        # Check if this file should have a service schema
        if filename not in SERVICE_SCHEMAS:
            return 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Service schema already exists
        if '"@type": "Service"' in content or '"@type":"Service"' in content:
            print(f"[SKIP] {filename}: Service schema already present")
            return 0
        
        # Create the schema
        schema = create_service_schema(SERVICE_SCHEMAS[filename])
        schema_json = json.dumps(schema, indent=2)
        
        # Create the script tag
        schema_script = f'''
  <script type="application/ld+json">
{schema_json}
  </script>
'''
        
        # Find the </head> tag
        head_end = content.find('</head>')
        if head_end == -1:
            print(f"[ERROR] {filename}: No </head> tag found")
            return -1
        
        # Insert before </head>
        new_content = content[:head_end] + schema_script + '  ' + content[head_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 1
        
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return -1

def main():
    """Process service pages."""
    base_dir = Path(__file__).parent / "services"
    
    service_files = list(base_dir.glob("*.html"))
    
    print(f"SERVICE SCHEMA INSERTION")
    print(f"Found {len(service_files)} service pages\n")
    
    files_modified = 0
    files_skipped = 0
    errors = 0
    
    for filepath in sorted(service_files):
        filename = os.path.basename(filepath)
        result = add_service_schema(filepath)
        
        if result > 0:
            print(f"[OK] {filename}: Service schema added")
            files_modified += 1
        elif result == 0:
            files_skipped += 1
        else:
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Service pages processed: {len(service_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Files skipped: {files_skipped}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")
    
    return errors == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
