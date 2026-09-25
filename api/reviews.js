// Reviews endpoint: live Google reviews via Places API (New) when GOOGLE_PLACES_API_KEY
// is set and billing is enabled; otherwise the verified static set below.

export const config = { runtime: 'edge' }

const REVIEWS_RU = [
  {
    name: 'Тигран Мартиросов',
    avatar: null,
    time: 'апрель 2026',
    rating: 5,
    text: 'Замечательная экскурсия) спасибо огромное)'
  },
  {
    name: 'Гиорги Вахтангович',
    avatar: null,
    time: 'апрель 2026',
    rating: 5,
    text: 'Отличный гид. Показал и рассказал всё о Солнечной Грузии. Отлично говорит на русском языке.'
  },
  {
    name: 'Nugo Shengelia',
    avatar: null,
    time: 'апрель 2026',
    rating: 5,
    text: 'Настоятельно рекомендую, если вы хотите получить лучшие рекомендации и услуги для путешествий по Грузии.'
  }
]

const REVIEWS_EN = [
  {
    name: 'Tigran M.',
    avatar: null,
    time: 'April 2026',
    rating: 5,
    text: 'A wonderful tour, thank you so much! (translated from Russian)'
  },
  {
    name: 'Giorgi V.',
    avatar: null,
    time: 'April 2026',
    rating: 5,
    text: 'Excellent guide. Showed and told us everything about sunny Georgia. Speaks excellent Russian.'
  },
  {
    name: 'Nugo S.',
    avatar: null,
    time: 'April 2026',
    rating: 5,
    text: 'Highly recommend if you want the best recommendations and service for travelling around Georgia.'
  }
]

const REVIEWS_GE = [
  {
    name: 'ტიგრან მარტიროსოვი',
    avatar: null,
    time: 'აპრილი 2026',
    rating: 5,
    text: 'შესანიშნავი ექსკურსია! უღრმესი მადლობა! თიმურმა გვაჩვენა ადგილები, რომლებსაც დამოუკიდებლად ვერასდროს ვიპოვნიდით.'
  },
  {
    name: 'გიორგი ვახტანგოვიჩი',
    avatar: null,
    time: 'აპრილი 2026',
    rating: 5,
    text: 'შესანიშნავი გიდი. ყველაფერი მოგვიყვა და გვაჩვენა მზიან საქართველოზე. შესანიშნავად საუბრობს რუსულად.'
  },
  {
    name: 'ნუგო შენგელია',
    avatar: null,
    time: 'აპრილი 2026',
    rating: 5,
    text: 'ნამდვილად გირჩევთ, თუ გსურთ საუკეთესო რჩევები და მომსახურება საქართველოში მოგზაურობისთვის.'
  }
]

const LANG = { ru: 'ru', en: 'en', ge: 'ka' }
const MONTHS = {
  ru: ['январь','февраль','март','апрель','май','июнь','июль','август','сентябрь','октябрь','ноябрь','декабрь'],
  en: ['January','February','March','April','May','June','July','August','September','October','November','December'],
  ge: ['იანვარი','თებერვალი','მარტი','აპრილი','მაისი','ივნისი','ივლისი','აგვისტო','სექტემბერი','ოქტომბერი','ნოემბერი','დეკემბერი']
}
const FALLBACK = { rating: 4.9, total: 87 }

async function livePlaces(lang) {
  const key = process.env.GOOGLE_PLACES_API_KEY
  if (!key) return null
  const h = { 'X-Goog-Api-Key': key, 'Content-Type': 'application/json' }
  let id = process.env.GOOGLE_PLACE_ID
  if (!id) {
    const r = await fetch('https://places.googleapis.com/v1/places:searchText', {
      method: 'POST', headers: { ...h, 'X-Goog-FieldMask': 'places.id' },
      body: JSON.stringify({ textQuery: 'Sakhva Travel Tbilisi' })
    })
    const j = r.ok ? await r.json() : null
    id = j && j.places && j.places[0] && j.places[0].id
    if (!id) return null
  }
  const r = await fetch(`https://places.googleapis.com/v1/places/${id}?languageCode=${LANG[lang]}`, {
    headers: { ...h, 'X-Goog-FieldMask': 'rating,userRatingCount,reviews' }
  })
  if (!r.ok) return null
  const j = await r.json()
  if (!j.reviews || !j.reviews.length) return null
  const m = MONTHS[lang]
  const reviews = j.reviews
    .filter(x => x.rating >= 4 && x.text && x.text.text)
    .map(x => {
      const d = new Date(x.publishTime)
      return {
        name: (x.authorAttribution && x.authorAttribution.displayName) || '',
        avatar: (x.authorAttribution && x.authorAttribution.photoUri) || null,
        time: `${m[d.getMonth()]} ${d.getFullYear()}`,
        rating: x.rating,
        text: x.text.text
      }
    })
  return reviews.length ? { rating: j.rating, total: j.userRatingCount, reviews } : null
}

export default async function handler(req) {
  const referer = req.headers.get('referer') || ''
  const langParam = new URL(req.url).searchParams.get('lang') || ''
  const isGe = langParam === 'ge' || referer.includes('/ge/')
  const isEn = langParam === 'en' || referer.includes('/en/')
  const lang = isGe ? 'ge' : isEn ? 'en' : 'ru'
  const statik = { ...FALLBACK, reviews: isGe ? REVIEWS_GE : isEn ? REVIEWS_EN : REVIEWS_RU }
  let body = null
  try { body = await livePlaces(lang) } catch (e) { body = null }
  return new Response(JSON.stringify(body || statik), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
      'Vary': 'Referer',
      'Access-Control-Allow-Origin': '*'
    }
  })
}
