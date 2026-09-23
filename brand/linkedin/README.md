# LinkedIn

Three cover designs plus the profile picture. Each cover comes in two sizes.

| File | Where it goes |
|---|---|
| `export/*_perfil_1584x396@2x.png` | Cover of a personal profile |
| `export/*_empresa_1128x191@2x.png` | Cover of the kadabra company page |
| `export/perfil-icono-carbon_1080.png` (or `_400`) | Profile picture: the white card with gold sparkles on carbon; pairs with the carbon cover |
| `descripcion.md` | Company page tagline, description and specialties |

Covers are exported at twice the size LinkedIn asks for, so they stay sharp on high-density screens. LinkedIn scales them down on upload.

## Changing the text

Edit `copy.md`, then run this from the project folder:

```
node tools/linkedin.mjs
```

The images are rewritten in `export/`. To re-render just one design, pass part of its name, e.g. `node tools/linkedin.mjs carta`.

## How they're made

- `banners.html` is the template.
- The suits come from `src/suits-square-morph.json`, and the logo and icon from the site's `site/sprites.svg` (second edition).
- The smoke and the scattered suits use a fixed random seed, so every export draws the same picture.

Safe zones: the text starts right of the photo (personal profile) and right of the logo (company page). Nothing important sits near the edges.
