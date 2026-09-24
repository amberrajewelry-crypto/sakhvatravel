/* ============================================================
   SAKHVA TRAVEL — SMOOTH SCROLL (LENIS)
   Версия: 1.0
   Эффект: медленный инерционный скролл как на refractweb.com
   ============================================================ */

(() => {
  'use strict';

  // Проверка что Lenis загрузился
  if (typeof Lenis === 'undefined') {
    console.warn('[Sakhva] Lenis не загрузился. Проверьте подключение библиотеки.');
    return;
  }

  // Уважаем настройки доступности
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    console.info('[Sakhva] Smooth scroll отключён: prefers-reduced-motion.');
    return;
  }

  // Инициализация Lenis с параметрами под RefractWeb
  const lenis = new Lenis({
    duration: 3.2,           // длительность инерции (медленнее = премиальнее)
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    wheelMultiplier: 0.3,    // заметно медленнее нативного
    touchMultiplier: 0.9,    // на мобильных тоже медленнее
    lerp: 0.035,             // очень плавная интерполяция
    infinite: false,
  });

  // RAF цикл
  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // Делаем lenis доступным глобально (на случай отладки)
  window.lenis = lenis;

  // --- Поддержка якорных ссылок (#tours, #reviews, #faq) ---
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      if (href === '#' || href === '#!') return;

      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      lenis.scrollTo(target, {
        offset: -80, // отступ под фиксированную навигацию
        duration: 2.0,
      });
    });
  });

  // --- Останавливаем Lenis внутри модальных окон и попапов ---
  // (чтобы внутри них работал нормальный нативный скролл)
  document.querySelectorAll(
    '.modal, [class*="modal"], [data-lenis-prevent], .popup, [class*="popup"]'
  ).forEach((el) => {
    el.setAttribute('data-lenis-prevent', '');
  });

  console.info('[Sakhva] Smooth scroll активирован.');
})();
