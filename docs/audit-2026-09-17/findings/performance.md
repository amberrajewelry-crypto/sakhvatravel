# Performance / Core Web Vitals — sakhva-travel.com

Дата: 2026-09-17. PSI API вернула 429 (квота исчерпана другим проектом сегодня) — использованы Lighthouse 13 CLI (lab, mobile, simulated throttling) + curl timing + HTML/CSP анализ. CrUX (field) недоступен по той же причине.

## Score (Lighthouse Performance, mobile, lab)

| URL | Score | LCP | FCP | TBT | CLS | TTI/Speed Index |
|---|---|---|---|---|---|---|
| `/` (home) | **93/100** | 2.7s | 2.4s | 30ms | 0 | TTI 2.7s |
| `/ekskursiya/vinniy-marshrut-alazani/` (tour) | **95/100** | 2.6s | 2.2s | 20ms | 0 | TTI 4.7s |
| `/en/` | не снят (PSI 429, лимит вызовов) | — | — | — | — | — |
| `/blog/rayony-tbilisi-gde-ostanovitsya/` | не снят (PSI 429) | — | — | — | — | — |

Desktop lab и CrUX field — не получены (см. причину выше). Заметка себе: повторить `pagespeed_check.py` позже (лимит сброшен через ~1 мин при следующем окне 240 QPM/25000 QPD).

## Core Web Vitals статус (по lab-данным, mobile)

| Метрика | Home | Tour | Статус |
|---|---|---|---|
| LCP | 2.7s | 2.6s | **Needs Improvement** (порог good ≤2.5s, обе страницы чуть выше) |
| CLS | 0 | 0 | Good |
| TBT (прокси для INP) | 30ms / 22ms | Good — INP на реальных устройствах, скорее всего, тоже good |

INP по CrUX не получен (нет field data в этом прогоне) — TBT крайне низкий, main thread не забит, риска по INP не видно.

## TTFB / сеть (curl, --compressed)

| URL | TTFB (time_starttransfer) | Total | Размер HTML |
|---|---|---|---|
| `/` | 151ms | 167ms | 82 KB |
| `/en/` | 139ms | 154ms | 70 KB |
| tour | 152ms | 157ms | 20 KB |
| blog | 124ms | 131ms | 19 KB |

TTFB везде <200ms — хорошо, не бутылочное горлышко.

## Вес ресурсов

- Home: 689 KiB total
- Tour: 553 KiB total, включая ~51 KiB неиспользуемого JS (Lighthouse `unused-javascript`)

## Что уже сделано правильно (не трогать)

- Hero-изображение (`/images/guide-timur-*.webp`) с `fetchpriority="high"`, `loading="eager"`, `<link rel=preload as=image>` + `imagesrcset` под разные ширины — учебниковая LCP-оптимизация.
- Все `<img>` с `width`/`height` — нет источников CLS.
- Шрифты self-hosted (`/fonts/lora-*.woff2`), `preload as=font crossorigin` — нет FOIT/задержки.
- CSS через `preload + onload` (async-паттерн) для `all.css`, `deferred.css`, `seamless.css`, `overrides.css` — не блокирует рендер.
- Кэш статики: `cache-control: public, max-age=31536000, immutable` на изображениях — корректно.
- HTML: `cache-control: max-age=0, must-revalidate, s-maxage=86400, stale-while-revalidate=604800` — разумный edge-кэш с ревалидацией.
- CLS = 0 на обеих проверенных страницах.

## Сторонние скрипты (по CSP, домены подключены)

GTM (googletagmanager), Яндекс.Метрика (mc.yandex.ru, есть preconnect), Microsoft Clarity, PostHog, Ahrefs Analytics, Cloudflare Insights, Travelpayouts (tp.media/tpwgt.com/c31.travelpayouts.com), Kiwitaxi widget, Localrent widget, Google Ads/DoubleClick, Yandex Travel.

Это **7-9 независимых third-party доменов** — суммарный третье-парти вес не измерен точно (Lighthouse `third-party-summary` не вернул данные в этом прогоне без сети throttling-профиля blocking-time), но такое количество виджетов — типичный источник INP-деградации на слабых мобильных устройствах и лишних preconnect'ов, за которыми стоит следить.

## Проблемы и приоритет фиксов (по влиянию)

1. **LCP 2.6–2.7s — вплотную к порогу "needs improvement" (2.5s)** — Severity: Medium.
   Hero-изображение и так преloaded, шрифты preloaded; узкое место — вероятно render-delay между TTFB (150ms) и LCP paint (~2.5s), т.е. ~2.5s уходит на скачивание/декодирование preload-цепочки (шрифт + CSS + hero) до отрисовки. 
   Фикс: сжать `deferred.css`/`seamless.css`/`overrides.css` в один критический inline-блок для above-the-fold, остальное — грузить после LCP; проверить, не конкурирует ли `guide-timur-1200.webp` (какой реально размер грузится на mobile viewport) — если mobile получает 1200w вместо 768w, урезать точку в srcset. Ожидаемый эффект: LCP -300..600ms → уверенно в "good".

2. **7-9 сторонних доменов (GTM/Метрика/Clarity/PostHog/Ahrefs/Cloudflare Insights/Travelpayouts/Kiwitaxi/Localrent)** — Severity: Medium.
   Каждый — отдельный DNS+TLS хендшейк и потенциальный main-thread blocking JS. TBT сейчас низкий (22-30ms), но это lab-throttling без реальных мобильных CPU троттлингов такого масштаба виджетов (кивитакси/localrent виджеты обычно тяжелее в реальности).
   Фикс: грузить Clarity/PostHog/Ahrefs через GTM с задержкой (`load on interaction` / после LCP), не как отдельные блокирующие `<script>` в head, если они там; убрать `Kiwitaxi`/`Localrent` widget-скрипты с страниц, где они не используются (сузить CSP/подключение по маршруту). Ожидаемый эффект: -100-300ms TBT/INP на слабых устройствах, меньше network contention для LCP.

3. **51 KiB неиспользуемого JS на странице тура** — Severity: Low.
   Фикс: code-split / убрать неиспользуемые библиотеки на странице тура (Lighthouse укажет конкретный chunk в full JSON `unused-javascript.details.items`). Эффект: небольшой (TBT и так низкий), но снижает вес и парсинг.

4. **PSI/CrUX field data не собраны в этом прогоне** — Severity: Info (не баг сайта, ограничение среды).
   Повторить `pagespeed_check.py` для `/en/`, тура и блога, а также desktop-стратегию для home, когда квота 240 QPM сбросится; сверить lab LCP 2.6-2.7s с полевым p75 — CrUX может показывать хуже из-за реальных мобильных CPU/сетей (throttling в этом прогоне — Lighthouse simulate, не самый жёсткий).

## Итог

Сайт технически грамотно оптимизирован (preload/preconnect/self-hosted fonts/lazy images/immutable cache) — CLS идеален, TTFB отличный, TBT низкий. Единственный метрический риск — LCP на границе good/needs-improvement на mobile (2.6-2.7s против порога 2.5s), усугубляемый количеством сторонних доменов. Приоритет: (1) урезать критический CSS/preload-цепочку до LCP, (2) отложить non-critical third-party scripts за требование взаимодействия/idle.
