#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const blogDir = path.join(__dirname, '..', 'blog');

let fixed = 0;

for (const entry of fs.readdirSync(blogDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const fp = path.join(blogDir, entry.name, 'index.html');
  if (!fs.existsSync(fp)) continue;

  let html = fs.readFileSync(fp, 'utf8');

  // Strategy: find the pattern where </div>\n</article> has CTA blocks before it
  // but after the article-wrap's natural close point
  // Simpler: find </div>\n</article> at the end, and check what's before it

  // Find last </article>
  const articleIdx = html.lastIndexOf('</article>');
  if (articleIdx === -1) continue;

  // Find the </div> just before </article> (the article-wrap closer)
  const beforeArticle = html.substring(0, articleIdx).trimEnd();

  // Look for the pattern: content-wrap closes, then CTA blocks appear outside
  // The CTA blocks have distinctive markers
  const ctaMarkers = ['Нужен частный гид', 'Экскурсии из Тбилиси', 'Трансфер из аэропорта'];

  // Check if any CTA marker exists after the article-wrap content
  // Find where article-body div closes (</div> with comment or just </div> followed by CTA)

  // Find the LAST "Читайте также" block - CTA blocks should come after it
  const chitayteIdx = html.lastIndexOf('Читайте также');
  if (chitayteIdx === -1) continue;

  // Find the </div> that closes the "Читайте также" block
  let searchFrom = chitayteIdx;
  let chitayteBlockEnd = html.indexOf('</div>', searchFrom);
  if (chitayteBlockEnd === -1) continue;
  chitayteBlockEnd = html.indexOf('\n', chitayteBlockEnd) + 1;

  // Everything between chitayteBlockEnd and </article> should be examined
  const afterChitayte = html.substring(chitayteBlockEnd, articleIdx);

  // Count </div> in this section - we expect article-body close and article-wrap close
  const closeDivs = (afterChitayte.match(/<\/div>/g) || []).length;
  const openDivs = (afterChitayte.match(/<div[\s>]/g) || []).length;

  // If there are CTA blocks AND closing divs mixed, restructure
  const hasCTA = ctaMarkers.some(m => afterChitayte.includes(m));
  if (!hasCTA) continue;

  // Find where the two closing </div> are (article-body and article-wrap)
  // and move CTA content between them
  const lines = afterChitayte.split('\n');

  // Find first standalone </div> (closes article-body)
  // Find second standalone </div> (closes article-wrap)
  let firstClose = -1, secondClose = -1;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line === '</div>' || line === '</div><!-- /.article-body -->') {
      if (firstClose === -1) firstClose = i;
      else if (secondClose === -1) { secondClose = i; break; }
    }
  }

  if (firstClose === -1 || secondClose === -1) continue;

  // Check: is there CTA content AFTER secondClose?
  const afterWrapClose = lines.slice(secondClose + 1).filter(l => l.trim());
  const ctaAfterWrap = afterWrapClose.some(l =>
    ctaMarkers.some(m => l.includes(m)) ||
    l.includes('background:#F0FDF4') ||
    l.includes('background:#EFF6FF') ||
    l.includes('Автор:')
  );

  if (!ctaAfterWrap) continue;

  // Move: take CTA lines from after secondClose, put them before secondClose
  const beforeWrapClose = lines.slice(0, secondClose);
  const wrapCloseLine = lines[secondClose];
  const ctaLines = lines.slice(secondClose + 1);

  const newAfter = [...beforeWrapClose, ...ctaLines, wrapCloseLine].join('\n');
  html = html.substring(0, chitayteBlockEnd) + newAfter + html.substring(articleIdx);

  fs.writeFileSync(fp, html);
  fixed++;
  console.log(`✅ ${entry.name}`);
}

console.log(`\nFixed ${fixed} files.`);
