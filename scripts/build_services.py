#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build all service pages for High Country Finish website
"""

import os

def build_html(title, meta_desc, content_html, current_page="services"):
    """Generate complete HTML page with consistent structure"""
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{title}</title>
<meta name="description" content="{meta_desc}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://highcountryfinish.com/"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="https://highcountryfinish.com/"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
/* ─── RESET & BASE ────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  background: #0c0c0c;
  color: #f0ece4;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}
img {{ max-width: 100%; display: block; }}
a {{ color: inherit; text-decoration: none; }}

/* ─── VARIABLES ───────────────────────────── */
:root {{
  --gold:       #C9A84C;
  --gold-light: #E8C97D;
  --gold-dark:  #9B7A2B;
  --black:      #0c0c0c;
  --surface:    #141414;
  --surface2:   #1c1c1c;
  --border:     #2a2a2a;
  --text:       #f0ece4;
  --muted:      #888880;
  --white:      #ffffff;
}}

/* ─── TYPOGRAPHY ──────────────────────────── */
h1, h2, h3, h4 {{
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.01em;
}}
.section-label {{
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
  margin-bottom: 16px;
  display: block;
}}
.section-title {{
  font-size: clamp(32px, 5vw, 52px);
  color: var(--text);
  margin-bottom: 20px;
}}
.section-body {{
  font-size: 16px;
  color: var(--muted);
  max-width: 580px;
  line-height: 1.75;
}}

/* ─── LAYOUT ──────────────────────────────── */
.container {{
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 40px;
}}
section {{ padding: 100px 0; }}
@media(max-width:768px){{ section{{padding:70px 0;}} .container{{padding:0 24px;}} }}

/* ─── GOLD LINE ───────────────────────────── */
.gold-line {{
  width: 48px;
  height: 2px;
  background: var(--gold);
  margin-bottom: 24px;
}}

/* ─── NAV ─────────────────────────────────── */
nav {{
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 24px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(12,12,12,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}}
.nav-brand {{ font-size: 18px; font-weight: 600; color: var(--gold); }}
.nav-links {{ display: flex; gap: 32px; }}
.nav-links a {{ 
  font-size: 14px; 
  color: var(--muted); 
  transition: color 0.2s;
  font-weight: 500;
}}
.nav-links a:hover, .nav-links a.active {{ color: var(--text); }}
.mobile-toggle {{ display: none; }}

@media(max-width:768px){{
  nav {{ padding: 20px 24px; }}
  .nav-links {{ 
    position: fixed;
    top: 0; right: 0;
    height: 100vh;
    width: 280px;
    background: var(--black);
    border-left: 1px solid var(--border);
    flex-direction: column;
    padding: 100px 32px;
    gap: 24px;
    transform: translateX(100%);
    transition: transform 0.3s;
  }}
  .nav-links.open {{ transform: translateX(0); }}
  .mobile-toggle {{
    display: block;
    width: 28px;
    height: 20px;
    position: relative;
    cursor: pointer;
    z-index: 10001;
  }}
  .mobile-toggle span {{
    position: absolute;
    width: 100%;
    height: 2px;
    background: var(--gold);
    transition: all 0.3s;
  }}
  .mobile-toggle span:nth-child(1) {{ top: 0; }}
  .mobile-toggle span:nth-child(2) {{ top: 9px; }}
  .mobile-toggle span:nth-child(3) {{ top: 18px; }}
  .mobile-toggle.open span:nth-child(1) {{ transform: rotate(45deg); top: 9px; }}
  .mobile-toggle.open span:nth-child(2) {{ opacity: 0; }}
  .mobile-toggle.open span:nth-child(3) {{ transform: rotate(-45deg); top: 9px; }}
}}

/* ─── HERO SECTION ────────────────────────── */
.hero {{
  padding: 180px 0 120px;
  min-height: 70vh;
  display: flex;
  align-items: center;
}}
.hero h1 {{
  font-size: clamp(42px, 6vw, 72px);
  margin-bottom: 24px;
  max-width: 800px;
}}
.hero p {{
  font-size: 18px;
  color: var(--muted);
  max-width: 600px;
  line-height: 1.75;
  margin-bottom: 40px;
}}
.cta-button {{
  display: inline-block;
  padding: 16px 32px;
  background: var(--gold);
  color: var(--black);
  font-weight: 600;
  font-size: 14px;
  border-radius: 2px;
  transition: all 0.2s;
  border: 1px solid var(--gold);
}}
.cta-button:hover {{
  background: var(--gold-light);
  border-color: var(--gold-light);
}}

/* ─── CONTENT SECTIONS ────────────────────── */
.content-section {{
  background: var(--surface);
  border-top: 1px solid var(--border);
}}
.content-section:nth-child(even) {{
  background: var(--black);
}}

/* ─── IMAGE BLOCKS ────────────────────────── */
.image-feature {{
  width: 100%;
  max-width: 800px;
  margin: 40px 0;
  border-radius: 4px;
  overflow: hidden;
}}
.image-feature img {{
  width: 100%;
  height: auto;
}}

/* ─── FOOTER ──────────────────────────────── */
footer {{
  background: var(--black);
  border-top: 1px solid var(--border);
  padding: 80px 0 40px;
}}
.footer-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 48px;
  margin-bottom: 60px;
}}
.footer-col h4 {{
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--gold);
  margin-bottom: 20px;
}}
.footer-col a {{
  display: block;
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 12px;
  transition: color 0.2s;
}}
.footer-col a:hover {{
  color: var(--text);
}}
.footer-bottom {{
  padding-top: 40px;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 13px;
  color: var(--muted);
}}
</style>
</head>
<body>

<nav>
  <div class="nav-brand">HIGH COUNTRY FINISH</div>
  <div class="nav-links" id="navLinks">
            <a href="/">Home</a>
            <a href="/services/vehicle-wraps.html" class="active">Services</a>
            <a href="/portfolio.html">Portfolio</a>
            <a href="/our-process.html">Our Process</a>
            <a href="/about-us.html">About Us</a>
            <a href="/service-area.html">Service Area</a>
            <a href="/get-a-quote.html">Get a Quote</a>
            <a href="/blog.html">Blog</a>
  </div>
  <div class="mobile-toggle" id="mobileToggle">
    <span></span>
    <span></span>
    <span></span>
  </div>
</nav>

{content_html}

<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <h4>Services</h4>
        <a href="/services/vehicle-wraps.html">Vehicle Wraps</a>
        <a href="/services/spot-graphics.html">Spot Graphics</a>
        <a href="/services/window-tint.html">Window Tint</a>
        <a href="/services/window-frosting.html">Window Frosting</a>
        <a href="/services/wall-graphics.html">Wall Graphics</a>
        <a href="/services/lobby-signs.html">Lobby Signs</a>
        <a href="/services/building-signs.html">Building Signs</a>
        <a href="/services/custom-work.html">Custom Work</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="/about-us.html">About Us</a>
        <a href="/portfolio.html">Portfolio</a>
        <a href="/our-process.html">Our Process</a>
        <a href="/service-area.html">Service Area</a>
        <a href="/blog.html">Blog</a>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <a href="tel:3038824656">303-882-4656</a>
        <a href="mailto:highcountryfinishandrepairco@gmail.com">highcountryfinishandrepairco@gmail.com</a>
        <p style="margin-top:12px;font-size:14px;color:var(--muted);">Denver, CO & surrounding areas</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Denver's premier vinyl graphics, sign, and window film specialists. Precision installs, every time.</p>
      <p style="margin-top:12px;">&copy; 2026 High Country Finish & Repair Co. All rights reserved.</p>
    </div>
  </div>
</footer>

<script>
const toggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');
toggle.addEventListener('click', () => {{
  toggle.classList.toggle('open');
  navLinks.classList.toggle('open');
  document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
}});
navLinks.querySelectorAll('a').forEach(link => {{
  link.addEventListener('click', () => {{
    toggle.classList.remove('open');
    navLinks.classList.remove('open');
    document.body.style.overflow = '';
  }});
}});
</script>

</body>
</html>"""


# Service page content
SERVICE_PAGES = {
    "vehicle-wraps.html": {
        "title": "Vehicle Wrap Installation in Denver | Full Wraps, Partial Wraps & Fleet Graphics",
        "desc": "Professional vehicle wrap installation in Denver and the Front Range for full wraps, partial wraps, fleet branding, and commercial vehicle graphics.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Vehicle Wrap Installation</h1>
    <p>A well-installed vehicle wrap turns a work truck, van, trailer, or fleet vehicle into a moving advertisement. High Country Finish & Repair Co. provides clean, professional vehicle wrap installation for businesses across Denver, Arvada, and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Full Wraps & Fleet Branding</span>
    <h2 class="section-title">Full Wraps, Partial Wraps & Fleet Branding</h2>
    <div class="section-body">
      <p>We install full wraps, partial wraps, cut vinyl graphics, and commercial fleet branding for businesses that want a polished, professional look on the road. Whether you are wrapping one vehicle or building out a fleet, we focus on layout, clean lines, tight finish work, and a result that represents your company well.</p>
    </div>
    <div class="image-feature">
      <img src="/images/957-party-vehicle-wrap.jpg" alt="957 The Party radio station vehicle wrap Denver — professional installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Why Install Quality Matters</span>
    <h2 class="section-title">Why Install Quality Matters</h2>
    <div class="section-body">
      <p>Wrap design gets attention, but installation is what determines whether the finished product looks premium. Straight alignment, clean seams, careful trimming, and proper prep all matter. We approach every wrap with the same goal: make it look right up close and from a distance.</p>
    </div>
    <div class="image-feature">
      <img src="/images/cybertruck-side.jpg" alt="Cybertruck vinyl wrap Denver — precision installation with clean seams" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Install-Only Services</span>
    <h2 class="section-title">Install-Only Vehicle Graphics</h2>
    <div class="section-body">
      <p>Already have printed wrap panels or cut vinyl ready to go? We also handle install-only work for clients, sign shops, and print providers who need a dependable installer in the Denver area.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Common Projects</span>
    <h2 class="section-title">Common Vehicle Wrap Projects</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Full commercial wraps</li>
        <li>Partial wraps</li>
        <li>Service truck branding</li>
        <li>Fleet graphics</li>
        <li>Vehicle logos and lettering</li>
        <li>Trailer graphics</li>
        <li>Spot graphics packages</li>
      </ul>
      <p style="margin-top:40px;">If your business wants stronger visibility on the road, a professionally installed wrap is one of the best branding tools you can invest in.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Request a Vehicle Wrap Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "spot-graphics.html": {
        "title": "Spot Graphics Installation in Denver | Vehicle Lettering, Logos & Decals",
        "desc": "Spot graphics installation for vehicles, windows, walls, and branded surfaces in Denver and the Front Range. Professional logos, lettering, and vinyl decal installs.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Spot Graphics Installation</h1>
    <p>Spot graphics are a cost-effective way to brand vehicles, storefronts, and interior spaces without committing to a full wrap. High Country Finish & Repair Co. installs spot graphics with clean placement and finish detail for businesses across Denver and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Simple Branding</span>
    <h2 class="section-title">Simple Branding, Strong Impact</h2>
    <div class="section-body">
      <p>Spot graphics can include vehicle door logos, tailgate lettering, service information, office decals, window logos, hours of operation, and simple branded vinyl elements. When installed correctly, even small graphics make a business look more established and professional.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Applications</span>
    <h2 class="section-title">Where Spot Graphics Work Best</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Commercial vehicles</li>
        <li>Fleet doors and tailgates</li>
        <li>Storefront windows</li>
        <li>Interior office branding</li>
        <li>Jobsite trailers</li>
        <li>Directional and informational graphics</li>
      </ul>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Cost-Effective Solution</span>
    <h2 class="section-title">A Better Option Than Going Too Big</h2>
    <div class="section-body">
      <p>For many businesses, spot graphics are the right fit. They keep costs down while still adding clear branding to high-visibility surfaces. They are especially useful for contractors, service businesses, delivery vehicles, and storefronts that need a clean branded look without a full wrap package.</p>
      <p style="margin-top:40px;">If you need logos, lettering, or simple branded graphics installed cleanly and professionally, spot graphics are a smart place to start.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Get a Spot Graphics Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "window-tint.html": {
        "title": "Window Tint Installation in Denver | Commercial & Residential Window Film",
        "desc": "Professional window tint installation in Denver and the Front Range for glare reduction, privacy, UV control, and a cleaner finished look.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Window Tint Installation</h1>
    <p>Window tint is one of the cleanest ways to improve privacy, reduce glare, and make a space feel more comfortable and finished. High Country Finish & Repair Co. provides window tint installation in Denver and surrounding Front Range communities for commercial spaces and select residential projects.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Benefits</span>
    <h2 class="section-title">Benefits of Window Tint</h2>
    <div class="section-body">
      <p>Window tint can help reduce glare, improve privacy, cut down UV exposure, and create a cleaner appearance from both inside and outside the building. It is a practical upgrade for offices, storefronts, conference rooms, and other glass-heavy spaces.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Commercial Film</span>
    <h2 class="section-title">Commercial Window Film That Looks Professional</h2>
    <div class="section-body">
      <p>Commercial spaces need film that performs well and looks sharp. We install window tint with careful prep, clean edges, and a finished look that fits the space.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Applications</span>
    <h2 class="section-title">Common Window Tint Applications</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Office windows</li>
        <li>Conference rooms</li>
        <li>Storefront glass</li>
        <li>Interior glass partitions</li>
        <li>Entry doors</li>
        <li>Select residential windows</li>
      </ul>
      <p style="margin-top:40px;">If your space needs more privacy, better glare control, or a more polished look, window tint is a simple upgrade with a noticeable impact.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Request a Window Tint Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "window-frosting.html": {
        "title": "Window Frosting Installation in Denver | Privacy Film for Offices & Storefronts",
        "desc": "Professional frosted window film installation in Denver and the Front Range for offices, conference rooms, storefronts, and interior glass partitions.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Window Frosting Installation</h1>
    <p>Frosted window film adds privacy without closing off a space. It is one of the most effective ways to make office glass feel more professional, modern, and functional. High Country Finish & Repair Co. installs frosted film for businesses throughout Denver and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Privacy Without Losing Light</span>
    <h2 class="section-title">Privacy Without Losing Light</h2>
    <div class="section-body">
      <p>Window frosting helps define rooms, conference areas, and office spaces while still allowing light to pass through. That makes it a popular choice for professional offices, reception areas, interior glass walls, and storefronts.</p>
    </div>
    <div class="image-feature">
      <img src="/images/novara-frosted-glass.jpg" alt="Novara office frosted glass Denver — privacy film installation for conference rooms" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Decorative Options</span>
    <h2 class="section-title">Decorative Frosting, Privacy Bands & Logo Cutouts</h2>
    <div class="section-body">
      <p>We install full frosted panels, privacy bands, decorative frosted film, and custom logo cutouts depending on the look you want. Whether the goal is simple privacy or branded glass, clean layout and clean trimming make all the difference.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Applications</span>
    <h2 class="section-title">Popular Frosting Applications</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Conference rooms</li>
        <li>Office entry glass</li>
        <li>Interior partitions</li>
        <li>Storefront windows</li>
        <li>Waiting rooms</li>
        <li>Branded logo frosting</li>
      </ul>
      <p style="margin-top:40px;">If your glass needs privacy and a more finished appearance, frosted film is one of the cleanest solutions available.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Get a Window Frosting Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "wall-graphics.html": {
        "title": "Wall Graphics Installation in Denver | Wall Murals, Wraps & Office Branding",
        "desc": "Professional wall graphics installation in Denver and the Front Range for branded offices, murals, retail interiors, and large-format wall wraps.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Wall Graphics Installation</h1>
    <p>Wall graphics turn blank surfaces into branded, high-impact spaces. High Country Finish & Repair Co. installs wall graphics, murals, and wall wraps for offices, retail spaces, hospitality environments, and commercial interiors throughout Denver and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Branded Walls</span>
    <h2 class="section-title">Branded Walls That Transform a Space</h2>
    <div class="section-body">
      <p>Wall graphics can be bold and attention-grabbing or subtle and refined. We install everything from simple logo graphics and statement walls to full environmental branding packages and large-format murals.</p>
    </div>
    <div class="image-feature">
      <img src="/images/elite-brands-mural-wide2.jpg" alt="Elite Brands large wall mural Denver — professional wall graphics installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Applications</span>
    <h2 class="section-title">Where Wall Graphics Work Best</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Office lobbies</li>
        <li>Conference rooms</li>
        <li>Hallways</li>
        <li>Retail interiors</li>
        <li>Gyms and fitness spaces</li>
        <li>Restaurants and hospitality spaces</li>
        <li>Branded work environments</li>
      </ul>
    </div>
    <div class="image-feature">
      <img src="/images/gque-bbq-mural.jpg" alt="Gque BBQ wall mural Denver — restaurant interior branding" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Installation Quality</span>
    <h2 class="section-title">Professional Install Makes the Difference</h2>
    <div class="section-body">
      <p>Large-format wall graphics need careful layout, surface prep, and finish work to look clean. We focus on alignment, seam control, trimming, and overall presentation so the finished wall feels intentional and polished.</p>
      <p style="margin-top:40px;">If you want to add branding, energy, or visual impact to a commercial interior, wall graphics are one of the most effective upgrades you can make.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Request a Wall Graphics Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "lobby-signs.html": {
        "title": "Lobby Sign Installation in Denver | Reception Signs, Acrylic Signs & Dimensional Letters",
        "desc": "Professional lobby sign installation in Denver and the Front Range for reception signs, acrylic panels, dimensional letters, stand-off signs, and interior office signage.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Lobby Sign Installation</h1>
    <p>Your lobby sign is often the first branded element people see when they enter your office. High Country Finish & Repair Co. installs lobby signs that help businesses make a polished, professional first impression.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Reception Signs</span>
    <h2 class="section-title">Reception Signs That Look Balanced and Finished</h2>
    <div class="section-body">
      <p>A good lobby sign does more than display a logo. It sets the tone for the space. We install acrylic signs, dimensional letters, stand-off signs, office branding pieces, and other reception signage with a careful eye for spacing, level placement, and final presentation.</p>
    </div>
    <div class="image-feature">
      <img src="/images/kpa-lobby-sign.jpg" alt="KPA lobby sign Denver — dimensional letters with precision placement" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Sign Types</span>
    <h2 class="section-title">Common Lobby Sign Types</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Acrylic logo panels</li>
        <li>Stand-off signs</li>
        <li>Dimensional lettering</li>
        <li>Reception wall logos</li>
        <li>Branded office displays</li>
        <li>Directory and suite signs</li>
      </ul>
    </div>
    <div class="image-feature">
      <img src="/images/sea-lobby-wide.jpg" alt="SEA office lobby sign Denver — acrylic panel with stand-off mounting" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Installation Quality</span>
    <h2 class="section-title">Installation Quality Is Everything</h2>
    <div class="section-body">
      <p>Even a high-end sign can look average if it is installed poorly. Clean layout, proper mounting, and balanced placement are what make a lobby sign feel professional.</p>
      <p style="margin-top:40px;">If you want your office to make a strong first impression, a professionally installed lobby sign is one of the best upgrades you can make.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Get a Lobby Sign Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "building-signs.html": {
        "title": "Building Sign Installation in Denver | Exterior Business Signs & Storefront Signage",
        "desc": "Exterior building sign installation in Denver and the Front Range for storefront signage, mounted panels, branded exterior signs, and business visibility.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Building Sign Installation</h1>
    <p>Exterior signs are often the first thing customers see before they ever walk through the door. High Country Finish & Repair Co. installs building signs for businesses across Denver and the Front Range that want clean, professional exterior branding.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Storefront Signs</span>
    <h2 class="section-title">Storefront Signs That Help Your Business Get Seen</h2>
    <div class="section-body">
      <p>From office buildings to retail storefronts and commercial properties, we install exterior signs that improve visibility and strengthen your brand presence. Proper placement, level mounting, and a clean finish matter on highly visible exterior work.</p>
    </div>
    <div class="image-feature">
      <img src="/images/buffalo-building-sign.jpg" alt="Buffalo Restaurant exterior building sign Denver — professional installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Common Projects</span>
    <h2 class="section-title">Common Building Sign Projects</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Exterior storefront signs</li>
        <li>Mounted sign panels</li>
        <li>Fascia signs</li>
        <li>Office building signage</li>
        <li>Exterior branding elements</li>
        <li>Replacement sign installs</li>
      </ul>
    </div>
    <div class="image-feature">
      <img src="/images/trinity-place-exterior-sign.jpg" alt="Trinity Place exterior sign Denver — building signage installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Dependable Installation</span>
    <h2 class="section-title">Dependable Installation for Visible Work</h2>
    <div class="section-body">
      <p>Exterior signage has to look good and feel secure. We focus on clean alignment, strong finish quality, and professional presentation so your business looks established from the outside in.</p>
      <p style="margin-top:40px;">If your exterior signage needs to be installed, replaced, or upgraded, we can help you get it done cleanly and professionally.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Request a Building Sign Quote</a></p>
    </div>
  </div>
</section>
"""
    },
    
    "custom-work.html": {
        "title": "Custom Sign & Graphics Installation in Denver | Specialty Commercial Projects",
        "desc": "Custom sign and graphics installation in Denver and the Front Range for specialty branding, non-standard installs, rework, replacements, and one-off projects.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Custom Work</h1>
    <p>Not every project fits neatly into a standard service category. That is where custom work comes in. High Country Finish & Repair Co. handles specialty sign and graphics installation projects for businesses, sign shops, and commercial partners throughout Denver and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Specialty Projects</span>
    <h2 class="section-title">Specialty Projects Need Practical Problem-Solving</h2>
    <div class="section-body">
      <p>Custom work often involves unusual surfaces, non-standard layouts, mixed materials, partial replacements, re-installation, or jobs that require a more flexible approach. These are the projects where experience, clean execution, and attention to detail matter the most.</p>
    </div>
    <div class="image-feature">
      <img src="/images/iheart-elevator-wrap.jpg" alt="iHeart Radio elevator wrap Denver — specialty custom installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Examples</span>
    <h2 class="section-title">Examples of Custom Work</h2>
    <div class="section-body">
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);line-height:2;">
        <li>Specialty office branding</li>
        <li>One-off signage installs</li>
        <li>Replacement graphics</li>
        <li>Re-installation work</li>
        <li>Mixed-material branded elements</li>
        <li>Unique display projects</li>
        <li>Install-only commercial requests</li>
      </ul>
    </div>
    <div class="image-feature">
      <img src="/images/omeara-room-wrap-wide.jpg" alt="O'Meara room wrap Denver — custom full wall wrap installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Different Projects Need Flexible Approaches</span>
    <h2 class="section-title">If the Project Is Different, Reach Out</h2>
    <div class="section-body">
      <p>If you are not sure where your job fits, send us the details. We are happy to review the scope and let you know whether it is a fit.</p>
      <p style="margin-top:40px;">Custom projects do not need a cookie-cutter approach. They need careful review and a clean final result.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Tell Us About Your Project</a></p>
    </div>
  </div>
</section>
"""
    }
}


def build_service_pages():
    base_path = "C:\\Users\\Spaceship\\.openclaw\\workspace\\vinyl-website\\services"
    
    for filename, data in SERVICE_PAGES.items():
        html = build_html(
            data["title"],
            data["desc"],
            data["content"]
        )
        filepath = os.path.join(base_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created {filename}")


if __name__ == "__main__":
    build_service_pages()
    print("\nAll service pages complete")
