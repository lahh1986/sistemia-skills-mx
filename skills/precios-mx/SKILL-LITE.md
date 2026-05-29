---
name: precios-mx (preview)
description: |
  Versión preview pública. Documenta el método y los outputs esperados pero
  NO incluye la base precios.duckdb (916 MB, 10.5M registros). Para acceso
  completo al DB (descarga directa o servicio gestionado), contacta a
  Sistemia.
---

# precios-mx — preview

> Consulta precios reales mexicanos por colonia, cadena y periodo.
>
> **Esta es la versión preview.** Documenta cómo funciona el skill, pero el DB
> consolidado de 10.5 millones de capturas PROFECO **no está incluido en este
> repo público** (pesa 916 MB). Para acceso al DB completo (descarga o servicio
> gestionado), ve a [**WhatsApp Sistemia**](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20precios-mx).

---

## Qué hace este skill

Cuando le preguntas a Claude Code algo como "¿cuánto cuesta un kilo de tortilla en Iztapalapa?" o "¿dónde es más barata la Coca-Cola en Monterrey?", `precios-mx` activa un wrapper sobre la base **Quién es Quién en los Precios** de PROFECO (programa público desde 2002, capturas en sitio de retail mexicano).

Devuelve:
- **Mediana, mínimo, máximo** del SKU en la zona y periodo
- **Top 3 cadenas más baratas** y más caras
- **Comparativo por estado** si la pregunta es geográfica
- **Tendencia histórica** del precio
- **Recomendación accionable** (no solo datos)

---

## Cobertura del dataset (versión completa)

| Dimensión | Cobertura |
|---|---|
| Capturas totales | **10.5 millones** |
| Periodo | 2024-01-02 → 2026-02-28 |
| Productos | 911 SKUs (catálogo PROFECO) |
| Cadenas | 231 (Walmart, Soriana, Aurrera, Chedraui, La Comer, Costco, Sam's, HEB, OXXO, etc.) |
| Estados | 31 + CDMX |
| Granularidad geo | Estado · Municipio · Lat/Lon de la sucursal |
| Cadencia de actualización | Semanal (con cron en versión hosted) |

---

## Ejemplo de uso

> **Tú:** "¿Dónde es más barato el aceite Capullo 850 ml en Guadalajara?"

> **Claude Code (con `precios-mx`):**
>
> | Cadena | Sucursal | Precio | Fecha |
> |---|---|---|---|
> | Bodega Aurrera | Av. López Mateos | $44.50 | 2026-02-21 |
> | Walmart | Plaza México | $46.90 | 2026-02-19 |
> | Soriana | Plaza del Sol | $48.50 | 2026-02-18 |
>
> **Mediana últimos 90 días en ZMG:** $47.20
> **Insight:** Bodega Aurrera consistentemente 5-8% bajo de la mediana en ZMG. Ahorro estimado vs Walmart para una familia: $25/mes en aceite básico.

---

## Versión preview vs completa

| Característica | Preview (este repo) | Completo (Sistemia) |
|---|---|---|
| Documentación del método | ✅ Sí | ✅ Sí |
| Script `scripts/query.sh` | ✅ Sí | ✅ Sí |
| `precios.duckdb` (916 MB) | ❌ No | ✅ Descarga directa o acceso hosted |
| 10.5M capturas | ❌ No | ✅ Sí |
| Actualización semanal | ❌ No | ✅ Sí (versión hosted) |
| Soporte | Comunidad GitHub Issues | Directo (WhatsApp/email) |
| Diccionario de campos | ❌ No | ✅ `profeco_qqp_diccionario.csv` |

---

## Cómo conseguir la versión completa

Dos opciones para acceder al DB:

**1. Servicio hosted** — usas mi infra. Cero setup, queries por API o desde Claude Code. Pricing por volumen.
**2. Descarga del DB** — bajas el `.duckdb` una sola vez, corre localmente. Pricing por dataset.

→ [Escríbenos por WhatsApp](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20precios-mx) y te paso opciones + precios.

---

## Instalación (preview)

```bash
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cd sistemia-skills-mx
cp -r skills/precios-mx ~/.claude/skills/precios-mx-preview
```

Sin el `.duckdb`, el script `query.sh` te indica que falta el DB. Para construirlo tú mismo desde PROFECO bruto (datos.gob.mx), se publicará un `scripts/build_db.py` open source en una próxima versión.

---

*Preview liberado bajo MIT. La base `precios.duckdb` consolidada, el catálogo de equivalencias entre cadenas, y el diccionario de productos son producto comercial de Sistemia.*
