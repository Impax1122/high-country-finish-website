#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update homepage with new navigation and service links
Maintaining dark luxury aesthetic
"""

from pathlib import Path

index_path = Path("C:/Users/Spaceship/.openclaw/workspace/vinyl-website/index.html")

# Read current index
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update nav to include new pages
old_nav = """  <div class="nav-links" id="navLinks">
    <a href="/" class="active">Home</a>
    <a href="/portfolio.html">Portfolio</a>
    <a href="tel:3038824656" class="mobile-only">Call Now</a>
  </div>"""

new_nav = """  <div class="nav-links" id="navLinks">
    <a href="/" class="active">Home</a>
    <a href="/services/vehicle-wraps.html">Services</a>
    <a href="/portfolio.html">Portfolio</a>
    <a href="/our-process.html">Our Process</a>
    <a href="/about-us.html">About Us</a>
    <a href="/service-area.html">Service Area</a>
    <a href="/get-a-quote.html">Get a Quote</a>
    <a href="/blog.html">Blog</a>
  </div>"""

html = html.replace(old_nav, new_nav)

# Update footer to include all new pages
old_footer_content = """    <div class="footer-grid">
      <div class="footer-col">
        <h4>Contact</h4>
        <a href="tel:3038824656">303-882-4656</a>
        <a href="mailto:highcountryfinishandrepairco@gmail.com">Email Us</a>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="/portfolio.html">View Portfolio</a>
        <a href="#services">Our Services</a>
      </div>
      <div class="footer-col">
        <h4>Location</h4>
        <p style="margin:0;font-size:14px;color:var(--muted);line-height:1.6;">Serving Denver, Arvada & the Front Range</p>
      </div>
    </div>"""

new_footer_content = """    <div class="footer-grid">
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
    </div>"""

html = html.replace(old_footer_content, new_footer_content)

# Write updated file
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Homepage updated with new navigation and footer")
