---
name: focus-mx-report-generator
description: Genera un reporte Focus MX en PDF (diagnóstico de pre-test publicitario) aplicado al material del cliente. Usa la arquitectura Paged.js + template editorial canónico. ESTE SKILL ES PRIVADO de Sistemia — no se distribuye en el repo público de skills.
private: true
owner: Sistemia.mx · Luis Huerta
status: active · v2.0
---

# Focus MX Report Generator — skill interno

Genera el entregable canónico de Focus MX para un cliente que pagó un diagnóstico. La salida es un PDF editorial de ~7-9 páginas siguiendo la estructura documentada.

## Cuándo usar este skill

Cuando alguien dice cualquiera de estos:
- "Genera el reporte para [cliente/producto]"
- "Aplica Focus MX a esta página: [URL]"
- "Hazme el diagnóstico para [material del cliente]"
- "PDF de diagnóstico con el formato de [Rufino / ejemplo / nuestro template]"

## Recursos del skill

- **`ESTRUCTURA.md`** — Documentación canónica de la arquitectura del reporte
- **`ejemplo-rufino.html`** — Template HTML de referencia (Diagnóstico #2155 · Rufino)

## Procedimiento

1. **Confirma con el operador (Luis) qué material se evalúa:**
   - URL de la página o texto del cliente
   - Categoría declarada (servicio digital, fintech, retail, etc.)
   - Datos opcionales: ciudad, canal de distribución, presupuesto en juego

2. **Si la URL es accesible, usa WebFetch** para analizar el material. Si no, pide al operador que pegue el texto/captura.

3. **Aplica el método FGMX-Score:**
   - Identifica perfiles del panel relevantes (de los 19 documentados)
   - Calcula puntajes en cada una de las 7 dimensiones con sustento
   - Cita fuentes públicas (INEGI, AMAI, CONDUSEF, INAH, ENDUTIH, ENIGH, ENSANUT, CONEVAL, PROFECO QQP, PROFECO Anual, CIDE, Latinobarómetro, MOPRADEF, Censo Económico, ENOE, PRODECON)
   - Cuantifica el impacto (% del panel afectado, asimetría económica)

4. **Copia el template canónico:**
   ```bash
   cp /Volumes/Storage/sistemia-skills-mx/skills/focus-group-mx/report-template/ejemplo-rufino.html /tmp/reporte-XXXX.html
   ```

5. **Edita el HTML siguiendo las reglas de `ESTRUCTURA.md`:**
   - Cambia los datos de portada (#número, fecha, categoría, URL, título, lede, stats)
   - Reemplaza el contenido de cada uno de los 8 capítulos
   - Actualiza las coordenadas del polígono SVG del radar chart según los puntajes nuevos
   - NO incluyas "Entregado por WhatsApp" en la portada
   - Cada cita debe tener perfil completo
   - Cada número debe tener fuente

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
     "file:///tmp/reporte-XXXX.html"
   ```

7. **Manda el PDF al operador por Telegram** (Bot `Chombicode_bot`, chat_id `5668200045`).

## Reglas críticas (no negociables)

- Cada cita atribuida a un perfil debe corresponder a un perfil del panel de 19
- Cada número debe ser trazable a una fuente listada
- El capítulo de cierre siempre incluye caveats explícitos + fuentes consultadas + CTA al siguiente engagement ($15,000 MXN sprint)
- No prometas predicciones de venta, no claim de muestra representativa
- NO mencionar "Entregado por WhatsApp" en portada
- Mantén la voz: honesta, basada en datos, mexicana sin folclor

## Numeración de diagnósticos

Hasta hoy:
- #2155 — Rufino · 29 mayo 2026 (referencia canónica)

El próximo es #2156. Lleva control consecutivo al generar reportes nuevos.

## Privacidad

Este skill **NO se distribuye en el repo público `sistemia-skills-mx`**. Vive solo en local. El template, los recursos y la documentación son propiedad interna de Sistemia.

Si en algún momento decidimos abrir esto, primero limpiamos:
- Datos de clientes específicos
- Números de contacto WhatsApp
- Referencias a casos privados
