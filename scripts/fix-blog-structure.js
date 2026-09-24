#!/usr/bin/env node
// Fix blog structural issues: P2 (duplicate "Читайте также"), P3 (CTA outside wrap), P5 (📸 placeholders)
const fs = require('fs');
const path = require('path');
const blogDir = path.join(__dirname, '..', 'blog');

let totalFixed = 0;
let filesFixed = 0;

function getArticleDirs(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      const indexPath = path.join(dir, entry.name, 'index.html');
      if (fs.existsSync(indexPath)) results.push(indexPath);
    }
  }
  return results;
}

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;
  const fixes = [];
  const rel = path.relative(path.join(__dirname, '..'), filePath);

  // P5: Remove 📸 photo placeholders
  const placeholderRe = /<div class="photo-ph">.*?<\/div>\n?/g;
  const placeholderCount = (html.match(placeholderRe) || []).length;
  if (placeholderCount > 0) {
    html = html.replace(placeholderRe, '');
    fixes.push(`P5: removed ${placeholderCount} photo placeholders`);
  }

  // P2: Remove duplicate "Читайте также" blocks
  // Pattern: <div style="background:#F9FAFB...">...<p ...>Читайте также:</p>...<a ...>...</a>...</div>
  const chitayteRe = /<div style="background:#F9FAFB;border-radius:12px;padding:20px 24px;margin:32px 0">\s*<p[^>]*>Читайте также:<\/p>\s*(?:<a[^>]*>[^<]*<\/a>\s*)+<\/div>/g;
  const chitayteMatches = html.match(chitayteRe);
  if (chitayteMatches && chitayteMatches.length > 1) {
    // Keep first, remove subsequent
    let count = 0;
    html = html.replace(chitayteRe, (match) => {
      count++;
      if (count > 1) {
        fixes.push(`P2: removed duplicate "Читайте также" block #${count}`);
        return '';
      }
      return match;
    });
  }

  // P3: Move CTA blocks inside article-wrap
  // Pattern: </div>\n</div>\n\n<green CTA blocks>\n\n</div>\n</article>
  // The issue is CTA blocks appear after article-wrap closes
  // We need to detect: closing of article-wrap followed by CTA divs followed by </article>

  // Strategy: Find the pattern where </div> (article-body) </div> (article-wrap) is followed by
  // CTA-style divs (background:#F0FDF4 or author bio or background:#EFF6FF)
  // Then move those divs before the article-wrap closing </div>

  const ctaPattern = /(<\/div><!-- \/\.article-body -->\n*)([\s\S]*?)(\n*<\/div>\s*\n*<\/article>)/;
  // This won't work for all cases. Let me try a different approach.

  // Find the last </div>\n</article> and check if CTA blocks are between article-wrap close and article close
  const lines = html.split('\n');

  // Find article-wrap open and close
  let articleWrapOpen = -1;
  let articleBodyOpen = -1;
  let articleBodyClose = -1;
  let articleClose = -1;

  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('class="article-wrap"')) articleWrapOpen = i;
    if (lines[i].includes('class="article-body"')) articleBodyOpen = i;
    if (lines[i].includes('<!-- /.article-body -->')) articleBodyClose = i;
    if (lines[i].includes('</article>')) articleClose = i;
  }

  // If we have article close, look for CTA blocks between article-wrap area and article close
  if (articleClose > 0 && articleWrapOpen > 0) {
    // Find all green CTA blocks (background:#F0FDF4, author bio with flex, background:#EFF6FF guide CTA)
    // that are outside article-wrap (after the second-to-last </div> before </article>)

    // Count divs to find where article-wrap closes
    let depth = 0;
    let articleWrapClose = -1;
    for (let i = articleWrapOpen; i < articleClose; i++) {
      const openCount = (lines[i].match(/<div[\s>]/g) || []).length;
      const closeCount = (lines[i].match(/<\/div>/g) || []).length;
      depth += openCount - closeCount;
      if (depth === 0 && i > articleWrapOpen) {
        articleWrapClose = i;
        break;
      }
    }

    if (articleWrapClose > 0 && articleWrapClose < articleClose - 1) {
      // There's content between article-wrap close and article close
      const ctaLines = lines.slice(articleWrapClose + 1, articleClose).filter(l => l.trim());
      const hasCTA = ctaLines.some(l =>
        l.includes('background:#F0FDF4') ||
        l.includes('background:#EFF6FF') ||
        l.includes('Автор:') ||
        l.includes('Трансфер') ||
        l.includes('Экскурсии из Тбилиси') ||
        l.includes('Нужен частный гид')
      );

      if (hasCTA && ctaLines.length > 0) {
        // Move these lines before the article-wrap closing </div>
        const ctaContent = lines.slice(articleWrapClose + 1, articleClose);
        const before = lines.slice(0, articleWrapClose);
        const wrapClose = [lines[articleWrapClose]]; // </div> for article-wrap
        const after = lines.slice(articleClose); // </article> and beyond

        const newLines = [...before, ...ctaContent, ...wrapClose, ...after];
        html = newLines.join('\n');
        fixes.push(`P3: moved ${ctaLines.length} CTA lines inside article-wrap`);
      }
    }
  }

  if (html !== original) {
    fs.writeFileSync(filePath, html);
    filesFixed++;
    totalFixed += fixes.length;
    console.log(`✅ ${rel}: ${fixes.join(', ')}`);
  }
}

const files = getArticleDirs(blogDir);
console.log(`Scanning ${files.length} blog articles...\n`);

for (const f of files) {
  try {
    fixFile(f);
  } catch (e) {
    console.error(`❌ ${path.relative(path.join(__dirname, '..'), f)}: ${e.message}`);
  }
}

console.log(`\nDone: ${filesFixed} files fixed, ${totalFixed} total fixes applied.`);
