# kadabra — sitio web

Sitio de **kadabra**, estudio costarricense de talleres prácticos de IA de medio día.
Producción: https://kadabra-site.pages.dev (Cloudflare Pages).

## Estructura

| Carpeta | Qué contiene |
| --- | --- |
| `site/` | Lo que se publica. HTML, CSS, JS y SVG, sin framework ni pasos de compilación. |
| `src/` | Fuentes de las tres rutas: `shell.html`, `app.src.js`, `field_r8.js` y `build.py`. |
| `tools/` | Verificaciones con Playwright y capturas de pantalla. |
| `brand/` | Logotipo en SVG y archivos originales de Affinity. |
| `docs/` | Investigación, datos citados en el sitio, retroalimentación y exploraciones. |

## Cómo trabajar

Editá siempre `src/`, nunca `site/app.js` ni los `index.html` generados.

```bash
python src/build.py                  # regenera site/app.js y las tres rutas
python -m http.server 4173 --bind 127.0.0.1 --directory site
cd tools && BASE=http://127.0.0.1:4173 node shots.mjs   # 14 verificaciones
```

## Publicar

```bash
wrangler pages deploy site --project-name=kadabra-site --branch=main --commit-dirty=true
```

## Pendientes

- Número de WhatsApp, correo, LinkedIn y ciudad: hoy son `TODO` visibles en rojo.
- Traducción del sitio al español.
