// Partner stats API — proxies Short.io API, hides API key
module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://sakhva-travel.com');
  res.setHeader('Access-Control-Allow-Methods', 'GET');

  // Same-site only (blocks external enumeration of partner stats)
  const ref = req.headers.referer || req.headers.origin || '';
  if (!ref.startsWith('https://sakhva-travel.com')) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { slug } = req.query;
  if (!slug || !/^[a-z0-9-]{2,30}$/i.test(slug)) {
    return res.status(400).json({ error: 'Invalid slug' });
  }

  const API_KEY = process.env.SHORTIO_API_KEY;
  if (!API_KEY) {
    return res.status(500).json({ error: 'Not configured' });
  }
  const DOMAIN_ID = 1782098;

  try {
    // Get link by path
    const linkRes = await fetch(
      `https://api.short.io/api/links?domain_id=${DOMAIN_ID}&path=${encodeURIComponent(slug)}`,
      { headers: { Authorization: API_KEY } }
    );
    const linkData = await linkRes.json();
    const links = linkData.links || linkData;
    const link = Array.isArray(links) ? links.find(l => l.path === slug) : null;

    if (!link) {
      return res.status(404).json({ error: 'Link not found' });
    }

    // Parallel: last30 stats + today stats
    const [statsRes, todayRes] = await Promise.all([
      fetch(
        `https://statistics.short.io/statistics/link/${link.id}?period=last30&tz=Asia/Tbilisi`,
        { headers: { Authorization: API_KEY } }
      ),
      fetch(
        `https://statistics.short.io/statistics/link/${link.id}?period=today&tz=Asia/Tbilisi`,
        { headers: { Authorization: API_KEY } }
      )
    ]);

    const [stats, todayStats] = await Promise.all([
      statsRes.json(),
      todayRes.json()
    ]);

    // Parse clickStatistics chart data
    let timeline = [];
    if (stats.clickStatistics && stats.clickStatistics.datasets) {
      const ds = stats.clickStatistics.datasets[0];
      if (ds && ds.data) {
        timeline = ds.data.map(p => ({
          date: p.x.slice(0, 10),
          clicks: parseInt(p.y, 10) || 0
        }));
      }
    }

    return res.status(200).json({
      partner: link.title || slug,
      slug: link.path,
      totalClicks: stats.totalClicks || stats.humanClicks || 0,
      created: link.createdAt,
      today: todayStats.humanClicks || todayStats.totalClicks || 0,
      last30days: stats.humanClicks || stats.totalClicks || 0,
      countries: (stats.country || []).map(c => ({ name: c.countryName || c.country, count: c.score })),
      cities: (stats.city || []).map(c => ({ name: c.name || c.city, count: c.score })),
      browsers: (stats.browser || []).map(b => ({ name: b.browser, count: b.score })),
      os: (stats.os || []).map(o => ({ name: o.os, count: o.score })),
      referrers: (stats.referer || []).map(r => ({ name: r.referer || 'Прямой', count: r.score })),
      social: (stats.social || []).filter(s => s.social).map(s => ({ name: s.social, count: s.score })),
      timeline
    });
  } catch (e) {
    return res.status(500).json({ error: 'Failed to fetch stats' });
  }
};
