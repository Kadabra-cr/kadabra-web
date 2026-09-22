# mistral.ai — CSS motion notes

Files: `astro.css` (177 KB, Tailwind v4 build + theme tokens), `main.css` (12.6 KB).
Everything is driven by Tailwind v4 `@theme` custom properties: `--animate-*` tokens map a
keyframe + duration + delay + easing, then get used as `animate-<name>` utilities.

## Signature keyframes

```css
/* "falls from above and squashes" — used for the bento / markitecture blocks */
@keyframes markitecture-fall{0%{opacity:0;transform:translateY(-300px)}
 50%{opacity:1;transform:translateY(0) scaleY(1)}
 65%{transform:translateY(0) scaleY(.95)}   /* squash  */
 80%{transform:translateY(0) scaleY(1.02)}  /* stretch */
 to{transform:translateY(0) scaleY(1)}}
@keyframes bento-fall{ /* same, from -200px */ }
/* applied as: .5s ease-in forwards */

/* clip-path wipes for cards/posts */
@keyframes reveal-post-left {0%{clip-path:polygon(0 0,0 0,0 0,0 0);transform:translateY(20px)}
 to{clip-path:polygon(0 0,100% 0,100% 100%,0 100%);transform:translateY(0)}}
--animate-reveal-post-right: reveal-post-right 1s cubic-bezier(.51,-.01,.49,1);
--animate-reveal-top-right:  reveal-top-right .5s .2s cubic-bezier(1,0,.64,.69) both;

/* ambient blinking terminal/dot vocabulary */
@keyframes dot-lane {0%{opacity:.1}30%{opacity:1}60%,to{opacity:.1}}      /* 1.6s linear inf */
@keyframes dot-pulse{0%{opacity:1;border-width:0}50%,to{opacity:0;border-width:1rem}} /* 2s */
@keyframes blink     {0%,to{opacity:1}50%{opacity:.2}}                    /* 2s linear inf */
@keyframes logo-flicker{0%,to{opacity:.2}50%{opacity:1}}
@keyframes fading-arrow-scroll{0%,40%{opacity:.2}50%{opacity:1}60%,to{opacity:.2}}
/* three arrows, same 2s loop, delays 0s / .2s / .4s => downward chase */

/* entrance family: one keyframe per direction, staggered by delay only */
brand-from-left/-right/-top/-tl/-br  .7s ease-out both, delays .1 .1 .4 .55 .5 2s

/* OCR "scanner" demo — pure CSS fake product UI, all 4s ease-in-out infinite */
@keyframes animate-hero-ocr4-scanner{0%{opacity:0;width:0;right:100%}5%{opacity:1;width:50px}
 45%{opacity:1;width:200px;right:0}50%,to{opacity:0;width:0}}
@keyframes animate-hero-ocr4-block-1{0%,5%,to{opacity:0;transform:translateX(5px)}
 15%,72%{opacity:1;transform:translateX(0)}82%{opacity:0;transform:translateX(-5px)}}
/* blocks 2..5 identical, each shifted +5% => text lines "detected" one by one */

/* slow drifting gradient covers (4 layers, different periods so they never re-sync) */
--animate-cover-gradient-1: cover-gradient-1 8s 3s infinite linear;  /* +2,3,4: 10s,5s,6s */
@keyframes cover-gradient-1{50%{background-position:50% 100%;background-size:80% 80%;
 transform:scale(3) rotate(-75deg)}}

/* misc UI */
@keyframes animate-pop-in{0%{transform:scale(0)}50%{transform:scale(1.1)}to{transform:scale(1)}} /* .3s */
@keyframes animate-unroll-in{0%{opacity:0;max-height:0}30%{opacity:1}to{opacity:1;max-height:100%}}
@keyframes scaleIn{0%{transform:scale(0) translateY(10px)}to{transform:scale(1) translateY(0)}}
 /* .5s cubic-bezier(.68,-.55,.27,1.55) backwards — the only overshoot ease in the sheet */
@keyframes wave-a/-b/-c { y/height on <rect> — SVG audio bars, 3 phase-offset variants }
```

## Easing inventory
- CSS: `cubic-bezier(.68,-.55,.27,1.55)` (overshoot), `cubic-bezier(.51,-.01,.49,1)`,
  `cubic-bezier(1,0,.64,.69)`, `cubic-bezier(.65,0,.15,.99)`, `cubic-bezier(.4,0,.2,1)`,
  plus plain `linear` for every infinite ambient loop.
- GSAP: default for the hero headline is `power4.inOut` @ 1s; elsewhere `power2.out`,
  `power4.out`, `back.out(2.5)`, `elastic.in`, `none`.
- Rule of thumb on this site: **content entrances get expressive eases, ambient loops get `linear`.**

## Transition usage (Tailwind utilities, counted in home.html)
`transition-all` 203 · `transition-transform` 175 · `transition-colors` 101 ·
`transition-[width]` 32 · `transition-opacity` 30.
Hover is almost entirely `group-hover:translate-x-*` (arrows sliding right 6–20 units)
with `group-hover:delay-75/100` to stagger icon-then-label, plus
`group-hover/link:w-full` on a `transition-[width]` underline.
Images fade in on decode: `group-data-[loaded=false]:opacity-0 transition-opacity duration-500 ease-in-out`.

## Texture
`bg-[url(/images/noise/noise-rectangle.png)]` — a 71 KB tiled noise PNG laid over flat fills.
