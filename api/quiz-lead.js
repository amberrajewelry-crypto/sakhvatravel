import { notifyBot } from './_bot.js'

export const config = { runtime: 'edge' }

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 })
  }

  try {
    const { text } = await req.json()
    if (!text) {
      return new Response(JSON.stringify({ error: 'No text' }), { status: 400 })
    }

    if (await notifyBot('quiz', { text })) {
      return new Response(JSON.stringify({ ok: true }), { status: 200 })
    }
    const token = (process.env.TELEGRAM_MANAGER_TOKEN || process.env.TELEGRAM_BOT_TOKEN)
    const chatId = (process.env.TELEGRAM_MANAGER_CHAT || process.env.TELEGRAM_CHAT_ID)

    if (!token || !chatId) {
      return new Response(JSON.stringify({ error: 'TG not configured' }), { status: 500 })
    }

    const tgRes = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'HTML'
      })
    })

    if (!tgRes.ok) {
      const err = await tgRes.text()
      console.error('TG error:', err)
      return new Response(JSON.stringify({ error: 'TG send failed' }), { status: 502 })
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (e) {
    console.error('Quiz lead error:', e)
    return new Response(JSON.stringify({ error: 'Server error' }), { status: 500 })
  }
}
