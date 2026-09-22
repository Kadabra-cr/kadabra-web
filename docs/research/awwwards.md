# Award-site research for kadabra hero/motion direction

## 1. multiverse.io hero (plain English)

The hero centers two short stacked headlines ("Upskill your team." / "Accelerate AI adoption.") plus a one-line supporting tagline, all center-aligned in the viewport — no left-aligned marketing block. Flanking the centered text, at the left and right edges of the hero, sit two symmetrical decorative SVG illustrations (`hero-creative-left.svg` / `hero-creative-right.svg`) that frame the copy rather than compete with it — this is the "flanking elements" effect the founder referenced. Below the tagline sits a single centered "Contact sales" CTA button, keeping the whole composition on one vertical axis. I could not reach the actual CSS/JS bundle (fetch only returns rendered markup, no stylesheet/animation source), so I cannot confirm real entrance durations or easing — treat any "slides in from the edges" description as inferred from asset naming/positioning, not verified motion code. Mobile behavior is likewise not visible in markup; it's presumably handled by media queries that stack or hide the side SVGs, but this is unconfirmed.

## 2. Relevant award-winning sites (last ~24 months, opened where possible)

| Site | Award | Why it's award-worthy | Pattern kadabra could adapt | What NOT to copy |
|---|---|---|---|---|
| [State of AI 2025 (Vention)](https://www.awwwards.com/sites/state-of-ai-2025) | Awwwards Honorable Mention | Lime-green (#CAF35A) on deep purple (#39175B), horizontal-scroll timeline turns a data report into an "immersive experience," 9.5+ jury scores | Treat stats as a scroll-driven narrative (horizontal timeline) instead of a static grid; high-contrast accent-on-dark-field palette formula | Full horizontal-scroll hijack is heavy UX risk for a marketing site — use sparingly, one section max |
| [Axelar network (dot matrix)](https://www.awwwards.com/inspiration/interactive-dot-matrix-animations-axelar) | Featured Awwwards element (Digital Panda) | WebGL + Lottie dot matrix that reacts to mouse, sophisticated but not gimmicky | Background field of small reactive glyphs/tiles for hero or section dividers | Don't over-animate — Axelar keeps it subtle behind foreground copy |
| [Microsoft AI](https://www.awwwards.com/sites/microsoft-ai) | Awwwards SOTD | Restrained 2-color palette (cream/warm brown), WebGL, scored 8.0/10 dev on animation smoothness — "grounded in warmth, trust, humanity" | Minimal 2-color discipline + smooth, non-mechanical transitions as the whole design system | Palette itself (warm neutrals) isn't kadabra's — don't borrow the colors, borrow the restraint |
| [GitHub Universe '24](https://www.awwwards.com/sites/github-universe-24) | Awwwards Honorable Mention | Neon green (#6EF08E) on white, video hero, WebGL/3D, celebratory event narrative over raw stats | High-contrast single accent green on a light/dark field for CTAs and highlights | Video-heavy hero is expensive to produce/maintain for a small studio site |
| [Artlist Trend Report 2025](https://www.awwwards.com/sites/artlist-trend-report-2025) | Awwwards Honorable Mention | Magazine-style scroll-triggered layout, yellow accent (#FFDA2A) drives hierarchy, "visual compass" narrative framing | Section-to-section scroll transitions that feel like page turns, curated "journey" structure for workshop offerings | Yellow accent and magazine density don't fit kadabra's carbon/felt-green reading areas |
| [Living Canvas](https://www.awwwards.com/sites/living-canvas) | Awwwards Honorable Mention | WebGL background that reacts to real-world data (weather/time) as well as mouse, purple/yellow duo | Idea of a background that's "alive" and contextual, not just decorative — could tie to workshop schedule/CR time-of-day | Full real-time-data WebGL scene is overkill for a marketing site; scope down to a lightweight canvas |
| [Won J. You Studios](https://www.awwwards.com/sites/won-j-you-studios-2) | Awwwards SOTD (Oct 2025) | Closest positioning match: design-coaching/mentorship studio (B2B education), 2-color bold palette, GSAP scroll storytelling, 8.4/10 on animations | Scroll-driven "our mission changed" narrative structure for an about/manifesto page; confident 2-color minimalism | Palette is coral-red/cream, not green — and it's motion-heavy/video-led, more agency-flashy than the "professional gamified" tone kadabra wants |
| [Vertex3D](https://www.awwwards.com/sites/vertex3d) | Awwwards Honorable Mention | Spatial Web/Enterprise UX studio, WebGL portfolio with live AI hand/head tracking | Shows a B2B/enterprise-serious brand can still use playful WebGL interaction without reading as a game | The live AI tracking gimmick is far beyond scope needed here |
| [Awwwards green collection](https://www.awwwards.com/websites/green/) | Mixed (mostly 2022, dated) | Useful as a palette-adjacent reference set, but entries are largely outside the 24-month window | General green-on-dark visual grammar cues only | Don't treat as "recent" — most entries are 2022, noted here for transparency rather than as a strong recommendation |

Note: I could not find an awwwards/cssdesignawards/godly site in the last 24 months combining dark-green palette + centered display type + workshop/education positioning as a single close match — Won J. You Studios is the closest on positioning/motion, State of AI 2025 the closest on palette-contrast-and-storytelling. Treat the table as a composite reference set, not one perfect analog.

## 3. Big-statistic / contrast-number storytelling sections

| Example | Composition |
|---|---|
| State of AI 2025 (Vention) | Numbers appear inline within a horizontal-scroll timeline of AI trends — each stat is anchored to a year/moment and a short causal caption, not listed in a grid; scroll = time = argument |
| GitHub Universe '24 | Explicitly avoids a stats grid — leads with narrative ("10 years, fun, food, connection") and folds any numbers into that emotional arc rather than isolating them |
| Artlist Trend Report 2025 | Numbers/data points are embedded in a magazine-style scroll journey (trend → example → takeaway), each section a "spread" rather than a tile |
| General pattern (from case-study research, not a single site) | Cause → effect → so-what structure: large number callout (e.g. "20+", "32 hours") paired immediately with the human/business consequence sentence beneath it, not a bank of unrelated KPIs |

Kadabra takeaway: avoid a 4-up stat-tile grid; instead pick 2–3 numbers max, each with its own scroll beat and one-line "so what" (e.g., workshop hours saved → teams shipped → so what for the client).

## 4. Mouse-reactive background fields of small shapes

| Example | Technique |
|---|---|
| Axelar network dot matrix | WebGL + Lottie; dots form a matrix that reacts to pointer proximity, sits behind foreground content, subtle rather than dominant |
| Living Canvas | WebGL canvas; background shapes/particles respond to both mouse and external context (weather/time), showing the same reactive-field idea can be data-driven, not just cursor-driven |
| Generic reference (codepen/playground, not an award site) | Canvas 2D dot grid where dots "breathe" and refract/displace away from the pointer — cited by search as a common lightweight technique (no WebGL needed) if kadabra wants a cheaper build than Axelar's stack |

Kadabra takeaway: WebGL (via a library like OGL/Three.js) gives the polished Axelar-level result; a plain Canvas2D dot-grid with pointer-distance displacement is the low-cost fallback and still reads as "professional gamified" if damped/smoothed rather than snappy.
