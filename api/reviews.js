// Static reviews endpoint — returns verified Google reviews
// TODO: connect to Google Places API when API key is available

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
    text: 'Amazing tour, thank you so much! Timur showed us places we would never have found on our own.'
  },
  {
    name: 'Giorgi V.',
    avatar: null,
    time: 'April 2026',
    rating: 5,
    text: 'Excellent guide. Showed and told us everything about sunny Georgia. Speaks perfect English.'
  },
  {
    name: 'Nugo S.',
    avatar: null,
    time: 'April 2026',
    rating: 5,
    text: 'Highly recommend if you want the best recommendations and service for travelling around Georgia.'
  }
]

export default function handler(req) {
  const referer = req.headers.get('referer') || ''
  const langParam = new URL(req.url).searchParams.get('lang') || ''
  const isEn = langParam === 'en' || referer.includes('/en/')
  const reviews = isEn ? REVIEWS_EN : REVIEWS_RU

  return new Response(JSON.stringify({
    rating: 4.9,
    total: 87,
    reviews
  }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
      'Access-Control-Allow-Origin': '*'
    }
  })
}
