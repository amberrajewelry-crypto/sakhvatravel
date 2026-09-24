#!/usr/bin/env node
// parse-catalog.js — Parse all tour subpages into data/catalog.json
// Run: node scripts/parse-catalog.js

const fs = require('fs');
const path = require('path');

const EKSKURSIYA_DIR = path.join(__dirname, '..', 'ekskursiya');

// Multi-day tours (go to /tury/ hub)
const MULTI_DAY_SLUGS = [
  'tur-gruziya-3-dnya', 'tur-gruziya-5-dney', 'tur-gruziya-7-dney',
  'tur-gruziya-10-dney', 'tur-gruziya-armeniya', 'tur-vsya-gruziya',
  'tur-tbilisi-kazbegi-kakheti', 'tur-tbilisi-svaneti', 'slow-travel'
];

// Tag rules: slug keywords → tag name
const TAG_KEYWORDS = {
  'Пешеходные': ['peshaya', 'stary-tbilisi', 'narikala', 'mtatsminda', 'abanotubani', 'po-hramam', 'art-tur'],
  'Гастро': ['gastronomicheskiy', 'khachapuri', 'chacha', 'dinner', 'degustatsiya', 'shopping-tur'],
  'Винные': ['vinniy', 'vinodelie', 'kvevri', 'alazani', 'kindzmarauli'],
  'Фото': ['fotosessiya', 'photo'],
  'Ночные': ['nochnaya', 'night'],
  'Старый Тбилиси': ['stary-tbilisi', 'sovetskiy', 'abanotubani'],
  'Мастер-классы': ['master-klass'],
  'Для детей': ['family', 'dlya-detey', 'dlya-pensionerov'],
  'Казбеги': ['kazbegi', 'gudauri', 'truso', 'voennaya-gruzinskaya', 'jvari', 'ananuri'],
  'Кахетия': ['kakheti', 'sighnaghi', 'alazani', 'kindzmarauli', 'degustatsiya-vina'],
  'Батуми': ['batumi'],
};

// Manual tag overrides for slugs that can't be auto-detected
const MANUAL_TAGS = {
  'ekskursiya-borjomi-iz-tbilisi': ['За городом'],
  'ekskursiya-david-gareji': ['За городом'],
  'ekskursiya-gori-iz-tbilisi': ['За городом'],
  'ekskursiya-mtskheta-iz-tbilisi': ['За городом'],
  'ekskursiya-svaneti-iz-tbilisi': ['За городом'],
  'ekskursiya-tusheti': ['За городом'],
  'ekskursiya-uplistsikhe-iz-tbilisi': ['За городом'],
  'ekskursiya-vardzia': ['За городом'],
  'ekskursiya-zugdidi': ['За городом'],
  'tur-kutaisi-iz-tbilisi': ['За городом'],
  'gruppa-10-chelovek-tbilisi': ['Группы'],
  'korporativniy-tur-tbilisi': ['Группы'],
  'priklyuchencheskiy-tur-gruziya': ['Активный'],
  'romanticheskiy-tur-tbilisi': ['Романтика'],
  'svadebny-tur-gruziya': ['Романтика'],
  'transfer-aeroport-tbilisi': ['Трансфер'],
  'tur-dlya-emigrantov-tbilisi': ['Релоканты'],
  'tur-dlya-relokantov-tbilisi': ['Релоканты'],
  'tur-gruziya-leto': ['Сезонные'],
  'tur-gruziya-noviy-god': ['Сезонные'],
};

function parseSubpage(slug) {
  const htmlPath = path.join(EKSKURSIYA_DIR, slug, 'index.html');
  if (!fs.existsSync(htmlPath)) return null;
  const html = fs.readFileSync(htmlPath, 'utf8');

  // Title from <title> tag
  const titleMatch = html.match(/<title>([^<]+)<\/title>/);
  let title = titleMatch ? titleMatch[1].replace(/\s*\|.*$/, '').replace(/\s*2026\s*/, ' ').trim() : slug;

  // Meta description
  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]+)"/)
    || html.match(/<meta\s+content="([^"]+)"\s+name="description"/);
  const description = descMatch ? descMatch[1] : '';

  // Price from JSON-LD offers
  const priceMatch = html.match(/"price":\s*"(\d+)"/);
  const price = priceMatch ? parseInt(priceMatch[1]) : 0;

  // Currency from JSON-LD
  const currMatch = html.match(/"priceCurrency":\s*"([^"]+)"/);
  const currency = currMatch ? currMatch[1] : 'GEL';

  // Duration from JSON-LD (PT14H or P3D format)
  let hours = 0;
  let days = 0;
  const durHMatch = html.match(/"duration":\s*"PT(\d+)H"/);
  const durDMatch = html.match(/"duration":\s*"P(\d+)D"/);
  if (durHMatch) hours = parseInt(durHMatch[1]);
  if (durDMatch) days = parseInt(durDMatch[1]);

  // OG image, with fallback to hero <img src>
  const imgMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/)
    || html.match(/<meta\s+content="([^"]+)"\s+property="og:image"/);
  let image = imgMatch ? imgMatch[1] : '/images/og-cover.jpg';

  // Check if og:image file exists, fallback to hero img src
  const imgLocalPath = image.replace('https://sakhva-travel.com', '');
  const imgDiskPath = path.join(__dirname, '..', imgLocalPath.split('?')[0]);
  if (!fs.existsSync(imgDiskPath)) {
    // Try hero <img src="/images/...">
    const heroMatch = html.match(/src="(\/images\/[a-z0-9_-]+(?:-\d+)?\.(?:webp|jpg|png))(?:\?[^"]*)?"/);
    if (heroMatch) {
      image = heroMatch[1];
    }
  }

  // Type
  const isMultiDay = MULTI_DAY_SLUGS.includes(slug);

  // Days for multi-day tours (from slug or manual)
  if (isMultiDay && days === 0) {
    const dayMatch = slug.match(/(\d+)-dn/);
    if (dayMatch) days = parseInt(dayMatch[1]);
    else if (slug === 'slow-travel') days = 3;
    else if (slug.includes('svaneti')) days = 2;
    else if (slug.includes('kazbegi-kakheti')) days = 2;
    else if (slug.includes('armeniya')) days = 5;
    else if (slug === 'tur-vsya-gruziya') days = 7;
  }

  // Auto-tag from slug keywords
  const tags = [];
  for (const [tag, keywords] of Object.entries(TAG_KEYWORDS)) {
    if (keywords.some(kw => slug.includes(kw))) {
      tags.push(tag);
    }
  }
  // Manual tag overrides
  if (MANUAL_TAGS[slug]) {
    MANUAL_TAGS[slug].forEach(t => { if (!tags.includes(t)) tags.push(t); });
  }

  // Format
  const isGroup = slug.includes('gruppa') || hours >= 10;
  const format = isGroup ? 'group' : 'individual';

  // Duration text
  let durationText = '';
  if (isMultiDay && days > 0) {
    if (days === 1) durationText = '1 день';
    else if (days >= 2 && days <= 4) durationText = `${days} дня`;
    else durationText = `${days} дней`;
  } else if (hours > 0) {
    durationText = `${hours}ч`;
  }

  return {
    slug,
    title,
    description: description.substring(0, 140),
    price,
    currency,
    hours,
    days,
    durationText,
    image,
    format,
    tags,
    type: isMultiDay ? 'tour' : 'excursion',
    url: `/ekskursiya/${slug}/`
  };
}

// Parse all subpages
const dirs = fs.readdirSync(EKSKURSIYA_DIR)
  .filter(f => {
    const fullPath = path.join(EKSKURSIYA_DIR, f);
    return f !== 'index.html' && fs.statSync(fullPath).isDirectory();
  })
  .sort();

const catalog = dirs.map(parseSubpage).filter(Boolean);

const excursions = catalog.filter(t => t.type === 'excursion');
const tours = catalog.filter(t => t.type === 'tour');

// Filter out entries with generic/duplicate hero images
const GENERIC_IMAGES = ['old-tbilisi-tour.webp', 'og-cover.jpg', 'og-cover.webp'];
function hasUniqueImage(entry) {
  const imgFile = entry.image.split('/').pop().split('?')[0];
  return !GENERIC_IMAGES.includes(imgFile);
}

const excursionsFiltered = excursions.filter(hasUniqueImage);
const toursFiltered = tours.filter(hasUniqueImage);

const result = {
  excursions: excursionsFiltered,
  tours: toursFiltered,
  stats: {
    totalExcursions: excursionsFiltered.length,
    totalTours: toursFiltered.length,
    total: excursionsFiltered.length + toursFiltered.length,
    skippedNoImage: catalog.length - excursionsFiltered.length - toursFiltered.length
  },
  generated: new Date().toISOString()
};

const outPath = path.join(__dirname, '..', 'data', 'catalog.json');
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf8');

console.log(`Parsed: ${excursions.length} excursions, ${tours.length} tours`);
console.log(`Output: ${outPath}`);

// Show tag distribution
const tagCounts = {};
excursions.forEach(e => e.tags.forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; }));
console.log('\nTag distribution (excursions):');
Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).forEach(([tag, count]) => {
  console.log(`  ${tag}: ${count}`);
});

// Show untagged
const untagged = excursions.filter(e => e.tags.length === 0);
if (untagged.length > 0) {
  console.log(`\nUntagged excursions (${untagged.length}):`);
  untagged.forEach(e => console.log(`  ${e.slug} — ${e.title}`));
}

// Show tours
console.log(`\nTours (${tours.length}):`);
tours.forEach(t => console.log(`  ${t.slug} — ${t.durationText} — ₾${t.price}`));
