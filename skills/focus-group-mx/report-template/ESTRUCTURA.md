# Reporte Focus MX · Estructura del entregable

Documentación canónica del formato de entrega de diagnósticos Focus MX. Un cliente paga $2,500 MXN o más por un reporte siguiendo esta estructura. Cualquier reporte nuevo se construye sobre esta arquitectura.

---

## Arquitectura técnica

**Stack:**
- HTML semántico (secciones, no páginas)
- CSS Paged Media (spec W3C)
- **Paged.js** como polyfill (`https://unpkg.com/pagedjs/dist/paged.polyfill.js`)
- Chrome headless para generar el PDF final

**Por qué este stack:**
- HTML/CSS estándar no maneja paginación predecible
- `height: 11in` clipa contenido si excede
- `min-height: 11in` deja espacios vacíos cuando contenido es corto
- `page-break-inside: avoid` es advisory en Chrome — Paged.js lo respeta de verdad

**Cómo funciona:**
1. El reporte se escribe como secciones semánticas (`<section class="chapter">`)
2. Paged.js corre en el navegador, lee el contenido, lo pagina aplicando las reglas CSS
3. Inserta encabezados y pie de página automáticos con número de página y nombre de sección
4. Chrome headless imprime el resultado paginado a PDF

**El resultado:** un reporte que se pagina solo según su contenido. Reporte corto → menos páginas. Reporte largo → más páginas. Bloques nunca se cortan. Títulos nunca quedan huérfanos.

---

## Comando para generar el PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --print-to-pdf="/ruta/reporte.pdf" \
  --virtual-time-budget=30000 \
  --run-all-compositor-stages-before-draw \
  --hide-scrollbars \
  "file:///ruta/reporte.html"
```

**Notas:**
- `--virtual-time-budget=30000` da 30 segundos para que Paged.js termine de paginar
- `--run-all-compositor-stages-before-draw` espera el render completo
- El input es un `file://` URL, no una página web

---

## Estructura del documento

El reporte se compone de **una portada** + **N capítulos**. Cada capítulo es un `<section class="chapter" data-section="...">`.

### Anatomía completa

```html
<!DOCTYPE html>
<html lang="es-MX">
<head>
  <!-- Fonts: Fraunces + Inter + JetBrains Mono -->
  <style>
    /* Tokens (paleta + tipos) */
    /* Reglas @page (Paged Media) */
    /* Estilos de cada bloque */
  </style>
</head>
<body>

  <!-- PORTADA -->
  <div class="cover"> ... </div>

  <!-- CAPÍTULOS -->
  <section class="chapter" data-section="Resumen ejecutivo">
    <h1 class="chapter-title">...</h1>
    <!-- bloques -->
  </section>

  <section class="chapter" data-section="Diagnóstico detallado">
    ...
  </section>

  <!-- N capítulos más -->

  <!-- Paged.js polyfill -->
  <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
</body>
</html>
```

### El atributo `data-section`

Cada `<section class="chapter">` debe llevar `data-section="Nombre del capítulo"`. Ese nombre aparece automáticamente en el pie de página centrado de cada página de ese capítulo, gracias a:

```css
section.chapter {
  string-set: section-name attr(data-section);
}

@page {
  @bottom-center { content: string(section-name); }
}
```

---

## Capítulos canónicos (orden recomendado)

Los nueve capítulos del template de Rufino. Para un reporte nuevo, mantén este orden y nombres salvo cuando el caso lo justifique. La consistencia entre reportes es parte del valor de marca.

| # | data-section | Contenido del capítulo |
|---|---|---|
| 01 | Resumen ejecutivo | Veredicto + 2 numbers (Comprabilidad, Dispersión) + radar chart + flecha de proyección |
| 02 | Diagnóstico detallado | Material evaluado (URL + texto del cliente) + tabla 7 dimensiones |
| 03 | Mapa de mercado | 4 segmentos con barras horizontales + detalle por línea |
| 04 | Voces del panel | 6 quote blocks con perfil + avatar + tags |
| 05 | Análisis estructural | 3 huecos estructurales con sustento citado |
| 06 | Recomendaciones | Riesgo regulatorio (si aplica) + hero rewriteado + por qué cada cambio |
| 07 | Plan de acción | 5 micro-cambios accionables con título y body |
| 08 | Cierre | Predicción post-ajustes + caveats + fuentes consultadas + CTA "cómo seguir" |

La portada (`.cover`) no es capítulo. No tiene `data-section` propio (o tiene `Portada` pero no se usa porque la portada usa `@page cover` que oculta el pie de página).

---

## Componentes disponibles

Cada componente es una clase CSS con uso específico. **Usa los componentes existentes antes de inventar nuevos** — la consistencia visual entre reportes es el valor.

### Portada

| Clase | Uso |
|---|---|
| `.cover` | Wrapper de la portada. Full bleed (sin margen). Usa `@page cover` |
| `.cover-brand` | Logo "Focus.MX" arriba a la izquierda |
| `.cover-meta` | Bloque arriba a la derecha (#número, fecha, categoría) |
| `.cover-eyebrow` | Etiqueta "// Pre-test de página de aterrizaje" o similar |
| `.cover-title` | Título principal del reporte, Fraunces 60px |
| `.cover-lede` | Subtítulo italic descriptivo |
| `.cover-stats` | Grid de 3 columnas con stats clave (Comprabilidad actual, # ausencias, Proyección) |
| `.cover-bottom` | Pie de portada (URL evaluada + contacto) |

### Cabezales de capítulo

| Clase | Uso |
|---|---|
| `.chapter` | Wrapper del capítulo. Forza `break-before: page`. Lleva `data-section` |
| `.chapter-eyebrow` | Etiqueta superior `// Tipo de sección` en mono |
| `.chapter-title` | Título grande Fraunces 34px del capítulo |
| `.chapter-lede` | Párrafo italic descriptivo, fuente más grande que body |
| `.section-eyebrow` | Etiqueta para sub-secciones dentro del capítulo |
| `.h2-title` | Sub-título Fraunces 24px para dividir capítulo internamente |

### Bloques destacados

| Clase | Uso |
|---|---|
| `.veredicto-callout` | Caja rosa terracota con el veredicto en italic grande |
| `.evaluado-box` | Caja azul añil con la URL + texto del material evaluado |
| `.riesgo-card` | Caja con borde ámbar para riesgos detectados (regulatorios, culturales, etc.) |
| `.sugerida-hero` | Caja verde nopal con el headline reescrito propuesto |
| `.por-que-card` | Caja paper claro con los "por qué" cada cambio del rewrite |
| `.cierre-card` | Caja oscura ink con CTA al siguiente engagement |
| `.fuentes-block` | Caja paper con lista de fuentes consultadas en mono |

### Stats

| Clase | Uso |
|---|---|
| `.stats-grid` | Grid 2-col: stats a la izquierda, radar chart a la derecha |
| `.big-num-card` | Tarjeta blanca con label + número Fraunces 44px + sub italic |
| `.radar-card` | Tarjeta blanca que contiene el SVG del radar |
| `.radar-svg` | El radar chart SVG (ver código de ejemplo en `ejemplo-rufino.html`) |
| `.arrow-card` | Tarjeta verde con flecha de proyección 6.4 → 8.1 |
| `.summary-card` | Tarjeta resumen con número grande y texto italic al lado |

### Tabla de dimensiones

| Clase | Uso |
|---|---|
| `.dim-table` | Tabla completa de las 7 dimensiones |
| `.dim-name` | Columna del nombre de dimensión, Fraunces 15px |
| `.dim-score` | Columna del puntaje grande Fraunces 26px |
| `.dim-score.crit` | Puntaje crítico (color rojo terracota deep) |
| `.dim-score.warn` | Puntaje advertencia (color ámbar) |
| `.dim-score.high` | Puntaje alto positivo (color verde nopal) |
| `.dim-score.na` | Puntaje N/A (color gris) |
| `.dim-lectura` | Lectura del panel con citas inline (`.cite`) |

### Mapa de mercado

| Clase | Uso |
|---|---|
| `.mapa-segment` | Fila de un segmento (label + barra + puntaje + detalle) |
| `.mapa-segment-label` | Nombre del segmento + sub con perfiles |
| `.mapa-bar-track` | Track de la barra de fondo |
| `.mapa-bar-fill.verde` / `.amarillo` / `.rojo` | Relleno de la barra con gradiente |
| `.mapa-segment-pct.verde` / `.amarillo` / `.rojo` | Puntaje grande del segmento |
| `.mapa-detail` | Texto explicativo debajo de cada barra |

### Quotes (objeciones)

| Clase | Uso |
|---|---|
| `.quotes-grid` | Grid 2x3 de quote blocks |
| `.quote-block` | Una cita con perfil. Tiene comilla decorativa gigante |
| `.quote-block-text` | El texto de la cita en italic |
| `.quote-avatar` | Círculo con inicial del perfil |
| `.quote-name` | Nombre y edad del perfil |
| `.quote-tags` | Tags en mono (ciudad · NSE · ocupación) |

### Huecos estructurales

| Clase | Uso |
|---|---|
| `.hueco-block` | Bloque completo de un hueco estructural |
| `.hueco-number` | Número gigante Fraunces 38px |
| `.hueco-title` | Título del hueco Fraunces 19px |
| `.hueco-body` | Cuerpo explicativo con sustento embebido |
| `.hueco-sustento` | Caja paper claro al final con sustento + cita |

### Micro-cambios accionables

| Clase | Uso |
|---|---|
| `.micro-item` | Una fila de micro-cambio (numero + título + body) |
| `.micro-num` | Número Fraunces 28px |
| `.micro-title` | Título del cambio |
| `.micro-body` | Descripción del cambio con call to action específico |

### Caveats y límites

| Clase | Uso |
|---|---|
| `.limit-grid` | Grid 2-col de límites del diagnóstico |
| `.limit-item` | Un límite con guión terracota al inicio |

---

## Sistema de tokens

### Paleta

```css
--terracota: #9d422a;        /* primary, accents */
--terracota-deep: #5f1503;   /* puntajes críticos */
--terracota-light: #ffdbd2;  /* fondo callouts terracota */

--anil: #405aa9;             /* "evaluado" (input) */
--anil-light: #dce1ff;       /* fondo evaluado-box */

--nopal: #4c6707;            /* "sugerido" (output) */
--nopal-light: #cdee85;      /* fondo sugerida-hero */

--bg: #fefbf9;               /* background general */
--bg-paper: #f8efe9;         /* fondo de cards secundarias */
--bg-soft: #fbeeea;          /* fondo veredicto-callout */
--ink: #1a1614;              /* texto principal */
--ink-soft: #4a4344;         /* texto secundario */
--ink-muted: #82736e;        /* labels, captions */
--rule: #e6d3ce;             /* bordes y separadores */
```

### Color como narrativa

- **Terracota** = análisis Focus MX (puntajes, veredictos, alertas)
- **Añil** = input del cliente (material evaluado)
- **Nopal** = recomendaciones (versión sugerida, mejora esperada)
- **Ámbar** (`#c97a26`) = riesgo regulatorio detectado
- **Gris neutro** = límites, caveats, fuentes

Esta narrativa de color debe respetarse en cada reporte nuevo.

### Tipografía

| Familia | Uso |
|---|---|
| **Fraunces** (variable: opsz, wght, SOFT) | Display, títulos, quotes italic. La voz editorial. |
| **Inter** | Body text, labels de UI, párrafos descriptivos |
| **JetBrains Mono** | Section labels, etiquetas técnicas, citas a fuentes |

### Tipo scale

```
Cover title:    60px Fraunces 600
Chapter title:  34px Fraunces 600
H2 title:       24px Fraunces 600
Big number:     44px Fraunces 700
Hueco number:   38px Fraunces 700
Micro number:   28px Fraunces 700
Quote:          13px Fraunces italic 500
Body:           12px Inter 400
Mono label:     9-10px JetBrains Mono 500-600, 0.16em letter-spacing
```

---

## Patrón canónico de un nuevo capítulo

```html
<section class="chapter" data-section="Nombre del capítulo">
  <div class="chapter-eyebrow">// Etiqueta de la sección</div>
  <h1 class="chapter-title">Título grande. <em>Acento italic.</em></h1>
  <p class="chapter-lede">
    Párrafo descriptivo italic que orienta al lector sobre qué encontrará en este capítulo.
  </p>

  <!-- Bloques de contenido específicos del capítulo -->
  <div class="hueco-block">...</div>
  <div class="hueco-block">...</div>

  <div class="section-eyebrow">// Sub-sección</div>
  <h2 class="h2-title">Sub-título <em>con accento.</em></h2>

  <!-- Más bloques -->
</section>
```

**Reglas duras:**
- Siempre `data-section` con un nombre corto
- Siempre `.chapter-eyebrow` antes del `.chapter-title`
- `.chapter-lede` es opcional pero recomendado para capítulos extensos
- Cada bloque destacado (`.hueco-block`, `.quote-block`, etc.) ya tiene `break-inside: avoid`
- **No inserts manuales** de `<div class="page">` ni saltos de página manuales — confía en Paged.js

---

## Cómo crear un reporte nuevo

1. **Copia el archivo de referencia:**
   ```bash
   cp ejemplo-rufino.html nuevo-reporte.html
   ```

2. **Cambia los datos de portada:**
   - `#número del diagnóstico` (próximo consecutivo)
   - Fecha
   - Categoría
   - URL evaluada
   - Título y lede
   - Stats (Comprabilidad actual, # ausencias, Proyección)
   - Pie de portada (NO incluye "Entregado por WhatsApp" — solo dominio + teléfono)

3. **Reemplaza el contenido de cada capítulo:**
   - Mantén la estructura de los 8 capítulos
   - Reemplaza el contenido específico (texto, números, citas)
   - Si un capítulo no aplica (ej: no hay riesgo regulatorio), elimínalo o reemplázalo
   - Si necesitas un capítulo nuevo, sigue el patrón canónico

4. **Actualiza la matemática del puntaje:**
   - Comprabilidad agregada en portada + resumen ejecutivo
   - Dispersión
   - Puntajes de cada dimensión en la tabla
   - Predicción post-ajustes
   - Las coordenadas del polígono SVG del radar chart (ver cálculo en `ejemplo-rufino.html` líneas con `<polygon points=...>`)

5. **Verifica que cada cita tenga sustento:**
   - Cada quote del panel debe llevar perfil completo (nombre, edad, ciudad, NSE, ocupación)
   - Cada dato citado debe tener fuente en `.cite` (ej: "ENDUTIH 2024", "CONDUSEF Reporte Anual 2024")
   - La sección de fuentes consultadas debe listar TODAS las que aparecen en las citas

6. **Genera el PDF:**
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless --disable-gpu \
     --no-pdf-header-footer \
     --print-to-pdf-no-header \
     --print-to-pdf="/tmp/reporte-XXXX.pdf" \
     --virtual-time-budget=30000 \
     --run-all-compositor-stages-before-draw \
     --hide-scrollbars \
     "file:///ruta/al/reporte.html"
   ```

7. **Verifica el PDF:**
   - Cada capítulo empieza en página propia
   - Cada bloque sigue completo en una página (no se corta a la mitad)
   - Numeración correcta (1 / N hasta N / N)
   - Encabezado y pie de página repetidos con el nombre del capítulo

---

## Reglas críticas (no negociables)

1. **Honestidad metodológica.** Cada reporte debe incluir el capítulo de cierre con:
   - Caveats explícitos (qué NO captura el diagnóstico)
   - Lista de fuentes consultadas
   - Reconocimiento de los límites del método

2. **Cada cita atribuida a un perfil debe corresponder a un perfil del panel de 19.** Si la cita no proviene del panel oficial (ej: análisis interno), márcalo claramente.

3. **Cada número en el reporte debe ser trazable a una fuente.** Si dices "73% del C busca registro CONDUSEF", esa cifra debe estar respaldada por ENDUTIH 2024 o equivalente. Si es estimación, dilo.

4. **No uses jerga sin definirla.** "Comprabilidad", "FGMX-Score", "BARS" deben tener contexto en el reporte o ser obvios.

5. **No prometas lo que el diagnóstico no puede entregar.** El método detecta problemas estructurales en mensajes; no predice ventas, no reemplaza humanos, no es muestra representativa.

6. **NO incluyas "Entregado por WhatsApp" en la portada.** La portada solo lleva dominio + teléfono. El detalle del canal de entrega es operacional, no parte del reporte.

7. **El CTA final siempre debe ofrecer el siguiente paso accionable** ("sprint de implementación", "diagnóstico de seguimiento", "ronda de A/B testing", etc.). El reporte no es el fin — es la entrada al siguiente engagement.

---

## Roadmap del template

Próximas mejoras posibles:

- **Migrar de polyfill a `pagedjs-cli`** cuando volumen lo justifique — corre en Node, no requiere navegador, más rápido y predecible para producción
- **Migrar a WeasyPrint** (Python) si necesitamos generar reportes desde un servicio backend sin Chrome
- **Sistema de variables/templating** (Handlebars o similar) para no editar HTML manualmente
- **Página de índice** opcional para reportes largos (>12 capítulos)
- **Versión de portada con foto/screenshot** del material evaluado (cuando aplique)
- **Códigos QR** para enlazar al reporte en línea desde la versión impresa

---

## Archivos en este directorio

- **`ESTRUCTURA.md`** — Este documento (referencia canónica)
- **`ejemplo-rufino.html`** — Reporte completo de referencia (#2155, Rufino, 29 mayo 2026)

Cualquier reporte nuevo se construye copiando `ejemplo-rufino.html` y siguiendo las reglas de este documento.
