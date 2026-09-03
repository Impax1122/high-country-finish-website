# High Country Finish and Repair CO — website

Static marketing site for a Denver / Front Range commercial sign and vinyl graphics installer.
Plain HTML, CSS and JavaScript — no build step. Deployed to Netlify from the repository root.

## Layout

```
index.html            Homepage (source of truth for shared CSS, nav and footer — see docs/BRAND.md)
services.html         Services hub
services/*.html       One page per service
portfolio.html        Full portfolio grid
about-us.html, our-process.html, service-area.html, get-a-quote.html, blog.html
blog/*.html           Articles
404.html              Custom not-found page
images/               Photos, logo, share card (og-home.jpg), favicons
sitemap.xml, robots.txt, netlify.toml, favicon.ico
docs/                 Brand guide, launch guide and build logs (not served)
scripts/              Historical one-off build/patch scripts (not served, do not re-run)
```

## Editing

* Every page carries its own copy of the shared CSS, nav and footer. When you change one of
  those, apply the same change to all 22 pages (a scripted find-and-replace is the safest way).
* Save files as UTF-8 without a byte-order mark.
* The quote forms post to Formspree (`https://formspree.io/f/mqeydnkg`) and include a `_gotcha`
  honeypot field for spam.
* `netlify.toml` blocks `/docs/*`, `/scripts/*` and `/README.md` from being served and sets the
  security headers. If you add a third-party script or embed, extend the Content-Security-Policy there.

## Deploying

Push to `master`; Netlify publishes the repository root.
