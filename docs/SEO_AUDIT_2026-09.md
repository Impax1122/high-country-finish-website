# SEO Audit — September 17, 2026

Scope: all 22 pages in the repo, `sitemap.xml`, `robots.txt`, structured data, internal links,
images, meta tags, and the live deploy at highcountryfinish.com (checked with curl).

## Summary

The technical foundation is in good shape. The gaps are off-site (no Google Business Profile,
no reviews), measurement (no analytics), one URL-consistency bug on the live deploy (fixed in
this pass), and content depth on the original blog posts.

| Area | Status |
|---|---|
| On-page (titles, descriptions, H1s, canonicals) | Good — 22/22 pages pass |
| Structured data | Good — valid on every page |
| Images (alt, dimensions, WebP, caching) | Good |
| Internal links / broken links | Good — 0 broken |
| URL consistency on the live site | Was broken — fixed (see P1) |
| Local SEO (GBP, reviews, citations, `sameAs`) | Not started |
| Measurement (analytics) | Missing |
| Content depth | Thin on the five original posts; six new long-form posts added |
| Legal pages (privacy, terms) | Missing |

## What passed (checked programmatically with a script over every page)

- Unique `<title>` (39–60 chars) and unique meta description (111–154 chars) on all 22 pages.
- Correct self-referencing canonical on every page; exactly one `<h1>`; `lang="en"`; a `<main>` landmark.
- `robots` index/follow everywhere except `404.html` (noindex, correct).
- JSON-LD parses on every page: `LocalBusiness` + `WebSite` (home), `Service` + `BreadcrumbList`
  (8 service pages), `BlogPosting` + `BreadcrumbList` (posts), `BreadcrumbList` (everything else).
- Every `<img>` has alt text and width/height. The only empty alts are the two lightbox
  placeholders, which is correct.
- 0 broken internal links, 0 missing image files, every `og:image` exists and is 1200×630.
- WebP + `srcset` on photo pages; images cached immutable; HTML `must-revalidate`.
- Security headers on the live site (HSTS, CSP, X-Frame-Options, Referrer-Policy).
- `www` → apex and `http` → `https` both 301 correctly; sitemap and robots serve with the right types.
- Google Search Console verification tag is present on the homepage.

## Findings, in priority order

### P1 — Live site linked to a different URL than the canonical (fixed)

Netlify's "pretty URLs" post-processing (`pretty_urls = true` in `netlify.toml`) rewrote every
internal link on the deployed site to the extensionless form (`/blog/slug`, `/services/wall-graphics`),
while the canonical tags, sitemap, Open Graph URLs, and breadcrumb schema all use `/page.html`.
Both forms returned 200 with no redirect between them, so every page existed at two URLs and
internal links pointed at the one the canonical did not name.

**Fix applied:** `pretty_urls = false`. Links now match the canonicals and the sitemap. Netlify
still serves the extensionless URLs, so nothing that was shared breaks.

If you would rather standardise on clean URLs later, it is a mechanical change: rewrite the
canonical, `og:url`, `@id`, breadcrumb and sitemap values in `build.js`, change internal links
to drop `.html`, and generate a `_redirects` file with one `301` per page from `.html` to the
clean path. Do it once, all at once, not gradually.

### P1 — No analytics

No GA4, Plausible, or similar on any page. You cannot see which pages bring quote requests.
Add one (Plausible or Fathom are the lightest and need no cookie banner) and extend the
`Content-Security-Policy` in `netlify.toml` (`script-src` and `connect-src`) for its domain.
Also set up conversion tracking on the Formspree success state (`#form-success` becoming visible).

### P1 — Google Business Profile and reviews

Still unchecked on `LAUNCH_GUIDE.md`. For "sign installation Denver" style searches, the map
pack is where the clicks are, and the site cannot appear there without a profile. Order of
operations: create and verify the profile, upload the portfolio photos, ask the last ten
commercial clients for a review, then add the profile URL (plus Instagram / LinkedIn when they
exist) as `sameAs` on the `LocalBusiness` schema in `index.html`.

### P2 — Original blog posts are thin

The five March posts are 320–420 words with no images. The six new posts are 1,000–1,400 words
with a photo, a table, cited sources where a code is involved, and internal links. Bring the
older five up to the same standard over time (the wall-prep and lobby-sign posts are the best
candidates since they already get internal links from service pages).

### P2 — No privacy policy or terms page

Needed before adding analytics, running Google Ads, taking online payments, and for Google
Business. Also a basic trust signal. One page, linked from the footer.

### P2 — No city pages although 13 cities are claimed

The schema and service-area page list Arvada, Lakewood, Boulder, Aurora, Littleton, Castle Rock
and more, but there is no page that can rank for "sign installation Arvada". Three to five real
pages (unique copy, local project photos, the local permitting note) would earn those searches.
Do not template thirteen near-identical pages; that pattern gets ignored or penalised.

### P3 — Smaller items

- Homepage `meta keywords` tag: ignored by Google and lists client names. Remove or trim.
- Homepage has no "from the blog" section; the blog is reachable only from nav and footer.
  A three-card strip would push link equity to the new commercial posts.
- `LocalBusiness` schema has no `openingHoursSpecification` or `sameAs`. Add when known.
- Blog author is the Organization. A `Person` author (the lead installer, with the 3M
  credential) on the code-focused posts would strengthen E-E-A-T.
- Fonts load from Google Fonts (two extra origins on first paint). Self-hosting Inter and
  Cormorant would shave 100–200 ms on first load. Optional.
- No RSS feed. Minor; could be generated by `build.js` from the `BlogPosting` schema.

## Changes made in this pass

- `netlify.toml`: `pretty_urls = false` (P1 fix above).
- `build.js`: sitemap image entries now include the figures in `blog/` pages.
- `blog.html`: six new posts, category tags on every card, updated description and intro.
- Six new posts in `blog/` with `BlogPosting` + breadcrumb schema, `article:` Open Graph tags,
  branded 1200×630 share cards in `images/og/`, an in-article figure with WebP `srcset`,
  tables, and cross-links:
  - `sign-installation-on-fire-rated-doors.html`
  - `ada-sign-installation-mounting-height-and-placement.html`
  - `how-to-hire-a-commercial-sign-installer-in-denver.html`
  - `wall-wraps-vs-paint-for-commercial-interiors.html`
  - `what-to-expect-during-a-commercial-wall-wrap-installation.html`
  - `can-you-wrap-a-textured-wall.html`
- Related-link blocks on five service pages, `our-process.html`, `service-area.html`, and three
  older posts now link to the new posts.
- `sitemap.xml` regenerated by `node build.js`.

## Next 30 days (owner tasks, not code)

1. Google Business Profile: create, verify, add photos, request reviews.
2. Add analytics and the CSP entries for it.
3. Add a privacy policy page and link it in the footer.
4. In Search Console: submit `sitemap.xml` again and request indexing for the six new posts.
5. Share the fire-door and ADA posts on LinkedIn to property managers, GCs, and facility
   groups. Those two are written to earn links from the commercial side.
