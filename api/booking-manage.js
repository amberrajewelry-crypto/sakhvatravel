// Самообслуживание брони с сайта: /booking-manage/?id=SK-…&t=<hmac>
// GET  → детали брони (из бота-менеджера, источник — база броней)
// POST {action:'cancel'} | {action:'reschedule', date, time}
// Подпись t = HMAC-SHA256(orderId, BOT_EVENT_TOKEN)[:32] — та же, что ставит бот в ваучер.
// Возврат при отмене ≥48 ч: BOG refund по bogOrderId (только карта; крипто/СБП — вручную).
import crypto from 'crypto'
import { notifyBot } from './_bot.js'

const BOG_AUTH_URL = 'https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token'
const BOG_REFUND_URL = 'https://api.bog.ge/payments/v1/payment/refund'

function sign(orderId) {
  return crypto.createHmac('sha256', process.env.BOT_EVENT_TOKEN || '').update(orderId).digest('hex').slice(0, 32)
}

async function bot(type, data) {
  const url = process.env.BOT_EVENT_URL || 'https://api.sakhva-travel.com/greenwh/site'
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Event-Token': process.env.BOT_EVENT_TOKEN },
    body: JSON.stringify({ type, ...data }),
    signal: AbortSignal.timeout(20000)
  })
  return r.json()
}

async function bogRefund(bogOrderId, amount) {
  const basic = Buffer.from(`${process.env.BOG_CLIENT_ID}:${process.env.BOG_CLIENT_SECRET}`).toString('base64')
  const t = await fetch(BOG_AUTH_URL, {
    method: 'POST',
    headers: { Authorization: `Basic ${basic}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'grant_type=client_credentials'
  }).then(r => r.json())
  const r = await fetch(`${BOG_REFUND_URL}/${encodeURIComponent(bogOrderId)}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${t.access_token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount })
  })
  return { ok: r.ok, status: r.status, text: (await r.text()).slice(0, 300) }
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store')
  const q = { ...(req.query || {}), ...(req.method === 'POST' ? (req.body || {}) : {}) }
  const orderId = String(q.id || q.orderId || '')
  const t = String(q.t || '')
  if (!process.env.BOT_EVENT_TOKEN) return res.status(503).json({ error: 'not_configured' })
  if (!/^SK-[\w-]{6,40}$/.test(orderId) || t.length !== 32 ||
      !crypto.timingSafeEqual(Buffer.from(t), Buffer.from(sign(orderId)))) {
    return res.status(403).json({ error: 'bad_link' })
  }
  try {
    if (req.method === 'GET') return res.status(200).json(await bot('manage_get', { orderId }))
    if (req.method !== 'POST') return res.status(405).json({ error: 'method' })
    const { action, date, time } = q
    if (action === 'reschedule') {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(String(date)) || !/^\d{2}:\d{2}$/.test(String(time))) {
        return res.status(400).json({ error: 'bad_date' })
      }
      return res.status(200).json(await bot('manage_reschedule', { orderId, date, time }))
    }
    if (action === 'cancel') {
      const out = await bot('manage_cancel', { orderId })
      if (out.ok && out.refundable && out.amount > 0) {
        // bogOrderId лежит у бота в payment-событии; он отдаёт его только на отмену
        const rf = out.bogOrderId ? await bogRefund(out.bogOrderId, out.amount) : { ok: false, text: 'no bogOrderId' }
        out.refund = rf.ok ? 'requested' : 'failed'
        await notifyBot('refund', { orderId, amount: out.amount, ok: rf.ok, note: rf.ok ? '' : `${rf.status || ''} ${rf.text}` })
      }
      return res.status(200).json(out)
    }
    return res.status(400).json({ error: 'bad_action' })
  } catch (e) {
    return res.status(502).json({ error: 'bot_unavailable', details: String(e.message).slice(0, 200) })
  }
}
