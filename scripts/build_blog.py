#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build blog pages for High Country Finish website
"""

import os

def build_html(title, meta_desc, content_html, current_page="blog"):
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
<meta property="og:type" content="article"/>
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

/* ─── ARTICLE STYLES ──────────────────────── */
article {{
  max-width: 720px;
  margin: 0 auto;
}}
article h2 {{
  font-size: clamp(28px, 4vw, 42px);
  margin: 60px 0 20px;
  color: var(--text);
}}
article p {{
  font-size: 17px;
  line-height: 1.8;
  color: var(--muted);
  margin-bottom: 24px;
}}

/* ─── BLOG INDEX GRID ─────────────────────── */
.blog-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 40px;
  margin-top: 60px;
}}
.blog-card {{
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 32px;
  transition: border-color 0.2s;
}}
.blog-card:hover {{
  border-color: var(--gold-dark);
}}
.blog-card h3 {{
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--text);
}}
.blog-card p {{
  font-size: 15px;
  color: var(--muted);
  line-height: 1.7;
  margin-bottom: 16px;
}}
.blog-card a {{
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
            <a href="/">Home</a>
            <a href="/services/vehicle-wraps.html">Services</a>
            <a href="/portfolio.html">Portfolio</a>
            <a href="/our-process.html">Our Process</a>
            <a href="/about-us.html">About Us</a>
            <a href="/service-area.html">Service Area</a>
            <a href="/get-a-quote.html">Get a Quote</a>
            <a href="/blog.html" class="active">Blog</a>
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


BLOG_PAGES = {
    "blog.html": {
        "title": "Blog | Sign, Window Film & Graphics Tips from High Country Finish & Repair Co.",
        "desc": "Read tips and guides on vehicle wraps, window frosting, wall graphics, lobby signs, and building signage for Denver businesses.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Blog</h1>
    <p>Practical tips, comparisons, and project guidance for business owners, office managers, and commercial clients planning sign, graphics, and window film projects in Denver and the Front Range.</p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <div class="blog-grid">
      <div class="blog-card">
        <h3>How Long Do Vehicle Wraps Last in Colorado?</h3>
        <p>Learn how long vehicle wraps typically last in Colorado, what affects lifespan, and how to keep your wrap looking clean and professional.</p>
        <a href="/blog/how-long-do-vehicle-wraps-last-in-colorado.html">Read More →</a>
      </div>
      <div class="blog-card">
        <h3>Frosted Glass vs. Window Tint for Offices: What's Better?</h3>
        <p>Compare frosted glass film and window tint for offices. Learn which option is better for privacy, glare control, appearance, and day-to-day function.</p>
        <a href="/blog/frosted-glass-vs-window-tint-for-offices.html">Read More →</a>
      </div>
      <div class="blog-card">
        <h3>What Makes a Lobby Sign Look Expensive?</h3>
        <p>Learn what separates an average lobby sign from one that looks premium, polished, and professionally installed.</p>
        <a href="/blog/what-makes-a-lobby-sign-look-expensive.html">Read More →</a>
      </div>
      <div class="blog-card">
        <h3>How to Prepare a Wall for Wall Graphics and Murals</h3>
        <p>Find out how to prepare painted walls for wall graphics and murals so vinyl installs cleanly and looks its best.</p>
        <a href="/blog/how-to-prepare-a-wall-for-wall-graphics-and-murals.html">Read More →</a>
      </div>
      <div class="blog-card">
        <h3>Choosing the Right Building Sign for Your Denver Business</h3>
        <p>Learn how to choose the right building sign for your business based on visibility, location, branding goals, and property conditions.</p>
        <a href="/blog/choosing-the-right-building-sign-for-your-denver-business.html">Read More →</a>
      </div>
    </div>
  </div>
</section>
""",
        "path": ""
    },
    
    "how-long-do-vehicle-wraps-last-in-colorado.html": {
        "title": "How Long Do Vehicle Wraps Last in Colorado?",
        "desc": "Learn how long vehicle wraps typically last in Colorado, what affects lifespan, and how to keep your wrap looking clean and professional.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>How Long Do Vehicle Wraps Last in Colorado?</h1>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <article>
      <p>Vehicle wraps are one of the best ways to turn a company vehicle into a moving advertisement, but one of the first questions clients ask is how long the wrap will last. The honest answer is that lifespan depends on the material, the installation quality, the amount of sun exposure, and how the vehicle is cared for over time.</p>

      <p>In Colorado, sun exposure is a big factor. Higher elevation and strong UV can be hard on exterior finishes, including vinyl. A professionally installed wrap using quality material will usually hold up for years, but the exact lifespan can vary depending on whether the vehicle is parked outside full time, how often it is washed, and whether the wrap covers high-wear areas.</p>

      <h2>What Affects Wrap Lifespan?</h2>
      <p>The biggest factors are material quality, install quality, environmental exposure, and maintenance. Cheap vinyl usually fails sooner. Poor prep and poor installation can lead to lifting edges, shrinking, or early wear. Constant sun exposure, snow, ice, and road grime also add stress over time.</p>

      <h2>Why Installation Quality Matters</h2>
      <p>Even great material can underperform if it is installed poorly. Clean prep, proper adhesion, good finishing technique, and attention to edges all play a role in how the wrap holds up. A wrap should not just look good on day one. It should still look clean after months of driving and weather.</p>

      <h2>How to Make a Wrap Last Longer</h2>
      <p>Regular hand washing, avoiding harsh chemicals, and keeping the vehicle clean all help. Covered parking also extends the life of the wrap. If a section gets damaged, addressing it early can prevent a small issue from turning into a larger one.</p>

      <h2>A Smart Branding Investment</h2>
      <p>For many businesses, a wrap is one of the most cost-effective forms of ongoing advertising. It works every time the vehicle is on the road, parked at a jobsite, or sitting in front of a client's building.</p>

      <p>If you are thinking about wrapping a work truck, van, or fleet vehicle, the best place to start is with quality material and a clean installation. That combination gives you the best chance at a wrap that keeps looking professional for the long haul.</p>

      <p style="margin-top:60px;"><a href="/get-a-quote.html" class="cta-button">Get a Vehicle Wrap Quote</a></p>
    </article>
  </div>
</section>
""",
        "path": "blog/"
    },
    
    "frosted-glass-vs-window-tint-for-offices.html": {
        "title": "Frosted Glass vs. Window Tint for Offices: What's Better?",
        "desc": "Compare frosted glass film and window tint for offices. Learn which option is better for privacy, glare control, appearance, and day-to-day function.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Frosted Glass vs. Window Tint for Offices: What's Better?</h1>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <article>
      <p>Office glass can look clean and modern, but it also creates practical challenges. Some spaces need more privacy. Others deal with harsh sunlight and glare. Two of the most common solutions are frosted glass film and window tint. The right choice depends on what problem you are trying to solve.</p>

      <h2>When Frosted Glass Makes More Sense</h2>
      <p>Frosted film is usually the better option when privacy is the main goal. It works well on conference rooms, office entry glass, waiting rooms, and interior partitions where you still want light to pass through. Frosting also adds a clean, professional look that feels intentional in office settings.</p>

      <h2>When Window Tint Makes More Sense</h2>
      <p>Window tint is usually the better option when the main issue is glare, heat, or UV exposure. It can help make offices more comfortable while also improving privacy to some degree, depending on the film. Tint is especially useful on exterior-facing glass that gets strong direct sun.</p>

      <h2>Can You Combine Them?</h2>
      <p>Yes. In some office environments, tint and frosting can work together. For example, tint may be used on exterior glass for solar control, while frosting is used on interior conference room glass for privacy and design.</p>

      <h2>Appearance Matters Too</h2>
      <p>Frosted film tends to feel more architectural and design-forward inside an office. Window tint tends to feel more performance-driven. Both can look excellent when installed cleanly. The key is choosing the right product for the space and making sure the installation is sharp.</p>

      <h2>Which One Is Right for Your Office?</h2>
      <p>If you need privacy, start with frosting. If you need glare and heat control, start with tint. If you need both, a mixed approach may be the best solution.</p>

      <p>The right answer comes down to how the space is used. A quick review of the glass, the lighting, and the function of the room can usually make the decision much easier.</p>

      <p style="margin-top:60px;"><a href="/get-a-quote.html" class="cta-button">Get a Quote</a></p>
    </article>
  </div>
</section>
""",
        "path": "blog/"
    },
    
    "what-makes-a-lobby-sign-look-expensive.html": {
        "title": "What Makes a Lobby Sign Look Expensive?",
        "desc": "Learn what separates an average lobby sign from one that looks premium, polished, and professionally installed.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>What Makes a Lobby Sign Look Expensive?</h1>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <article>
      <p>A lobby sign does not have to be oversized or flashy to make an impression. In many cases, the signs that look the most expensive are the ones that feel balanced, clean, and intentional. The difference usually comes down to design choices, materials, spacing, and installation quality.</p>

      <h2>Material Choice Sets the Tone</h2>
      <p>Acrylic, brushed metal, dimensional lettering, stand-off hardware, and layered logo elements can all elevate the look of a sign. Even simple materials can look premium when they are proportioned well and installed correctly.</p>

      <h2>Good Placement Changes Everything</h2>
      <p>One of the biggest mistakes in lobby signage is poor placement. A beautiful sign can look wrong if it is too high, too low, off center, or out of scale with the wall. A premium-looking sign feels balanced in the space.</p>

      <h2>Spacing and Alignment Matter</h2>
      <p>Crisp letter spacing, clean level lines, and even stand-off spacing all contribute to a more polished result. These details may sound small, but they are often what people notice without realizing it.</p>

      <h2>The Wall Behind the Sign Matters Too</h2>
      <p>The surrounding environment affects how the sign reads. A textured feature wall, clean paint, good lighting, and a strong reception area all help a sign feel more intentional and high-end.</p>

      <h2>Installation Is What Finishes the Job</h2>
      <p>Even a well-designed sign can lose its impact if the installation is rushed. Uneven placement, sloppy mounting, or poor layout immediately lower the perceived quality. Clean installation is what turns a sign into a finished branding element.</p>

      <p>If you want a lobby sign to look expensive, focus on balance, materials, and install quality. Those are the pieces that create a strong first impression the moment someone walks through the door.</p>

      <p style="margin-top:60px;"><a href="/services/lobby-signs.html" class="cta-button">Learn More About Lobby Signs</a></p>
    </article>
  </div>
</section>
""",
        "path": "blog/"
    },
    
    "how-to-prepare-a-wall-for-wall-graphics-and-murals.html": {
        "title": "How to Prepare a Wall for Wall Graphics and Murals",
        "desc": "Find out how to prepare painted walls for wall graphics and murals so vinyl installs cleanly and looks its best.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>How to Prepare a Wall for Wall Graphics and Murals</h1>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <article>
      <p>A great wall graphic starts before the vinyl ever touches the wall. Surface condition has a major impact on how well graphics install, how clean they look, and how well they hold over time. If the wall is not ready, even a good design and a good installer have less to work with.</p>

      <h2>Start with a Clean, Dry Surface</h2>
      <p>Walls should be free of dust, grease, residue, and loose debris. Freshly painted walls also need adequate cure time before graphics are installed. Rushing that step can create adhesion issues and lead to problems later.</p>

      <h2>Wall Texture Matters</h2>
      <p>The smoother the wall, the cleaner the finished graphic usually looks. Light texture may be workable depending on the material, but heavy texture can affect both appearance and adhesion. If the wall is highly textured, it is worth reviewing the surface before final production.</p>

      <h2>Repair Damage Before Install</h2>
      <p>Dents, flaking paint, patched areas, and rough spots should be addressed before installation. Wall graphics tend to highlight imperfections rather than hide them, especially on large open areas and high-contrast designs.</p>

      <h2>Why Paint Quality Matters</h2>
      <p>Low-quality paint, chalky surfaces, or poorly bonded old paint can create issues. A stable, cured wall with a clean finish gives the best foundation for wall vinyl.</p>

      <h2>A Better Wall Creates a Better Final Result</h2>
      <p>When the surface is ready, the install goes more smoothly and the finished product looks much more professional. That is especially important on murals, logo walls, and feature graphics where presentation matters.</p>

      <p>If you are planning a wall graphic project, it is worth reviewing the surface early. Good prep protects the finished result.</p>

      <p style="margin-top:60px;"><a href="/services/wall-graphics.html" class="cta-button">Explore Wall Graphics</a></p>
    </article>
  </div>
</section>
""",
        "path": "blog/"
    },
    
    "choosing-the-right-building-sign-for-your-denver-business.html": {
        "title": "Choosing the Right Building Sign for Your Denver Business",
        "desc": "Learn how to choose the right building sign for your business based on visibility, location, branding goals, and property conditions.",
        "content": """
<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Choosing the Right Building Sign for Your Denver Business</h1>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <article>
      <p>A building sign does more than mark a location. It shapes first impressions, improves visibility, and helps customers recognize your business before they ever step inside. The right sign depends on your building, your brand, and how people approach the property.</p>

      <h2>Start with Visibility</h2>
      <p>Think about how the sign will be seen. Is it viewed from a parking lot, from the street, or mainly on foot? Distance and angle matter. A sign that looks good close up may not read well from farther away.</p>

      <h2>Match the Sign to the Property</h2>
      <p>Storefronts, office buildings, and multi-tenant properties all have different conditions and restrictions. The right sign should feel like it belongs on the building while still standing out enough to do its job.</p>

      <h2>Think About Brand Presentation</h2>
      <p>Your exterior sign is part of your brand. Clean, simple signage often performs better than something overly complicated. The best signs usually balance visibility, readability, and a professional appearance.</p>

      <h2>Installation Quality Still Matters</h2>
      <p>A strong sign can lose impact fast if it is installed crooked, mounted poorly, or placed without consideration for the building. Exterior signage is highly visible, which means install quality matters even more.</p>

      <h2>Choose for the Long Term</h2>
      <p>A good building sign should still feel right months and years later. It should fit the space, support the brand, and help customers find you without effort.</p>

      <p>If you are planning exterior signage for your business, the best place to start is by looking at the building, how the sign will be viewed, and what kind of first impression you want to make.</p>

      <p style="margin-top:60px;"><a href="/services/building-signs.html" class="cta-button">View Building Sign Services</a></p>
    </article>
  </div>
</section>
""",
        "path": "blog/"
    }
}


def build_blog_pages():
    base_path = "C:\\Users\\Spaceship\\.openclaw\\workspace\\vinyl-website"
    
    for filename, data in BLOG_PAGES.items():
        html = build_html(
            data["title"],
            data["desc"],
            data["content"]
        )
        
        # Determine full path
        if data["path"]:
            filepath = os.path.join(base_path, data["path"], filename)
        else:
            filepath = os.path.join(base_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created {filename}")


if __name__ == "__main__":
    build_blog_pages()
    print("\nBlog pages complete")
