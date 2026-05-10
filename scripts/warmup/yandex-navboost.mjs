#!/usr/bin/env node
/**
 * Yandex NavBoost — targeted organic clicks on sakhva-travel.com
 *
 * Prerequisite: profiles must be warmed up (Day 1-3 via warmup.mjs).
 * This script simulates real Yandex searches → click on sakhva-travel.com
 * → browse 2-4 pages → spend 2-5 min on site.
 *
 * Usage:
 *   node yandex-navboost.mjs --all                    # all RU profiles
 *   node yandex-navboost.mjs --profiles 01,03,05      # specific profiles
 *   node yandex-navboost.mjs --all --queries 3        # 3 queries per profile
 *   node yandex-navboost.mjs --all --dry-run           # print plan, don't run
 *
 * Safety:
 *   - Only clicks ORGANIC results (skips ads)
 *   - Max 5 queries per profile per run
 *   - Randomized delays between actions
 *   - Logs everything to JSONL
 */

import { chromium } from 'playwright';
import { parseArgs } from 'node:util';
import { readFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------------------------------------------------------------------------
// .env
// ---------------------------------------------------------------------------
function loadEnv() {
  const p = resolve(__dirname, '.env');
  if (!existsSync(p)) return;
  for (const line of readFileSync(p, 'utf-8').split('\n')) {
    const m = line.match(/^\s*([\w]+)\s*=\s*(.+)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}
loadEnv();

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const CONFIG_PATH = resolve(__dirname, 'warmup-config.json');
function loadConfig() {
  if (!existsSync(CONFIG_PATH)) {
    console.error(`Config not found: ${CONFIG_PATH}`);
    process.exit(1);
  }
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

// ---------------------------------------------------------------------------
// Logger
// ---------------------------------------------------------------------------
const LOG_DIR = resolve(__dirname, 'logs');
if (!existsSync(LOG_DIR)) mkdirSync(LOG_DIR, { recursive: true });
const LOG_FILE = resolve(
  LOG_DIR,
  `navboost-${new Date().toISOString().slice(0, 10)}.jsonl`
);

function log(profileId, action, details = {}) {
  const entry = { ts: new Date().toISOString(), profile: profileId, action, ...details };
  appendFileSync(LOG_FILE, JSON.stringify(entry) + '\n');
  const lbl = details.url || details.query || '';
  console.log(`  [${action}] ${lbl} ${details.duration_s ? `(${details.duration_s}s)` : ''}`);
}

// ---------------------------------------------------------------------------
// Telegram (optional)
// ---------------------------------------------------------------------------
async function tgNotify(text) {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chatId) return;
  try {
    await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML' }),
    });
  } catch { /* non-critical */ }
}

// ---------------------------------------------------------------------------
// MLX helpers
// ---------------------------------------------------------------------------
const XCLI = '/Users/vladimir/mlx/deps/cli/xcli';

async function mlxSignIn() {
  const email = execSync(
    'security find-generic-password -a "$USER" -s "mlx-email" -w',
    { encoding: 'utf-8' }
  ).trim();
  const pass = execSync(
    'security find-generic-password -a "$USER" -s "mlx-password" -w',
    { encoding: 'utf-8' }
  ).trim();
  try {
    execSync(`${XCLI} login --username '${email}' --password '${pass}'`, {
      encoding: 'utf-8',
      timeout: 15000,
    });
    console.log('[MLX] Signed in');
  } catch (e) {
    console.log('[MLX] Login:', e.message?.split('\n')[0] || 'ok');
  }
}

async function mlxStartProfile(profileId) {
  const folderId = loadConfig().folder_id;
  let out;
  try {
    out = execSync(
      `${XCLI} profile-start --profile-id '${profileId}' -f '${folderId}' --automation puppeteer`,
      { encoding: 'utf-8', timeout: 90000 }
    );
  } catch (e) {
    const stdout = e.stdout || '';
    const match = stdout.match(/port[:\s]+(\d+)/i) || stdout.match(/(\d{5})/);
    if (match) return parseInt(match[1], 10);
    throw new Error(`xcli start failed: ${(e.stderr || '').slice(0, 200)}`);
  }
  const match = out.match(/port[:\s]+(\d+)/i) || out.match(/(\d{5})/);
  if (match) return parseInt(match[1], 10);
  throw new Error(`Cannot parse port: ${out.slice(0, 200)}`);
}

async function mlxStopProfile(profileId) {
  try {
    execSync(`${XCLI} profile-stop --profile-id '${profileId}'`, {
      encoding: 'utf-8',
      timeout: 15000,
    });
  } catch { /* ignore */ }
}

// ---------------------------------------------------------------------------
// Human-like helpers
// ---------------------------------------------------------------------------
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
const shuffle = (arr) => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

async function humanScroll(page, times = 3) {
  for (let i = 0; i < times; i++) {
    await page.mouse.wheel(0, rand(200, 600));
    await sleep(rand(800, 2500));
  }
}

async function humanType(page, selector, text) {
  try {
    await page.click(selector, { timeout: 10000 });
  } catch {
    await page.keyboard.press('Tab');
    await sleep(500);
  }
  await sleep(rand(200, 500));
  for (const ch of text) {
    await page.keyboard.type(ch, { delay: rand(50, 180) });
  }
}

// ---------------------------------------------------------------------------
// TARGET QUERIES — Yandex organic
// Sorted by priority: queries where we already rank (positions 2-20)
// ---------------------------------------------------------------------------
const TARGET_QUERIES = {
  // High priority — already ranking, need CTR boost
  high: [
    'казбеги тбилиси 2026',                        // pos 2.5
    'что делать в тбилиси в дождь',                 // pos 3-4
    'уплисцихе сколько нужно времени',              // pos 3
    'куда пойти в тбилиси в дождь',                 // pos 3
    'сколько денег нужно в грузию на 7 дней',        // pos 5.7
    'еда в тбилиси цены 2026',                      // pos 4.5
    'экскурсии из тбилиси в батуми',                // pos 6.5
    'сколько лари на 3 дня в тбилиси',              // pos 6.5
  ],
  // Medium — need to break into top 10
  medium: [
    'грузия для детей 2026',                         // pos 6.5
    'грузия сколько стоит 2026',                     // pos 10.3
    'мцхета как добраться из тбилиси',               // pos 8
    'сколько денег брать в грузию',                   // pos 10
    'нетуристические места тбилиси',                 // pos 10.5
    'экскурсия мцхета из тбилиси цены 2026',         // pos 8
    'трансфер тбилиси казбеги',                      // pos 8
    'серные бани тбилиси 2026',                      // pos 5
  ],
  // Low — commercial, far but important
  low: [
    'гид в тбилиси',                                // pos 17.5
    'туры в кахетию из тбилиси',                     // pos 15
    'частный гид тбилиси',
    'экскурсии тбилиси 2026',
    'тур в казбеги из тбилиси',
    'экскурсия кахетия тбилиси',
    'тур в батуми из тбилиси',
    'ночной тбилиси экскурсия',
  ],
};

// Internal pages to visit after landing (deep engagement signal)
const INTERNAL_PAGES = [
  '/tour/kazbegi/',
  '/tour/kakheti/',
  '/tour/mtskheta/',
  '/tour/night-tbilisi/',
  '/tour/batumi/',
  '/tour/walking/',
  '/tour/wine/',
  '/blog/',
  '/about/',
  '/tour/dinner/',
  '/tour/kutaisi/',
];

// ---------------------------------------------------------------------------
// CORE: Yandex search + targeted click
// ---------------------------------------------------------------------------

async function yandexSearch(page, query, profileId) {
  // Go to Yandex
  try {
    await page.goto('https://yandex.ru', {
      waitUntil: 'domcontentloaded',
      timeout: 20000,
    });
  } catch (e) {
    log(profileId, 'yandex_load_error', { error: e.message });
    return false;
  }
  await sleep(rand(1500, 3000));

  // Type query into search box
  const input = 'input#text, input.input__control, textarea.input__control';
  try {
    await page.waitForSelector(input, { timeout: 10000 });
  } catch {
    log(profileId, 'yandex_input_not_found');
    return false;
  }

  await humanType(page, input, query);
  await sleep(rand(600, 1500));
  await page.keyboard.press('Enter');

  try {
    await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
  } catch { /* ok */ }
  await sleep(rand(2000, 4000));

  log(profileId, 'yandex_search', { query });
  return true;
}

async function findAndClickTarget(page, profileId, maxPages = 2) {
  const TARGET_DOMAIN = 'sakhva-travel.com';

  for (let pageNum = 1; pageNum <= maxPages; pageNum++) {
    if (pageNum > 1) {
      log(profileId, 'yandex_next_page', { page: pageNum });
    }

    // Scroll SERP like a human — read results first
    await humanScroll(page, rand(2, 4));
    await sleep(rand(1000, 3000));

    // Find organic results (skip ads marked with data-cid or .Organic)
    // Yandex organic: li.serp-item a, .OrganicTitle-Link
    const organicLinks = page.locator([
      'a.OrganicTitle-Link',
      'li.serp-item:not([data-fast]) a.link',
      '.Organic a.Link',
      'li.serp-item .organic a[href]',
    ].join(', '));

    const count = await organicLinks.count().catch(() => 0);

    for (let i = 0; i < count; i++) {
      try {
        const href = await organicLinks.nth(i).getAttribute('href', { timeout: 3000 });
        if (href && href.includes(TARGET_DOMAIN)) {
          // Found our site! Pause before clicking (natural behavior)
          await sleep(rand(500, 2000));

          // Scroll to the element
          await organicLinks.nth(i).scrollIntoViewIfNeeded().catch(() => {});
          await sleep(rand(300, 800));

          await organicLinks.nth(i).click({ timeout: 10000 });

          try {
            await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
          } catch { /* ok */ }

          log(profileId, 'target_click', {
            url: href,
            position: i + 1,
            serp_page: pageNum,
          });
          return true;
        }
      } catch {
        continue;
      }
    }

    // Not found on this page — go to next
    if (pageNum < maxPages) {
      const nextBtn = page.locator(
        'a.Pager-Item_type_next, .pager__item_kind_next a, a[aria-label="next page"]'
      );
      if (await nextBtn.count() > 0) {
        await nextBtn.first().click().catch(() => {});
        await sleep(rand(2000, 5000));
        try {
          await page.waitForLoadState('domcontentloaded', { timeout: 20000 });
        } catch { /* ok */ }
      } else {
        break;
      }
    }
  }

  log(profileId, 'target_not_found');
  return false;
}

async function browseTarget(page, profileId) {
  // On-site engagement: scroll, read, visit internal pages
  const startTime = Date.now();

  // 1. Read main landing page (60-120s)
  const readTime = rand(60, 120);
  await humanScroll(page, rand(4, 8));
  await sleep(readTime * 1000);
  log(profileId, 'read_landing', { duration_s: readTime });

  // 2. Click 1-3 internal pages
  const pagesToVisit = rand(1, 3);
  const pages = shuffle(INTERNAL_PAGES).slice(0, pagesToVisit);

  for (const path of pages) {
    // Try clicking internal link or navigate directly
    const internalLink = page.locator(`a[href="${path}"], a[href*="${path}"]`).first();
    const linkExists = await internalLink.count().catch(() => 0);

    if (linkExists > 0) {
      try {
        await internalLink.scrollIntoViewIfNeeded();
        await sleep(rand(500, 1500));
        await internalLink.click({ timeout: 10000 });
      } catch {
        await page.goto(`https://sakhva-travel.com${path}`, {
          waitUntil: 'domcontentloaded',
          timeout: 20000,
        }).catch(() => {});
      }
    } else {
      await page.goto(`https://sakhva-travel.com${path}`, {
        waitUntil: 'domcontentloaded',
        timeout: 20000,
      }).catch(() => {});
    }

    await sleep(rand(2000, 4000));
    const pageReadTime = rand(30, 90);
    await humanScroll(page, rand(3, 6));
    await sleep(pageReadTime * 1000);
    log(profileId, 'visit_page', { url: path, duration_s: pageReadTime });
  }

  const totalTime = Math.round((Date.now() - startTime) / 1000);
  log(profileId, 'browse_complete', {
    pages_visited: pagesToVisit + 1,
    total_duration_s: totalTime,
  });
}

async function decoySearch(page, query, profileId) {
  // Search something unrelated, click a random result (not our site)
  if (!await yandexSearch(page, query, profileId)) return;
  await humanScroll(page, rand(2, 3));
  await sleep(rand(2000, 5000));

  // Click random organic result (NOT sakhva-travel)
  const links = page.locator('a.OrganicTitle-Link, li.serp-item a.link');
  const count = await links.count().catch(() => 0);
  if (count > 0) {
    for (let attempt = 0; attempt < 3; attempt++) {
      const idx = rand(0, Math.min(count - 1, 7));
      try {
        const href = await links.nth(idx).getAttribute('href', { timeout: 3000 });
        if (href && !href.includes('sakhva-travel')) {
          await links.nth(idx).click({ timeout: 10000 });
          const readSec = rand(10, 30);
          await sleep(readSec * 1000);
          log(profileId, 'decoy_click', { url: href, duration_s: readSec });
          await page.goBack().catch(() => {});
          await sleep(rand(1000, 3000));
          return;
        }
      } catch { continue; }
    }
  }
}

// ---------------------------------------------------------------------------
// DECOY QUERIES (natural Yandex behavior before/after target)
// ---------------------------------------------------------------------------
const DECOY_QUERIES = [
  'погода тбилиси', 'курс лари к рублю', 'рейсы в тбилиси',
  'тбилиси отели цены', 'грузия виза 2026', 'тбилиси аэропорт как добраться',
  'грузинская кухня рецепты', 'вино грузия купить', 'грузия безопасность 2026',
  'тбилиси фото', 'грузия отзывы туристов', 'кавказ горы фото',
  'батуми погода', 'авиабилеты тбилиси дешевые', 'бронирование отелей грузия',
];

// ---------------------------------------------------------------------------
// Main session per profile
// ---------------------------------------------------------------------------

async function runProfile(profileCfg, queriesPerRun) {
  const { id: profileId, name, persona, lang } = profileCfg;

  // Only RU profiles for Yandex
  if (lang !== 'ru') {
    console.log(`  [SKIP] ${name} — EN profile, Yandex only for RU`);
    return;
  }

  console.log(`\n--- ${name} (${persona}) ---`);
  log(profileId, 'session_start', { name, persona });

  let port;
  try {
    port = await mlxStartProfile(profileId);
  } catch (e) {
    log(profileId, 'start_error', { error: e.message });
    console.log(`  [ERROR] Cannot start: ${e.message}`);
    return;
  }

  let browser;
  try {
    // Wait for browser to be ready for CDP connection
    await sleep(5000);
    const cdpUrl = `http://127.0.0.1:${port}`;
    let cdpRetries = 3;
    while (cdpRetries > 0) {
      try {
        browser = await chromium.connectOverCDP(cdpUrl, { timeout: 30000 });
        break;
      } catch (cdpErr) {
        cdpRetries--;
        if (cdpRetries === 0) throw cdpErr;
        log(profileId, 'cdp_retry', { remaining: cdpRetries });
        await sleep(5000);
      }
    }
    const ctx = browser.contexts()[0] || await browser.newContext();
    const page = ctx.pages()[0] || await ctx.newPage();

    // Select queries for this session
    const allTarget = [
      ...shuffle(TARGET_QUERIES.high).slice(0, 2),
      ...shuffle(TARGET_QUERIES.medium).slice(0, 1),
      ...shuffle(TARGET_QUERIES.low).slice(0, 1),
    ];
    const queries = shuffle(allTarget).slice(0, queriesPerRun);
    const decoys = shuffle(DECOY_QUERIES).slice(0, rand(1, 2));

    // Session pattern: decoy → target → browse → decoy → target → ...
    // Start with a decoy to warm up Yandex session
    if (decoys.length > 0) {
      await decoySearch(page, decoys[0], profileId);
      await sleep(rand(3000, 8000));
    }

    for (let i = 0; i < queries.length; i++) {
      const query = queries[i];
      log(profileId, 'target_query_start', { query, index: i + 1 });

      // Search on Yandex
      if (!await yandexSearch(page, query, profileId)) continue;

      // Find and click sakhva-travel.com
      const found = await findAndClickTarget(page, profileId, 2);

      if (found) {
        // Browse the site — deep engagement
        await browseTarget(page, profileId);

        // Go back to Yandex (important: shows site was satisfying)
        // DON'T go back immediately — long dwell time is the signal
      } else {
        // Site not found for this query — just scroll SERP
        await humanScroll(page, rand(2, 4));
        await sleep(rand(3000, 8000));
      }

      // Pause between queries (natural behavior)
      if (i < queries.length - 1) {
        await sleep(rand(5000, 15000));

        // Occasional decoy between targets
        if (Math.random() < 0.3 && decoys.length > 1) {
          await decoySearch(page, decoys[decoys.length - 1], profileId);
          await sleep(rand(3000, 8000));
        }
      }
    }

    log(profileId, 'session_complete', {
      queries_attempted: queries.length,
    });
  } catch (e) {
    log(profileId, 'session_error', { error: e.message });
    console.log(`  [ERROR] ${e.message}`);
  } finally {
    if (browser) await browser.close().catch(() => {});
    await mlxStopProfile(profileId);
    await sleep(rand(2000, 5000));
  }
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
const { values: args } = parseArgs({
  options: {
    all: { type: 'boolean', default: false },
    profiles: { type: 'string', default: '' },
    queries: { type: 'string', default: '3' },
    'dry-run': { type: 'boolean', default: false },
  },
});

const config = loadConfig();
const queriesPerRun = Math.min(parseInt(args.queries, 10) || 3, 5);

// Parse profiles — config.profiles can be object {id: {...}} or array
let profiles;
if (Array.isArray(config.profiles)) {
  profiles = config.profiles;
} else {
  profiles = Object.entries(config.profiles).map(([id, p]) => ({ id, ...p }));
}

if (!args.all && args.profiles) {
  const ids = args.profiles.split(',').map((s) => s.trim());
  profiles = profiles.filter((p) =>
    ids.some((id) => p.name?.includes(id) || p.id?.startsWith(id))
  );
}

// Only RU profiles for Yandex
const ruProfiles = profiles.filter((p) => p.lang === 'ru');

console.log(`\n=== Yandex NavBoost ===`);
console.log(`Profiles: ${ruProfiles.length} (RU only)`);
console.log(`Queries per profile: ${queriesPerRun}`);
console.log(`Target: sakhva-travel.com`);
console.log(`Log: ${LOG_FILE}\n`);

if (args['dry-run']) {
  console.log('DRY RUN — plan:');
  for (const p of ruProfiles) {
    const qs = [
      ...shuffle(TARGET_QUERIES.high).slice(0, 2),
      ...shuffle(TARGET_QUERIES.medium).slice(0, 1),
    ];
    console.log(`  ${p.name} (${p.persona}): ${qs.slice(0, queriesPerRun).join(' | ')}`);
  }
  process.exit(0);
}

// Run
(async () => {
  await mlxSignIn();
  const startTime = Date.now();
  let ok = 0;
  let fail = 0;

  for (const profile of shuffle(ruProfiles)) {
    try {
      await runProfile(profile, queriesPerRun);
      ok++;
    } catch (e) {
      console.log(`  [FAIL] ${profile.name}: ${e.message}`);
      fail++;
    }
    // Pause between profiles (5-15 min)
    if (ruProfiles.indexOf(profile) < ruProfiles.length - 1) {
      const pauseMin = rand(5, 15);
      console.log(`  [PAUSE] ${pauseMin} min between profiles`);
      await sleep(pauseMin * 60 * 1000);
    }
  }

  const totalMin = Math.round((Date.now() - startTime) / 60000);
  const summary = `NavBoost done: ${ok} OK, ${fail} fail, ${totalMin} min`;
  console.log(`\n${summary}`);
  await tgNotify(`<b>NavBoost</b>\n${summary}`);
})();
