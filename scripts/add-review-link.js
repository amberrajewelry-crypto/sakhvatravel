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
const allFiles = [
  path.join(ROOT, 'index.html'),
  path.join(ROOT, 'en/index.html'),
  ...findFiles(path.join(ROOT, 'tour')),
  ...findFiles(path.join(ROOT, 'en/tour')),
  ...findFiles(path.join(ROOT, 'blog')),
  ...findFiles(path.join(ROOT, 'en/blog')),
  ...findFiles(path.join(ROOT, 'tours')),
  ...findFiles(path.join(ROOT, 'en/tours')),
  ...findFiles(path.join(ROOT, 'about')),
  ...findFiles(path.join(ROOT, 'chastniy-gid-tbilisi')),
  ...findFiles(path.join(ROOT, 'ekskursiya')),
].filter(f => fs.existsSync(f));

// Google review link via Maps CID
const REVIEW_LINK_RU = `<a href="https://www.google.com/maps?cid=14070083063461040701&action=write-review" target="_blank" rel="noopener" style="color:#6B7280;font-size:14px;text-decoration:none;padding:8px 0;display:inline-block">Оставить отзыв ★</a>`;
const REVIEW_LINK_EN = `<a href="https://www.google.com/maps?cid=14070083063461040701&action=write-review" target="_blank" rel="noopener" style="color:#6B7280;font-size:14px;text-decoration:none;padding:8px 0;display:inline-block">Leave a review ★</a>`;

let added = 0, skipped = 0;

for (const f of allFiles) {
  let html = fs.readFileSync(f, 'utf8');

  // Skip if already has review link
  if (html.includes('action=write-review')) {
    skipped++;
    continue;
  }

  const isEN = f.includes('/en/');
  const link = isEN ? REVIEW_LINK_EN : REVIEW_LINK_RU;

  // Add after the email link in footer contacts
  // Pattern: foot-email link followed by script
  const marker = `})();</script>`;
  const footIdx = html.lastIndexOf(marker);
  if (footIdx !== -1) {
    const insertPos = footIdx + marker.length;
    html = html.substring(0, insertPos) + '\n' + link + html.substring(insertPos);
    fs.writeFileSync(f, html, 'utf8');
    added++;
  } else {
    skipped++;
  }
}

console.log(`Review link added: ${added}`);
console.log(`Skipped: ${skipped}`);
