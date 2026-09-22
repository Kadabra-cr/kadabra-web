# kadabra — decision prototypes brief

Purpose: the founder picks copy, suit style, hero behaviour, palette weight and puzzle feel from these. Each prototype is one standalone HTML. Nothing is the final site.

Read `PRODUCT.md` in this folder first. Then the impeccable skill (see agent prompt).

## Palette (start here, tune freely within it)
- felt: #1B3A2F (main dark surface; try one lighter and one darker step)
- felt-deep: #12261F
- bone: #F3EFE6 (reading surfaces, use sparingly)
- white: #FFFFFF
- carbon: #1C1A17 (text on bone)
- red: #8E1424 (CTA only; deeper than a typical red, must read on both felt and bone)
- gold: #C9A227 (tiny, optional, reward/sparkle only)

## Type
- Titles: Gabarito 800 (never 900), tight tracking (-0.03em), very large. Titles only.
- Everything else: pick ONE humanist or grotesque sans from Google Fonts that is not Inter/Roboto/Open Sans/Poppins/Montserrat. Suggested: Hanken Grotesk, Instrument Sans, or Bricolage Grotesque at low weights. Justify in a comment.

## Copy (use verbatim; TODO items stay visibly marked)

### Hero headline candidates (show all; "trick / magic" angle, on brand, not cringe)
1. The trick is teaching, not tools.
2. Nothing up our sleeves. Just your work, done faster.
3. Your team already holds the wand. We teach the trick.
4. Less magic show. More magic.
5. Learn the trick behind the trick.

Sub-line: Half-day, hands-on AI workshops for teams in Costa Rica. Your real work, your tools, nothing to buy afterwards.
CTA: **Talk to us on WhatsApp** → href `#TODO-whatsapp` (mark TODO in red in the hub, not on the button).

### Contrast section ("It works. Until it doesn't.")
Big numbers, each with a one-line and a source line:
- 93% of Costa Rican tech companies save time on repetitive tasks with AI. Only 9% have any AI policy. (PROCOMER, 2025)
- 95% of company AI pilots show no measurable return. (MIT NANDA, 2025)
- Beginners get up to 34% more done with AI. Experts: almost nothing. (NBER, 2023)
- 52% of employees hide that they use AI at work. (Microsoft Work Trend Index, 2024)
Closing line: The difference is never the tool. It's whether anyone taught the team.

### Puzzle ("Will AI replace the accountant?")
Intro: Sort six things an accountant does every month. Where does AI actually land?
Buckets: **AI does it** · **AI helps** · **Stays human**
Tasks and the honest answer (revealed after sorting, no right/wrong scoring):
1. Enter supplier invoices into the system → AI does it (a person spot-checks)
2. Chase clients who pay late → AI helps (drafts the messages; a person decides who to push)
3. Prepare the monthly report → AI helps (drafts; a person verifies every number)
4. Answer the owner's "can we afford this?" → Stays human
5. Prepare the tax filing → AI helps (prep; a person signs and is liable)
6. Spot a transaction that looks wrong → AI helps (flags; a person judges)
Reveal copy: 0 of 6 tasks disappear. 5 of 6 change. Then: In theory AI could do 94% of knowledge-work tasks. In practice it's used for 33%. (La Nación / MICITT, 2026). The gap is training.
Tone: the reveal shows the visitor's sort next to the honest one. No "wrong". No confetti.

### Why us (four statements, one suit each) + half-day timeline
- ♠ Your real work, not slides.
- ♥ We grew up with these tools.
- ♦ The risks, not just the hype.
- ♣ Nothing to sell you afterwards.
Timeline "A half day with kadabra":
- 9:00 Discovery. What your team actually does all week.
- 10:00 Hands-on. Three of those tasks, with AI, on your own files.
- 12:00 The catch. Where it breaks, and what never leaves the building.
- Next week. A one-page plan: priorities, guardrails, what to try first.

### Closing CTA
Ready when you are. → **Book a half-day** (WhatsApp, same TODO link)

## Prototype list and owner
Agent "system": `suits.html`, `hero-a.html`, `hero-b.html`, `hero-c.html`
Agent "interaction": `puzzle.html`, `contrast.html`, `index.html` (hub)

## Rules for every prototype
- One file each, vanilla, Google Fonts only, `prefers-reduced-motion` respected.
- Smooth easing (cubic-bezier / spring-like), no `steps()`.
- Green-heavy. Bone/cream only where reading comfort needs it.
- Suits are the signature. Cards appear at most once, only where the brief says.
- No placeholder lorem, no fake logos, no fake testimonials, no prices.
- Verify with one Playwright screenshot round (desktop 1440 and mobile 390), fix, one more round max.
