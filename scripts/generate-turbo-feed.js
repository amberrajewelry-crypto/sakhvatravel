#!/usr/bin/env node
// Generate Yandex Turbo Pages RSS feed from blog articles and tour pages
const fs = require('fs');
const path = require('path');

const BASE = 'https://sakhva-travel.com';
const ROOT = path.resolve(__dirname, '..');

function extractMeta(html, property) {
  const m = html.match(new RegExp(`<meta\\s+(?:name|property)="${property}"\\s+content="([^"]*)"`, 'i'))
    || html.match(new RegExp(`content="([^"]*)"\\s+(?:name|property)="${property}"`, 'i'));
  return m ? m[1] : '';
}

function extractTag(html, tag) {
  const m = html.match(new RegExp(`<${tag}[^>]*>([^<]*)</${tag}>`, 'i'));
  return m ? m[1].trim() : '';
}

function extractArticleBody(html) {
  const start = html.indexOf('<div class="article-body">');
  if (start < 0) return '';
  let depth = 0;
  let i = start;
  let bodyStart = -1;
  for (; i < html.length; i++) {
    if (html.substring(i, i + 4) === '<div') {
      if (bodyStart < 0) bodyStart = i;
      depth++;
    }
    if (html.substring(i, i + 6) === '</div>') {
      depth--;
      if (depth === 0) break;
    }
  }
  let body = html.substring(start + '<div class="article-body">'.length, i);

  // Clean up: remove scripts, styles, forms, CTAs, photo placeholders
  body = body.replace(/<script[\s\S]*?<\/script>/gi, '');
  body = body.replace(/<style[\s\S]*?<\/style>/gi, '');
  body = body.replace(/<form[\s\S]*?<\/form>/gi, '');
  body = body.replace(/<div class="article-cta[\s\S]*?<\/div>\s*<\/div>/gi, '');
  body = body.replace(/<div class="blog-discount-btn[\s\S]*?<\/div>/gi, '');
  body = body.replace(/<div class="photo-ph[^"]*">[^<]*<\/div>/gi, '');
  body = body.replace(/<nav class="article-toc[\s\S]*?<\/nav>/gi, '');
  body = body.replace(/<div class="author-byline[\s\S]*?<\/div>\s*<\/div>/gi, '');
  body = body.replace(/<div class="key-fact[^>]*>[\s\S]*?<\/div>/gi, '');
  body = body.replace(/<div class="review-quote[\s\S]*?<\/div>\s*<\/div>/gi, '');

  // Fix relative image URLs
  body = body.replace(/src="\//g, `src="${BASE}/`);
  body = body.replace(/href="\//g, `href="${BASE}/`);

  // Remove inline styles (Turbo doesn't need them)
  body = body.replace(/ style="[^"]*"/gi, '');

  // Remove class attributes
  body = body.replace(/ class="[^"]*"/gi, '');

  // Remove empty divs
  body = body.replace(/<div>\s*<\/div>/gi, '');

  // Keep only allowed tags: h1-h6, p, figure, img, a, ul, ol, li, strong, em, br, table, tr, td, th
  // Remove other divs but keep content
  body = body.replace(/<\/?div[^>]*>/gi, '');
  body = body.replace(/<\/?span[^>]*>/gi, '');
  body = body.replace(/<\/?section[^>]*>/gi, '');

  // Clean up whitespace
  body = body.replace(/\n{3,}/g, '\n\n').trim();

  return body;
}

function toRFC822(dateStr) {
  if (!dateStr) return new Date().toUTCString();
  const d = new Date(dateStr + 'T12:00:00+04:00');
  return d.toUTCString();
}

function escapeXml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ─── BLOG ARTICLES ───
function processBlog(dir, langPrefix) {
  const items = [];
  const blogDir = path.join(ROOT, dir);
  if (!fs.existsSync(blogDir)) return items;

  const slugs = fs.readdirSync(blogDir).filter(f => {
    const p = path.join(blogDir, f, 'index.html');
    return f !== 'index.html' && fs.existsSync(p);
  });

  for (const slug of slugs) {
    try {
      const filePath = path.join(blogDir, slug, 'index.html');
      const html = fs.readFileSync(filePath, 'utf-8');

      const title = extractMeta(html, 'og:title') || extractTag(html, 'title');
      const desc = extractMeta(html, 'description');
      const image = extractMeta(html, 'og:image') || `${BASE}/images/blog/${slug}.webp`;
      const pubDate = extractMeta(html, 'article:published_time');
      const canonical = `${BASE}/${dir}${slug}/`;
      const body = extractArticleBody(html);

      if (!title || !body || body.length < 200) {
        console.log(`SKIP (thin): ${dir}${slug}/ (${body.length} chars)`);
        continue;
      }

      items.push({
        link: canonical,
        topic: title,
        pubDate: toRFC822(pubDate),
        image,
        body
      });
    } catch (e) {
      console.error(`ERROR: ${dir}${slug}/: ${e.message}`);
    }
  }
  return items;
}

// ─── TOUR PAGES ───
function processTours(dir) {
  const items = [];
  const tourDir = path.join(ROOT, dir);
  if (!fs.existsSync(tourDir)) return items;

  const slugs = fs.readdirSync(tourDir).filter(f => {
    const p = path.join(tourDir, f, 'index.html');
    return f !== 'index.html' && fs.existsSync(p);
  });

  for (const slug of slugs) {
    try {
      const filePath = path.join(tourDir, slug, 'index.html');
      const html = fs.readFileSync(filePath, 'utf-8');

      const title = extractMeta(html, 'og:title') || extractTag(html, 'title');
      const desc = extractMeta(html, 'description');
      const image = extractMeta(html, 'og:image') || `${BASE}/images/${slug}-tour.webp`;
      const pubDate = extractMeta(html, 'article:published_time') || '2026-05-01';
      const canonical = `${BASE}/${dir}${slug}/`;
      const body = extractArticleBody(html);

      // Build turbo content from description + body
      let content = '';
      if (desc) content += `<p>${escapeXml(desc)}</p>\n`;
      if (body && body.length > 100) {
        content += body;
      }

      if (!title || content.length < 100) {
        console.log(`SKIP (thin tour): ${dir}${slug}/ (${content.length} chars)`);
        continue;
      }

      items.push({
        link: canonical,
        topic: title,
        pubDate: toRFC822(pubDate),
        image,
        body: content
      });
    } catch (e) {
      console.error(`ERROR: ${dir}${slug}/: ${e.message}`);
    }
  }
  return items;
}

// ─── GENERATE FEED ───
const blogRU = processBlog('blog/');
const tourRU = processTours('ekskursiya/');

console.log(`\nBlog RU: ${blogRU.length} items`);
console.log(`Tours RU: ${tourRU.length} items`);

const allItems = [...blogRU, ...tourRU];
console.log(`Total: ${allItems.length} items`);

let xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:yandex="http://news.yandex.ru/schemas/turbo/" xmlns:media="http://search.yahoo.com/mrss/" xmlns:turbo="http://turbo.yandex.ru" version="2.0">
<channel>
<title>Sakhva Travel — Туры и блог о Грузии</title>
<link>${BASE}/</link>
<description>Частный гид по Грузии. Блог, маршруты, экскурсии от Тимура.</description>
<language>ru</language>
<turbo:analytics type="Yandex" id="109038950"></turbo:analytics>
`;

for (const item of allItems) {
  xml += `<item turbo="true">
  <link>${item.link}</link>
  <turbo:topic>${escapeXml(item.topic)}</turbo:topic>
  <pubDate>${item.pubDate}</pubDate>
  <turbo:content><![CDATA[
    <header>
      <h1>${escapeXml(item.topic)}</h1>
      <figure><img src="${item.image}"/></figure>
    </header>
    ${item.body}
    <div data-block="widget-feedback" data-stick="false">
      <div data-type="call" data-url="tel:+995511272623">Позвонить</div>
      <div data-type="chat" data-url="https://wa.me/995511272623">WhatsApp</div>
    </div>
  ]]></turbo:content>
</item>
`;
}

xml += `</channel>
</rss>`;

const outPath = path.join(ROOT, 'turbo-feed.xml');
fs.writeFileSync(outPath, xml, 'utf-8');

const sizeMB = (Buffer.byteLength(xml, 'utf-8') / 1024 / 1024).toFixed(2);
console.log(`\nWritten: turbo-feed.xml (${sizeMB} MB, ${allItems.length} items)`);
