# Sakhva Travel — облегчение главной + параллакс hero + Oura-стиль

**Дата:** 2026-05-16
**Статус:** approved
**Scope:** index.html, css/deferred.src.css, страницы /tour/*/

## Контекст (SEO)

Сайт невидим по коммерческим ключам в Google ("гид тбилиси" = 0 показов, "экскурсия тбилиси" = 0). Страницы туров проиндексированы, но ранжируются ниже 100-й позиции. Текущий HTML = 265KB (норма <50KB), 22 скрипта, 60+ видео. Core Web Vitals — фактор ранжирования. Облегчение = прямой путь к позициям.

## Визуальный эталон

https://ouraring.com/ — взять стиль скролл-анимаций и появлений, адаптировать под цвета Sakhva (#1A3D2E зелёный + тёплый бежевый). Ключевые элементы:
- Чистые секции с большим пространством между блоками
- Fade-in reveal при скролле (opacity + translateY)
- Крупная serif-типографика с italic-акцентами (Lora уже есть)
- Минимализм — ничего лишнего, каждый элемент дышит

## Цель

Убрать все видео с главной и страниц туров, заменить на фото высшего качества. Добавить параллакс в hero + Oura-стиль scroll reveal. Тексты не менять.

## Performance-цели

| Метрика | Сейчас | Цель |
|---------|--------|------|
| HTML size | 265 KB | < 100 KB |
| Script tags | 22 | < 10 |
| Video files loaded | 10+ | 0 |
| LCP | ~4-6s | < 2.5s |
| CLS | ~0.1 | 0 |
| images/ total | 205 MB | < 50 MB |

## Что меняется

### 1. Hero — параллакс вместо видео

**Убрать:**
- `<video id="hero-vid">` и inline-скрипт загрузки видео (index.html:447-450)
- `#video-backdrop` обёртку с video-логикой

**Оставить:**
- `<img id="hero-poster-img">` — уже есть, preload в head, srcset с 3 размерами
- Весь контент `<header id="hero">` — stats, h1, buttons, micro text

**Добавить:**
- CSS parallax через `transform: translate3d()` на скролл
- Два слоя: фоновое фото (скорость 0.5x) и текстовый блок (скорость 1x)
- JS: ~20 строк, IntersectionObserver + requestAnimationFrame + scroll listener (passive)
- На мобилке (max-width:768px) параллакс отключается — статичная картинка

**Реализация параллакса:**
```
#video-backdrop → переименовать в #hero-bg
  position: relative → sticky не нужен
  img: transform: translate3d(0, calc(scrollY * 0.3), 0)
  hero-overlay: transform: translate3d(0, calc(scrollY * -0.1), 0)
```

JS-логика:
```js
var heroBg = document.getElementById('hero-bg');
var heroImg = heroBg.querySelector('img');
var heroOverlay = document.getElementById('hero');
var ticking = false;

window.addEventListener('scroll', function() {
  if (!ticking) {
    requestAnimationFrame(function() {
      var scrollY = window.pageYOffset;
      if (scrollY < window.innerHeight * 1.5) {
        heroImg.style.transform = 'translate3d(0,' + (scrollY * 0.3) + 'px,0)';
        heroOverlay.style.transform = 'translate3d(0,' + (scrollY * -0.1) + 'px,0)';
      }
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });
```

На мобилке — `@media(max-width:768px)` отключать через `will-change: auto` и не применять transforms.

### 2. Карточки туров — видео → фото

**Убрать:**
- `<video>` внутри `.tc-media` (12 карточек)
- Атрибуты `data-src` для lazy video

**Заменить на:**
- `<img>` с текущими poster-картинками (уже существуют):
  - kazbegi-tour.webp
  - kakheti-tour.webp
  - kutaisi-tour.webp
  - batumi-tour.webp
  - и т.д.
- `loading="lazy"` на всех кроме первых 2
- Убрать класс `tc-video` с articles

### 3. Gallery preview — видео → фото

**Убрать:**
- 4 элемента `.gp-item` с `<video>` (gallery-17, 18, 19, 28)

**Заменить на:**
- `<img>` с существующими фото из галереи (gallery-1.webp, gallery-3.webp, gallery-7.webp, gallery-10.webp)
- `loading="lazy"`

### 4. Gallery modal — видео → фото

**Убрать:**
- 7 элементов `.gm-item` с `<video>` (gallery-17, 18, 19, 24, 26, 27, 28, 30, 33)

**Заменить на:**
- Пропустить эти слоты (оставить только фото-элементы)
- Или заменить на скриншоты из видео (если есть)

### 5. CSS изменения (deferred.src.css)

- Убрать стили для `.tc-video` video-специфичных правил
- Добавить параллакс-стили для `#hero-bg`:
  ```css
  #hero-bg { overflow: hidden; }
  #hero-bg img { will-change: transform; }
  @media(max-width:768px) {
    #hero-bg img { will-change: auto; transform: none !important; }
  }
  ```

## Что НЕ меняется

- Структура секций (9 секций, порядок тот же)
- Все тексты (data-ru, data-en)
- Навигация (#nav, burger, drawer)
- FAB (#fab-main)
- main.js — НЕ ТРОГАЕМ
- Модалы (payment, contact, booking, quiz)
- Blog, FAQ, footer секции
- SEO: meta tags, schema, canonical, hreflang
- Шрифты, цвета, типографика

### 6. Страницы туров (/tour/*/) — видео → фото

11 видео на страницах туров тоже заменяем на фото. Извлекаем лучшие кадры из видео через ffmpeg (макс. качество, WebP q92). Если качество кадров недостаточно (исходные видео 1280x720) — пользователь предоставит оригиналы фото.

### 7. Oura-стиль scroll reveal

Усилить существующую систему `.reveal`:
- Добавить `translateY(40px)` → `translateY(0)` с `opacity: 0 → 1`
- Stagger-эффект: дочерние элементы появляются каскадом (transition-delay через CSS)
- Добавить blur(4px) → blur(0) для премиального feel
- Большие отступы между секциями (padding: 80px → 120px)
- На мобилке: упрощённый reveal без blur

### 8. Удаление дублей видео

Три версии каждого видео (video.mp4 / video-hd.mp4 / video-1080.mp4) — после замены на фото, удалить неиспользуемые видео-файлы. Это отдельный шаг после проверки что ни одна страница их не использует.

## Файлы которые НЕ удаляем (пока)

Видео-файлы удаляются только после проверки что ни одна страница на них не ссылается. Удаление — отдельный шаг с подтверждением.

## Ограничения

- main.js нельзя трогать (CLAUDE.md)
- main.js перезаписывает #rev-grid через fetch /api/reviews — не мешает этой задаче
- Параллакс JS добавляется как inline script в index.html (не в main.js)
- Predeploy check обязателен перед деплоем

## Ожидаемый результат

- HTML < 100KB (сейчас 265KB) → быстрее парсинг, лучше crawl budget
- LCP < 2.5s → Core Web Vitals pass → фактор ранжирования Google
- CLS: 0 (размеры img заданы)
- 0 видео на главной и страницах туров → -150MB трафика
- images/ < 50MB (сейчас 205MB) после удаления дублей видео
- Визуал: параллакс hero + Oura-стиль reveal анимации
- Совместимость: все браузеры, iOS Safari, Android Chrome
- SEO: улучшение Core Web Vitals → рост позиций коммерческих страниц
