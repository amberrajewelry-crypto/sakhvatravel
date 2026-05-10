#!/usr/bin/env python3
"""Generate 13 missing OG images for blog articles."""
import requests, os, time, sys

OPENAI_API_KEY = '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'
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'blog')

PROMPTS = {
    'borzhomi': 'Borjomi mineral spring park Georgia, lush green forest, historic stone pavilion over bubbling mineral water spring, Soviet-era architecture, peaceful nature atmosphere, professional travel photography, no text, no people',
    'chastny-gid-tbilisi-cena': 'Private tour guide showing tourists Tbilisi old town, colorful carved wooden balconies, narrow cobblestone alley, warm golden light, travel lifestyle photography, no text',
    'digital-nomad-tbilisi': 'Modern coworking space in Tbilisi with view of old town rooftops and Narikala fortress through large windows, laptop on desk, specialty coffee, bright airy interior, no people, no text',
    'kakheti-za-1-den': 'Kakheti wine region Georgia, endless vineyard rows in golden autumn light, Caucasus mountains in background, Georgian winery, dramatic sky, professional travel photography, no text, no people',
    'kazbegi-iz-tbilisi-2026': 'Gergeti Trinity Church on dramatic rocky cliff, snow-capped Mount Kazbek 5047m towering behind, alpine meadows, crystal blue sky, epic Caucasus landscape, no text, no people',
    'kogda-ekhat-v-kazbegi': 'Kazbegi Georgia four seasons montage feel — spring wildflowers, summer green peaks, autumn golden slopes with church, winter snow panorama, Gergeti Trinity Church visible, professional photography, no text',
    'restorany-tbilisi': 'Georgian restaurant interior Tbilisi, traditional stone walls with wine jugs, candlelight, wooden tables with khinkali and churchkhela, warm cozy atmosphere, food photography, no text, no people',
    'skrytye-mesta-tbilisi': 'Hidden courtyard in Tbilisi old town, colorful carved wooden balconies overhanging, laundry lines, cats on steps, authentic local life, warm afternoon light, no text, no people',
    'tbilisi-dlya-relokantov': 'Tbilisi modern neighborhood panorama, mix of Soviet architecture and new cafes, expat community feel, tree-lined boulevard, colorful apartment facades, bright day, no text, no people',
    'tbilisi-fotolokatsii': 'Tbilisi iconic photography spots collage feel — Narikala fortress at sunset, colorful Abanotubani domes, Metekhi bridge, Dry Bridge market, old town balconies, golden hour light, no text, no people',
    'tbilisi-za-1-den': 'Tbilisi one day panoramic view, Narikala fortress on green hill, Kura river below, Peace Bridge, old town rooftops, Mtatsminda TV tower, golden hour light, professional travel photography, no text, no people',
    'uplistsikhe': 'Uplistsikhe ancient cave city Georgia, carved rock chambers and tunnels, dramatic Caucasus landscape, Mtkvari river in valley below, sunny day, archaeological site, no text, no people',
    'vardzia': 'Vardzia cave monastery Georgia, hundreds of carved cave rooms in volcanic cliff face, ancient frescoes visible, green Mtkvari river valley below, epic scale landscape, no text, no people',
}

def generate(slug, prompt):
    out = os.path.join(IMAGES_DIR, f'{slug}.webp')
    if os.path.exists(out):
        print(f'  ⏭  {slug} — уже есть')
        return True
    print(f'  🎨 {slug}...')
    r = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        json={'model':'dall-e-3','prompt':prompt,'n':1,'size':'1792x1024','quality':'standard','style':'natural'},
        timeout=90
    )
    if r.status_code != 200:
        print(f'  ❌ {r.status_code}: {r.text[:150]}')
        return False
    url = r.json()['data'][0]['url']
    img = requests.get(url, timeout=60).content
    with open(out, 'wb') as f:
        f.write(img)
    print(f'  ✅ {slug}.webp ({len(img)//1024} KB)')
    return True

slugs = sys.argv[1:] if len(sys.argv) > 1 else list(PROMPTS.keys())
print(f'Генерирую {len(slugs)} изображений...\n')
for i, slug in enumerate(slugs):
    if slug not in PROMPTS:
        print(f'  ❓ {slug} не в списке')
        continue
    generate(slug, PROMPTS[slug])
    if i < len(slugs) - 1:
        time.sleep(2)

print('\nГотово!')
