---
name: demografia-mx
description: |
  Usar cuando el usuario quiera hacer MARKET SIZING o consultas demográficas
  precisas para México por edad, sexo, entidad, año (incluyendo proyecciones
  hasta 2070). Cubre 32 entidades + nacional, edades 0-100+, sexo, periodo
  1950-2070, con datos CONAPO Conciliación Demográfica oficial. Ideal para:
  TAM/SAM/SOM por target, planeación de cohortes, ventana demográfica, bono
  demográfico, esperanza de vida, comparativos entre estados.

  Triggers: "cuántas personas X edad", "mujeres 25-34 en Guadalajara",
  "tamaño de mercado", "market sizing México", "cuántos jóvenes hay en",
  "proyección de población", "bono demográfico", "envejecimiento México",
  "pirámide poblacional", "esperanza de vida", "TAM México", "cohorte",
  "CONAPO", "censo INEGI", "demografía MX".
---

# demografia-mx — Consultas demográficas oficiales México (1950-2070)

> Wrapper sobre `demografia.duckdb`, construido desde la **Conciliación
> Demográfica 1950-2019 + Proyecciones de Población 2020-2070** del CONAPO
> (Secretaría de Gobernación). Granularidad: año × entidad × edad simple ×
> sexo. Total: ~5.9 millones de renglones × 32 entidades + nacional.

## Cuándo activarte

- El usuario pregunta tamaño de un segmento demográfico ("¿cuántas mujeres 25-34 viven en Guadalajara?")
- El usuario quiere market sizing: TAM/SAM/SOM por edad/género/entidad
- El usuario quiere comparar tamaño poblacional entre estados, generaciones o años
- El usuario quiere proyecciones futuras (cuántos serán adultos mayores en 2040, etc.)
- El usuario pregunta sobre bono demográfico, envejecimiento, pirámide poblacional
- El usuario menciona CONAPO, proyecciones, esperanza de vida, fecundidad

**NO actives si:** el usuario pregunta densidad poblacional por colonia/CP exacta. CONAPO va hasta entidad. Para colonia necesitas Censo INEGI 2020 (no incluido aún — pendiente para v1.1).

## Cobertura del dataset

| Dimensión | Cobertura |
|---|---|
| Periodo | 1950 – 2070 (121 años) |
| Granularidad temporal | Anual |
| Entidades | 32 + Nacional (33 totales) |
| Edad | Simple (0-100+, sin truncar) |
| Sexo | Hombres, Mujeres |
| Métricas | Población a mitad de año, esperanza de vida al nacer |
| Fuente original | CONAPO Conciliación 1950-2019 + Proyecciones 2020-2070 |

**Tablas en `demografia.duckdb`:**
- `poblacion` — granular (año, entidad, edad simple, sexo, población)
- `esperanza_vida` — esperanza al nacer por año/entidad/sexo
- Vistas: `poblacion_total`, `poblacion_por_grupo` (grupos: 0-4, 5-14, 15-17, 18-24, 25-34, 35-44, 45-54, 55-64, 65+)

## Workflow

### Paso 1: Identifica intent

| Caso | Pregunta del usuario | Query base |
|---|---|---|
| A. **Cohorte simple** | "¿Cuántas mujeres 25-34 hay en Jalisco?" | `SELECT SUM(poblacion) FROM poblacion WHERE anio=2025 AND sexo='Mujeres' AND edad BETWEEN 25 AND 34 AND entidad='Jalisco'` |
| B. **Comparativo entre estados** | "¿Dónde hay más jóvenes 18-24 por habitante?" | Por entidad: ratio (18-24) / total |
| C. **Proyección futura** | "¿Cuántos adultos mayores tendrá MX en 2040?" | `WHERE anio=2040 AND edad>=65` |
| D. **Tendencia histórica** | "¿Cómo ha crecido el grupo 30-40 en CDMX?" | Series por año, edad agrupada |
| E. **Bono demográfico** | "¿Cuándo termina el bono?" | Ratio dependencia: (0-14 + 65+) / (15-64) |
| F. **Pirámide poblacional** | "Dame la pirámide de Nuevo León 2025" | Group by edad bucket × sexo |

### Paso 2: Consulta

**Path al DB:** `/Volumes/Storage/sistemia-skills-mx/research/demografia.duckdb`

**Si el DB no existe**, córrelo primero:
```bash
python3 ~/sistemia-skills-mx/skills/demografia-mx/scripts/build_db.py
```
(tarda ~2 min; requiere `openpyxl` y `duckdb` en Python).

**Helper:**
```bash
~/sistemia-skills-mx/skills/demografia-mx/scripts/query.sh "<SQL>"
```

**Convenciones:**
- Año por defecto: si el usuario no lo especifica, usa el año actual (2026 hoy).
- Entidades: usa el nombre exacto CONAPO (`Ciudad de México` con acento, `Nuevo León`, `Yucatán`, etc. — ver `data/entidades.json`).
- Cuando el usuario diga "México" sin estado, usa `entidad = 'República Mexicana'` (es el agregado nacional).
- Para market sizing realista, NO te limites a "viven ahí". Considera también penetración del producto (combina con `precios-mx` o `habitos-digitales-mx`).

### Paso 3: Output al usuario

```markdown
## {{Pregunta interpretada}}

**Respuesta: {{N}} personas** ({{año}}, fuente CONAPO)

### Desglose
| Métrica | Valor |
| Total | {{N}} |
| Hombres | {{Nh}} ({{%}}) |
| Mujeres | {{Nm}} ({{%}}) |
| Como % de la entidad | {{%}} |
| Como % nacional | {{%}} |

### Comparativo
{{Top 3 entidades con más / menos del mismo segmento}}

### Trayectoria
{{año -5 / actual / año +5 / año +15}}

### Lectura para tu pregunta
{{1-2 líneas con la implicación de negocio}}
```

### Paso 4: Implicación accionable

Cierra siempre con la **implicación**:
- "Tu TAM mexicano de {{segmento}} es {{N}}. Si tu producto tiene CAC de $X y LTV de $Y, necesitas penetrar {{P%}} para cubrir un mercado de {{Z}} MXN."
- "Este segmento crece a {{%}} anual hasta {{año}} y empieza a contraerse. Tu ventana de adquisición está en los próximos {{X}} años."
- "En {{entidad}} este segmento es {{X%}} mayor por capita que el promedio nacional. Sesgo geográfico claro para asignar presupuesto."

## Ejemplos clave de queries (cheat sheet)

```sql
-- Población actual de un segmento específico
SELECT SUM(poblacion) AS n
FROM poblacion
WHERE anio = 2026
  AND entidad = 'Jalisco'
  AND sexo = 'Mujeres'
  AND edad BETWEEN 25 AND 34;

-- Pirámide poblacional de una entidad
SELECT grupo_edad, sexo, poblacion
FROM poblacion_por_grupo
WHERE anio = 2026 AND entidad = 'Nuevo León'
ORDER BY grupo_edad, sexo;

-- Comparativo nacional: cuántos jóvenes 18-30 por entidad
SELECT entidad,
       SUM(CASE WHEN edad BETWEEN 18 AND 30 THEN poblacion ELSE 0 END) AS jovenes,
       SUM(poblacion) AS total,
       100.0 * SUM(CASE WHEN edad BETWEEN 18 AND 30 THEN poblacion ELSE 0 END) / SUM(poblacion) AS pct
FROM poblacion
WHERE anio = 2026 AND entidad != 'República Mexicana'
GROUP BY entidad
ORDER BY pct DESC;

-- Ratio de dependencia (medida del bono demográfico)
SELECT anio,
       SUM(CASE WHEN edad < 15 OR edad >= 65 THEN poblacion ELSE 0 END) * 100.0
         / SUM(CASE WHEN edad BETWEEN 15 AND 64 THEN poblacion ELSE 0 END) AS dependencia
FROM poblacion
WHERE entidad = 'República Mexicana'
GROUP BY anio
ORDER BY anio;

-- Proyección de adultos mayores 2025 vs 2050
SELECT anio, SUM(poblacion) AS adultos_mayores
FROM poblacion
WHERE entidad = 'República Mexicana' AND edad >= 65 AND anio IN (2025, 2040, 2050, 2070)
GROUP BY anio
ORDER BY anio;
```

## Lo que NO hace este skill

- **No baja a colonia/CP/AGEB.** Para eso necesitas Censo INEGI 2020 (pendiente — v1.1 agregará scripts para descargarlo).
- **No es ingreso ni gasto.** Para eso → `nse-mx` o queries directas a ENIGH.
- **No es migración bilateral.** Para flujos remesas/migración usa el reporte BBVA Anuario Migración Remesas 2024 (`research/bbva/`).
- **Las proyecciones >2030 tienen incertidumbre creciente.** CONAPO publica intervalos de confianza en el documento metodológico pero las proyecciones puntuales son la mejor estimación.

## Fuentes

- **CONAPO Conciliación Demográfica 1950-2019 + Proyecciones 2020-2070** (DOF actualización 2023-04). Path: `research/conapo/conapo_conciliacion_demografica_proyecciones_2020_2070.zip` (extraído en `research/conapo/extracted/`).
- Para densidad submunicipal: **Censo de Población y Vivienda 2020 INEGI** (pendiente — v1.1).
- Indicadores: `research/conapo/extracted/.../5_Indicadores_demográficos_proyecciones.xlsx`.
