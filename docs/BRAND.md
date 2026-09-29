# High Country Finish & Repair CO — Brand Identity

**DO NOT DEVIATE FROM THIS FILE**  
All design changes must reference this document.

---

## Colors

```css
--gold:       #C9A84C;  /* Primary accent */
--gold-light: #E8C97D;  /* Hover states */
--gold-dark:  #9B7A2B;  /* Subtle accents */
--black:      #0c0c0c;  /* Page background */
--surface:    #141414;  /* Card/section backgrounds */
--surface2:   #1c1c1c;  /* Elevated surfaces */
--border:     #2a2a2a;  /* Dividers, borders */
--text:       #f0ece4;  /* Primary text */
--muted:      #888880;  /* Secondary text */
--white:      #ffffff;  /* Pure white (rare use) */
```

**Never use:**
- Bright colors
- Neon accents
- Multi-color gradients

---

## Typography

### Fonts
- **Headings:** `'Cormorant Garamond', serif` (Google Fonts)
- **Body:** `'Inter', sans-serif` (Google Fonts)

### Font Weights
- Cormorant Garamond: 400, 500, 600, 700
- Inter: 300, 400, 500, 600

### Sizes & Hierarchy

**Headings:**
```css
h1, h2, h3, h4 {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.01em;
}
```

**Section Labels:**
```css
.section-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
  margin-bottom: 16px;
}
```

**Section Titles:**
```css
.section-title {
  font-size: clamp(32px, 5vw, 52px);
  color: var(--text);
  margin-bottom: 20px;
}
```

**Section Body:**
```css
.section-body {
  font-size: 16px;
  color: var(--muted);
  max-width: 580px;
  line-height: 1.75;
}
```

---

## Spacing

### Container
```css
.container {
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 40px;
}

@media(max-width:768px) {
  .container { padding: 0 24px; }
}
```

### Section Padding
```css
section { padding: 100px 0; }

@media(max-width:768px) {
  section { padding: 70px 0; }
}
```

---

## Navigation

### Desktop Nav
```css
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 24px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background .3s, padding .3s, border-color .3s;
  border-bottom: 1px solid transparent;
}

nav.scrolled {
  background: rgba(12,12,12,.97);
  backdrop-filter: blur(12px);
  padding: 16px 40px;
  border-color: var(--border);
}
```

### Nav Logo
```css
.nav-logo .logo-main {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  letter-spacing: 0.5px;
}

.nav-logo .logo-sub {
  font-size: 9px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
  margin-top: 3px;
}
```

### Nav Links
```css
.nav-links {
  display: flex;
  gap: 36px;
  align-items: center;
}

.nav-links a {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: .5px;
  color: #aaa;
  transition: color .2s;
}

.nav-links a:hover { color: var(--text); }
```

### Nav Dropdown
```css
.nav-item {
  position: relative;
}

.nav-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 20px;
  background: rgba(20, 20, 20, 0.98);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 0;
  min-width: 220px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  z-index: 2000;
}

.nav-item:hover .nav-dropdown {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.nav-dropdown a {
  display: block;
  padding: 10px 24px;
  font-size: 13px;
  color: var(--muted);
}

.nav-dropdown a:hover {
  background: var(--surface2);
  color: var(--text);
  padding-left: 28px;
}
```

---

## Footer

### Structure
```html
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="logo-main">High Country</div>
        <div class="logo-sub">Finish &amp; Repair Co.</div>
        <p>Commercial sign installation and vinyl graphics. Based in Arvada, CO.</p>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Services</p>
        <ul>...</ul>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Company</p>
        <ul>...</ul>
      </div>
      <div class="footer-col">
        <p class="footer-heading">Contact</p>
        <ul>...</ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 High Country Finish &amp; Repair Co. All rights reserved.</p>
      <p>Arvada, CO &middot; 303-882-4656</p>
    </div>
  </div>
</footer>
```

### Footer CSS
```css
footer {
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 60px 0 32px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
  margin-bottom: 48px;
}

.footer-brand .logo-main {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 4px;
}

.footer-brand .logo-sub {
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--gold);
}

.footer-brand p {
  font-size: 13px;
  color: var(--muted);
  margin-top: 16px;
  max-width: 260px;
  line-height: 1.7;
}

.footer-col .footer-heading {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--gold);
  margin-bottom: 16px;
}

.footer-col ul {
  list-style: none;
}

.footer-col ul li {
  font-size: 13px;
  color: var(--muted);
  padding: 5px 0;
}

.footer-col ul li a:hover {
  color: var(--gold);
}

.footer-bottom {
  border-top: 1px solid var(--border);
  padding-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.footer-bottom p {
  font-size: 12px;
  color: var(--muted);
}

@media(max-width:900px) {
  .footer-grid { grid-template-columns: 1fr 1fr; gap: 36px; }
}

@media(max-width:600px) {
  .footer-grid { grid-template-columns: 1fr; }
}
```

---

## Buttons

### Primary CTA
```css
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
```

### Secondary CTA
```css
.cta-button.secondary {
  background: transparent;
  color: var(--gold);
}

.cta-button.secondary:hover {
  background: var(--surface);
}
```

---

## Cards

### Service Cards
```css
.service-card {
  background: var(--surface2);
  padding: 40px 32px;
  border: 1px solid var(--border);
  border-radius: 4px;
  transition: border-color 0.3s, transform 0.3s;
}

.service-card:hover {
  border-color: var(--gold-dark);
  transform: translateY(-4px);
}
```

---

## Gold Line Accent
```css
.gold-line {
  width: 48px;
  height: 2px;
  background: var(--gold);
  margin-bottom: 24px;
}
```

---

## Brand Messaging

Public copy follows Brand Guide v2.3, with these website decisions from Alex:

- Display name: **High Country Finish & Repair Co.** Always the ampersand and "Co." Never "Finish and Repair CO."
- Public location: **Arvada, CO**. Say where the business is based as "Arvada, CO" (for example, "Based in Arvada, CO, serving Denver and the Front Range"). No street address and no postal code on the site, including JSON-LD. JSON-LD address is addressLocality "Arvada", addressRegion "CO", addressCountry "US". Service-area city lists can still name Denver and other cities. Do not use "Denver metro" as the business location.
- Who we serve: homeowners and residential work, alongside businesses and sign shops. Do not say or imply commercial-only.
- White-label installs are the default on trade jobs. Never post photos of a sign shop's job without that shop's OK.
- Structured data telephone: **+1-303-882-4656**. Visible phone and tel: links: **303-882-4656**.
- Email: **alexdrew@highcountryfinish.com**. Phone: **303-882-4656**.
- Experience: **20+ years**. Certification: **3M Preferred Installer**. Install count: **500+ installs**, credited to our lead installer.
- Insurance on the site: **COI upon request**. Do not print "general liability insured," coverage limits, workers' comp, commercial auto, "fully insured," or additional-insured wording.
- End-client line: "Every install should look like it came from the factory."
- Trade page (`/trade.html`): "Your install crew — without the payroll." Descriptor: "Wholesale sign installation for the trade."
- Do not use "guaranteed," "no questions asked," "premier," "flawless," "solutions," or "clients who demand the best."
- Service names, in order: Sign Installation, Lobby Signs, Building Signs, Wall Graphics & Murals, Window Frosting & Tint, Vehicle Wraps & Graphics, Spot Graphics, Sign Removal, Site Surveys. Existing pages stay at their URLs. Window frosting and window tint remain separate pages. Custom Work stays because that page already exists. Sign removal and site surveys are named on the trade page and the services intro; they don't have their own pages.
- Site surveys have a fee. Alex decides job by job whether to credit that fee on larger jobs that go ahead. Do not describe a survey as free, complimentary, or included at no charge, and do not publish a dollar amount. Quotes stay free: "Free Quote" and "Request a Free Quote" stay as written.
- Do not advertise ADA signage or contract or vinyl cutting as a service (no service-list item, form option, or schema offer). The ADA mounting-height post can stay as a rules article; its quote button is a generic sign-install quote. Passing mentions of ADA rules inside other posts can stay. Do not add new pages for that work.

### Voice & Tone
- **Direct** — No fluff, no corporate speak
- **Plain** — Short sentences, contractions, concrete details
- **Confident** — We know what we're doing
- **Local** — Based in Arvada, CO, serving Denver and the Front Range

### Key Phrases
- "Every install should look like it came from the factory."
- "3M Preferred Installer"
- "20+ years"
- "COI upon request"
- "Detail-obsessed"

---

## Design Principles

1. **Dark luxury aesthetic** — Never bright or loud
2. **Typography-driven** — Let fonts do the heavy lifting
3. **Minimal accents** — Gold used sparingly
4. **Clean spacing** — Generous whitespace
5. **Professional photography** — Real work, no stock photos
6. **Smooth animations** — Subtle, never distracting

---

## Mobile Responsiveness

### Breakpoints
- Desktop: 1240px max-width container
- Tablet: 768px and below
- Mobile: 600px and below

### Mobile Nav
- Full-screen overlay
- Large touch targets (18px font minimum)
- Body scroll lock when open
- Smooth hamburger → X animation

---

## File Structure

```
vinyl-website/
├── index.html           (Homepage - THE SOURCE OF TRUTH)
├── portfolio.html       (Match homepage exactly)
├── services.html        (Match homepage exactly)
├── about-us.html        (Match homepage exactly)
├── our-process.html     (Match homepage exactly)
├── service-area.html    (Match homepage exactly)
├── get-a-quote.html     (Match homepage exactly)
├── trade.html           (Wholesale page for sign companies)
├── blog.html            (Match homepage exactly)
├── services/
│   ├── vehicle-wraps.html
│   ├── spot-graphics.html
│   ├── window-tint.html
│   ├── window-frosting.html
│   ├── wall-graphics.html
│   ├── lobby-signs.html
│   ├── building-signs.html
│   └── custom-work.html
├── blog/
│   └── [blog posts]
└── images/
```

---

## Homepage = Master Template

**Nav and footer markup live in `partials/` and are copied into every page by `node build.js` — edit them there, never in a page.**

**The homepage (`index.html`) is the source of truth for:**
- All CSS
- Font loading
- Color variables
- Spacing
- Typography
- Footer structure
- Navigation structure

**When making changes:**
1. Update homepage first
2. Extract changes to this BRAND.md
3. Apply systematically to all other pages
4. Never deviate from homepage styling

---

**Last updated:** September 29, 2026  
**Maintained by:** HC Overlord

Share images under `images/og/` were not redrawn. Any "Denver's Premier" text baked into those image files is still there until the artwork is replaced.
