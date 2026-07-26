#!/usr/bin/env node
/**
 * Pre-deploy check для sakhva-travel.com
 * Запускать перед каждым: npx vercel deploy --prod
 * Использование: node scripts/predeploy-check.js [path/to/file.html]
 */

const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

let errors = 0;
let warnings = 0;

function ok(msg)   { console.log('  ✅', msg); }
function warn(msg) { console.log('  ⚠️ ', msg); warnings++; }
function err(msg)  { console.log('  ❌', msg); errors++; }

function checkHTML(filePath) {
  const rel = path.relative(ROOT, filePath);
  const html = fs.readFileSync(filePath, 'utf8');

  console.log(`\n── ${rel} (${(Buffer.byteLength(html)/1024).toFixed(1)}KB)`);

  // 1. Структура тегов
  const tagCheck = (tag) => {
    const o = (html.match(new RegExp(`<${tag}[\\s>]`,'g'))||[]).length;
    const c = (html.match(new RegExp(`</${tag}>`,'g'))||[]).length;
    if (o !== c) err(`<${tag}> не закрыт: open=${o} close=${c}`);
    else ok(`<${tag}> структура`);
  };
  tagCheck('section'); tagCheck('div'); tagCheck('nav');

  // 2. Дублирующиеся id
  const ids = (html.match(/id="([^"]+)"/g)||[]).map(i=>i.slice(4,-1));
  const idMap = {};
  ids.forEach(id => idMap[id]=(idMap[id]||0)+1);
  const dups = Object.entries(idMap).filter(([,v])=>v>1);
  if (dups.length) err(`Дублирующиеся id: ${dups.map(([k])=>k).join(', ')}`);
  else ok('Нет дублирующихся id');

  // 3. Обязательные SEO теги
  const seo = {
    'title':      /<title>[^<]{10,}<\/title>/.test(html),
    'description':/<meta name="description"/.test(html),
    'canonical':  /rel="canonical"/.test(html),
    'og:image':   /og:image/.test(html),
    'JSON-LD':    /application\/ld\+json/.test(html),
    'GA4':        /G-3X83YZHY6S/.test(html),
    'hreflang':   /hreflang/.test(html),
  };
  Object.entries(seo).forEach(([k,v]) => v ? ok(`SEO: ${k}`) : warn(`SEO отсутствует: ${k}`));

  // 4. Обязательные UI элементы (для страниц туров)
  if (filePath.includes('/tour/')) {
    const ui = {
      'burger menu':       html.includes('closeDrawer'),
      'footer':            html.includes('id="footer"'),
      'breadcrumbs':       html.includes('breadcrumb'),
      'WhatsApp CTA':      html.includes('wa.me/995511272623'),
    };
    Object.entries(ui).forEach(([k,v]) => v ? ok(`UI: ${k}`) : err(`UI отсутствует: ${k}`));
  }

  // 4b. GE-специфичные проверки (только для /ge/ страниц)
  if (filePath.includes('/ge/') || /\/ge\/index\.html$/.test(filePath)) {
    /<html[^>]*lang="ka"/.test(html) ? ok('GE: lang="ka"') : err('GE: нет lang="ka"');
    /hreflang="ka"/.test(html) ? ok('GE: hreflang ka') : err('GE: нет hreflang ka');
    const can = (html.match(/<link[^>]*rel="canonical"[^>]*>/)||[''])[0];
    if (!can) err('GE: нет canonical');
    else if (can.includes('/ge/')) ok('GE: canonical-self → /ge/');
    else err(`GE: canonical не /ge/ (${can.slice(0,80)})`);
    /noto-sans-georgian/.test(html) && /\/css\/ge\.css/.test(html)
      ? ok('GE: шрифт Noto + ge.css') : err('GE: нет preload шрифта/ge.css');
    const title = (html.match(/<title>(.*?)<\/title>/s)||[,''])[1];
    /[Ⴀ-ჿ]/.test(title) ? ok('GE: <title> на грузинском')
      : warn('GE: <title> без груз. вязи — возможно не переведён');
    const _hasRu = /hreflang="ru"/.test(html), _hasEn = /hreflang="en"/.test(html);
    if (_hasRu && _hasEn) ok('GE: квадра hreflang ru+en+ka');
    else if (_hasEn) warn('GE: hreflang en+ka без ru — кластер EN+GE (нет RU-двойника), проверь намеренность');
    else if (_hasRu) warn('GE: hreflang ru+ka без en — кластер RU+GE (нет EN-двойника), проверь намеренность');
    else err('GE: неполная квадра hreflang (нет ru и en)');
  }

  // 5. Проверка мёртвых CSS классов (определены но не используются в HTML)
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  if (styleMatch) {
    const css = styleMatch[1];
    const definedClasses = [...css.matchAll(/\.([a-zA-Z][a-zA-Z0-9_-]*)\s*\{/g)].map(m=>m[1]);
    const deadClasses = definedClasses.filter(cls => {
      const inHTML = new RegExp(`class="[^"]*${cls}[^"]*"`).test(html);
      return !inHTML;
    });
    if (deadClasses.length > 5) warn(`Мёртвых CSS классов: ${deadClasses.length} (${deadClasses.slice(0,5).join(', ')}...)`);
    else if (deadClasses.length > 0) warn(`Мёртвых CSS классов: ${deadClasses.length} (${deadClasses.join(', ')})`);
    else ok('Нет мёртвых CSS классов');
  }

  // 6. Конфликты: одинаковые CSS-свойства перекрывают друг друга
  // Ищем одинаковые классы определённые более 1 раза
  const styleMatch2 = html.match(/<style>([\s\S]*?)<\/style>/);
  if (styleMatch2) {
    const css = styleMatch2[1];
    const classBlocks = [...css.matchAll(/\.([\w-]+)\s*\{/g)].map(m=>m[1]);
    const classCount = {};
    classBlocks.forEach(c => classCount[c]=(classCount[c]||0)+1);
    const dupCSS = Object.entries(classCount).filter(([,v])=>v>1);
    if (dupCSS.length) warn(`CSS классы определены дважды: ${dupCSS.map(([k])=>k).join(', ')}`);
    else ok('Нет дублирующихся CSS блоков');
  }

  // 7. Размер файла (главная может быть крупнее)
  const kb = Buffer.byteLength(html)/1024;
  const isMain = filePath.endsWith('index.html') && !filePath.includes('/tour/') && !filePath.includes('/blog/');
  const sizeLimit = isMain ? 350 : 150;
  const sizeWarn  = isMain ? 200 : 100;
  if (kb > sizeLimit) err(`Файл слишком большой: ${kb.toFixed(0)}KB (>${sizeLimit}KB)`);
  else if (kb > sizeWarn) warn(`Файл большой: ${kb.toFixed(0)}KB — рассмотри оптимизацию`);
  else ok(`Размер OK: ${kb.toFixed(1)}KB`);

  // 8. Inline скрипты без nonce (CSP risk)
  const inlineScripts = (html.match(/<script(?![^>]*src=)[^>]*>/g)||[])
    .filter(s => !s.includes('application/ld+json') && !s.includes('dataLayer'));
  if (inlineScripts.length > 2) warn(`Inline скриптов: ${inlineScripts.length} (проверь CSP)`);
  else ok(`Inline скриптов: ${inlineScripts.length}`);
}

// Определяем файлы для проверки
const args = process.argv.slice(2);
let filesToCheck = [];

if (args.length > 0) {
  filesToCheck = args.map(a => path.resolve(a));
} else {
  // Проверяем все ключевые файлы
  filesToCheck = [
    path.join(ROOT, 'index.html'),
    ...fs.readdirSync(path.join(ROOT, 'tour'))
      .map(d => path.join(ROOT, 'tour', d, 'index.html'))
      .filter(f => fs.existsSync(f)),
  ];
}

console.log('┌─────────────────────────────────────────┐');
console.log('│  PRE-DEPLOY CHECK — sakhva-travel.com  │');
console.log('└─────────────────────────────────────────┘');

filesToCheck.forEach(f => {
  try { checkHTML(f); }
  catch(e) { console.log(`  ❌ Не удалось прочитать: ${f}`); errors++; }
});

console.log('\n══════════════════════════════════════════');
console.log(`ИТОГ: ошибок ${errors}, предупреждений ${warnings}`);
if (errors > 0) {
  console.log('🚫 ДЕПЛОЙ ЗАБЛОКИРОВАН — исправь ошибки');
  process.exit(1);
} else if (warnings > 0) {
  console.log('⚠️  Есть предупреждения — проверь вручную');
  process.exit(0);
} else {
  console.log('🚀 Всё чисто — можно деплоить');
  process.exit(0);
}
