#!/usr/bin/env node
/**
 * Авто-пинг IndexNow (Bing + Yandex) для изменённых страниц.
 *
 * Использование:
 *   node scripts/indexnow-ping.js                 # авто: изменённые *.html из git (HEAD vs origin)
 *   node scripts/indexnow-ping.js a/index.html b/ # явный список путей/URL
 *   node scripts/indexnow-ping.js --last-commit   # файлы из последнего коммита
 *
 * Не требует credentials — чистый IndexNow POST. Google Indexing API
 * остаётся в scripts/boost-unindexed.py (нужен service-account).
 */
'use strict';
const { execSync } = require('child_process');
const https = require('https');

const HOST = 'sakhva-travel.com';
const KEY = 'DE25F3FA51D1F1E934763682A270AF53'; // совпадает с прод /DE25F3FA...txt и boost-unindexed.py
const BASE = `https://${HOST}`;

function fileToUrl(f) {
  if (/^https?:\/\//.test(f)) return f.replace(/\/index\.html$/, '/');
  let p = f.replace(/^\.\//, '').replace(/^\/+/, '');
  p = p.replace(/index\.html$/, '').replace(/\.html$/, '');
  if (p && !p.endsWith('/')) p += '/';
  return `${BASE}/${p}`;
}

function changedFiles() {
  const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
  if (args.length) return args;
  let range = 'origin/HEAD...HEAD';
  if (process.argv.includes('--last-commit')) range = 'HEAD~1...HEAD';
  let out = '';
  try {
    out = execSync(`git diff --name-only --diff-filter=ACMR ${range} -- '*.html'`, {
      encoding: 'utf8',
    });
  } catch {
    // origin/HEAD может отсутствовать — фолбэк на последний коммит
    out = execSync("git diff --name-only --diff-filter=ACMR HEAD~1...HEAD -- '*.html'", {
      encoding: 'utf8',
    });
  }
  return out.split('\n').map((s) => s.trim()).filter(Boolean);
}

function ping(urls) {
  const body = JSON.stringify({
    host: HOST,
    key: KEY,
    keyLocation: `${BASE}/${KEY}.txt`,
    urlList: urls,
  });
  const req = https.request(
    {
      hostname: 'api.indexnow.org',
      path: '/indexnow',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(body),
      },
    },
    (res) => {
      console.log(`IndexNow HTTP ${res.statusCode} (200/202 = принято)`);
      res.resume();
    }
  );
  req.on('error', (e) => console.error('IndexNow ошибка:', e.message));
  req.write(body);
  req.end();
}

function main() {
  const files = changedFiles();
  // исключаем не-прод пути
  const skip = /(^|\/)(scripts|node_modules|design-previews|demo|_preview|dashboard|links|test-results|qa-screenshots|screenshots)(\/|$)/;
  const urls = [...new Set(files.filter((f) => !skip.test(f)).map(fileToUrl))];
  if (!urls.length) {
    console.log('IndexNow: нет изменённых прод-страниц для пинга.');
    return;
  }
  console.log(`IndexNow: пингую ${urls.length} URL:`);
  urls.forEach((u) => console.log('  ' + u));
  ping(urls);
}

main();
