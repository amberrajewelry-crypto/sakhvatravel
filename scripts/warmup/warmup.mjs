#!/usr/bin/env node
/**
 * SEO Dissertation — Profile Warmup Script
 * ШАГ 0.8: Multilogin CookieRobot replacement
 *
 * 3-дневный прогрев браузерных профилей перед целевыми сессиями.
 *
 * Day 1: Бытовая жизнь — 0% Грузия, 0% travel (30-45 мин/профиль)
 * Day 2: Travel general + первое касание Грузии 20-30% (40-60 мин/профиль)
 * Day 3: Deep Georgia/Tbilisi 80-100%, конкретные туры (45-60 мин/профиль)
 *
 * Каждое действие логируется в JSONL для диссертационной воспроизводимости.
 *
 * Usage:
 *   node warmup.mjs --day 1 --all                   # День 1: все профили
 *   node warmup.mjs --day 2 --profiles p1,p2,p3     # День 2: конкретные
 *   node warmup.mjs --day 3 --all --sequential       # День 3: по очереди
 *
 * Env (.env в этой папке):
 *   MLX_EMAIL, MLX_PASSWORD        — Multilogin X аккаунт
 *   MLX_FOLDER_ID                  — папка профилей (опционально)
 *   MLX_LAUNCHER_URL               — local agent (default http://127.0.0.1:45001)
 *   TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID — уведомления (опционально)
 */

import { chromium } from 'playwright';
import { parseArgs } from 'node:util';
import { readFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------------------------------------------------------------------------
// .env loader
// ---------------------------------------------------------------------------

function loadEnv() {
  const envPath = resolve(__dirname, '.env');
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, 'utf-8').split('\n')) {
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
    console.error('Copy warmup-config.example.json -> warmup-config.json');
    process.exit(1);
  }
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

// MLX paths resolved at runtime via xcli

// ---------------------------------------------------------------------------
// Dissertation logger — JSONL for reproducibility
// ---------------------------------------------------------------------------

const LOG_DIR = resolve(__dirname, 'logs');
if (!existsSync(LOG_DIR)) mkdirSync(LOG_DIR, { recursive: true });

const LOG_FILE = resolve(LOG_DIR, `warmup-${new Date().toISOString().slice(0, 10)}.jsonl`);

function log(profileId, action, details = {}) {
  const entry = {
    ts: new Date().toISOString(),
    profile: profileId,
    action,
    ...details,
  };
  const line = JSON.stringify(entry);
  appendFileSync(LOG_FILE, line + '\n');
  const label = details.url ? ` ${details.url}` : details.query ? ` "${details.query}"` : '';
  console.log(`  [${action}]${label} ${details.duration_s ? `(${details.duration_s}s)` : ''}`);
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
// Multilogin X — via xcli + local launcher
// ---------------------------------------------------------------------------

import { execSync } from 'node:child_process';

const XCLI = '/Users/vladimir/mlx/deps/cli/xcli';

async function mlxSignIn() {
  // Get credentials from macOS keychain
  const email = execSync('security find-generic-password -a "$USER" -s "mlx-email" -w', { encoding: 'utf-8' }).trim();
  const pass = execSync('security find-generic-password -a "$USER" -s "mlx-password" -w', { encoding: 'utf-8' }).trim();

  try {
    execSync(`${XCLI} login --username '${email}' --password '${pass}'`, { encoding: 'utf-8', timeout: 15000 });
    console.log('[MLX] Signed in via xcli');
  } catch (e) {
    // May already be logged in
    console.log('[MLX] Login attempt:', e.message?.split('\n')[0] || 'ok');
  }
}

async function mlxStartProfile(profileId, headless = false) {
  const folderId = loadConfig().folder_id;
  const hlFlag = headless ? ' --headless' : '';
  let out;
  try {
    out = execSync(
      `${XCLI} profile-start --profile-id '${profileId}' -f '${folderId}' --automation puppeteer${hlFlag}`,
      { encoding: 'utf-8', timeout: 90000 }
    );
  } catch (execErr) {
    const stderr = execErr.stderr || '';
    const stdout = execErr.stdout || '';
    // xcli sometimes exits non-zero but still provides a port
    const rescueMatch = stdout.match(/port[:\s]+(\d+)/i) || stdout.match(/(\d{5})/);
    if (rescueMatch) {
      console.log(`[MLX] Start had error but port found: ${rescueMatch[1]}`);
      return parseInt(rescueMatch[1], 10);
    }
    console.log(`[MLX] Start failed: ${stderr.slice(0, 200)} | ${stdout.slice(0, 200)}`);
    const err = new Error(`xcli start failed: ${stderr.slice(0, 200)}`);
    err.stderr = stderr;
    throw err;
  }
  // Output: "Profile started and available on this port: 57703"
  const portMatch = out.match(/port[:\s]+(\d+)/i) || out.match(/(\d{5})/);
  if (portMatch) return parseInt(portMatch[1], 10);

  console.log('[MLX] Start output:', out.trim());
  throw new Error(`Cannot parse port from xcli output: ${out.slice(0, 200)}`);
}

async function mlxStopProfile(profileId) {
  try {
    execSync(`${XCLI} profile-stop --profile-id '${profileId}'`, { encoding: 'utf-8', timeout: 15000 });
  } catch { /* ignore — may already be stopped */ }
}

// ---------------------------------------------------------------------------
// Human-like helpers
// ---------------------------------------------------------------------------

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

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
    // Fallback: try focusing via keyboard
    await page.keyboard.press('Tab');
    await sleep(500);
  }
  await sleep(rand(200, 500));
  for (const ch of text) {
    await page.keyboard.type(ch, { delay: rand(40, 160) });
  }
}

async function safeClick(page, selector, timeout = 5000) {
  try {
    await page.waitForSelector(selector, { timeout });
    await sleep(rand(300, 800));
    await page.click(selector);
    return true;
  } catch {
    return false;
  }
}

async function safeGoto(page, url, profileId) {
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      return true;
    } catch (e) {
      const msg = e.message || '';
      if (attempt === 0 && (msg.includes('Timeout') || msg.includes('SOCKS'))) {
        log(profileId, 'navigate_retry', { url, attempt: 1 });
        await sleep(3000);
        continue;
      }
      log(profileId, 'navigate_error', { url, error: msg });
      return false;
    }
  }
  return false;
}

async function googleSearch(page, query, profileId) {
  if (!await safeGoto(page, 'https://www.google.com', profileId)) return false;
  await sleep(rand(1500, 3000));

  // Accept cookies (multi-language: EN, RU, DE, FR, TR)
  await safeClick(page, [
    'button:has-text("Accept all")',
    'button:has-text("Accept")',
    'button:has-text("Agree")',
    'button:has-text("Принять")',
    'button:has-text("Alle akzeptieren")',
    'button:has-text("Tout accepter")',
    'button:has-text("Tümünü kabul et")',
    'button#L2AGLb',
    'button[aria-label="Accept all"]',
  ].join(', '), 5000);
  await sleep(rand(500, 1000));

  // Type query
  const input = 'textarea[name="q"], input[name="q"]';
  try {
    await page.waitForSelector(input, { timeout: 10000 });
  } catch {
    log(profileId, 'google_input_not_found');
    return false;
  }

  await humanType(page, input, query);
  await sleep(rand(600, 1500));
  await page.keyboard.press('Enter');

  try {
    await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
  } catch { /* timeout ok */ }

  await sleep(rand(2000, 4000));
  log(profileId, 'google_search', { query });
  return true;
}

async function clickResult(page, profileId, maxPos = 5) {
  const results = page.locator('#search a[href]:not([href*="google"])');
  const count = await results.count();
  if (count === 0) return null;

  const idx = rand(0, Math.min(count - 1, maxPos - 1));
  try {
    const href = await results.nth(idx).getAttribute('href', { timeout: 5000 });
    await results.nth(idx).click({ timeout: 10000 });
    await page.waitForLoadState('domcontentloaded', { timeout: 30000 }).catch(() => {});
    const readTime = rand(15, 60);
    await sleep(readTime * 1000);
    await humanScroll(page, rand(2, 5));
    log(profileId, 'click_result', { url: href, read_s: readTime });
    return href;
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// PERSONA-BASED SITE & SEARCH POOLS — each profile gets unique behavior
// ---------------------------------------------------------------------------

const SITES_BY_GEO = {
  // RU cities — Russian web ecosystem
  moscow: {
    news: ['https://lenta.ru', 'https://rbc.ru', 'https://ria.ru', 'https://dzen.ru', 'https://kommersant.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://ozon.ru', 'https://wildberries.ru'],
    social: ['https://vk.com', 'https://pikabu.ru', 'https://habr.com', 'https://vc.ru'],
    maps: 'https://yandex.ru/maps/213/moscow/',
  },
  spb: {
    news: ['https://fontanka.ru', 'https://lenta.ru', 'https://rbc.ru', 'https://dzen.ru', 'https://dp.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://ozon.ru', 'https://wildberries.ru'],
    social: ['https://vk.com', 'https://pikabu.ru', 'https://habr.com', 'https://dtf.ru'],
    maps: 'https://yandex.ru/maps/2/saint-petersburg/',
  },
  kazan: {
    news: ['https://business-gazeta.ru', 'https://lenta.ru', 'https://rbc.ru', 'https://dzen.ru', 'https://tass.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://ozon.ru', 'https://kinopoisk.ru'],
    social: ['https://vk.com', 'https://ok.ru', 'https://pikabu.ru', 'https://vc.ru'],
    maps: 'https://yandex.ru/maps/43/kazan/',
  },
  novosibirsk: {
    news: ['https://ngs.ru', 'https://lenta.ru', 'https://rbc.ru', 'https://dzen.ru', 'https://iz.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://2gis.ru', 'https://ozon.ru'],
    social: ['https://vk.com', 'https://pikabu.ru', 'https://ok.ru', 'https://habr.com'],
    maps: 'https://yandex.ru/maps/65/novosibirsk/',
  },
  ekb: {
    news: ['https://e1.ru', 'https://lenta.ru', 'https://rbc.ru', 'https://dzen.ru', 'https://tass.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://ozon.ru', 'https://wildberries.ru'],
    social: ['https://vk.com', 'https://pikabu.ru', 'https://vc.ru', 'https://dtf.ru'],
    maps: 'https://yandex.ru/maps/54/yekaterinburg/',
  },
  krasnodar: {
    news: ['https://93.ru', 'https://lenta.ru', 'https://rbc.ru', 'https://dzen.ru', 'https://kubnews.ru'],
    services: ['https://yandex.ru', 'https://avito.ru', 'https://ozon.ru', 'https://wildberries.ru'],
    social: ['https://vk.com', 'https://ok.ru', 'https://pikabu.ru', 'https://vc.ru'],
    maps: 'https://yandex.ru/maps/35/krasnodar/',
  },
  // EN cities — international web ecosystem
  berlin: {
    news: ['https://bbc.com', 'https://theguardian.com', 'https://reuters.com', 'https://spiegel.de', 'https://dw.com'],
    services: ['https://amazon.de', 'https://ebay.de', 'https://idealo.de', 'https://check24.de'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://linkedin.com', 'https://instagram.com'],
    maps: 'https://www.google.com/maps/place/Berlin/',
  },
  london: {
    news: ['https://bbc.co.uk', 'https://theguardian.com', 'https://independent.co.uk', 'https://telegraph.co.uk', 'https://reuters.com'],
    services: ['https://amazon.co.uk', 'https://ebay.co.uk', 'https://argos.co.uk', 'https://rightmove.co.uk'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://linkedin.com', 'https://instagram.com'],
    maps: 'https://www.google.com/maps/place/London/',
  },
  paris: {
    news: ['https://lemonde.fr', 'https://bbc.com', 'https://reuters.com', 'https://france24.com', 'https://lefigaro.fr'],
    services: ['https://amazon.fr', 'https://leboncoin.fr', 'https://fnac.com', 'https://cdiscount.com'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://linkedin.com', 'https://instagram.com'],
    maps: 'https://www.google.com/maps/place/Paris/',
  },
  istanbul: {
    news: ['https://bbc.com', 'https://reuters.com', 'https://dailysabah.com', 'https://hurriyetdailynews.com', 'https://dw.com'],
    services: ['https://amazon.com.tr', 'https://hepsiburada.com', 'https://trendyol.com', 'https://sahibinden.com'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://instagram.com', 'https://linkedin.com'],
    maps: 'https://www.google.com/maps/place/Istanbul/',
  },
  dubai: {
    news: ['https://gulfnews.com', 'https://bbc.com', 'https://reuters.com', 'https://khaleejtimes.com', 'https://thenationalnews.com'],
    services: ['https://amazon.ae', 'https://noon.com', 'https://dubizzle.com', 'https://carrefouruae.com'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://linkedin.com', 'https://instagram.com'],
    maps: 'https://www.google.com/maps/place/Dubai/',
  },
  nyc: {
    news: ['https://nytimes.com', 'https://bbc.com', 'https://reuters.com', 'https://washingtonpost.com', 'https://cnn.com'],
    services: ['https://amazon.com', 'https://ebay.com', 'https://walmart.com', 'https://target.com'],
    social: ['https://reddit.com', 'https://twitter.com', 'https://linkedin.com', 'https://instagram.com'],
    maps: 'https://www.google.com/maps/place/New+York/',
  },
};

// =====================================================================
// DAY 1 — ЧИСТАЯ БЫТОВАЯ ЖИЗНЬ (0% Грузия, 0% travel)
// =====================================================================
const DAY1_BY_PERSONA = {
  relocant: {
    ru: [
      '{city} погода сегодня', 'курс доллара к рублю', 'новости {city}',
      '{city} доставка еды', 'рецепты быстрый завтрак', '{city} коворкинг',
      '{city} кофейни рядом', 'фриланс биржа',
    ],
    en: [
      '{city} weather today', 'usd exchange rate', '{city} news',
      '{city} food delivery', 'healthy breakfast recipe', '{city} coworking',
      '{city} best cafes', 'freelance platforms 2026',
    ],
  },
  tourist: {
    ru: [
      '{city} погода', '{city} новости', '{city} афиша выходные',
      'рецепты ужин', '{city} достопримечательности', 'фильмы 2026 рейтинг',
      '{city} кафе центр', 'что посмотреть на выходных',
    ],
    en: [
      '{city} weather', '{city} news today', '{city} events weekend',
      'dinner recipe easy', '{city} attractions', 'movies 2026 rating',
      '{city} cafe downtown', 'things to do this weekend',
    ],
  },
  business: {
    ru: [
      'курс доллара', '{city} новости бизнес', '{city} рестораны деловой ужин',
      '{city} расписание рейсов', 'forbes россия', '{city} финансовые новости',
      'инвестиции 2026', '{city} бизнес центр',
    ],
    en: [
      'usd exchange rate', '{city} business news', '{city} business dinner restaurants',
      '{city} airport flights', 'bloomberg markets', '{city} financial news',
      'investment trends 2026', '{city} business district',
    ],
  },
  backpacker: {
    ru: [
      '{city} погода', 'стрит фуд {city}', '{city} парки прогулка',
      'pikabu главная', '{city} дёшево поесть', 'рюкзак для похода',
      '{city} вокзал расписание', 'фильмы про путешествия',
    ],
    en: [
      '{city} weather', 'street food {city}', '{city} parks walking',
      'reddit frontpage', '{city} cheap eats', 'backpack hiking gear',
      '{city} train station schedule', 'travel movies best',
    ],
  },
  family: {
    ru: [
      '{city} погода', '{city} детские площадки', '{city} парки аттракционы',
      'рецепты для детей быстро', '{city} торговый центр', '{city} новости',
      'мультфильмы 2026', '{city} школа каникулы',
    ],
    en: [
      '{city} weather', '{city} playgrounds', '{city} amusement parks',
      'kid friendly recipes easy', '{city} shopping mall', '{city} news',
      'animated movies 2026', '{city} school holidays',
    ],
  },
};

// =====================================================================
// DAY 2 — TRAVEL GENERAL + ПЕРВОЕ КАСАНИЕ ГРУЗИИ (20-30% Грузия)
// =====================================================================
const DAY2_BY_PERSONA = {
  relocant: {
    ru: [
      'куда поехать весной 2026', 'лучшие страны для релокации',
      'безвизовые страны для россиян', 'коворкинг за границей',
      // первое касание:
      'грузия для фрилансеров', 'тбилиси отзывы жизнь',
    ],
    en: [
      'best countries to relocate 2026', 'digital nomad destinations',
      'visa free countries', 'coworking abroad cheap',
      'tbilisi digital nomad', 'georgia remote work',
    ],
  },
  tourist: {
    ru: [
      'куда поехать без визы 2026', 'лучшие направления весна',
      'авиабилеты дёшево', 'отзывы туристов куда ехать',
      // первое касание:
      'грузия отзывы туристов 2026', 'тбилиси что посмотреть',
    ],
    en: [
      'best travel destinations 2026', 'visa free countries europe',
      'cheap flights spring', 'travel reviews where to go',
      'georgia travel reviews 2026', 'tbilisi things to do',
    ],
  },
  business: {
    ru: [
      'бизнес конференции 2026', 'деловые поездки направления',
      'авиабилеты бизнес класс', 'лучшие бизнес отели европа',
      // первое касание:
      'грузия бизнес климат', 'тбилиси деловой визит',
    ],
    en: [
      'business conferences 2026', 'business travel destinations',
      'business class flights deals', 'best business hotels europe',
      'georgia business climate', 'tbilisi business visit',
    ],
  },
  backpacker: {
    ru: [
      'дешёвые страны для путешествий 2026', 'автостоп европа',
      'бюджетный треккинг', 'хостелы рейтинг',
      // первое касание:
      'грузия бюджетно', 'тбилиси хостелы',
    ],
    en: [
      'cheapest countries to visit 2026', 'hitchhiking europe tips',
      'budget trekking destinations', 'best hostels europe',
      'georgia on a budget', 'tbilisi hostels cheap',
    ],
  },
  family: {
    ru: [
      'куда поехать с детьми 2026', 'безопасные страны семейный отдых',
      'авиабилеты семья дёшево', 'семейные отели всё включено',
      // первое касание:
      'грузия с детьми отзывы', 'тбилиси с детьми',
    ],
    en: [
      'family vacation destinations 2026', 'safest countries family travel',
      'cheap family flights', 'family hotels all inclusive',
      'georgia with kids reviews', 'tbilisi with kids',
    ],
  },
};

// =====================================================================
// DAY 3 — УГЛУБЛЕНИЕ ГРУЗИЯ/ТБИЛИСИ (80-100% Грузия, конкретные туры)
// =====================================================================
const DAY3_BY_PERSONA = {
  relocant: {
    ru: [
      'экскурсии из тбилиси', 'казбеги из тбилиси', 'кахетия винный тур',
      'мцхета как добраться', 'тбилиси ночной тур', 'грузия горы маршруты',
      'тбилиси фуникулёр', 'лучшие рестораны тбилиси 2026',
      'тбилиси блошиный рынок', 'парк мтацминда',
    ],
    en: [
      'tours from tbilisi', 'kazbegi from tbilisi', 'kakheti wine tour',
      'mtskheta how to get', 'tbilisi night tour', 'georgia mountain routes',
      'tbilisi funicular', 'best restaurants tbilisi 2026',
      'tbilisi flea market', 'mtatsminda park',
    ],
  },
  tourist: {
    ru: [
      'гид тбилиси цена', 'экскурсии тбилиси отзывы', 'казбеги экскурсия',
      'кахетия тур из тбилиси', 'тбилиси пешеходная экскурсия',
      'грузия достопримечательности', 'тбилиси серные бани',
      'мцхета джвари', 'тбилиси обзорная экскурсия', 'wine tour tbilisi',
    ],
    en: [
      'tbilisi guide price', 'tbilisi tours reviews', 'kazbegi tour',
      'kakheti tour from tbilisi', 'tbilisi walking tour',
      'georgia attractions', 'tbilisi sulfur baths',
      'mtskheta jvari', 'tbilisi sightseeing tour', 'wine tour tbilisi',
    ],
  },
  business: {
    ru: [
      'vip тур тбилиси', 'приватный гид тбилиси', 'казбеги приватный тур',
      'кахетия дегустация', 'лучшие винодельни грузия',
      'тбилиси трансфер аэропорт', 'грузия корпоратив',
      'тбилиси ресторан с видом', 'бутик отель тбилиси',
    ],
    en: [
      'vip tour tbilisi', 'private guide tbilisi', 'kazbegi private tour',
      'kakheti wine tasting', 'best wineries georgia',
      'tbilisi airport transfer', 'georgia corporate events',
      'tbilisi restaurant with view', 'boutique hotel tbilisi',
    ],
  },
  backpacker: {
    ru: [
      'бесплатный тур тбилиси', 'тбилиси пешком маршрут', 'казбеги самостоятельно',
      'грузия треккинг', 'тбилиси хостел район', 'мцхета автобус',
      'сванетия бюджетно', 'тбилиси бар улица',
    ],
    en: [
      'free tour tbilisi', 'tbilisi walking route', 'kazbegi on your own',
      'georgia trekking', 'tbilisi hostel area', 'mtskheta bus',
      'svaneti budget', 'tbilisi bar street',
    ],
  },
  family: {
    ru: [
      'тбилиси экскурсия с детьми', 'казбеги семейный тур', 'грузия с детьми отзывы',
      'тбилиси зоопарк', 'тбилиси детский парк', 'кахетия с детьми',
      'грузия море с ребёнком батуми', 'тбилиси канатная дорога',
    ],
    en: [
      'tbilisi tour with kids', 'kazbegi family tour', 'georgia with kids reviews',
      'tbilisi zoo', 'tbilisi kids park', 'kakheti with children',
      'georgia beach batumi kids', 'tbilisi cable car',
    ],
  },
};

// Interest-specific sites for browsing
const INTEREST_SITES = {
  yoga: ['https://yogajournal.ru', 'https://youtube.com/results?search_query=yoga+flow'],
  cafe: ['https://afisha.ru/msk/restaurants/', 'https://tripadvisor.com'],
  coworking: ['https://vc.ru', 'https://habr.com'],
  hiking: ['https://alltrails.com', 'https://wikiloc.com'],
  wine: ['https://vivino.com', 'https://wine-searcher.com'],
  photography: ['https://unsplash.com', 'https://500px.com', 'https://flickr.com'],
  finance: ['https://rbc.ru/finances/', 'https://bloomberg.com', 'https://investing.com'],
  restaurants: ['https://afisha.ru/msk/restaurants/', 'https://tripadvisor.com/Restaurants'],
  flights: ['https://skyscanner.com', 'https://aviasales.ru', 'https://kayak.com'],
  hostels: ['https://hostelworld.com', 'https://booking.com'],
  'street-food': ['https://tripadvisor.com', 'https://youtube.com/results?search_query=street+food'],
  history: ['https://wikipedia.org', 'https://britannica.com'],
  kids: ['https://afisha.ru/msk/kids/', 'https://tripadvisor.com/Attractions'],
  parks: ['https://tripadvisor.com/Attractions', 'https://google.com/maps'],
  shopping: ['https://wildberries.ru', 'https://ozon.ru'],
};

// Travel sites per persona
const TRAVEL_SITES_BY_PERSONA = {
  relocant: ['https://booking.com', 'https://tripadvisor.com', 'https://otzovik.com', 'https://maps.google.com'],
  tourist: ['https://booking.com', 'https://tripadvisor.com', 'https://viator.com', 'https://getyourguide.com'],
  business: ['https://booking.com', 'https://tripadvisor.com', 'https://kayak.com', 'https://hotels.com'],
  backpacker: ['https://hostelworld.com', 'https://booking.com', 'https://rome2rio.com', 'https://wikivoyage.org'],
  family: ['https://booking.com', 'https://tripadvisor.com', 'https://familywithkids.com', 'https://airbnb.com'],
};

// YouTube searches — Day 1 (neutral, NO Georgia/travel)
const YOUTUBE_DAY1 = {
  relocant: {
    ru: ['утренняя йога 20 минут', 'кофейни обзор', 'фриланс советы 2026', 'рецепты завтрак'],
    en: ['morning yoga routine', 'cafe vlog', 'freelance tips 2026', 'healthy breakfast recipe'],
  },
  tourist: {
    ru: ['фильмы 2026 обзор', 'рецепты ужин быстро', 'фотография обучение', 'музыка для работы'],
    en: ['movies 2026 review', 'easy dinner recipe', 'photography tutorial', 'lofi music work'],
  },
  business: {
    ru: ['рынки обзор сегодня', 'мотивация бизнес', 'инвестиции 2026', 'тайм менеджмент'],
    en: ['market analysis today', 'business motivation', 'investment 2026', 'time management tips'],
  },
  backpacker: {
    ru: ['автостоп советы', 'готовим в походе', 'рюкзак обзор', 'фильмы про путешествия'],
    en: ['hitchhiking tips', 'camp cooking', 'backpack review', 'travel movies best'],
  },
  family: {
    ru: ['рецепты для детей', 'мультфильмы новинки 2026', 'поделки с детьми', 'парк развлечений обзор'],
    en: ['recipes for kids', 'animated movies 2026', 'crafts with kids', 'theme park review'],
  },
};

// YouTube searches — Day 2 (travel general + hint of Georgia)
const YOUTUBE_DAY2 = {
  relocant: {
    ru: ['куда уехать из россии 2026', 'жизнь за границей влог', 'тбилиси влог', 'коворкинг за границей'],
    en: ['digital nomad life 2026', 'best cities to live abroad', 'tbilisi vlog', 'coworking abroad'],
  },
  tourist: {
    ru: ['куда поехать весной 2026', 'путешествия бюджет', 'грузия влог', 'красивые места'],
    en: ['travel destinations 2026', 'budget travel tips', 'georgia travel vlog', 'beautiful places'],
  },
  business: {
    ru: ['бизнес за границей', 'деловые поездки советы', 'грузия бизнес', 'инвестиции за рубежом'],
    en: ['business abroad', 'business travel tips', 'georgia business', 'foreign investments'],
  },
  backpacker: {
    ru: ['бюджетные путешествия 2026', 'автостоп европа', 'грузия бюджетно', 'кавказ влог'],
    en: ['budget travel 2026', 'hitchhiking europe', 'georgia on a budget', 'caucasus vlog'],
  },
  family: {
    ru: ['отдых с детьми куда', 'семейные путешествия', 'грузия с детьми', 'безопасный отдых семья'],
    en: ['family travel destinations', 'traveling with kids tips', 'georgia with kids', 'safe family travel'],
  },
};

// YouTube searches — Day 3 (deep Georgia/Tbilisi)
const YOUTUBE_DAY3 = {
  relocant: {
    ru: ['тбилиси влог релокант', 'жизнь в грузии 2026', 'переезд в тбилиси', 'экскурсии тбилиси'],
    en: ['tbilisi digital nomad', 'living in georgia 2026', 'moving to tbilisi', 'tbilisi tours'],
  },
  tourist: {
    ru: ['тбилиси что посмотреть', 'кахетия тур влог', 'казбеги влог', 'грузинская кухня обзор'],
    en: ['tbilisi travel guide', 'kakheti wine tour vlog', 'kazbegi trip', 'georgian food tour'],
  },
  business: {
    ru: ['тбилиси бизнес', 'кахетия премиум дегустация', 'грузия инвестиции', 'luxury tbilisi'],
    en: ['tbilisi business trip', 'kakheti private wine tour', 'invest in georgia', 'luxury tbilisi tour'],
  },
  backpacker: {
    ru: ['тбилиси бюджетно влог', 'казбеги самостоятельно', 'грузия автостоп', 'хостелы тбилиси'],
    en: ['tbilisi budget travel', 'kazbegi hiking', 'georgia backpacking', 'tbilisi hostels review'],
  },
  family: {
    ru: ['грузия с детьми 2026', 'тбилиси семейный отдых', 'мтацминда парк', 'батуми с ребёнком'],
    en: ['georgia family travel 2026', 'tbilisi with kids vlog', 'mtatsminda park', 'batumi with kids'],
  },
};

/**
 * Build personalized query replacing {city} placeholder
 */
function buildQuery(template, profileCfg) {
  return template.replace(/\{city\}/g, profileCfg.homeCity || 'Москва');
}

/**
 * Get sites pool for a profile based on its geo
 */
function getGeoSites(profileCfg) {
  return SITES_BY_GEO[profileCfg.geo] || SITES_BY_GEO.moscow;
}

/**
 * Get personalized Day 1 searches
 */
function getDay1Searches(profileCfg) {
  const persona = profileCfg.persona || 'tourist';
  const lang = profileCfg.lang || 'ru';
  const pool = DAY1_BY_PERSONA[persona]?.[lang] || DAY1_BY_PERSONA.tourist.ru;
  return pool.map((q) => buildQuery(q, profileCfg));
}

/**
 * Get personalized Day 2 searches
 */
function getDay2Searches(profileCfg) {
  const persona = profileCfg.persona || 'tourist';
  const lang = profileCfg.lang || 'ru';
  const pool = DAY2_BY_PERSONA[persona]?.[lang] || DAY2_BY_PERSONA.tourist.ru;
  return pool.map((q) => buildQuery(q, profileCfg));
}

/**
 * Get personalized Day 3 searches
 */
function getDay3Searches(profileCfg) {
  const persona = profileCfg.persona || 'tourist';
  const lang = profileCfg.lang || 'ru';
  const pool = DAY3_BY_PERSONA[persona]?.[lang] || DAY3_BY_PERSONA.tourist.ru;
  return pool.map((q) => buildQuery(q, profileCfg));
}

/**
 * Get YouTube query for specific day
 */
function getYouTubeQuery(profileCfg, day) {
  const persona = profileCfg.persona || 'tourist';
  const lang = profileCfg.lang || 'ru';
  const pool = day === 1 ? YOUTUBE_DAY1 : day === 2 ? YOUTUBE_DAY2 : YOUTUBE_DAY3;
  const queries = pool[persona]?.[lang] || pool.tourist.ru;
  return pick(queries);
}

// ---------------------------------------------------------------------------
// Day 1 scenarios (15-20 min per profile)
// ---------------------------------------------------------------------------

async function day1(page, profileId, profileCfg) {
  const startMs = Date.now();
  const geoSites = getGeoSites(profileCfg);
  const searches = getDay1Searches(profileCfg);
  const persona = profileCfg.persona || 'tourist';

  log(profileId, 'day1_persona', {
    persona, geo: profileCfg.geo, lang: profileCfg.lang,
    homeCity: profileCfg.homeCity,
  });

  // 1. Google search — home city context (weather/news)
  const q1 = pick(searches.slice(0, 3));
  await googleSearch(page, q1, profileId);
  await humanScroll(page, 2);
  await sleep(rand(3000, 6000));

  // 2. YouTube — NEUTRAL search + watch 2-4 min (no travel, no Georgia)
  log(profileId, 'youtube_start');
  const ytQuery = getYouTubeQuery(profileCfg, 1);
  if (await safeGoto(page, `https://www.youtube.com/results?search_query=${encodeURIComponent(ytQuery)}`, profileId)) {
    await sleep(rand(2000, 4000));
    await safeClick(page, 'button:has-text("Accept"), button:has-text("Принять")', 3000);
    await sleep(rand(1000, 2000));

    const vids = page.locator('ytd-video-renderer a#thumbnail, a#thumbnail');
    const vidCount = await vids.count().catch(() => 0);
    if (vidCount > 0) {
      try {
        await vids.nth(rand(0, Math.min(vidCount - 1, 5))).click();
        const watchSec = rand(15, 30);
        log(profileId, 'youtube_watch', { query: ytQuery, duration_s: watchSec });
        await sleep(watchSec * 1000);
      } catch {
        log(profileId, 'youtube_click_failed');
      }
    }
  }

  // 3. News site from profile's geo — browse + click article
  const newsSite = pick(geoSites.news);
  log(profileId, 'news_browse', { url: newsSite });
  if (await safeGoto(page, newsSite, profileId)) {
    await sleep(rand(2000, 4000));
    await humanScroll(page, rand(3, 7));
    await sleep(rand(5000, 10000));

    const links = page.locator('a[href]').filter({ hasText: /\S{10,}/ });
    const linkCount = await links.count().catch(() => 0);
    if (linkCount > 3) {
      try {
        await links.nth(rand(0, Math.min(linkCount - 1, 10))).click({ timeout: 3000 });
        await sleep(rand(5000, 15000));
        await humanScroll(page, rand(2, 5));
        log(profileId, 'news_article_read');
      } catch { /* ok */ }
    }
  }

  // 4. Services from profile's geo — 2 random visits
  const svcSites = [...geoSites.services].sort(() => Math.random() - 0.5).slice(0, 2);
  for (const site of svcSites) {
    if (await safeGoto(page, site, profileId)) {
      await sleep(rand(3000, 8000));
      await humanScroll(page, rand(1, 3));
      log(profileId, 'service_visit', { url: site });
    }
  }

  // 5. Interest-specific sites (1-2 based on persona interests)
  const interests = profileCfg.interests || [];
  const interestSites = interests
    .flatMap((i) => INTEREST_SITES[i] || [])
    .sort(() => Math.random() - 0.5)
    .slice(0, rand(1, 2));
  for (const site of interestSites) {
    if (await safeGoto(page, site, profileId)) {
      await sleep(rand(5000, 12000));
      await humanScroll(page, rand(2, 4));
      log(profileId, 'interest_visit', { url: site });
    }
  }

  // 6. Social from profile's geo — 1 site
  const socialSite = pick(geoSites.social);
  if (await safeGoto(page, socialSite, profileId)) {
    await sleep(rand(5000, 15000));
    await humanScroll(page, rand(3, 6));
    log(profileId, 'social_visit', { url: socialSite });
  }

  // 7. Gmail (if configured)
  if (profileCfg.gmail) {
    log(profileId, 'gmail_check');
    if (await safeGoto(page, 'https://mail.google.com', profileId)) {
      await sleep(rand(4000, 8000));
      await humanScroll(page, 2);
    }
  }

  // 8. Extra Google search — different query from persona pool
  const q2 = pick(searches.slice(3));
  await googleSearch(page, q2, profileId);
  await clickResult(page, profileId);

  // 9. Home city map check (natural behavior)
  if (geoSites.maps && Math.random() > 0.5) {
    log(profileId, 'maps_home', { url: geoSites.maps });
    if (await safeGoto(page, geoSites.maps, profileId)) {
      await sleep(rand(3000, 8000));
    }
  }

  const totalMin = Math.round((Date.now() - startMs) / 60000);
  log(profileId, 'day1_complete', { total_min: totalMin, persona });
}

// ---------------------------------------------------------------------------
// Day 2 scenarios (20-30 min per profile)
// ---------------------------------------------------------------------------

async function day2(page, profileId, profileCfg) {
  const startMs = Date.now();
  const persona = profileCfg.persona || 'tourist';
  const searches = getDay2Searches(profileCfg);
  const geoSites = getGeoSites(profileCfg);

  log(profileId, 'day2_persona', {
    persona, geo: profileCfg.geo, lang: profileCfg.lang,
  });

  // 1. Multiple Google searches — persona-specific travel queries
  const queries = [...searches].sort(() => Math.random() - 0.5).slice(0, rand(3, 5));
  for (const q of queries) {
    if (await googleSearch(page, q, profileId)) {
      await clickResult(page, profileId);
      await sleep(rand(2000, 5000));
      await page.goBack({ timeout: 15000 }).catch(() => {});
      await sleep(rand(1000, 3000));
    }
  }

  // 2. Social media — geo-appropriate
  const socials = profileCfg.lang === 'en'
    ? ['https://www.reddit.com/r/tbilisi', 'https://www.reddit.com/r/sakartvelo', 'https://www.reddit.com/r/travel']
    : ['https://vk.com/tbilisi_georgia', 'https://pikabu.ru', 'https://www.reddit.com/r/sakartvelo'];
  const social = pick(socials);
  log(profileId, 'social_browse', { url: social });
  if (await safeGoto(page, social, profileId)) {
    await sleep(rand(3000, 5000));
    await humanScroll(page, rand(4, 8));
    await sleep(rand(8000, 20000));
  }

  // 3. Deep browsing — 2-3 result clicks on travel query
  const deepQ = pick(searches.slice(-4));
  if (await googleSearch(page, deepQ, profileId)) {
    for (let i = 0; i < rand(2, 3); i++) {
      await clickResult(page, profileId);
      await humanScroll(page, rand(3, 6));
      const readSec = rand(10, 25);
      await sleep(readSec * 1000);
      log(profileId, 'deep_read', { query: deepQ, duration_s: readSec });
      await page.goBack({ timeout: 15000 }).catch(() => {});
      await sleep(rand(1000, 3000));
    }
  }

  // Early-exit tracker: skip remaining steps if proxy is dead
  let consecutiveErrors = 0;
  const MAX_CONSECUTIVE_ERRORS = 3;
  async function gotoOrSkip(url) {
    if (consecutiveErrors >= MAX_CONSECUTIVE_ERRORS) return false;
    const ok = await safeGoto(page, url, profileId);
    if (ok) { consecutiveErrors = 0; } else { consecutiveErrors++; }
    return ok;
  }

  // 4. Travel sites — persona-specific
  const travelPool = TRAVEL_SITES_BY_PERSONA[persona] || TRAVEL_SITES_BY_PERSONA.tourist;
  const travelSites = [...travelPool].sort(() => Math.random() - 0.5).slice(0, 2);
  for (const site of travelSites) {
    if (await gotoOrSkip(site)) {
      await sleep(rand(5000, 15000));
      await humanScroll(page, rand(2, 5));
      log(profileId, 'travel_site', { url: site, persona });
    }
  }

  // 5. Interest sites — unique per profile
  const interests = profileCfg.interests || [];
  const interestSites = interests
    .flatMap((i) => INTEREST_SITES[i] || [])
    .sort(() => Math.random() - 0.5)
    .slice(0, rand(1, 2));
  for (const site of interestSites) {
    if (await gotoOrSkip(site)) {
      await sleep(rand(5000, 15000));
      await humanScroll(page, rand(2, 5));
      log(profileId, 'interest_visit', { url: site });
    }
  }

  // 6. Gmail
  if (profileCfg.gmail && consecutiveErrors < MAX_CONSECUTIVE_ERRORS) {
    log(profileId, 'gmail_check');
    if (await gotoOrSkip('https://mail.google.com')) {
      await sleep(rand(4000, 8000));
      await humanScroll(page, 2);
    }
  }

  // 7. Google Maps — Tbilisi (target geo, all personas)
  if (consecutiveErrors < MAX_CONSECUTIVE_ERRORS) {
    log(profileId, 'maps_tbilisi');
    if (await gotoOrSkip('https://maps.google.com/maps?q=tbilisi+tours')) {
      await sleep(rand(5000, 10000));
      await humanScroll(page, rand(1, 3));
    }
  }

  // 8. YouTube — travel content + hint of Georgia
  if (consecutiveErrors < MAX_CONSECUTIVE_ERRORS) {
    const ytQ = getYouTubeQuery(profileCfg, 2);
    if (await gotoOrSkip(`https://www.youtube.com/results?search_query=${encodeURIComponent(ytQ)}`)) {
      await sleep(rand(2000, 3000));
      const vids = page.locator('ytd-video-renderer a#thumbnail, a#thumbnail');
      const vidCount = await vids.count().catch(() => 0);
      if (vidCount > 0) {
        try {
          await vids.nth(rand(0, Math.min(vidCount - 1, 5))).click();
          const watchSec = rand(15, 30);
          log(profileId, 'youtube_travel', { query: ytQ, duration_s: watchSec });
          await sleep(watchSec * 1000);
        } catch { /* ok */ }
      }
    }
  }

  if (consecutiveErrors >= MAX_CONSECUTIVE_ERRORS) {
    log(profileId, 'early_exit', { reason: 'proxy_dead', skipped_steps: true });
  }

  const totalMin = Math.round((Date.now() - startMs) / 60000);
  log(profileId, 'day2_complete', { total_min: totalMin, persona });
}

// ---------------------------------------------------------------------------
// Day 2.5 — bonus session for weak profiles (5-8 min)
// ---------------------------------------------------------------------------

async function day25(page, profileId, profileCfg) {
  const startMs = Date.now();
  const persona = profileCfg.persona || 'tourist';
  const searches = getDay2Searches(profileCfg);

  log(profileId, 'day25_persona', { persona, geo: profileCfg.geo });

  // 1. Two Google searches with clicks + reading
  const queries = [...searches].sort(() => Math.random() - 0.5).slice(0, 2);
  for (const q of queries) {
    if (await googleSearch(page, q, profileId)) {
      await clickResult(page, profileId);
      const readSec = rand(20, 60);
      await humanScroll(page, rand(2, 5));
      await sleep(readSec * 1000);
      log(profileId, 'bonus_read', { query: q, duration_s: readSec });
      await page.goBack({ timeout: 15000 }).catch(() => {});
      await sleep(rand(1000, 3000));
    }
  }

  // 2. YouTube watch — the main missing signal
  const ytQ = getYouTubeQuery(profileCfg, 2);
  if (await safeGoto(page, `https://www.youtube.com/results?search_query=${encodeURIComponent(ytQ)}`, profileId)) {
    await sleep(rand(2000, 3000));
    const vids = page.locator('ytd-video-renderer a#thumbnail, a#thumbnail');
    const vidCount = await vids.count().catch(() => 0);
    if (vidCount > 0) {
      try {
        await vids.nth(rand(0, Math.min(vidCount - 1, 5))).click();
        const watchSec = rand(15, 30);
        log(profileId, 'youtube_bonus', { query: ytQ, duration_s: watchSec });
        await sleep(watchSec * 1000);
      } catch { /* ok */ }
    }
  }

  // 3. One travel site browse
  const TRAVEL_POOL = TRAVEL_SITES_BY_PERSONA[persona] || TRAVEL_SITES_BY_PERSONA.tourist;
  const site = pick(TRAVEL_POOL);
  if (await safeGoto(page, site, profileId)) {
    await sleep(rand(5000, 15000));
    await humanScroll(page, rand(2, 5));
    log(profileId, 'bonus_travel', { url: site });
  }

  const totalMin = Math.round((Date.now() - startMs) / 60000);
  log(profileId, 'day25_complete', { total_min: totalMin, persona });
}

// ---------------------------------------------------------------------------
// Day 3 scenarios (45-60 min per profile) — DEEP GEORGIA/TBILISI
// ---------------------------------------------------------------------------

async function day3(page, profileId, profileCfg) {
  const startMs = Date.now();
  const persona = profileCfg.persona || 'tourist';
  const searches = getDay3Searches(profileCfg);

  log(profileId, 'day3_persona', {
    persona, geo: profileCfg.geo, lang: profileCfg.lang,
  });

  // 1. Gmail check first (natural start)
  if (profileCfg.gmail) {
    log(profileId, 'gmail_check');
    if (await safeGoto(page, 'https://mail.google.com', profileId)) {
      await sleep(rand(3000, 6000));
      await humanScroll(page, 2);
    }
  }

  // 2. Quick news scan from home geo (normal routine)
  const geoSites = getGeoSites(profileCfg);
  const newsSite = pick(geoSites.news);
  if (await safeGoto(page, newsSite, profileId)) {
    await sleep(rand(3000, 6000));
    await humanScroll(page, rand(2, 4));
    log(profileId, 'news_quick', { url: newsSite });
  }

  // 3. Multiple Georgia-focused searches with deep clicks (4-6 queries)
  const queries = [...searches].sort(() => Math.random() - 0.5).slice(0, rand(4, 6));
  for (const q of queries) {
    if (await googleSearch(page, q, profileId)) {
      // Click 1-2 results per query, read deeply
      const clicks = rand(1, 2);
      for (let i = 0; i < clicks; i++) {
        const href = await clickResult(page, profileId);
        if (href) {
          await humanScroll(page, rand(3, 7));
          const readSec = rand(10, 25);
          await sleep(readSec * 1000);
          log(profileId, 'deep_read_georgia', { query: q, url: href, duration_s: readSec });
        }
        await page.goBack({ timeout: 15000 }).catch(() => {});
        await sleep(rand(1500, 4000));
      }
    }
    // Pause between searches (human doesn't search non-stop)
    await sleep(rand(5000, 15000));
  }

  // 4. Google Maps — Tbilisi tours + explore
  log(profileId, 'maps_tbilisi_deep');
  const mapsQuery = profileCfg.lang === 'en' ? 'tbilisi tours guide' : 'тбилиси экскурсии гид';
  if (await safeGoto(page, `https://maps.google.com/maps?q=${encodeURIComponent(mapsQuery)}`, profileId)) {
    await sleep(rand(5000, 10000));
    await humanScroll(page, rand(2, 4));
    // Click on a result in Maps
    const mapResults = page.locator('a[href*="maps/place"]');
    const mapCount = await mapResults.count().catch(() => 0);
    if (mapCount > 0) {
      try {
        await mapResults.nth(rand(0, Math.min(mapCount - 1, 3))).click();
        await sleep(rand(5000, 12000));
        await humanScroll(page, rand(1, 3));
        log(profileId, 'maps_result_click');
      } catch { /* ok */ }
    }
  }

  // 5. Travel sites — persona-specific, Tbilisi-focused
  const travelPool = TRAVEL_SITES_BY_PERSONA[persona] || TRAVEL_SITES_BY_PERSONA.tourist;
  const travelSite = pick(travelPool);
  const tbilisiSuffix = travelSite.includes('tripadvisor')
    ? '/Attractions-g294195-Activities-Tbilisi.html'
    : travelSite.includes('booking')
      ? '/searchresults.html?ss=Tbilisi'
      : travelSite.includes('getyourguide')
        ? '/tbilisi-l766/'
        : travelSite.includes('viator')
          ? '/Tbilisi/d5765-ttd'
          : '';
  const travelUrl = travelSite + tbilisiSuffix;
  log(profileId, 'travel_tbilisi', { url: travelUrl });
  if (await safeGoto(page, travelUrl, profileId)) {
    await sleep(rand(8000, 20000));
    await humanScroll(page, rand(4, 8));
    // Click on a tour/listing
    const listings = page.locator('a[href]').filter({ hasText: /tour|excursion|тур|экскурс/i });
    const listCount = await listings.count().catch(() => 0);
    if (listCount > 0) {
      try {
        await listings.nth(rand(0, Math.min(listCount - 1, 5))).click({ timeout: 5000 });
        await sleep(rand(10000, 25000));
        await humanScroll(page, rand(3, 6));
        log(profileId, 'tour_listing_read');
      } catch { /* ok */ }
    }
  }

  // 6. YouTube — deep Georgia content, watch longer
  const ytQ = getYouTubeQuery(profileCfg, 3);
  log(profileId, 'youtube_georgia');
  if (await safeGoto(page, `https://www.youtube.com/results?search_query=${encodeURIComponent(ytQ)}`, profileId)) {
    await sleep(rand(2000, 4000));
    const vids = page.locator('ytd-video-renderer a#thumbnail, a#thumbnail');
    const vidCount = await vids.count().catch(() => 0);
    if (vidCount > 0) {
      // Watch 1 video about Georgia (short)
      try {
        await vids.nth(rand(0, Math.min(vidCount - 1, 5))).click();
        const watchSec = rand(15, 30);
        log(profileId, 'youtube_georgia_watch', { query: ytQ, video: 1, duration_s: watchSec });
        await sleep(watchSec * 1000);
      } catch { /* ok */ }
    }
  }

  // 7. Social — Georgia-specific communities
  const geoSocials = profileCfg.lang === 'en'
    ? ['https://www.reddit.com/r/tbilisi', 'https://www.reddit.com/r/sakartvelo']
    : ['https://vk.com/tbilisi_georgia', 'https://www.reddit.com/r/sakartvelo'];
  const socialUrl = pick(geoSocials);
  log(profileId, 'social_georgia', { url: socialUrl });
  if (await safeGoto(page, socialUrl, profileId)) {
    await sleep(rand(5000, 10000));
    await humanScroll(page, rand(4, 8));
    await sleep(rand(5000, 15000));
  }

  // 8. One more Google search — different query from pool
  const extraQ = pick(searches.filter((q) => !queries.includes(q)));
  if (extraQ && await googleSearch(page, extraQ, profileId)) {
    await clickResult(page, profileId);
    await humanScroll(page, rand(2, 4));
    await sleep(rand(15000, 40000));
  }

  const totalMin = Math.round((Date.now() - startMs) / 60000);
  log(profileId, 'day3_complete', { total_min: totalMin, persona });
}

// ---------------------------------------------------------------------------
// Profile orchestrator
// ---------------------------------------------------------------------------

async function warmupProfile(profileId, profileCfg, day, headless = false, attempt = 1) {
  const MAX_ATTEMPTS = 3;
  console.log(`\n=== Profile: ${profileId} | Day ${day} | Attempt ${attempt} ===`);
  log(profileId, 'warmup_start', { day, headless, attempt });

  // Clean stop before start to avoid "already running" conflicts
  await mlxStopProfile(profileId);
  await sleep(2000);

  let port;
  try {
    port = await mlxStartProfile(profileId, headless);
    log(profileId, 'mlx_started', { port });
  } catch (e) {
    const errMsg = e.stderr || e.message || String(e);
    log(profileId, 'mlx_start_failed', { error: errMsg.slice(0, 300) });
    if (attempt < MAX_ATTEMPTS) {
      log(profileId, 'mlx_restart_attempt', { attempt: attempt + 1 });
      await sleep(8000);
      return warmupProfile(profileId, profileCfg, day, headless, attempt + 1);
    }
    return { profileId, ok: false, error: errMsg };
  }

  let browser;
  let dayCompleted = false;
  try {
    // Wait for browser to be ready for CDP connection
    await sleep(5000);
    let cdpRetries = 3;
    while (cdpRetries > 0) {
      try {
        browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
        break;
      } catch (cdpErr) {
        cdpRetries--;
        if (cdpRetries === 0) throw cdpErr;
        log(profileId, 'cdp_retry', { remaining: cdpRetries });
        await sleep(5000);
      }
    }
    const context = browser.contexts()[0];
    const page = context.pages()[0] || await context.newPage();
    await page.setViewportSize({ width: rand(1280, 1920), height: rand(800, 1080) });

    // Monitor SOCKS failures via page error events
    let socksErrors = 0;
    page.on('pageerror', (err) => {
      if (String(err).includes('SOCKS')) socksErrors++;
    });

    // Profile-level timeout: 15 min for day1/day2, 20 min for day3
    const PROFILE_TIMEOUT = (day === 3 ? 20 : 15) * 60 * 1000;
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('PROFILE_TIMEOUT')), PROFILE_TIMEOUT)
    );

    const dayFn = day === 1 ? day1 : day === 2 ? day2 : day === 25 ? day25 : day3;
    const dayPromise = dayFn(page, profileId, profileCfg).then(() => { dayCompleted = true; });
    await Promise.race([dayPromise, timeoutPromise]);

    log(profileId, 'warmup_success', { day, attempt });
    return { profileId, ok: true };
  } catch (e) {
    const msg = e.message || e.stack || String(e);

    // If day function already completed, don't retry on timeout
    if (dayCompleted && msg.includes('PROFILE_TIMEOUT')) {
      log(profileId, 'warmup_success', { day, attempt, note: 'timeout_after_complete' });
      return { profileId, ok: true };
    }

    console.log(`  [warmup_error] ${msg.slice(0, 200)}`);
    log(profileId, 'warmup_error', { error: msg.slice(0, 500), day, attempt });

    // If SOCKS cascade or timeout, retry with fresh proxy session
    if (attempt < MAX_ATTEMPTS && (msg.includes('SOCKS') || msg.includes('PROFILE_TIMEOUT'))) {
      if (browser) await browser.close().catch(() => {});
      await mlxStopProfile(profileId);
      log(profileId, 'proxy_restart', { reason: 'SOCKS cascade' });
      await sleep(5000);
      return warmupProfile(profileId, profileCfg, day, headless, attempt + 1);
    }

    return { profileId, ok: false, error: msg };
  } finally {
    if (browser) await browser.close().catch(() => {});
    await sleep(2000);
    await mlxStopProfile(profileId);
    log(profileId, 'mlx_stopped');
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const { values } = parseArgs({
  options: {
    day: { type: 'string', short: 'd', default: '1' },
    profiles: { type: 'string', short: 'p' },
    all: { type: 'boolean', short: 'a', default: false },
    sequential: { type: 'boolean', short: 's', default: false },
    headless: { type: 'boolean', default: false },
  },
});

const day = parseInt(values.day, 10);
if (![1, 2, 3, 25].includes(day)) {
  console.error('--day must be 1, 2, 3 or 25');
  process.exit(1);
}

const config = loadConfig();
let profileIds;

if (values.all) {
  profileIds = Object.keys(config.profiles);
} else if (values.profiles) {
  profileIds = values.profiles.split(',').map((s) => s.trim());
} else {
  console.error('Specify --profiles id1,id2 or --all');
  process.exit(1);
}

// Credentials stored in macOS keychain (mlx-email, mlx-password)

console.log(`\nSEO Dissertation — Warmup Day ${day}`);
console.log(`Profiles: ${profileIds.length} | Log: ${LOG_FILE}`);
console.log('─'.repeat(50));

await mlxSignIn();
await tgNotify(`🔄 Warmup Day ${day} started | ${profileIds.length} profiles`);

let results;
if (values.sequential) {
  results = [];
  for (const id of profileIds) {
    results.push(await warmupProfile(id, config.profiles[id] || {}, day, values.headless));
  }
} else {
  results = await Promise.allSettled(
    profileIds.map((id) => warmupProfile(id, config.profiles[id] || {}, day, values.headless))
  ).then((r) => r.map((x) => x.status === 'fulfilled' ? x.value : { ok: false, error: x.reason }));
}

const ok = results.filter((r) => r?.ok).length;
const fail = results.length - ok;

console.log('\n' + '─'.repeat(50));
console.log(`Warmup Day ${day} complete: ${ok} ok, ${fail} failed`);
console.log(`Log: ${LOG_FILE}`);

await tgNotify(`✅ Warmup Day ${day} done\n${ok} ok / ${fail} failed\nLog: ${LOG_FILE}`);
