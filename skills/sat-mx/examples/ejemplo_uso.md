# Ejemplo de uso — sat-mx

## Conversación típica

**Usuario:**
> Necesito mi Constancia de Situación Fiscal, me la pide un cliente nuevo.

**Claude:**
> Te ayudo. Voy a usar el skill `sat-mx`. Antes de empezar:
>
> 1. Tus credenciales se usan **solo en tu computadora**. No salen de aquí.
> 2. ¿Ya corriste `bash scripts/setup.sh` alguna vez? Si es tu primera vez, hay que hacerlo.
>
> Para descargar la Constancia necesito:
> - Tu **RFC**
> - Tu **contraseña CIEC** (la que usas en el portal del SAT)
> - Dónde quieres guardar el PDF (default: `~/Downloads/constancia-{rfc}-{fecha}.pdf`)

**Usuario:**
> RFC: XAXX010101000, CIEC: mipassword123, guárdalo en ~/Downloads/

**Claude:**
> Corriendo. Te va a pedir resolver un captcha en consola — escribe lo que ves en la imagen.

```bash
SAT_RFC="XAXX010101000" \
SAT_CIEC="mipassword123" \
SAT_OUTPUT="$HOME/Downloads/constancia-XAXX010101000-2026-06-07.pdf" \
php scripts/descargar_csf.php
```

```
→ Conectando al portal SAT…
→ Resolviendo captcha y autenticando…
  (si aparece el captcha, escribe lo que ves y presiona Enter)

[imagen ASCII del captcha]
Captcha: a8k2n

✓ Constancia descargada: /Users/luis/Downloads/constancia-XAXX010101000-2026-06-07.pdf (94823 bytes)
```

**Claude:** Listo. Parseando datos…

```bash
python3 scripts/parse_pdf.py ~/Downloads/constancia-XAXX010101000-2026-06-07.pdf
```

> **Constancia descargada en:** `~/Downloads/constancia-XAXX010101000-2026-06-07.pdf`
>
> **Resumen:**
> - **RFC:** XAXX010101000
> - **Nombre:** Tu nombre aquí
> - **Régimen:** Personas Físicas con Actividades Empresariales
> - **Domicilio:** Calle X #123, Col. Centro, CP 64000, Monterrey, Nuevo León
> - **Obligaciones activas:** 3
> - **Fecha de emisión:** 07/06/2026
>
> ¿Quieres que también te baje la Opinión de Cumplimiento?

---

## Caso licitación

**Usuario:**
> Tengo licitación mañana, me piden Opinión positiva con fecha del día.

**Claude:**
> Voy con la Opinión. Mismo flujo: RFC, CIEC, captcha.

```bash
SAT_RFC="..." SAT_CIEC="..." SAT_OUTPUT="$HOME/Downloads/opinion-2026-06-07.pdf" \
php scripts/descargar_opinion.php
```

> **Opinión descargada:** `~/Downloads/opinion-2026-06-07.pdf`
>
> ✅ **Sentido: POSITIVA**
> Folio: 12ABC34567
> Fecha emisión: 07/06/2026
>
> Lista para la licitación.

---

## Si el SAT cambió la plataforma

**Claude:**
> El scraper devolvió error: "Could not parse SAT response".
>
> Esto pasa cuando el SAT modifica su portal. La organización phpcfdi suele actualizar la librería en pocos días — revisa o reporta en:
> https://github.com/phpcfdi/csf-sat-scraper/issues
>
> Mientras tanto, no podré descargarte el PDF automáticamente.
