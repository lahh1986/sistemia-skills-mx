---
name: sat-mx
description: |
  Descarga la Constancia de Situación Fiscal y la Opinión de Cumplimiento del SAT México
  desde Claude Code. Entrega el PDF más los datos parseados (RFC, régimen, domicilio,
  código postal, obligaciones fiscales, fecha de emisión). Las credenciales del usuario
  (RFC + CIEC) jamás salen de su computadora.
---

# SAT MX

> Bájate tu Constancia de Situación Fiscal y Opinión de Cumplimiento sin entrar al portal del SAT.

Por debajo orquesta dos librerías de **phpcfdi** (la comunidad PHP más reconocida de México para temas SAT/CFDI):
- `phpcfdi/csf-sat-scraper` — descarga la Constancia
- `phpcfdi/opinion-cumplimiento-sat-scraper` — descarga la Opinión de Cumplimiento

Sistemia agrega la orquestación + parseo del PDF a datos estructurados.

---

## Cuándo activar este skill

Activa este skill cuando el usuario pida cualquiera de estas cosas (con variaciones de redacción):

- "Bájame mi Constancia de Situación Fiscal"
- "Necesito mi CSF"
- "Descarga mi Opinión de Cumplimiento"
- "Mi opinión 32-D"
- "Saca mi 32-D positiva"
- "Bájame los papeles del SAT que me pide [cliente]"
- "Tengo licitación, necesito Opinión positiva del día"
- "Tráeme la constancia con los datos parseados"

**No activar si:**
- El usuario pide algo de **e.firma** (.cer/.key) — este skill solo funciona con CIEC
- El usuario pide **declarar impuestos** o cualquier trámite escritural — esto solo descarga PDFs informativos
- El usuario pide validar facturas CFDI — eso es otro skill (`cfdi-validator`)

---

## Flujo de uso (pasos exactos a seguir)

### Paso 0 — Setup (correr una sola vez)

Antes del primer uso, ejecuta el setup:

```bash
bash scripts/setup.sh
```

Este script:
1. Verifica que PHP 8.2+ esté instalado (si no, guía al usuario para instalarlo via `brew` en Mac o `apt` en Linux)
2. Verifica que Composer esté instalado (si no, lo instala)
3. Corre `composer install` dentro del directorio del skill para bajar las librerías de phpcfdi
4. Verifica que `pdftotext` (de `poppler`) esté disponible para el parseo (si no, sugiere `brew install poppler` o `apt install poppler-utils`)

Si algún paso falla, **detente y reporta al usuario qué le falta instalar** — no intentes seguir.

### Paso 1 — Pedir credenciales (cada vez, nunca persistir)

Solicita al usuario:
1. **RFC** (13 caracteres persona física, 12 caracteres moral)
2. **Contraseña CIEC** (la que usa en el portal del SAT)

**Reglas críticas de seguridad:**
- Nunca guardes la CIEC en ningún archivo
- Nunca incluyas la CIEC en respuestas de texto al usuario (ni en ejemplos, ni en confirmación)
- Pásala únicamente como variable de ambiente al script PHP, no como argumento de línea de comandos (los args aparecen en `ps`)
- Avisa explícitamente al usuario: "Tus credenciales se usan solo en tu computadora. No salen de aquí, no llegan a Anthropic ni a Sistemia."

### Paso 2 — Ejecutar el scraper

**Para Constancia de Situación Fiscal:**

```bash
SAT_RFC="<RFC>" SAT_CIEC="<CIEC>" SAT_OUTPUT="<ruta_pdf>" php scripts/descargar_csf.php
```

**Para Opinión de Cumplimiento:**

```bash
SAT_RFC="<RFC>" SAT_CIEC="<CIEC>" SAT_OUTPUT="<ruta_pdf>" php scripts/descargar_opinion.php
```

**Sobre el captcha:**
El SAT pide resolver un captcha visual. El script lo imprime como ASCII art en la consola. El usuario debe leerlo y escribir la solución. Si falla, vuelve a intentar — el captcha se regenera.

Si el usuario quiere automatizar el captcha (servicios como 2captcha o anti-captcha), avísale que tendrá que configurar `SAT_CAPTCHA_PROVIDER` y `SAT_CAPTCHA_KEY` — está documentado en el README pero no es default.

### Paso 3 — Parsear el PDF

Después de descargar, corre el parser para extraer los datos a JSON:

```bash
python3 scripts/parse_pdf.py <ruta_pdf>
```

Devuelve algo así:

```json
{
  "tipo": "constancia_situacion_fiscal",
  "rfc": "XAXX010101000",
  "nombre": "...",
  "regimen_fiscal": "...",
  "domicilio": {
    "calle": "...",
    "colonia": "...",
    "municipio": "...",
    "entidad": "...",
    "codigo_postal": "..."
  },
  "obligaciones": ["..."],
  "fecha_emision": "YYYY-MM-DD"
}
```

Para Opinión de Cumplimiento, devuelve:

```json
{
  "tipo": "opinion_cumplimiento",
  "rfc": "XAXX010101000",
  "sentido": "POSITIVA | NEGATIVA | NO_INSCRITO",
  "fecha_emision": "YYYY-MM-DD",
  "folio": "..."
}
```

### Paso 4 — Entregar al usuario

Responde con:
- Ruta del PDF descargado
- Resumen legible de los datos parseados (no pegues el JSON crudo a menos que el usuario lo pida)
- Si es Opinión: destacar el **sentido** (positiva/negativa) con énfasis — es el dato que importa

---

## Errores comunes y cómo manejarlos

| Error | Causa probable | Qué decir al usuario |
|---|---|---|
| `Las credenciales son incorrectas` | RFC o CIEC mal escritos | "El SAT rechazó las credenciales. Verifica tu RFC y CIEC y volvemos a intentar." |
| `El captcha no es válido` | Mal tipeado el captcha | "El captcha no coincidió, generemos uno nuevo." (vuelve a correr) |
| `Could not parse response` | El SAT cambió su HTML | "El portal del SAT cambió. Hay que esperar a que phpcfdi actualice la librería — suele tardar pocos días. Reporta en https://github.com/phpcfdi/csf-sat-scraper/issues" |
| `Connection timeout` | Portal SAT caído (pasa seguido) | "El portal del SAT no responde. Vuelve a intentar en unos minutos." |
| `PHP not found` | Setup incompleto | "Necesitas correr `bash scripts/setup.sh` primero." |

---

## Lo que SÍ y NO hace este skill

**SÍ:**
- Descarga Constancia de Situación Fiscal (PDF)
- Descarga Opinión de Cumplimiento (PDF)
- Parsea ambos a JSON estructurado
- Funciona con RFC + CIEC
- Todo corre local — credenciales no salen de la máquina

**NO:**
- No reemplaza a un contador
- No funciona con e.firma (.cer/.key)
- No guarda credenciales en ningún lado
- No declara impuestos ni hace ningún trámite escritural
- No descarga otros documentos del SAT (acuses, declaraciones, facturas)

---

## Créditos

Este skill se apoya completamente en el trabajo de [**phpcfdi**](https://www.phpcfdi.com) y sus mantenedores (Cesar Aguilera et al.). Si el skill te ahorra tiempo, considera dejar una star en sus repos:

- https://github.com/phpcfdi/csf-sat-scraper
- https://github.com/phpcfdi/opinion-cumplimiento-sat-scraper

---

## Licencia

MIT (heredada de phpcfdi). El skill mismo es de Sistemia y se distribuye sin costo desde [El Tianguis](https://eltianguis.sistemia.mx/s/sat-mx).
