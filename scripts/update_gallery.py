# update_gallery.py — Replace portfolio section with grouped gallery layout
import re, sys

FILE = r"C:\Users\Spaceship\.openclaw\workspace\vinyl-website\index.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ── New portfolio section ────────────────────────────────────────────────────
NEW_SECTION = """<!-- PORTFOLIO -->
<style>
/* ── Gallery Groups ─────────────────────────────────────────────────── */
.gallery-group { margin-bottom: 56px; }
.gallery-group:last-child { margin-bottom: 0; }
.gallery-group-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 0.03em;
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(201,168,76,.25);
  display: flex;
  align-items: center;
  gap: 12px;
}
.gallery-group-title::before {
  content: '';
  display: inline-block;
  width: 28px;
  height: 2px;
  background: var(--gold);
  flex-shrink: 0;
}
.group-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.group-grid.cols-2 {
  grid-template-columns: repeat(2, 1fr);
  max-width: 820px;
}
.group-grid.cols-1 {
  grid-template-columns: 1fr;
  max-width: 520px;
}
@media(max-width: 900px) {
  .group-grid,
  .group-grid.cols-2 { grid-template-columns: 1fr 1fr; }
}
@media(max-width: 600px) {
  .group-grid,
  .group-grid.cols-2 { grid-template-columns: 1fr; max-width: 100%; }
}
.group-item {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border-radius: 4px;
  background: var(--surface2);
}
.group-item img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform .6s ease;
}
.group-item:hover img { transform: scale(1.04); }
.group-item-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,.82) 0%, transparent 55%);
  opacity: 0;
  transition: opacity .3s ease;
  display: flex;
  align-items: flex-end;
  padding: 16px;
}
.group-item:hover .group-item-overlay { opacity: 1; }
.group-item-caption {
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  letter-spacing: .4px;
  line-height: 1.4;
}
</style>

<section id="portfolio">
  <div class="container">

    <div class="section-header" style="text-align:center;margin-bottom:3rem;">
      <span class="section-label reveal">Our Work</span>
      <h2 class="section-title reveal">Denver Sign &amp; Graphics<br/>Portfolio</h2>
      <p class="reveal" style="color:var(--muted);max-width:540px;margin:0 auto 2rem;">A sample of our recent commercial installs across Denver and the Front Range.</p>
    </div>

    <!-- Group 1: Vehicle Wraps -->
    <div class="gallery-group reveal">
      <div class="gallery-group-title">Vehicle Wraps</div>
      <div class="group-grid cols-2">

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/cybertruck-side.jpg"
               alt="Cybertruck commercial vehicle graphics Denver — Black Rock Vinyl lettering and body wrap"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Cybertruck — Black Rock Vinyl Lettering</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/957-party-vehicle-wrap.jpg"
               alt="Full vehicle wrap Denver CO — 95.7 The Party radio station SUV branded wrap"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">95.7 The Party — Full Vehicle Wrap</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Group 2: Lobby & Office Signs -->
    <div class="gallery-group reveal">
      <div class="gallery-group-title">Lobby &amp; Office Signs</div>
      <div class="group-grid">

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/peak-elevator-lobby-sign.jpg"
               alt="PEAK Elevator Performance Group lobby sign installation Denver — large dimensional acrylic panel"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">PEAK Elevator Performance Group</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/novara-frosted-glass.jpg"
               alt="Novara office reception sign and frosted glass installation Denver"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Novara — Reception &amp; Frosted Glass</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/kpa-lobby-sign.jpg"
               alt="KPA lobby sign installation Denver — branded reception area signage"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">KPA Lobby Sign</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/glover-masonry-lobby.jpg"
               alt="Glover Masonry lobby acrylic sign installation Denver — wide angle reception sign"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Glover Masonry — Lobby Sign</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Group 3: Wall Murals & Graphics -->
    <div class="gallery-group reveal">
      <div class="gallery-group-title">Wall Murals &amp; Graphics</div>
      <div class="group-grid">

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/omeara-room-wrap.jpg"
               alt="O'Meara Ford and 106.7 KBPI full room wall wrap installation Denver — branded interior mural"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">O&#8217;Meara Ford / KBPI — Full Room Wrap</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/elite-brands-wall-mural.jpg"
               alt="Elite Brands office wall mural installation Denver — large format branded graphics with core values"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Elite Brands — Office Wall Mural</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/gque-bbq-mural.jpg"
               alt="GQue BBQ large format wall mural installation Denver — restaurant interior branded graphics"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">GQue BBQ — Large Format Wall Mural</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Group 4: Elevator & Building Wraps -->
    <div class="gallery-group reveal">
      <div class="gallery-group-title">Elevator &amp; Building Wraps</div>
      <div class="group-grid cols-1">

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/iheart-elevator-wrap.jpg"
               alt="iHeartMedia elevator wrap installation Denver — commercial vinyl elevator door graphics"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">iHeartMedia — Elevator Wrap</span>
          </div>
        </div>

      </div>
    </div>

    <!-- Group 5: Exterior Signage -->
    <div class="gallery-group reveal">
      <div class="gallery-group-title">Exterior Signage</div>
      <div class="group-grid">

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/buffalo-restaurant-exterior.jpg"
               alt="The Buffalo Restaurant and Bar exterior storefront signage installation Front Range Colorado"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">The Buffalo Restaurant &amp; Bar</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/trinity-place-exterior-sign.jpg"
               alt="Trinity Place 1801 Broadway Denver exterior building sign installation — commercial signage"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Trinity Place — 1801 Broadway Denver</span>
          </div>
        </div>

        <div class="group-item" onclick="openGroupModal(this)">
          <img src="images/westbound-building-sign.jpg"
               alt="Westbound and Down Brewing exterior building sign installation Colorado — commercial brewery signage"
               loading="lazy"/>
          <div class="group-item-overlay">
            <span class="group-item-caption">Westbound &amp; Down Brewing</span>
          </div>
        </div>

      </div>
    </div>

    <div style="text-align:center;margin-top:2.5rem;" class="reveal">
      <a href="portfolio.html" class="btn-primary">View Full Portfolio &rarr;</a>
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
</script>"""

# ── Find the portfolio section boundaries and replace ───────────────────────
# Match from <!-- PORTFOLIO --> comment through closing </section>
pattern = r'<!-- PORTFOLIO -->.*?</section>'
match = re.search(pattern, html, re.DOTALL)

if not match:
    print("ERROR: Could not find <!-- PORTFOLIO --> section!", file=sys.stderr)
    sys.exit(1)

old_section = match.group(0)

# Count items in old section
old_items = len(re.findall(r'<div class="featured-item', old_section))
print(f"Old gallery items found: {old_items}")

new_html = html[:match.start()] + NEW_SECTION + html[match.end():]

# Count items in new section
new_items = len(re.findall(r'<div class="group-item"', new_html))
print(f"New gallery items written: {new_items}")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done. File written successfully.")
