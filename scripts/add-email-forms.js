#!/usr/bin/env node
/**
 * Add email collection forms to all pages:
 * 1. Lead magnet before footer (all pages)
 * 2. Email CTA after blog articles (blog pages only)
 */
const fs = require('fs');
const path = require('path');
// no glob needed, using manual walk

// Find files manually
function findFiles(dir, pattern) {
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

// Lead magnet HTML (inline, one-line style)
const MAGNET_RU = `
<section id="lead-magnet" style="position:relative;z-index:2;padding:32px clamp(16px,3.5vw,56px);background:#fff;border-top:1px solid #E8E0D8">
<div style="max-width:760px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap">
<p style="font-family:'Lora',serif;font-size:17px;font-weight:400;color:#111827;letter-spacing:-0.02em;margin:0">Гайд: 15 мест в Тбилиси не из путеводителя + скидка 5%</p>
<form class="magnet-form" onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='flex'" style="display:flex;gap:8px;flex-shrink:0">
<input type="email" placeholder="Email" required style="width:200px;padding:11px 16px;border:1px solid #E5E7EB;border-radius:8px;background:#fff;color:#111827;font-family:'Lora',serif;font-size:14px;outline:none">
<button type="submit" style="padding:11px 20px;background:#1A3D2E;color:#fff;border:none;border-radius:8px;font-family:'Lora',serif;font-size:14px;cursor:pointer;white-space:nowrap">Получить</button>
</form>
<div style="display:none;align-items:center;gap:8px"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A3D2E" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="font-family:'Lora',serif;font-size:15px;color:#111827">Отправлено — проверьте почту</span></div>
</div>
</section>
`;

const MAGNET_EN = `
<section id="lead-magnet" style="position:relative;z-index:2;padding:32px clamp(16px,3.5vw,56px);background:#fff;border-top:1px solid #E8E0D8">
<div style="max-width:760px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap">
<p style="font-family:'Lora',serif;font-size:17px;font-weight:400;color:#111827;letter-spacing:-0.02em;margin:0">Guide: 15 places in Tbilisi not in any guidebook + 5% off</p>
<form class="magnet-form" onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='flex'" style="display:flex;gap:8px;flex-shrink:0">
<input type="email" placeholder="Email" required style="width:200px;padding:11px 16px;border:1px solid #E5E7EB;border-radius:8px;background:#fff;color:#111827;font-family:'Lora',serif;font-size:14px;outline:none">
<button type="submit" style="padding:11px 20px;background:#1A3D2E;color:#fff;border:none;border-radius:8px;font-family:'Lora',serif;font-size:14px;cursor:pointer;white-space:nowrap">Get it</button>
</form>
<div style="display:none;align-items:center;gap:8px"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A3D2E" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span style="font-family:'Lora',serif;font-size:15px;color:#111827">Sent — check your inbox</span></div>
</div>
</section>
`;

// Blog email CTA (replaces article-cta block)
const BLOG_CTA_RU = `<div class="article-cta" style="text-align:left">
    <h3 style="font-family:'Lora',serif;font-weight:400;font-size:20px;margin-bottom:6px">Понравилась статья?</h3>
    <p style="margin-bottom:20px">Пришлём маршрут + скидку 5% на тур с гидом</p>
    <form class="blog-email-form" onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='block'" style="display:flex;gap:10px;max-width:420px">
      <input type="email" placeholder="Email" required style="flex:1;padding:12px 16px;border:1px solid rgba(255,255,255,0.12);border-radius:8px;background:rgba(255,255,255,0.06);color:#fff;font-family:'Lora',serif;font-size:14px;outline:none">
      <button type="submit" style="padding:12px 22px;background:#1A3D2E;color:#fff;border:none;border-radius:8px;font-family:'Lora',serif;font-size:14px;cursor:pointer;white-space:nowrap">Получить</button>
    </form>
    <div style="display:none"><p style="font-family:'Lora',serif;font-size:17px;color:#fff;margin-bottom:4px">Отправлено</p><p style="font-size:13px;color:rgba(255,255,255,.5)">Маршрут и промокод уже в пути</p></div>
  </div>`;

const BLOG_CTA_EN = `<div class="article-cta" style="text-align:left">
    <h3 style="font-family:'Lora',serif;font-weight:400;font-size:20px;margin-bottom:6px">Enjoyed this article?</h3>
    <p style="margin-bottom:20px">We'll send you a route + 5% off a tour with a guide</p>
    <form class="blog-email-form" onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='block'" style="display:flex;gap:10px;max-width:420px">
      <input type="email" placeholder="Email" required style="flex:1;padding:12px 16px;border:1px solid rgba(255,255,255,0.12);border-radius:8px;background:rgba(255,255,255,0.06);color:#fff;font-family:'Lora',serif;font-size:14px;outline:none">
      <button type="submit" style="padding:12px 22px;background:#1A3D2E;color:#fff;border:none;border-radius:8px;font-family:'Lora',serif;font-size:14px;cursor:pointer;white-space:nowrap">Get it</button>
    </form>
    <div style="display:none"><p style="font-family:'Lora',serif;font-size:17px;color:#fff;margin-bottom:4px">Sent</p><p style="font-size:13px;color:rgba(255,255,255,.5)">Route and promo code on the way</p></div>
  </div>`;

let stats = { magnetAdded: 0, magnetSkipped: 0, ctaReplaced: 0, ctaSkipped: 0, errors: [] };

// --- 1. Add lead magnet before footer ---
function addMagnet(filePath, isEN) {
  let html = fs.readFileSync(filePath, 'utf8');

  // Skip if already has lead-magnet
  if (html.includes('id="lead-magnet"') || html.includes('class="magnet-form"')) {
    stats.magnetSkipped++;
    return;
  }

  const magnet = isEN ? MAGNET_EN : MAGNET_RU;

  // Try all footer patterns
  const patterns = [
    '<footer id="footer" style="padding:16px clamp(16px,3.5vw,56px)">',
    '<footer id="footer">',
    '<footer>'
  ];

  let replaced = false;
  for (const pat of patterns) {
    if (html.includes(pat)) {
      html = html.replace(pat, magnet + '\n' + pat);
      replaced = true;
      break;
    }
  }

  if (replaced) {
    fs.writeFileSync(filePath, html, 'utf8');
    stats.magnetAdded++;
  } else {
    stats.errors.push(`No footer found: ${filePath}`);
  }
}

// --- 2. Replace article-cta in blog ---
function replaceBlogCTA(filePath, isEN) {
  let html = fs.readFileSync(filePath, 'utf8');

  // Skip if already replaced
  if (html.includes('class="blog-email-form"')) {
    stats.ctaSkipped++;
    return;
  }

  // Find and replace the article-cta div
  // Pattern: <div class="article-cta"> ... </div> (with content inside)
  const ctaRegex = /<div class="article-cta">[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/;
  const ctaSimple = /<div class="article-cta">[\s\S]*?<\/div>\s*<\/div>/;

  const newCTA = isEN ? BLOG_CTA_EN : BLOG_CTA_RU;

  if (html.includes('<div class="article-cta">')) {
    // Replace everything from <div class="article-cta"> to its closing
    // Count nested divs to find correct closing
    const startIdx = html.indexOf('<div class="article-cta">');
    if (startIdx === -1) { stats.ctaSkipped++; return; }

    let depth = 0;
    let endIdx = startIdx;
    let i = startIdx;
    while (i < html.length) {
      if (html.substring(i, i+4) === '<div') {
        depth++;
        i += 4;
      } else if (html.substring(i, i+6) === '</div>') {
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
      html = html.substring(0, startIdx) + newCTA + html.substring(endIdx);
      fs.writeFileSync(filePath, html, 'utf8');
      stats.ctaReplaced++;
    } else {
      stats.errors.push(`CTA parse error: ${filePath}`);
    }
  } else {
    stats.ctaSkipped++;
  }
}

// Process tour pages
const tourRU = findFiles(path.join(ROOT, 'tour'), 'index.html');
const tourEN = findFiles(path.join(ROOT, 'en/tour'), 'index.html');
const blogRU = findFiles(path.join(ROOT, 'blog'), 'index.html');
const blogEN = findFiles(path.join(ROOT, 'en/blog'), 'index.html');

// Also handle category pages
const toursRU = findFiles(path.join(ROOT, 'tours'), 'index.html');
const toursEN = findFiles(path.join(ROOT, 'en/tours'), 'index.html');

// Other pages
const otherPages = [
  path.join(ROOT, 'en/index.html'),
  path.join(ROOT, 'about/index.html'),
  path.join(ROOT, 'chastniy-gid-tbilisi/index.html'),
].filter(f => fs.existsSync(f));

console.log(`Files found:`);
console.log(`  Tour RU: ${tourRU.length}, Tour EN: ${tourEN.length}`);
console.log(`  Blog RU: ${blogRU.length}, Blog EN: ${blogEN.length}`);
console.log(`  Tours RU: ${toursRU.length}, Tours EN: ${toursEN.length}`);
console.log(`  Other: ${otherPages.length}`);

// Add magnet to all
tourRU.forEach(f => addMagnet(f, false));
tourEN.forEach(f => addMagnet(f, true));
blogRU.forEach(f => addMagnet(f, false));
blogEN.forEach(f => addMagnet(f, true));
toursRU.forEach(f => addMagnet(f, false));
toursEN.forEach(f => addMagnet(f, true));
otherPages.forEach(f => addMagnet(f, f.includes('/en/')));

// Replace blog CTA
blogRU.forEach(f => replaceBlogCTA(f, false));
blogEN.forEach(f => replaceBlogCTA(f, true));

console.log(`\nResults:`);
console.log(`  Magnet added: ${stats.magnetAdded}`);
console.log(`  Magnet skipped (already exists): ${stats.magnetSkipped}`);
console.log(`  Blog CTA replaced: ${stats.ctaReplaced}`);
console.log(`  Blog CTA skipped: ${stats.ctaSkipped}`);
if (stats.errors.length) {
  console.log(`  Errors:`);
  stats.errors.forEach(e => console.log(`    ${e}`));
}
