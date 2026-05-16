# Homepage Lighten + Parallax Hero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all videos from homepage and tour pages, replace with high-quality photos, add parallax hero effect and Oura-style scroll reveal animations to improve Core Web Vitals and Google rankings.

**Architecture:** Static HTML site (no framework). All changes are in HTML files (index.html + 11 tour pages) and CSS (deferred.src.css). main.js is NOT touched. Parallax and reveal JS is added as inline `<script>` in index.html. Images extracted from existing videos via ffmpeg, converted to WebP q92.

**Tech Stack:** HTML, CSS, inline JS (vanilla), ffmpeg for frame extraction, cwebp for WebP conversion, Vercel for deploy.

**Spec:** `docs/superpowers/specs/2026-05-16-homepage-lighten-design.md`

---

## Pre-flight: Sync Local with Production

**CRITICAL:** Production runs a `vercel promote`d deployment from 2026-05-15. Local git (branch `redesign/final`, commit `7690362`) does NOT match prod. Before any changes, create a clean branch from the current state.

---

### Task 0: Create feature branch and backup

**Files:**
- No file changes — git operations only

- [ ] **Step 1: Create backup alias of current prod**

```bash
cd /Users/vladimir/sakhva-travel
~/.npm-global/bin/vercel ls 2>&1 | head -5
```

Note the current production URL for rollback if needed.

- [ ] **Step 2: Create feature branch from current state**

```bash
cd /Users/vladimir/sakhva-travel
git checkout -b feature/lighten-homepage
```

- [ ] **Step 3: Commit**

```bash
git commit --allow-empty -m "feature/lighten-homepage: start branch"
```

---

### Task 1: Extract high-quality frames from all videos

**Files:**
- Create: `/images/extracted-frames/*.webp` (13 files)

This task extracts the best frame from each video used on the site and converts to WebP q92 at the video's native resolution (1280x720 or 1280x956). These replace the existing low-resolution poster images (800x270).

- [ ] **Step 1: Extract best frames from all tour videos as PNG (lossless)**

```bash
cd /Users/vladimir/sakhva-travel/images
mkdir -p extracted-hq

# Hero background video (1280x956)
~/bin/ffmpeg -y -i tours-bg-video-v2.mp4 -vf "select='eq(n,48)',scale=-1:-1" -frames:v 1 -q:v 1 extracted-hq/hero-bg.png 2>/dev/null

# Tour videos — extract frame at ~2 seconds (best scenic moment)
~/bin/ffmpeg -y -i kazbegi-hero-video.mp4 -ss 3 -frames:v 1 -q:v 1 extracted-hq/kazbegi.png 2>/dev/null
~/bin/ffmpeg -y -i kakheti-video-hd.mp4 -ss 3 -frames:v 1 -q:v 1 extracted-hq/kakheti.png 2>/dev/null
~/bin/ffmpeg -y -i kutaisi-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/kutaisi.png 2>/dev/null
~/bin/ffmpeg -y -i batumi-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/batumi.png 2>/dev/null
~/bin/ffmpeg -y -i borjomi-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/borjomi.png 2>/dev/null
~/bin/ffmpeg -y -i night-tbilisi-video-hd.mp4 -ss 3 -frames:v 1 -q:v 1 extracted-hq/night-tbilisi.png 2>/dev/null
~/bin/ffmpeg -y -i dinner-video-hd.mp4 -ss 1.5 -frames:v 1 -q:v 1 extracted-hq/dinner.png 2>/dev/null
~/bin/ffmpeg -y -i soviet-card-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/soviet.png 2>/dev/null
~/bin/ffmpeg -y -i mtskheta-card-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/mtskheta.png 2>/dev/null
~/bin/ffmpeg -y -i digital-nomad-video-hd.mp4 -ss 2 -frames:v 1 -q:v 1 extracted-hq/digital-nomad.png 2>/dev/null
~/bin/ffmpeg -y -i slow-travel-video-hd.mp4 -ss 3 -frames:v 1 -q:v 1 extracted-hq/slow-travel.png 2>/dev/null
```

- [ ] **Step 2: Convert PNG to WebP q92 (highest quality)**

```bash
cd /Users/vladimir/sakhva-travel/images/extracted-hq
for f in *.png; do
  name="${f%.png}"
  cwebp -q 92 -m 6 "$f" -o "../${name}-tour-hq.webp" 2>/dev/null
  echo "Done: ${name}-tour-hq.webp ($(du -h "../${name}-tour-hq.webp" | cut -f1))"
done
```

Expected: 13 WebP files, ~80-150KB each, 1280px wide.

- [ ] **Step 3: Verify all output files exist and have reasonable size**

```bash
cd /Users/vladimir/sakhva-travel/images
ls -lh *-tour-hq.webp hero-bg-tour-hq.webp 2>/dev/null
identify *-tour-hq.webp hero-bg-tour-hq.webp 2>/dev/null | head -15
```

Expected: All files 1280px wide, 50-200KB each.

- [ ] **Step 4: Commit extracted images**

```bash
cd /Users/vladimir/sakhva-travel
git add images/*-tour-hq.webp images/hero-bg-tour-hq.webp
git commit -m "images: high-quality WebP frames extracted from videos (q92, 1280px)"
```

---

### Task 2: Remove hero video from index.html

**Files:**
- Modify: `index.html:446-451` (hero video section)

- [ ] **Step 1: Remove `<video>` element and video-loading script from hero**

In `index.html`, find lines 446-451. Replace the entire `#video-backdrop` div:

**FIND (lines 446-451):**
```html
<div id="video-backdrop">
<video id="hero-vid" muted loop playsinline preload="none" poster="/images/hero-photo-1200.webp?v=3" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
</video>
<img id="hero-poster-img" src="/images/hero-photo-mob-tall.webp?v=4" srcset="/images/hero-photo-mob-tall.webp?v=4 768w, /images/hero-photo-960.webp 960w, /images/hero-photo-1200.webp?v=3 1200w" sizes="100vw" alt="Тбилиси — частные экскурсии с гидом Тимуром" width="1200" height="800" fetchpriority="high" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1;transition:opacity .6s ease">
<script>!function(){var v=document.getElementById('hero-vid'),im=document.getElementById('hero-poster-img');if(!v)return;var loaded=false;function loadVideo(){if(loaded)return;loaded=true;var src=document.createElement('source');src.src='/images/tours-bg-video.mp4';src.type='video/mp4';v.appendChild(src);v.load();v.play().catch(function(){});v.addEventListener('playing',function(){if(im){im.style.opacity='0';im.style.pointerEvents='none'}},{once:true})}var mob=window.innerWidth<=768;if(mob){document.addEventListener('touchstart',function(){setTimeout(loadVideo,100)},{once:true,passive:true});document.addEventListener('scroll',function(){setTimeout(loadVideo,100)},{once:true,passive:true})}else if('requestIdleCallback' in window){requestIdleCallback(loadVideo,{timeout:3000})}else{setTimeout(loadVideo,2000)}}()</script>
</div>
```

**REPLACE WITH:**
```html
<div id="hero-bg">
<img id="hero-poster-img" src="/images/hero-photo-mob-tall.webp?v=4" srcset="/images/hero-photo-mob-tall.webp?v=4 768w, /images/hero-photo-960.webp 960w, /images/hero-photo-1200.webp?v=3 1200w" sizes="100vw" alt="Тбилиси — частные экскурсии с гидом Тимуром" width="1200" height="800" fetchpriority="high" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
</div>
```

This removes: the `<video>` tag, the inline script (video loader), and the `z-index:1;transition:opacity .6s ease` from the img (no longer needed — no video to crossfade to).

- [ ] **Step 2: Verify predeploy check passes**

```bash
cd /Users/vladimir/sakhva-travel
node scripts/predeploy-check.js index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

Expected: 0 errors.

- [ ] **Step 3: Commit**

```bash
cd /Users/vladimir/sakhva-travel
git add index.html
git commit -m "hero: remove video, keep static photo in #hero-bg"
```

---

### Task 3: Add parallax effect to hero

**Files:**
- Modify: `index.html` (add inline script after `</header>` closing tag at line 468)
- Modify: `css/deferred.src.css` (add parallax styles)

- [ ] **Step 1: Add parallax CSS to deferred.src.css**

Append at the end of `css/deferred.src.css`:

```css
/* ── Hero parallax ── */
#hero-bg{overflow:hidden}
#hero-bg img{will-change:transform;transition:none}
@media(max-width:768px){
  #hero-bg img{will-change:auto;transform:none!important}
  #hero{transform:none!important}
}
@media(prefers-reduced-motion:reduce){
  #hero-bg img{transform:none!important}
  #hero{transform:none!important}
}
```

- [ ] **Step 2: Add parallax JS as inline script after hero closing tag**

In `index.html`, after line 468 (`</header>`), before line 469 (`<main ...>`), insert:

```html
<script>
!function(){
  if(window.innerWidth<=768||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var bg=document.getElementById('hero-bg'),img=bg&&bg.querySelector('img'),hero=document.getElementById('hero');
  if(!bg||!img||!hero)return;
  var ticking=false;
  window.addEventListener('scroll',function(){
    if(!ticking){requestAnimationFrame(function(){
      var y=window.pageYOffset;
      if(y<window.innerHeight*1.5){
        img.style.transform='translate3d(0,'+y*0.3+'px,0)';
        hero.style.transform='translate3d(0,'+y*-0.1+'px,0)';
      }
      ticking=false;
    });ticking=true}
  },{passive:true});
}();
</script>
```

- [ ] **Step 3: Rebuild minified CSS**

```bash
cd /Users/vladimir/sakhva-travel
# If there's a CSS build step, run it. Otherwise copy src to dist:
cp css/deferred.src.css css/deferred.css
```

- [ ] **Step 4: Verify predeploy**

```bash
node scripts/predeploy-check.js index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

- [ ] **Step 5: Commit**

```bash
git add index.html css/deferred.src.css css/deferred.css
git commit -m "hero: add parallax effect (CSS transform3d, disabled on mobile)"
```

---

### Task 4: Replace tour card videos with photos on homepage

**Files:**
- Modify: `index.html:482-614` (11 tour cards with `<video>`)

- [ ] **Step 1: Replace each `<video>` in `.tc-media` with `<img>`**

For each of the 11 tour cards in `index.html`, replace the pattern:

```html
<div class="tc-media"><video muted loop playsinline preload="none" poster="/images/TOUR-tour.webp" data-src="/images/VIDEO.mp4"></video></div>
```

With:

```html
<div class="tc-media"><img src="/images/TOUR-tour.webp" alt="TOUR_ALT" width="1280" height="720" loading="lazy" style="width:100%;height:100%;object-fit:cover"></div>
```

Complete replacement list (poster → img src, add descriptive alt):

| Line | poster file | alt text (RU) |
|------|------------|---------------|
| 482 | kazbegi-tour.webp | Вид на Гергетскую церковь в Казбеги |
| 494 | kakheti-tour.webp | Виноградники и горы Кахетии |
| 506 | kutaisi-tour.webp | Каньон Мартвили в Кутаиси |
| 518 | batumi-tour.webp | Набережная Батуми |
| 530 | borjomi-tour.webp?v=1 | Парк Боржоми |
| 542 | night-tbilisi-tour.webp | Ночной Тбилиси с подсветкой |
| 554 | dinner-tour.webp | Грузинский ужин с вином |
| 566 | soviet-tour.webp | Советская архитектура Тбилиси |
| 578 | mtskheta-tour.webp | Монастырь Джвари в Мцхете |
| 590 | digital-nomad-tour.webp | Коворкинг в Тбилиси |
| 602 | slow-travel-tour.webp | Горная дорога в Грузии |

First two cards (`kazbegi`, `kakheti`) get `loading="eager"`, rest get `loading="lazy"`.

- [ ] **Step 2: Remove `tc-video` class from all article elements**

Remove the class `tc-video` from each `<article class="tc tc-video"` — change to `<article class="tc"`.

- [ ] **Step 3: Remove the video IO script (lines 619-642)**

Delete the entire script block that handles video preloading and play/pause:

```html
<script>
/* Video IO: preload nearby + play visible cards */
(function(){
var preloadIO=new IntersectionObserver(function(entries){
...
})();
</script>
```

This is lines 619-642 in the current file. Remove it entirely.

- [ ] **Step 4: Verify predeploy**

```bash
node scripts/predeploy-check.js index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "tours: replace 11 card videos with static photos"
```

---

### Task 5: Replace gallery videos with photos on homepage

**Files:**
- Modify: `index.html:1025-1028` (gallery preview — 4 videos)
- Modify: `index.html:1052-1068` (gallery modal — 9 videos)

- [ ] **Step 1: Replace 4 gallery preview videos**

Replace lines 1025-1028. Each `.gp-item` video becomes an `<img>`:

```html
<div class="gp-item"><img src="/images/gallery-1.webp?v=4" alt="Туристы у арки монастыря" loading="lazy" width="400" height="533" style="width:100%;height:100%;object-fit:cover;display:block"></div>
<div class="gp-item"><img src="/images/gallery-3.webp?v=2" alt="Пара у Хроники Грузии" loading="lazy" width="400" height="533" style="width:100%;height:100%;object-fit:cover;display:block"></div>
<div class="gp-item"><img src="/images/gallery-7.webp" alt="Гид Тимур с туристами" loading="lazy" width="400" height="533" style="width:100%;height:100%;object-fit:cover;display:block"></div>
<div class="gp-item"><img src="/images/gallery-10.webp" alt="Группа туристов на вершине Казбеги" loading="lazy" width="400" height="533" style="width:100%;height:100%;object-fit:cover;display:block"></div>
```

- [ ] **Step 2: Remove 9 video entries from gallery modal**

Remove these `.gm-item` divs containing `<video>` from the gallery modal (lines 1052-1068):
- gallery-17.webm (line 1052)
- gallery-18.webm (line 1053)
- gallery-19.webm (line 1054)
- gallery-24.webm (line 1059)
- gallery-26.webm (line 1061)
- gallery-27.webm (line 1062)
- gallery-28.webm (line 1063)
- gallery-30.webm (line 1065)
- gallery-33.webm (line 1068)

Delete each entire `<div class="gm-item"><video ...></video></div>` line.

- [ ] **Step 3: Verify predeploy**

```bash
node scripts/predeploy-check.js index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "gallery: replace preview videos with photos, remove modal videos"
```

---

### Task 6: Replace videos on 11 tour pages

**Files:**
- Modify: `tour/kazbegi/index.html`
- Modify: `tour/kakheti/index.html`
- Modify: `tour/kutaisi/index.html`
- Modify: `tour/batumi/index.html`
- Modify: `tour/borjomi/index.html`
- Modify: `tour/night-tbilisi/index.html`
- Modify: `tour/dinner/index.html`
- Modify: `tour/soviet/index.html`
- Modify: `tour/mtskheta/index.html`
- Modify: `tour/digital-nomad/index.html`
- Modify: `tour/slow-travel/index.html`

Each tour page has the same pattern — a `.page-hero-video` element with `<source>` and a small inline script. Replace with `<img>`.

- [ ] **Step 1: Replace video with img on each tour page**

For each tour page, find:

```html
  <video class="page-hero-video" autoplay muted loop playsinline preload="metadata" poster="/images/TOUR-tour.webp">
    <source src="/images/VIDEO.mp4?v=1" type="video/mp4">
  </video>
  <script>!function(){var v=document.querySelector('.page-hero-video');if(!v)return;v.addEventListener('playing',function(){},{ once:true })}()</script>
```

Replace with:

```html
  <img class="page-hero-video" src="/images/TOUR-tour.webp" alt="TOUR_ALT" width="1280" height="720" fetchpriority="high" style="width:100%;height:100%;object-fit:cover">
```

Tour-specific replacements:

| Tour | poster → src | alt |
|------|-------------|-----|
| kazbegi | kazbegi-tour.webp | Казбеги — Гергетская церковь |
| kakheti | kakheti-tour.webp | Кахетия — виноградники |
| kutaisi | kutaisi-tour.webp | Кутаиси — каньон Мартвили |
| batumi | batumi-tour.webp | Батуми — набережная |
| borjomi | borjomi-tour.webp | Боржоми — парк |
| night-tbilisi | night-tbilisi-tour.webp | Ночной Тбилиси |
| dinner | dinner-tour.webp | Грузинский ужин |
| soviet | soviet-tour.webp | Советский Тбилиси |
| mtskheta | mtskheta-tour.webp | Мцхета — Джвари |
| digital-nomad | digital-nomad-tour.webp | Тбилиси для номадов |
| slow-travel | slow-travel-tour.webp | Горы Грузии |

Keep the existing CSS class `.page-hero-video` — it has `position:absolute;inset:0;width:100%;height:100%;object-fit:cover` defined in each page's inline styles.

- [ ] **Step 2: Remove the inline video-playing script from each page**

Delete the `<script>!function(){var v=document.querySelector('.page-hero-video')...}</script>` from each tour page.

- [ ] **Step 3: Verify a sample page**

```bash
node scripts/predeploy-check.js tour/kazbegi/index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

- [ ] **Step 4: Commit**

```bash
git add tour/*/index.html
git commit -m "tour pages: replace 11 hero videos with static photos"
```

---

### Task 7: Enhance scroll reveal animations (Oura-style)

**Files:**
- Modify: `css/deferred.src.css:32-40` (existing `.reveal` styles)

- [ ] **Step 1: Update reveal CSS to add blur and increased translateY**

In `css/deferred.src.css`, find the existing reveal styles (lines 32-40) and update:

**FIND:**
```css
.reveal{opacity:0;transform:translateY(24px);transition:opacity .8s cubic-bezier(.22,1,.36,1),transform .8s cubic-bezier(.22,1,.36,1)}
.reveal.on{opacity:1;transform:translateY(0)}
```

**REPLACE WITH:**
```css
.reveal{opacity:0;transform:translateY(40px);filter:blur(3px);transition:opacity .9s cubic-bezier(.22,1,.36,1),transform .9s cubic-bezier(.22,1,.36,1),filter .9s cubic-bezier(.22,1,.36,1)}
.reveal.on{opacity:1;transform:translateY(0);filter:blur(0)}
```

- [ ] **Step 2: Add stagger delays for child elements**

Append after the reveal styles:

```css
.reveal>[data-anim-d="1"]{transition-delay:.1s}
.reveal>[data-anim-d="2"]{transition-delay:.2s}
.reveal>[data-anim-d="3"]{transition-delay:.3s}
.reveal>[data-anim-d="4"]{transition-delay:.4s}
```

Note: `data-anim-d` attributes already exist on elements in index.html.

- [ ] **Step 3: Add reduced-motion fallback**

```css
@media(prefers-reduced-motion:reduce){
  .reveal,.reveal-left,.reveal-right,.reveal-scale{opacity:1;transform:none;filter:none;transition:none}
}
```

- [ ] **Step 4: Disable blur on mobile (performance)**

```css
@media(max-width:768px){
  .reveal{filter:none;transform:translateY(24px)}
  .reveal.on{transform:translateY(0)}
}
```

- [ ] **Step 5: Increase section spacing for Oura-style breathing room**

In the section styles in `css/deferred.src.css`, find `.sec` padding and update:

**FIND:**
```css
.sec{padding:...
```

Update the padding-top and padding-bottom to `clamp(80px,10vw,120px)`.

- [ ] **Step 6: Rebuild CSS and commit**

```bash
cp css/deferred.src.css css/deferred.css
git add css/deferred.src.css css/deferred.css
git commit -m "reveal: Oura-style animations — blur, stagger, increased spacing"
```

---

### Task 8: Remove scroll-reveal-video dead code

**Files:**
- Modify: `css/deferred.src.css:47-60` (scroll-reveal-video styles)
- Modify: `index.html:1363+` (scroll-reveal-video JS)

The `.scroll-reveal-video` / `.reveal-wrapper` / `.reveal-video` CSS and JS is for video reveal that is no longer used.

- [ ] **Step 1: Check if scroll-reveal-video is used in HTML**

```bash
grep -n 'scroll-reveal-video\|reveal-wrapper\|reveal-video' index.html
```

If no HTML elements use these classes (only JS referencing them), they can be removed.

- [ ] **Step 2: Remove `.scroll-reveal-video` CSS from deferred.src.css**

Remove lines 47-60 (the `.reveal-wrapper`, `.reveal-video`, `.reveal-overlay`, `.scroll-reveal-video.is-fullscreen` rules).

- [ ] **Step 3: Remove the scroll-reveal-video JS from index.html**

Find the script at line 1363+ that references `.scroll-reveal-video` and remove it.

- [ ] **Step 4: Rebuild CSS and commit**

```bash
cp css/deferred.src.css css/deferred.css
git add index.html css/deferred.src.css css/deferred.css
git commit -m "cleanup: remove scroll-reveal-video dead code (CSS + JS)"
```

---

### Task 9: Audit and remove unused video files

**Files:**
- Delete: Multiple `.mp4` and `.webm` files from `/images/`

- [ ] **Step 1: Build list of all video files referenced anywhere on the site**

```bash
cd /Users/vladimir/sakhva-travel
grep -roh '/images/[^"]*\.\(mp4\|webm\)' index.html tour/*/index.html en/tour/*/index.html blog/*/index.html about/index.html en/index.html 2>/dev/null | sort -u
```

- [ ] **Step 2: Compare with all video files on disk**

```bash
cd /Users/vladimir/sakhva-travel
ls images/*.mp4 images/*.webm 2>/dev/null | sort > /tmp/all-videos.txt
```

- [ ] **Step 3: Identify files that are no longer referenced**

Compare the two lists. Any file on disk but NOT in grep output is safe to delete.

- [ ] **Step 4: Get user confirmation before deleting**

Print the list of files to delete and their total size. Wait for user confirmation.

```bash
# Example:
echo "Files to delete:"
cat /tmp/unused-videos.txt
echo "Total size:"
du -ch $(cat /tmp/unused-videos.txt) | tail -1
```

- [ ] **Step 5: Delete confirmed files and commit**

```bash
# Only after user confirms:
xargs rm < /tmp/unused-videos.txt
git add -u images/
git commit -m "cleanup: remove unused video files (-XXX MB)"
```

---

### Task 10: Final verification and deploy

**Files:**
- No new files

- [ ] **Step 1: Run predeploy check**

```bash
cd /Users/vladimir/sakhva-travel
node scripts/predeploy-check.js index.html index.html 2>&1 | grep -E "ошибок|ИТОГ"
```

- [ ] **Step 2: Check final HTML size**

```bash
wc -c index.html
```

Expected: significantly less than 265KB.

- [ ] **Step 3: Count remaining script tags**

```bash
grep -c '<script' index.html
```

Expected: fewer than original 22.

- [ ] **Step 4: Check images/ directory size**

```bash
du -sh images/
```

Expected: significantly less than 205MB.

- [ ] **Step 5: Local preview**

```bash
cd /Users/vladimir/sakhva-travel
python3 -m http.server 8765 &
```

Open http://localhost:8765 and verify:
- Hero loads with static photo + parallax effect on scroll
- Tour cards show photos instead of videos
- Gallery shows photos
- Scroll reveal animations work (fade + blur + stagger)
- Mobile: parallax disabled, reveal without blur
- All texts unchanged
- Navigation, FAB, modals work

- [ ] **Step 6: Deploy to Vercel**

```bash
cd /Users/vladimir/sakhva-travel
~/.npm-global/bin/vercel deploy --prod --yes 2>&1 | grep -E "Aliased|Error|error|Ready|Production"
```

- [ ] **Step 7: Verify production**

Open https://sakhva-travel.com and check:
- Hero photo loads fast (no video spinner)
- Parallax works on desktop
- All tour pages show photos
- Mobile works correctly

- [ ] **Step 8: Commit any final fixes**

```bash
git add -A
git commit -m "deploy: homepage lighten — videos removed, parallax + Oura reveal"
```
