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
const files = [
  ...findFiles(path.join(ROOT, 'blog')),
  ...findFiles(path.join(ROOT, 'en/blog'))
];

// Replace sync GA with deferred loading
const SYNC_GA = `<script async src="https://www.googletagmanager.com/gtag/js?id=G-3X83YZHY6S"></script>
<script>gtag('js',new Date());gtag('config','G-3X83YZHY6S');gtag('config','AW-8133499399');</script>`;

const DEFERRED_GA = `<script>
(function(){var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-3X83YZHY6S';
s.onload=function(){gtag('js',new Date());gtag('config','G-3X83YZHY6S');gtag('config','AW-8133499399')};
if('requestIdleCallback' in window){requestIdleCallback(function(){document.head.appendChild(s)},{timeout:3000})}
else{setTimeout(function(){document.head.appendChild(s)},2000)}})();
</script>`;

let fixed = 0, skipped = 0;

for (const f of files) {
  let html = fs.readFileSync(f, 'utf8');
  if (!html.includes('<script async src="https://www.googletagmanager.com/gtag/js?id=G-3X83YZHY6S">')) {
    skipped++;
    continue;
  }
  html = html.replace(SYNC_GA, DEFERRED_GA);
  fs.writeFileSync(f, html, 'utf8');
  fixed++;
}

console.log(`GA deferred: ${fixed}`);
console.log(`Skipped: ${skipped}`);
