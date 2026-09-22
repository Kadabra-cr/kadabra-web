# mistral.ai — animation & visual system

## Stack and libraries
- **Astro** (static, `/_astro/*` hashed assets), deployed on **Netlify**; 475 KB HTML, no React/Next island hydration.
- **Custom elements, not a framework**: every section is a `<mistral-section-*>` / `<mistral-block-*>` / `<mistral-atom-*>` web component (23 tags on the homepage), each hydrating itself.
- **Tailwind v4** for all styling; motion exposed as `--animate-*` theme tokens → `animate-*` utilities.
- **GSAP** + **ScrollTrigger** + **SplitText** + **Flip** + **Observer** + **ScrollSmoother** — one 1 MB `layout.*.js` bundle.
- **Lenis** smooth scroll; **Swiper** for carousels; **dotLottie** (WASM, `/dotlottie-player.wasm`) rendering `.lottie` files to `<canvas>`.
- **three.js** is in the bundle (WebGLRenderer, ShaderMaterial, InstancedMesh) but **no WebGL canvas runs on the homepage** — 1 canvas total, and it's the Lottie.
- Astro View Transitions (`astroFadeIn/Out`, `astroSlideFrom*`) for page-to-page.

## Palette
Brand orange `#ff5229` / `#fa500f` / `#ff6529`, deep red `#e51300` / `#c4001d`, amber `#ffaf01` / `#fec63a`, blue `#0082e6` / `#55b3fb` / `#b9daff` / `#044298`, green `#44ba82`, pink `#ff92dc`.
Neutrals are warm, not grey: cream surfaces `#fbfbf8`, `#f5f4ef`, `#ebe9e0`, `#fafaf4`; borders `#e4e3de`. Dark mode flips to navy-black `#151524`, `#242433`, borders `#31313a`. Texture: tiled `noise-rectangle.png` over flat fills.

## Fonts
`ALTMistral` (custom grotesk, Regular/Medium/Semibold + italics, self-hosted woff2) for display and body; `Space Mono` for all uppercase micro-labels ("FEATURED NEWS", "AGENT ORCHESTRATION"); `Inter` variable as fallback UI.

## Section-by-section (11,630 px page)
**1. Nav** — flat bar, hairline-divided cells, pixel-art "M" logo.
Hover slides an arrow `translate-x-6…20` with `delay-75/100` so icon leads label; dropdown panel slides `-translate-y-10 → 0`.
Grid-of-cells + a single moving arrow reads as a machine UI, not a marketing nav.

**2. Hero** — "Frontier AI. In your hands.", 200 dvh tall with a `sticky top-0` inner; right rail holds the sub-headline, a triple fading down-arrow, and a "Featured news" card. Lower half is a full-bleed pixel grid of orange/red squares with a tiny pixel-art black cat.
GSAP `SplitText` into lines/words/chars; chars `y:100% → 0%` (some to `-50%`), `duration 1s, ease power4.inOut`, per-char stagger `randInt(1,5) × .005s`, lines offset `0.7s × index`, and line boxes grow `height:0 → auto`. The grid below is a **dotLottie on canvas**, autoplay+loop. The whole sticky block is scrubbed by a ScrollTrigger `start:top end:bottom scrub:true` over the 2-viewport section.
Randomised per-char stagger makes the type feel typed rather than animated; pinning for 2 viewports buys time for the loop to read as a world, not a decoration.

**3. Featured-news carousel** — one headline card with thumbnail, auto-advancing.
`<mistral-atom-progressbar data-variant=horizontal>` is a 4 px amber `#ffaf01` bar animating `width 0→100%` (`will-change-width`) as the timer for the swap; Swiper `loop:true`, `speed:1500`.
The progress bar turns an autoplay carousel into something legible and interruptible.

**4. Logo wall** — enterprise logos (HSBC, IBM, SAP, ASML, Cisco…), black/white pairs for theme swap.
`mistral-block-slider-infinite-scrolling`: continuous marquee, `linear`, plus `hover:grayscale-0` per logo.
Constant linear drift at low contrast, colour only on hover — reads as a background fact, not a claim.

**5. Customer story cards** — industry-tagged cards (HSBC, ASML, CMA CGM) with dot navigation.
Horizontal slider, `animate-dot-lane` (1.6 s linear infinite, opacity .1→1→.1) on the dots; card copy slides on `translate` under `group-hover`.
Same ambient blink vocabulary as the terminal micro-labels ties nav dots to the brand.

**6. "Do it all with Mistral." — markitecture bento** — product tiles (Vibe, Vibe Code, Studio, Forge, Compute, Applied AI) assembling into an isometric-ish grid.
Blocks drop in with `markitecture-fall` / `bento-fall`: `translateY(-300px) → 0` then `scaleY .95 → 1.02 → 1` squash-and-stretch, `.5s ease-in forwards`, fired on scroll, staggered; rotated pieces use `scale(0)→1` instead.
The squash frame gives cheap physical weight and makes an abstract diagram feel built.

**7. Product detail sections** (×6, sticky left icon rail) — each: heading, paragraph, a full-width coloured pixel-grid panel with a floating UI mock, then a row of mono-caps feature tags.
Panel backgrounds are the same pixel-tile system recoloured per product (blue for Studio, cream for Applied AI); cards use `reveal-post-left/right` clip-path wipes (`1s cubic-bezier(.51,-.01,.49,1)`) and the OCR demo runs a pure-CSS 4 s scanner loop (sweeping bar + 5 text blocks fading in 5 % apart). Left rail icons highlight via ScrollTrigger.
One recoloured motif carries six sections, so variety comes from hue, not from new ideas.

**8. "Supported by expert partnership."** — 4 playable feature cards with per-card progress bars.
`data-playable` slideshow: each card's bar fills, then advances; pixel-art SVG icons sit above.

**9. Deployment cards + footer** — self-hosted/cloud cards, then a huge pixel "M" over a hot orange-to-crimson gradient band with the pixel cat sitting on it, plus theme + language switchers.
Footer band uses the slow `cover-gradient-*` loops (5/6/8/10 s, `linear`, deliberately non-harmonic periods) so it never visibly repeats.

## Recurring motion motifs
- **Squash-and-stretch drop-in** (`translateY(-300px)` → `scaleY .95/1.02/1`) for every block that "assembles".
- **Progress bars as timers** — amber `width 0→100%` on every autoplaying carousel.
- **Randomised per-char SplitText rise** with `power4.inOut` for all display headlines.
- **Ambient `linear` blinks/flickers** (`dot-lane`, `blink`, `logo-flicker`, chased arrows at 0/.2/.4 s delay) as idle-state texture.
- **Clip-path polygon wipes** rather than fades for card and image reveals.
- **Arrow-leads-label hover**: `group-hover:translate-x-*` with `delay-75/100` on ~200 links, the site's single unifying micro-interaction.
- **Pixel-art everywhere**: icons are SVGs built from 1.4 px `<rect>` grids, not raster sprites.

## Files saved
`home.html` (475 KB) · `astro.css` (177 KB) · `main.css` (12.6 KB) · `layout.js` (1.05 MB) ·
`css-notes.md` · `shots.mjs` · `home-full.png` · `home-1.png`…`home-5.png` ·
`assets/hero-mistral-ai-lottie-2.svg.lottie` (68 KB, hero animation) ·
`assets/robot.svg`, `assets/earth.svg`, `assets/icon-m-flower.svg` (vector pixel-art icons) ·
`assets/ai-app_LCReD.webp` · `assets/noise-rectangle.png` (texture tile).
