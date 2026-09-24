(function() {
  // Respect system preference
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reducedMotion) {
    document.querySelectorAll('.tours-slide, .fade-on-scroll, [data-anim], .reveal, .sec-divider').forEach(function(el) {
      el.classList.add('is-visible', 'is-active', 'is-vis', 'on');
    });
    var nav = document.getElementById('nav');
    if (nav) nav.classList.add('nav-loaded');
    return;
  }

  var isMobile = window.matchMedia('(max-width: 768px)').matches;

  // ─── 0. NAV ENTRANCE ───
  var nav = document.getElementById('nav');
  if (nav) {
    requestAnimationFrame(function() {
      nav.classList.add('nav-loaded');
    });
  }

  // ─── 1. SCROLL PROGRESS BAR ───
  var progressBar = document.getElementById('scroll-progress');
  if (progressBar) {
    var sTicking = false;
    function updateProgress() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? (window.pageYOffset / h) * 100 : 0;
      progressBar.style.width = pct + '%';
      sTicking = false;
    }
    window.addEventListener('scroll', function() {
      if (!sTicking) { requestAnimationFrame(updateProgress); sTicking = true; }
    }, { passive: true });
  }

  // ─── 2. Universal scroll animation observer ───
  var animObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-vis');
        animObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -60px 0px'
  });

  document.querySelectorAll('[data-anim], .sec-divider').forEach(function(el) {
    animObserver.observe(el);
  });

  // ─── 3. Legacy fade-on-scroll ───
  var fadeObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });

  document.querySelectorAll('.fade-on-scroll').forEach(function(el) {
    fadeObserver.observe(el);
  });

  // ─── 4. Reveal observer ───
  var revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('on');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  });

  document.querySelectorAll('.reveal').forEach(function(el) {
    revealObserver.observe(el);
  });

  // ─── 5. Counter animation for stat numbers ───
  var counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var el = entry.target;
        var text = el.textContent;
        var match = text.match(/(\d[\d\s,.]*)/);
        if (match) {
          var raw = match[1].replace(/[\s,.]/g, '');
          var target = parseInt(raw, 10);
          if (target > 0 && target < 10000) {
            var hasPlus = text.includes('+');
            var prefix = text.substring(0, text.indexOf(match[1]));
            var suffix = text.substring(text.indexOf(match[1]) + match[1].length);
            var duration = 1400;
            var startTime = null;
            function step(ts) {
              if (!startTime) startTime = ts;
              var progress = Math.min((ts - startTime) / duration, 1);
              var eased = 1 - Math.pow(1 - progress, 3);
              var current = Math.round(target * eased);
              el.textContent = prefix + current + (hasPlus ? '+' : '') + suffix;
              if (progress < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
          }
        }
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.guide-badge-num, [data-counter]').forEach(function(el) {
    counterObserver.observe(el);
  });

  // ─── 6. Image parallax on cards ───
  if (!isMobile) {
    var cards = document.querySelectorAll('.tours-track .tc-media video');
    if (cards.length) {
      var paraTicking = false;
      function updateCardParallax() {
        cards.forEach(function(img) {
          var rect = img.getBoundingClientRect();
          if (rect.bottom > 0 && rect.top < window.innerHeight) {
            var center = (rect.top + rect.bottom) / 2;
            var viewCenter = window.innerHeight / 2;
            var offset = (center - viewCenter) * 0.04;
            img.style.transform = 'translateY(' + offset + 'px) scale(1)';
          }
        });
        paraTicking = false;
      }
      window.addEventListener('scroll', function() {
        if (!paraTicking) { requestAnimationFrame(updateCardParallax); paraTicking = true; }
      }, { passive: true });
    }
  }

  // ─── 7. HERO PARALLAX — text scrolls up, fades out ───
  if (!isMobile) {
    var heroWrap = document.querySelector('.hero-wrap');
    var heroStats = document.querySelector('.hero-stats');
    var hero = document.getElementById('hero');

    if (heroWrap && hero) {
      var pTicking = false;

      function updateHeroParallax() {
        var scrollY = window.pageYOffset;
        var heroH = hero.offsetHeight;

        if (scrollY < heroH) {
          var ratio = scrollY / heroH;
          var translateY = -(scrollY * 0.5);
          var opacity = 1 - ratio * 1.5;
          opacity = Math.max(0, Math.min(1, opacity));

          heroWrap.style.transform = 'translate3d(0,' + translateY + 'px,0)';
          heroWrap.style.opacity = opacity;

          if (heroStats) {
            heroStats.style.transform = 'translate3d(0,' + (translateY * 0.3) + 'px,0)';
            heroStats.style.opacity = opacity;
          }
        }

        pTicking = false;
      }

      window.addEventListener('scroll', function() {
        if (!pTicking) {
          requestAnimationFrame(updateHeroParallax);
          pTicking = true;
        }
      }, { passive: true });
    }
  }
})();
