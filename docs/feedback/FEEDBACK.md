# Founder feedback on round 1 prototypes (2026-09-21)

Verbatim intent, grouped. Everything here overrides BRIEF.md where they conflict.

## Type
- Gabarito **800**, not 900, everywhere titles appear.
- Descenders ("g", "y", "p") were clipped in hero-c by the per-word rise mask. Never clip descenders; clip only during the rise, or pad the mask.

## Suits (suits.html is liked; keep its styling)
1. Sharp set: **no chevron notch inside**. Sharp silhouettes only.
2. Grid of suits **flickers**: sometimes a cell flashes another icon at full opacity instead of a smooth transition. This is dangerous (photosensitivity) and must be gone. Only smooth transitions, ever.
3. Decision: **sharp for UI, classic ("smooth") on the rare cards.**
4. Classic club: the three lobes sit too far from the stem and the join is not smooth. Redraw: lobes tangent to each other, stem meeting the bottom lobe cleanly, silhouette reads as one shape at 16 px.

## Hero (option A direction wins, but changed)
- **No cursor replacement.** Keep mouse tracking to interact with background elements.
- Layout: **centered** hero. Tech should feel centered. Decorations come in from the sides (reference: multiverse.io hero: centered type, elements flanking from left/right edges).
- Background: the whole felt hero has a field of **very dim white and red squares** (not only the bottom band). Much lower opacity near the headline and CTA to avoid collision.
- Mouse over the background: squares under/near the pointer get slightly more opaque and **morph square → a random suit**, then after a while morph **back to square**, leaving a trail of magic. Square to shape only, never shape to shape, in the hero.
- Morph means **shape morph**, not crossfade. If true path morphing is too hard, make the crossfade much smoother; but try morphing first.
- **Less glow.** Glow feels cheap here.
- Headline: candidate 1 ("The trick is teaching, not tools."). No selector needed anymore.
- Wand: neither the sweeping wand (B) nor the static illustration (C). Bring wand/sparkle back only if it earns its place as a side decoration.

## Contrast section
- Variant 1 (green-heavy grid of numbers) rejected: "a bunch of random numbers".
- Variant 2 (green + bone split) is very cool. Keep the **93% vs 9%** pair, it sets the contrast.
- The three bottom datapoints (95 / 34 / 52) don't tell a story on their own and aren't selling points. Rework: either give them a narrative (cause → effect → what we do), or drop to what earns its place.
- **No left-aligned commentary bubbles** (like "The difference is never the tool…"). They leave most of the screen empty and overload one corner. Find a composition that uses the width.

## Puzzle → "swipe" classification
- Current sort-into-three-buckets is too complicated.
- New mechanic: **swipe cards left/right** (the founder calls it "AI-Tinder", never brand it that way). Right = "AI can take this", left = "best not". About **5 cards**. This is one of the rare places real vertical cards are allowed.
- It is a gentle **trap**: most visitors will swipe "AI can take this" on most cards. At the end, reveal that AI *can* do those, but each has caveats: needs assistance, can go wrong like this, this and this.
- **No right/wrong, no green/red.** Caveats are marked with asterisks, yellow/gold notes, "careful" and "over-optimism" language. The goal is to show they still have things to learn, warmly.

## Process
- Use **/impeccable iteratively**: brand study first (design philosophy from PRODUCT.md + this feedback + awwwards research), then one mockup site that combines every prototype with this feedback applied. Not the final site. Stay far from slop and lazy design.

## Copy for the reworked pieces (creative director, use verbatim)

### Swipe puzzle: "Can AI take this?"
Intro: Five things that land on an office desk every week. Swipe right if AI can take it. Left if best not.
Right label: **AI can take it** · Left label: **Best not**
Cards (front) and their asterisk (revealed at the end, gold, never red/green):
1. Answer a client asking why their invoice is higher this month. * It writes a convincing reply. If it doesn't have the numbers, it invents a reason. Give it the invoice, then read before sending.
2. Summarise the 40-page supplier contract. * Good summary, and it will skip the one clause that matters. Ask for the clause list, then read those pages yourself.
3. Enter this stack of receipts into the system. * Reads receipts well. Blind to duplicates and wrong dates. Spot-check one in ten.
4. Write the monthly report for the owner. * The structure in a minute. Every number needs a human check; numbers are where it sounds most sure and is most wrong.
5. Decide whether the new client gets 60-day payment terms. * It can list the pros and cons. The decision, and the risk, stay with a person.
Reveal: "You swiped right on N of 5. So do most people. All five work, with an asterisk." Then the five asterisks. Closing line: **The asterisks are the workshop.**
If the visitor swipes left on everything: "Careful is good. Three of these are safe to hand over today, with the asterisk." Same reveal.

### Contrast section narrative (replaces the three loose numbers)
Keep the 93% vs 9% pair as the opener. Then a three-beat story, read left to right or top to bottom, each beat a cause of the next:
1. 88% of companies now use AI in at least one function. (McKinsey, 2025)
2. 95% of their AI pilots show no measurable return. (MIT NANDA, 2025)
3. Only 47% of employees ever received any AI training. (KPMG, 2025)
Resolution beat, set apart: Beginners who are taught get up to 34% more done. (NBER, 2023)
Section closing line, full width, not a bubble: **Nobody taught the team.**
