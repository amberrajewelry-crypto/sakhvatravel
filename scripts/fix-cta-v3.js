#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const blogDir = path.join(__dirname, '..', 'blog');

let fixed = 0;

for (const entry of fs.readdirSync(blogDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const fp = path.join(blogDir, entry.name, 'index.html');
  if (!fs.existsSync(fp)) continue;

  const html = fs.readFileSync(fp, 'utf8');
  const lines = html.split('\n');

  // Find </article> line
  let articleEndLine = -1;
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].includes('</article>')) { articleEndLine = i; break; }
  }
  if (articleEndLine === -1) continue;

  // Search backwards from </article> to find the first standalone </div>
  // This should be the article-wrap closer
  let wrapCloseLine = -1;
  for (let i = articleEndLine - 1; i >= 0; i--) {
    if (lines[i].trim() === '</div>') { wrapCloseLine = i; break; }
  }
  if (wrapCloseLine === -1) continue;

  // Check if there's CTA content between wrapCloseLine and </article>
  const between = lines.slice(wrapCloseLine + 1, articleEndLine);
  const ctaMarkers = ['Нужен частный гид', 'Экскурсии из Тбилиси', 'Трансфер', 'Автор:'];
  const hasCTA = between.some(l => ctaMarkers.some(m => l.includes(m)));

  if (!hasCTA) continue;

  // Now find what closes before the CTA: search backwards from CTA start
  // The </div> at wrapCloseLine might close article-wrap
  // But there might be another </div> above that closes article-body
  // We need the CTA content to be INSIDE article-wrap but OUTSIDE article-body

  // Search backwards from wrapCloseLine to find another </div> (article-body closer)
  let bodyCloseLine = -1;
  for (let i = wrapCloseLine - 1; i >= 0; i--) {
    const trimmed = lines[i].trim();
    if (trimmed === '</div>' || trimmed === '</div><!-- /.article-body -->') {
      bodyCloseLine = i;
      break;
    }
  }

  // Check: is there content between bodyCloseLine and wrapCloseLine that's NOT CTA?
  // If bodyCloseLine is right before wrapCloseLine (or separated by whitespace),
  // then the CTA should go between them
  if (bodyCloseLine === -1) continue;

  // Move: take content from (wrapCloseLine+1 to articleEndLine-1),
  // put it between bodyCloseLine and wrapCloseLine
  const ctaContent = lines.slice(wrapCloseLine + 1, articleEndLine);
  if (ctaContent.filter(l => l.trim()).length === 0) continue;

  const newLines = [
    ...lines.slice(0, wrapCloseLine),      // everything up to wrap close
    ...ctaContent,                          // CTA blocks
    lines[wrapCloseLine],                   // </div> (wrap close)
    ...lines.slice(articleEndLine)          // </article> and rest
  ];

  fs.writeFileSync(fp, newLines.join('\n'));
  fixed++;
  console.log(`✅ ${entry.name}`);
}

console.log(`\nFixed ${fixed} files.`);
