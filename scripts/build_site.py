#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build out full High Country Finish website
Dark luxury aesthetic, clean typography, premium feel
"""

import os

# Common HTML structure
def build_html(title, meta_desc, content_html, current_page=""):
    """Generate complete HTML page with consistent structure"""
    
    # Navigation active state logic
    nav_items = {
        "home": "",
        "services": "services",
        "portfolio": "portfolio",
        "process": "our-process",
        "about": "about-us",
        "area": "service-area",
        "quote": "get-a-quote",
        "blog": "blog"
    }
    
    nav_html = ""
    for key, page in nav_items.items():
        if key == "home":
            link = "/"
            text = "Home"
        elif key == "services":
            link = "/services/vehicle-wraps.html"
            text = "Services"
        elif key == "portfolio":
            link = "/portfolio.html"
            text = "Portfolio"
        elif key == "process":
            link = "/our-process.html"
            text = "Our Process"
        elif key == "about":
            link = "/about-us.html"
            text = "About Us"
        elif key == "area":
            link = "/service-area.html"
            text = "Service Area"
        elif key == "quote":
            link = "/get-a-quote.html"
            text = "Get a Quote"
        elif key == "blog":
            link = "/blog.html"
            text = "Blog"
        
        active_class = ' class="active"' if current_page == page else ""
        nav_html += f'            <a href="{link}"{active_class}>{text}</a>\n'
    
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
.cta-button.secondary {{
  background: transparent;
  color: var(--gold);
  margin-left: 16px;
}}
.cta-button.secondary:hover {{
  background: var(--surface);
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

/* ─── GRID LAYOUTS ────────────────────────── */
.services-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  margin-top: 60px;
}}
.service-card {{
  background: var(--surface2);
  padding: 32px;
  border: 1px solid var(--border);
  border-radius: 4px;
  transition: border-color 0.2s;
}}
.service-card:hover {{
  border-color: var(--gold-dark);
}}
.service-card h3 {{
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--text);
}}
.service-card p {{
  font-size: 15px;
  color: var(--muted);
  line-height: 1.7;
}}
.service-card a {{
  display: inline-block;
  margin-top: 16px;
  color: var(--gold);
  font-size: 14px;
  font-weight: 600;
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
{nav_html}  </div>
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
// Mobile menu toggle
const toggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');
toggle.addEventListener('click', () => {{
  toggle.classList.toggle('open');
  navLinks.classList.toggle('open');
  document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
}});

// Close menu when clicking a link
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


# Page content builders
def about_us_content():
    return """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>About Us</h1>
    <p>High Country Finish & Repair Co. is a Denver-area vinyl graphics and sign installation company built around one simple idea: the finished product should look right. Not close enough. Not good from ten feet away. Right.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Our Approach</span>
    <h2 class="section-title">A Detail-Obsessed Approach to Installation</h2>
    <div class="section-body">
      <p>We work on projects where finish quality matters. Vehicle graphics. Window film. Wall wraps. Lobby signs. Building signs. Custom branded environments. In every category, the difference between average work and professional work usually comes down to the details.</p>
      <p style="margin-top:20px;">That is where we put our focus. Clean lines. Careful layout. Proper prep. Sharp trimming. Balanced placement. Secure mounting. We believe clients should be proud of the finished result and confident putting their name on it.</p>
    </div>
    <div class="image-feature">
      <img src="/images/peak-elevator-lobby-sign.jpg" alt="PEAK Elevator lobby sign installation Denver — precision-mounted dimensional letters" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Who We Serve</span>
    <h2 class="section-title">Built for Commercial Clients, Sign Shops & Print Partners</h2>
    <div class="section-body">
      <p>Some of our clients come to us directly for their own office, storefront, fleet, or property. Others are print providers, sign shops, and commercial partners who need a reliable installer they can trust to show up, represent the work well, and complete the job professionally.</p>
      <p style="margin-top:20px;">We understand that install quality reflects on everyone involved. That is why we keep communication clear, show up prepared, and treat every project like it matters.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Why Clients Return</span>
    <h2 class="section-title">Why Clients Call Us Back</h2>
    <div class="section-body">
      <p>Clients come back to High Country Finish & Repair Co. because they know what to expect: clear communication, dependable scheduling, professional installation, and work that looks polished when it is done. We are not trying to be the biggest shop in town. We are trying to be the one people trust when the finish matters.</p>
    </div>
    <div class="image-feature">
      <img src="/images/elite-brands-wall-mural.jpg" alt="Elite Brands office wall mural Denver — full wall branded graphics installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Service Area</span>
    <h2 class="section-title">Serving Denver & the Front Range</h2>
    <div class="section-body">
      <p>We are based in the Denver metro area and regularly serve businesses throughout Arvada and surrounding Front Range communities. From one-off installs to repeat commercial work, we bring the same standard to every project: do it clean, do it right, and leave the site looking better than we found it.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Get a Free Quote</a></p>
    </div>
  </div>
</section>
"""


def our_process_content():
    return """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Our Process</h1>
    <p>We keep the process simple so projects move quickly and cleanly. Whether you are a business owner, office manager, sign shop, or print provider, our goal is to make the path from quote to finished install as straightforward as possible.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 1</span>
    <h2 class="section-title">Project Review</h2>
    <div class="section-body">
      <p>Send over the details you have: sizes, photos, address, surfaces, access information, and timeline. We review the scope carefully so we understand what the project actually requires before quoting it.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 2</span>
    <h2 class="section-title">Clear Quote</h2>
    <div class="section-body">
      <p>Once the scope is clear, we provide straightforward pricing based on the work involved. We aim to keep estimates easy to understand, with no confusion about what is included.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 3</span>
    <h2 class="section-title">Planning & Scheduling</h2>
    <div class="section-body">
      <p>After approval, we coordinate scheduling around your timeline, material readiness, and site access. Good installs start before install day, so we make sure the logistics are in place.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 4</span>
    <h2 class="section-title">Surface Prep & Layout</h2>
    <div class="section-body">
      <p>Before final installation, we prep the surface, verify layout, and make sure everything is positioned correctly. That prep work is a major part of what separates a rushed install from a professional one.</p>
    </div>
    <div class="image-feature">
      <img src="/images/glover-masonry-lobby.jpg" alt="Glover Masonry lobby sign Denver — clean layout and precision installation" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 5</span>
    <h2 class="section-title">Precision Installation</h2>
    <div class="section-body">
      <p>We install carefully, trim cleanly, and finish the work so it looks intentional and complete. Whether the project is vinyl, film, or mounted signage, the goal is the same: a polished result that represents your business well.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Step 6</span>
    <h2 class="section-title">Final Review</h2>
    <div class="section-body">
      <p>Before wrapping up, we do a final review to make sure the finished work looks right and the site is left clean. We want the job to feel complete when we leave.</p>
      <p style="margin-top:40px;">Clear communication. Careful prep. Clean finish. That is how we approach every project.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Request a Quote</a></p>
    </div>
  </div>
</section>
"""


def service_area_content():
    return """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Service Area</h1>
    <p>High Country Finish & Repair Co. serves businesses throughout Denver, Arvada, and surrounding Front Range communities. We provide professional installation for vinyl graphics, wall graphics, window film, lobby signs, building signs, and custom branded environments.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Coverage</span>
    <h2 class="section-title">Areas We Commonly Serve</h2>
    <div class="section-body">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;margin-top:32px;">
        <div style="color:var(--text);">Denver</div>
        <div style="color:var(--text);">Arvada</div>
        <div style="color:var(--text);">Lakewood</div>
        <div style="color:var(--text);">Wheat Ridge</div>
        <div style="color:var(--text);">Westminster</div>
        <div style="color:var(--text);">Thornton</div>
        <div style="color:var(--text);">Broomfield</div>
        <div style="color:var(--text);">Littleton</div>
        <div style="color:var(--text);">Englewood</div>
        <div style="color:var(--text);">Golden</div>
        <div style="color:var(--text);">Aurora</div>
        <div style="color:var(--text);">Castle Rock</div>
        <div style="color:var(--text);">Boulder</div>
      </div>
    </div>
    <div class="image-feature" style="margin-top:60px;">
      <img src="/images/service-area-map.jpg" alt="Front Range service area map — Denver metro and surrounding communities" loading="lazy"/>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Commercial Installation</span>
    <h2 class="section-title">Commercial Installation Across the Front Range</h2>
    <div class="section-body">
      <p>We regularly travel for commercial work throughout the Denver metro area and nearby Front Range cities. If your project is outside the immediate area, send us the address and scope. For larger projects, extended travel may be available.</p>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Who We Work With</span>
    <h2 class="section-title">Who We Work With</h2>
    <div class="section-body">
      <p>We work with business owners, office managers, property managers, contractors, print shops, sign shops, and commercial partners who need reliable installation and a polished final result.</p>
      <p style="margin-top:40px;">Not sure if your project falls inside our standard service area? Reach out with your location and we will let you know.</p>
      <p style="margin-top:32px;"><a href="/get-a-quote.html" class="cta-button">Check Availability</a></p>
    </div>
  </div>
</section>
"""


def get_quote_content():
    return """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Get a Quote</h1>
    <p>Need pricing for a sign or graphics installation project? Send us the details and we will review the scope and get back to you with a clear next step.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">What We Quote</span>
    <h2 class="section-title">Services We Provide</h2>
    <div class="services-grid">
      <div class="service-card">
        <h3>Vehicle Wraps</h3>
        <p>Full wraps, partial wraps, and spot graphics</p>
      </div>
      <div class="service-card">
        <h3>Window Film</h3>
        <p>Tint and frosted glass film</p>
      </div>
      <div class="service-card">
        <h3>Wall Graphics</h3>
        <p>Murals and interior branding</p>
      </div>
      <div class="service-card">
        <h3>Lobby Signs</h3>
        <p>Reception signage and dimensional letters</p>
      </div>
      <div class="service-card">
        <h3>Building Signs</h3>
        <p>Exterior graphics and storefront signs</p>
      </div>
      <div class="service-card">
        <h3>Custom Work</h3>
        <p>Specialty installation projects</p>
      </div>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">What to Include</span>
    <h2 class="section-title">Help Us Quote Your Project Accurately</h2>
    <div class="section-body">
      <p>To help us quote your project accurately, send as much of the following as you can:</p>
      <ul style="margin-top:24px;margin-left:20px;color:var(--muted);">
        <li>Service needed</li>
        <li>Approximate dimensions</li>
        <li>Photos of the surface or site</li>
        <li>Project address or city</li>
        <li>Desired timeline</li>
        <li>Whether materials are supplied or install-only is needed</li>
      </ul>
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <span class="section-label">Fast Response</span>
    <h2 class="section-title">Fast, Straightforward Responses</h2>
    <div class="section-body">
      <p>We aim to respond quickly and keep the quoting process simple. If you do not have every detail yet, that is okay. Send what you have and we will help you figure out the next step.</p>
      <p style="margin-top:40px;font-size:18px;">
        <strong>Call:</strong> <a href="tel:3038824656" style="color:var(--gold);">303-882-4656</a><br/>
        <strong>Email:</strong> <a href="mailto:highcountryfinishandrepairco@gmail.com" style="color:var(--gold);">highcountryfinishandrepairco@gmail.com</a>
      </p>
    </div>
  </div>
</section>
"""


# Generate all core pages
def build_core_pages():
    base_path = "C:\\Users\\Spaceship\\.openclaw\\workspace\\vinyl-website"
    
    pages = {
        "about-us.html": {
            "title": "About Us | High Country Finish & Repair Co. Denver Sign & Graphics Installer",
            "desc": "Learn more about High Country Finish & Repair Co., a Denver-area company specializing in commercial vinyl graphics, wall graphics, window film, and sign installation.",
            "content": about_us_content(),
            "current": "about-us"
        },
        "our-process.html": {
            "title": "Our Process | High Country Finish & Repair Co. Denver Install Process",
            "desc": "See how High Country Finish & Repair Co. handles sign and graphics installation from review and quote through scheduling, installation, and final walkthrough.",
            "content": our_process_content(),
            "current": "our-process"
        },
        "service-area.html": {
            "title": "Service Area | Denver, Arvada & Front Range Sign Installation",
            "desc": "High Country Finish & Repair Co. provides commercial sign, vinyl graphics, wall wrap, and window film installation throughout Denver, Arvada, and nearby Front Range communities.",
            "content": service_area_content(),
            "current": "service-area"
        },
        "get-a-quote.html": {
            "title": "Get a Quote | Denver Sign & Graphics Installation Pricing",
            "desc": "Request a quote for vehicle wraps, spot graphics, wall graphics, window film, lobby signs, building signs, and custom installation work in Denver and the Front Range.",
            "content": get_quote_content(),
            "current": "get-a-quote"
        }
    }
    
    for filename, data in pages.items():
        html = build_html(
            data["title"],
            data["desc"],
            data["content"],
            data["current"]
        )
        filepath = os.path.join(base_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created {filename}")


if __name__ == "__main__":
    build_core_pages()
    print("\nCore pages complete")
