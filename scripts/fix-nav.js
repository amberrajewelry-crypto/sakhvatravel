#!/usr/bin/env node
// Mass-fix navigation across all subpages
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

// New nav for RU subpages (links to main page anchors)
const RU_NAV = `<div class="nav-links">
    <a href="/#tours">Туры</a>
    <a href="/#guide">О нас</a>
    <a href="/#reviews">Отзывы</a>
    <a href="/blog/">Блог</a>
    <a href="/#faq">FAQ</a>
    <a href="/contacts/">Контакты</a>`;

// New nav for EN subpages
const EN_NAV = `<div class="nav-links">
    <a href="/en/#tours">Tours</a>
    <a href="/en/#guide">About</a>
    <a href="/en/#reviews">Reviews</a>
    <a href="/en/blog/">Blog</a>
    <a href="/en/#faq">FAQ</a>
    <a href="/en/contacts/">Contacts</a>`;

// New drawer for RU subpages
const RU_DRAWER_LINKS = `<a href="/#tours" onclick="closeDrawer()">Туры</a>
  <a href="/#guide" onclick="closeDrawer()">О нас</a>
  <a href="/#reviews" onclick="closeDrawer()">Отзывы</a>
  <a href="/blog/" onclick="closeDrawer()">Блог</a>
  <a href="/#faq" onclick="closeDrawer()">FAQ</a>
  <a href="/contacts/" onclick="closeDrawer()">Контакты</a>`;

// New drawer for EN subpages
const EN_DRAWER_LINKS = `<a href="/en/#tours" onclick="closeDrawer()">Tours</a>
  <a href="/en/#guide" onclick="closeDrawer()">About</a>
  <a href="/en/#reviews" onclick="closeDrawer()">Reviews</a>
  <a href="/en/blog/" onclick="closeDrawer()">Blog</a>
  <a href="/en/#faq" onclick="closeDrawer()">FAQ</a>
  <a href="/en/contacts/" onclick="closeDrawer()">Contacts</a>`;

function findHtmlFiles(dir) {
  let results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.name === '.vercel' || e.name === 'node_modules' || e.name === '.git') continue;
    if (e.isDirectory()) {
      results = results.concat(findHtmlFiles(full));
    } else if (e.name === 'index.html') {
      results.push(full);
    }
  }
  return results;
}

function isEN(filePath) {
  const rel = path.relative(ROOT, filePath);
  return rel.startsWith('en/') || rel.startsWith('en\\');
}

function isMainPage(filePath) {
  const rel = path.relative(ROOT, filePath);
  return rel === 'index.html' || rel === 'en/index.html';
}

let fixed = 0;
let skipped = 0;
let errors = [];

const files = findHtmlFiles(ROOT);

for (const file of files) {
  if (isMainPage(file)) {
    skipped++;
    continue;
  }

  let html = fs.readFileSync(file, 'utf8');
  const orig = html;
  const en = isEN(file);

  // Fix nav-links: replace content between <div class="nav-links"> and the nav-btn/lang-sw/</div>
  // Strategy: find <div class="nav-links"> and replace all <a> tags before the nav-btn or lang-sw
  const navRegex = /<div class="nav-links">\s*([\s\S]*?)(<a[^>]*class="nav-btn"[^>]*>|<div class="lang-sw">|<button[^>]*class="nav-btn")/;
  const navMatch = html.match(navRegex);

  if (navMatch) {
    const navContent = navMatch[1];
    const afterNav = navMatch[2];
    const newNav = en ? EN_NAV : RU_NAV;

    // Build replacement: new nav div opening + links + whatever comes after (btn/lang-sw)
    html = html.replace(
      `<div class="nav-links">\n` + navMatch[1] + navMatch[2],
      newNav + '\n    ' + afterNav
    );
    // Also try without newline
    if (html === orig.substring(0, html.length > 0 ? undefined : 0)) {
      html = orig; // reset if no change
    }
  }

  // Simpler approach: regex replace the nav-links block
  // Match from <div class="nav-links"> to the first nav-btn or lang-sw
  const navPattern = /(<div class="nav-links">)([\s\S]*?)(<(?:a|button)[^>]*(?:class="nav-btn"|onclick="openPayment")[^>]*>)/;
  const navM = orig.match(navPattern);

  if (navM) {
    const replacement = (en ? EN_NAV : RU_NAV) + '\n    ' + navM[3];
    html = orig.replace(navPattern, replacement);
  }

  // Fix drawer links: replace <a> tags after <div class="drawer" id="drawer"> until the first non-nav element
  const drawerPattern = /(<div class="drawer" id="drawer">)\s*((?:<a[^>]*onclick="closeDrawer\(\)"[^>]*>[^<]*<\/a>\s*)+)/;
  const drawerM = html.match(drawerPattern);

  if (drawerM) {
    const newDrawer = drawerM[1] + '\n  ' + (en ? EN_DRAWER_LINKS : RU_DRAWER_LINKS) + '\n  ';
    html = html.replace(drawerPattern, newDrawer);
  }

  // Remove standalone phone links in nav that weren't part of the pattern
  // Remove <a href="tel:+995511272623">+995 511 272 623</a> from nav area
  html = html.replace(/\s*<a href="tel:\+995511272623"[^>]*>\+995 511 272 623<\/a>/g, '');

  // Remove phone from drawer too
  html = html.replace(/\s*<a href="tel:\+995511272623"[^>]*onclick="closeDrawer\(\)"[^>]*>[^<]*<\/a>/g, '');

  if (html !== orig) {
    fs.writeFileSync(file, html, 'utf8');
    fixed++;
    console.log('FIXED:', path.relative(ROOT, file));
  } else {
    skipped++;
  }
}

console.log(`\nDone: ${fixed} fixed, ${skipped} skipped, ${files.length} total`);
