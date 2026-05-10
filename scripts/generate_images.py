#!/usr/bin/env python3
"""
DALL-E 3 image generator for Sakhva Travel blog articles.
Usage: python3 generate_images.py [slug]
       python3 generate_images.py all
"""

import requests, json, os, sys, time

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'blog')

# Промпты по slug — уникальные, не пересекаются с существующими фото
PROMPTS = {
    # НЕДЕЛЯ 1 (контент-план 9-15 апр)
    'tbilisi-za-2-dnya': 'Old Tbilisi streets at golden hour, cobblestone alleys, colorful balconies with carved wooden details, Metekhi Church visible in background, warm evening light, professional travel photography, no text, no people',
    'gde-ostanovitsya-tbilisi': 'Aerial view of Tbilisi neighborhoods at dusk, Narikala fortress on hilltop, Kura river winding through city, lights beginning to glow, dramatic sky, travel photography',
    'tbilisi-shopping': 'Georgian traditional crafts market, colorful carpets, silver jewelry, clay pottery, churchkhela hanging, Dry Bridge market atmosphere, vibrant colors, no text',
    'kazbegi-v-mae': 'Gergeti Trinity Church surrounded by blooming wildflowers in May, snow-capped Kazbek peak in background, green alpine meadows, dramatic storm clouds, golden light, no people, no text',
    'gergetskaya-troitsa': 'Close-up of Gergeti Trinity Church stone walls and tower, medieval Georgian architecture, misty mountains behind, dramatic sky, professional photography, no text',
    'kazbegi-gde-ostanovitsya': 'Cozy mountain guesthouse in Kazbegi village, traditional Georgian stone architecture, garden with mountain views, Kazbek peak visible, warm hospitality atmosphere, no text',
    'signagi-dostoprimechatelnosti': 'Sighnaghi town walls and towers at sunset, Alazani valley vineyards below, Caucasus mountains on horizon, golden hour, romantic atmosphere, no text, no people',
    'telavi-za-1-den': 'Telavi old town center, ancient plane tree, traditional Georgian architecture, wine region landscape in background, sunny day, travel photography, no text',
    'boji-park-kakheti': 'Lush subtropical park in Kakheti, exotic trees and palms, wine barrels decoration, Georgian countryside feel, green nature, no text',
    'gruziya-v-mae': 'Georgia in May, diverse landscapes collage feel — green mountains, blooming orchards, ancient churches, spring wildflowers, vibrant nature, professional travel photography, no text',
    'gruziya-bezopasnost': 'Friendly Georgian street scene, locals and tourists walking together safely, colorful Tbilisi old town, welcoming atmosphere, sunny day, no text',
    'chto-nelzya-gruziya': 'Georgian Orthodox church interior with candles, respectful atmosphere, golden icons, ancient stone walls, soft light, no people, no text',
    'khinkali-tbilisi-luchshie': 'Close-up of fresh Georgian khinkali dumplings steaming on plate, rustic wooden table, Georgian restaurant atmosphere, food photography, no text',
    'khachapuri-adjarski-tbilisi': 'Adjaruli khachapuri fresh from oven, egg and butter melting, traditional Georgian bakery, food photography, warm tones, no text',
    'tbilisi-kofeyni': 'Cozy Tbilisi coffee shop interior, exposed brick walls, vintage decor, specialty coffee cups, plants, warm lighting, no people, no text',
    'kutaisi-za-1-den': 'Kutaisi Bagrati Cathedral on hilltop, green Rioni river valley below, blue sky, ancient Georgian architecture, dramatic perspective, no text',
    'borzhomi-iz-tbilisi': 'Borjomi mineral spring park, lush green trees, historic Victorian-era pavilion over mineral water spring, peaceful nature, no text',
    'ananuri-krepost': 'Ananuri fortress complex on Georgian Military Highway, medieval towers reflected in Zhinvali reservoir, dramatic sky, no people, no text',
    'gruziya-na-mashine': 'Scenic Georgian Military Highway road through Caucasus mountains, dramatic mountain landscape, winding road, clear sky, travel photography, no text, no cars',
    'transport-tbilisi': 'Tbilisi metro station interior, modern design, Georgian script on signs, clean architecture, no people, no text overlay',
    'pogoda-tbilisi-po-mesyatsam': 'Four seasons in Tbilisi collage feel — spring blossoms, summer sun, autumn golden leaves, light winter snow, old town backdrop, no text',
}

def generate_image(slug, prompt):
    out_path = os.path.join(IMAGES_DIR, f'{slug}.webp')
    if os.path.exists(out_path):
        print(f'  ⏭  {slug} — уже существует, пропускаю')
        return True

    print(f'  🎨 Генерирую: {slug}...')
    r = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
        json={
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1792x1024',
            'quality': 'standard',
            'style': 'natural'
        },
        timeout=60
    )
    if r.status_code != 200:
        print(f'  ❌ Ошибка {r.status_code}: {r.text[:100]}')
        return False

    url = r.json()['data'][0]['url']
    img = requests.get(url, timeout=30).content
    os.makedirs(IMAGES_DIR, exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(img)
    print(f'  ✅ {slug}.webp ({len(img)//1024} KB)')
    return True


def main():
    args = sys.argv[1:]

    if not args or args[0] == 'all':
        slugs = list(PROMPTS.keys())
        print(f'Генерирую {len(slugs)} изображений...\n')
        for i, (slug, prompt) in enumerate(PROMPTS.items()):
            generate_image(slug, prompt)
            if i < len(slugs) - 1:
                time.sleep(1)  # rate limit
    else:
        slug = args[0]
        if slug not in PROMPTS:
            print(f'❌ Slug "{slug}" не найден в списке')
            print('Доступные:', ', '.join(PROMPTS.keys()))
            return
        generate_image(slug, PROMPTS[slug])

if __name__ == '__main__':
    main()
