# High Country Finish and Repair CO — Launch Guide

> **Status (Sept 2026):** photos, the Formspree form, hosting, domain and favicons are all done.
> The remaining items are the business listings (section 5–6) and the owner decisions listed at
> the bottom of this file.

## 1. Photos

All portfolio and hero photos live in `images/` and are already wired into the pages.
The homepage "About" block currently shows an install photo (`images/sea-lobby-sign.jpg`);
to swap in a team photo, replace that `<img>` in `index.html` (keep `object-fit:cover`).

---

## 2. Contact Form (Formspree)

Both quote forms (homepage and `get-a-quote.html`) post to
`https://formspree.io/f/mqeydnkg` via JavaScript and show an inline success message.
They include a hidden `_gotcha` honeypot field for spam. Manage submissions and the
notification email at **https://formspree.io**.

Free tier: 50 submissions/month. Paid: $10/mo unlimited.

---

## 3. Hosting (Recommended: Netlify — Free)

1. Go to **https://netlify.com** → sign up free
2. Drag and drop the `vinyl-website` folder onto the Netlify dashboard
3. Your site goes live instantly at a random URL like `amazing-site-123.netlify.app`
4. Connect your custom domain (step 4 below)

Netlify also handles the Formspree alternative — you can use **Netlify Forms** instead (built-in, free 100/mo):
- Add `netlify` attribute to the form tag
- Remove the Formspree action
- Submissions appear in your Netlify dashboard

---

## 4. Domain Name

Recommended domains (check availability):
- `highcountryfinish.com`
- `highcountryfinishandrepairco.com`
- `hcfinishco.com`

Buy from **Namecheap.com** (~$12/yr) or **Cloudflare Registrar** (cheapest, at-cost).

Once you have a domain, point it to Netlify in the domain DNS settings — Netlify has a 2-minute walkthrough.

---

## 5. Google Business Profile (Gets You on Maps)

This is FREE and critical for local search.

1. Go to **https://business.google.com**
2. Sign in with your Google account
3. Search for "High Country Finish and Repair CO" — if it doesn't exist, click "Add your business"
4. Fill in:
   - Business name: **High Country Finish and Repair CO**
   - Category: **Sign Shop** (primary), add **Window Tinting Service**, **Auto Wrapping Service**
   - Phone: **303-882-4656**
   - Service area: Denver + list the specific cities
   - Website: (add once your site is live)
   - Hours of operation
5. Verify by postcard or phone (Google mails a card with a PIN)
6. Add all your portfolio photos to the Google listing — this is huge for conversions

---

## 6. Other Free Listings to Create

In order of priority:

| Platform | URL | Notes |
|---|---|---|
| **Google Business** | business.google.com | #1 priority — do this first |
| **Yelp for Business** | biz.yelp.com | Free, helps local SEO |
| **Facebook Business** | business.facebook.com | Create a page, post your work |
| **Instagram** | instagram.com | @highcountryfinish or similar — post every job |
| **Thumbtack** | thumbtack.com/pro | Good for residential leads |
| **Angi (Angie's List)** | angi.com | Good for commercial leads |
| **BBB** | bbb.org | Credibility, especially for commercial clients |
| **Houzz** | houzz.com/pro | Good for residential window frosting/wall graphics |

---

## 7. SEO Checklist (Already Built In)

The site already has:
- ✅ Meta title and description with local keywords
- ✅ Schema-ready structure
- ✅ Canonical URL (update to your real domain)
- ✅ Mobile-first responsive design
- ✅ Fast loading (no heavy frameworks)
- ✅ Semantic HTML headings
- ✅ Alt text placeholders on images
- ✅ Local city mentions throughout content

**After launch, also do:**
- Submit sitemap to Google Search Console (free)
- Get 5+ Google reviews ASAP (ask every satisfied customer)
- Post your Google Business profile photos weekly for first month

---

## 8. Owner decisions (need real-world facts, not code)

The template's made-up numbers and badges were removed from the homepage during the
September 2026 audit and replaced with claims the site already makes elsewhere
(24-hour quote turnaround, 1-hour travel radius, in-house installs, premium cast vinyl).
If you want the original style of stats back, edit `index.html` with **true** figures:

- Hero stats (`.hero-stat` blocks): e.g. real installs completed, years in business.
- About badges (`.about-badges`): "Fully Insured" is still there — confirm it is accurate.
  "3M Preferred Installer" and "5-Star Rated" were removed; restore only if you hold the
  3M certification / have public 5-star reviews.
- Street address: the LocalBusiness schema on the homepage publishes
  city level only (Arvada, CO) at the owner's request — no street address or ZIP is published.
- Social profiles: add `sameAs` links (Google Business, Instagram, Facebook) to the
  LocalBusiness schema once the profiles exist.

---

## Summary Checklist

- [x] Add hero + portfolio photos
- [x] Replace template hero stats / badges (see section 8 for restoring real numbers)
- [x] Formspree form connected
- [x] Deploy to Netlify
- [x] Domain connected (highcountryfinish.com)
- [ ] Set up Google Business Profile
- [ ] Create Yelp, Facebook, Instagram accounts
- [ ] Get first 5 Google reviews
