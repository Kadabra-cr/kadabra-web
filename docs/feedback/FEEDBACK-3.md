# Founder feedback on mockup round 2 (2026-09-22) + creative direction for round 3

Overrides FEEDBACK.md and BRIEF.md where they conflict. Read all three.

## Brand assets (real, use them, we worked hard on them)
Folder: `C:/Users/david/Vault/Business/Startup/kadabra/logo/`
- `kadabra-first-edition.svg`: full lockup. Card-with-sparkle mark, "kadabra" wordmark (custom cut Gabarito Black), a chevron ribbon rule under the wordmark. Canvas is 1920×1080 with lots of empty space: crop the viewBox to the artwork. Fill is carbon; convert to `currentColor` so it sits on felt, cream and carbon.
- `kadabra-first-edition-icon-only.svg`: the card-with-sparkle mark alone (345×359). Use for favicon, header on mobile, and the small mark.
- `kadabra-first-edition-wand.svg`: the chevron ribbon / wand rule (1312×60). This is THE brand rule: use it as section dividers, underline of key statements, and the wand in the hero if a wand appears at all.
The hand-drawn card mark from round 2 is retired.

## Suits
- Founder now prefers the **classic ("smooth") set for most of the site**; sharp only where a glyph must be tiny and crisp. Hearts may stay sharp. Decide per placement, be consistent.
- Classic club: the two side lobes sit too high, it reads as a tree. Lower the side lobes so their centres are at or just above the centre lobe's equator; stem short and wide.
- Hero morph: the club does not read as a club mid- or end-morph ("horrible"). Fix the club target path or raise the segment count for all shapes so the club has real lobes. If the club still can't read, drop club from the morph set and morph to spade/heart/diamond only.
- Trail: the hover trail must be **more noticeable** (still no glow, use opacity and a slightly longer hold before returning to square).

## Hero and header
- Add a **slim header bar** (carbon or white, founder undecided; direct it) with the real logo, two or three anchor links, and the CTA. The hero must not feel like the entire screen is a box of squares.
- The corner decorations (semi-transparent wand, diamond, club, spade) are rejected. Remove.
- The full grid of squares feels **boxed in**. Replace with something that breathes: a sparse field of floating squares/marks that drift slowly and morph under the pointer, or an arrangement that is clearly not a wall. The founder said: "don't stay just with my descriptions, take a look at the site and iterate."
- Headline stays: "The trick is teaching, not tools."

## Palette rhythm
Too much felt green reads as gambling. New rhythm, directed by Fable:
- Header: carbon `#1C1A17`.
- Hero: felt-deep.
- Contrast section: **cream** `#F6F2EA` (lighter than bone) with carbon text; the 9% panel dark.
- Swipe section: felt.
- Why us: cream or white.
- Timeline: carbon, full-screen, scroll-driven (see below).
- Closing CTA: felt-deep. Footer: carbon.
Felt should carry roughly 40% of the page, not 80%. Red stays CTA-only. Gold stays for the notes.

## Contrast section
- 93% and 9% are too far apart: the eye travels too much. Put them **adjacent**, one tight pair, same baseline, the "9%" visibly the answer to the "93%".
- Keep the three-beat story and the resolution beat, keep "Nobody taught the team." full width.

## Animations
- Current entrances are "generic AI animations". Use **impeccable `animate`** on the whole page. Motion must have a reason per section: the hero field breathes, numbers count, the pair snaps together, the cards deal, the timeline scrolls as a journey, the why-us statements react.

## Swipe cards ("Can AI take this?")
- Corner indices: top-left index is not in the top-left. Fix: index in both corners, mirrored, like a real card.
- Give each card a **red band across the middle** carrying the card text, so the text is a line on a card, not floating in the centre.
- **Cards never leave the screen.** Swiping sends a card to a left pile ("Best not") or a right pile ("AI can take it") that stay visible.
- After the fifth card, the two piles **expand into two groups**, still on screen, so the visitor sees their own answers and reflects. Each card then shows its **unique footnote mark** (use distinct marks: `*`, `†`, `‡`, `§`, `¶`, in gold), and below the groups the breakdown lists the five marks with their notes.
- Wording "You swiped right on N of 5" is rejected (sounds like a score). Replace with:
  - Headline: **Here's your desk.**
  - Sub: Two piles. Every card on the right works, with a note. Every card on the left could work too, with the same note.
  - Then the breakdown by mark. Closing line stays: **The asterisks are the workshop.** (rename to "The notes are the workshop." if asterisks are no longer literal; keep the founder's line if `*` still leads the list.)

## Why us
- Rejected as generic: "a bunch of words", no interactivity, no movement. Rebuild with movement: e.g. each statement occupies its own band that reacts on hover/scroll (suit morphs in, statement slides, a one-line proof appears), or a pinned sequence. Keep the four statements verbatim. Add one short proof line under each (no invented facts; use what the workshop actually does):
  - ♠ Your real work, not slides. / We open your files, not a template.
  - ♥ We grew up with these tools. / Daily users, not certified presenters.
  - ♦ The risks, not just the hype. / We make it fail in front of you on purpose.
  - ♣ Nothing to sell you afterwards. / No licences, no platform, no upsell.

## Timeline → "AI without the smoke screen"
- The horizontal 9:00 / 10:00 / 12:00 timeline is rejected. Replace with a **vertical, full-screen, scroll-driven journey** on carbon. Moments, not hours. This is the main workshop, name it on screen: **AI without the smoke screen** (future Spanish: "Inteligencia artificial sin humo"; do not show Spanish now).
- Moments (copy verbatim, one screen-ish each while scrolling; the brand ribbon runs down the spine):
  1. **The smoke.** What your team has been told AI does. We clear it in ten minutes, using your own examples.
  2. **Your desk.** Three real tasks from your team's week. Not ours. Yours.
  3. **Hands on.** Everyone at a keyboard, with the tools they already have.
  4. **The first trick.** One task, done with AI, in front of everyone. Then everyone does theirs.
  5. **Where it breaks.** We make it fail on purpose: the invented number, the pasted client data, the confident nonsense.
  6. **House rules.** What never leaves the building. Who checks what. Three lines, written together.
  7. **Next week.** A one-page plan lands in your inbox: what to automate first, what to guard, what to ignore.

## Still TODO by the founder
- WhatsApp number and message. Keep `#TODO-whatsapp` and the red footer TODO.

## Page margins (founder, 2026-09-22, from Mistral)
- Keep a **content-free margin on both sides of the page**, roughly an inch (about 96 px at 1440, scale down to ~20 px on mobile). No content and nothing eye-catching lives in those margins.
- **Colour and background fields may bleed edge to edge** (the hero field, section backgrounds, the ribbon rule), but text, cards, numbers, buttons, decorations and the header's content stay inside the margin.
- The reason: it feels spacious, not trapped. Round 2 felt boxed in. Make this a fixed layout rule in DESIGN.md: one content column with generous outer gutters, backgrounds full-bleed.
