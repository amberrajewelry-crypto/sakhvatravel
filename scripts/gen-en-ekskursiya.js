#!/usr/bin/env node
// Generate EN versions of /ekskursiya/ pages
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'ekskursiya');
const DST = path.join(ROOT, 'en', 'ekskursiya');

// Translation map for common patterns
const tr = {
  // Meta & structural
  'lang="ru"': 'lang="en"',
  'Экскурсия': 'Excursion',
  'Экскурсии': 'Excursions',
  'экскурсия': 'excursion',
  'экскурсии': 'excursions',
  'Sakhva Travel': 'Sakhva Travel',

  // Facts box
  'Ключевые факты': 'Key Facts',
  'Цена': 'Price',
  'Продолжительность': 'Duration',
  'Группа': 'Group',
  'Язык': 'Language',
  'до 7 человек': 'up to 7 people',
  'до 6 человек': 'up to 6 people',
  'до 10 человек': 'up to 10 people',
  'до 4 человек': 'up to 4 people',
  'Русский / English': 'Russian / English',
  'Русский': 'Russian',

  // Duration patterns
  'часов': 'hours',
  'часа': 'hours',
  'час': 'hour',
  'дней': 'days',
  'дня': 'days',
  'день': 'day',

  // Includes box
  'Включено в стоимость': 'Included',
  'Не включено': 'Not included',
  'Трансфер из Тбилиси и обратно': 'Round-trip transfer from Tbilisi',
  'Гид на русском языке': 'Russian-speaking guide',
  'Остановки для фото': 'Photo stops',
  'Питание и напитки': 'Food and drinks',

  // CTA
  'Готовы забронировать?': 'Ready to book?',
  'Забронировать экскурсию': 'Book this excursion',
  'Написать в WhatsApp': 'Write on WhatsApp',
  'Все экскурсии': 'All excursions',
  'Смотрите также:': 'See also:',
  'Подробнее о частном гиде в Тбилиси': 'Learn more about a private guide in Tbilisi',

  // Guide info
  'Тимур — Sakhva Travel': 'Timur — Sakhva Travel',
  'Тимур · Sakhva Travel · рейтинг 4.9 · 500+ туристов': 'Timur · Sakhva Travel · rating 4.9 · 500+ tourists',
  'Тимур — частный русскоязычный гид с рейтингом 4.9. Группы до 7 человек, трансфер от отеля, предоплата 10%.': 'Timur is a private Russian-speaking guide with a 4.9 rating. Groups of up to 7 people, hotel transfer, pay on the day of the tour.',
  'Тбилиси, Грузия': 'Tbilisi, Georgia',

  // Breadcrumb
  'Главная': 'Home',

  // Footer
  'Частный русскоязычный гид по Грузии 2026. Тбилиси, Казбеги, Кахетия.': 'Private Russian-speaking guide in Georgia 2026. Tbilisi, Kazbegi, Kakheti.',
  'Туры': 'Tours',
  'Блог': 'Blog',
  'Казбеги за 1 день': 'Kazbegi Day Trip',
  'Ночной Тбилиси': 'Night Tbilisi',
  'Кахетия и Сигнаги': 'Kakheti & Sighnaghi',
  'Тур для эмигрантов': 'Expat Tour',
  'Гайд: Казбеги 2026': 'Guide: Kazbegi 2026',
  '15 скрытых мест Тбилиси': '15 Hidden Gems of Tbilisi',
  'Виза в Грузию 2026': 'Georgia Visa 2026',
  'Кахетия за 1 день': 'Kakheti Day Trip',
  'Оставить отзыв ★': 'Leave a review ★',
  'На главную': 'Home',
  'Написать': 'Contact',

  // Nav
  'О нас': 'About',
  'Отзывы': 'Reviews',
  'Контакты': 'Contacts',
  'Меню': 'Menu',
  'Гид': 'Guide',

  // Common article phrases
  'Маршрут экскурсии': 'Excursion Route',
  'Практическая информация': 'Practical Information',
  'Практические советы': 'Practical Tips',
  'Часто задаваемые вопросы': 'Frequently Asked Questions',
  'Подробный маршрут и что смотреть': 'Detailed Route and What to See',
  'Что входит в стоимость': 'What\'s Included',
  'Как забронировать': 'How to Book',
  'Маршрут': 'Route',
  'Что посмотреть': 'What to See',
  'Почему стоит ехать': 'Why Visit',
  'Когда лучше ехать': 'Best Time to Visit',
  'Кому подойдёт': 'Who It\'s For',
  'Для кого': 'Who It\'s For',

  // Locale
  'ru_RU': 'en_US',
  'Русскоязычные туристы': 'English-speaking tourists',
};

// City/place translations
const places = {
  'Тбилиси': 'Tbilisi',
  'Казбеги': 'Kazbegi',
  'Казбек': 'Kazbek',
  'Кахетия': 'Kakheti',
  'Кахетии': 'Kakheti',
  'Мцхета': 'Mtskheta',
  'Мцхету': 'Mtskheta',
  'Мцхеты': 'Mtskheta',
  'Батуми': 'Batumi',
  'Грузия': 'Georgia',
  'Грузии': 'Georgia',
  'Грузию': 'Georgia',
  'Сванетия': 'Svaneti',
  'Сванетии': 'Svaneti',
  'Сванети': 'Svaneti',
  'Кутаиси': 'Kutaisi',
  'Боржоми': 'Borjomi',
  'Гудаури': 'Gudauri',
  'Сигнаги': 'Sighnaghi',
  'Сигнахи': 'Sighnaghi',
  'Давид Гареджи': 'David Gareja',
  'Ананури': 'Ananuri',
  'Вардзия': 'Vardzia',
  'Уплисцихе': 'Uplistsikhe',
  'Тушети': 'Tusheti',
  'Зугдиди': 'Zugdidi',
  'Гергети': 'Gergeti',
  'Гергетская Троица': 'Gergeti Trinity Church',
  'Светицховели': 'Svetitskhoveli',
  'Джвари': 'Jvari',
  'Нарикала': 'Narikala',
  'Абанотубани': 'Abanotubani',
  'Мтацминда': 'Mtatsminda',
  'Степанцминда': 'Stepantsminda',
  'Военно-Грузинская дорога': 'Georgian Military Highway',
  'Военно-Грузинской дороге': 'Georgian Military Highway',
  'Военно-Грузинской дорогой': 'Georgian Military Highway',
  'Крестовый перевал': 'Cross Pass',
  'Крестового перевала': 'Cross Pass',
};

function translatePage(html, slug) {
  let out = html;

  // Fix lang
  out = out.replace('lang="ru"', 'lang="en"');

  // Fix URLs: /ekskursiya/ -> /en/ekskursiya/
  out = out.replace(/href="\/ekskursiya\//g, 'href="/en/ekskursiya/');
  out = out.replace(/href="\/#/g, 'href="/en/#');
  out = out.replace(/href="\/blog\//g, 'href="/en/blog/');
  out = out.replace(/href="\/contacts\//g, 'href="/en/contacts/');
  out = out.replace(/href="\/tour\//g, 'href="/en/tour/');
  out = out.replace(/href="\/tours\//g, 'href="/en/tours/');
  out = out.replace(/href="\/chastniy-gid-tbilisi\//g, 'href="/en/');
  out = out.replace(/href="\/"(?!en)/g, 'href="/en/"');

  // Fix canonical and hreflang
  const enUrl = `https://sakhva-travel.com/en/ekskursiya/${slug}/`;
  const ruUrl = `https://sakhva-travel.com/ekskursiya/${slug}/`;
  out = out.replace(
    `<link rel="canonical" href="${ruUrl}">`,
    `<link rel="canonical" href="${enUrl}">`
  );
  out = out.replace(
    new RegExp(`<link rel="alternate" hreflang="ru" href="${ruUrl}">`),
    `<link rel="alternate" hreflang="ru" href="${ruUrl}">`
  );
  out = out.replace(
    `<link rel="alternate" hreflang="en" href="https://sakhva-travel.com/en/">`,
    `<link rel="alternate" hreflang="en" href="${enUrl}">`
  );
  out = out.replace(
    `<link rel="alternate" hreflang="x-default" href="${ruUrl}">`,
    `<link rel="alternate" hreflang="x-default" href="${enUrl}">`
  );

  // Fix og:url
  out = out.replace(
    `content="${ruUrl}"`,
    `content="${enUrl}"`
  );

  // Fix og:locale
  out = out.replace('content="ru_RU"', 'content="en_US"');

  // Fix nav links for EN
  out = out.replace(/>Туры<\/a>/g, '>Tours</a>');
  out = out.replace(/>О нас<\/a>/g, '>About</a>');
  out = out.replace(/>Отзывы<\/a>/g, '>Reviews</a>');
  out = out.replace(/>Блог<\/a>/g, '>Blog</a>');
  out = out.replace(/>Контакты<\/a>/g, '>Contacts</a>');
  out = out.replace(/>Написать<\/a>/g, '>Contact</a>');
  out = out.replace(/>Написать в WhatsApp<\/a>/g, '>Write on WhatsApp</a>');
  out = out.replace('aria-label="Меню"', 'aria-label="Menu"');
  out = out.replace('>Гид</a>', '>Guide</a>');

  // Apply translations
  Object.entries(tr).forEach(([ru, en]) => {
    // Only replace in visible text, not in URLs
    const escaped = ru.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    out = out.replace(new RegExp(escaped, 'g'), en);
  });

  // Apply place translations (careful not to break URLs)
  Object.entries(places).forEach(([ru, en]) => {
    // Only in text content, not href attributes
    const escaped = ru.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    // Replace in visible text (between > and <)
    out = out.replace(new RegExp(`(>)([^<]*?)${escaped}`, 'g'), (m, pre, mid) => {
      return pre + mid.replace(new RegExp(escaped, 'g'), en);
    });
    // Replace in content="" attributes
    out = out.replace(new RegExp(`(content="[^"]*?)${escaped}`, 'g'), (m, pre) => {
      return pre.replace(new RegExp(escaped, 'g'), ru) // keep original in content
        .replace(ru, en); // then translate
    });
  });

  // Fix footer text
  out = out.replace('>© 2026 Sakhva Travel · Тбилиси, Грузия<', '>© 2026 Sakhva Travel · Tbilisi, Georgia<');

  // Fix WA text
  out = out.replace(/text=Хочу\+узнать\+про\+туры\+2026/g, 'text=Hi!+I+want+to+book+a+tour+2026');
  out = out.replace(/text=Хочу\+забронировать\+/g, 'text=I+want+to+book+');

  // Fix breadcrumb JSON-LD
  out = out.replace('"name": "Главная"', '"name": "Home"');
  out = out.replace('"name": "Home"', '"name": "Home"');

  // Fix schema touristType
  out = out.replace('"touristType": "Русскоязычные туристы"', '"touristType": "English-speaking tourists"');
  out = out.replace('"touristType": "English-speaking tourists"', '"touristType": "English-speaking tourists"');

  return out;
}

// Create EN ekskursiya directory
if (!fs.existsSync(DST)) fs.mkdirSync(DST, { recursive: true });

const entries = fs.readdirSync(SRC, { withFileTypes: true });
let created = 0;

entries.forEach(e => {
  if (!e.isDirectory()) {
    // Handle ekskursiya/index.html
    if (e.name === 'index.html') {
      const src = path.join(SRC, 'index.html');
      const dst = path.join(DST, 'index.html');
      let html = fs.readFileSync(src, 'utf8');
      html = translatePage(html, '');
      fs.writeFileSync(dst, html);
      created++;
      console.log('Created: en/ekskursiya/index.html');
    }
    return;
  }

  const srcFile = path.join(SRC, e.name, 'index.html');
  if (!fs.existsSync(srcFile)) return;

  const dstDir = path.join(DST, e.name);
  const dstFile = path.join(dstDir, 'index.html');

  if (!fs.existsSync(dstDir)) fs.mkdirSync(dstDir, { recursive: true });

  let html = fs.readFileSync(srcFile, 'utf8');
  html = translatePage(html, e.name);
  fs.writeFileSync(dstFile, html);
  created++;
});

console.log(`Created ${created} EN ekskursiya pages`);
