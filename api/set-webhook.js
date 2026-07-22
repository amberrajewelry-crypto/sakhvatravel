export const config = { runtime: 'edge' }
export default async function handler(req) {
  const s = new URL(req.url).searchParams.get('secret')
  if (s !== 'fix2026') return new Response('No', { status: 403 })
  const BOT = process.env.TELEGRAM_BOT_TOKEN
  const whSecret = process.env.TELEGRAM_WEBHOOK_SECRET
  const setBody = { url: 'https://sakhva-travel.com/api/telegram-webhook/', allowed_updates: ['message','callback_query','inline_query'] }
  if (whSecret) setBody.secret_token = whSecret
  const r = await (await fetch(`https://api.telegram.org/bot${BOT}/setWebhook`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(setBody)
  })).json()
  const info = await (await fetch(`https://api.telegram.org/bot${BOT}/getWebhookInfo`)).json()
  return new Response(JSON.stringify({ set: r, webhook: info.result }, null, 2))
}
