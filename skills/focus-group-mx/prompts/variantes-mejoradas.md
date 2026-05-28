# Prompt: Generación de 3 Variantes Mejoradas

> Cómo generar 3 variantes del copy original que atacan las dimensiones más débiles
> identificadas por el FGMX-Score grupal.

---

## Principio rector

Una variante NO es "el copy original con un cambio cosmético". Una variante:

1. **Identifica la dimensión más débil** del scoring (la menor)
2. **Implementa un cambio fundamental** que ataca esa dimensión
3. **Preserva las fortalezas** existentes (no quema lo que sí funciona)
4. **Es concreta y publicable** — no abstracta, no "más auténtico"
5. **Tiene Buyability proyectado** explícito

---

## Workflow de generación

### Paso 1: Identificar las 3 dimensiones más débiles

Tomar el análisis por dimensión de `sintesis-grupo.md`. Ordenar de menor a mayor.

Ejemplo:
| Dimensión | Promedio target |
|---|---:|
| Diferenciación | 5.3 ⚠️ |
| Emocional | 5.8 🟡 |
| Intención | 5.8 🟡 |
| Relevancia | 6.5 🟡 |
| Credibilidad | 6.8 ✅ |
| Affordability | 7.3 ✅ |
| Comprensión | 8.3 ✅ |

**Las 3 dimensiones a atacar:**
1. Diferenciación (5.3)
2. Emocional (5.8)
3. Intención (5.8)

### Paso 2: Identificar las fortalezas a preservar

Las 2-3 dimensiones más altas. No tocar lo que sí funciona.

Ejemplo:
- ✅ Comprensión 8.3 — el mensaje es claro, NO complicarlo
- ✅ Affordability 7.3 — el precio funciona, NO cambiarlo
- ✅ Credibilidad 6.8 — la marca es creíble, NO arriesgar tono

### Paso 3: Generar Variante A (ataca dimensión #1 más débil)

**Para cada dimensión débil, hay tácticas conocidas:**

#### Si Diferenciación es débil:
- Agregar **prueba específica única** del producto vs competencia
  ("Lo único que se hornea con leña real" vs "Hecho con amor")
- Reposicionar contra un competidor específico nombrado
- Cambiar el hero shot a algo nadie más usa
- Agregar mención de patente/certificación/exclusividad

#### Si Emocional es débil:
- Agregar narrativa humana específica (caso real, no genérico)
- Cambiar el hero protagonista a alguien con quien target se identifica
- Agregar tensión y resolución (problema → solución personal)
- Cambiar música/tono a algo más reconocible culturalmente

#### Si Relevancia es débil:
- Re-anclar el copy al momento de vida del target (no genérico)
- Mencionar contexto temporal específico ("este fin de mes", "antes de regreso a clases")
- Cambiar pronombres ("tú" vs "usted" vs "ustedes") según target
- Agregar referencia regional ("aquí en Monterrey", "los Edomex sabemos")

#### Si Credibilidad es débil:
- Reducir hyperbole (cambiar "el mejor" por dato específico)
- Agregar social proof (números reales, testimonios)
- Mencionar respaldo institucional o tradición
- Quitar palabras que disparan desconfianza ("garantizado", "milagroso")

#### Si Affordability es débil:
- Cambiar precio principal por **precio mensual / por uso**
- Agregar comparación útil ("menos que un café diario")
- Agregar opción de financiamiento explícita
- Hacer visible el costo-beneficio total

#### Si Intención es débil:
- Agregar **call to action más concreto** y urgente
- Reducir fricción (eliminar pasos, agregar 1-click)
- Especificar **dónde y cuándo** comprarlo
- Agregar incentivo de urgencia genuino (no falso)

#### Si Comprensión es débil:
- Reducir copy 30-50%
- Reordenar para que la promesa principal esté primero
- Reducir tecnicismos
- Cambiar a un solo mensaje principal (no 3-4 mensajes)

### Paso 4: Formato de salida por variante

```markdown
### Variante A — [Nombre descriptivo del cambio]

**Dimensión atacada:** Diferenciación 5.3 → 7.2 (+1.9)
**Buyability proyectado:** 7.4 (+1.6 vs original 5.8)
**Cambio fundamental:** [Una frase explicando qué cambió]

#### Copy

[COPY COMPLETO y publicable. No abstracto. Como se vería en el ad real.]

#### Justificación

- **Por qué sube Diferenciación:** [específico]
- **Por qué no quema fortalezas:** [específico]
- **Riesgo a vigilar:** [si lo hay]
```

### Paso 5: Generar Variante B (ataca dimensión #2 más débil)

Mismo formato. Diferente táctica.

### Paso 6: Generar Variante C (ataca dimensión #3 más débil O hace dos a la vez)

Si las dos dimensiones débiles tienen tácticas compatibles, una variante puede
atacar ambas. Si no, atacar la tercera.

---

## Reglas críticas

### 1. NO inventar features del producto

Si el producto NO tiene una certificación, NO la inventes en la variante.
Si NO es el más rápido, NO digas que lo es. Las variantes mejoran el COPY,
no el producto.

### 2. NO ser abstracto

❌ "Hacer el ad más auténtico"
✅ "Cambiar 'familia perfecta' por 'familia que pelea por la mesa'"

❌ "Mejorar el call to action"
✅ "Cambiar 'Conoce más' por 'Pídelo a tu Oxxo de la esquina'"

### 3. Mantener voz original

Si la marca es seria/corporativa, no propongas variante chistosa.
Si es juvenil, no la conviertes en formal.

### 4. Calcular Buyability proyectado de forma realista

Buyability proyectado = recalcular con SCORING.md pesos, asumiendo la nueva
puntuación en la dimensión atacada + sin cambios en otras dimensiones.

Ejemplo:
- Original: Diferenciación 5.3 → Buyability 5.8
- Variante A sube Diferenciación a 7.2, otras dimensiones igual
- Nueva Buyability = (8.3×Wcompr) + (6.5×Wrelev) + ... + (7.2×Wdif) + ...
- = 7.4 (con pesos consumo_masivo)

**SI** el cambio quita algo de otra dimensión (ej. cambiar precio sube
Affordability pero podría bajar Credibilidad), reflejarlo.

### 5. Ordenar variantes por Buyability proyectado

Variante A debe tener el delta más alto. Variante C el más bajo (pero >0).

### 6. Explicar el "no quemar fortalezas"

Si la variante mantiene las fortalezas, dilo explícito. El cliente necesita
saber que no estás sacrificando lo que sí funciona.

---

## Ejemplo completo

**Original (consumo masivo, Aurrera):**
> "Aurrera, lo nuevo y lo de siempre. Más por menos."

**Scoring del original:**
- Comprensión 8.3 ✅
- Relevancia 6.5 🟡
- Credibilidad 6.8 ✅
- **Diferenciación 5.3 ⚠️** ← más débil
- **Emocional 5.8 🟡**
- Affordability 7.3 ✅
- Intención 5.8 🟡

**Buyability:** 6.4 (pesos consumo_masivo)

---

### Variante A — Reposicionamiento generacional

**Dimensión atacada:** Diferenciación 5.3 → 7.5 (+2.2)
**Buyability proyectado:** 7.0 (+0.6 vs 6.4)
**Cambio fundamental:** Diferenciar como la tienda "que no me hace sentir mal por comprar barato".

#### Copy

> "Aurrera es Aurrera. Sin pena. Sin floreo. Sin diseñador de moda escogiéndote
> la pasta de dientes. Aquí cuidas tu quincena como debe ser: con dignidad."

#### Justificación

- **Por qué sube Diferenciación:** Aurrera ahora no es "más por menos" (eso lo dice Walmart). Es "sin pena" — único territorio emocional.
- **Por qué no quema fortalezas:** Mantiene affordability ("cuidas tu quincena") y credibilidad ("Aurrera es Aurrera" = familiaridad).
- **Riesgo a vigilar:** Puede sentirse defensivo. Probar con María Fer y Lupita primero.

---

### Variante B — Anchor de comparación cultural

**Dimensión atacada:** Emocional 5.8 → 7.4 (+1.6)
**Buyability proyectado:** 6.8 (+0.4)
**Cambio fundamental:** Agregar narrativa familiar de fin de mes.

#### Copy

> "La quincena ya casi se acaba pero el frijol no se acaba.
> Aurrera porque tu mesa no espera al lunes."

#### Justificación

- **Por qué sube Emocional:** Toca tensión real (quincena se acaba) + resolución cotidiana (mesa que no espera). Cualquier mexicana C-/D+ lo siente.
- **Por qué no quema fortalezas:** Mantiene comprensión simple (2 frases), affordability implícito ("no se acaba").
- **Riesgo a vigilar:** Podría sentirse paternalista si no se acompaña con visual digno.

---

### Variante C — CTA con anclaje regional

**Dimensión atacada:** Intención 5.8 → 7.0 (+1.2)
**Buyability proyectado:** 6.7 (+0.3)
**Cambio fundamental:** Mover de "marca general" a "tu Aurrera específica".

#### Copy

> "Aurrera de Ecatepec. Aurrera de Iztapalapa. Aurrera de Tlaquepaque.
> Cada mercado mexicano tiene su Aurrera. Búscala — todos los días te conviene."

#### Justificación

- **Por qué sube Intención:** Hace tangible la acción ("búscala") + anchor geográfico personaliza.
- **Por qué no quema fortalezas:** Mantiene credibilidad (lista de geografías reales = familia).
- **Riesgo a vigilar:** Puede sentirse excluyente para mercados no listados — solución: rotar geografías por región.

---

## Anti-patterns

### ❌ Variante cosmética
"Cambiar el color del CTA de azul a rojo." → No es variante, es A/B testing visual. Variante = cambio sustantivo.

### ❌ Variante que adivina
"Si pusieran una mamá millennial con un bebé sería mejor." → ¿Por qué? Sin razón fundamentada en scores, es opinión.

### ❌ Variante sin proyección
"Esto sería mejor." → Mejor cuánto? En qué dimensión? Buyability proyectado obligatorio.

### ❌ Tres variantes con la misma táctica
Si las 3 variantes solo cambian el slogan principal, no son variantes — son
parafraseo. Cada variante debe atacar una dimensión distinta.

### ❌ Variante que ignora el dossier original

Si las personas del focus group dijeron específicamente "el precio no cabe",
ignorar Affordability en las variantes = malinterpretar el feedback.

---

## Output final esperado

Al usuario entregar:

```markdown
## 3 Variantes Mejoradas

### Variante A — [Nombre]
**Buyability proyectado:** X.X (+Y vs original)
**Dimensión atacada:** [Dim] [original] → [proyectado]

[Copy completo]

[Justificación]

### Variante B — [Nombre]
[...]

### Variante C — [Nombre]
[...]

## Recomendación

Implementar **Variante {X}** primero porque [razón específica].

A/B testing sugerido: original vs Variante {X} con 50/50 split, presupuesto
mínimo $5,000 MXN por 7 días para significancia.
```
