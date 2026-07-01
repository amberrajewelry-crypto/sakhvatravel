// Flitt (ex-Fondy) — обработчик возврата клиента после оплаты (response_url).
// Flitt возвращает браузер методом POST с параметрами платежа. Статические
// страницы Vercel на POST отдают 405 → "Страница недоступна". Поэтому Flitt
// шлёт POST сюда, а мы делаем 302-redirect (GET) на success/fail страницу.

export const config = { runtime: 'edge' }

export default async function handler(req) {
  const siteUrl = process.env.SITE_URL || 'https://sakhva-travel.com'

  let data = {}
  if (req.method === 'POST') {
    const ct = req.headers.get('content-type') || ''
    try {
      if (ct.includes('application/json')) {
        const j = await req.json()
        data = j.response || j
      } else {
        const t = await req.text()
        data = Object.fromEntries(new URLSearchParams(t))
      }
    } catch { /* ignore */ }
  } else {
    data = Object.fromEntries(new URL(req.url).searchParams)
  }

  const ok = data.order_status === 'approved'
  const orderId = data.order_id || ''
  const amountGel = data.amount ? (Number(data.amount) / 100) : ''

  const dest = ok
    ? `${siteUrl}/payment-success/?order_id=${encodeURIComponent(orderId)}&amount=${amountGel}`
    : `${siteUrl}/payment-fail/?order_id=${encodeURIComponent(orderId)}`

  return new Response(null, { status: 302, headers: { Location: dest } })
}
