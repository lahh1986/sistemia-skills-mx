---
name: demografia-mx (preview)
description: |
  Versión preview pública. Documenta el método y queries de ejemplo. La base
  demografia.duckdb consolidada (CONAPO 1950-2070, 5.9M registros) está
  disponible bajo Sistemia. Para acceso completo (download o hosted), contacta.
---

# demografia-mx — preview

> Market sizing y proyecciones demográficas oficiales mexicanas, 1950-2070.
>
> **Esta es la versión preview.** Explica cómo funciona el skill. La base
> `demografia.duckdb` con 5.9M de registros consolidados de CONAPO no se
> distribuye en este repo público — la versión completa vive en Sistemia.
> [**Acceder vía WhatsApp**](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20demografia-mx).

---

## Qué hace este skill

Cuando preguntas algo como "¿cuántas mujeres 25-34 viven en Jalisco?" o "¿cuántos adultos mayores tendrá México en 2040?", `demografia-mx` consulta la Conciliación Demográfica + Proyecciones de Población de CONAPO (Secretaría de Gobernación) y te devuelve la cifra real con contexto:

- **Total + desglose por sexo**
- **Comparativo entre entidades** (top 3 más altos / bajos)
- **Trayectoria histórica + proyección futura**
- **Implicación de negocio** (TAM/SAM/SOM si aplica, ventana demográfica, etc.)

---

## Cobertura del dataset (versión completa)

| Dimensión | Cobertura |
|---|---|
| Periodo | **1950 → 2070** (121 años) |
| Granularidad temporal | Anual |
| Entidades | 32 + Nacional |
| Edad | Simple (0-100+, sin truncar) |
| Sexo | Hombres, Mujeres |
| Métricas | Población a mitad de año + esperanza de vida al nacer |
| Registros | ~5.9 millones |
| Fuente original | CONAPO Conciliación 1950-2019 + Proyecciones 2020-2070 |

---

## Ejemplo de uso

> **Tú:** "¿Cuántas mujeres 25-34 viven en Jalisco hoy?"

> **Claude Code (con `demografia-mx`):**
>
> **Respuesta: 668,400 mujeres** (2026, fuente CONAPO)
>
> | Métrica | Valor |
> |---|---|
> | Total Jalisco 25-34 (ambos sexos) | 1.3M |
> | Mujeres | 668,400 (51%) |
> | Hombres | 642,600 (49%) |
> | Como % de Jalisco total | 7.8% |
> | Como % nacional del segmento | 8.4% |
>
> **Trayectoria:** Este cohorte crece 0.9%/año hasta 2031 y empieza a contraerse. Ventana de adquisición: próximos 5 años.

---

## Versión preview vs completa

| Característica | Preview (este repo) | Completo (Sistemia) |
|---|---|---|
| Documentación + cheat sheet de queries | ✅ Sí | ✅ Sí |
| `scripts/query.sh` helper | ✅ Sí | ✅ Sí |
| `demografia.duckdb` (~24 MB) | ❌ No | ✅ Descarga directa o hosted |
| 121 años × 32 entidades × edades simples × sexos | ❌ No | ✅ Sí |
| Tablas derivadas (grupos AMAI, cohortes) | ❌ No | ✅ Sí |
| Soporte para actualizar con cada nueva Proyección CONAPO | ❌ No | ✅ Sí |

---

## Cómo conseguir la versión completa

→ [Escríbenos por WhatsApp](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20demografia-mx) y te paso opciones:

1. **Servicio hosted** (queries por API o desde Claude Code, sin setup)
2. **Descarga del `.duckdb`** (24 MB, corres local)

Si solo necesitas un análisis puntual ("dame el TAM de mi target"), también vendemos consultas individuales sin suscripción.

---

## Instalación (preview)

```bash
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cp -r sistemia-skills-mx/skills/demografia-mx ~/.claude/skills/demografia-mx-preview
```

Sin el `.duckdb`, los queries fallan con `Catalog Error: Table 'poblacion' does not exist`. La documentación de cómo construirlo desde Excel CONAPO se incluye en una próxima versión open source.

---

*Preview liberado bajo MIT. La consolidación del corpus CONAPO en `demografia.duckdb`, las tablas derivadas y el pipeline de refresco son producto comercial de Sistemia.*
