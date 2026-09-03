#!/usr/bin/env python3
"""
NAP Consistency Fix Script
Replaces all instances of "High Country Finish & Repair" with "High Country Finish and Repair"
"""

import os
import glob
from pathlib import Path

# Patterns to replace
REPLACEMENTS = [
    ("High Country Finish & Repair CO", "High Country Finish and Repair CO"),
    ("High Country Finish & Repair", "High Country Finish and Repair"),
    ("Finish &amp; Repair", "Finish and Repair"),
    ("Finish & Repair", "Finish and Repair"),
]

def fix_nap_in_file(filepath):
    """Fix NAP consistency in a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        for old_pattern, new_pattern in REPLACEMENTS:
            if old_pattern in content:
                count = content.count(old_pattern)
                content = content.replace(old_pattern, new_pattern)
                changes_made += count
                print(f"  - Replaced {count}x: '{old_pattern}' -> '{new_pattern}'")
        
        if changes_made > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made
        return 0
        
    except Exception as e:
        print(f"[ERROR] in {filepath}: {e}")
        return -1

def main():
    """Process all HTML files in the website."""
    base_dir = Path(__file__).parent
    
    # Find all HTML files
    html_files = []
    html_files.extend(glob.glob(str(base_dir / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "blog" / "*.html")))
    html_files.extend(glob.glob(str(base_dir / "services" / "*.html")))
    
    print(f"NAP CONSISTENCY FIX")
    print(f"Found {len(html_files)} HTML files\n")
    
    total_changes = 0
    files_modified = 0
    errors = 0
    
    for filepath in sorted(html_files):
        filename = os.path.basename(filepath)
        changes = fix_nap_in_file(filepath)
        
        if changes > 0:
            print(f"[OK] {filename}: {changes} changes")
            total_changes += changes
            files_modified += 1
        elif changes == 0:
            print(f"[--] {filename}: no changes needed")
        else:
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Files processed: {len(html_files)}")
    print(f"  Files modified: {files_modified}")
    print(f"  Total changes: {total_changes}")
    print(f"  Errors: {errors}")
    print(f"{'='*60}")
    
    return errors == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
