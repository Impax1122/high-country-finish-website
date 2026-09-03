#!/usr/bin/env python3
"""
Enhance LocalBusiness Schema in index.html
Adds image, priceRange, and other missing fields
"""

import json
import re

def enhance_localbusiness_schema(filepath):
    """Enhance the LocalBusiness schema with additional fields."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the LocalBusiness schema script tag
        pattern = r'(<script type="application/ld\+json">)\s*(\{[^}]*"@type":\s*"LocalBusiness"[^}]*\})\s*(</script>)'
        
        # More robust pattern to match the entire JSON-LD block
        pattern = r'(<script type="application/ld\+json">)(.*?)(@context.*?LocalBusiness.*?)(</script>)'
        
        # Find the schema block
        schema_start = content.find('<script type="application/ld+json">')
        if schema_start == -1:
            print("[ERROR] Could not find LocalBusiness schema")
            return -1
        
        # Find the JSON block start
        json_start = schema_start + len('<script type="application/ld+json">')
        
        # Find the matching closing brace for the JSON
        brace_count = 0
        json_end = json_start
        in_json = False
        
        for i in range(json_start, len(content)):
            char = content[i]
            if char == '{':
                brace_count += 1
                in_json = True
            elif char == '}':
                brace_count -= 1
                if in_json and brace_count == 0:
                    json_end = i + 1
                    break
        
        json_content = content[json_start:json_end].strip()
        
        # Find the script closing tag
        schema_end = content.find('</script>', json_end)
        if schema_end == -1:
            print("[ERROR] Could not find schema end tag")
            return -1
        
        # Parse the JSON
        try:
            schema = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Could not parse JSON: {e}")
            return -1
        
        # Check if already enhanced
        if 'image' in schema and 'priceRange' in schema:
            print("[SKIP] Schema already has image and priceRange")
            return 0
        
        # Add missing fields
        changes_made = 0
        
        if 'image' not in schema:
            schema['image'] = "https://highcountryfinish.com/images/peak-elevator-lobby-sign.jpg"
            changes_made += 1
            print("[ADD] Added 'image' field")
        
        if 'priceRange' not in schema:
            schema['priceRange'] = "$$"
            changes_made += 1
            print("[ADD] Added 'priceRange' field")
        
        # Pretty print the enhanced schema
        enhanced_json = json.dumps(schema, indent=2)
        
        # Replace the schema in the content
        new_schema_block = f'<script type="application/ld+json">\n{enhanced_json}\n</script>'
        new_content = content[:schema_start] + new_schema_block + content[schema_end + len('</script>'):]
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return changes_made
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return -1

def main():
    """Enhance LocalBusiness schema in index.html."""
    filepath = "index.html"
    
    print("LOCALBUSINESS SCHEMA ENHANCEMENT")
    print(f"Processing: {filepath}\n")
    
    result = enhance_localbusiness_schema(filepath)
    
    if result > 0:
        print(f"\n[OK] Schema enhanced with {result} new fields")
    elif result == 0:
        print(f"\n[SKIP] No changes needed")
    else:
        print(f"\n[ERROR] Failed to enhance schema")
    
    return result >= 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
