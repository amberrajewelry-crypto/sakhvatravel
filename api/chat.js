// Sakhva AI Chat v2 — GPT-4o-mini with function calling
// Tools: search_tours, get_tour_details, create_booking_draft,
//        get_cross_sell, escalate_to_timur
// Logs conversations to Airtable via /api/chat-log/

export const config = { runtime: 'edge' }

const SYSTEM_PROMPT = `Ты — AI-помощник Тимура, частного гида в Тбилиси. Сегодня ${new Date().toLocaleDateString('ru-RU', {weekday:'long', day:'numeric', month:'long', year:'numeric'})}. Даты в ответах — только текущий год или позже.

══════════════════════════════════════════
РАЗДЕЛ 1: СТИЛЬ ТИМУРА
══════════════════════════════════════════

Тимур — местный частный гид, НЕ агентство. Говори от его имени в первом лице: «я покажу», «свожу», «я знаю место».
Ответы КОРОТКИЕ: 2-4 предложения максимум. Конкретные цифры всегда.
Используй местные слова: марани, квеври, хинкали, Сигнахи, Гергети, чурчхела, лобио.

ЗАПРЕЩЁННЫЕ ФРАЗЫ — НИКОГДА не используй:
«отличный выбор», «удивительный», «насладиться», «незабываемые впечатления», «замечательный», «потрясающий», «идеальный способ», «уникальный опыт», «обязательно посетите», «откройте для себя», «великолепный», «чудесный», «волшебный», «изумительный».

ПРИМЕРЫ ФРАЗ ТИМУРА (имитируй этот стиль):
- «Для первого раза берите Казбеги + Старый Тбилиси — горы и город за 2 дня.»
- «Кахетия — это вино, виноградники и обед у хозяйки. 170 лари с человека, 11 часов.»
- «С детьми — Казбеги: у них горы, у вас вид. Без серпантинов, подъём на джипе.»
- «Группа 6+ — скидка 10%. Корпоратив — напишите, подберу программу.»
- «Мцхета — 4 часа, 77 лари. Если в Тбилиси на 1 день — только это и успеете.»

══════════════════════════════════════════
РАЗДЕЛ 2: КОГДА ВЫЗЫВАТЬ TOOLS (КРИТИЧНО)
══════════════════════════════════════════

▶ search_tours — ВЫЗЫВАЙ ОБЯЗАТЕЛЬНО когда:
- Клиент упомянул ЛЮБОЙ конкретный интерес: винодельня, Гори, фотограф, корпоратив, горы, еда, ночной, дети
- В сообщении есть хотя бы 2 из 3: кто едет / сколько дней / что хочет
- Клиент явно просит подбор: «что посмотреть», «какие туры есть», «посоветуй»
- Клиент назвал бюджет или длительность

ТЕКСТОМ отвечай ТОЛЬКО когда:
- Нужен уточняющий вопрос (не понятно что ищет)
- Общий вопрос не про туры (виза, погода, оплата)
- Приветствие без конкретного запроса

НИКОГДА не описывай туры текстом если можешь вернуть карточку через search_tours. Карточки — всегда приоритет.

▶ create_booking_draft — ВЫЗЫВАЙ когда клиент назвал в одном сообщении:
- Какой тур (название или описание) + дату (точную или относительную) + количество людей
- Относительные даты: «суббота» → ближайшая суббота, «выходные» → ближайшая суббота, «на неделе» → ближайшая среда

▶ get_cross_sell — ВЫЗЫВАЙ после search_tours по правилам:
- Винный тур → страховка
- Многодневный тур → трансфер + страховка
- Тур из Тбилиси к достопримечательностям → трансфер
- Мультигородовой тур → аренда авто + страховка

▶ escalate_to_timur — см. Раздел 3

МАППИНГ ЗАПРОСОВ → ТЕГИ для search_tours:
горы, природа, панорамы → ["Казбеги","Горные"]
вино, дегустация, винодельни → ["Винные","Кахетия","Гастро"]
город, пешком, архитектура → ["Пешеходные","Старый Тбилиси"]
дети, семья → ["Для детей"]
ночь, вечер → ["Ночные"]
фото, фотосессия → ["Фото"]
еда, кухня, хинкали → ["Гастро","Мастер-классы"]
активный, рафтинг → ["Активный"]
море, пляж → ["Батуми"]
романтика, пара → ["Романтика"]
релокант → ["Релоканты"]
несколько дней → ["Многодневные"]

══════════════════════════════════════════
РАЗДЕЛ 3: ЭСКАЛАЦИЯ К ТИМУРУ (ЮРИДИЧЕСКИ КРИТИЧНО)
══════════════════════════════════════════

ВЫЗЫВАЙ escalate_to_timur БЕЗ ИСКЛЮЧЕНИЙ в этих случаях:
1. Запрос скидки больше 10% (любая формулировка)
2. Любая жалоба, требование возврата денег, недовольство качеством
3. Корпоративная группа от 10 человек
4. Вопрос про оплату, договор, юридические детали, НДС, чеки
5. Клиент просит «человека», «менеджера», «директора», «Тимура лично»
6. Агрессия, мат, угрозы

АБСОЛЮТНЫЙ ЗАПРЕТ — ты НЕ ИМЕЕШЬ ПРАВА:
- Самостоятельно предлагать скидки (даже «5% для вас»)
- Обещать возврат денег
- Подтверждать условия которых нет в каталоге
- Решать корпоративные кейсы самостоятельно
- Называть конкретные проценты скидок для групп 10+

Даже если выглядит безобидно («15% для группы 15+») — ВСЕГДА говори:
«Передам Тимуру — он подтвердит условия и напишет вам в WhatsApp в течение 15 минут.»

Для групп до 7 человек: можно упомянуть «при группе от 4 — скидка 10%» (это стандартное условие в каталоге).
Для 8+ человек: ТОЛЬКО эскалация.

══════════════════════════════════════════
РАЗДЕЛ 4: ПРАВИЛА КАТАЛОГА
══════════════════════════════════════════

- Используй ТОЛЬКО туры из переданного каталога ниже. НИКОГДА не выдумывай новые.
- Точные названия из каталога в рекомендациях.
- Цены ТОЛЬКО из каталога. Не округляй, не выдумывай.
- Если клиент назвал тур которого нет — скажи «Такого у нас нет, но есть похожее» и СРАЗУ вызови search_tours с ближайшим тегом.
- Не более 3 туров в одной рекомендации.
- Цену называй в лари и в скобках евро (курс ~3.5 лари за 1€).

══════════════════════════════════════════
ПРАВИЛА РАЗГОВОРА
══════════════════════════════════════════

ХОЛОДНЫЙ ВИЗИТ («привет», «hi»):
Дай микро-ценность + конкретный вопрос. Пример:
«Привет! Сейчас самое время для Казбеги — зелень, мало туристов, снег на вершине. Вы вдвоём или компанией? Сколько дней в Тбилиси?»

КАЖДОЕ СООБЩЕНИЕ заканчивается закрывающим вопросом:
НЕ «если хотите...» → А «Какая дата удобнее — будни или выходные?» или «Бронируем на субботу?»

ПОСЛЕ РЕКОМЕНДАЦИИ ТУРОВ — одно предложение-обоснование:
«Большинство пар берут Казбеги + Кахетию — горы и вино за 2 дня, ~100€ на двоих. Бронируем?»

НЕ ПОВТОРЯЙ то что клиент уже знает. Если показал карточку — не описывай маршрут текстом.

НЕТОЧНЫЕ ДАТЫ: не переспрашивай. «Суббота» → вычисли ближайшую и предложи.

SOCIAL PROOF (используй естественно): «500+ туров с 2023 года», «рейтинг 4.9/5 из 87 отзывов», «большинство выбирают Казбеги первым туром».

═══ PLAYBOOK ВОЗРАЖЕНИЙ ═══

ЦЕНА: «На Tripster Казбеги — 90-120€ автобус 15 человек. У нас — от 50€, минивэн 4-7 человек, всё включено.»
ОБМАН: «4.9 из 5, 87 отзывов Google Maps: maps.app.goo.gl/sakhva. ИП с грузинской регистрацией, 500+ групп.»
ПРЕДОПЛАТА: «10% — обычно 5-7€. Остальное гиду в день тура. Отмена за 24ч — полный возврат.»
ОПЛАТА: «Visa, Mastercard, крипто, наличные (лари/евро/доллары). МИР не работает в Грузии.»
БЕЗОПАСНОСТЬ: «Грузия — топ-10 безопасных стран (Global Peace Index). 500+ групп, ни одного инцидента.»
ВИЗА: «Безвизовый вход 365 дней для РФ, Украины, Беларуси, Казахстана. Нужен только загранпаспорт.»
ДЕТИ: «Семейные маршруты, автокресло предоставим. До 5 лет бесплатно.»
БОЛЬШАЯ ГРУППА 8-9: «Организуем второй транспорт. Для 10+ — передам Тимуру для расчёта.»
КОНКУРЕНТЫ: «Агрегаторы — автобус 15-30 человек. У Тимура — минивэн, гибкий маршрут, домашний обед.»
АРЕНДА АВТО: «Серпантины, специфические правила. С гидом — расслабляетесь и дегустируете.»
ДУМАЕМ: «Без давления. Зарезервирую дату на 24 часа без обязательств?»
ENGLISH: Switch to English. «No problem! Timur speaks fluent English. Mountains, wine country, or city walks?»

Контакты: WhatsApp +995 511 272 623, Telegram @SakhvaGuideBot
Сайт: sakhva-travel.com`

const TOOLS = [
  {
    type: 'function',
    function: {
      name: 'search_tours',
      description: 'Search tours by criteria. ALWAYS use multiple tags for broader results. Example: for "mountains" use tags ["Казбеги","Горные"], for "wine" use ["Винные","Кахетия","Гастро"].',
      parameters: {
        type: 'object',
        properties: {
          tags: {
            type: 'array',
            items: { type: 'string' },
            description: 'Tour tags: Казбеги, Кахетия, Гастро, Винные, Пешеходные, Старый Тбилиси, За городом, Многодневные, Активный, Батуми, Для детей, Фото, Романтика, Горные, Мастер-классы, Ночные, Релоканты, Сезонные'
          },
          max_price_gel: { type: 'number', description: 'Max price per person in GEL' },
          max_hours: { type: 'number', description: 'Max duration in hours' },
          min_hours: { type: 'number', description: 'Min duration in hours' },
          format: { type: 'string', enum: ['group', 'individual'] },
          query: { type: 'string', description: 'Free text search in title/description' }
        }
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'get_tour_details',
      description: 'Get full details of a specific tour by slug',
      parameters: {
        type: 'object',
        properties: {
          slug: { type: 'string', description: 'Tour slug from catalog' }
        },
        required: ['slug']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'create_booking_draft',
      description: 'Create a booking draft. Call this as soon as you have: tour slug + guest count + name. Date is optional — use the nearest matching date for relative dates ("суббота"→nearest Saturday, "выходные"→nearest Saturday). Do NOT ask for exact date if client gave a relative one.',
      parameters: {
        type: 'object',
        properties: {
          tour_slug: { type: 'string', description: 'Tour slug from catalog' },
          date: { type: 'string', description: 'Date as YYYY-MM-DD. Convert relative dates: "суббота"→nearest Saturday, "воскресенье"→nearest Sunday, "выходные"→nearest Saturday, "на неделе"→nearest Wednesday. If no date given, leave empty.' },
          guests: { type: 'number', description: 'Number of guests (1-7)' },
          client_name: { type: 'string', description: 'Client name' },
          client_email: { type: 'string', description: 'Client email (optional)' },
          client_phone: { type: 'string', description: 'Client phone (optional)' }
        },
        required: ['tour_slug', 'guests', 'client_name']
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'get_cross_sell',
      description: 'Get cross-sell partner offers after a booking is confirmed. Call this after create_booking_draft succeeds.',
      parameters: {
        type: 'object',
        properties: {
          tour_type: { type: 'string', description: 'Type of tour booked: day_trip, multi_day, city_walk, transfer' }
        }
      }
    }
  },
  {
    type: 'function',
    function: {
      name: 'escalate_to_timur',
      description: 'Escalate to human guide Timur via Telegram. Use when client asks for human or AI is not confident.',
      parameters: {
        type: 'object',
        properties: {
          reason: { type: 'string', description: 'Why: client_request, complex_query, booking_issue' },
          client_name: { type: 'string' },
          client_contact: { type: 'string' },
          summary: { type: 'string', description: 'Brief summary for Timur' }
        },
        required: ['reason', 'summary']
      }
    }
  }
]

// Catalog cache
let catalogCache = null
async function getCatalog(origin) {
  if (catalogCache) return catalogCache
  try {
    const resp = await fetch(`${origin}/data/catalog.json`)
    const data = await resp.json()
    catalogCache = data.excursions || []
  } catch {
    catalogCache = []
  }
  return catalogCache
}

function searchTours(tours, params) {
  let results = [...tours]

  if (params.tags?.length) {
    results = results.filter(t =>
      params.tags.some(tag =>
        t.tags.some(tt => tt.toLowerCase().includes(tag.toLowerCase()))
      )
    )
  }
  if (params.max_price_gel) {
    results = results.filter(t => t.price <= params.max_price_gel)
  }
  if (params.max_hours) {
    results = results.filter(t => t.hours <= params.max_hours)
  }
  if (params.min_hours) {
    results = results.filter(t => t.hours >= params.min_hours)
  }
  if (params.format) {
    results = results.filter(t => t.format === params.format)
  }
  if (params.query) {
    const q = params.query.toLowerCase()
    results = results.filter(t =>
      t.title.toLowerCase().includes(q) ||
      t.description.toLowerCase().includes(q)
    )
  }

  if (params.tags?.length) {
    results.sort((a, b) => {
      const aMatch = params.tags.filter(tag =>
        a.tags.some(tt => tt.toLowerCase().includes(tag.toLowerCase()))
      ).length
      const bMatch = params.tags.filter(tag =>
        b.tags.some(tt => tt.toLowerCase().includes(tag.toLowerCase()))
      ).length
      return bMatch - aMatch
    })
  }

  return results.slice(0, 5).map(t => ({
    slug: t.slug,
    title: t.title,
    description: t.description,
    price: t.price,
    currency: t.currency,
    price_eur: Math.round(t.price / 3.5),
    hours: t.hours,
    days: t.days,
    durationText: t.durationText,
    image: t.image,
    format: t.format,
    tags: t.tags,
    url: t.url,
    discount: t.discount || 0
  }))
}

function createBookingDraft(tours, params) {
  // Exact match first, then fuzzy (slug contains or title contains)
  let tour = tours.find(t => t.slug === params.tour_slug)
  if (!tour) {
    const q = (params.tour_slug || '').toLowerCase()
    tour = tours.find(t => t.slug.includes(q) || q.includes(t.slug))
    if (!tour) {
      tour = tours.find(t => t.title.toLowerCase().includes(q) || q.split('-').some(w => w.length > 3 && t.title.toLowerCase().includes(w)))
    }
  }
  if (!tour) return { error: 'Tour not found', suggestion: 'Use get_tour_details or search_tours to find the correct slug first' }

  const guests = Math.min(Math.max(params.guests || 1, 1), 7)
  const totalGel = tour.price * guests
  const discount = guests >= 4 && tour.discount ? tour.discount : 0
  const totalWithDiscount = discount
    ? Math.round(totalGel * (1 - discount / 100))
    : totalGel
  const prepay = Math.round(totalWithDiscount * 0.1)

  return {
    success: true,
    tour_slug: tour.slug,
    tour_name: tour.title,
    tour_url: tour.url,
    tour_image: tour.image,
    date: params.date || 'уточнить',
    guests,
    client_name: params.client_name,
    client_email: params.client_email || '',
    client_phone: params.client_phone || '',
    price_per_person: tour.price,
    total: totalWithDiscount,
    discount_percent: discount,
    prepay,
    currency: 'GEL',
    total_eur: Math.round(totalWithDiscount / 3.5),
    prepay_eur: Math.round(prepay / 3.5),
    booking_url: `${tour.url}#booking`
  }
}

function getCrossSell(params) {
  const offers = [
    {
      type: 'insurance',
      title: 'Страховка для Грузии',
      description: 'Медицинская страховка от 8€ за неделю. Покрывает отмену рейса, задержку багажа.',
      price: 'от 8€',
      url: 'https://cherehapa.ru/?partner_id=12946',
      icon: 'shield'
    },
    {
      type: 'transfer',
      title: 'Трансфер из аэропорта',
      description: 'Водитель с табличкой, фиксированная цена, без сюрпризов.',
      price: 'от 25€',
      url: 'https://kiwitaxi.tpx.lu/ks5vMJWm',
      icon: 'car'
    },
    {
      type: 'car_rental',
      title: 'Аренда авто по Грузии',
      description: 'Без залога, доставка в аэропорт, полная страховка включена.',
      price: 'от 30€/день',
      url: 'https://localrent.tpx.lu/eBsVy3dO',
      icon: 'key'
    }
  ]

  // Filter by relevance
  if (params?.tour_type === 'transfer') {
    return offers.filter(o => o.type !== 'transfer')
  }
  if (params?.tour_type === 'multi_day') {
    return offers
  }
  // Day trip: insurance + transfer most relevant
  return offers.filter(o => o.type !== 'car_rental')
}

async function sendTelegramEscalation(params, history) {
  const botToken = process.env.TELEGRAM_BOT_TOKEN
  const chatId = process.env.TELEGRAM_CHAT_ID
  if (!botToken || !chatId) return false

  const historyText = history
    .slice(-6)
    .map(m => `${m.role === 'user' ? 'Клиент' : 'AI'}: ${m.content}`)
    .join('\n')

  const text = [
    '🔔 Эскалация из Sakhva-AI чата',
    '',
    `Причина: ${params.reason}`,
    params.client_name ? `Имя: ${params.client_name}` : '',
    params.client_contact ? `Контакт: ${params.client_contact}` : '',
    '',
    `Резюме: ${params.summary}`,
    '',
    'Последние сообщения:',
    historyText
  ].filter(Boolean).join('\n')

  try {
    await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text, parse_mode: 'HTML' })
    })
    return true
  } catch {
    return false
  }
}

// Fire-and-forget log to Airtable
async function logToAirtable(origin, data) {
  try {
    await fetch(`${origin}/api/chat-log/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  } catch { /* silent */ }
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  // Only serve requests coming from our own site (limits OpenAI cost abuse).
  const ALLOWED_ORIGIN = 'https://sakhva-travel.com'
  const _o = req.headers.get('origin') || ''
  const _r = req.headers.get('referer') || ''
  if (_o !== ALLOWED_ORIGIN && !_r.startsWith(ALLOWED_ORIGIN + '/') && _r !== ALLOWED_ORIGIN) {
    return new Response(JSON.stringify({ error: 'Forbidden' }), {
      status: 403, headers: { 'Content-Type': 'application/json' }
    })
  }

  const KEY = process.env.OPENAI_API_KEY
  if (!KEY) {
    return new Response(JSON.stringify({
      reply: 'Я сейчас не на связи. Напишите Тимуру: +995 511 272 623',
      error: 'no_key'
    }), { status: 200, headers: { 'Content-Type': 'application/json' } })
  }

  let body
  try {
    body = await req.json()
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  const { message, history = [], sessionId, page, lang } = body
  if (!message) {
    return new Response(JSON.stringify({ error: 'No message' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  const isKA = lang === 'ka' || (page && page.startsWith('/ge/'))
  const isEN = !isKA && (lang === 'en' || (page && page.startsWith('/en/')))
  const origin = new URL(req.url).origin
  const tours = await getCatalog(origin)

  const langNote = isKA
    ? '\n\nIMPORTANT: The client is on the Georgian (ქართული) version of the site. Reply in Georgian. Use the same tools and rules but respond in Georgian.'
    : isEN
    ? '\n\nIMPORTANT: The client is on the English version of the site. Reply in English. Use the same tools and rules but respond in English.'
    : ''

  const messages = [
    { role: 'system', content: SYSTEM_PROMPT + langNote },
    ...history.slice(-10).map(m => ({
      role: m.role,
      content: m.content
    })),
    { role: 'user', content: message }
  ]

  try {
    let resp = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        max_tokens: 600,
        tools: TOOLS,
        tool_choice: 'auto',
        messages
      })
    })

    let data = await resp.json()
    let choice = data?.choices?.[0]

    // Handle tool calls
    if (choice?.finish_reason === 'tool_calls' || choice?.message?.tool_calls) {
      const toolCalls = choice.message.tool_calls || []
      const toolMessages = [choice.message]
      let bookingDraft = null
      let crossSellOffers = null

      for (const tc of toolCalls) {
        const args = JSON.parse(tc.function.arguments || '{}')
        let result

        if (tc.function.name === 'search_tours') {
          result = searchTours(tours, args)
        } else if (tc.function.name === 'get_tour_details') {
          const tour = tours.find(t => t.slug === args.slug)
          result = tour || { error: 'Tour not found' }
        } else if (tc.function.name === 'create_booking_draft') {
          result = createBookingDraft(tours, args)
          if (result.success) bookingDraft = result
        } else if (tc.function.name === 'get_cross_sell') {
          result = getCrossSell(args)
          crossSellOffers = result
        } else if (tc.function.name === 'escalate_to_timur') {
          const sent = await sendTelegramEscalation(args, history)
          result = {
            escalated: sent,
            message: sent
              ? 'Уведомление отправлено Тимуру'
              : 'Не удалось отправить, предложи контакт напрямую'
          }
        }

        toolMessages.push({
          role: 'tool',
          tool_call_id: tc.id,
          content: JSON.stringify(result)
        })
      }

      // Second call with tool results
      resp = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${KEY}`
        },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          max_tokens: 600,
          messages: [...messages, ...toolMessages]
        })
      })

      data = await resp.json()
      choice = data?.choices?.[0]

      const tourCards = toolCalls
        .filter(tc => tc.function.name === 'search_tours')
        .flatMap(tc => {
          const args = JSON.parse(tc.function.arguments || '{}')
          return searchTours(tours, args).slice(0, 3)
        })

      const reply = choice?.message?.content || ''
      const responseData = { reply }
      if (tourCards.length) responseData.tours = tourCards
      if (bookingDraft) responseData.booking = bookingDraft
      if (crossSellOffers) responseData.crossSell = crossSellOffers
      if (toolCalls.some(tc => tc.function.name === 'escalate_to_timur')) {
        responseData.escalated = true
      }

      // Log async
      logToAirtable(origin, {
        sessionId,
        page,
        messages: [...history, { role: 'user', content: message }, { role: 'assistant', content: reply }],
        toursRecommended: tourCards.map(t => t.slug).join(','),
        booked: !!bookingDraft,
        escalated: responseData.escalated || false
      })

      return new Response(JSON.stringify(responseData), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // No tool calls
    const reply = choice?.message?.content || ''

    logToAirtable(origin, {
      sessionId,
      page,
      messages: [...history, { role: 'user', content: message }, { role: 'assistant', content: reply }]
    })

    return new Response(JSON.stringify({ reply }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (e) {
    return new Response(JSON.stringify({
      reply: 'Кажется я сейчас не на связи. Напишите Тимуру напрямую в WhatsApp: +995 511 272 623',
      error: 'api_error'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}
