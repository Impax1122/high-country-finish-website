with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'rb') as f:
    raw = f.read()

# Strip any leading BOMs (UTF-8 BOM = EF BB BF)
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
    print("Stripped one BOM")

# Decode as UTF-8
content = raw.decode('utf-8')

# Fix the checkmark in the success message - use HTML entity to be safe
content = content.replace('✓ Message received!', '&#10003; Message received!')

# Fix any other special unicode chars in visible text that might cause issues
# Replace em-dash decorators in CSS comments (not visible, but clean up)
# Leave them - they're in comments only and don't affect rendering

# Write back without BOM
with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done. File length: {len(content)} chars")

# Verify
with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', 'rb') as f:
    start = f.read(10)
print(f"First bytes: {start.hex()}")
print("BOM present:", start.startswith(b'\xef\xbb\xbf'))
