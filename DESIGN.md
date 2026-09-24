# Design System — Sakhva Travel

## Product Context
- **What this is:** Private tour guide service in Tbilisi, Georgia (sakhva-travel.com)
- **Who it's for:** Russian-speaking relocants in Tbilisi, tourists, English-speaking travelers
- **Space/industry:** Travel, boutique tour guide, Georgia tourism
- **Project type:** Marketing site + booking (static HTML, no framework)

## Aesthetic Direction
- **Direction:** Luxury/Refined with editorial touches
- **Decoration level:** Intentional (grain texture, backdrop blur, subtle shadows)
- **Mood:** Premium but approachable. Forest green = trust, gold = warmth. Not corporate, not casual
- **Reference:** Aker Companies design language (dark body, white section "rooms", monumental spacing)

## Typography
- **Display/Hero/Body:** Lora (Georgia serif fallback) — warm editorial serif, conveys heritage and trust
- **UI/Labels:** Lora — unified type system, differentiated by weight and letter-spacing
- **Logo:** Raleway (SVG embedded)
- **Code/Data:** Not applicable (no code blocks on site)
- **Loading:** Self-hosted woff2 (`/fonts/`), `font-display: optional` to prevent CLS
- **Scale:**
  - Hero H1: clamp(26px, 4vw, 52px), weight 700, tracking -0.01em
  - Section title: clamp(26px, 3.2vw, 38px), weight 500, line-height 1.18
  - Section label: 13px, weight 500, tracking 0.2em, uppercase
  - Body: 16-17px, weight 400, line-height 1.7
  - Small/Caption: 12-13px
  - Nav links: 13px, weight 700, tracking 0.1em, uppercase

## Color

### Brand
- **Primary green:** #1A3D2E — nav, buttons, CTA, trust
- **Accent gold:** #F59E0B — headings, highlights, badges, urgency
- **Orange accent:** #e8742a — section labels (Aker), scroll progress bar

### Text
- **Heading:** #111827 (near-black)
- **Body:** #111827
- **Muted:** #4B5563
- **Light muted:** #6B7280
- **On dark:** #fff, rgba(255,255,255,.7-.9)

### Surfaces
- **Page background:** #fff
- **Alt section:** #F9F8F8
- **Card background:** #fff
- **Dark hero/footer:** #0a1628
- **Nav default:** rgba(0,0,0,.35) transparent
- **Nav scrolled:** #1A3D2E solid
- **Input/subtle:** #F9FAFB
- **Border:** #E5E7EB, #D1D5DB

### Semantic
- **Success:** #16A34A (badges), #25D366 (WhatsApp CTA)
- **Warning:** #F59E0B (same as accent gold)
- **Error:** #DC2626
- **Info:** #93C5FD
- **Discount badge:** #DC2626 (red) or #F59E0B (gold)

### Dark mode
Not implemented. Hero section and tours carousel use dark overlays on video/images.

## Spacing
- **Base unit:** 4px
- **Density:** Comfortable (marketing site, generous whitespace)
- **Horizontal padding:** clamp(16px, 3.5vw, 56px)
- **Section vertical:** clamp(36px, 5vw, 64px) top/bottom (seamless.css)
- **Mobile section vertical:** clamp(28px, 5vw, 48px)
- **Content max-width:** 1100px (.si container)
- **Wide content:** 1200px (tours grid, filters)
- **Gallery max-width:** 1280px
- **Nav height:** 72px fixed
- **Scale:** 2px / 4px / 8px / 12px / 16px / 20px / 24px / 28px / 32px / 48px / 64px / 96px

## Layout
- **Approach:** Grid-disciplined (CSS Grid + Flexbox, no creative-editorial)
- **Grid columns:**
  - Desktop: 3-4 columns (tours: 3, tour grid: 4, gallery: 4)
  - Tablet (<=1024px): 3 columns
  - Mobile (<=768px): 1-2 columns
  - Small mobile (<=480px): 2 columns (compact cards)
- **Max content width:** 1100px
- **Border radius:**
  - xs: 6px (small badges, pills)
  - sm: 8px (inputs, filter buttons, small cards)
  - md: 10-12px (cards, dropdowns, FAQ items)
  - lg: 14-16px (tour cards, sections, large cards)
  - full: 9999px (buttons, nav CTA, cookie buttons, trust badge)

## Motion
- **Approach:** Intentional (entrance animations, scroll reveals, hover states)
- **Easing curves (Aker tokens):**
  - Smooth: cubic-bezier(0.165, 0.84, 0.44, 1) — fades, nav transitions
  - Heavy: cubic-bezier(0.19, 1, 0.22, 1) — dramatic reveals
  - Subtle: cubic-bezier(0.455, 0.03, 0.515, 0.955) — radius morph
  - Main: cubic-bezier(0.22, 1, 0.36, 1) — default for most animations
- **Durations:**
  - Micro: 150ms (hover color, border-color)
  - Short: 200-300ms (nav background, button hover, filter transitions)
  - Medium: 400-700ms (reveal animations, opacity transitions)
  - Long: 800-1200ms (scroll reveals, hero animations, divider width)
- **Scroll reveal:** `.reveal` class — opacity 0 to 1, translateY(24px) to 0, blur(4px) to none
- **Data animations:** `[data-anim]` system — up/down/left/right/scale/fade/lines/clip variants
- **Mobile:** Hero animations disabled on <=768px (opacity:1, animation:none, transform:none)
- **Reduced motion:** All transitions disabled via `prefers-reduced-motion: reduce`

## Components (key patterns)

### Buttons
- **Primary CTA:** bg #1A3D2E, text #fff, radius 9999px, shadow 0 4px 14px rgba(26,61,46,.35)
- **WhatsApp CTA:** bg #25D366, text #fff, radius 9999px, shadow gold-tinted
- **Telegram CTA:** bg #229ED9, text #fff, radius 9999px
- **Outline hero:** transparent bg, 1.5px border rgba(255,255,255,.7), radius 9999px
- **Filter button:** bg #fff, 1px border #D1D5DB, radius 8px

### Cards
- **Tour card (carousel):** radius 16px, bg #111, height 520px (desktop) / 700px (mobile), video background
- **Tour card (grid):** radius 12px, bg #fff, border 1px #E5E7EB, aspect-ratio 3/2 image
- **HP card (catalog):** radius 12px, border 1px #F3F4F6, bg #fff, 200px image height

### Nav
- **Fixed top:** height 72px, z-index 900
- **Default:** transparent with backdrop rgba(0,0,0,.35)
- **Scrolled:** solid #1A3D2E with box-shadow
- **Mobile:** burger menu + drawer (white bg, full-screen)

### Cookie bar
- **Fixed bottom:** z-index 9999, bg rgba(15,17,26,.95) + backdrop-blur(12px)
- **Slide up:** transform translateY animation

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04 | Lora as sole typeface | Warm editorial serif fits premium travel brand. Unified type system = fewer font requests |
| 2026-04 | #1A3D2E + #F59E0B palette | Forest green = Georgia/nature/trust. Gold = warmth/premium. High contrast pair |
| 2026-04 | Aker design language | Monumental spacing, dark/light section rhythm, editorial feel |
| 2026-04 | font-display: optional | Prevents CLS from font swapping. Acceptable tradeoff: rare fallback on slow connections |
| 2026-05 | Seamless.css spacing overrides | Unified section spacing via external CSS for consistency across all pages |
| 2026-06 | CSS files made blocking | Deferred loading caused CLS 0.359. Blocking load eliminates layout shifts |
| 2026-06 | DESIGN.md created | Formalize existing design system for consistency across 266 pages |
