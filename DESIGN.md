# Design System: Sakhva Travel

## 1. Visual Theme & Atmosphere

A warm, editorial-luxe travel interface with confident asymmetric layouts and fluid spring-physics motion. The atmosphere evokes a curated travel journal — intimate, unhurried, and tactile, like flipping through a beautifully bound guidebook in a Tbilisi wine bar. Georgian warmth meets European editorial restraint.

- **Density:** 4 — generous whitespace, gallery-airy sections
- **Variance:** 7 — offset asymmetric compositions, no centered hero
- **Motion:** 6 — fluid CSS with GSAP typewriter choreography, Lenis smooth scroll

---

## 2. Color Palette & Roles

### Primary Brand
- **Forest Depth** (#1A3D2E) — Primary CTA fill, nav active state, brand anchor. The soul of the palette
- **Forest Hover** (#143020) — Darkened CTA hover, pressed states
- **Sunset Terracotta** (#E8742A) — Single accent for section labels, visual punctuation, "how it works" hover glow. Saturation ~75%
- **Terracotta Hover** (#D4651F) — Darkened accent for interactive states

### Text Hierarchy
- **Deep Ink** (#111827) — Primary headings, hero text, high-contrast body
- **Warm Charcoal** (#374151) — Secondary body text, descriptions
- **Muted Stone** (#4B5563) — Tertiary text, metadata, timestamps
- **Faded Slate** (#6B7280) — Subdued labels, placeholders, disabled states

### Surfaces
- **Canvas White** (#FFFFFF) — Primary background, card fills
- **Warm Linen** (#FAFAF8) — Alternating section backgrounds, subtle warmth
- **Soft Bone** (#F9FAFB) — Card backgrounds when on white canvas
- **Pale Ash** (#F3F4F6) — Input backgrounds, badge fills, dividers

### Borders & Dividers
- **Whisper Gray** (#E5E7EB) — Standard card borders, structural lines
- **Warm Cream** (#E8E0D8) — Section dividers, footer border (warmer variant)
- **Sand Line** (#E0D8D0) — Decorative section separators

### Dark Surfaces (Hero, CTA, Ticker)
- **Night Sky** (#0A1628) — Hero video fallback, deep dark surface
- **Steel Dark** (#1F2937) — CTA sections, dark feature blocks
- **Ink Bar** (#111827) — Ticker background, trust bar

### Functional
- **Amber Star** (#F59E0B) — Rating stars, logo sun element
- **WhatsApp Mint** (#25D366) — WhatsApp CTA, scroll progress gradient end
- **Telegram Sky** (#229ED9) — Telegram button
- **Alert Crimson** (#DC2626) — Error states, destructive actions
- **Success Emerald** (#16A34A) — Confirmation, positive feedback

### Banned
- Pure black (#000000) — always use Deep Ink or Night Sky
- Purple/neon anything — no AI purple, no glowing gradients
- Saturated blues — not a tech product, keep warm

---

## 3. Typography Rules

### Display / Headlines
- **Font:** `Lora` (serif) — editorial warmth, literary character
- **Weight:** 400 (light elegance, not bold shouting)
- **Letter-spacing:** -0.02em (track-tight for intimacy)
- **Scale:** `clamp(26px, 4vw, 52px)` for h1, `clamp(28px, 3.8vw, 48px)` for h2
- **Line-height:** 1.15 for headlines

### Body / UI
- **Font:** `Raleway` (sans-serif) — clean, geometric, pairs well with Lora
- **Weight:** 400 body, 500 labels, 600 nav/micro
- **Size:** 16px base, line-height 1.7 for body text
- **Max-width:** 65ch for readable body paragraphs

### Section Labels
- **Font:** Raleway
- **Size:** 0.6875rem (11px)
- **Weight:** 500
- **Letter-spacing:** 0.15em
- **Transform:** uppercase
- **Color:** Sunset Terracotta (#E8742A) — visual accent marker

### Mono / Data
- **Font:** System monospace (for counters, stats, timestamps)
- **Use:** Hero counter animations, pricing numbers

### Banned
- `Inter` — generic, overused
- `Times New Roman`, `Georgia`, `Garamond` — generic serifs
- `Montserrat` as primary — only as Lora fallback
- Bold (700+) on Lora headings — weight 400 maximum for editorial feel
- Font sizes below 11px anywhere

---

## 4. Component Stylings

### Buttons
- **Primary (Forest):** Background Forest Depth, white text, border-radius 9999px (pill), shadow `0 2px 8px rgba(26,61,46,.25)`. Hover: darken to #143020, shadow `0 4px 14px rgba(26,61,46,.35)`, translateY(-1px). Active: translateY(0), shadow contracts
- **Ghost/Outline (Hero):** Transparent fill, 1px white border, white text, pill radius. Hover: white fill, Forest text
- **CTA Green:** Same as primary with larger padding. No outer glow ever
- **Disabled:** Pale Ash background, Faded Slate text, no shadow, no hover

### Cards (Tour Cards)
- **Shape:** 16px radius top (image), 16px radius bottom (body). No full-card radius
- **Shadow:** None at rest. Hover: `0 8px 24px rgba(0,0,0,.08)`, translateY(-4px)
- **Border:** 1px Whisper Gray
- **Image:** Aspect-ratio constrained, `object-fit: cover`, 0.7s ease zoom on hover (scale 1.05)
- **Padding:** 20px 20px 22px body area

### Section Structure
- **Label:** Uppercase, Terracotta, 0.15em tracking — acts as eyebrow
- **Title:** Lora 400, Deep Ink, tight tracking
- **Subtitle:** Raleway 400, Warm Charcoal, line-height 1.7
- **Head margin-bottom:** 48px desktop, 16px mobile

### Inputs / Forms
- **Style:** Label above input, Pale Ash background, Whisper Gray border
- **Focus:** Border transitions to Forest Depth, subtle ring
- **Error:** Alert Crimson text below, border turns crimson
- **Radius:** 8-10px (not pill — pills are for buttons only)

### FAQ Accordion
- **Toggle:** Max-height transition 0.38s ease
- **Icon:** Rotate 0.3s on expand
- **Border:** Bottom border Whisper Gray between items
- **No card wrapper** — flat list with dividers

### Loading States
- **Skeleton:** Pale Ash blocks matching layout dimensions, subtle shimmer
- **No circular spinners** — skeletal loaders only

### Trust Elements
- **Star rating:** Amber Star (#F59E0B), inline with count
- **Badges:** 10px radius, light background, subtle border
- **Counter animation:** 1600ms easeInQuad rAF loop on scroll intersection

---

## 5. Layout Principles

### Grid Architecture
- **Container:** `max-width: 1100px`, centered with auto margins
- **Section padding:** `clamp(56px, 7vw, 96px)` vertical, `clamp(16px, 3.5vw, 56px)` horizontal
- **Section-to-section gap:** 64px top padding between consecutive sections
- **Tour grid:** CSS Grid, 28px gap, responsive columns

### Hero Section
- **Full viewport:** `min-h-[100dvh]`, never `h-screen`
- **Structure:** Split/asymmetric — video background with overlay gradient, left-aligned or offset text
- **Overlay:** Multi-stop gradient `rgba(0,0,0,.18)` top to `rgba(0,0,0,.42)` bottom
- **Stats bar:** Absolute bottom, gradient backdrop, 4 metric columns
- **No centered layouts** — text left-aligned or offset asymmetric
- **Maximum 1 CTA button** in hero. No "Learn more" secondary links

### Content Sections
- **Alternating backgrounds:** White and Warm Linen (#FAFAF8) for visual rhythm
- **2-column zig-zag** preferred over 3-column equal grids
- **Cards only when elevation communicates hierarchy** — otherwise use border-top dividers
- **Generous section head spacing:** 48px below section header

### Banned Layout Patterns
- Centered hero layouts
- 3 equal cards in a horizontal row
- `calc()` percentage hacks — use CSS Grid
- Overlapping elements, absolute-positioned stacking
- `h-screen` (iOS Safari viewport jump)

---

## 6. Responsive Rules

### Mobile-First Collapse (< 768px)
- All multi-column layouts collapse to single column
- Hero animations disabled: `animation: none !important`, `opacity: 1 !important`
- GSAP typewriter skipped entirely (text shown immediately)
- Section padding reduces: `clamp(36px, 5vw, 64px)` vertical
- Section head margin: 16px (vs 48px desktop)
- Navigation collapses to hamburger menu

### Typography Scaling
- Headlines: `clamp()` functions ensure smooth scaling
- Body text minimum: 16px (never below)
- Nav links: 12px, uppercase, 0.12em tracking

### Touch & Interaction
- All interactive elements: minimum 44px tap target
- No hover-dependent content reveals on mobile
- Parallax disabled on mobile (scroll performance)
- Smooth scroll touch disabled: `smoothTouch: false`

### Horizontal Overflow
- Horizontal scroll on mobile is a critical failure
- Tour carousel uses horizontal scroll with snap points (intentional, controlled)

---

## 7. Motion & Interaction

### Lenis Smooth Scroll
- **Duration:** 1.4s
- **Easing:** Custom exponential decay `1.001 - Math.pow(2, -10 * t)`
- **Lerp:** 0.1 (smooth, weighty feel)
- **Wheel multiplier:** 0.7 (deliberate, not frantic)
- **Touch:** Disabled (native scroll on mobile)
- **Anchor offset:** -80px (nav clearance), 1.4s duration

### GSAP Typewriter (Hero H1, Desktop Only)
- Split text into `<span class="typewriter-char">` per character
- Words wrapped in `display:inline-block; white-space:nowrap`
- Reveal: `clipPath: inset(0 100% 0 0)` to `inset(0 0% 0 0)`
- Duration: 0.03s per char, stagger 0.045s, ease: none, delay: 0.3s
- Cursor blink: `0.8s step-end infinite`, fades out after 1.5s
- Fallback: `.no-gsap` class after 2s timeout shows text immediately

### Section Stagger Reveal (GSAP)
- Children fade: `opacity:0, y:20` to `opacity:1, y:0`
- Duration: 0.8s, stagger: 0.12s, ease: `power2.out`
- Triggered by IntersectionObserver at threshold 0.15

### CSS Scroll Reveal
- **Default:** `translateY(24px)` to origin, `opacity 0` to `1`
- **Left variant:** `translateX(-40px)`
- **Right variant:** `translateX(40px)`
- **Scale variant:** `scale(0.92)`
- **Easing:** `cubic-bezier(.22,1,.36,1)` — smooth deceleration
- **Duration:** 0.8s
- **Stagger nth-child delays:** +0.1s per item (max ~0.48s for 7th)
- **Trigger:** IntersectionObserver, threshold 0.05, rootMargin `0px 0px 60px 0px`

### Hero Entrance Cascade (CSS)
- Elements stagger from 0.5s to 0.9s delay
- Duration: 0.9s per element
- Easing: `cubic-bezier(.22,1,.36,1)`
- Order: subtitle (0.5s) → bullets (0.6s) → buttons (0.7s) → micro (0.8s) → stats (0.9s)

### Animated Underlines (Aker-Style)
- `::after` pseudo-element, height 1px
- `width: 0` to `width: 100%` on hover
- Duration: 0.3s ease-in-out
- Applied to: nav links, footer links

### Perpetual Micro-Interactions
- **Urgency dot:** Blink animation 1.4s ease-in-out infinite (opacity 1 → 0.25 → 1)
- **FAB pulse:** Box-shadow ring expansion 2s infinite
- **Ticker scroll:** Infinite horizontal translate3d loop
- **Cursor blink:** 0.8s step-end infinite on typewriter cursor

### Parallax
- Hero background: `translateY(scrollY * 0.35px)` on desktop only
- Stops after scrollY > 900px (performance guard)
- GPU-accelerated via translate3d

### Grain Texture
- Fixed-position SVG noise overlay
- `feTurbulence` fractalNoise, baseFrequency 0.65, 5 octaves
- Opacity: 0.045
- Pointer-events: none, z-index: 9999
- Static (no animation) — subtle paper texture feel

### Transition Timing Reference
| Element | Duration | Easing |
|---------|----------|--------|
| Background/color | 0.2s | ease |
| Transform hover lift | 0.15s | ease |
| Box-shadow | 0.15-0.25s | ease |
| Underline width | 0.3s | ease-in-out |
| FAQ max-height | 0.38s | ease |
| Tour image zoom | 0.7s | ease |
| Guide image slow zoom | 8s | ease (hover) |
| Nav bg transition | 0.3s | ease |
| Cookie bar slide | 0.4s | cubic-bezier(.22,1,.36,1) |
| Page entrance | 0.4s | ease |

### Performance Rules
- Animate only `transform` and `opacity` — never `top`, `left`, `width`, `height`
- Grain overlay on fixed pseudo-element, pointer-events none
- Parallax GPU-accelerated via translate3d
- Mobile: all hero animations disabled for performance
- IntersectionObserver for lazy triggering, not scroll listeners

---

## 8. Anti-Patterns (Banned)

### Typography
- No `Inter` font anywhere
- No generic serifs (`Times New Roman`, `Georgia`, `Garamond`)
- No Lora weight above 400 for headings (editorial, not corporate)
- No font sizes below 11px

### Color
- No pure black (#000000) — use Deep Ink (#111827) or Night Sky (#0A1628)
- No neon/outer glow shadows
- No purple/blue AI aesthetic
- No oversaturated accents (keep below 80% saturation)
- No gradient text on large headers
- No warm/cool gray fluctuation — stick to warm neutrals

### Layout
- No centered hero sections — asymmetric or left-aligned only
- No 3-column equal card grids — use 2-column zig-zag or asymmetric
- No overlapping elements — clean spatial separation always
- No `h-screen` — use `min-h-[100dvh]`
- No `calc()` percentage hacks — CSS Grid only
- No horizontal overflow on mobile (critical failure)

### Content
- No emojis
- No generic placeholder names ("John Doe", "Acme Corp")
- No fake round numbers ("99.99%", "50%")
- No AI copywriting cliches ("Elevate", "Seamless", "Unleash", "Next-Gen", "Curated Experience")
- No filler UI text: "Scroll to explore", "Swipe down", scroll arrows, bouncing chevrons
- No broken Unsplash links — use `picsum.photos` or real photography

### Interaction
- No custom mouse cursors
- No circular loading spinners — skeletal loaders only
- No hover-dependent content on mobile
- No `preventDefault` on wheel events
- No linear easing — use cubic-bezier or spring physics

### Technical
- No `animation` on mobile hero elements — force `opacity:1`
- No scroll listeners for reveal — use IntersectionObserver
- No animated grain overlay (static only, performance)
- No floating labels in forms — label above, always visible
