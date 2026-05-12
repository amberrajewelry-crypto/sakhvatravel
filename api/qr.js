// QR code proxy — fetches from quickchart.io and serves as image
module.exports = async (req, res) => {
  const { url } = req.query;
  if (!url) return res.status(400).send('Missing url');

  try {
    const qrRes = await fetch('https://quickchart.io/qr?text=' + encodeURIComponent(url) + '&size=280&margin=2');
    const buf = Buffer.from(await qrRes.arrayBuffer());
    res.setHeader('Content-Type', 'image/png');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    res.status(200).send(buf);
  } catch (e) {
    res.status(500).send('QR generation failed');
  }
};
