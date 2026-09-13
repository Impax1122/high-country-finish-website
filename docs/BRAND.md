# High Country Finish & Repair CO — Brand & Design System ("HC Light")

**Single source of truth for the website's look.** The stylesheet that implements it is `css/site.css`
(one file, every page). If a change is not expressible with the tokens below, add a token here first.

The system follows Anthropic's design standards: a warm paper ground, ink text, one accent colour used
with restraint, geometric headings, a readable serif for body copy, generous whitespace, few borders,
almost no shadows.

---

## Colors

```css
:root {
  --paper:    #faf9f5;  /* page ground */
  --paper-2:  #f1efe8;  /* cards, alternate section surfaces */
  --line:     #e8e6dc;  /* hairlines, solid borders */
  --line-2:   rgba(20,20,19,.18); /* stronger borders (inputs, hover) */
  --mid:      #b0aea5;  /* meta text on dark surfaces, placeholders */
  --ink-2:    #5f5e5a;  /* secondary text — 6.4:1 on paper */
  --ink:      #141413;  /* primary text, dark sections (footer, CTA band) */
  --orange:   #d97757;  /* the accent: primary buttons, eyebrow rules, list marks */
  --orange-2: #c96b4b;  /* accent hover, coloured display words */
  --blue:     #6a9bcc;  /* secondary mark (icons, badges) */
  --green:    #788c5d;  /* tertiary mark (icons, success) */
}
```

Rules:
- Text is `--ink` or `--ink-2` on paper; `--paper` or `--mid` on ink. Every pairing is ≥ 4.5:1.
- Orange is for shapes and large display text only. Never set small body text in orange on paper (3:1).
- Cycle orange → blue → green across repeated icons or badges; never put two accents on one component.
- No gold, no pure white surfaces, no gradients except the photo-caption overlay in galleries.
- Dark surfaces: footer, the services-hub CTA band, the lightbox. Everything else is paper.

Legacy names (`--gold`, `--black`, `--surface`, `--border`, `--text`, `--muted`, …) are aliased onto the
tokens above so old inline styles keep working. Do not use them in new code.

## Typography

- **Headings and UI** (nav, buttons, labels, stats, captions): `'Poppins', Arial, sans-serif`
- **Body copy**: `'Lora', Georgia, serif`
- Google Fonts request (already in every page head):
  `family=Poppins:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400`

| Role | Face | Size | Weight | Notes |
|---|---|---|---|---|
| Display (home h1) | Poppins | clamp(40px, 5.6vw, 68px) | 600 | line-height 1.06, letter-spacing -0.02em, `text-wrap: balance` |
| Page h1 | Poppins | clamp(38px, 5.2vw, 62px) | 600 | max-width 18ch |
| Section title (h2) | Poppins | clamp(30px, 4vw, 44px) | 600 | max-width 22ch |
| Card / step h3 | Poppins | 20–22px | 600 | |
| Eyebrow label | Poppins | 12px | 500 | uppercase, letter-spacing .14em, `--ink-2`, 22px orange rule before it |
| Body | Lora | 17px (16px mobile) | 400 | line-height 1.7, max-width ~62ch |
| Lead / hero paragraph | Lora | 19px | 400 | `--ink-2` |
| Article body | Lora | 18px | 400 | line-height 1.8, `--ink` |
| Buttons | Poppins | 15px | 500 | sentence case, never uppercase |
| Nav links | Poppins | 14px | 500 | `--ink-2`, orange 2px underline on hover |
| Stats number | Poppins | 36px | 600 | tabular numerals |

## Shape, depth, motion

- Radius: 6px buttons and inputs, 12px cards and gallery tiles, 14px photo frames.
- Borders: 1px `--line`; inputs use `--line-2`. Shadows only on floating things (scrolled nav, dropdown,
  card hover) and kept light.
- Buttons: primary = orange fill + ink text; secondary = transparent + `--line-2` border, fills ink on hover.
- Focus: 2px orange outline, 3px offset (`:focus-visible`). Inputs get an ink border + soft orange ring.
- Motion: `.reveal` fades in with a 14px rise over .55s; nav gains a hairline and soft shadow on scroll;
  hovers lift 2–3px. All of it collapses under `prefers-reduced-motion`.

## Layout

- Container 1240px, side padding 40px (24px under 768px). Sections 96px vertical (64px mobile).
- Headings left-aligned. Centering is reserved for the portfolio header and the CTA band.
- Service pages: a section that contains a photo becomes two columns at ≥1000px and alternates the
  photo side (`:has()`-driven, degrades to a single column).
- Photos always sit in a rounded frame; never tinted.

## Logo and imagery

- `images/logo-ink.png` — transparent ink mark for paper surfaces (nav).
- `images/logo-light.png` — transparent paper mark for dark surfaces (footer).
- `images/logo.png` — the original gold-on-dark file; only referenced by structured data.
- Icons (`favicon.ico`, `images/favicon-32.png`, `apple-touch-icon.png`, `icon-192/512.png`) are the
  emblem in paper on an ink tile. `images/og-home.jpg` is the paper share card; per-page share images
  are photos.

## Voice

- Sentence case for headings and buttons. Concrete nouns, no hype.
- Speak to both audiences: business owners and property managers, and the sign shops that subcontract
  installs. Never phrase copy as anti-subcontractor.
- Credentials are stated once per page at most: 3M-certified installer, 25 years in the trade,
  500+ installs (the lead installer's, not the company's), $1M general liability. No street address.
