// Flitt (ex-Fondy) — server callback (webhook о статусе платежа)
// Docs: https://docs.flitt.com/api/building-signature/ (раздел verify response)
//
// Flitt шлёт POST с параметрами платежа и signature. Проверяем подпись тем же
// алгоритмом (secret + значения по алфавиту через "|", исключая signature и
// response_signature_string). При order_status=approved — уведомление в Telegram.
//
// Env vars: FLITT_PAYMENT_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

export const config = { runtime: 'edge' }

async function buildSignature(params, secret) {
  const keys = Object.keys(params)
    .filter(k => k !== 'signature' && k !== 'response_signature_string' && params[k] !== '' && params[k] != null)
    .sort()
  const base = [secret, ...keys.map(k => String(params[k]))].join('|')
  const digest = await crypto.subtle.digest('SHA-1', new TextEncoder().encode(base))
  return [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('')
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  // Flitt может прислать JSON или form-urlencoded
  let data = {}
  try {
    const ct = req.headers.get('content-type') || ''
    if (ct.includes('application/json')) {
      const j = await req.json()
      data = j.response || j
    } else {
      const text = await req.text()
      const p = new URLSearchParams(text)
      data = Object.fromEntries(p.entries())
    }
  } catch {
    return new Response('Bad request', { status: 400 })
  }

  const secret = process.env.FLITT_PAYMENT_KEY
  const received = data.signature
  if (!secret || !received) {
    return new Response('No signature', { status: 400 })
  }

  const expected = await buildSignature(data, secret)
  if (expected !== received) {
    console.error('Flitt callback: signature mismatch', { order_id: data.order_id })
    return new Response('Invalid signature', { status: 400 })
  }

  // Подпись верна. Уведомляем об успешной оплате.
  if (data.order_status === 'approved') {
    const tgToken = process.env.TELEGRAM_BOT_TOKEN
    const tgChat = process.env.TELEGRAM_CHAT_ID
    if (tgToken && tgChat) {
      const amountGel = data.amount ? (Number(data.amount) / 100).toFixed(2) : '?'
      const msg = `💳 Оплата подтверждена (Flitt)\n\n🔖 ${data.order_id || '—'}\n💰 ${amountGel} ${data.currency || 'GEL'}\n📝 ${data.order_desc || '—'}\n🧾 payment_id: ${data.payment_id || '—'}`
      try {
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text: msg })
        })
      } catch (e) {
        console.error('Flitt callback Telegram error:', e.message)
      }
    }
  }

  // Flitt ожидает 200 OK для подтверждения получения
  return new Response('OK', { status: 200 })
}
