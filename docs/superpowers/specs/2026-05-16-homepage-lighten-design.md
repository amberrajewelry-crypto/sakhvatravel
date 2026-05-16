# Sakhva Travel — облегчение главной + параллакс hero

**Дата:** 2026-05-16
**Статус:** approved
**Scope:** index.html, css/deferred.src.css

## Цель

Убрать все видео с главной страницы, заменить на статичные фото. Добавить параллакс-эффект в hero для визуальной уникальности. Тексты не менять.

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

## Файлы которые НЕ удаляем

Видео-файлы в /images/ остаются — они используются на страницах туров (/tour/*/).
Удаление видео-файлов — отдельная задача после проверки зависимостей.

## Ограничения

- main.js нельзя трогать (CLAUDE.md)
- main.js перезаписывает #rev-grid через fetch /api/reviews — не мешает этой задаче
- Параллакс JS добавляется как inline script в index.html (не в main.js)
- Predeploy check обязателен перед деплоем

## Ожидаемый результат

- Загрузка главной: -3-5 сек (нет video preload/decode)
- LCP: улучшится (фото уже preload)
- CLS: 0 (размеры img заданы)
- Визуал: параллакс в hero — движение без видео
- Совместимость: все браузеры, iOS Safari, Android Chrome
