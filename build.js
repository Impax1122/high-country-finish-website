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
for (const m of missing) console.error(`warning: ${m}`);
console.log(`${pages.length} pages, ${Object.keys(partials).length} partials, ${changed} ${check ? 'out of date' : 'updated'}`);
if (missing.length || (check && changed)) process.exit(1);
