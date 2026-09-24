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

    // Consolidate raw referrers into friendly source buckets (all variants → one name)
    const classify = (raw) => {
      const r = String(raw || '').toLowerCase();
      if (!r || r === 'direct' || r === 'прямой') return 'Прямой / приложение';
      if (/t\.me|telegram|\btg\b/.test(r)) return 'Telegram';
      if (/wa\.me|whatsapp/.test(r)) return 'WhatsApp';
      if (/instagram|instagr\.am|l\.ig/.test(r)) return 'Instagram';
      if (/facebook|fb\.com|fbclid|(^|\.)fb(\.|$)|l\.facebook/.test(r)) return 'Facebook';
      if (/vk\.com|vkontakte|(^|\.)vk(\.|$)/.test(r)) return 'VK';
      if (/t\.co|twitter|(^|\.)x\.com/.test(r)) return 'X (Twitter)';
      if (/youtube|youtu\.be/.test(r)) return 'YouTube';
      if (/tiktok/.test(r)) return 'TikTok';
      if (/google/.test(r)) return 'Google';
      try { return new URL(r.startsWith('http') ? r : 'http://' + r).hostname.replace(/^www\./, ''); } catch (e) { return raw; }
    };
    const srcBucket = {};
    for (const rr of (stats.referer || [])) {
      const k = classify(rr.referer);
      srcBucket[k] = (srcBucket[k] || 0) + (rr.score || 0);
    }
    const sources = Object.entries(srcBucket).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count);

    // Exclude known pre-launch test clicks so the cabinet starts clean — without changing the
    // slug or promo code. ponytail: hardcoded per-partner offset; drop once real traffic dwarfs it.
    const BASELINES = { oleg: { total: 6, day: '2026-08-11', dayClicks: 4 } };
    let totalC = stats.totalClicks || stats.humanClicks || 0;
    let todayC = todayStats.humanClicks || todayStats.totalClicks || 0;
    let monthC = stats.humanClicks || stats.totalClicks || 0;
    const bl = BASELINES[String(slug).toLowerCase()];
    if (bl) {
      totalC = Math.max(0, totalC - bl.total);
      monthC = Math.max(0, monthC - bl.total);
      const todayStr = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Tbilisi' });
      if (todayStr === bl.day) todayC = Math.max(0, todayC - bl.dayClicks);
      timeline = timeline.map(p => p.date === bl.day ? { ...p, clicks: Math.max(0, (p.clicks || 0) - bl.total) } : p);
    }

    return res.status(200).json({
      partner: link.title || slug,
      slug: link.path,
      sources,
      totalClicks: totalC,
      created: link.createdAt,
      today: todayC,
      last30days: monthC,
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
