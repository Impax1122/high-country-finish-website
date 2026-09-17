# Selling Online — Roadmap for Products and Services

Written September 2026 in answer to "what should we expand the site into for purchasing
options for products and services". Recommendation first, then the phases, then what to avoid.

## Recommendation in one paragraph

Do not turn the site into a store. Almost everything High Country sells is priced by the wall,
the vehicle, the substrate, and the access, and a checkout page that guesses at that will either
lose money or lose the customer. Instead, add three ways to pay and book that fit a service
business, in this order: (1) online deposits and invoice payment on quotes you have already
written, (2) a short list of fixed-price, install-included packages that are safe to sell sight
unseen, and (3) a small product catalogue only where a product plus local installation is
something a national website cannot offer. Each phase pays for the next, and all three run on
the current static Netlify site without a rebuild.

## Phase 1 — Take money on quotes you already win (1–2 days)

**What:** A `/pay.html` page and a "pay your deposit" link in every quote email.

**How:** Stripe Payment Links or Stripe Invoicing (Square Invoices is the equivalent). Hosted
checkout, no card data on the site, no PCI scope, no backend. A payment link is a plain `<a>`
to `checkout.stripe.com`, so the Content-Security-Policy does not need to change. Cost is the
card fee only.

**Why first:** It shortens the gap between "yes" and "scheduled", which is where jobs stall,
and it moves deposits off phone calls and paper checks. It also creates the Stripe account,
customer records, and receipts everything else builds on.

**Also add:** a "Book a site survey" button using Cal.com or Calendly. For a service business,
scheduling is the purchase. The embed needs `frame-src` and `script-src` entries in the CSP.

**Legal:** a deposit and refund policy, terms of service, and a privacy policy page. Stripe
requires them and the site has none today.

## Phase 2 — Fixed-price packages with installation (2–4 weeks)

Sell only what you can quote without a site visit. Candidates, all of which the new blog posts
already send traffic toward:

| Package | Why it is safe to price online |
|---|---|
| ADA room sign packages, installed (restroom pair, suite number, stair/exit set) | Standard sizes, known mounting rules, small install window; property managers buy these in batches |
| Fire-door compliance signage kit, installed ("Fire Door, Keep Closed" decals sized inside the 5 % limit) | Fixed material, adhesive only, quick; ties directly to the NFPA 80 post |
| USDOT / MC number and fleet lettering, per vehicle | Required by law for commercial carriers, fixed format, repeat buyers |
| Storefront hours + logo decal package | Small vinyl, one glass panel, predictable |
| Frosted privacy band, priced per linear foot up to a cap | Linear pricing, one film, standard height |
| Install-only day rate for sign shops (half day / full day, lift extra) | You already sell this; a published rate card with a booking form converts shops faster |

**Mechanics:** each package is a Stripe Payment Link with required fields for site address,
contact, and preferred dates, and a note that the install date is confirmed by phone. Refund
automatically if the address is outside the service radius. Show the package cards on a new
`/packages.html` page and link each from the matching service page and blog post.

**Upgrade path when volume justifies it:** a Netlify Function that creates a Stripe Checkout
Session from a small configurator (service, quantity, surface) so prices stay in code, plus a
webhook that emails the confirmation and drops the job into the Formspree inbox alongside the
quote requests. Same site, same deploy, still no server to run.

## Phase 3 — Products, only where "product + local install" is the edge (later)

Selling bare products (sign blanks, vinyl kits, wrap care kits) puts you against national
suppliers on price and shipping. The exceptions worth testing are products bundled with Denver
installation, and reorders from existing commercial clients: replacement ADA signs, additional
suite signs, a second vehicle in the fleet, a replacement wall-wrap panel from files you keep.

**If you get here:** embed Snipcart or the Shopify Buy Button inside the existing site at
`/shop/` rather than launching a separate Shopify store on a subdomain. The site's SEO equity
lives on `highcountryfinish.com`; a store on another domain or subdomain starts from zero. Both
options need CSP changes (`script-src`, `connect-src`, `frame-src`) and Colorado sales tax
handling for shipped goods; installed signage attached to real property is treated differently,
so confirm the treatment with your accountant before publishing prices.

## What to avoid

- A full rebuild on Shopify, Wix, or Squarespace "to add a store". You would lose the
  structured data, the URL structure, the speed, and the ranking history for a cart you would
  use for a dozen items.
- Per-square-foot online pricing for wall wraps, murals, or vehicle wraps. Every one of those
  needs the survey. Publish "from" prices in copy if you want to anchor expectations, but keep
  the transaction after the survey.
- Taking payment through the quote form itself. Keep the form for leads and the payment link
  for money; mixing them adds fraud and refund handling to a lead form.

## What this changes on the site

- Nav: keep "Get a Quote" as the primary button; add "Packages" to the Services dropdown and
  "Pay an Invoice" to the footer Company column.
- `netlify.toml`: `Permissions-Policy` currently disables `payment=()`. That header only
  affects the in-page Payment Request API and does not block a hosted Stripe checkout, but
  revisit it if you ever embed checkout on the page.
- Measurement: add analytics before Phase 2 so you can see which blog post or service page
  produced each package sale. Without it you are pricing in the dark.

## Suggested order

1. Stripe account, `/pay.html`, deposit link in the quote email template, policy pages.
2. Survey booking embed.
3. Two packages to start: ADA sign packages and fire-door signage kits. They are the cheapest
   to fulfil and they have content on the site already.
4. Add fleet lettering and install-only day rates once the first two are selling.
5. Revisit products in six months with real numbers.
