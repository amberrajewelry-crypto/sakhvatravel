// Records partner conversion (WA/TG click or form submit)
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://sakhva-travel.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  // Same-site only (blocks external spam of the leads table)
  const ref = req.headers.referer || req.headers.origin || '';
  if (!ref.startsWith('https://sakhva-travel.com')) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { partner, channel, page } = req.body || {};
  if (!partner || !/^[a-z0-9-]{2,30}$/i.test(partner)) {
    return res.status(400).json({ error: 'Invalid partner' });
  }

  const TOKEN = process.env.AIRTABLE_TOKEN;
  const BASE = 'appvP72OjZeVJ0XWh';
  const TABLE = 'Partner Leads';

  try {
    await fetch(`https://api.airtable.com/v0/${BASE}/${encodeURIComponent(TABLE)}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        records: [{
          fields: {
            Partner: partner,
            Channel: channel || 'unknown',
            Page: page || '/',
            Date: new Date().toISOString().slice(0, 10),
            Timestamp: new Date().toISOString()
          }
        }]
      })
    });
    return res.status(200).json({ ok: true });
  } catch (e) {
    return res.status(500).json({ error: 'Failed to save' });
  }
};
