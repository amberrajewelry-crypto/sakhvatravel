# Performance / Core Web Vitals — sakhva-travel.com

Score: **82/100**. Замер: прямой curl (desktop, Тбилиси-регион) + анализ ресурсов. Агент seo-performance упал по socket — замер выполнен вручную оркестратором.

## Контекст (установлено ранее, НЕ пере-открытие)
PSI mobile 79-93; потолок держат 3rd-party (Yandex Metrica ~870мс, GTM, PostHog) + Vercel TTFB ~653мс (mobile lantern). Реальный foreground LCP ~690мс. Аналитика уже отложена на interaction. hero-grain убран, hero 66KB webp/async. H1/аналитику/клоакинг НЕ трогать.

## Замеры (desktop)
| URL | TTFB | Total | HTML |
|---|---|---|---|
| `/` | 318мс | 373мс | **358 KB** |
| `/blog/metro-tbilisi/` | 182мс | 191мс | 72 KB |
| `/ekskursiya/tur-batumi-iz-tbilisi/` | 325мс | 339мс | 86 KB |

## Находки

### Medium — главная 358 KB HTML (крупный inline-документ)
Главная отдаёт 358 KB HTML (inline CSS + весь контент секций). На мобиле это время парсинга DOM + main-thread. Блог/тур — 72-86 KB (норма). 
**Фикс:** проверить, весь ли inline-CSS главной используется above-the-fold; вынести below-fold секции (галерея, отзывы, explore-хаб) в отложенную загрузку/меньший критический HTML. Выигрыш: −100-150 KB с критического парсинга, TBT/INP на mobile.

### Medium — 8 render-blocking stylesheet-линков на главной
В `<head>` главной 8 `rel="stylesheet"` + 2 внешних `<script src>`. Даже при deferred-стратегии это цепочка блокирующих запросов. 
**Фикс:** подтвердить, что не-критические CSS идут через `media="print"`+onload swap или preload; сконсолидировать. Выигрыш: FCP на mobile при слабой сети.

### Low (закрыто, не проблема) — inline-SVG схема метро
`/blog/metro-tbilisi/` inline-SVG: 2 svg, 23 circle, 9 line, 26 text ≈ 60 элементов, ~несколько KB, статичный, с явными размерами viewBox. **Влияния на LCP/CLS нет** — вопрос закрыт, менять не нужно. Плюс для image-intent «карта метро».

### Info — INP не замерен инструментально
Прямого INP-замера нет (нужен реальный Chrome-трейс с взаимодействием). По архитектуре (статика + отложенная аналитика) риск низкий, но FAB/квиз/переключатель языка стоит проверить на длинные таски при следующем реальном трейсе.

## Что работает
TTFB 180-325мс (desktop, ок), hero fetchpriority=high + webp/async, картинки блога webp lazy, аналитика отложена, hero-grain убран. Потолок PSI — 3rd-party + TTFB, а не код (менять смысла нет без отказа от трекинга).
