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
  ...findFiles(path.join(ROOT, 'tour')),
  ...findFiles(path.join(ROOT, 'en/tour')),
  ...findFiles(path.join(ROOT, 'blog')),
  ...findFiles(path.join(ROOT, 'en/blog')),
  ...findFiles(path.join(ROOT, 'tours')),
  ...findFiles(path.join(ROOT, 'en/tours')),
  ...findFiles(path.join(ROOT, 'about')),
  ...findFiles(path.join(ROOT, 'chastniy-gid-tbilisi')),
  ...findFiles(path.join(ROOT, 'ekskursiya')),
  path.join(ROOT, 'en/index.html'),
].filter(f => fs.existsSync(f));

let added = 0, skipped = 0;

for (const f of allFiles) {
  let html = fs.readFileSync(f, 'utf8');

  if (html.includes('action=write-review')) {
    skipped++;
    continue;
  }

  const isEN = f.includes('/en/');
  const reviewText = isEN ? 'Leave a review ★' : 'Оставить отзыв ★';

  // Find </div> right before </footer> — that's foot-legal or foot-bottom
  // Add review link inside foot-legal
  if (html.includes('class="foot-legal"')) {
    const marker = 'class="foot-legal">';
    const idx = html.lastIndexOf(marker);
    if (idx !== -1) {
      const insertPos = idx + marker.length;
      const link = `<a href="https://www.google.com/maps?cid=14070083063461040701&action=write-review" target="_blank" rel="noopener">${reviewText}</a>`;
      html = html.substring(0, insertPos) + link + html.substring(insertPos);
      fs.writeFileSync(f, html, 'utf8');
      added++;
      continue;
    }
  }

  // Fallback: add before </footer>
  const footerEnd = html.lastIndexOf('</footer>');
  if (footerEnd !== -1) {
    const link = `<div style="text-align:center;padding:8px 0"><a href="https://www.google.com/maps?cid=14070083063461040701&action=write-review" target="_blank" rel="noopener" style="color:#6B7280;font-size:12px">${reviewText}</a></div>\n`;
    html = html.substring(0, footerEnd) + link + html.substring(footerEnd);
    fs.writeFileSync(f, html, 'utf8');
    added++;
    continue;
  }

  skipped++;
}

console.log(`Review link added: ${added}`);
console.log(`Skipped: ${skipped}`);
