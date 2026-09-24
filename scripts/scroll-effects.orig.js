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
        var text = el.textContent.trim();
        var match = text.match(/(\d[\d\s,.]*)/);
        if (match) {
          var numStr = match[1].trim();
          var dotPos = numStr.indexOf('.');
          var decimals = dotPos >= 0 ? numStr.length - dotPos - 1 : 0;
          var raw = numStr.replace(/[\s,]/g, '');
          var target = parseFloat(raw);
          if (target > 0 && target < 10000) {
            var prefix = text.substring(0, text.indexOf(numStr));
            var afterNum = text.substring(text.indexOf(numStr) + numStr.length);
            var suffix = afterNum.replace(/^\+/, '');
            var hasPlus = afterNum.charAt(0) === '+';
            var duration = 1400;
            var startTime = null;
            function step(ts) {
              if (!startTime) startTime = ts;
              var progress = Math.min((ts - startTime) / duration, 1);
              var eased = 1 - Math.pow(1 - progress, 3);
              var current = target * eased;
              var display = decimals > 0 ? current.toFixed(decimals) : Math.round(current);
              el.textContent = prefix + display + (hasPlus ? '+' : '') + suffix;
              if (progress < 1) requestAnimationFrame(step);
            }
            requestAnimationFrame(step);
          }
        }
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.guide-badge-num, [data-counter], .counter, .hs-val').forEach(function(el) {
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

  // ─── 8. HERO IMAGE PARALLAX — background moves slower ───
  var heroImg = document.getElementById('hero-poster-img');
  if (heroImg) {
    var imgTicking = false;
    function updateHeroImgParallax() {
      var scrollY = window.pageYOffset;
      var heroH = document.getElementById('hero').offsetHeight;
      if (scrollY < heroH) {
        var offset = scrollY * 0.25;
        heroImg.style.transform = 'translate3d(0,' + offset + 'px,0) scale(1.08)';
      }
      imgTicking = false;
    }
    heroImg.style.willChange = 'transform';
    heroImg.style.transform = 'translate3d(0,0,0) scale(1.08)';
    window.addEventListener('scroll', function() {
      if (!imgTicking) { requestAnimationFrame(updateHeroImgParallax); imgTicking = true; }
    }, { passive: true });
  }

  // ─── 9. BLUR-TO-FOCUS SECTIONS — sections appear with blur dissolve ───
  var blurStyle = document.createElement('style');
  blurStyle.textContent = '.blur-reveal{opacity:0;filter:blur(8px);transform:translateY(32px);transition:opacity .9s cubic-bezier(.22,1,.36,1),filter 1s cubic-bezier(.22,1,.36,1),transform .9s cubic-bezier(.22,1,.36,1)}.blur-reveal.is-revealed{opacity:1;filter:blur(0);transform:translateY(0)}';
  document.head.appendChild(blurStyle);

  var blurObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
        blurObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -80px 0px' });

  document.querySelectorAll('.sec, #guide, #instagram, #why, #how, #faq').forEach(function(el) {
    if (!el.closest('#hero') && !el.closest('.tours-pinned')) {
      el.classList.add('blur-reveal');
      blurObserver.observe(el);
    }
  });

  // ─── 10. 3D TILT ON TOUR CARDS — perspective tilt on hover ───
  if (!isMobile) {
    var tiltStyle = document.createElement('style');
    tiltStyle.textContent = '.hp-card{transition:transform .5s cubic-bezier(.32,.72,0,1),box-shadow .5s cubic-bezier(.32,.72,0,1),border-color .3s;transform-style:preserve-3d;will-change:transform;border:1px solid #f0f0ee !important}.hp-card:hover{box-shadow:0 24px 48px rgba(26,61,46,.10),0 8px 20px rgba(0,0,0,.06);border-color:rgba(245,158,11,.25) !important}';
    document.head.appendChild(tiltStyle);

    document.addEventListener('mousemove', function(e) {
      var cards = document.querySelectorAll('.hp-card');
      cards.forEach(function(card) {
        var rect = card.getBoundingClientRect();
        if (e.clientX >= rect.left && e.clientX <= rect.right &&
            e.clientY >= rect.top && e.clientY <= rect.bottom) {
          var x = (e.clientX - rect.left) / rect.width;
          var y = (e.clientY - rect.top) / rect.height;
          var rotateX = (0.5 - y) * 8;
          var rotateY = (x - 0.5) * 8;
          card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) scale(1.02)';
        }
      });
    }, { passive: true });

    document.addEventListener('mouseleave', function(e) {
      if (e.target && e.target.classList && e.target.classList.contains('hp-card')) {
        e.target.style.transform = '';
      }
    }, true);

    document.querySelectorAll('.hp-card').forEach(function(card) {
      card.addEventListener('mouseleave', function() {
        this.style.transform = '';
      });
    });

    // Also apply to dynamically rendered cards
    var gridObserver = new MutationObserver(function() {
      document.querySelectorAll('.hp-card').forEach(function(card) {
        card.addEventListener('mouseleave', function() {
          this.style.transform = '';
        });
      });
    });
    var hpGrid = document.getElementById('hp-grid');
    if (hpGrid) gridObserver.observe(hpGrid, { childList: true });
  }

  // ─── 11. MAGNETIC BUTTONS — hero CTAs attract toward cursor ───
  if (!isMobile) {
    var magnets = document.querySelectorAll('.btn-primary, .btn-outline-hero');
    magnets.forEach(function(btn) {
      btn.style.transition = 'transform .3s cubic-bezier(.22,1,.36,1)';
      btn.addEventListener('mousemove', function(e) {
        var rect = btn.getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = 'translate(' + (x * 0.2) + 'px,' + (y * 0.25) + 'px)';
      });
      btn.addEventListener('mouseleave', function() {
        btn.style.transform = 'translate(0,0)';
      });
    });
  }

  // ─── 12. STAGGERED CARD ENTRANCE (first 9 only) ───
  if (!isMobile) {
    var cardStyle = document.createElement('style');
    cardStyle.textContent = '.hp-card.card-anim{opacity:0;transform:translateY(30px);transition:opacity .5s cubic-bezier(.22,1,.36,1),transform .5s cubic-bezier(.22,1,.36,1)}.hp-card.card-anim.card-in{opacity:1;transform:translateY(0)}';
    document.head.appendChild(cardStyle);

    var hpGridEl = document.getElementById('hp-grid');
    if (hpGridEl) {
      var cardObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            var cards = hpGridEl.querySelectorAll('.hp-card');
            var limit = Math.min(cards.length, 9);
            for (var i = 0; i < limit; i++) {
              cards[i].classList.add('card-anim');
            }
            requestAnimationFrame(function() {
              for (var j = 0; j < limit; j++) {
                (function(idx) {
                  setTimeout(function() {
                    cards[idx].classList.add('card-in');
                  }, idx * 80);
                })(j);
              }
            });
            cardObserver.unobserve(hpGridEl);
          }
        });
      }, { threshold: 0.02, rootMargin: '0px 0px -20px 0px' });

      cardObserver.observe(hpGridEl);
    }
  }

})();
