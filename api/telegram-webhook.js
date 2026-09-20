export const config = { runtime: 'edge' }

// Prices updated from site schema (GEL ÷ 3.5 ≈ EUR, rounded)
const TOURS = {
  kazbegi: {
    name: 'Казбеги за 1 день', nameEn: 'Kazbegi Day Trip',
    price: '€50', gel: '₾175',
    emoji: '🏔', duration: '10-12 часов', durationEn: '10-12 hours',
    desc: 'Военно-Грузинская дорога, крепость Ананури, Гергетская Троица с видом на Казбек (5047 м). Трансфер + гид + билеты.',
    descEn: 'Georgian Military Highway, Ananuri fortress, Gergeti Trinity Church with Kazbek view (5047m). Transfer + guide + tickets.',
    img: 'https://sakhva-travel.com/images/kazbegi-tour.webp',
    url: 'sakhva-travel.com/tour/kazbegi', urlEn: 'sakhva-travel.com/en/tour/kazbegi'
  },
  kakheti: {
    name: 'Кахетия и вино', nameEn: 'Kakheti Wine Tour',
    price: '€49', gel: '₾170',
    emoji: '🍷', duration: '10-12 часов', durationEn: '10-12 hours',
    desc: 'Город любви Сигнахи, монастырь Бодбе, дегустация квеври-вина, обед у хозяйки. Группы до 6 чел.',
    descEn: 'City of Love Sighnaghi, Bodbe monastery, qvevri wine tasting, lunch at local home.',
    img: 'https://sakhva-travel.com/images/kakheti-tour.webp',
    url: 'sakhva-travel.com/tour/kakheti', urlEn: 'sakhva-travel.com/en/tour/kakheti'
  },
  tbilisi: {
    name: 'Старый Тбилиси', nameEn: 'Old Tbilisi Walking Tour',
    price: '€26', gel: '₾90',
    emoji: '🏛', duration: '3-4 часа', durationEn: '3-4 hours',
    desc: 'Серные бани Абанотубани, крепость Нарикала, монастырь Метехи, Старый базар. Пешая прогулка с гидом.',
    descEn: 'Sulfur baths, Narikala fortress, Metekhi church, Old Bazaar. 3-4 hour walk with guide.',
    img: 'https://sakhva-travel.com/images/old-tbilisi-tour.webp',
    url: 'sakhva-travel.com/tour/old-tbilisi', urlEn: 'sakhva-travel.com/en/tour/tbilisi'
  },
  hidden: {
    name: 'Скрытые места Тбилиси', nameEn: 'Hidden Tbilisi',
    price: '€27', gel: '₾94',
    emoji: '🔍', duration: '5-6 часов', durationEn: '5-6 hours',
    desc: 'Дворы-колодцы, серные бани, армянский квартал, стрит-арт, локальные кафе. Нетуристический маршрут.',
    descEn: 'Courtyards, street art, local cafes, Armenian quarter. Off the beaten path.',
    img: 'https://sakhva-travel.com/images/tbilisi-hidden.webp',
    url: 'sakhva-travel.com/tour/tbilisi-hidden', urlEn: 'sakhva-travel.com/en/tour/tbilisi-hidden'
  },
  night: {
    name: 'Ночной Тбилиси', nameEn: 'Night Tbilisi',
    price: '€27', gel: '₾94',
    emoji: '🌙', duration: '2.5-3 часа', durationEn: '2.5-3 hours',
    desc: 'Серные бани при свечах, подсвеченный Мост Мира, ужин во дворе. Старт в 20:00.',
    descEn: 'Candlelit sulfur baths, illuminated Bridge of Peace, dinner in a courtyard. Start at 8pm.',
    img: 'https://sakhva-travel.com/images/night-tbilisi-tour.webp',
    url: 'sakhva-travel.com/tour/night-tbilisi', urlEn: 'sakhva-travel.com/en/tour/night-tbilisi'
  },
  mtskheta: {
    name: 'Мцхета + Джвари', nameEn: 'Mtskheta + Jvari',
    price: '€26', gel: '₾90',
    emoji: '⛪', duration: '4-5 часов', durationEn: '4-5 hours',
    desc: 'Древняя столица Грузии. Собор Светицховели + монастырь Джвари — объекты ЮНЕСКО. 40 мин от Тбилиси.',
    descEn: 'Ancient capital of Georgia. Svetitskhoveli + Jvari monastery — UNESCO sites. 40 min from Tbilisi.',
    img: 'https://sakhva-travel.com/images/mtskheta-tour.webp',
    url: 'sakhva-travel.com/tour/mtskheta', urlEn: 'sakhva-travel.com/en/tour/mtskheta'
  },
  photo: {
    name: 'Тур + фотосессия', nameEn: 'Tour + Photoshoot',
    price: '€56', gel: '₾196',
    emoji: '📸', duration: '3-4 часа', durationEn: '3-4 hours',
    desc: 'Экскурсия + профессиональный фотограф. 30-50 обработанных фото на лучших локациях. Популярно у пар.',
    descEn: 'Tour + professional photographer. 30-50 edited photos at best locations.',
    img: 'https://sakhva-travel.com/images/photo-tour.webp',
    url: 'sakhva-travel.com/tour/photo', urlEn: 'sakhva-travel.com/en/tour/photo'
  },
  emigrant: {
    name: 'Тур для релокантов', nameEn: 'Expat Orientation Tour',
    price: '€39', gel: '₾135',
    emoji: '🧳', duration: '4-5 часов', durationEn: '4-5 hours',
    desc: 'Банки, SIM-карты, рынки, районы для аренды, тайные бары. Практический Тбилиси для переехавших.',
    descEn: 'Banks, SIM cards, markets, neighborhoods for rent. Practical Tbilisi for expats.',
    img: 'https://sakhva-travel.com/images/emigrant-tour.webp',
    url: 'sakhva-travel.com/tour/emigrant', urlEn: 'sakhva-travel.com/en/tour/emigrant'
  },
  dinner: {
    name: 'Тур + ужин у местных', nameEn: 'Tour + Local Dinner',
    price: '€61', gel: '₾213',
    emoji: '🍽', duration: '6-7 часов', durationEn: '6-7 hours',
    desc: 'Экскурсия + домашний ужин у грузинской семьи: хинкали, квеври-вино, живое общение.',
    descEn: 'Tour + homemade dinner with a Georgian family: khinkali, qvevri wine.',
    img: 'https://sakhva-travel.com/images/dinner-tour.webp',
    url: 'sakhva-travel.com/tour/dinner', urlEn: 'sakhva-travel.com/en/tour/dinner'
  },
  soviet: {
    name: 'Тбилиси обзорная', nameEn: 'Tbilisi Overview',
    price: '€39', gel: '₾135',
    emoji: '🏙️', duration: '4-5 часов', durationEn: '4-5 hours',
    desc: 'Мост Дружбы, серные бани, Метехи, Самеба, Мтацминда. Весь Тбилиси за один день.',
    descEn: 'Bridge of Peace, sulfur baths, Metekhi, Sameba, Mtatsminda. Full Tbilisi in one day.',
    img: 'https://sakhva-travel.com/images/soviet-tour.webp',
    url: 'sakhva-travel.com/tour/soviet', urlEn: 'sakhva-travel.com/en/tour/soviet'
  },
  borjomi: {
    name: 'Боржоми и Рабати', nameEn: 'Borjomi & Rabati',
    price: '€51', gel: '₾178',
    emoji: '🏔️', duration: '10-12 часов', durationEn: '10-12 hours',
    desc: 'Минеральные источники Боржоми, парк, канатная дорога и крепость Рабати в Ахалцихе.',
    descEn: 'Borjomi mineral springs, park, cable car and Rabati Fortress in Akhaltsikhe.',
    img: 'https://sakhva-travel.com/images/borjomi-tour.webp',
    url: 'sakhva-travel.com/tour/borjomi', urlEn: 'sakhva-travel.com/en/tour/borjomi'
  },
  nomad: {
    name: 'Digital Nomad Tour', nameEn: 'Digital Nomad Tour',
    price: '€35', gel: '₾123',
    emoji: '💻', duration: '3 часа', durationEn: '3 hours',
    desc: 'Лучшие коворкинги, кафе с Wi-Fi, районы для удалённой работы. На русском и английском.',
    descEn: 'Best coworkings, cafes with Wi-Fi, neighborhoods for remote work.',
    img: 'https://sakhva-travel.com/images/digital-nomad-tour.webp',
    url: 'sakhva-travel.com/tour/digital-nomad', urlEn: 'sakhva-travel.com/en/tour/digital-nomad'
  },
  slow: {
    name: 'Slow Travel — 3 дня', nameEn: 'Slow Travel — 3 Days',
    price: '€170', gel: '₾595',
    emoji: '🌿', duration: '3 дня', durationEn: '3 days',
    desc: 'Каждый день новый маршрут: Тбилиси + Кахетия + Мцхета. Трансфер из аэропорта включён. Полное погружение.',
    descEn: 'Different route each day: Tbilisi + Kakheti + Mtskheta. Airport transfer included.',
    img: 'https://sakhva-travel.com/images/slow-travel-tour.webp',
    url: 'sakhva-travel.com/tour/slow-travel', urlEn: 'sakhva-travel.com/en/tour/slow-travel'
  }
}

const TIMUR_PHOTO = 'https://sakhva-travel.com/images/timur-guide.jpg'
const IMG = 'https://sakhva-travel.com/images'

const GALLERY = {
  kazbegi: [`${IMG}/og-kazbegi.jpg`, `${IMG}/kazbegi-church.webp`],
  kakheti: [`${IMG}/og-kakheti.jpg`],
  tbilisi: [`${IMG}/og-old-tbilisi.jpg`, `${IMG}/old-tbilisi-hero.webp`],
  hidden: [`${IMG}/og-hidden-tbilisi.jpg`],
  night: [`${IMG}/og-night-tbilisi.jpg`],
  photo: [`${IMG}/og-photo-tour.jpg`],
  dinner: [`${IMG}/og-dinner.jpg`],
  soviet: [`${IMG}/og-soviet.jpg`],
  slow: [`${IMG}/og-slow-travel.jpg`]
}

const MONTHS_RU = {
  'январ': '01', 'феврал': '02', 'март': '03', 'апрел': '04',
  'мая': '05', 'май': '05', 'июн': '06', 'июл': '07', 'август': '08',
  'сентябр': '09', 'октябр': '10', 'ноябр': '11', 'декабр': '12'
}

// --- Language helpers ---
// Callback prefix: r. = Russian, e. = English
function L(lang) { return lang === 'e' ? 'en' : 'ru' }

function tourName(t, lang) { return lang === 'e' ? t.nameEn : t.name }
function tourDesc(t, lang) { return lang === 'e' ? t.descEn : t.desc }
function tourDur(t, lang) { return lang === 'e' ? t.durationEn : t.duration }
function tourUrl(t, lang) { return lang === 'e' ? t.urlEn : t.url }
// RU: GEL primary (₾), EUR secondary | EN: EUR primary (€)
function tourPrice(t, lang) { return lang === 'e' ? t.price : t.gel }
function tourPriceFull(t, lang) { return lang === 'e' ? `${t.price} (${t.gel})` : `${t.gel} (${t.price})` }

// --- Reply Keyboards ---
function replyKb(lang) {
  if (lang === 'e') {
    return {
      keyboard: [
        ['🗺 Tours', '🔥 TOP-3'],
        ['💰 Prices', '📅 Book now'],
        ['📱 Contacts', 'ℹ️ About guide'],
        ['❓ FAQ', '🔗 Share']
      ],
      resize_keyboard: true, is_persistent: true
    }
  }
  return {
    keyboard: [
      ['🗺 Туры', '🔥 ТОП-3'],
      ['💰 Цены', '📅 Забронировать'],
      ['📱 Контакты', 'ℹ️ О гиде'],
      ['❓ FAQ', '🔗 Поделиться']
    ],
    resize_keyboard: true, is_persistent: true
  }
}

// --- Inline tour grid ---
function tourGrid(lang) {
  const p = lang + '.'
  const rows = []
  const entries = Object.entries(TOURS)
  for (let i = 0; i < entries.length; i += 2) {
    const row = []
    for (let j = i; j < Math.min(i + 2, entries.length); j++) {
      const [key, t] = entries[j]
      const label = lang === 'e'
        ? `${t.emoji} ${t.nameEn.slice(0, 14)} — ${t.price}`
        : `${t.emoji} ${t.name.slice(0, 14)} — ${t.gel}`
      row.push({ text: label, callback_data: `${p}tour:${key}` })
    }
    rows.push(row)
  }
  return { inline_keyboard: rows }
}

// --- Telegram API helper ---
async function tg(token, method, body) {
  const r = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  return r.json()
}

// --- Airtable save ---
async function saveToAirtable(data) {
  const token = process.env.AIRTABLE_TOKEN
  const baseId = process.env.AIRTABLE_BASE_ID || 'appvP72OjZeVJ0XWh'
  if (!token) return null
  const today = new Date().toISOString().split('T')[0]
  try {
    const res = await fetch(
      `https://api.airtable.com/v0/${baseId}/tblI8B0GUqQtGatWp`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          fields: {
            'Имя': data.name,
            'Телефон/WhatsApp': data.phone || '',
            'Источник': 'Telegram Bot',
            'Маршрут': data.tour,
            'Дата': data.date || null,
            'Кол-во': parseInt(data.guests) || 1,
            'Статус': 'новый',
            'Дата первого контакта': today
          }
        })
      }
    )
    const client = await res.json()
    if (!res.ok) return null

    await fetch(
      `https://api.airtable.com/v0/${baseId}/tbl0rlhK4KyAMk8UB`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          fields: {
            'Тур': data.tour,
            'Дата тура': data.date || null,
            'Кол-во человек': parseInt(data.guests) || 1,
            'Статус': 'новая',
            'Заметки': `Telegram @${data.username || '—'}`,
            'Клиент': [{ id: client.id }]
          }
        })
      }
    )
    return client.id
  } catch {
    return null
  }
}

// --- Date parser (Russian + numeric) ---
function parseDate(text) {
  const iso = text.match(/(\d{4})-(\d{2})-(\d{2})/)
  if (iso) return iso[0]
  const dot = text.match(/(\d{1,2})[\.\/\-](\d{1,2})(?:[\.\/\-](\d{2,4}))?/)
  if (dot) {
    const y = dot[3] || new Date().getFullYear()
    return `${y}-${dot[2].padStart(2, '0')}-${dot[1].padStart(2, '0')}`
  }
  const ru = text.match(
    /(\d{1,2})\s+(январ\w*|феврал\w*|март\w*|апрел\w*|ма[йя]\w*|июн\w*|июл\w*|август\w*|сентябр\w*|октябр\w*|ноябр\w*|декабр\w*)/i
  )
  if (ru) {
    const day = ru[1].padStart(2, '0')
    const mw = ru[2].toLowerCase()
    for (const [pref, num] of Object.entries(MONTHS_RU)) {
      if (mw.startsWith(pref)) {
        return `${new Date().getFullYear()}-${num}-${day}`
      }
    }
  }
  return null
}

// --- Booking step parser from reply context ---
function getBookingStep(replyText) {
  if (!replyText) return null
  const m = replyText.match(/\[STEP:(\w+)\|TOUR:([^\]]+)\]/)
  if (m) return { step: m[1], tour: m[2] }
  const legacy = replyText.match(/Бронирование:\s*(.+)/)
  if (legacy) return { step: 'LEGACY', tour: legacy[1].trim() }
  return null
}

// Extract lang prefix from booking reply text
function getBookingLang(replyText) {
  if (!replyText) return 'r'
  const m = replyText.match(/\[LANG:(\w)\]/)
  return m ? m[1] : 'r'
}

// --- Tour keyword search ---
function findTourByKeyword(text) {
  const map = {
    kazbegi: ['казбег', 'kazbegi', 'степанцминда', 'гергет', 'троиц', 'военно-грузин'],
    kakheti: ['кахет', 'kakheti', 'вино', 'сигнах', 'бодбе', 'дегустац', 'марани', 'wine'],
    tbilisi: ['старый тбилиси', 'old tbilisi', 'абанотубани', 'нарикал', 'серн бан', 'старый город'],
    hidden: ['скрыт', 'hidden', 'нетуристич', 'стрит-арт', 'дворы', 'секрет'],
    night: ['ночн', 'night', 'вечерн', 'бар', 'подсветк'],
    mtskheta: ['мцхет', 'джвари', 'mtskheta', 'светицховели'],
    photo: ['фото', 'photo', 'фотосесс', 'снимк', 'instagram'],
    emigrant: ['релокант', 'эмигрант', 'переех', 'emigrant', 'переезд'],
    dinner: ['ужин', 'dinner', 'домашн', 'гастро'],
    soviet: ['обзорн', 'overview', 'по городу', 'city tour', 'весь тбилиси', 'full tbilisi'],
    borjomi: ['боржом', 'borjomi', 'рабати', 'rabati', 'ахалцихе', 'akhaltsikhe', 'минеральн'],
    nomad: ['nomad', 'номад', 'коворкинг', 'digital', 'фриланс'],
    slow: ['slow', '3 дня', 'три дня', 'несколько дней']
  }
  for (const [key, words] of Object.entries(map)) {
    for (const w of words) {
      if (text.includes(w)) return key
    }
  }
  return null
}

// --- Detect language from message text ---
function detectLang(text) {
  if (/[а-яА-ЯёЁ]/.test(text)) return 'r'
  if (/^[a-zA-Z\s\d.,!?'"()-]+$/.test(text)) return 'e'
  return 'r'
}

// --- Conversational matcher (bilingual) ---
function matchConversation(lower, name, lang) {
  const g = name ? `, ${name}` : ''
  const en = lang === 'e'

  if (/^(привет|здравствуй|хай|hi|hello|добр|салам|хеллоу|йо|ку|hey)\b/.test(lower)) {
    return {
      text: en
        ? `Hello${g}! 👋 I'm Timur's assistant in Tbilisi.\n\nPick a tour or ask me anything!`
        : `Привет${g}! 👋 Я помощник гида Тимура в Тбилиси.\n\nВыберите тур из меню или задайте любой вопрос!`
    }
  }
  if (/спасибо|благодар|thanks|thank you/.test(lower)) {
    return { text: en ? `Happy to help${g}! Feel free to ask anytime 😊` : `Рад помочь${g}! Если что — пишите, всегда на связи 😊` }
  }
  if (/погод|weather|когда лучше|когда ехать|сезон|климат|best time/.test(lower)) {
    return {
      text: en
        ? '🌤 <b>Tbilisi weather:</b>\n\n🌸 Spring (Mar-May) — 15-22°C\n☀️ Summer (Jun-Aug) — 28-35°C\n🍂 Autumn (Sep-Nov) — 15-25°C, perfect!\n❄️ Winter (Dec-Feb) — 2-8°C\n\nBest time: April-June & September-October.'
        : '🌤 <b>Погода в Тбилиси:</b>\n\n🌸 Весна (март-май) — 15-22°C\n☀️ Лето (июнь-авг) — 28-35°C\n🍂 Осень (сент-нояб) — 15-25°C, идеально!\n❄️ Зима (дек-фев) — 2-8°C\n\nЛучшее время — апрель-июнь и сентябрь-октябрь.'
    }
  }
  if (/что посмотреть|куда сходить|рекоменд|посоветуй|suggest|what to see|recommend/.test(lower)) {
    return {
      text: en
        ? `TOP-5 in Tbilisi:\n\n1. 🏔 Kazbegi — mountains, Trinity (1 day)\n2. 🍷 Kakheti — wine, Sighnaghi\n3. 🏛 Old Town — baths, Narikala\n4. ⛪ Mtskheta — ancient capital\n5. 🌙 Night Tbilisi — panorama\n\nFirst time? Kazbegi + Old Tbilisi.`
        : `ТОП-5 для Тбилиси:\n\n1. 🏔 Казбеги — горы, Троица (1 день)\n2. 🍷 Кахетия — вино, Сигнахи\n3. 🏛 Старый город — бани, Нарикала\n4. ⛪ Мцхета — древняя столица\n5. 🌙 Ночной Тбилиси — панорама\n\nДля первого раза: Казбеги + Старый Тбилиси.`
    }
  }
  if (/групп|компани|корпоратив|много людей|group|company|corporate/.test(lower)) {
    return {
      text: en
        ? `Groups of 1-20 people${g}.\n\n👫 1-4 — sedan/SUV\n👨‍👩‍👧‍👦 5-8 — minivan\n🚌 9-20 — minibus\n\n10% off for 6+ people!`
        : `Работаю с группами 1-20 чел${g}.\n\n👫 1-4 — седан/джип\n👨‍👩‍👧‍👦 5-8 — минивэн\n🚌 9-20 — микроавтобус\n\nОт 6 чел — скидка 10%. Напишите детали!`
    }
  }
  if (/дет|ребён|семь|family|child|с детьми|kids/.test(lower)) {
    return {
      text: en
        ? '👨‍👩‍👧 <b>With kids:</b>\n\n🏔 Kazbegi — kids love it (5+)\n🏛 Old Tbilisi — cable car, fortress\n🍽 Dinner tour — kids make khinkali!\n\nChild seat — free. Family-friendly pace.'
        : '👨‍👩‍👧 <b>С детьми:</b>\n\n🏔 Казбеги — дети в восторге (от 5 лет)\n🏛 Старый Тбилиси — канатка, крепость\n🍽 Ужин у местных — дети лепят хинкали!\n\nДетское кресло — бесплатно. Темп под семью.'
    }
  }
  if (/трансфер|аэропорт|airport|transfer|встрет|pickup/.test(lower)) {
    return {
      text: en
        ? '🚗 <b>Transfer:</b>\n\n• Tbilisi airport ↔ city — €15\n• Kutaisi ↔ Tbilisi — €80\n• Included in all tours!\n\nI meet with a sign.'
        : '🚗 <b>Трансфер:</b>\n\n• Аэропорт Тбилиси ↔ город — €15\n• Кутаиси ↔ Тбилиси — €80\n• Включён во все туры!\n\nВстречу с табличкой.',
      markup: {
        inline_keyboard: [[{
          text: en ? '📱 Book transfer' : '📱 Заказать трансфер',
          url: 'https://wa.me/995511272623?text=' +
            encodeURIComponent(en ? 'I need a transfer' : 'Нужен трансфер')
        }]]
      }
    }
  }
  if (/где поесть|ресторан|хинкали|хачапури|кухня|food|eat|restaurant/.test(lower)) {
    return {
      text: en
        ? '🍽 <b>Where to eat:</b>\n\n• Khinkali — Pasanauri, Zakhar Zakharich\n• Khachapuri — Retro\n• Shashlik — Deserter Bazaar\n• Wine — any marani in Kakheti\n\nOr Tour + local dinner — €71!'
        : '🍽 <b>Где поесть:</b>\n\n• Хинкали — Pasanauri, Захар Захарыч\n• Хачапури — Retro\n• Шашлык — Дезертирский базар\n• Вино — любая марани в Кахетии\n\nИли тур + ужин у местных — ₾250!',
      markup: {
        inline_keyboard: [[{ text: en ? '🍽 Tour + dinner' : '🍽 Тур + ужин', callback_data: `${lang}.tour:dinner` }]]
      }
    }
  }
  if (/оплат|как платить|карт|нал|cash|pay|предоплат|payment/.test(lower)) {
    return {
      text: en
        ? '💳 <b>Payment:</b>\n\n• Pay on tour day\n• Cash (GEL/EUR/USD)\n• Bank transfer\n• Crypto (BTC, ETH, USDT)\n\nFree cancellation 24h before.'
        : '💳 <b>Оплата:</b>\n\n• Оплата в день тура\n• Наличные (лари/евро/доллар)\n• Перевод на карту\n• Крипто (BTC, ETH, USDT)\n\nОтмена бесплатно за 24 часа.'
    }
  }
  if (/отзыв|review|рейтинг|rating/.test(lower)) {
    return {
      text: en
        ? '⭐ <b>Reviews:</b>\n\n"Best guide in Tbilisi!" — Anna\n"Showed places tourists never find" — Dmitry\n"Perfect with kids" — Olga\n\n4.9 ⭐ on Google Maps'
        : '⭐ <b>Отзывы:</b>\n\n«Лучший гид в Тбилиси!» — Анна\n«Показал места, куда туристы не ходят» — Дмитрий\n«С детьми было идеально» — Ольга\n\n4.9 ⭐ на Google Maps',
      markup: {
        inline_keyboard: [[{
          text: en ? '🌐 All reviews' : '🌐 Все отзывы',
          url: 'https://sakhva-travel.com/#reviews'
        }]]
      }
    }
  }
  if (/батум|batumi|море|пляж|beach|sea/.test(lower)) {
    return {
      text: en
        ? '🏖 <b>Batumi:</b>\n\n5-6h by car or 30 min flight.\nTransfer Tbilisi → Batumi — from €120.\n\nI can arrange a tour!'
        : '🏖 <b>Батуми:</b>\n\n5-6 часов на авто или 30 мин самолёт.\nТрансфер Тбилиси → Батуми — от €120.\n\nМогу организовать тур, пишите!'
    }
  }
  if (/виз|visa|документ|паспорт|границ|passport/.test(lower)) {
    return {
      text: en
        ? '🛂 <b>Visa:</b>\n\n• Russia, Ukraine, Belarus — visa-free up to 1 year\n• EU, USA — visa-free up to 1 year\n\nJust bring your passport!'
        : '🛂 <b>Виза:</b>\n\n• Россия, Украина, Беларусь — без визы до 1 года\n• ЕС, США — без визы до 1 года\n\nНужен только загранпаспорт!'
    }
  }
  if (/безопасн|safe|опасн|danger/.test(lower)) {
    return {
      text: en
        ? '🛡 Georgia is one of the safest countries in Europe.\nTbilisi is safe day and night. Even safer with a guide!'
        : '🛡 Грузия — одна из самых безопасных стран Европы.\nТбилиси безопасен днём и ночью. С гидом — ещё спокойнее!'
    }
  }
  if (/язык|english|по-английски|language/.test(lower)) {
    return {
      text: en
        ? 'Timur gives tours in Russian and English. Choose what works!'
        : 'Тимур проводит туры на русском и английском. Выбирайте удобный!'
    }
  }
  if (/сколько.*час|длительн|duration|how long/.test(lower)) {
    return {
      text: en
        ? '⏱ <b>Duration:</b>\n\n🏛 Walking — 3-4h\n⛪ Mtskheta — 4-5h\n🏔 Kazbegi — 10-12h\n🍷 Kakheti — 10-12h\n🌿 Slow — 3 days\n\nStart 9-10am. Flexible!'
        : '⏱ <b>Длительность:</b>\n\n🏛 Пешие — 3-4 ч\n⛪ Мцхета — 4-5 ч\n🏔 Казбеги — 10-12 ч\n🍷 Кахетия — 10-12 ч\n🌿 Slow — 3 дня\n\nСтарт 9:00-10:00. Гибко!'
    }
  }
  if (/релокац|переезд|жить в грузии|переехать|relocat|expat|moving/.test(lower)) {
    return {
      text: en
        ? '🧳 Special tour for expats!\nBanks, SIM, markets, rent — all in 1 day, from €39.'
        : '🧳 Для релокантов — специальный тур!\nБанки, SIM, рынки, аренда — всё за 1 день, от ₾135.',
      markup: {
        inline_keyboard: [
          [{ text: en ? '🧳 Expat Tour' : '🧳 Тур для релокантов', callback_data: `${lang}.tour:emigrant` }],
          [{ text: '💻 Digital Nomad', callback_data: `${lang}.tour:nomad` }]
        ]
      }
    }
  }
  return null
}

// =================== HANDLER ===================
export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('OK', { status: 200 })
  }

  const BOT = process.env.TELEGRAM_BOT_TOKEN
  const NOTIFY = process.env.TELEGRAM_MANAGER_CHAT || process.env.TELEGRAM_CHAT_ID
  const MGR = process.env.TELEGRAM_MANAGER_TOKEN || BOT  // manager alerts go to whatsapp_manager bot
  if (!BOT) return new Response('No token', { status: 500 })

  let upd
  try { upd = await req.json() } catch { return new Response('OK') }

  // ========== CALLBACK QUERY ==========
  if (upd.callback_query) {
    const cb = upd.callback_query
    const cid = cb.message.chat.id
    const d = cb.data
    const nm = cb.from?.first_name || ''

    await tg(BOT, 'answerCallbackQuery', { callback_query_id: cb.id })

    // --- Language selection ---
    if (d === 'lang:r' || d === 'lang:e') {
      const lang = d.split(':')[1]
      const en = lang === 'e'

      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              `Hello${nm ? ', ' + nm : ''}! 👋`,
              '',
              "I'm <b>Timur</b>, your private guide in Tbilisi, Georgia.",
              '',
              '🗺 12 unique tours',
              '💰 from €26/person, all included',
              '🚗 Comfortable car with AC',
              '📅 Book in 2 minutes',
              '',
              'Choose a tour below 👇'
            ].join('\n')
          : [
              `Гамарджоба${nm ? ', ' + nm : ''}! 👋`,
              '',
              'Меня зовут <b>Тимур</b>, я частный гид в Тбилиси.',
              '',
              'Покажу настоящую Грузию — не туристические маршруты,',
              'а места, куда ходят сами грузины.',
              '',
              '🗺 12 авторских туров',
              '💰 от ₾90/чел, всё включено',
              '🚗 Комфортный авто с кондиционером',
              '📅 Бронь за 2 минуты',
              '',
              'Выберите тур или задайте вопрос — помогу! 👇'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: replyKb(lang)
      })

      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en ? '🗺 <b>Tour catalog:</b>' : '🗺 <b>Каталог туров:</b>',
        parse_mode: 'HTML',
        reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    // Parse lang prefix from callback: "r.tour:kazbegi" or "e.tour:kazbegi"
    // Also support legacy "tour:kazbegi" (default to Russian)
    let lang = 'r'
    let action = d
    if (d.length > 2 && d[1] === '.') {
      lang = d[0]
      action = d.slice(2)
    }
    const en = lang === 'e'

    // --- Tour card ---
    if (action.startsWith('tour:')) {
      const key = action.split(':')[1]
      const t = TOURS[key]
      if (!t) return new Response('OK')

      const caption = [
        `${t.emoji} <b>${tourName(t, lang)}</b>`,
        '',
        tourDesc(t, lang),
        '',
        `💰 ${en ? 'from' : 'от'} <b>${tourPrice(t, lang)}</b>/${en ? 'person' : 'чел'} (${en ? t.gel : t.price})`,
        `⏱ ${tourDur(t, lang)}`,
        '',
        en ? '✅ Transfer + guide + tickets included' : '✅ Трансфер + гид + входные включены',
        en ? '✅ Pay on tour day' : '✅ Оплата в день тура',
        en ? '✅ Free cancellation 24h before' : '✅ Отмена бесплатно за 24ч'
      ].join('\n')

      const buttons = [
        [{ text: en ? '📅 Book now' : '📅 Забронировать', callback_data: `${lang}.book:${key}` }],
        [
          { text: en ? '🌐 Website' : '🌐 На сайте', url: `https://${tourUrl(t, lang)}` },
          {
            text: '📱 WhatsApp',
            url: 'https://wa.me/995511272623?text=' +
              encodeURIComponent(en ? `I want: ${t.nameEn}` : `Хочу: ${t.name}`)
          }
        ]
      ]
      if (GALLERY[key] && GALLERY[key].length > 0) {
        buttons.push([{ text: en ? '🖼 More photos' : '🖼 Ещё фото', callback_data: `${lang}.gallery:${key}` }])
      }
      buttons.push([{ text: en ? '⬅️ All tours' : '⬅️ Все туры', callback_data: `${lang}.menu` }])

      await tg(BOT, 'sendPhoto', {
        chat_id: cid,
        photo: t.img,
        caption,
        parse_mode: 'HTML',
        reply_markup: { inline_keyboard: buttons }
      })
      return new Response('OK')
    }

    // --- Start booking: step 1 — ask name ---
    if (action.startsWith('book:')) {
      const key = action.split(':')[1]
      const t = TOURS[key]
      const tn = t ? tourName(t, lang) : (en ? 'tour' : 'тур')

      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? `📝 <b>Booking: ${tn}</b>\n\nWhat is your name?\n\n<i>[STEP:NAME|TOUR:${tn}][LANG:${lang}]</i>`
          : `📝 <b>Бронирование: ${tn}</b>\n\nКак вас зовут?\n\n<i>[STEP:NAME|TOUR:${tn}][LANG:${lang}]</i>`,
        parse_mode: 'HTML',
        reply_markup: { force_reply: true, input_field_placeholder: en ? 'Your name' : 'Ваше имя' }
      })
      return new Response('OK')
    }

    // --- Prices ---
    if (action === 'prices') {
      let txt = en ? '💰 <b>Tour prices</b> (all included):\n\n' : '💰 <b>Цены на туры</b> (всё включено):\n\n'
      for (const [, t] of Object.entries(TOURS)) {
        txt += `${t.emoji} ${tourName(t, lang)} — ${en ? 'from ' : 'от '}${tourPrice(t, lang)}\n`
      }
      txt += en
        ? '\n✅ Transfer + guide + tickets\n✅ Pay on tour day'
        : '\n✅ Трансфер + гид + входные\n✅ Оплата в день тура'
      await tg(BOT, 'sendMessage', {
        chat_id: cid, text: txt, parse_mode: 'HTML',
        reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    // --- Contacts ---
    if (action === 'contacts') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              '📱 <b>Contact Timur:</b>',
              '',
              '• WhatsApp: +995 511 272 623',
              '• Telegram: @SakhvaGuideBot',
              '• Website: sakhva-travel.com',
              '',
              'Usually replies within 15 minutes!'
            ].join('\n')
          : [
              '📱 <b>Связаться с Тимуром:</b>',
              '',
              '• WhatsApp: +995 511 272 623',
              '• Telegram: @SakhvaGuideBot',
              '• Сайт: sakhva-travel.com',
              '',
              'Отвечаю за 15 минут!'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [
              { text: '📱 WhatsApp', url: 'https://wa.me/995511272623' },
              { text: en ? '🌐 Website' : '🌐 Сайт', url: en ? 'https://sakhva-travel.com/en/' : 'https://sakhva-travel.com' }
            ],
            [{ text: en ? '⬅️ All tours' : '⬅️ Все туры', callback_data: `${lang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    // --- About ---
    if (action === 'about') {
      await tg(BOT, 'sendPhoto', {
        chat_id: cid,
        photo: TIMUR_PHOTO,
        caption: en
          ? [
              'ℹ️ <b>Timur — your guide in Tbilisi</b>',
              '',
              '📍 Living in Georgia, knows every corner',
              '🗣 Russian & English',
              '🚗 Comfortable car with AC',
              '⭐ 4.9 on Google Maps | 50+ clients',
              '',
              'Not an agency — personal approach to everyone.'
            ].join('\n')
          : [
              'ℹ️ <b>Тимур — ваш гид в Тбилиси</b>',
              '',
              '📍 Живу в Грузии, знаю каждый закоулок',
              '🗣 Русский и English',
              '🚗 Комфортный авто с кондиционером',
              '⭐ 4.9 на Google Maps | 50+ клиентов',
              '',
              'Не агентство — личный подход к каждому.'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: en ? '⭐ Reviews' : '⭐ Отзывы', url: 'https://sakhva-travel.com/#reviews' }],
            [{ text: en ? '🗺 Tours' : '🗺 Туры', callback_data: `${lang}.menu` }],
            [{ text: '📱 WhatsApp', url: 'https://wa.me/995511272623' }]
          ]
        }
      })
      return new Response('OK')
    }

    // --- Menu (tour grid) ---
    if (action === 'menu') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? `Choose a tour${nm ? ', ' + nm : ''}:`
          : `Выберите тур${nm ? ', ' + nm : ''}:`,
        reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    // --- Photo gallery ---
    if (action.startsWith('gallery:')) {
      const key = action.split(':')[1]
      const t = TOURS[key]
      const extra = GALLERY[key]
      if (!t || !extra || extra.length === 0) return new Response('OK')

      const media = [
        { type: 'photo', media: t.img, caption: `${t.emoji} ${tourName(t, lang)}`, parse_mode: 'HTML' },
        ...extra.map(url => ({ type: 'photo', media: url }))
      ]
      await tg(BOT, 'sendMediaGroup', { chat_id: cid, media })
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: `${t.emoji} <b>${tourName(t, lang)}</b> — ${en ? 'from ' : 'от '}${tourPrice(t, lang)}/${en ? 'person' : 'чел'}`,
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: en ? '📅 Book now' : '📅 Забронировать', callback_data: `${lang}.book:${key}` }],
            [{ text: en ? '⬅️ All tours' : '⬅️ Все туры', callback_data: `${lang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    // --- Post-tour review request ---
    if (action === 'review') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              '⭐ <b>Thanks for the tour with Timur!</b>',
              '',
              'If you enjoyed it — please leave a review.',
              "It takes 1 minute and helps a lot!",
              '',
              'Every review = another happy tourist 😊'
            ].join('\n')
          : [
              '⭐ <b>Спасибо за тур с Тимуром!</b>',
              '',
              'Если вам понравилось — оставьте отзыв.',
              'Это займёт 1 минуту и очень поможет!',
              '',
              'Каждый отзыв = новый довольный турист 😊'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: '⭐ Google Maps', url: 'https://g.page/r/CaUzuaJELU4aEB0/review' }],
            [{
              text: en ? '📤 Share with a friend' : '📤 Рекомендовать другу',
              url: 'https://t.me/share/url?url=https://t.me/SakhvaGuideBot&text=' +
                encodeURIComponent(en ? 'Had a tour with Timur in Tbilisi — recommend! 🇬🇪' : 'Был на туре с Тимуром в Тбилиси — рекомендую! 🇬🇪')
            }],
            [{ text: en ? '🗺 More tours' : '🗺 Ещё туры', callback_data: `${lang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    return new Response('OK')
  }

  // ========== INLINE QUERY ==========
  if (upd.inline_query) {
    const q = (upd.inline_query.query || '').toLowerCase()
    const results = []
    let id = 1

    for (const [key, t] of Object.entries(TOURS)) {
      const match = !q ||
        t.name.toLowerCase().includes(q) ||
        t.nameEn.toLowerCase().includes(q) ||
        t.desc.toLowerCase().includes(q) ||
        key.includes(q)

      if (match) {
        results.push({
          type: 'article',
          id: String(id++),
          title: `${t.emoji} ${t.name} — ${t.price}`,
          description: `${t.duration} | ${t.desc.slice(0, 80)}...`,
          thumbnail_url: t.img,
          input_message_content: {
            message_text: [
              `${t.emoji} <b>${t.name}</b> — от ${t.price}/чел`,
              '',
              t.desc,
              '',
              `⏱ ${t.duration}`,
              '✅ Всё включено. Оплата в день тура.',
              '',
              `🔗 Подробнее: https://${t.url}`,
              '📅 Забронировать: https://t.me/SakhvaGuideBot'
            ].join('\n'),
            parse_mode: 'HTML'
          },
          reply_markup: {
            inline_keyboard: [
              [{ text: '📅 Забронировать', url: 'https://t.me/SakhvaGuideBot?start=book' }],
              [{ text: '🌐 На сайте', url: `https://${t.url}` }]
            ]
          }
        })
      }
    }

    await tg(BOT, 'answerInlineQuery', {
      inline_query_id: upd.inline_query.id,
      results: results.slice(0, 12),
      cache_time: 300,
      switch_pm_text: '🗺 Открыть каталог',
      switch_pm_parameter: 'inline'
    })
    return new Response('OK')
  }

  // ========== MESSAGE ==========
  if (upd.message) {
    const msg = upd.message
    const cid = msg.chat.id
    const txt = (msg.text || '').trim()
    const fname = msg.from?.first_name || ''
    const uname = msg.from?.username || ''

    // --- /start → language picker ---
    if (txt === '/start' || txt.startsWith('/start ')) {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: [
          `${fname ? fname + ', ' : ''}🇬🇪`,
          '',
          '🇷🇺 Выберите язык',
          '🇬🇧 Choose your language'
        ].join('\n'),
        reply_markup: {
          inline_keyboard: [
            [
              { text: '🇷🇺 Русский', callback_data: 'lang:r' },
              { text: '🇬🇧 English', callback_data: 'lang:e' }
            ]
          ]
        }
      })
      return new Response('OK')
    }

    // --- Detect language from reply keyboard buttons ---
    // Russian buttons
    const ruButtons = {
      '🗺 Туры': 'tours', '🔥 ТОП-3': 'top3', '💰 Цены': 'prices',
      '📅 Забронировать': 'book', '📱 Контакты': 'contacts',
      'ℹ️ О гиде': 'about', '❓ FAQ': 'faq', '🔗 Поделиться': 'share'
    }
    // English buttons
    const enButtons = {
      '🗺 Tours': 'tours', '🔥 TOP-3': 'top3', '💰 Prices': 'prices',
      '📅 Book now': 'book', '📱 Contacts': 'contacts',
      'ℹ️ About guide': 'about', '❓ FAQ': 'faq', '🔗 Share': 'share'
    }

    let btnAction = ruButtons[txt]
    let lang = 'r'
    if (!btnAction) {
      btnAction = enButtons[txt]
      if (btnAction) lang = 'e'
    }
    const en = lang === 'e'

    if (btnAction === 'tours') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en ? '🗺 <b>Tour catalog:</b>' : '🗺 <b>Каталог туров:</b>',
        parse_mode: 'HTML', reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    if (btnAction === 'prices') {
      let p = en ? '💰 <b>Prices</b> (all included):\n\n' : '💰 <b>Цены</b> (всё включено):\n\n'
      for (const [, t] of Object.entries(TOURS)) {
        p += `${t.emoji} ${tourName(t, lang)} — ${en ? 'from ' : 'от '}${tourPrice(t, lang)}\n`
      }
      p += en
        ? '\n✅ Pay on tour day.'
        : '\n✅ Оплата в день тура.'
      await tg(BOT, 'sendMessage', {
        chat_id: cid, text: p, parse_mode: 'HTML', reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    if (btnAction === 'book') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en ? 'Choose a tour to book:' : 'Выберите тур для бронирования:',
        reply_markup: tourGrid(lang)
      })
      return new Response('OK')
    }

    if (btnAction === 'contacts') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? '📱 <b>Timur\'s contacts:</b>\n\n• WhatsApp: +995 511 272 623\n• Telegram: @SakhvaGuideBot\n• Website: sakhva-travel.com'
          : '📱 <b>Контакты Тимура:</b>\n\n• WhatsApp: +995 511 272 623\n• Telegram: @SakhvaGuideBot\n• Сайт: sakhva-travel.com',
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [
              { text: '📱 WhatsApp', url: 'https://wa.me/995511272623' },
              { text: en ? '🌐 Website' : '🌐 Сайт', url: en ? 'https://sakhva-travel.com/en/' : 'https://sakhva-travel.com' }
            ]
          ]
        }
      })
      return new Response('OK')
    }

    if (btnAction === 'about') {
      await tg(BOT, 'sendPhoto', {
        chat_id: cid,
        photo: TIMUR_PHOTO,
        caption: en
          ? [
              'ℹ️ <b>Timur — your guide in Tbilisi</b>',
              '',
              '📍 Living in Georgia, knows every corner',
              '🗣 Russian & English',
              '🚗 Comfortable car with AC',
              '⭐ 4.9 on Google Maps',
              '👥 50+ happy clients',
              '',
              'Not a bus tour — personal approach.',
              'I show places locals go to.',
              '',
              'Tours every day, 7 days a week.'
            ].join('\n')
          : [
              'ℹ️ <b>Тимур — ваш гид в Тбилиси</b>',
              '',
              '📍 Живу в Грузии, знаю каждый закоулок',
              '🗣 Русский и English',
              '🚗 Комфортный авто с кондиционером',
              '⭐ 4.9 на Google Maps',
              '👥 50+ довольных клиентов',
              '',
              'Не агентство, не автобус — личный подход.',
              'Покажу места, куда ходят сами грузины.',
              '',
              'Провожу туры каждый день, 7 дней в неделю.'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: en ? '⭐ Reviews' : '⭐ Отзывы', url: 'https://sakhva-travel.com/#reviews' }],
            [{ text: en ? '🗺 Choose tour' : '🗺 Выбрать тур', callback_data: `${lang}.menu` }],
            [{ text: en ? '📱 Message Timur' : '📱 Написать Тимуру', url: 'https://wa.me/995511272623' }]
          ]
        }
      })
      return new Response('OK')
    }

    if (btnAction === 'faq') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              '❓ <b>FAQ:</b>',
              '',
              '<b>Is prepayment required?</b>',
              'No. Pay on tour day — cash, card, or crypto.',
              '',
              '<b>Can I cancel?</b>',
              'Yes, free cancellation 24h before.',
              '',
              "<b>What's included?</b>",
              'Transfer, guide, tickets. Food is extra (except dinner tour).',
              '',
              '<b>Group size?</b>',
              'Private! Just you and your guide. No bus.',
              '',
              '<b>What language?</b>',
              'Russian & English.',
              '',
              '<b>Do I need a visa?</b>',
              'No. Russia, Ukraine, Belarus, EU — visa-free up to 1 year.',
              '',
              '<b>Child seat available?</b>',
              'Yes, free. Just mention when booking.'
            ].join('\n')
          : [
              '❓ <b>Частые вопросы:</b>',
              '',
              '<b>Нужна ли предоплата?</b>',
              'Нет. Оплата в день тура наличными, картой или крипто.',
              '',
              '<b>Можно ли отменить?</b>',
              'Да, бесплатно за 24 часа.',
              '',
              '<b>Что включено в цену?</b>',
              'Трансфер, гид, входные билеты. Еда — за ваш счёт (кроме тура с ужином).',
              '',
              '<b>Сколько человек в группе?</b>',
              'Индивидуально! Только вы и гид. Не автобус.',
              '',
              '<b>На каком языке?</b>',
              'Русский и English.',
              '',
              '<b>Нужна ли виза?</b>',
              'Нет. РФ, Украина, Беларусь, ЕС — без визы до 1 года.',
              '',
              '<b>Есть ли детское кресло?</b>',
              'Да, бесплатно. Скажите при бронировании.'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: en ? '🗺 Choose tour' : '🗺 Выбрать тур', callback_data: `${lang}.menu` }],
            [{
              text: en ? '📱 Ask Timur' : '📱 Спросить Тимура',
              url: 'https://wa.me/995511272623?text=' +
                encodeURIComponent(en ? 'Question about a tour' : 'Вопрос по туру')
            }]
          ]
        }
      })
      return new Response('OK')
    }

    if (btnAction === 'top3') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              '🔥 <b>TOP-3 — most popular tours:</b>',
              '',
              '1. 🏔 <b>Kazbegi Day Trip</b> — €56',
              'Mountains, Trinity Church, Military Highway. Most impressive!',
              '',
              '2. 🍷 <b>Kakheti Wine Tour</b> — €56',
              'Sighnaghi, tasting, lunch at local home. For wine lovers.',
              '',
              '3. 🏛 <b>Old Tbilisi</b> — €47',
              'Sulfur baths, Narikala, Metekhi. Perfect for day one.',
              '',
              '💡 First time in Georgia? Take Kazbegi + Old Tbilisi.'
            ].join('\n')
          : [
              '🔥 <b>ТОП-3 — самые популярные туры:</b>',
              '',
              '1. 🏔 <b>Казбеги за 1 день</b> — ₾205',
              'Горы, Троица, Военно-Грузинская дорога. Самый впечатляющий тур!',
              '',
              '2. 🍷 <b>Кахетия и вино</b> — ₾205',
              'Сигнахи, дегустация, обед у хозяйки. Для ценителей вина.',
              '',
              '3. 🏛 <b>Старый Тбилиси</b> — ₾165',
              'Серные бани, Нарикала, Метехи. Идеально для первого дня.',
              '',
              '💡 Первый раз в Грузии? Берите Казбеги + Старый Тбилиси.'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: en ? '🏔 Kazbegi' : '🏔 Казбеги', callback_data: `${lang}.tour:kazbegi` }],
            [{ text: en ? '🍷 Kakheti' : '🍷 Кахетия', callback_data: `${lang}.tour:kakheti` }],
            [{ text: en ? '🏛 Old Tbilisi' : '🏛 Старый Тбилиси', callback_data: `${lang}.tour:tbilisi` }],
            [{ text: en ? '🗺 All 12 tours' : '🗺 Все 12 туров', callback_data: `${lang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    if (btnAction === 'share') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: en
          ? [
              '🔗 <b>Share this bot with friends!</b>',
              '',
              'If you liked the service — tell your friends.',
              'Timur will appreciate it 😊'
            ].join('\n')
          : [
              '🔗 <b>Поделитесь ботом с друзьями!</b>',
              '',
              'Если вам понравился сервис — расскажите друзьям.',
              'Им будет полезно, а Тимуру приятно 😊'
            ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{
              text: en ? '📤 Send to a friend' : '📤 Отправить другу',
              url: 'https://t.me/share/url?url=https://t.me/SakhvaGuideBot&text=' +
                encodeURIComponent(en ? 'Great guide in Tbilisi! Tours from €26, book in 2 min 🇬🇪' : 'Отличный гид в Тбилиси! Туры от ₾90, бронь за 2 минуты 🇬🇪')
            }],
            [{
              text: en ? '⭐ Leave a Google review' : '⭐ Оставить отзыв на Google',
              url: 'https://g.page/r/CaUzuaJELU4aEB0/review'
            }],
            [{ text: en ? '🗺 All tours' : '🗺 Все туры', callback_data: `${lang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    // --- Commands ---
    if (txt === '/tours' || txt === '/menu') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid, text: '🗺 <b>Каталог туров:</b>',
        parse_mode: 'HTML', reply_markup: tourGrid('r')
      })
      return new Response('OK')
    }

    if (txt === '/prices') {
      let p = '💰 <b>Цены</b> (всё включено):\n\n'
      for (const [, t] of Object.entries(TOURS)) {
        p += `${t.emoji} ${t.name} — от ${t.gel}\n`
      }
      p += '\n✅ Оплата в день тура.'
      await tg(BOT, 'sendMessage', {
        chat_id: cid, text: p, parse_mode: 'HTML', reply_markup: tourGrid('r')
      })
      return new Response('OK')
    }

    if (txt === '/contacts') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: '📱 WhatsApp: +995 511 272 623\n🌐 sakhva-travel.com\nОтвет за 15 минут!',
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: '📱 WhatsApp', url: 'https://wa.me/995511272623' }]
          ]
        }
      })
      return new Response('OK')
    }

    if (txt === '/help') {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: [
          '❓ <b>Что умеет этот бот:</b>',
          '',
          '🗺 <b>Туры</b> — каталог с описаниями и фото',
          '💰 <b>Цены</b> — актуальные цены в GEL и EUR',
          '📅 <b>Забронировать</b> — бронь за 2 минуты',
          '📱 <b>Контакты</b> — WhatsApp, сайт',
          'ℹ️ <b>О гиде</b> — про Тимура',
          '',
          'Или просто напишите вопрос:',
          '• «Что посмотреть за 1 день?»',
          '• «Какая погода в мае?»',
          '• «Есть ли тур с детьми?»',
          '• «Нужна ли виза?»',
          '',
          '/tours — каталог | /prices — цены',
          '/contacts — связь | /help — помощь'
        ].join('\n'),
        parse_mode: 'HTML',
        reply_markup: replyKb('r')
      })
      return new Response('OK')
    }

    // --- Step-by-step booking (force_reply chain) ---
    const isReply = msg.reply_to_message?.from?.is_bot
    if (isReply) {
      const rTxt = msg.reply_to_message.text || ''
      const step = getBookingStep(rTxt)
      const bLang = getBookingLang(rTxt)
      const bEn = bLang === 'e'

      if (step) {
        const tour = step.tour

        // Step 1: got name → ask phone
        if (step.step === 'NAME') {
          const name = txt
          await tg(BOT, 'sendMessage', {
            chat_id: cid,
            text: bEn
              ? `👤 ${name}\n\nYour phone or WhatsApp?\n\n<i>[STEP:PHONE|TOUR:${tour}|NAME:${name}][LANG:${bLang}]</i>`
              : `👤 ${name}\n\nТелефон или WhatsApp для связи?\n\n<i>[STEP:PHONE|TOUR:${tour}|NAME:${name}][LANG:${bLang}]</i>`,
            parse_mode: 'HTML',
            reply_markup: {
              force_reply: true,
              input_field_placeholder: bEn ? '+1... or WhatsApp' : '+7... или WhatsApp номер'
            }
          })
          return new Response('OK')
        }

        // Step 2: got phone → ask date
        if (step.step === 'PHONE') {
          const nameM = rTxt.match(/NAME:([^\]|]+)/)
          const name = nameM ? nameM[1] : ''
          const phone = txt

          await tg(BOT, 'sendMessage', {
            chat_id: cid,
            text: bEn
              ? `📱 ${phone}\n\nWhat date? (e.g.: May 5, 15/06)\n\n<i>[STEP:DATE|TOUR:${tour}|NAME:${name}|PHONE:${phone}][LANG:${bLang}]</i>`
              : `📱 ${phone}\n\nКакая дата? (например: 5 мая, 15.06)\n\n<i>[STEP:DATE|TOUR:${tour}|NAME:${name}|PHONE:${phone}][LANG:${bLang}]</i>`,
            parse_mode: 'HTML',
            reply_markup: {
              force_reply: true,
              input_field_placeholder: bEn ? 'Tour date' : 'Дата тура'
            }
          })
          return new Response('OK')
        }

        // Step 3: got date → ask guests
        if (step.step === 'DATE') {
          const nameM = rTxt.match(/NAME:([^|]+)/)
          const phoneM = rTxt.match(/PHONE:([^\]|]+)/)
          const name = nameM ? nameM[1] : ''
          const phone = phoneM ? phoneM[1] : ''
          const date = parseDate(txt) || txt

          await tg(BOT, 'sendMessage', {
            chat_id: cid,
            text: bEn
              ? `📅 ${txt}\n\nHow many people?\n\n<i>[STEP:GUESTS|TOUR:${tour}|NAME:${name}|PHONE:${phone}|DATE:${date}][LANG:${bLang}]</i>`
              : `📅 ${txt}\n\nСколько человек?\n\n<i>[STEP:GUESTS|TOUR:${tour}|NAME:${name}|PHONE:${phone}|DATE:${date}][LANG:${bLang}]</i>`,
            parse_mode: 'HTML',
            reply_markup: {
              force_reply: true,
              input_field_placeholder: bEn ? 'Number of people' : 'Кол-во человек'
            }
          })
          return new Response('OK')
        }

        // Step 4: got guests → confirm & save
        if (step.step === 'GUESTS') {
          const nameM = rTxt.match(/NAME:([^|]+)/)
          const phoneM = rTxt.match(/PHONE:([^|]+)/)
          const dateM = rTxt.match(/DATE:([^\]|]+)/)
          const name = nameM ? nameM[1] : ''
          const phone = phoneM ? phoneM[1] : ''
          const date = dateM ? dateM[1] : ''
          const guests = txt.replace(/\D/g, '') || '1'

          const booking = { name, phone, date, guests, tour, username: uname }
          const saved = await saveToAirtable(booking)

          await tg(BOT, 'sendMessage', {
            chat_id: cid,
            text: bEn
              ? [
                  '✅ <b>Booking confirmed!</b>',
                  '',
                  `🗺 ${tour}`,
                  `👤 ${name}`,
                  `📱 ${phone}`,
                  `📅 ${date || 'TBD'}`,
                  `👥 ${guests} people`,
                  '',
                  'Timur will contact you shortly!',
                  'Usually replies within 15 minutes.'
                ].join('\n')
              : [
                  '✅ <b>Бронирование подтверждено!</b>',
                  '',
                  `🗺 ${tour}`,
                  `👤 ${name}`,
                  `📱 ${phone}`,
                  `📅 ${date || 'уточним'}`,
                  `👥 ${guests} чел.`,
                  '',
                  'Тимур свяжется с вами в ближайшее время!',
                  'Обычно отвечает за 15 минут.'
                ].join('\n'),
            parse_mode: 'HTML',
            reply_markup: {
              inline_keyboard: [
                [{
                  text: bEn ? '📱 WhatsApp Timur' : '📱 Написать в WhatsApp',
                  url: 'https://wa.me/995511272623?text=' +
                    encodeURIComponent(bEn
                      ? `Booking: ${tour}, ${name}, ${date || 'date?'}, ${guests} ppl`
                      : `Бронь: ${tour}, ${name}, ${date || 'дата?'}, ${guests} чел`)
                }],
                [
                  { text: '⭐ Google', url: 'https://g.page/r/CaUzuaJELU4aEB0/review' },
                  {
                    text: '🔗',
                    url: 'https://t.me/share/url?url=https://t.me/SakhvaGuideBot&text=' +
                      encodeURIComponent(bEn ? 'Great guide in Tbilisi! 🇬🇪' : 'Классный гид в Тбилиси! 🇬🇪')
                  }
                ],
                [{ text: bEn ? '🗺 All tours' : '🗺 Все туры', callback_data: `${bLang}.menu` }]
              ]
            }
          })

          // Notify Timur
          if (NOTIFY) {
            await tg(MGR, 'sendMessage', {
              chat_id: NOTIFY,
              text: [
                '🗓 <b>Новая бронь из Telegram!</b>',
                '',
                `🗺 ${tour}`,
                `👤 ${name}`,
                `📱 ${phone}`,
                `📅 ${date || '—'}`,
                `👥 ${guests} чел.`,
                `💬 @${uname || '—'}`,
                `🌐 ${bEn ? 'EN' : 'RU'}`,
                saved ? '✅ Airtable OK' : '⚠️ Airtable ошибка'
              ].join('\n'),
              parse_mode: 'HTML'
            })
          }
          return new Response('OK')
        }

        // Legacy: single-message booking
        if (step.step === 'LEGACY') {
          const phone = txt.match(/\+?\d[\d\s\-()]{5,}/)
          const date = parseDate(txt)
          const guestsM = txt.match(/(\d+)\s*(?:чел|человек|people|pax)/i)
          const parts = txt.split(/[,\n]/).map(s => s.trim())
          const name = parts[0]?.replace(/\+?\d[\d\s\-()]{5,}/, '').trim() || fname

          const booking = {
            name, phone: phone ? phone[0] : '',
            date, guests: guestsM ? guestsM[1] : '1',
            tour: step.tour, username: uname
          }
          const saved = await saveToAirtable(booking)

          await tg(BOT, 'sendMessage', {
            chat_id: cid,
            text: [
              '✅ <b>Бронирование принято!</b>',
              '',
              `🗺 ${booking.tour}`,
              `👤 ${booking.name}`,
              `📱 ${booking.phone || 'не указан'}`,
              `📅 ${booking.date || 'уточним'}`,
              `👥 ${booking.guests} чел.`,
              '',
              'Тимур свяжется с вами!'
            ].join('\n'),
            parse_mode: 'HTML',
            reply_markup: {
              inline_keyboard: [
                [{ text: '🗺 Все туры', callback_data: 'r.menu' }]
              ]
            }
          })

          if (NOTIFY) {
            await tg(MGR, 'sendMessage', {
              chat_id: NOTIFY,
              text: `🗓 Бронь: ${booking.tour}\n👤 ${booking.name}\n📱 ${booking.phone || '—'}\n📅 ${booking.date || '—'}\n👥 ${booking.guests} чел.\n💬 @${uname || '—'}`,
              parse_mode: 'HTML'
            })
          }
          return new Response('OK')
        }
      }
    }

    // --- Smart matching ---
    const lower = txt.toLowerCase()
    // Detect lang from text for free-form messages
    const msgLang = detectLang(txt)

    // Tour keyword match
    const tourKey = findTourByKeyword(lower)
    if (tourKey) {
      const t = TOURS[tourKey]
      const mEn = msgLang === 'e'
      await tg(BOT, 'sendPhoto', {
        chat_id: cid,
        photo: t.img,
        caption: `${t.emoji} <b>${tourName(t, msgLang)}</b> — ${mEn ? 'from ' : 'от '}${tourPrice(t, msgLang)}/${mEn ? 'person' : 'чел'}\n\n${tourDesc(t, msgLang)}\n\n⏱ ${tourDur(t, msgLang)}`,
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [{ text: mEn ? '📅 Book now' : '📅 Забронировать', callback_data: `${msgLang}.book:${tourKey}` }],
            [
              { text: mEn ? '🌐 Website' : '🌐 На сайте', url: `https://${tourUrl(t, msgLang)}` },
              {
                text: '📱 WhatsApp',
                url: 'https://wa.me/995511272623?text=' +
                  encodeURIComponent(mEn ? `I want: ${t.nameEn}` : `Хочу: ${t.name}`)
              }
            ],
            [{ text: mEn ? '⬅️ All tours' : '⬅️ Все туры', callback_data: `${msgLang}.menu` }]
          ]
        }
      })
      return new Response('OK')
    }

    // Conversational
    const conv = matchConversation(lower, fname, msgLang)
    if (conv) {
      await tg(BOT, 'sendMessage', {
        chat_id: cid,
        text: conv.text,
        parse_mode: 'HTML',
        reply_markup: conv.markup || tourGrid(msgLang)
      })
      return new Response('OK')
    }

    // Default — friendly + menu
    const dEn = msgLang === 'e'
    await tg(BOT, 'sendMessage', {
      chat_id: cid,
      text: dEn
        ? [
            `${fname ? fname + ', I' : 'I'} didn't quite get that, but Timur can help!`,
            '',
            'Try:',
            '• Pick a tour from the catalog 👇',
            '• Ask about weather, prices, visa',
            '• Message on WhatsApp directly'
          ].join('\n')
        : [
            `${fname ? fname + ', я' : 'Я'} пока не понял вопрос, но Тимур точно поможет!`,
            '',
            'Попробуйте:',
            '• Выбрать тур из каталога 👇',
            '• Спросить про погоду, цены, визу',
            '• Написать в WhatsApp напрямую'
          ].join('\n'),
      reply_markup: tourGrid(msgLang)
    })
    return new Response('OK')
  }

  return new Response('OK')
}
