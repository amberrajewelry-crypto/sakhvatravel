// Bank of Georgia (BOG) — callback (webhook о статусе платежа)
// Docs: https://api.bog.ge/docs/en/payments/standard-process/callback
//
// BOG шлёт POST с телом заказа и заголовком Callback-Signature — это подпись
// СЫРОГО тела алгоритмом SHA256withRSA (base64). Проверяем её публичным ключом BOG.
// Тело: { event:"order_payment", zoned_request_time, body:{ external_order_id,
//        order_status:{ key,value }, purchase_units, ... } }
// При order_status.key === "completed" — уведомление в Telegram.
//
// Edge-runtime: req.text() даёт сырое тело (нужно для верификации подписи), WebCrypto — проверка.
// Env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

import { notifyBot } from './_bot.js'

export const config = { runtime: 'edge' }

// Публичный ключ BOG для верификации подписи callback (из офиц. документации)
const BOG_PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu4RUyAw3+CdkS3ZNILQh
zHI9Hemo+vKB9U2BSabppkKjzjjkf+0Sm76hSMiu/HFtYhqWOESryoCDJoqffY0Q
1VNt25aTxbj068QNUtnxQ7KQVLA+pG0smf+EBWlS1vBEAFbIas9d8c9b9sSEkTrr
TYQ90WIM8bGB6S/KLVoT1a7SnzabjoLc5Qf/SLDG5fu8dH8zckyeYKdRKSBJKvhx
tcBuHV4f7qsynQT+f2UYbESX/TLHwT5qFWZDHZ0YUOUIvb8n7JujVSGZO9/+ll/g
4ZIWhC1MlJgPObDwRkRd8NFOopgxMcMsDIZIoLbWKhHVq67hdbwpAq9K9WMmEhPn
PwIDAQAB
-----END PUBLIC KEY-----`

function b64ToBytes(b64) {
  const bin = atob(b64)
  const out = new Uint8Array(bin.length)
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i)
  return out
}

async function importKey(pem) {
  const der = b64ToBytes(pem.replace(/-----[^-]+-----/g, '').replace(/\s+/g, ''))
  return crypto.subtle.importKey(
    'spki',
    der,
    { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
    false,
    ['verify']
  )
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  const raw = await req.text()
  const sigHeader = req.headers.get('callback-signature') || req.headers.get('Callback-Signature')
  if (!sigHeader) {
    return new Response('No signature', { status: 400 })
  }

  // Верификация подписи
  try {
    const key = await importKey(BOG_PUBLIC_KEY_PEM)
    const ok = await crypto.subtle.verify(
      'RSASSA-PKCS1-v1_5',
      key,
      b64ToBytes(sigHeader),
      new TextEncoder().encode(raw)
    )
    if (!ok) {
      console.error('BOG callback: signature mismatch')
      return new Response('Invalid signature', { status: 400 })
    }
  } catch (e) {
    console.error('BOG callback: verify error', e.message)
    return new Response('Verify error', { status: 400 })
  }

  let payload
  try { payload = JSON.parse(raw) } catch { return new Response('Bad JSON', { status: 400 }) }

  const b = payload.body || {}
  const statusKey = b.order_status?.key || ''
  const orderId = b.external_order_id || b.order_id || '—'

  if (statusKey === 'completed') {
    const tgToken = process.env.TELEGRAM_BOT_TOKEN
    const tgChat = process.env.TELEGRAM_CHAT_ID
    const pu = b.purchase_units || {}
    const amount = pu.request_amount || pu.transfer_amount || pu.total_amount || '?'
    const currency = pu.currency_code || pu.currency || 'GEL'
    // ref — телефон клиента из ссылки бота (/oplata/?ref=995…) → orderId PAY-…-995…
    const ref = (String(orderId).match(/^PAY-\d+-(\d{9,15})$/) || [])[1] || ''  // без ref совпадал бы timestamp
    const desc = (pu.basket && pu.basket[0] && pu.basket[0].description) || ''
    const sent = await notifyBot('payment', { orderId, amount, currency, phone: ref, note: desc,
      bogOrderId: b.order_id || '' })
    if (!sent && tgToken && tgChat) {
      const msg = `💳 Оплата подтверждена (BOG)\n\n🔖 ${orderId}\n💰 ${amount} ${currency}\n🧾 order_id: ${b.order_id || '—'}`
      try {
        await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: tgChat, text: msg })
        })
      } catch (e) {
        console.error('BOG callback Telegram error:', e.message)
      }
    }
  }

  // BOG ожидает 200 OK
  return new Response('OK', { status: 200 })
}
