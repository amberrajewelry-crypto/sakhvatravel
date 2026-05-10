#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const dir = '/Users/vladimir/sakhva-travel/ekskursiya';
const entries = fs.readdirSync(dir, { withFileTypes: true });
let fixed = 0;

for (const e of entries) {
  if (!e.isDirectory()) continue;
  const f = path.join(dir, e.name, 'index.html');
  if (!fs.existsSync(f)) continue;

  let html = fs.readFileSync(f, 'utf8');
  if (html.includes('noindex')) continue;

  html = html.replace(
    '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
    '<meta name="robots" content="noindex,follow">'
  );
  fs.writeFileSync(f, html, 'utf8');
  fixed++;
}
console.log(`Noindex added: ${fixed}`);
