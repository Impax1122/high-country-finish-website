"""
Full SEO pass for High Country Finish & Repair CO — index.html
Covers: title, meta desc, meta keywords, canonical, OG tags, H1, H2s, H3s,
        img alt text, LocalBusiness schema, footer NAP.
"""

from pathlib import Path

HTML_FILE = Path(r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html')

content = HTML_FILE.read_text(encoding='utf-8')

# ── 1. TITLE TAG ──────────────────────────────────────────────────────────────
content = content.replace(
    '<title>High Country Finish and Repair CO | Denver Vinyl Wraps, Signs & Window Tint</title>',
    '<title>Sign Installation Denver | High Country Finish CO</title>'
)

# ── 2. META DESCRIPTION ───────────────────────────────────────────────────────
content = content.replace(
    '<meta name="description" content="Denver\'s premier vinyl wrap, sign, and window tint specialists. Vehicle wraps, spot graphics, lobby signs, building signs, wall graphics, and commercial window frosting. Serving Denver and surrounding areas."/>',
    '<meta name="description" content="Expert sign installation &amp; commercial vinyl graphics in Denver. Lobby signs, vehicle graphics, storefront wraps &amp; window frosting. Call 303-882-4656 for a free quote."/>'
)

# ── 3. META KEYWORDS ──────────────────────────────────────────────────────────
content = content.replace(
    '<meta name="keywords" content="vinyl wrap Denver, vehicle wrap Denver, car wrap Colorado, window tint Denver, frosted glass Denver, lobby signs Denver, building signs Colorado, wall graphics — sign company Denver, High Country Finish"/>',
    '<meta name="keywords" content="sign installation Denver, commercial vinyl graphics Denver, lobby signs Denver, wall murals Denver CO, window frosting Denver, vehicle graphics Denver, vehicle lettering Denver, storefront graphics Denver, sign shop subcontractor Denver, Front Range vinyl installation, Arvada sign company, commercial graphics installer Colorado"/>'
)

# ── 4. CANONICAL URL ──────────────────────────────────────────────────────────
content = content.replace(
    '<link rel="canonical" href="https://highcountryfinishandrepairco.com/"/>',
    '<link rel="canonical" href="https://highcountryfinish.com/"/>'
)

# ── 5. OG TAGS ────────────────────────────────────────────────────────────────
content = content.replace(
    '<meta property="og:title" content="High Country Finish and Repair CO | Denver Vinyl &amp; Sign Specialists"/>',
    '<meta property="og:title" content="Sign Installation Denver | High Country Finish CO"/>'
)
content = content.replace(
    '<meta property="og:description" content="Premium vinyl wraps, signs, and window tint serving Denver and the Front Range."/>',
    '<meta property="og:description" content="Expert sign installation &amp; commercial vinyl graphics in Denver. Lobby signs, vehicle graphics, storefront wraps &amp; window frosting. Call for a free quote."/>'
)
# Insert og:url and og:image right after og:type
content = content.replace(
    '<meta property="og:type" content="website"/>',
    '<meta property="og:type" content="website"/>\n<meta property="og:url" content="https://highcountryfinish.com/"/>\n<meta property="og:image" content="https://highcountryfinish.com/images/cybertruck-side.jpg"/>'
)

# ── 6. JSON-LD LocalBusiness SCHEMA ──────────────────────────────────────────
schema = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "High Country Finish & Repair CO",
  "url": "https://highcountryfinish.com/",
  "telephone": "303-882-4656",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "9563 Joyce Way",
    "addressLocality": "Arvada",
    "addressRegion": "CO",
    "postalCode": "80007",
    "addressCountry": "US"
  },
  "description": "Denver's premier commercial vinyl graphics and sign installation company. Vehicle graphics, lobby signs, wall murals, window frosting, and storefront graphics serving the Denver metro and Front Range.",
  "areaServed": [
    "Denver", "Arvada", "Aurora", "Lakewood", "Englewood",
    "Thornton", "Westminster", "Broomfield", "Littleton",
    "Castle Rock", "Boulder", "Front Range Colorado"
  ],
  "serviceType": [
    "Sign Installation",
    "Commercial Vinyl Graphics",
    "Lobby Signs",
    "Wall Murals",
    "Window Frosting",
    "Vehicle Graphics",
    "Vehicle Lettering",
    "Storefront Graphics",
    "Building Signs",
    "Fleet Branding",
    "Sign Shop Subcontractor"
  ]
}
</script>
</head>"""

content = content.replace('</head>', schema)

# ── 7. H1 — exactly one, includes primary keyword ────────────────────────────
content = content.replace(
    '      <h1 class="hero-title">\n        Precision craft.<br/>\n        <em>Elevated finish.</em>\n      </h1>',
    '      <h1 class="hero-title">\n        Commercial Vinyl Graphics<br/>\n        <em>&amp; Sign Installation Denver</em>\n      </h1>'
)

# ── 8. H2 TAGS ────────────────────────────────────────────────────────────────
# Services section
content = content.replace(
    '    <h2 class="section-title reveal">Comprehensive vinyl<br/>and sign solutions</h2>',
    '    <h2 class="section-title reveal">Commercial Vinyl Graphics<br/>&amp; Sign Solutions Denver</h2>'
)

# Portfolio section
content = content.replace(
    '      <h2 class="section-title reveal">Built to Last.<br/>Built to Impress.</h2>',
    '      <h2 class="section-title reveal">Denver Sign &amp; Graphics<br/>Portfolio</h2>'
)

# Process section
content = content.replace(
    '    <h2 class="section-title reveal">Simple process,<br/>flawless results</h2>',
    '    <h2 class="section-title reveal">Simple Process,<br/>Flawless Denver Installs</h2>'
)

# About section
content = content.replace(
    '        <h2 class="section-title">Denver\'s detail-<br/>obsessed install crew</h2>',
    '        <h2 class="section-title">Denver\'s Detail-Obsessed<br/>Sign Installation Crew</h2>'
)

# Service Area section
content = content.replace(
    '        <h2 class="section-title">Denver &amp; the<br/>Front Range</h2>',
    '        <h2 class="section-title">Denver &amp; Front Range<br/>Vinyl Installation Area</h2>'
)

# Contact section
content = content.replace(
    '        <h2 class="section-title">Ready to start<br/>your project?</h2>',
    '        <h2 class="section-title">Get a Free Denver<br/>Sign Installation Quote</h2>'
)

# ── 9. H3 SERVICE CARDS — add location where natural ─────────────────────────
content = content.replace(
    '        <h3>Vehicle Wraps &amp; Graphics</h3>',
    '        <h3>Vehicle Graphics &amp; Wraps Denver</h3>'
)
content = content.replace(
    '        <h3>Window Tint &amp; Frosting</h3>',
    '        <h3>Window Frosting &amp; Tinting Denver</h3>'
)
content = content.replace(
    '        <h3>Lobby &amp; Building Signs</h3>',
    '        <h3>Lobby Signs &amp; Building Signs Denver</h3>'
)
content = content.replace(
    '        <h3>Wall Graphics &amp; Murals</h3>',
    '        <h3>Wall Murals &amp; Graphics Denver CO</h3>'
)

# ── 10. IMG ALT TEXT ─────────────────────────────────────────────────────────
# Portfolio images
content = content.replace(
    'alt="Full room wall wrap - O\'Meara Ford / 106.7 KBPI"',
    'alt="full wall mural installation Denver - O\'Meara Ford and 106.7 KBPI branded room wrap"'
)
content = content.replace(
    'alt="Cybertruck full side graphics - Black Rock HVAC"',
    'alt="commercial vehicle graphics Denver - Cybertruck fleet wrap for Black Rock HVAC"'
)
content = content.replace(
    'alt="Elevator door wrap - iHeartMedia"',
    'alt="commercial vinyl wrap Denver - elevator door graphics installation for iHeartMedia"'
)
content = content.replace(
    'alt="Dimensional lobby sign - Novara"',
    'alt="lobby sign installation Denver - dimensional reception sign for Novara office"'
)

# ── 11. FOOTER NAP (Name, Address, Phone) ────────────────────────────────────
old_footer_brand = '''        <p>Denver's premier vinyl wrap, sign, and window tint specialists. Precision installs, every time.</p>
      </div>'''
new_footer_brand = '''        <p>Denver's premier vinyl wrap, sign, and window tint specialists. Precision installs, every time.</p>
        <address style="font-size:12px;color:var(--muted);margin-top:14px;font-style:normal;line-height:1.9;">
          High Country Finish &amp; Repair CO<br/>
          9563 Joyce Way, Arvada, CO 80007<br/>
          <a href="tel:3038824656" style="color:var(--muted)">303-882-4656</a>
        </address>
      </div>'''
content = content.replace(old_footer_brand, new_footer_brand)

# ── WRITE OUTPUT ──────────────────────────────────────────────────────────────
HTML_FILE.write_text(content, encoding='utf-8')
print("SEO pass complete. File written successfully.")
