#!/usr/bin/env node
// Shared-markup build step (no dependencies).
//
// Every page carries the site nav and footer between marker comments:
//   <!-- build:nav --> ... <!-- /build:nav -->
//   <!-- build:footer --> ... <!-- /build:footer -->
// The single source for each block is partials/<name>.html. Running
//   node build.js          rewrites the block in every page from its partial
//   node build.js --check  exits 1 if any page is out of date (used by CI/Netlify)
// Edit the partial, run the build, commit the result. Never edit the block inside a page directly.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const check = process.argv.includes('--check');

const partials = {};
for (const f of fs.readdirSync(path.join(ROOT, 'partials'))) {
  if (f.endsWith('.html')) partials[f.slice(0, -5)] = fs.readFileSync(path.join(ROOT, 'partials', f), 'utf8').trim();
}

const pages = [];
for (const dir of ['', 'services', 'blog']) {
  const abs = path.join(ROOT, dir);
  for (const f of fs.readdirSync(abs)) if (f.endsWith('.html')) pages.push(path.join(dir, f));
}
pages.sort();

let changed = 0;
const missing = [];
for (const rel of pages) {
  const file = path.join(ROOT, rel);
  const before = fs.readFileSync(file, 'utf8');
  let after = before;
  for (const [name, body] of Object.entries(partials)) {
    const re = new RegExp(`(<!-- build:${name} -->)[\\s\\S]*?(<!-- /build:${name} -->)`);
    if (!re.test(after)) { missing.push(`${rel}: no build:${name} markers`); continue; }
    after = after.replace(re, () => `$1\n${body}\n$2`.replace('$1', `<!-- build:${name} -->`).replace('$2', `<!-- /build:${name} -->`));
  }
  if (after !== before) {
    changed++;
    if (check) console.log(`out of date: ${rel}`); else { fs.writeFileSync(file, after); console.log(`updated: ${rel}`); }
  }
}
// --- shared stylesheet cache-busting: keep ?v= in every page equal to the current css/site.css hash
const cssPath = path.join(ROOT, 'css', 'site.css');
if (fs.existsSync(cssPath)) {
  const hash = require('crypto').createHash('md5').update(fs.readFileSync(cssPath)).digest('hex').slice(0, 8);
  for (const rel of pages) {
    const file = path.join(ROOT, rel);
    const before = fs.readFileSync(file, 'utf8');
    const after = before.replace(/href="\/css\/site\.css\?v=[0-9a-f]+"/g, `href="/css/site.css?v=${hash}"`);
    if (after !== before) { changed++; if (check) console.log(`stale stylesheet version: ${rel}`); else { fs.writeFileSync(file, after); console.log(`stylesheet version updated: ${rel}`); } }
  }
}

// --- sitemap.xml: one entry per page (404 excluded), lastmod from git, image entries for the photo pages.
// Only regenerated locally (not in --check), because Netlify's shallow clone has no per-file history.
if (!check) {
  const { execSync } = require('child_process');
  const SITE = 'https://highcountryfinish.com';
  const today = new Date().toISOString().slice(0, 10);
  const lastmod = (rel) => { try { return execSync(`git log -1 --format=%cs -- "${rel}"`, { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim() || today; } catch { return today; } };
  const prio = (rel) => rel === 'index.html' ? '1.0' : /^(services|portfolio|get-a-quote)\.html$/.test(rel) ? '0.9' : rel.startsWith('services/') ? '0.8' : rel.startsWith('blog/') ? '0.6' : '0.7';
  const freq = (rel) => /^(index|portfolio|blog)\.html$/.test(rel) ? 'weekly' : 'monthly';
  const entries = pages.filter(r => r !== '404.html').map(rel => {
    const loc = rel === 'index.html' ? SITE + '/' : `${SITE}/${rel}`;
    const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    const imgs = [];
    if (/^(portfolio|index|services)\.html$|^services\//.test(rel)) {
      const re = /<img\b[^>]*src="([^"]+\.jpg)"[^>]*alt="([^"]*)"/g; let m;
      while ((m = re.exec(html))) { const src = m[1].startsWith('/') ? m[1] : '/' + m[1]; if (!/logo/.test(src)) imgs.push(`    <image:image><image:loc>${SITE}${src}</image:loc><image:title>${m[2].replace(/&/g, '&amp;')}</image:title></image:image>`); }
    }
    return `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${lastmod(rel)}</lastmod>\n    <changefreq>${freq(rel)}</changefreq>\n    <priority>${prio(rel)}</priority>\n${imgs.join('\n')}${imgs.length ? '\n' : ''}  </url>`;
  });
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n${entries.join('\n')}\n</urlset>\n`;
  const smPath = path.join(ROOT, 'sitemap.xml');
  if (!fs.existsSync(smPath) || fs.readFileSync(smPath, 'utf8') !== xml) { fs.writeFileSync(smPath, xml); console.log('sitemap.xml regenerated'); }
}

for (const m of missing) console.error(`warning: ${m}`);
console.log(`${pages.length} pages, ${Object.keys(partials).length} partials, ${changed} ${check ? 'out of date' : 'updated'}`);
if (missing.length || (check && changed)) process.exit(1);
