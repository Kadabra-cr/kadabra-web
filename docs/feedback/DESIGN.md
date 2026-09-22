# DESIGN.md: the kadabra visual world

## The world: a close-up magic mat

Not a stage. Not a casino table. A close-up pad is a *working* surface: dark felt,
measured, where a professional puts real objects down in front of three people and
shows them the method. That is what a half-day workshop is. The page is that mat
seen from above, in good light, with the team's real work on it.

- Nothing is a "reveal". The trick is shown slowly, at arm's length.
- The magic is sharp and quiet. No glow, no sparkle spam, no deck, no chips.
- Density is the only tone: the hero models light with opacity alone.
- Rows, not tiles: statements and beats are ruled full-width rows.
- One accent per control: gold belongs to the notes and nothing else.

## Layout rule (fixed)

**One content column, generous outer gutters, backgrounds full-bleed.**

- Gutter `clamp(20px, 6.6vw, 96px)`: about an inch at 1440, about 20 px at 390.
- Content column `width: min(100% - 2*gutter, 1248px)`, centred. Every text block,
  card, number, button, footnote and the header's own content lives inside it.
- Colour and background fields bleed edge to edge: the hero mark field, every
  section ground, the ribbon rule. Nothing eye-catching sits in the gutters.
- The reason: spacious, not trapped. Round 2 felt boxed in.

## Palette rhythm

Too much felt reads as gambling. Felt carries roughly 40% of the page, not 80%.

| Role | Colour | Where |
|---|---|---|
| carbon | `#1C1A17` | header, the timeline, the footer |
| felt-deep | `#12261F` | hero, closing CTA |
| felt | `#1B3A2F` | the swipe section |
| cream | `#F6F2EA` | the contrast section, why us |
| white | `#FFFFFF` | titles on dark, the mark field |
| red | `#8E1424` | the CTA, the card band, the footer TODO. Nothing else. |
| gold | `#C9A227` | footnote marks and the resolution number. Nothing else. |

Order down the page: carbon, felt-deep, cream, felt, cream, carbon, felt-deep,
carbon. Dark and light alternate so no surface outstays its welcome.

## The logo

The lockup is drawn, not described. `logo-sprite.svg` carries `logo-full`,
`logo-mark` and `logo-ribbon`, every fill `currentColor`, viewBoxes cropped to the
artwork. **Never redraw the mark in markup.** Reference the symbol, set
`fill-rule: evenodd` on the `use`, and let it take the colour of its ground.

- `logo-full`: header (about 28 px tall) and footer.
- `logo-mark`: favicon and any place too narrow for the lockup.
- `logo-ribbon`: THE brand rule. Underline of a closing statement; rotated 90
  degrees it is the spine of the timeline and its progress indicator.

## The one owned asset

**A square that becomes a suit.** One path, `M + 24C + Z`, lerped number for number
between `square` and a suit. One element, one path, so there is nothing that can
crossfade and nothing that can flash. Ordinary work, taught, becomes something with
a shape.

Square to suit only. Never suit to suit.

## Suits

**Classic (smooth) is the primary set** everywhere a suit is seen: the hero field,
the five cards, the why-us bands. Sharp is reserved for glyphs under about 16 px
where the smooth silhouette would mush. Be consistent within a section. The classic
club's side lobes sit at the centre lobe's equator; 24 segments is what gives it
real lobes mid-morph.

## Type

- **Titles:** Gabarito 800, tracking -0.035em, line-height 0.95 and up. Titles and
  the wordmark only. 900 is the logo's alone.
- **Body:** Hanken Grotesk 400/500/600. Humanist, slightly narrow, reads as a
  person talking rather than a deck.
- **Numbers:** Gabarito 800, tabular figures, so a counting number does not jitter.
- Descenders are never clipped. Entrances fade and rise the whole line.

## Composition

- The hero is **centred** on one vertical axis: headline, sub-line, CTA. No corner
  decorations; the field is the only thing behind it.
- Statements are **full width** inside the column.
- **No corner bubbles**, no eyebrows, no 01/02/03, no cards as page structure.
- More space above a heading than below it.

## The timeline is a vertical journey

"AI without the smoke screen" is not a schedule of hours, it is seven moments. The
section is carbon, each moment about a viewport tall on desktop, the ribbon running
down the spine and brightening as the reader passes. Scroll-driven by
IntersectionObserver and sticky positioning only: the page never takes the scroll
away from the reader.

## Motion

Motion has a reason per section, never one generic entrance repeated:

- **Hero:** the field breathes and wakes under the pointer. Squares near the
  pointer rise in opacity and morph into a random classic suit, hold about 1.4 s,
  then morph back. The trail is opacity and dwell only.
- **Contrast:** the 9% panel slides in to butt against the 93%; numbers count once.
- **Swipe:** cards deal, then fly to a pile that stays on screen.
- **Why us:** a square morphs into the band's suit, the statement settles, the
  proof line arrives after it.
- **Timeline:** the spine fills as a journey.

Rules: exponential ease-out, no `steps()`, no bounce. Morph, never crossfade.
**Never flash:** no opacity change of 0.15 or more within 50 ms, anywhere. The
cursor is never replaced. Numbers count once and stay. Nothing moves while it is
being read. `prefers-reduced-motion`: the field is a static sparse set of squares,
numbers print at final value, the deck advances by button and keyboard.

## Gamification

One puzzle: five cards, swipe right or left. A warm trap, not a quiz. No score, no
right, no wrong, no green, no red, no confetti. Cards never leave the screen; they
land in two piles that expand at the end so the visitor reads their own desk back.
The reveal is five gold footnote marks and one line.

## Anti-slop list

1. No cursor replacement. 2. No glow, bloom or neon. 3. No flicker. 4. No clipped
descenders. 5. No wall of squares behind the hero; the field is sparse. 6. No grid
of loose numbers with no story; every number causes the next. 7. No left-aligned
commentary bubble. 8. No red/green verdicts, no "you got 3 of 5". 9. No casino.
10. No fake logos, testimonials, prices or client names. 11. No em-dashes in copy.
12. No stock icons; suits, chevrons and the ribbon are drawn here. 13. No scroll
hijack, no full-page loader. 14. No 4-up stat tiles. 15. No Spanish on screen yet.
16. Nothing in the gutters.
