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

let removed = 0, skipped = 0, errors = [];

for (const f of files) {
  let html = fs.readFileSync(f, 'utf8');

  if (!html.includes('class="article-cta"')) {
    skipped++;
    continue;
  }

  // Find <div class="article-cta" ...> and remove the entire div
  const startIdx = html.indexOf('<div class="article-cta"');
  if (startIdx === -1) { skipped++; continue; }

  let depth = 0;
  let endIdx = startIdx;
  let i = startIdx;
  while (i < html.length) {
    if (html.substring(i, i + 4) === '<div') {
      depth++;
      i += 4;
    } else if (html.substring(i, i + 6) === '</div>') {
      depth--;
      if (depth === 0) {
        endIdx = i + 6;
        break;
      }
      i += 6;
    } else {
      i++;
    }
  }

  if (endIdx > startIdx) {
    // Also remove surrounding whitespace
    let before = startIdx;
    while (before > 0 && html[before - 1] === '\n') before--;
    let after = endIdx;
    while (after < html.length && (html[after] === '\n' || html[after] === ' ')) after++;

    html = html.substring(0, before) + '\n' + html.substring(after);
    fs.writeFileSync(f, html, 'utf8');
    removed++;
  } else {
    errors.push(f);
  }
}

console.log(`Removed: ${removed}`);
console.log(`Skipped: ${skipped}`);
if (errors.length) console.log(`Errors: ${errors.join(', ')}`);
