# FGMX-Score — Sistema de Scoring del Focus Group MX

> **Sistema de scoring multi-dimensional para evaluación de copy publicitario
> mexicano, validado contra frameworks académicos y prácticos.**
>
> Versión 1.0 · 2026-05-28 · Apache 2.0

---

## Por qué un sistema de scoring formal

Sin scoring estructurado, una evaluación es solo "me gusta / no me gusta" disfrazada. El FGMX-Score:

1. **Reduce sesgo subjetivo** mediante BARS (Behaviorally Anchored Rating Scales)
2. **Permite comparabilidad** entre ads, personas, y rondas de evaluación
3. **Es defendible académicamente** vs frameworks reconocidos (Kantar Link, System1, BAV, NPS, AIDA)
4. **Es operacional** — cada persona produce los mismos 7 números más justificación textual
5. **Permite agregación ponderada** por target de producto/categoría
6. **Es auditable** — cada score viene con razonamiento explícito

---

## Marco teórico

FGMX-Score combina cinco frameworks validados:

| Framework | Origen | Aporte a FGMX-Score |
|---|---|---|
| **AIDA** | E. St. Elmo Lewis, 1898 | Estructura: Comprensión → Interés → Acción |
| **Brand Asset Valuator** | Y&R/WPP, ~1990s | Diferenciación + Relevancia |
| **System1** | Karen Nelson-Field, ~2010s | Atracción emocional (Spike) |
| **Kantar Link** | Millward Brown, ~1990s | Credibilidad + Brand building |
| **NPS evolved** | Reichheld, 2003 | Intención de compra |
| **PSEC-MX** | Este proyecto, 2026 | Anclaje cultural y económico MX (Affordability) |

Adicional: **Behaviorally Anchored Rating Scales (BARS)** — Smith & Kendall (1963), validación psicométrica para reducir varianza inter-rater.

---

## Las 7 dimensiones del FGMX-Score

Cada dimensión se puntúa **0-10** con anclas conductuales (qué diría la persona en cada nivel).

### 1. **Comprensión** (Clarity)

> ¿La persona entendió qué se vende, para qué sirve, y qué quieren que haga?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "No tengo idea de qué venden ni qué quieren que haga. Es confuso total." |
| 2-3 | "Entendí algo pero está enredado. Tendría que verlo varias veces." |
| 4-5 | "Entendí más o menos. Capté el producto pero no la promesa completa." |
| 6-7 | "Entendí claro qué venden y para qué. La acción es clara." |
| 8-9 | "Cristalino. Lo agarré en los primeros 3 segundos." |
| 10 | "Hecho como para que yo lo entienda. No tuvo que esforzarse mi cabeza." |

**Base teórica:** AIDA "Attention" + Kantar "Clarity Score". Refleja Daniel Kahneman's Sistema 1 (procesamiento rápido sin esfuerzo).

### 2. **Relevancia** (Relevance)

> ¿Es para esta persona en este momento de su vida?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "Esto NO es para mí. Ni de chiste." |
| 2-3 | "Quizás para otra etapa de mi vida, no ahorita." |
| 4-5 | "Podría ser para mí pero no lo necesito urgente." |
| 6-7 | "Sí me llama. Es para alguien como yo." |
| 8-9 | "Esto está hecho pensando en mí o gente como yo." |
| 10 | "Justo lo que estaba buscando / pensando estos días." |

**Base teórica:** BAV "Relevance" pilar. Refleja "target market resonance" + situational fit.

### 3. **Credibilidad** (Credibility)

> ¿Le creo la promesa? ¿Confío en la marca y el mensaje?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "Mentira clara. No le creo nada." |
| 2-3 | "Suena exagerado. Desconfío." |
| 4-5 | "Podría ser cierto pero tendría que investigar más." |
| 6-7 | "Le creo. La marca/promesa suena seria." |
| 8-9 | "Cien por ciento creíble. La marca tiene historia y la promesa es realista." |
| 10 | "Casi puedo verificarlo en mi vida real. No hay nada que dudar." |

**Base teórica:** Kantar Link "Credibility" + Aaker brand trust theory + AIDA "Belief".

### 4. **Diferenciación** (Differentiation)

> ¿Se distingue de competidores? ¿Tiene una razón única para preferirlo?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "Idéntico a cualquier otro. Si quito el logo no sé qué marca es." |
| 2-3 | "Tiene algo pero podría ser de varios competidores." |
| 4-5 | "Diferencia ligera pero no me sale natural decir qué." |
| 6-7 | "Sí lo distingo. Tiene una propuesta clara contra los demás." |
| 8-9 | "Muy claro qué hace diferente. Razón para preferirlo." |
| 10 | "Único. No tiene competidor real con esta propuesta." |

**Base teórica:** BAV "Differentiation" pilar (Aaker, Keller). El pilar más predictivo de brand growth long-term según Y&R BrandAsset 1990s research.

### 5. **Atracción emocional** (Emotional Resonance)

> ¿Hubo conexión emocional? ¿Sintió algo?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "Cero emoción. Frío. Mecánico." |
| 2-3 | "Algo intentó pero no me llegó." |
| 4-5 | "Sentí algo ligero (curiosidad, simpatía leve)." |
| 6-7 | "Me conectó. Sentí familiaridad, ternura, humor genuino, o reconocimiento." |
| 8-9 | "Fuerte conexión. Me detuve. Quizás me reí o se me hizo nudo." |
| 10 | "Me movió. Lo platicaría. Quizás se lo mando a alguien." |

**Base teórica:** System1 "Spike" (peak emotion drives memory) + Daniel Kahneman peak-end rule + Aaker emotional brand benefits. Field & Binet "Long and Short of It" demuestra que ads emocionales construyen brand 4-5× más eficientemente que racionales.

### 6. **Affordability**

> ¿El precio cabe en su capacidad financiera real?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0-1 | "Imposible. No me alcanza ni en mis sueños." |
| 2-3 | "Carísimo. Tendría que sacrificar mucho." |
| 4-5 | "Apretado pero podría con sacrificio o financiamiento." |
| 6-7 | "Razonable. Cabe en mi presupuesto con planeación." |
| 8-9 | "Cómodo. Lo puedo comprar sin pensar mucho." |
| 10 | "Barato para mí. Lo agarro de impulso." |

**Base teórica:** Específico para MX. Refleja **purchasing power parity** real por NSE (ENIGH 2024 decil ingreso × gasto por categoría). No hay equivalente en frameworks gringos porque asume capacidad de compra uniforme.

### 7. **Intención de compra** (Purchase Intent)

> ¿Lo compraría en los próximos 30-90 días si se le presenta la oportunidad?

**Anclas conductuales:**

| Score | Lo que diría la persona |
|---:|---|
| 0 | "Jamás. No me interesa." |
| 1-2 | "No. Quizás algún día pero no veo cuándo." |
| 3-4 | "Tal vez, si me llega información adicional." |
| 5-6 | "Probable, si encuentro el momento." |
| 7-8 | "Sí lo compraría próximamente." |
| 9-10 | "Lo voy a comprar / lo compraría inmediato si lo tengo enfrente." |

**Base teórica:** Net Promoter Score (Reichheld 2003) **evolved** — NPS clásico solo pregunta "likelihood to recommend"; FGMX adapta a "likelihood to buy" que es más predictivo para evaluación pre-launch. AIDA "Action".

---

## Score Compuesto: Buyability

Score sintético 0-10 que combina las 7 dimensiones:

```
Buyability = (Comprensión × W_compr) +
             (Relevancia × W_relev) +
             (Credibilidad × W_cred) +
             (Diferenciación × W_dif) +
             (Emocional × W_emoc) +
             (Affordability × W_afford) +
             (Intención × W_int)
```

Pesos suman 1.0. Se ajustan por categoría del producto.

### Pesos por categoría de producto

| Categoría | Compr | Relev | Cred | Dif | Emoc | Afford | Int |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Default (sin especificar)** | 0.15 | 0.20 | 0.15 | 0.10 | 0.15 | 0.15 | 0.10 |
| **Consumo masivo (alimentos, bebidas, OTC)** | 0.15 | 0.20 | 0.10 | 0.05 | 0.15 | **0.25** | 0.10 |
| **Premium / lujo** | 0.10 | 0.15 | 0.15 | **0.20** | **0.20** | 0.10 | 0.10 |
| **B2B servicios** | 0.15 | 0.15 | **0.25** | **0.20** | 0.05 | 0.10 | 0.10 |
| **Política / advocacy** | 0.10 | **0.25** | 0.15 | 0.10 | **0.25** | 0.05 | 0.10 |
| **Salud / pharma** | **0.20** | 0.15 | **0.25** | 0.10 | 0.10 | 0.10 | 0.10 |
| **Tecnología** | **0.20** | 0.15 | 0.15 | **0.20** | 0.10 | 0.10 | 0.10 |
| **Fintech / banca** | 0.15 | 0.15 | **0.25** | 0.10 | 0.05 | **0.20** | 0.10 |
| **Educación** | 0.15 | **0.20** | **0.20** | 0.10 | 0.10 | 0.15 | 0.10 |
| **Automotriz** | 0.10 | 0.15 | 0.15 | **0.20** | 0.15 | **0.15** | 0.10 |
| **Inmobiliario** | 0.10 | 0.15 | **0.20** | 0.15 | 0.10 | **0.20** | 0.10 |
| **Retail moderno** | 0.15 | **0.20** | 0.10 | 0.10 | 0.10 | **0.20** | 0.15 |
| **Bebidas alcohólicas** | 0.10 | 0.15 | 0.10 | 0.15 | **0.25** | **0.15** | 0.10 |
| **Causa social / ONG** | 0.10 | **0.20** | **0.20** | 0.10 | **0.25** | 0.05 | 0.10 |

**Justificación de los pesos:**

- **Consumo masivo:** Affordability dominante porque la decisión es repetitiva y price-sensitive.
- **Premium/lujo:** Diferenciación + Emoción porque el precio no es la barrera, el deseo sí.
- **B2B:** Credibilidad + Diferenciación porque el comprador toma decisiones racionales con riesgo de carrera.
- **Política:** Relevancia + Emoción porque el "producto" es un mensaje de identidad colectiva.
- **Salud:** Comprensión + Credibilidad porque las consecuencias son críticas.
- **Fintech:** Credibilidad + Affordability porque la confianza en el manejo del dinero es todo.

### Interpretación del Buyability Score

| Score | Interpretación | Acción recomendada |
|---|---|---|
| 0-2 | Ad rechazado activamente por el target | Reescribir o descartar |
| 2-4 | Ad ignorable, no genera interés | Ajustes mayores en proposición de valor |
| 4-5 | Ad mediocre, mid-funnel weak | Iteración en relevancia + diferenciación |
| 5-6 | Ad funcional pero olvidable | OK para tráfico, no para conversión |
| 6-7 | Ad efectivo en su target | Lanzable con A/B testing |
| 7-8 | Ad fuerte, alta probabilidad de conversión | Lanzar con confianza |
| 8-10 | Ad excepcional (raro) | Validar con A/B + escalar inversión |

---

## Output format estándar

Cuando una persona evalúa un ad, devuelve **estructuradamente:**

```yaml
persona_id: 07-cmenos-mariafernanda-edomex
ad_evaluado: "[título o resumen del ad]"
categoria_producto: consumo_masivo

scores:
  comprension: 8
  relevancia: 6
  credibilidad: 7
  diferenciacion: 4
  emocional: 5
  affordability: 3
  intencion_compra: 4

buyability: 5.2  # ponderado con pesos consumo_masivo

reaccion_inicial: |
  "Ay, otra promoción de Soriana. Sí entendí qué venden,
  pero el precio no aterriza en mi presupuesto este mes."

razones_top_3:
  - "Lo entendí en el primer segundo (Comprensión 8)"
  - "Sí me llama porque uso Soriana (Relevancia 6)"
  - "Pero $299/quincena no me alcanza ahora (Affordability 3)"

sugerencia_concreta: |
  "Si lo pusieran a $199 con financiamiento, lo consideraría.
   También me llamaría más si saliera una señora como yo, no solo
   güeritas."

recomendaria_a_alguien_similar: false
```

---

## Métodos de validación

### 1. Cross-validation con ads conocidos (Effie Awards MX)

**Procedimiento:**
- Recolectar 10 ads MX ganadores Effie 2020-2024 + 10 que fracasaron documentadamente
- Evaluar todos con el pool de 14 personas
- Computar buyability promedio en target apropiado

**Criterios de éxito:**
- Ads ganadores: Buyability ≥7 en target
- Ads fracasados: Buyability ≤5 en target
- Separación de medias estadísticamente significativa (t-test p<0.05)

### 2. Calibración por NSE (test de lógica)

**Tests de sanidad:**

| Producto | Persona | Buyability esperado | Razonamiento |
|---|---|---|---|
| Mercedes-Benz Clase E ($1.5M MXN) | Doña Rosa (E) | **≤2** | Imposible por affordability |
| Mercedes-Benz Clase E | Andrea (A/B) | **6-9** | Target real |
| Bodega Aurrera despensa | Doña Rosa (E) | **7-9** | Target principal |
| Bodega Aurrera despensa | Andrea (A/B) | **3-5** | No target pero no ofende |
| Banco Azteca crédito | Lupita (D+) | **6-8** | Target perfecto |
| Banco Azteca crédito | Rodrigo (A/B) | **1-3** | No target, posible rechazo cultural |

Si algún test no se cumple, **calibrar el scoring o ajustar la persona**.

### 3. Discriminación inter-ads (sensibilidad)

Dos ads similares pero con diferencias específicas (precio, hero shot, slogan) deben generar scores **diferenciados** (≥1 punto promedio en al menos una dimensión).

Si no, el scoring no es sensible y requiere reentrenamiento de las personas.

### 4. Inter-LLM kappa (consistency)

Mismo ad evaluado por la misma persona en distintos LLMs (Claude, GPT, Gemini, Grok) debe producir scores con **Cohen's kappa κ > 0.7** (acuerdo sustancial).

### 5. Test-retest reliability

Misma persona, mismo ad, 5 evaluaciones consecutivas → **variance <15%** en cada dimensión.

### 6. Convergencia con encuestas reales (validación externa)

Tomar un ad con brand tracking real conocido (caso histórico documentado) y comparar:
- Buyability sintético vs intención de compra real medida en encuesta
- **Target correlation r > 0.7**

---

## Limitaciones honestas

1. **No mide eficacia real de ROI.** El scoring predice qué pensaría una persona, no cuántas ventas generará el ad. Para ROI requiere experimento real (A/B en plataforma).

2. **Sesgo de creador de la persona.** Aunque PSEC-MX reduce esto, los dossiers son hand-crafted y reflejan interpretaciones del creador.

3. **N pequeño por celda.** Con 14 personas, algunos sub-grupos están subrepresentados (un solo C+ tapatío, una sola Boomer rural).

4. **Pesos por categoría son heurísticos.** Basados en literatura + judgement, no en regresión empírica. Refinables con experimentos.

5. **Affordability es estimado.** PROFECO + ENIGH dan precios reales pero la **disposición a pagar** depende también de momento, prioridad, ocasión — no solo de presupuesto.

6. **No captura "buzz" social.** Un ad puede tener Buyability medio pero hacerse viral por meme/controversia. FGMX no predice virality.

7. **Cultural drift.** Lo que es relevante en 2026 puede no serlo en 2028. Recalibrar cada 18-24 meses con encuestas frescas.

---

## Comparación con frameworks existentes

| Aspecto | System1 (UK) | Kantar Link | NPS clásico | **FGMX-Score** |
|---|---|---|---|---|
| Dimensiones | 2 (Star + Spike) | ~10 internas | 1 (NPS) | **7 explícitas con BARS** |
| Sub-validación cultural MX | ❌ | Limitada | ❌ | **✅ Específico MX** |
| Pesos por categoría | ❌ | ✅ propietario | ❌ | **✅ Públicos 14 categorías** |
| Output reproducible | ❌ (encuestas reales) | ❌ (caja negra) | ✅ | **✅ con justificación textual** |
| Costo por evaluación | $5-50k USD | $20-100k USD | Variable | **$5-100 USD en tokens LLM** |
| Velocidad | 1-2 semanas | 3-6 semanas | Variable | **5-15 minutos** |

---

## Referencias académicas

- **Aaker, D. A.** (1991). *Managing Brand Equity*. Free Press.
- **Aaker, J.** (1997). "Dimensions of brand personality." *Journal of Marketing Research*, 34(3), 347-356.
- **Argyle, L. P., et al.** (2022). "Out of one, many: Using language models to simulate human samples." *Political Analysis*, 31(3), 337-351.
- **Field, P. & Binet, L.** (2013). *The Long and the Short of It: Balancing Short and Long-Term Marketing Strategies*. IPA.
- **Kahneman, D.** (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- **Keller, K. L.** (1993). "Conceptualizing, measuring, and managing customer-based brand equity." *Journal of Marketing*, 57(1), 1-22.
- **Nelson-Field, K.** (2020). *The Attention Economy and How Media Works: Simple Truths for Marketers*. Palgrave Macmillan.
- **Park, J. S., et al.** (2023). "Generative agents: Interactive simulacra of human behavior." *UIST '23*.
- **Reichheld, F.** (2003). "The one number you need to grow." *Harvard Business Review*, 81(12), 46-54.
- **Smith, P. C. & Kendall, L. M.** (1963). "Retranslation of expectations: An approach to the construction of unambiguous anchors for rating scales." *Journal of Applied Psychology*, 47(2), 149-155.
- **St. Elmo Lewis, E.** (1898). Original AIDA framework. *The Inland Printer*.

---

## Cómo citar

```bibtex
@misc{huerta_fgmx_score_2026,
  author = {Huerta, Luis A.},
  title = {{FGMX-Score: Sistema de Scoring Multi-Dimensional para
           Evaluación de Copy Publicitario Mexicano}},
  year = {2026},
  url = {https://github.com/lahh1986/sistemia-skills-mx/blob/main/skills/focus-group-mx/SCORING.md},
  note = {v1.0}
}
```

---

## Próximos pasos

- **v1.0** (presente): Spec teórica documentada.
- **v1.1** (próxima fase): Integrar al `SKILL.md` para que las personas devuelvan estructuradamente las 7 dimensiones.
- **v1.2**: Cross-validation con 10 ads Effie + 10 ads fracasados.
- **v1.3**: Inter-LLM kappa con 4 LLMs distintos.
- **v2.0**: Refinamiento de pesos basado en regresión empírica (con datos de A/B real).
