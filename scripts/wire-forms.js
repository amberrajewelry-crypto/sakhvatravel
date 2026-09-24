#!/usr/bin/env node
/**
 * Replace onsubmit handlers in magnet forms to call /api/subscribe
 */
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

const allFiles = [
  path.join(ROOT, 'index.html'),
  path.join(ROOT, 'en/index.html'),
  ...findFiles(path.join(ROOT, 'tour')),
  ...findFiles(path.join(ROOT, 'en/tour')),
  ...findFiles(path.join(ROOT, 'blog')),
  ...findFiles(path.join(ROOT, 'en/blog')),
  ...findFiles(path.join(ROOT, 'tours')),
  ...findFiles(path.join(ROOT, 'en/tours')),
  ...findFiles(path.join(ROOT, 'about')),
  ...findFiles(path.join(ROOT, 'chastniy-gid-tbilisi')),
].filter(f => fs.existsSync(f));

// Old onsubmit for magnet forms
const OLD_MAGNET = `onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='flex'"`;
const NEW_MAGNET = `onsubmit="event.preventDefault();var f=this,e=f.querySelector('input').value;f.style.display='none';f.nextElementSibling.style.display='flex';fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:e,source:'footer-magnet',lang:document.documentElement.lang||'ru'})}).catch(function(){})"`;

// Old onsubmit for quiz email
const OLD_QUIZ = `onsubmit="event.preventDefault();this.style.display='none';document.getElementById('qm-email-ok').style.display='flex'"`;
const NEW_QUIZ = `onsubmit="event.preventDefault();var f=this,e=f.querySelector('input').value;f.style.display='none';document.getElementById('qm-email-ok').style.display='flex';fetch('/api/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:e,source:'quiz',lang:document.documentElement.lang||'ru'})}).catch(function(){})"`;

let magnetFixed = 0, quizFixed = 0;

for (const f of allFiles) {
  let html = fs.readFileSync(f, 'utf8');
  let changed = false;

  if (html.includes(OLD_MAGNET)) {
    html = html.split(OLD_MAGNET).join(NEW_MAGNET);
    magnetFixed++;
    changed = true;
  }

  if (html.includes(OLD_QUIZ)) {
    html = html.split(OLD_QUIZ).join(NEW_QUIZ);
    quizFixed++;
    changed = true;
  }

  if (changed) fs.writeFileSync(f, html, 'utf8');
}

console.log(`Magnet forms wired: ${magnetFixed}`);
console.log(`Quiz forms wired: ${quizFixed}`);
console.log(`Total files: ${allFiles.length}`);
