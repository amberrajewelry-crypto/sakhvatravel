#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function findFiles(dir) {
  const results = [];
  function walk(d) {
    if (!fs.existsSync(d)) return;
    const entries = fs.readdirSync(d, { withFileTypes: true });
    for (const e of entries) {
      const full = path.join(d, e.name);
      if (e.isDirectory()) walk(full);
      else if (e.name === 'index.html') results.push(full);
    }
  }
  walk(dir);
  return results;
}

const ROOT = '/Users/vladimir/sakhva-travel';
const files = [
  ...findFiles(path.join(ROOT, 'blog')),
  ...findFiles(path.join(ROOT, 'en/blog'))
];

const OLD = `<link rel="stylesheet" href="/fonts/raleway.css">
<link rel="stylesheet" href="/fonts/lora.css">`;

const NEW = `<link rel="preload" href="/fonts/lora-10.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/raleway.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<link rel="preload" href="/fonts/lora.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/fonts/raleway.css"><link rel="stylesheet" href="/fonts/lora.css"></noscript>`;

let fixed = 0, skipped = 0;

for (const f of files) {
  let html = fs.readFileSync(f, 'utf8');
  if (!html.includes(OLD)) { skipped++; continue; }
  html = html.replace(OLD, NEW);
  fs.writeFileSync(f, html, 'utf8');
  fixed++;
}

console.log(`Font loading fixed: ${fixed}`);
console.log(`Skipped: ${skipped}`);
