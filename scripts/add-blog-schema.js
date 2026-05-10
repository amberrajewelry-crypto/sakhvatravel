#!/usr/bin/env node
// Add BlogPosting JSON-LD schema to blog articles that don't have it
const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '..', 'blog');
const dirs = fs.readdirSync(blogDir).filter(d => {
  const p = path.join(blogDir, d, 'index.html');
  return fs.existsSync(p) && !fs.readFileSync(p, 'utf8').includes('BlogPosting');
});

console.log(`Found ${dirs.length} articles without BlogPosting schema`);

let count = 0;
for (const dir of dirs) {
  const filePath = path.join(blogDir, dir, 'index.html');
  let html = fs.readFileSync(filePath, 'utf8');

  // Extract meta values
  const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || '';
  const cleanTitle = title.replace(/ \| Sakhva Travel$/, '').trim();
  const desc = (html.match(/name="description"\s+content="([^"]+)"/) || [])[1] || '';
  const published = (html.match(/article:published_time"\s+content="([^"]+)"/) || [])[1] || '2026-04-01';
  const modified = (html.match(/article:modified_time"\s+content="([^"]+)"/) || [])[1] || published;
  const canonical = (html.match(/rel="canonical"\s+href="([^"]+)"/) || [])[1] || `https://sakhva-travel.com/blog/${dir}/`;
  const ogImage = (html.match(/og:image"\s+content="([^"]+)"/) || [])[1] || `https://sakhva-travel.com/images/blog/${dir}.webp`;
  const lang = (html.match(/<html\s+lang="([^"]+)"/) || [])[1] || 'ru';

  const schema = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": cleanTitle,
    "description": desc,
    "url": canonical,
    "datePublished": published,
    "dateModified": modified,
    "inLanguage": lang,
    "image": {
      "@type": "ImageObject",
      "url": ogImage,
      "width": 1200,
      "height": 630
    },
    "author": {
      "@type": "Person",
      "name": "Тимур",
      "url": "https://sakhva-travel.com/about/",
      "image": {
        "@type": "ImageObject",
        "url": "https://sakhva-travel.com/images/timur.webp",
        "width": 72,
        "height": 72
      }
    },
    "publisher": {
      "@type": "Organization",
      "name": "Sakhva Travel",
      "url": "https://sakhva-travel.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://sakhva-travel.com/images/logo-schema.webp",
        "width": 300,
        "height": 60
      }
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": canonical
    }
  };

  const scriptTag = `<script type="application/ld+json">\n${JSON.stringify(schema, null, 2)}\n</script>`;

  // Insert before </head>
  if (html.includes('</head>')) {
    html = html.replace('</head>', scriptTag + '\n</head>');
    fs.writeFileSync(filePath, html);
    count++;
    console.log(`+ ${dir}: "${cleanTitle.substring(0, 50)}..."`);
  } else {
    console.log(`! ${dir}: no </head> found, skipped`);
  }
}

console.log(`\nDone: ${count}/${dirs.length} articles updated`);
