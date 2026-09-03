import re

# LocalBusiness JSON-LD Schema
schema = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "High Country Finish & Repair CO",
  "description": "Professional sign installation and commercial vinyl graphics in Denver and the Front Range. Lobby signs, vehicle wraps, window frosting, wall graphics, and building signs.",
  "url": "https://highcountryfinish.com",
  "telephone": "303-882-4656",
  "email": "highcountryfinishandrepairco@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "9563 Joyce Way",
    "addressLocality": "Arvada",
    "addressRegion": "CO",
    "postalCode": "80007",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "39.8028",
    "longitude": "-105.0875"
  },
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": {
      "@type": "GeoCoordinates",
      "latitude": "39.7392",
      "longitude": "-104.9903"
    },
    "geoRadius": "80000",
    "description": "Denver metro area and the Front Range, including Arvada, Westminster, Thornton, Broomfield, Boulder, Longmont, Fort Collins, Colorado Springs, and surrounding areas"
  },
  "priceRange": "$$",
  "openingHours": "Mo-Fr 08:00-17:00",
  "servesCuisine": "",
  "image": "https://highcountryfinish.com/images/peak-elevator-lobby-sign.jpg",
  "sameAs": [
    "https://www.yelp.com/biz/high-country-finish-and-repair-co-arvada"
  ]
}
</script>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert schema before the <style> tag in <head>
if '<script type="application/ld+json">' in content:
    print("[INFO] Schema already exists, skipping...")
else:
    # Find the <style> tag and insert before it
    content = re.sub(
        r'(<link href="https://fonts\.googleapis\.com/css2\?family=Cormorant.*?" rel="stylesheet"/>\s*)',
        r'\1' + schema + '\n',
        content,
        count=1
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] LocalBusiness schema added to index.html")
