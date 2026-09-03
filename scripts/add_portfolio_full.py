# -*- coding: utf-8 -*-
"""
add_portfolio_full.py
Inserts #portfolio-full section after the existing #portfolio section,
and adds a "Full Portfolio" nav link.
"""

import re

FILE = r"C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ─── 1. BUILD THE NEW SECTION ────────────────────────────────────────────────

new_section = r"""

<!-- PORTFOLIO FULL -->
<style>
/* ── #portfolio-full scoped styles ─────────────────────────────────────────── */
#portfolio-full {
  background: #0c0c0c;
  padding: 100px 0;
}
#portfolio-full .pf-section-header {
  text-align: center;
  margin-bottom: 72px;
}
#portfolio-full .pf-section-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: #C9A84C;
  margin-bottom: 16px;
  display: block;
}
#portfolio-full .pf-section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 600;
  color: #f0ece4;
  line-height: 1.15;
  margin-bottom: 16px;
}
#portfolio-full .pf-section-sub {
  font-size: 16px;
  color: #888880;
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.75;
}
#portfolio-full .pf-gold-line {
  width: 48px;
  height: 2px;
  background: #C9A84C;
  margin: 0 auto 28px;
}
/* Project cards */
#portfolio-full .pf-project {
  margin-bottom: 64px;
  border: 1px solid #2a2a2a;
  border-radius: 4px;
  overflow: hidden;
  background: #141414;
}
#portfolio-full .pf-project-header {
  padding: 20px 28px;
  border-bottom: 1px solid #2a2a2a;
  display: flex;
  align-items: center;
  gap: 14px;
}
#portfolio-full .pf-project-header::before {
  content: '';
  display: inline-block;
  width: 32px;
  height: 2px;
  background: #C9A84C;
  flex-shrink: 0;
}
#portfolio-full .pf-project-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: #C9A84C;
  letter-spacing: 0.03em;
}
#portfolio-full .pf-photos-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  background: #2a2a2a;
}
#portfolio-full .pf-photos-grid.cols-2 {
  grid-template-columns: repeat(2, 1fr);
}
#portfolio-full .pf-photos-grid.cols-1 {
  grid-template-columns: 1fr;
}
@media(max-width: 900px) {
  #portfolio-full .pf-photos-grid,
  #portfolio-full .pf-photos-grid.cols-2 {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media(max-width: 600px) {
  #portfolio-full .pf-photos-grid,
  #portfolio-full .pf-photos-grid.cols-2,
  #portfolio-full .pf-photos-grid.cols-1 {
    grid-template-columns: 1fr;
  }
  #portfolio-full { padding: 70px 0; }
}
#portfolio-full .pf-photo-cell {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  background: #1c1c1c;
  display: flex;
  flex-direction: column;
}
#portfolio-full .pf-photo-cell img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 0.6s ease;
}
#portfolio-full .pf-photo-cell:hover img {
  transform: scale(1.04);
}
#portfolio-full .pf-photo-overlay {
  position: absolute;
  inset: 0 0 auto 0;
  top: 0; left: 0; right: 0; bottom: 40px;
  background: linear-gradient(to top, rgba(0,0,0,0.82) 0%, transparent 55%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}
#portfolio-full .pf-photo-cell:hover .pf-photo-overlay {
  opacity: 1;
}
#portfolio-full .pf-caption {
  padding: 10px 14px;
  font-size: 12px;
  color: #888880;
  letter-spacing: 0.4px;
  background: #141414;
  border-top: 1px solid #1c1c1c;
  line-height: 1.4;
  flex-shrink: 0;
}
/* CTA at bottom */
#portfolio-full .pf-cta {
  text-align: center;
  margin-top: 32px;
}
</style>

<section id="portfolio-full">
  <div class="container">

    <div class="pf-section-header reveal">
      <span class="pf-section-label">Full Portfolio</span>
      <div class="pf-gold-line"></div>
      <h2 class="pf-section-title">Every Project, Organized by Job</h2>
      <p class="pf-section-sub">Every commercial install we&rsquo;ve documented — grouped by client and ordered by impact.</p>
    </div>

    <!-- ── 1. PEAK Elevator Performance Group ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">PEAK Elevator Performance Group</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/peak-elevator-lobby-sign.jpg"
               alt="PEAK Elevator Performance Group lobby acrylic sign installation Denver CO — large dimensional panel in reception area"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Acrylic Sign &mdash; Denver, CO</div>
        </div>
      </div>
    </div>

    <!-- ── 2. Novara ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Novara</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/novara-frosted-glass.jpg"
               alt="Novara office reception sign and decorative frosted glass panel installation Denver"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Reception &amp; Frosted Glass Panel</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/novara-lobby.jpg"
               alt="Novara lobby wall lettering vinyl graphics Denver office interior signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Wall Lettering</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/novara-reception.jpg"
               alt="Novara reception desk signage installation Denver commercial vinyl graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Reception Desk Signage</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/novara-waiting-area.jpg"
               alt="Novara waiting area wall graphics Denver office interior vinyl installation"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Waiting Area Graphics</div>
        </div>
      </div>
    </div>

    <!-- ── 3. O'Meara Ford / KBPI ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">O&rsquo;Meara Ford / KBPI</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/omeara-room-wrap.jpg"
               alt="O'Meara Ford KBPI 106.7 full room wall and ceiling wrap installation Denver — branded interior mural"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Full Room Wrap &mdash; Wall &amp; Ceiling</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/omeara-room-wrap-wide.jpg"
               alt="O'Meara Ford KBPI room wrap installation Denver wide angle view — full branded interior"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Room Wrap &mdash; Wide View</div>
        </div>
      </div>
    </div>

    <!-- ── 4. Elite Brands ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Elite Brands</span>
      </div>
      <div class="pf-photos-grid">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/elite-brands-wall-mural.jpg"
               alt="Elite Brands office wall mural installation Denver — large format core values branded graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Office Wall Mural &mdash; Core Values</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/elite-brands-mural-wide2.jpg"
               alt="Elite Brands office wall mural full width view Denver — panoramic branded interior graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Wall Mural &mdash; Full Width View</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/elite-brands-sign-detail.jpg"
               alt="Elite Brands lobby sign detail installation Denver — close-up acrylic reception signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Sign Detail</div>
        </div>
      </div>
    </div>

    <!-- ── 5. Cybertruck — Black Rock ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Cybertruck &mdash; Black Rock</span>
      </div>
      <div class="pf-photos-grid">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/cybertruck-side.jpg"
               alt="Tesla Cybertruck Black Rock vinyl lettering installation side view Denver CO — commercial vehicle graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Vinyl Lettering &mdash; Side</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/cybertruck-front.jpg"
               alt="Tesla Cybertruck Black Rock vinyl lettering front view Denver CO — precision vehicle graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Vinyl Lettering &mdash; Front</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/cybertruck-rear.jpg"
               alt="Tesla Cybertruck Black Rock vinyl lettering rear view Denver CO — full vehicle graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Vinyl Lettering &mdash; Rear</div>
        </div>
      </div>
    </div>

    <!-- ── 6. The Buffalo Restaurant & Bar ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">The Buffalo Restaurant &amp; Bar</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/buffalo-restaurant-exterior.jpg"
               alt="The Buffalo Restaurant and Bar exterior storefront signage installation Front Range Colorado"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Exterior Storefront Signage</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/buffalo-building-sign.jpg"
               alt="The Buffalo Restaurant and Bar building sign installation Colorado — commercial exterior signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Building Sign</div>
        </div>
      </div>
    </div>

    <!-- ── 7. iHeartMedia ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">iHeartMedia</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/iheart-elevator-wrap.jpg"
               alt="iHeartMedia elevator wrap installation Denver — commercial vinyl elevator door graphics broadcast media"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Elevator Wrap Installation</div>
        </div>
      </div>
    </div>

    <!-- ── 8. Children's Museum of Denver ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Children&rsquo;s Museum of Denver</span>
      </div>
      <div class="pf-photos-grid">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/childrens-museum-artstudio.jpg"
               alt="Children's Museum of Denver art studio dimensional letters installation — interior signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Art Studio &mdash; Dimensional Letters</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/childrens-museum-donor.jpg"
               alt="Children's Museum of Denver donor recognition wall installation — vinyl graphics and lettering"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Donor Recognition Wall</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/childrens-museum-donor2.jpg"
               alt="Children's Museum of Denver donor wall detail — close-up vinyl lettering installation"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Donor Wall &mdash; Detail</div>
        </div>
      </div>
    </div>

    <!-- ── 9. 95.7 The Party ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">95.7 The Party</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/957-party-vehicle-wrap.jpg"
               alt="95.7 The Party radio station full vehicle wrap SUV Denver CO — branded fleet graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Full Vehicle Wrap &mdash; SUV</div>
        </div>
      </div>
    </div>

    <!-- ── 10. Glover Masonry ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Glover Masonry</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/glover-masonry-lobby.jpg"
               alt="Glover Masonry lobby acrylic sign wide angle installation Denver — reception area commercial signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Acrylic Sign &mdash; Wide</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/glover-masonry-sign-closeup.jpg"
               alt="Glover Masonry lobby sign close-up detail Denver — dimensional acrylic letter installation"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Sign &mdash; Detail</div>
        </div>
      </div>
    </div>

    <!-- ── 11. GQue BBQ ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">GQue BBQ</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/gque-bbq-mural.jpg"
               alt="GQue BBQ restaurant large format wall mural installation Denver — interior branded graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Large Format Wall Mural</div>
        </div>
      </div>
    </div>

    <!-- ── 12. Gym Wall Mural ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Gym Wall Mural</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/gym-wall-mural.jpg"
               alt="Commercial gym large format wall mural installation Denver — fitness center branded interior graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Large Format Wall Mural</div>
        </div>
      </div>
    </div>

    <!-- ── 13. Trinity Place — 1801 Broadway Denver ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Trinity Place &mdash; 1801 Broadway Denver</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/trinity-place-exterior-sign.jpg"
               alt="Trinity Place 1801 Broadway Denver exterior building sign installation — commercial exterior signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Exterior Building Sign</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/trinity-place-exterior-sign2.jpg"
               alt="Trinity Place 1801 Broadway Denver exterior signage second angle — commercial building graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Exterior Signage &mdash; Second Angle</div>
        </div>
      </div>
    </div>

    <!-- ── 14. KPA ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">KPA</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/kpa-lobby-sign.jpg"
               alt="KPA lobby sign installation Denver — branded reception area dimensional signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Sign Installation</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/kpa-lobby-sign2.jpg"
               alt="KPA lobby sign alternate view Denver — dimensional acrylic reception signage detail"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Sign &mdash; Alternate View</div>
        </div>
      </div>
    </div>

    <!-- ── 15. Westbound & Down Brewing ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Westbound &amp; Down Brewing</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/westbound-building-sign.jpg"
               alt="Westbound and Down Brewing exterior building sign installation Colorado — brewery commercial signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Exterior Building Sign</div>
        </div>
      </div>
    </div>

    <!-- ── 16. SEA ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">SEA</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/sea-lobby-wide.jpg"
               alt="SEA lobby graphics wide view installation Denver — commercial office interior vinyl signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Graphics &mdash; Wide</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/sea-lobby-sign.jpg"
               alt="SEA lobby sign installation Denver — branded reception area commercial signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Lobby Sign</div>
        </div>
      </div>
    </div>

    <!-- ── 17. Dog & Pony ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Dog &amp; Pony</span>
      </div>
      <div class="pf-photos-grid cols-1">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/dog-pony-exterior.jpg"
               alt="Dog and Pony exterior sign installation Denver — commercial storefront signage and graphics"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Exterior Sign Installation</div>
        </div>
      </div>
    </div>

    <!-- ── 18. Office Directory ── -->
    <div class="pf-project reveal">
      <div class="pf-project-header">
        <span class="pf-project-name">Office Directory</span>
      </div>
      <div class="pf-photos-grid cols-2">
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/office-directory.jpg"
               alt="Commercial office directory board installation Denver — lobby wayfinding signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Directory Board Installation</div>
        </div>
        <div class="pf-photo-cell" onclick="openGroupModal(this)">
          <img src="images/directory-sign.jpg"
               alt="Office directory sign installation Denver — interior wayfinding and suite signage"
               loading="lazy"/>
          <div class="pf-photo-overlay"></div>
          <div class="pf-caption">Directory Sign</div>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="pf-cta reveal">
      <a href="#contact" class="btn-primary">
        Get a Free Quote
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>
    </div>

  </div>
</section>

"""

# ─── 2. INSERT BEFORE <!-- PROCESS --> ──────────────────────────────────────

PROCESS_MARKER = "<!-- PROCESS -->"
if PROCESS_MARKER not in html:
    raise RuntimeError("Could not find '<!-- PROCESS -->' marker in HTML")

html = html.replace(PROCESS_MARKER, new_section + PROCESS_MARKER, 1)
print("✔ Inserted #portfolio-full section before <!-- PROCESS -->")

# ─── 3. ADD NAV LINK ────────────────────────────────────────────────────────

OLD_NAV_ITEM = '<li><a href="#portfolio">Portfolio</a></li>'
NEW_NAV_ITEMS = '<li><a href="#portfolio">Portfolio</a></li>\n    <li><a href="#portfolio-full">Full Portfolio</a></li>'

if OLD_NAV_ITEM not in html:
    print("⚠  Nav Portfolio link not found — skipping nav update")
else:
    html = html.replace(OLD_NAV_ITEM, NEW_NAV_ITEMS, 1)
    print("✔ Added 'Full Portfolio' nav link")

# ─── 4. WRITE FILE ──────────────────────────────────────────────────────────

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✔ File written successfully")

# ─── 5. VERIFY ──────────────────────────────────────────────────────────────

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

assert 'id="portfolio-full"' in content, "ERROR: portfolio-full section not found!"
assert 'href="#portfolio-full"' in content, "ERROR: nav link not found!"

# Count photos added
photo_count = content.count('class="pf-photo-cell"')
print(f"✔ Total pf-photo-cell items in portfolio-full: {photo_count}")
print("✔ All assertions passed — file looks good")
