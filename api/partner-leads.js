// Partner leads API — reads conversions from Airtable
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://sakhva-travel.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET');

  // Same-site only (blocks external enumeration of partner leads)
  const ref = req.headers.referer || req.headers.origin || '';
  if (!ref.startsWith('https://sakhva-travel.com')) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { slug } = req.query;
  if (!slug || !/^[a-z0-9-]{2,30}$/i.test(slug)) {
    return res.status(400).json({ error: 'Invalid slug' });
  }

  const TOKEN = process.env.AIRTABLE_TOKEN;
  const BASE = 'appvP72OjZeVJ0XWh';
  const TABLE = 'Partner Leads';

  if (!TOKEN) {
    return res.status(200).json({ leads: 0, events: [] });
  }

  try {
    const formula = encodeURIComponent(`{Partner}='${slug}'`);
    const url = `https://api.airtable.com/v0/${BASE}/${encodeURIComponent(TABLE)}?filterByFormula=${formula}&sort%5B0%5D%5Bfield%5D=Timestamp&sort%5B0%5D%5Bdirection%5D=desc&maxRecords=50`;

    const atRes = await fetch(url, {
      headers: { 'Authorization': `Bearer ${TOKEN}` }
    });
    const data = await atRes.json();

    if (data.records) {
      const events = data.records.map(r => ({
        channel: r.fields.Channel || 'unknown',
        page: r.fields.Page || '/',
        date: r.fields.Date || '',
        time: r.fields.Timestamp || ''
      }));

      return res.status(200).json({
        leads: events.length,
        events: events.slice(0, 20)
      });
    }

    return res.status(200).json({ leads: 0, events: [] });
  } catch (e) {
    return res.status(200).json({ leads: 0, events: [] });
  }
};
