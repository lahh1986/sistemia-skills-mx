---
name: focus-group-mx
description: |
  Usar cuando el usuario quiera EVALUAR copy publicitario, anuncios, landing pages,
  posts de redes sociales, o cualquier material de marketing dirigido al mercado
  mexicano ANTES de gastar en ads. El skill activa un focus group sintético con
  19 personas mexicanas (NSE A/B → E × género × generación × región × voto 2024)
  que evalúan el material y devuelven FGMX-Score (7 dimensiones + Buyability ponderado).

  Triggers: "evalúa este anuncio", "qué opinarían los mexicanos", "focus group",
  "antes de lanzar el ad", "este copy funcionaría", "revisa esta landing",
  "panel de personas mexicanas", "validación de copy MX", "personas sintéticas",
  "antes de gastar en ads", "test de mensaje", "FGMX-Score".
---

# Focus Group MX — Skill principal v2.0

> 19 personas mexicanas validadas con PSEC-MX (ENIGH 2024 + AMAI + PROFECO + INE 2024)
> evalúan tu copy con **FGMX-Score** (7 dimensiones + Buyability ponderado).
>
> **v2.0 changelog**: +5 personas para cerrar gaps estructurales:
> Lourdes (A/B patrimonial heredada CDMX) · Diego (C+ Maynecista urbano CDMX) ·
> Pilar (C panista bastión católica Ags) · Mauricio (C medio CDMX millennial varón) ·
> Adriana (C+ Jal cristiana evangélica Maynecista). Distribución 11 Sheinbaum / 6 Xóchitl
> / 2 Máynez ahora refleja mejor el electorado real 2024.

## Cuándo activarte

- El usuario te muestra un anuncio (texto, imagen, video) y pide opinión sobre si funcionará en MX
- El usuario te pasa un landing page o link y pregunta cómo mejorarla
- El usuario está por gastar en ads digitales (Meta, Google, TikTok) y quiere validar primero
- El usuario menciona "focus group", "validar copy", "personas mexicanas", "antes de lanzar"
- El usuario te pasa copy para WhatsApp Business, Instagram, Facebook, TikTok ads
- El usuario quiere probar un naming, slogan, tagline, headline
- El usuario menciona "FGMX-Score", "scoring", "evaluar con métricas"

## Workflow

### Paso 1: Identificar producto + target + categoría

Antes de evaluar, identifica (pregunta o infiere):

- **¿Qué material es?** (Ad de Meta, post Instagram, landing, slogan, video, etc.)
- **¿Categoría del producto?** (Crítico para pesos del scoring)
  - `consumo_masivo` (alimentos, bebidas, OTC)
  - `premium_lujo`
  - `b2b_servicios`
  - `politica_advocacy`
  - `salud_pharma`
  - `tecnologia`
  - `fintech_banca`
  - `educacion`
  - `automotriz`
  - `inmobiliario`
  - `retail_moderno`
  - `bebidas_alcoholicas`
  - `causa_social_ong`
  - `default` (si no encaja en ninguna)
- **¿Precio aproximado?** (Crucial para NSE matching y Affordability)
- **¿Target hipotetizado?** (NSE, edad, género, región)
- **¿Vertical?** (B2C / B2B / mixto)

Si el usuario no lo da, infiere del material. Si tienes dudas, pregunta UNA vez antes de proceder.

### Paso 2: Seleccionar personas del pool (modelo C híbrido)

Lee `personas/metadata.json` y aplica reglas del selector:

**Modo Universal (las 14):** Para consumo masivo amplio (Coca-Cola, Bimbo, Sabritas).

**Modo Targeted (5-9 personas):** Para nicho. Cruza target con `categorias_compra_alta_propension`:
- Premium ($5,000+/mes): Andrea, Rodrigo + aspiracionales (Mariana/Daniel)
- Mid-market ($500-5,000): Mariana, Daniel, Karla, Jorge, María Fer
- Masivo barato (<$500): María Fer, Hugo, Lupita, Ramón, Doña Rosa, Brayan
- Bottom-of-pyramid: Lupita, Doña Rosa, Brayan, Sofía, Don Tomás
- B2B servicios: Andrea, Rodrigo, Daniel, Karla

**Modo Custom (con flagging):** Si target requiere perfil ausente del pool:
> "Tu target son [X]. Pool tiene 2 personas relevantes (Y, Z). ¿Procedo con 2, genero ad-hoc, o expandimos pool?"

**Control de rechazo:** SIEMPRE incluir 1-2 personas NO-target para detectar repulsión social. Ejemplos:
- Tesla → incluir María Fer/Hugo como control (no compradores pero ¿genera respeto o asco?)
- Aurrera → incluir Andrea como control (¿no la ofende? ¿se siente clasista?)

### Paso 3: Justificar selección al usuario

ANTES de evaluar, explica brevemente:
> "Categoría detectada: `premium_lujo` (auto >$1M MXN). Selección: Andrea (A/B NL),
> Rodrigo (A/B CDMX), Mariana (C+ JAL) y Daniel (C+ QRO) como compradores/aspiracionales.
> María Fer (C-) y Doña Rosa (D) como controles de rechazo social. Skip: 8 personas
> claramente fuera de target. Proceeding..."

### Paso 4: Cada persona evalúa con FGMX-Score

Para cada persona seleccionada, lee su dossier completo + `SCORING.md` + sigue
`prompts/evaluacion-individual.md`.

**Output esperado por persona** (YAML estructurado):

```yaml
persona_id: 07-cmenos-mariafernanda-edomex
ad_evaluado: "[hash o resumen breve]"
categoria_producto: consumo_masivo

scores:
  comprension: 8       # 0-10 según BARS de SCORING.md
  relevancia: 6
  credibilidad: 7
  diferenciacion: 4
  emocional: 5
  affordability: 3
  intencion_compra: 4

buyability: 5.2   # calculado con pesos categoria_producto

reaccion_inicial: |
  "[Frase corta en VOZ de la persona — primera persona — gut reaction]"

razones_top_3:
  - "Lo entendí en el primer segundo (Comprensión 8)"
  - "Sí me llama porque uso Soriana (Relevancia 6)"
  - "Pero $299 no me alcanza ahora (Affordability 3)"

sugerencia_concreta: |
  "[Qué cambio específico haría comprable — en voz de la persona]"

recomendaria_a_alguien_similar: false

es_target: true   # o false si es persona de control
```

### Paso 5: Sintetizar resultados (FGMX agregado)

Sigue `prompts/sintesis-grupo.md`. Output esperado:

**Tabla heatmap de scores por persona × dimensión:**

| Persona | Compr | Relev | Cred | Dif | Emoc | Afford | Int | **Buyability** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|
| Andrea (A/B) | 9 | 7 | 7 | 6 | 7 | 8 | 6 | **7.1** |
| Rodrigo (A/B) | 9 | 5 | 6 | 4 | 4 | 8 | 5 | **5.8** |
| Mariana (C+) | 8 | 8 | 7 | 6 | 7 | 7 | 7 | **7.2** |
| Daniel (C+) | 7 | 6 | 7 | 5 | 5 | 6 | 5 | **5.9** |
| María Fer (C-) **[CONTROL]** | 8 | 3 | 6 | 3 | 4 | 2 | 2 | **3.8** |

**Promedios:**
- **Buyability target (4 personas):** 6.5/10
- **Buyability controles (1 persona):** 3.8/10
- **Spread target-control:** 2.7 (sano: si fuera <1.0 sería alarma de mal targeting)

**Análisis por dimensión:**

| Dimensión | Promedio target | Insight |
|---|---:|---|
| Comprensión | 8.3 | ✅ Mensaje claro |
| Relevancia | 6.5 | ⚠️ Aceptable pero no fuerte |
| Credibilidad | 6.8 | ✅ Promesa creíble |
| Diferenciación | 5.3 | ⚠️ Cliché — el competidor podría decir lo mismo |
| Emocional | 5.8 | ⚠️ Frío, falta conexión |
| Affordability | 7.3 | ✅ Cabe en presupuesto target |
| Intención | 5.8 | ⚠️ Compra dudosa sin trigger adicional |

**Patrones detectados:**
- **Deal-breakers (todas/casi todas las personas mencionaron):** [...]
- **Lo que sí jala (todas reaccionaron positivo):** [...]
- **Polarización (opiniones opuestas):** [...]

**Detección de problemas:**
- ¿Cultural mismatch ("se siente gringo/traducido")? [Sí/No con quotes]
- ¿Affordability gap (target dice "no me alcanza")? [Sí/No]
- ¿Clasismo/machismo/edadismo no intencional? [Sí/No con quotes]
- ¿Confusión de vocabulario o idioma? [Sí/No]

### Paso 6: Generar 3 variantes mejoradas

Sigue `prompts/variantes-mejoradas.md`. Cada variante debe:

1. Abordar la dimensión MÁS débil del scoring (la más baja)
2. Mantener fortalezas existentes (no quemar lo que sí funciona)
3. Ser concreta y publicable (no abstracta)

**Output esperado:**

```markdown
### Variante A — [tema del cambio]
**Buyability proyectado:** 7.4 (+1.6 vs original)
**Dimensión mejorada:** Emocional 5.8 → 7.5

[Copy específico aquí, listo para usar]

### Variante B — [tema del cambio]
**Buyability proyectado:** 7.1 (+1.3 vs original)
**Dimensión mejorada:** Diferenciación 5.3 → 7.2

[Copy específico aquí]

### Variante C — [tema del cambio]
**Buyability proyectado:** 6.8 (+1.0 vs original)
**Dimensión mejorada:** Affordability 7.3 → 8.5 (anchor reducido)

[Copy específico aquí]
```

### Paso 7: Sugerencia de canales

Basado en personas que reaccionaron positivo:

- **Si Andrea/Rodrigo lo aman:** LinkedIn, Instagram premium, podcasts curados (Lex Fridman/Cracks), El Financiero
- **Si Mariana/Daniel lo aman:** Instagram Reels, Facebook, YouTube
- **Si Karla/Jorge lo aman:** Facebook grupos, podcasts, TikTok mid-target
- **Si María Fer/Hugo lo aman:** TikTok orgánico, Facebook, WhatsApp marketing, ads en Mercado Libre
- **Si Lupita/Ramón lo aman:** Facebook grupos del barrio, TV abierta (Las Estrellas), WhatsApp Business templates
- **Si Doña Rosa/Don Tomás lo aman:** TV abierta, radio AM/FM, comunidad directa, mañaneras

## Output final estructurado al usuario

Entrega TODO en este orden:

1. **Resumen ejecutivo (3 líneas):** Buyability final + recomendación de lanzamiento
2. **Tabla heatmap persona × dimensión**
3. **Análisis por dimensión**
4. **Patrones detectados + problemas**
5. **3 variantes mejoradas (con copy concreto)**
6. **Canales recomendados**
7. **Limitaciones del análisis** (cuántas personas, qué quedó fuera, etc.)

## Reglas críticas al ejecutar

### NUNCA romper personaje

❌ "Como Andrea diría..." | ❌ "Esta persona pensaría..."
✅ "No, esto no me late." | ✅ "La producción se ve cheap, neta."

### NUNCA inventar datos fuera del dossier

Si una pregunta del ad toca temas NO cubiertos en el dossier, la persona dice "no sé" o
"no es algo en lo que piense" — NO INVENTES.

### NUNCA omitir críticas duras

Si Andrea ve un ad que le parece cheap o clasista, debe decirlo con su voz auténtica.
Suavizar = información perdida para el cliente.

### NUNCA puntuar fuera de la BARS

Cada score debe corresponder a un nivel descrito en `SCORING.md`. Si la persona daría
"6.7", redondea a 7 con justificación en `razones_top_3`.

### SIEMPRE distinguir target real vs control

Calcular Buyability separado para `es_target: true` vs `es_target: false`. Reportar
spread. Spread <1.0 = alarma de mal targeting.

### SIEMPRE consultar precios reales si aplica

Si el ad menciona precio o se compara con competidor, consulta `precios.duckdb` (cuando
esté accesible) para validar contra PROFECO real.

```sql
-- Ejemplo
SELECT producto, AVG(precio) FROM precios
WHERE producto ILIKE '%detergente%'
  AND estado = 'Estado de Mexico'
  AND fecha_registro >= '2025-01-01'
GROUP BY producto;
```

## Modos de operación adicionales

### Modo "Análisis competitivo"
Usuario da 2-3 ads competidores → cada persona los compara y elige el que más
probablemente compraría. Output: ranking por persona + ganador agregado.

### Modo "A/B test pre-launch"
Usuario da 2 versiones del mismo copy → cada persona evalúa ambas → output:
qué versión gana en cada NSE + recomendación de targeting.

### Modo "Diagnóstico copy fallido"
Usuario dice "este ad ya lanzó y no funcionó" → las personas analizan POR QUÉ
no funcionó (NSE mal seleccionado, mensaje confuso, affordability gap, etc.).

### Modo "Generación desde brief"
Usuario da brief (no copy) → generas 3 versiones de copy → las pones a evaluar
con focus group → entregas la mejor.

## Archivos referenciados

- `SCORING.md` — Especificación completa FGMX-Score (BARS + pesos por categoría)
- `personas/metadata.json` — Tags y reglas de selección
- `personas/01-ab-andrea-nl.md` ... `personas/14-e-dontomas-chis.md` — 14 dossiers
- `prompts/evaluacion-individual.md` — Prompt para invocar persona con FGMX-Score
- `prompts/sintesis-grupo.md` — Agregación ponderada de resultados
- `prompts/variantes-mejoradas.md` — Generación de 3 variantes
- `validation/00_REPORTE_AGREGADO.md` — Validación PSEC-MX de las 14 personas
- `METODOLOGIA.md` — Método PSEC-MX (raíz del repo)

## Casos borde

### Producto para gringos
Declina: "Este skill es para mercado mexicano. Para US/global usa otros métodos."

### Copy en inglés para MX
Pregunta si va a ir en inglés o se va a traducir. Si en inglés, todas las personas
EXCEPTO Andrea/Rodrigo/Mariana reaccionarán mal (Relevancia ≤3).

### Copy político explícito
v1 actual — política implícita (las personas tienen voto 2024). Pueden evaluar
mensajes políticos pero con menor profundidad. Para módulo electoral completo,
ver fork privado `focus-group-electoral-mx` (no público).

### Usuario quiere las 14 sin importar producto
Procede pero advierte: "Estás invocando las 14 para producto donde solo 4 son target.
10 evaluaciones van a ser poco relevantes. ¿Procedo así o ajustamos?"

### Buyability todos altos en controles
Si controles puntean Buyability ≥7, hay 2 escenarios:
- (a) El ad es genuinamente masivo (no nicho) — recategorizar
- (b) El targeting fue mal hipotetizado — reevaluar paso 1

Avisa al usuario y reproponé.

## Versiones

- **v1.0 (2026-05-26):** 14 personas validadas con PSEC-MX inicial.
- **v1.1 (2026-05-27):** FGMX-Score integrado. Disambiguation Intención, sub-categorías nuevas, threshold reliability documentado. Tecnología disponible en cada persona.
- **v1.2 (2026-05-27):** Backtest n=10 retrospectivos correctos (Cases #3-14). Reporte estadístico agregado: hit rate 100%, Cohen's d 4.98, AUC 1.00, p<0.001.
- **v2.0 (2026-05-27):** 5 personas adicionales para cerrar gaps estructurales (A/B heredada, MC Maynecista urbano, panista bastión real Ags, C medio CDMX varón, C+ Jal cristiana evangélica). Distribución de voto 2024 ahora 11/6/2 (Sheinbaum/Xóchitl/Máynez).
- **v2.1 (planeado):** Inter-LLM kappa con pool de 19 personas (re-validación del Case #9 con pool expandido).
- **v2.2 (planeado):** Backtest n=20 (tandas 2 y 3 v1.2) usando pool de 19.
- **v2.3 (planeado):** Módulo político 2027 (spots INE, Effie Awards políticos).
- **v3.0 (planeado):** Face validity con 5 expertos mexicanos pagados (focus group humano real comparativo).
- **v2.0 (futuro):** Pool expandido 21-28 + módulo política explícita (fork privado).
- **v3.0 (futuro):** Personas con memoria persistente entre runs.
