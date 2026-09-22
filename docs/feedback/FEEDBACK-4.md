# Founder feedback on round 3 + direction for the REAL site (2026-09-22)

Overrides FEEDBACK-3.md, FEEDBACK.md, BRIEF.md where they conflict. Read PRODUCT.md and DESIGN.md too.
This round is not a mockup. It is the production site: robust, complete, professional, cutting edge.

## Verdict on round 3
Liked: margins, real logo in header, classic suits, hero field idea, 93%/9% pair, the swipe card design, why-us idea, the workshop as a vertical journey.
Missing overall: flavour, uniqueness, cutting edge. "Don't make it feel like just a landing page."

## 1. The chevron rule (HIGHEST PRIORITY, the wand is banned as a decoration)
- New asset: `kadabra/logo/kadabra-first-edition-chevron.svg` (viewBox 0 0 28 64). One chevron parallelogram.
- The wand SVG must NOT be used as an accent, divider, spine, or underline anywhere. Stretching it distorted it ("looks so bad").
- Instead: draw plain rules (bars) of the SAME thickness as the wand's bar (60 units tall in the wand SVG; on screen pick one thickness token, e.g. 10–14 px for spines/underlines, 4–6 px for small rules, chevron scaled proportionally, always 28:64 aspect).
- Cut the chevron OUT of the rule by subtraction (SVG `mask` or `clip-path` with the chevron path, or a CSS mask) so the arrows are printed into the line: one near the start, one further along, one near the end, like the original wand. This is how every brand rule is made from now on.
- Animate the chevrons ALONG the rule: they travel with scroll (timeline spine) or drift slowly (dividers), same thickness, never scaled non-uniformly. Vertical rules use the chevron rotated 90° pointing down.
- Be creative with it: chevrons can gather where the visitor is, spread out when idle, point toward the CTA.

## 2. Structure: three routes, not a landing page
- Header anchors that scroll the page are rejected ("unprofessional for a landing page").
- Routes: `/` Home (hero, numbers, swipe, why us, closing CTA), `/workshop` (the "AI without the smoke screen" journey), `/sources` (every citation).
- Header: logo (full lockup, links home) · The workshop · Sources · CTA "Talk to us on WhatsApp".
- Routing: client-side, no full reload. History API + `document.startViewTransition` where supported (fallback: a short crossfade-free wipe using the chevron/rule, under 500 ms, no opacity jump ≥0.15 per 50 ms). Direct URL hits must work on Cloudflare Pages: ship `index.html` plus `workshop/index.html` and `sources/index.html` (same shell, or a `_redirects` to `/index.html 200`). Back/forward must work. Scroll resets to top on route change. Titles update per route.
- Performance: one CSS file, one JS file, sprites inlined once, fonts preloaded, no framework, no build step required (a tiny build script is fine if it stays optional). Lighthouse-grade: no layout shift, images/svg sized.

## 3. Hero
- Pointer influence arrives too late / too weak. Make it immediate: a larger influence radius, squares nearest the pointer morph within ~120 ms, density can increase near the pointer (spawn extra squares into the pointer's neighbourhood, fade them in smoothly, never pop). It must feel like the pointer is doing magic, not that things react a second later.
- Keep: sparse drifting field, square → random classic suit → square, hold ~1.4 s, visible trail. Square→suit only.
- Glow: allow a soft glow on the MORPHED suit (never on idle squares). A bit flashier than round 3, still no cheap bloom.
- Steer the field AWAY from the text. Headline, sub, CTA sit in a "quiet zone": squares that drift into it are pushed out (soft repulsion field around the text block), so nothing overlaps the copy. Some squares may pass near the centre, but most live away from it. The hero must not be opaqued.
- Copy unchanged: "The trick is teaching, not tools." / sub / "Talk to us on WhatsApp" → `#TODO-whatsapp`.
- More interesting scroll effects across the page (parallax of the field, rules that draw as you pass, numbers that count once, suits that settle). Impeccable animate playbook: motion with a reason per section.

## 4. Numbers section (cream) — rebuilt
- Keep title "It works. Until it doesn't." and the 93% / 9% pair exactly as round 3 (adjacent, 9% on the dark panel). This part is liked.
- REMOVE 88% (McKinsey) and 95% (MIT NANDA). They "throw data at people".
- Replace the rest with ONE interactive graph: **47% of employees have ever received any AI training** (KPMG 2025) vs **beginners who are taught get up to 34% more done** (NBER 2023). Make it a visualization, not a number tile: e.g. a field of small squares standing for a team; 47% of them morph into suits (trained) as it enters the viewport; then the bar/lift of +34% draws for the trained group. Same morph dynamics as the hero, more glow allowed here. Interactive: hovering/scrubbing changes what is highlighted, a legend explains what each mark means. Citation lines aligned with the rest of the section (round 3's 34% citation was out of line: rejected).
- Closing line replaces "Nobody taught the team.": **Taught teams get more done.** Big, left-aligned like the rest of the page, underlined with the chevron rule (rule + subtracted chevrons, NOT the wand). Impactful.
- The story must connect: 93% get results → only 9% have rules → less than half were ever taught → the ones who are taught get more done → we teach.

## 5. Swipe "Can AI take this?" (felt)
- Card design is liked. Keep it.
- Guidance: the visitor lands and does not know what to do. Centre the section title and intro over the centred card. Show the gesture: on entry, if idle ~2 s, the top card nudges gently toward one side and back with a hint arrow (chevron) and labels "Best not" / "AI can take it" glowing on the side being nudged. Also show the keyboard hint (← →) on desktop. Buttons stay.
- Reveal ("Here's your desk.") is boring and the marks don't link: REBUILD. Requirements:
  - The two groups stay as vertical cards (small) and get **rearranged with animation**: cards slide into two columns, then **connectors ("cables")** draw from each card to its note, so the link between mark and note is visible. Notes list on the side; hovering a note lights its cable and card; hovering a card lights its note.
  - Cables are drawn as the chevron rule (thin bar with tiny subtracted chevrons travelling toward the note).
  - Copy verbatim: headline "Here's your desk." sub "Two piles. Every card on the right works, with a note. Every card on the left could work too, with the same note." Closing "The asterisks are the workshop." Marks stay unique gold * † ‡ § ¶.
  - **Reset button** ("Deal again") that restacks the cards with animation.
  - Award-level: interesting, fun, not unserious, not boring.

## 6. Why us (cream)
- Bug: on hover the finished suit snaps back to a square and slowly morphs again: jarring, "scares me instead of attracting me". Fix: never snap. On hover the suit may do a slow, small reaction (breathe, tilt, glow, or morph to a slightly bolder version of the same suit over ≥600 ms) and return just as slowly. No shape reset, no flicker.
- Entry morph square→suit once, when the band enters, then stays. Make the section more interesting than four rows: e.g. bands that expand on hover to show the proof line with the rule drawing under it, chevrons travelling toward the statement.
- Copy verbatim from FEEDBACK-3 (four statements + proof lines).

## 7. The workshop route: "AI without the smoke screen" (carbon, full-screen, scroll-driven)
- Spine = vertical chevron rule (bar + subtracted chevrons, chevrons travel down with scroll). NOT the wand.
- Round 3 screens were sparse. Give each moment one visual (a suit, squares, a keyboard/phone glyph drawn in the suit style, the rule) that animates with scroll, plus the copy. Not empty.
- Copy (approved 2026-09-22, verbatim):
  1. **The smoke.** What your team has been told AI does. We clear it in ten minutes, using your own examples.
  2. **Your desk.** Three real tasks from your team's week. Not ours. Yours.
  3. **Hands on.** Everyone at a keyboard or a phone, with the tools they already have. We bring our own tools for teaching, tailored to your team.
  4. **Teaching magic.** One task, done with AI, in front of everyone.
  5. **Where it breaks.** We make it fail on purpose, so you see it before a client does.
  6. **House rules.** What never leaves the building. Who checks what. Three lines, written together.
  7. **Next week.** (OPTIONAL, visually distinct: the spine becomes a dotted rule leading to it, label "Optional" small in gold) A one-page plan in your inbox: what to automate first, what to guard, what to ignore. Yours to use, no second session needed.
- End the route with the closing CTA block (see 9).

## 8. Sources route
- A list of every fact used on the site: the claim as shown, the exact figure, source name, year, link, and one line on what we took from it. Pull from `mistral-study/research/data.md`. Only the facts actually shown on the site (93%, 9%, 47%, 34%) plus a short "Also read" list of the others that informed the copy, clearly separated. Cream page, typographic, chevron rule as dividers.

## 9. Closing CTA (felt-deep) and footer (carbon)
- "Ready when you are." → "Book a half-day" is too simple. Add suits: a slow arrangement of the four classic suits and squares reacting to the pointer (reuse the hero field, lower density), the chevron rule pointing at the button.
- Footer, professional, Costa Rican conventions. Left: logo mark + "kadabra" + one line "Hands-on AI workshops for teams in Costa Rica." Middle: routes (Home · The workshop · Sources) and contact: WhatsApp (TODO), Email (TODO), LinkedIn (TODO). Right: "San José, Costa Rica" (TODO confirm), legal line "© 2026 kadabra. All rights reserved." plus "Cédula jurídica: TODO" (CR businesses list it). Every TODO in red, class `todo`, easy to grep.

## 10. Data hygiene
- Sources for the numbers shown:
  - 93% CR tech companies save time on repetitive tasks with AI, PROCOMER 2025 (Caracterización del Sector TIC 2025).
  - 9% have a formal AI governance policy, PROCOMER 2025.
  - 47% of employees have received AI training, KPMG × Melbourne Business School 2025.
  - +34% productivity for novice workers with an AI assistant, Brynjolfsson, Li & Raymond, NBER WP 31161, 2023.
  Links in `research/data.md`.

## Still TODO by the founder
WhatsApp number/message, email, LinkedIn URL, city, cédula jurídica. All shown as red TODOs.
