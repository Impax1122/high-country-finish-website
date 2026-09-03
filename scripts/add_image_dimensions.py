#!/usr/bin/env python3
"""
Add Width/Height Attributes to Images
Scans HTML files and adds explicit width/height attributes to prevent layout shift
"""

import os
import re
import glob
from pathlib import Path
from PIL import Image

def get_image_dimensions(image_path):
    """Get the dimensions of an image file."""
    try:
        with Image.open(image_path) as img:
            return img.size  # Returns (width, height)
    except Exception as e:
        print(f"[WARNING] Could not read {image_path}: {e}")
        return None

def add_dimensions_to_html(filepath, base_dir):
    """Add width/height attributes to img tags in HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        images_updated = 0
        
        # Find all <img> tags
        img_pattern = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)
        
        def replace_img(match):
            nonlocal images_updated
            img_tag = match.group(0)
            attrs = match.group(1)
            
            # Check if width and height already exist
            if 'width=' in attrs or 'height=' in attrs:
                return img_tag  # Already has dimensions
            
            # Extract src attribute
            src_match = re.search(r'src=["\'](.*?)["\']', attrs, re.IGNORECASE)
            if not src_match:
                return img_tag  # No src found
            
            src = src_match.group(1)
            
            # Resolve image path
            if src.startswith('http://') or src.startswith('https://'):
                return img_tag  # Skip external images
            
            # Remove leading slash
            src_path = src.lstrip('/')
            
            # Build full path
            img_path = base_dir / src_path
            
            if not img_path.exists():
                # Try alternate path (from file's directory)
                file_dir = Path(filepath).parent
                img_path = file_dir / src_path
            
            if not img_path.exists():
                return img_tag  # Image file not found
            
            # Get dimensions
            dimensions = get_image_dimensions(img_path)
            if not dimensions:
                return img_tag
            
            width, height = dimensions
            
            # Add width and height attributes
            # Insert after src attribute
            new_attrs = re.sub(
                r'(src=["\'][^"\']*["\'])',
                r'\1 width="' + str(width) + '" height="' + str(height) + '"',
                attrs
            )
            
            images_updated += 1
            return f'<img {new_attrs}>'
        
        # Replace all img tags
        new_content = img_pattern.sub(replace_img, content)
        
        if images_updated > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return images_updated
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] in {os.path.basename(filepath)}: {e}")
        return -1

def main():
    """Process all HTML files."""
    base_dir = Path(__file__).parent
    
    html_files = []
    html_files.extend(glob.glob(str(base_dir / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "blog" / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "services" / "*.html")))
    
    print(f"IMAGE DIMENSION ADDITION")
    print(f"Found {len(html_files)} HTML files\n")
    
    total_images = 0
    files_modified = 0
    errors = 0
    
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        result = add_dimensions_to_html(filepath, base_dir)
        
        if result > 0:
            print(f"[OK] {filename}: {result} images updated")
            total_images += result
            files_modified += 1
        elif result == 0:
            print(f"[--] {filename}: no changes needed")
        else:
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Images updated: {total_images}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")
    
    return errors == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
