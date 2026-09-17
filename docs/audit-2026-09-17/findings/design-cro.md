# sakhva-travel.com — Design + CRO Audit (2026-09-17)

Scope: homepage (/), tour page (/ekskursiya/vinniy-marshrut-alazani/), /contacts/.
Desktop 1440x900, iPhone 13 (390x844). Cross-checked against ~/sakhva-travel/DESIGN.md.
Screenshots: scratchpad/sakhva-travel.com-audit/screenshots/design-*.png

## Scores
- **Design: 74/100** — clearly not generic-AI (serif Lora, forest green/gold, no purple gradients/glassmorphism), but execution has real bugs (watermark overlap, FAB stacking) and residual emoji-icon debt.
- **CRO: 78/100** — tour page hero and booking flow are near-best-practice for the niche; homepage hero and contacts page under-sell trust signals that exist elsewhere on the site.

## What works (keep, don't touch)
1. **Tour page hero is excellent**: price ("от ₾175"), duration, group size, departure time, free cancellation, rating "4.8/5 · ответ за 15 мин" and a green WhatsApp CTA all sit above the fold on both desktop and mobile (design-tour-desktop-top.png, design-tour-mobile-top.png). This is the "who/what/where/price/CTA in 5 seconds" bar done right — do not let a redesign regress this.
2. First-person guide copy with concrete numbers ("Рейтинг 4.9 на Google Maps, 156 отзывов", license number, response time) — strong E-E-A-T, matches DESIGN.md's "premium but approachable" intent.
3. Booking friction is low: WhatsApp number, deposit %, cancellation window spelled out in plain text on the tour page itself — no form, no multi-step funnel.
4. Comparison block "Автобус / Самостоятельно / С Тимуром" (design-home-desktop-mid.png) is a real differentiated layout, not a 3-equal-card generic pattern — good CRO device, keep.
5. Reviews cross-linked to Google/Яндекс/TripAdvisor with real aggregate "4.9 из 5 — более 90 отзывов" on /contacts/ (design-contacts-desktop-mid.png) — matches the honest-rating requirement.
6. Typography (Lora serif) and palette (#1A3D2E green / #F59E0B gold) are followed consistently across all 3 pages — no drift from DESIGN.md found.

## Findings by severity

### High
1. **Text overlap / watermark bug on tour page body copy (mobile).** In `design-tour-mobile-mid.png`, a decorative sun emoji/logo watermark renders on top of the H2 "Как проходит бронирование" and a "TRAVEL" wordmark strikes through the paragraph "Напишите мне в WhatsApp: +995 511 272 623...". This is a stacking/opacity bug, not decoration — it reduces legibility of the exact paragraph that contains the phone number and cancellation policy (the objection-handling copy). Fix: find the background/watermark element (likely a `.grain`/logo ::before layer per DESIGN.md's "grain texture, backdrop blur" direction) and add `pointer-events:none; z-index` below content, or scope it to hero-only sections instead of the full page flow.
2. **Floating "Play music" button overlaps content on mobile.** On `/contacts/` mobile (design-contacts-mobile-top.png) it sits directly over the WhatsApp card's "Звоните из России: +7 (928)..." line, clipping the text. On the tour page mobile it competes for the same bottom-left corner as the sticky WhatsApp CTA bar. Three floating elements (music toggle, chat FAB, sticky book bar) stack in the same viewport region — pick two max. Fix: either dock "Play music" into the hero (desktop only, since it's ambient hero-video audio) or drop it — it is not a conversion element and is actively colliding with ones that are.
3. **No guide photo anywhere audited.** DESIGN.md and the audit brief both call for guide photo + name as a trust signal. /contacts/ names "Тимур Сахвадзе" with license number but shows zero photo — only real Instagram feed thumbnails buried further down the homepage carry an actual face. Add a real photo of Timur next to the intro paragraph on /contacts/ and in the tour-page "Почему выбирают этот тур" block — this is the single missing trust signal on an otherwise trust-rich page.

### Medium
4. **Emoji icons on /contacts/ contact-method cards** (📱 ✈️ 📧, design-contacts-desktop-top.png) — reads as generic/AI-templated against an otherwise premium Lora/serif system. Replace with a matched-stroke icon set (the site already uses proper line icons for WhatsApp/Telegram/phone/mail in the footer — reuse those instead of emoji).
5. **Emoji icons in the homepage comparison table** (🚌 🏞️ 🤝, design-home-desktop-mid.png) — same fix, swap for line icons; keep the copy, which is genuinely good.
6. **Instagram section interrupts the conversion argument too early on mobile homepage.** It appears directly after the hero/map and before "Почему выбирают" (design-home-mobile-mid.png) — sending a still-undecided visitor to an external app before price/trust/booking argument is made. Move it lower (after reviews, before footer) or drop it from mobile entirely.
7. **Homepage hero (as served, en-US locale) shows no price and no rating**, unlike the tour page (design-home-desktop-top.png vs design-tour-desktop-top.png). "Free cancellation 24h · Reply in 15 min" is present but rating/price is not — homepage is the highest-traffic entry for cold visitors and currently undersells trust vs. the tour pages. Add the same "★ 4.9 · 90+ отзывов" line used on /contacts/ under the homepage hero CTA row.
8. **Google Maps embed rendered blank in headless check** on /contacts/ desktop (design-contacts-desktop-mid.png shows an empty grey box under "Тбилиси на карте"; mobile shows a lazy-load placeholder that never resolved in the same run). No console errors were thrown, so this may be a headless-only referrer/API-key restriction — verify manually in a real browser before treating as a live bug, but if it also fails for real visitors this is a broken trust element on the one page whose whole job is "where do I meet the guide."

### Low
9. Route map on tour page (design-tour-desktop-bottom.png) is a flat SVG line over a plain grey background with no real terrain/street context — functionally fine but visually the thinnest-looking module on an otherwise photo-rich page; a static map tile image behind the pins would lift it to the same quality bar as the rest of the page.
10. Cookie banner covers the primary CTA row on first paint on mobile (design-home-mobile-top.png: "Decline/Accept" sits right under "Contact me/Choose a tour"). Not blocking since it's dismissible, but on a 390px screen it doubles the number of buttons in the first viewport — consider a slimmer single-line cookie bar.

## Top 5 prioritized changes (expected impact)

1. **Fix the watermark/text-overlap bug on tour pages (mobile)** — Effort: S. Impact: removes a legibility defect sitting directly on the booking-policy paragraph on your highest-intent page type (tour pages drive direct bookings). Ship first, it's a bug, not a design opinion.
2. **Resolve the floating-button stacking (Play music vs sticky CTA vs chat FAB)** — Effort: S. Impact: stops the ambient-audio toggle from visually competing with/covering the WhatsApp CTA, which is your primary conversion path on mobile.
3. **Add guide photo to /contacts/ and tour pages** — Effort: S (one asset + one `<img>` per template). Impact: closes the one trust signal the audit brief explicitly flags as missing; pairs with the license number and rating you already show.
4. **Bring rating + price into the homepage hero** — Effort: S (copy/template change, data already exists in DESIGN.md/tour pages). Impact: homepage is cold-traffic entry; right now it undersells vs. tour pages that already convert well — matching that bar should lift homepage → tour-page click-through.
5. **Swap emoji icons for the site's existing line-icon set on /contacts/ and homepage comparison table** — Effort: S. Impact: removes the one "generic AI" tell on an otherwise differentiated, premium-feeling site; near-zero risk since the icon set to reuse already exists in the footer.
