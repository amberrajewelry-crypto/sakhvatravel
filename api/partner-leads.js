// Partner leads API — queries PostHog for conversions by partner slug
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://sakhva-travel.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET');

  const { slug } = req.query;
  if (!slug || !/^[a-z0-9-]{2,30}$/i.test(slug)) {
    return res.status(400).json({ error: 'Invalid slug' });
  }

  const PH_KEY = process.env.POSTHOG_PERSONAL_API_KEY || '';
  const PROJECT_ID = '360981';

  // If no PostHog key, return 0 (will be configured later)
  if (!PH_KEY) {
    return res.status(200).json({ leads: 0, events: [] });
  }

  try {
    // Query PostHog for cta_click and form_submit events with partner=slug
    const query = {
      query: {
        kind: 'EventsQuery',
        select: ['event', 'timestamp', 'properties.channel', 'properties.tour'],
        where: [`properties.partner = '${slug}'`],
        event: ['cta_click', 'form_submit'],
        after: '-30d',
        limit: 50,
        orderBy: ['timestamp DESC']
      }
    };

    const phRes = await fetch(
      `https://us.posthog.com/api/projects/${PROJECT_ID}/query/`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${PH_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
      }
    );

    const data = await phRes.json();

    if (data.results) {
      const events = data.results.map(r => ({
        event: r[0],
        time: r[1],
        channel: r[2] || null,
        tour: r[3] || null
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
