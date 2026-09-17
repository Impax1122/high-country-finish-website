# High Country Finish and Repair CO — website

Static marketing site for a Denver / Front Range commercial sign and vinyl graphics installer.
Plain HTML, CSS and JavaScript — no build step. Deployed to Netlify from the repository root.

## Layout

```
index.html            Homepage (source of truth for shared CSS, nav and footer — see docs/BRAND.md)
services.html         Services hub
services/*.html       One page per service
portfolio.html        Full portfolio grid
about-us.html, our-process.html, service-area.html, get-a-quote.html, blog.html, privacy.html
blog/*.html           Articles
404.html              Custom not-found page
images/               Photos, logo, share card (og-home.jpg), favicons
sitemap.xml, feed.xml, robots.txt, netlify.toml, favicon.ico
partials/             nav.html and footer.html — the single source for the shared nav/footer
build.js              Copies the partials into every page, regenerates sitemap.xml and feed.xml (node build.js; --check on deploy)
docs/                 Brand guide, launch guide, SEO audit/work log, e-commerce roadmap, image credits and build logs (not served)
scripts/              Historical one-off build/patch scripts (not served, do not re-run)
```

## Editing

* The site nav and footer live in `partials/nav.html` and `partials/footer.html`. Edit the partial,
  then run `node build.js` to copy it into every page (each page holds the block between
  `<!-- build:nav -->` / `<!-- build:footer -->` markers). `node build.js --check` reports stale
  pages and is what Netlify runs on deploy, so a forgotten build fails loudly instead of shipping.
* The shared CSS is still duplicated per page; when you change it, apply the change to every page (run `node build.js --check` to list them).
* Save files as UTF-8 without a byte-order mark.
* Blog posts carry `BlogPosting` JSON-LD; `build.js` reads it to build `feed.xml` and the sitemap's
  image entries, so keep the schema block on every new post (copy an existing post as the template).
* Third-party photos must be public domain or CC0 and listed in `docs/IMAGE_CREDITS.md`.
* The quote forms post to Formspree (`https://formspree.io/f/mqeydnkg`) and include a `_gotcha`
  honeypot field for spam.
* `netlify.toml` blocks `/docs/*`, `/scripts/*` and `/README.md` from being served and sets the
  security headers. If you add a third-party script or embed, extend the Content-Security-Policy there.

## Deploying

Push to `master`; Netlify publishes the repository root.
