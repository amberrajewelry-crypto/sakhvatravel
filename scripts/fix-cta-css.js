#!/usr/bin/env node
// Fix P3 via CSS: add .blog-cta-wrap class to limit CTA width
// For all blog pages, wrap orphaned CTA blocks in a centered container
const fs = require('fs');
const path = require('path');
const blogDir = path.join(__dirname, '..', 'blog');

let fixed = 0;

for (const entry of fs.readdirSync(blogDir, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const fp = path.join(blogDir, entry.name, 'index.html');
  if (!fs.existsSync(fp)) continue;

  let html = fs.readFileSync(fp, 'utf8');

  // Check if file has orphaned CTAs (green blocks outside article-wrap)
  // Pattern: </div>\n\n followed by CTA div with background:#F0FDF4 or #EFF6FF
  // that is NOT inside article-wrap

  // Simple approach: wrap all CTA blocks that appear after article-wrap closes
  // in a <div class="article-wrap"> container

  // Find the closing </div> of article-wrap by looking for content pattern:
  // </div> followed by CTA blocks followed by <script or end of body

  // Better: just add CSS to constrain these specific CTA blocks
  // Add inline max-width to orphaned CTA divs

  const ctaPatterns = [
    { find: '<div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:12px;padding:20px 24px;margin:32px 0">',
      replace: '<div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:12px;padding:20px 24px;margin:32px auto;max-width:760px">' },
    { find: '<div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:12px;padding:20px 24px;margin:32px 0"><p',
      replace: '<div style="background:#F0FDF4;border-left:4px solid #16A34A;border-radius:12px;padding:20px 24px;margin:32px auto;max-width:760px"><p' },
    { find: '<div style="background:#EFF6FF;border-left:4px solid #1A56DB;border-radius:12px;padding:20px 24px;margin:32px 0">',
      replace: '<div style="background:#EFF6FF;border-left:4px solid #1A56DB;border-radius:12px;padding:20px 24px;margin:32px auto;max-width:760px">' },
    { find: '<div style="display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;border-radius:16px;padding:24px;margin:32px 0">',
      replace: '<div style="display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;border-radius:16px;padding:24px;margin:32px auto;max-width:760px">' },
  ];

  let changed = false;
  for (const { find, replace } of ctaPatterns) {
    if (html.includes(find)) {
      html = html.split(find).join(replace);
      changed = true;
    }
  }

  if (changed) {
    fs.writeFileSync(fp, html);
    fixed++;
    console.log(`✅ ${entry.name}`);
  }
}

console.log(`\nFixed ${fixed} files with max-width:760px + margin:auto on CTA blocks.`);
