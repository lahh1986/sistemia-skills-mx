# Prompt: Síntesis Grupal con FGMX-Score Agregado

> Cómo agregar los YAMLs individuales de N personas en un análisis ejecutivo.

---

## Input esperado

N archivos YAML (uno por persona del focus group), cada uno con la estructura
descrita en `evaluacion-individual.md`.

## Pasos de la síntesis

### Paso 1 — Calcular Buyability ponderado por persona

Para cada persona, aplicar pesos de su `categoria_producto` desde SCORING.md:

```python
# Pseudocódigo
PESOS = {
    "consumo_masivo": {"comprension": 0.15, "relevancia": 0.20, "credibilidad": 0.10,
                       "diferenciacion": 0.05, "emocional": 0.15, "affordability": 0.25,
                       "intencion_compra": 0.10},
    "premium_lujo":   {"comprension": 0.10, "relevancia": 0.15, "credibilidad": 0.15,
                       "diferenciacion": 0.20, "emocional": 0.20, "affordability": 0.10,
                       "intencion_compra": 0.10},
    # ... otras 12 categorías en SCORING.md
    "default":        {"comprension": 0.15, "relevancia": 0.20, "credibilidad": 0.15,
                       "diferenciacion": 0.10, "emocional": 0.15, "affordability": 0.15,
                       "intencion_compra": 0.10},
}

def buyability(persona_scores, categoria):
    pesos = PESOS.get(categoria, PESOS["default"])
    return sum(persona_scores[dim] * peso for dim, peso in pesos.items())
```

Buyability redondeado a 1 decimal.

### Paso 2 — Tabla heatmap persona × dimensión

```markdown
| Persona | NSE | Compr | Relev | Cred | Dif | Emoc | Afford | Int | **Buyability** |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| Andrea | A/B | 9 | 7 | 7 | 6 | 7 | 8 | 6 | **7.1** |
| Rodrigo | A/B | 9 | 5 | 6 | 4 | 4 | 8 | 5 | **5.8** |
| Mariana **[CONTROL]** | C+ | 8 | 3 | 6 | 3 | 4 | 2 | 2 | **3.8** |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | **...** |
```

**Convención visual:**
- Scores 0-3: ⚠️ (problema)
- Scores 4-5: 🟡 (mediocre)
- Scores 6-7: 🟢 (sano)
- Scores 8-10: ⭐ (excelente)

Si la tabla es muy ancha, usa colores en markdown o emoji.

### Paso 3 — Calcular promedios separados

**Buyability target real:** promedio de personas con `es_target: true`
**Buyability controles:** promedio de personas con `es_target: false`
**Spread:** `buyability_target - buyability_controles`

Interpretación del spread:
- **Spread ≥3:** Ad bien targeteado. Target ama, no-target no.
- **Spread 1-3:** Ad genérico. Funciona pero no diferencia.
- **Spread <1:** ⚠️ Ad mal targeteado. Reevaluar paso 1 o recategorizar producto.
- **Spread negativo:** 🚨 Ad atrae a NO-target más que a target. Crítico replantear.

### Paso 4 — Análisis por dimensión

Para cada una de las 7 dimensiones, calcular promedio del target:

```markdown
| Dimensión | Promedio target | Status | Insight |
|---|---:|:-:|---|
| Comprensión | 8.3 | ✅ | Mensaje claro, no requiere ajuste |
| Relevancia | 6.5 | 🟡 | Aceptable pero no fuerte |
| Credibilidad | 6.8 | ✅ | Promesa creíble |
| Diferenciación | 5.3 | ⚠️ | Cliché — competidor podría decir lo mismo |
| Emocional | 5.8 | 🟡 | Frío, falta conexión |
| Affordability | 7.3 | ✅ | Cabe en presupuesto target |
| Intención | 5.8 | 🟡 | Compra dudosa sin trigger adicional |
```

**Status criterios:**
- ✅ ≥7
- 🟡 5-6.9
- ⚠️ 3-4.9
- 🚨 <3

### Paso 5 — Patrones detectados

Buscar:

**A) Deal-breakers (todas/casi todas las personas mencionaron):**
- Extraer de `razones_top_3` de cada persona
- Si una crítica aparece en ≥60% de las personas target, es deal-breaker
- Quotearla textualmente (cita literal de una persona)

**B) Lo que sí jala (todas reaccionaron positivo):**
- Extraer aspectos mencionados positivamente en ≥60% de las personas target
- Quotearlo

**C) Polarización (opiniones opuestas entre personas):**
- Si la varianza de una dimensión >3 puntos entre personas target
- Reportar: "Andrea (8) vs Daniel (3) — el ad polariza por edad/región"

### Paso 6 — Detección de problemas

Buscar señales específicas en los YAMLs:

#### 6.1 Cultural mismatch
Busca en `reaccion_inicial` y `razones_top_3` quotes que mencionen:
- "Se siente gringo"
- "Es traducción"
- "No suena mexicano"
- "Esa palabra no la usamos"
- "El acento del modelo no es de aquí"

Si aparece en ≥2 personas, reportar como problema cultural.

#### 6.2 Affordability gap
Busca cuando `affordability < 4` en personas target. Si ≥40% de target tiene
affordability bajo, el precio está mal posicionado.

#### 6.3 Clasismo/machismo/edadismo
Busca quotes que mencionen:
- "Solo sale gente fresa / blanca"
- "Como si las mujeres solo sirviéramos para..."
- "Sale puro joven"
- "Es gente como ellos, no como nosotros"

Reportar literalmente.

#### 6.4 Confusión de vocabulario
Si ≥30% de las personas mencionan no entender una palabra/concepto, reportar.

### Paso 7 — Resumen ejecutivo

3 líneas máximo, al inicio del output:

```markdown
## Resumen ejecutivo

**Buyability target: 6.5/10** — Lanzable pero con ajustes.
**Hallazgo crítico:** Diferenciación débil (5.3) — el ad podría ser de cualquier competidor.
**Recomendación:** Implementar Variante B (subir Diferenciación a 7.2).
```

### Paso 8 — Output completo al usuario

Estructura final:

```markdown
# Evaluación Focus Group MX

## Resumen ejecutivo
[3 líneas]

## Personas seleccionadas (N personas)
**Target real:** Andrea, Rodrigo, Mariana, Daniel
**Controles de rechazo:** María Fer, Doña Rosa

## Heatmap de scores
[Tabla persona × dimensión × Buyability]

## Promedios
- Target real: 6.5/10
- Controles: 3.8/10
- Spread: 2.7 ✅ sano

## Análisis por dimensión
[Tabla con status por dimensión]

## Patrones detectados
- Deal-breaker: "..."
- Lo que sí jala: "..."
- Polarización: "..."

## Problemas detectados
- Cultural mismatch: ...
- Affordability gap: ...
- Etc.

## 3 variantes mejoradas
[Generadas con prompts/variantes-mejoradas.md]

## Canales recomendados
[Basado en personas que reaccionaron positivo]

## Limitaciones del análisis
- N personas evaluadas: X de 14 del pool
- Personas faltantes en target: [...]
- Generación pendiente: [si aplica]
```

---

## Reglas de la síntesis

1. **No promediar entre target y controles.** Siempre separar.
2. **Quotear literalmente** de los YAMLs individuales, no parafrasear.
3. **Citar dimensión específica** al reportar un problema (no "está mal", sí "Diferenciación 4.2").
4. **Reportar limitaciones honestas** — si solo evaluaron 4 personas, decirlo.
5. **Ordenar variantes** por impacto esperado en Buyability (variante con mejor delta primero).

---

## Heurística para "lanzable / no lanzable"

| Buyability target | Recomendación |
|---|---|
| ≥8.0 | 🚀 Lanzar con confianza alta. Considerar A/B con presupuesto fuerte. |
| 7.0-7.9 | ✅ Lanzar con A/B test estándar. |
| 6.0-6.9 | 🟡 Lanzar mid-funnel únicamente. Iterar para conversión. |
| 5.0-5.9 | ⚠️ NO lanzar todavía. Implementar variante mejorada primero. |
| <5.0 | 🚨 Replantear desde brief. El ad fundamentalmente no convence. |
