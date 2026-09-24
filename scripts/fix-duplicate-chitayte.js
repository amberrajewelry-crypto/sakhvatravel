#!/usr/bin/env node
// Remove duplicate "Читайте также" blocks - keep only the first occurrence
const fs = require('fs');
const path = require('path');

const files = [
  'khachapuri-po-adzharski', 'gruzinskoe-vino-gid', 'kazbegi-iz-tbilisi-2026',
  'tseny-v-tbilisi-2026', 'noviy-god-v-gruzii', 'kakheti-osenyu',
  'tbilisi-s-detmi-chto-posmotret', 'skolko-stoit-otdyh-v-gruzii',
  'gid-tbilisi-vs-gid-gruziya', 'gruzinskaya-kukhnya-chto-poprobovat',
  'skolko-stoit-gid-tbilisi', 'oshibki-turistov-tbilisi', 'gruziya-perviy-raz',
  'viza-v-gruziyu-2026', 'ekskursii-v-tbilisi', 'gruziya-v-sentyabre',
  'kutaisi-iz-tbilisi', 'voenno-gruzinskaya-doroga'
];

let fixed = 0;

for (const name of files) {
  const fp = path.join(__dirname, '..', 'blog', name, 'index.html');
  if (!fs.existsSync(fp)) { console.log(`skip: ${name}`); continue; }

  let html = fs.readFileSync(fp, 'utf8');
  const lines = html.split('\n');

  // Find all lines containing "Читайте также"
  const indices = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('Читайте также')) indices.push(i);
  }

  if (indices.length <= 1) continue;

  // For each duplicate (2nd, 3rd, etc.), find the enclosing <div>...</div> block and remove it
  const toRemove = new Set();
  for (let k = 1; k < indices.length; k++) {
    const lineIdx = indices[k];
    // Search backward for opening <div
    let blockStart = lineIdx;
    for (let j = lineIdx; j >= Math.max(0, lineIdx - 5); j--) {
      if (lines[j].match(/<div\s+style=/)) { blockStart = j; break; }
      if (lines[j].match(/<p\s.*Читайте также/)) { blockStart = j; break; }
    }
    // Search forward for closing </div>
    let blockEnd = lineIdx;
    let depth = 0;
    for (let j = blockStart; j < Math.min(lines.length, blockStart + 15); j++) {
      depth += (lines[j].match(/<div[\s>]/g) || []).length;
      depth -= (lines[j].match(/<\/div>/g) || []).length;
      if (depth <= 0) { blockEnd = j; break; }
    }
    for (let j = blockStart; j <= blockEnd; j++) toRemove.add(j);
  }

  if (toRemove.size === 0) continue;

  const newLines = lines.filter((_, i) => !toRemove.has(i));
  fs.writeFileSync(fp, newLines.join('\n'));
  fixed++;
  console.log(`✅ ${name}: removed ${toRemove.size} duplicate lines (blocks ${indices.length - 1})`);
}

console.log(`\nFixed ${fixed} files.`);
