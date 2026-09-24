/* Lenis smooth scroll — gentle slowdown for desktop + mobile */
(() => {
  'use strict';
  if (typeof Lenis === 'undefined') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const lenis = new Lenis({
    duration: 1.4,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
    smoothTouch: false,
    wheelMultiplier: 0.7,
    lerp: 0.1,
    infinite: false,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  window.lenis = lenis;

  // Respect modals — stop Lenis when body overflow is hidden
  const mo = new MutationObserver(() => {
    if (document.body.style.overflow === 'hidden') lenis.stop();
    else lenis.start();
  });
  mo.observe(document.body, { attributes: true, attributeFilter: ['style'] });

  // Anchor links support
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#' || href === '#!') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      lenis.scrollTo(target, { offset: -80, duration: 1.4 });
    });
  });

  // Prevent Lenis inside scrollable modals/popups
  document.querySelectorAll('[data-lenis-prevent], .modal, .popup, .drawer').forEach((el) => {
    el.setAttribute('data-lenis-prevent', '');
  });
})();
