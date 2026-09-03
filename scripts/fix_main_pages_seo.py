import re

# Main pages with their correct canonical URLs
main_pages = {
    'about-us.html': 'https://highcountryfinish.com/about-us.html',
    'blog.html': 'https://highcountryfinish.com/blog.html',
    'get-a-quote.html': 'https://highcountryfinish.com/get-a-quote.html',
    'our-process.html': 'https://highcountryfinish.com/our-process.html',
    'service-area.html': 'https://highcountryfinish.com/service-area.html',
    'services.html': 'https://highcountryfinish.com/services.html',
}

for filename, correct_url in main_pages.items():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix canonical tag (if it points to homepage)
        content = re.sub(
            r'<link rel="canonical" href="https://highcountryfinish\.com/"\s*/?>',
            f'<link rel="canonical" href="{correct_url}"/>',
            content
        )
        
        # Fix og:url (if it points to homepage)
        content = re.sub(
            r'<meta property="og:url" content="https://highcountryfinish\.com/"\s*/?>',
            f'<meta property="og:url" content="{correct_url}"/>',
            content
        )
        
        # Standardize NAP - "High Country Finish & Repair CO" (with &, capital CO)
        # Footer copyright line
        content = re.sub(
            r'High Country Finish and Repair CO',
            'High Country Finish & Repair CO',
            content
        )
        
        # Mixed case Co. -> CO
        content = re.sub(
            r'High Country Finish & Repair Co\.',
            'High Country Finish & Repair CO',
            content
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Fixed {filename}")
    
    except FileNotFoundError:
        print(f"[SKIP] {filename} not found")

print("\n[OK] Main pages SEO and NAP updated!")
