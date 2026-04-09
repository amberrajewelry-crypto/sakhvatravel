export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { message, history = [] } = req.body || {};
  if (!message) return res.status(400).json({ error: 'No message' });

  const ANTHROPIC_KEY = process.env.ANTHROPIC_API_KEY;
  if (!ANTHROPIC_KEY) return res.status(500).json({ error: 'No API key' });

  const system = `Ты — AI-помощник Тимура, частного гида в Тбилиси (Грузия). Помогаешь туристам выбрать тур.

Туры:
• Казбеги — 1 день: от €45/чел
• Кахетия — вино и горы: от €50/чел
• Мцхета + Джвари: от €35/чел
• Старый Тбилиси: от €30/чел
• Ночной Тбилиси: от €40/чел
• Скрытые места Тбилиси: от €38/чел
• Тур для эмигрантов: от €31/чел
• Тур + ужин у местных: от €71/чел
• Советский Тбилиси: от €32/чел
• Slow Travel 3 дня: от €161/чел
• Тур + фотосессия: от €75/чел
• Digital Nomad Tour: от €31/чел

Для бронирования направляй в Telegram-бот: https://t.me/SakhvaGuideBot
Там можно выбрать тур, дату, кол-во человек и оформить бронь за 2 минуты.

Контакты: WhatsApp +995 511 272 623, Telegram @SakhvaGuideBot

Отвечай коротко (2-4 предложения), по-русски, дружелюбно. Если спрашивают о конкретном туре — называй цену и направляй в бот для брони.`;

  try {
    const messages = [
      ...history.slice(-8).map(m => ({ role: m.role, content: m.content })),
      { role: 'user', content: message }
    ];

    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 300,
        system,
        messages
      })
    });

    const data = await resp.json();
    const reply = data?.content?.[0]?.text || '';
    res.json({ reply });
  } catch (e) {
    res.status(500).json({ error: 'API error' });
  }
}
