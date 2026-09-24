#!/usr/bin/env node
// Fix P3: Move CTA blocks inside article-wrap
const fs = require('fs');
const path = require('path');
const blogDir = path.join(__dirname, '..', 'blog');

let fixed = 0;

function getDirs() {
  const results = [];
  for (const entry of fs.readdirSync(blogDir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      const fp = path.join(blogDir, entry.name, 'index.html');
      if (fs.existsSync(fp)) results.push({ name: entry.name, path: fp });
    }
  }
  return results;
}

for (const { name, path: fp } of getDirs()) {
  const html = fs.readFileSync(fp, 'utf8');
  const lines = html.split('\n');

  // Find article-wrap opening line
  let wrapStart = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('class="article-wrap"')) { wrapStart = i; break; }
  }
  if (wrapStart === -1) continue;

  // Find </article> line
  let articleEnd = -1;
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].includes('</article>')) { articleEnd = i; break; }
  }
  if (articleEnd === -1) continue;

  // Track div depth from wrapStart to find where article-wrap closes
  let depth = 0;
  let wrapClose = -1;
  for (let i = wrapStart; i < articleEnd; i++) {
    const line = lines[i];
    const opens = (line.match(/<div[\s>]/g) || []).length;
    const closes = (line.match(/<\/div>/g) || []).length;
    depth += opens - closes;
    if (depth === 0 && i > wrapStart) {
      wrapClose = i;
      break;
    }
  }

  if (wrapClose === -1 || wrapClose >= articleEnd - 1) continue;

  // Check if there are CTA blocks between wrapClose and articleEnd
  const between = lines.slice(wrapClose + 1, articleEnd);
  const hasCTA = between.some(l =>
    l.includes('background:#F0FDF4') ||
    l.includes('background:#EFF6FF') ||
    l.includes('Нужен частный гид') ||
    l.includes('Экскурсии из Тбилиси') ||
    l.includes('Трансфер из аэропорта') ||
    l.includes('Автор:') ||
    (l.includes('display:flex') && l.includes('border-radius:16px'))
  );

  if (!hasCTA) continue;

  // Reconstruct: move CTA lines before the wrapClose line
  const before = lines.slice(0, wrapClose);
  const ctaContent = lines.slice(wrapClose + 1, articleEnd);
  const wrapCloseLine = lines[wrapClose]; // </div> that closes article-wrap
  const rest = lines.slice(articleEnd); // </article> and beyond

  const newLines = [...before, ...ctaContent, wrapCloseLine, ...rest];
  fs.writeFileSync(fp, newLines.join('\n'));
  fixed++;
  console.log(`✅ ${name}`);
}

console.log(`\nFixed ${fixed} files.`);
