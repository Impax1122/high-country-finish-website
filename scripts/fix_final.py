import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html', encoding='utf-8') as f:
    c = f.read()

# Find button text
btn = re.search(r'Send My Quote Request.{0,10}', c)
if btn:
    print("Button:", repr(btn.group()))

# Find checkmark area
ck = re.search(r'.{0,20}Message received.{0,10}', c)
if ck:
    print("Checkmark:", repr(ck.group()))

# Find all unique non-ASCII sequences outside of CSS comments
# Extract just visible text nodes (not inside style tags)
style_stripped = re.sub(r'<style.*?</style>', '', c, flags=re.DOTALL)
bad_seqs = set(re.findall(r'[\x80-\xff]+', style_stripped))
print("Bad sequences in visible text:", [repr(s) for s in bad_seqs])
