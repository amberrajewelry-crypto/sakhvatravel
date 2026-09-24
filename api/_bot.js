// Событие сайта → бот-менеджер WhatsApp (sakhva-bot на VPS). Одна карточка в TG
// с привязкой к лиду по телефону вместо «голого» уведомления от второго бота.
// Возвращает true при 2xx; вызывающий код при false шлёт старое TG-уведомление.
export async function notifyBot(type, data) {
  const token = process.env.BOT_EVENT_TOKEN
  if (!token) return false
  const url = process.env.BOT_EVENT_URL || 'https://api.sakhva-travel.com/greenwh/site'
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Event-Token': token },
      body: JSON.stringify({ type, ...data, ts: Date.now() }),
      signal: AbortSignal.timeout(6000)
    })
    return r.ok
  } catch (e) {
    console.error('notifyBot error:', e.message)
    return false
  }
}
