#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build services hub page - main services catalog
"""

def build_services_hub():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Services | Vehicle Wraps, Signs, Window Film & Wall Graphics in Denver</title>
<meta name="description" content="Explore commercial sign and graphics installation services from High Country Finish & Repair Co., including vehicle wraps, spot graphics, window film, wall graphics, lobby signs, and building signs."/>
<meta property="og:title" content="Services | High Country Finish & Repair Co."/>
<meta property="og:description" content="Commercial vinyl graphics, window film, wall graphics, lobby signs, and building sign installation in Denver and the Front Range."/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://highcountryfinish.com/services.html"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="https://highcountryfinish.com/services.html"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
/* ─── RESET & BASE ────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: #0c0c0c;
  color: #f0ece4;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }

/* ─── VARIABLES ───────────────────────────── */
:root {
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
}

/* ─── TYPOGRAPHY ──────────────────────────── */
h1, h2, h3, h4 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.01em;
}
.section-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
  margin-bottom: 16px;
  display: block;
}
.section-title {
  font-size: clamp(32px, 5vw, 52px);
  color: var(--text);
  margin-bottom: 20px;
}
.section-body {
  font-size: 16px;
  color: var(--muted);
  max-width: 580px;
  line-height: 1.75;
}

/* ─── LAYOUT ──────────────────────────────── */
.container {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 40px;
}
section { padding: 100px 0; }
@media(max-width:768px){ section{padding:70px 0;} .container{padding:0 24px;} }

/* ─── GOLD LINE ───────────────────────────── */
.gold-line {
  width: 48px;
  height: 2px;
  background: var(--gold);
  margin-bottom: 24px;
}

/* ─── NAV WITH DROPDOWN ───────────────────── */
nav {
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
}
.nav-brand { font-size: 18px; font-weight: 600; color: var(--gold); }
.nav-links { display: flex; gap: 32px; align-items: center; }
.nav-links > a, .nav-item { 
  font-size: 14px; 
  color: var(--muted); 
  transition: color 0.2s;
  font-weight: 500;
  position: relative;
}
.nav-links > a:hover, .nav-item:hover > a { color: var(--text); }
.nav-links a.active { color: var(--text); }

/* Dropdown */
.nav-item {
  position: relative;
}
.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 16px 0;
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
.nav-dropdown a {
  display: block;
  padding: 10px 20px;
  font-size: 14px;
  color: var(--muted);
  transition: all 0.2s;
}
.nav-dropdown a:hover {
  background: var(--surface2);
  color: var(--text);
  padding-left: 24px;
}

.mobile-toggle { display: none; }

@media(max-width:768px){
  nav { padding: 20px 24px; }
  .nav-links { 
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
    align-items: flex-start;
  }
  .nav-links.open { transform: translateX(0); }
  .nav-dropdown {
    position: static;
    margin-top: 8px;
    opacity: 1;
    visibility: visible;
    transform: none;
    box-shadow: none;
    border: none;
    padding-left: 16px;
    display: none;
  }
  .nav-item.open .nav-dropdown {
    display: block;
  }
  .mobile-toggle {
    display: block;
    width: 28px;
    height: 20px;
    position: relative;
    cursor: pointer;
    z-index: 10001;
  }
  .mobile-toggle span {
    position: absolute;
    width: 100%;
    height: 2px;
    background: var(--gold);
    transition: all 0.3s;
  }
  .mobile-toggle span:nth-child(1) { top: 0; }
  .mobile-toggle span:nth-child(2) { top: 9px; }
  .mobile-toggle span:nth-child(3) { top: 18px; }
  .mobile-toggle.open span:nth-child(1) { transform: rotate(45deg); top: 9px; }
  .mobile-toggle.open span:nth-child(2) { opacity: 0; }
  .mobile-toggle.open span:nth-child(3) { transform: rotate(-45deg); top: 9px; }
}

/* ─── HERO SECTION ────────────────────────── */
.hero {
  padding: 180px 0 120px;
  min-height: 70vh;
  display: flex;
  align-items: center;
}
.hero h1 {
  font-size: clamp(42px, 6vw, 72px);
  margin-bottom: 24px;
  max-width: 800px;
}
.hero p {
  font-size: 18px;
  color: var(--muted);
  max-width: 600px;
  line-height: 1.75;
  margin-bottom: 40px;
}

/* ─── SERVICE GRID ────────────────────────── */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 40px;
  margin-top: 60px;
}
.service-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
}
.service-card:hover {
  border-color: var(--gold-dark);
  transform: translateY(-4px);
}
.service-card-image {
  width: 100%;
  height: 240px;
  object-fit: cover;
}
.service-card-content {
  padding: 32px;
}
.service-card h3 {
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--text);
}
.service-card p {
  font-size: 15px;
  color: var(--muted);
  line-height: 1.7;
  margin-bottom: 16px;
}
.service-card a {
  display: inline-block;
  color: var(--gold);
  font-size: 14px;
  font-weight: 600;
  transition: color 0.2s;
}
.service-card a:hover {
  color: var(--gold-light);
}

/* ─── CTA SECTION ─────────────────────────── */
.cta-section {
  background: var(--surface);
  border-top: 1px solid var(--border);
  text-align: center;
}
.cta-button {
  display: inline-block;
  padding: 16px 32px;
  background: var(--gold);
  color: var(--black);
  font-weight: 600;
  font-size: 14px;
  border-radius: 2px;
  transition: all 0.2s;
  border: 1px solid var(--gold);
}
.cta-button:hover {
  background: var(--gold-light);
  border-color: var(--gold-light);
}

/* ─── FOOTER ──────────────────────────────── */
footer {
  background: var(--black);
  border-top: 1px solid var(--border);
  padding: 80px 0 40px;
}
.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 48px;
  margin-bottom: 60px;
}
.footer-col h4 {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--gold);
  margin-bottom: 20px;
}
.footer-col h4 a {
  color: var(--gold);
  transition: color 0.2s;
}
.footer-col h4 a:hover {
  color: var(--gold-light);
}
.footer-col a {
  display: block;
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 12px;
  transition: color 0.2s;
}
.footer-col a:hover {
  color: var(--text);
}
.footer-bottom {
  padding-top: 40px;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 13px;
  color: var(--muted);
}
</style>
</head>
<body>

<nav>
  <div class="nav-brand">HIGH COUNTRY FINISH</div>
  <div class="nav-links" id="navLinks">
    <a href="/">Home</a>
    <div class="nav-item">
      <a href="/services.html" class="active">Services</a>
      <div class="nav-dropdown">
        <a href="/services/vehicle-wraps.html">Vehicle Wraps</a>
        <a href="/services/spot-graphics.html">Spot Graphics</a>
        <a href="/services/window-tint.html">Window Tint</a>
        <a href="/services/window-frosting.html">Window Frosting</a>
        <a href="/services/wall-graphics.html">Wall Graphics</a>
        <a href="/services/lobby-signs.html">Lobby Signs</a>
        <a href="/services/building-signs.html">Building Signs</a>
        <a href="/services/custom-work.html">Custom Work</a>
      </div>
    </div>
    <a href="/portfolio.html">Portfolio</a>
    <div class="nav-item">
      <a href="/about-us.html">Company</a>
      <div class="nav-dropdown">
        <a href="/about-us.html">About Us</a>
        <a href="/our-process.html">Our Process</a>
        <a href="/service-area.html">Service Area</a>
      </div>
    </div>
    <a href="/blog.html">Blog</a>
    <a href="/get-a-quote.html">Get a Quote</a>
  </div>
  <div class="mobile-toggle" id="mobileToggle">
    <span></span>
    <span></span>
    <span></span>
  </div>
</nav>

<section class="hero">
  <div class="container">
    <div class="gold-line"></div>
    <h1>Services</h1>
    <p>We provide clean, professional installation for commercial vinyl graphics, signage, and window film across Denver and the Front Range. Explore our core services below.</p>
  </div>
</section>

<section style="padding:100px 0;background:var(--surface);">
  <div class="container">
    <div class="services-grid">
      
      <div class="service-card">
        <img src="/images/957-party-vehicle-wrap.jpg" alt="957 The Party vehicle wrap Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Vehicle Wraps</h3>
          <p>Full wraps, partial wraps, and fleet branding installed with clean lines and a professional finish.</p>
          <a href="/services/vehicle-wraps.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/cybertruck-side.jpg" alt="Spot graphics installation Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Spot Graphics</h3>
          <p>Door logos, vehicle lettering, window decals, branded cut vinyl, and simple graphic packages that make a strong impression without a full wrap.</p>
          <a href="/services/spot-graphics.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/directory-sign.jpg" alt="Window tint installation Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Window Tint</h3>
          <p>Window tint installation for privacy, glare control, UV reduction, and a more polished appearance.</p>
          <a href="/services/window-tint.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/novara-frosted-glass.jpg" alt="Frosted window film Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Window Frosting</h3>
          <p>Frosted film, privacy bands, and decorative glass graphics for offices, storefronts, and interior partitions.</p>
          <a href="/services/window-frosting.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/elite-brands-mural-wide2.jpg" alt="Wall graphics and murals Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Wall Graphics</h3>
          <p>Branded wall graphics, murals, and full-wall wraps for offices, retail, and hospitality spaces.</p>
          <a href="/services/wall-graphics.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/kpa-lobby-sign.jpg" alt="Lobby signs Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Lobby Signs</h3>
          <p>Reception signs, stand-off signs, acrylic panels, and dimensional letters installed with clean spacing and balance.</p>
          <a href="/services/lobby-signs.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/buffalo-building-sign.jpg" alt="Building signs Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Building Signs</h3>
          <p>Exterior business signs, mounted panels, storefront signage, and branded exterior elements.</p>
          <a href="/services/building-signs.html">Learn More →</a>
        </div>
      </div>

      <div class="service-card">
        <img src="/images/iheart-elevator-wrap.jpg" alt="Custom sign installation Denver" class="service-card-image"/>
        <div class="service-card-content">
          <h3>Custom Work</h3>
          <p>Specialty sign and graphics projects that don't fit a standard category.</p>
          <a href="/services/custom-work.html">Learn More →</a>
        </div>
      </div>

    </div>
  </div>
</section>

<section class="cta-section">
  <div class="container">
    <span class="section-label">Ready to Start?</span>
    <h2 class="section-title">Need a Quote for Your Project?</h2>
    <p class="section-body" style="max-width:100%;text-align:center;margin:0 auto 40px;">Whether you need vehicle graphics, window film, wall graphics, lobby signage, or a custom install, we will review your project and get back to you quickly with a clear next step.</p>
    <a href="/get-a-quote.html" class="cta-button">Request a Free Quote</a>
  </div>
</section>

<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <h4><a href="/services.html">Services</a></h4>
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
        <h4><a href="/about-us.html">Company</a></h4>
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
toggle.addEventListener('click', () => {
  toggle.classList.toggle('open');
  navLinks.classList.toggle('open');
  document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
});

// Close menu when clicking a link
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    toggle.classList.remove('open');
    navLinks.classList.remove('open');
    document.body.style.overflow = '';
  });
});

// Mobile dropdown toggles
if (window.innerWidth <= 768) {
  document.querySelectorAll('.nav-item > a').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      e.target.parentElement.classList.toggle('open');
    });
  });
}
</script>

</body>
</html>"""
    
    with open("C:\\Users\\Spaceship\\.openclaw\\workspace\\vinyl-website\\services.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Services hub page created")

if __name__ == "__main__":
    build_services_hub()
