#!/usr/bin/env python3
# patch_gallery.py — Apply 3 changes to index.html

import re

INPUT  = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'
OUTPUT = r'C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html'

with open(INPUT, encoding='utf-8') as f:
    html = f.read()

# ────────────────────────────────────────────────────────────────────
# CHANGE 1: Replace the entire <!-- PORTFOLIO --> section
# (from the <!-- PORTFOLIO --> comment through the closing </section>
#  that ends id="portfolio", then keep the <script> for openGroupModal
#  but regenerate it cleanly after the new section)
# ────────────────────────────────────────────────────────────────────

NEW_PORTFOLIO_SECTION = r"""<!-- PORTFOLIO -->
<style>
/* ── Hero gallery grid (5-photo) ─────────────────────────────────── */
.hero-gallery-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 2.5rem;
}
@media(max-width: 1100px) {
  .hero-gallery-grid { grid-template-columns: repeat(3, 1fr); }
}
@media(max-width: 768px) {
  .hero-gallery-grid { grid-template-columns: repeat(2, 1fr); }
}
@media(max-width: 480px) {
  .hero-gallery-grid { grid-template-columns: 1fr; }
}
.hero-gallery-item {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border-radius: 4px;
  background: var(--surface2);
}
.hero-gallery-item img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 0.6s ease;
}
.hero-gallery-item:hover img { transform: scale(1.04); }
.hero-gallery-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.82) 0%, transparent 55%);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  padding: 16px;
}
.hero-gallery-item:hover .hero-gallery-overlay { opacity: 1; }
.hero-gallery-caption {
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  letter-spacing: 0.4px;
  line-height: 1.4;
}
/* View Full Portfolio button */
.btn-portfolio {
  display: inline-block;
  border: 1px solid var(--gold);
  color: var(--gold);
  background: var(--black);
  padding: 14px 36px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  border-radius: 2px;
  transition: background 0.2s, color 0.2s;
  text-decoration: none;
}
.btn-portfolio:hover {
  background: var(--gold);
  color: #000;
}
</style>

<section id="portfolio">
  <div class="container">

    <div class="section-header" style="text-align:center;margin-bottom:3rem;">
      <span class="section-label reveal">Our Work</span>
      <h2 class="section-title reveal">Denver Sign &amp; Graphics<br/>Portfolio</h2>
      <p class="reveal" style="color:var(--muted);max-width:540px;margin:0 auto 2rem;">A sample of our recent commercial installs across Denver and the Front Range.</p>
    </div>

    <div class="hero-gallery-grid reveal">

      <div class="hero-gallery-item" onclick="openGroupModal(this)">
        <img src="images/peak-elevator-lobby-sign.jpg"
             alt="lobby sign installation Denver - PEAK Elevator Performance Group acrylic panel"
             loading="lazy"/>
        <div class="hero-gallery-overlay">
          <span class="hero-gallery-caption">PEAK Elevator Performance Group</span>
        </div>
      </div>

      <div class="hero-gallery-item" onclick="openGroupModal(this)">
        <img src="images/novara-frosted-glass.jpg"
             alt="office reception signage and frosted glass installation Denver - Novara"
             loading="lazy"/>
        <div class="hero-gallery-overlay">
          <span class="hero-gallery-caption">Novara &#8212; Reception &amp; Frosted Glass</span>
        </div>
      </div>

      <div class="hero-gallery-item" onclick="openGroupModal(this)">
        <img src="images/omeara-room-wrap.jpg"
             alt="full room wrap installation Denver - vinyl wall and ceiling graphics"
             loading="lazy"/>
        <div class="hero-gallery-overlay">
          <span class="hero-gallery-caption">O&#8217;Meara Ford / KBPI &#8212; Full Room Wrap</span>
        </div>
      </div>

      <div class="hero-gallery-item" onclick="openGroupModal(this)">
        <img src="images/buffalo-restaurant-exterior.jpg"
             alt="exterior storefront sign installation Front Range Colorado - The Buffalo Restaurant"
             loading="lazy"/>
        <div class="hero-gallery-overlay">
          <span class="hero-gallery-caption">The Buffalo Restaurant &amp; Bar</span>
        </div>
      </div>

      <div class="hero-gallery-item" onclick="openGroupModal(this)">
        <img src="images/cybertruck-side.jpg"
             alt="vehicle wrap installation Denver - Cybertruck Black Rock vinyl lettering side view"
             loading="lazy"/>
        <div class="hero-gallery-overlay">
          <span class="hero-gallery-caption">Cybertruck &#8212; Black Rock Vinyl Lettering</span>
        </div>
      </div>

    </div>

    <div style="text-align:center;" class="reveal">
      <a href="#portfolio-full" class="btn-portfolio">View Full Portfolio</a>
    </div>

  </div>
</section>

<script>
function openGroupModal(item) {
  var img = item.querySelector('img');
  if (!img) return;
  document.getElementById('modal-img').src = img.src;
  document.getElementById('modal-img').alt = img.alt;
  document.getElementById('modal').classList.add('open');
}
</script>
"""

# Match from <!-- PORTFOLIO --> through the closing </section> of id="portfolio",
# plus the inline <script> block with openGroupModal that follows immediately.
# Strategy: find the <!-- PORTFOLIO --> comment, then find the next
# </section> after id="portfolio", then consume the trailing <script>…</script>.
# We'll use a regex that is robust enough for this known structure.

portfolio_pattern = re.compile(
    r'<!-- PORTFOLIO -->.*?</section>\s*\n\s*<script>\s*\nfunction openGroupModal.*?</script>',
    re.DOTALL
)

if portfolio_pattern.search(html):
    html = portfolio_pattern.sub(NEW_PORTFOLIO_SECTION.strip(), html, count=1)
    print('✓ Change 1 applied: portfolio section replaced with 5-photo hero grid')
else:
    print('✗ Change 1 FAILED: could not find portfolio section pattern')


# ────────────────────────────────────────────────────────────────────
# CHANGE 2: Remove pf-section-header from #portfolio-full
# ────────────────────────────────────────────────────────────────────

section_header_pattern = re.compile(
    r'\s*<div class="pf-section-header reveal">.*?</div>\s*\n',
    re.DOTALL
)

if section_header_pattern.search(html):
    html = section_header_pattern.sub('\n', html, count=1)
    print('✓ Change 2 applied: pf-section-header removed from #portfolio-full')
else:
    print('✗ Change 2 FAILED: could not find pf-section-header block')


# ────────────────────────────────────────────────────────────────────
# CHANGE 3: Add gold divider line before <section id="portfolio-full">
# ────────────────────────────────────────────────────────────────────

DIVIDER = '''<hr style="border:none;border-top:1px solid var(--gold);opacity:0.35;margin:0;" aria-hidden="true"/>
'''

if '<section id="portfolio-full">' in html:
    html = html.replace(
        '<section id="portfolio-full">',
        DIVIDER + '<section id="portfolio-full">',
        1
    )
    print('✓ Change 3 applied: gold divider line added before #portfolio-full')
else:
    print('✗ Change 3 FAILED: could not find <section id="portfolio-full">')


# ────────────────────────────────────────────────────────────────────
# Write output
# ────────────────────────────────────────────────────────────────────
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone — index.html written.')
