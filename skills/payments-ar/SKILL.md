---
name: payments-ar
description: |
  Usar cuando el usuario quiera elegir, integrar o comparar métodos de pago y
  gateways en Argentina. Cubre las comisiones reales 2026 de Mercado Pago AR
  (con sus 4 planes de acreditación), Decidir/Prisma (regulado por categoría
  BCRA), dLocal, MODO, PayU, Ualá Bis y Naranja X; los métodos disponibles
  (tarjeta, débito, cuotas, QR interoperable/Transferencia 3.0, Rapipago,
  Pago Fácil, saldo MP, MODO, Mercado Crédito, Plan Z Naranja, USDT/Binance
  Pay); el contexto único de AR (cepo cambiario, inflación, cuotas culturales,
  Ahora 12 DEROGADO en jun-2026, BCRA Com 'A' 8432); y patrones de marketplace
  con MP Marketplace API. Devuelve una recomendación accionable, no una lista
  neutral.

  Triggers: "qué gateway uso en Argentina", "comparar Mercado Pago vs Decidir
  vs dLocal", "cómo cobro con Rapipago", "Pago Fácil online", "comisiones MP
  Argentina", "Transferencia 3.0", "QR interoperable Argentina", "cuotas sin
  interés AR", "Ahora 12 derogación", "marketplace Argentina split", "BCRA
  fintech", "MODO checkout", "dLocal pago USD desde Argentina", "Naranja X
  Plan Z", "Binance Pay Argentina", "USDT comercio AR", "cobrar en dólares
  Argentina cepo", "Ualá Bis link de pago".
---

# payments-ar — Pagos digitales en Argentina (gateways, métodos, cuotas, cepo)

> Wrapper de Claude Code que conoce las comisiones reales 2026, los métodos
> de pago con su adopción real, el contexto regulatorio (BCRA + cepo + AFIP),
> y la cultura argentina de cuotas. Para decidir qué stack usar, no para
> repetir docs ni asumir que "AR es como MX en español".

**Fuente de verdad:**
- `data/gateways.json` — 7 gateways con fees, payout por categoría, marketplace, gotchas
- `data/methods.json` — 14 métodos con adopción, settlement, recomendaciones por vertical

**Frescura:** datos verificados al `2026-06-10`. Aclaración importante: el plan
oficial **Ahora 12 fue derogado en junio 2026** — el "sin interés" subsidiado
ya no existe y el costo financiero ahora lo absorbe merchant o cliente.

---

## Cuándo activarte

- El usuario pregunta qué gateway/PSP usar en Argentina
- El usuario compara comisiones entre Mercado Pago, Decidir/Prisma, dLocal, MODO, PayU, Ualá Bis, Naranja X
- El usuario quiere integrar Rapipago, Pago Fácil, QR interoperable, MODO, tarjeta o cuotas en AR
- El usuario menciona Transferencia 3.0, PCT, CVU/CBU
- El usuario construye marketplace en AR y necesita split payments
- El usuario pregunta sobre Mercado Crédito, Naranja Plan Z, Wibond, WIPEI, Pareto BNPL
- El usuario pregunta sobre cobrar en USD desde AR (cepo) o el rol de USDT/Binance Pay
- El usuario menciona Ahora 12, cuotas sin interés, cuota simple
- El usuario menciona BCRA, AFIP, monotributo, Régimen Simplificado relacionados con cobro

**NO actives si:**
- El usuario pide ayuda con **AFIP / facturación electrónica argentina** (CAE, monotributo) — eso es scope de un futuro skill `afip-ar`.
- El usuario quiere integrar **POS físico puro** — eso es Posnet/Lapos/Clip, no online checkout.
- El usuario pregunta por pagos en otro país LATAM — referir al skill `payments-{cc}` correspondiente.

---

## Workflow

### Paso 1 — Diagnóstico del caso

Antes de recomendar, identificá:

| Variable | Pregunta a hacer | Por qué importa en AR específicamente |
|---|---|---|
| **Vertical** | ¿B2C ecom? ¿SaaS? ¿Marketplace? ¿Retail electro/indumentaria? ¿Freelance cross-border? | Verticales del interior dependen de Naranja. SaaS B2B usa tarjeta + QR. Freelance USD necesita dLocal/USDT. |
| **Cuotas culturales** | ¿Tu producto se vende con cuotas? ¿Qué plazos (3/6/12/18/24)? | Sin cuotas, perdés ~50% del mercado en electro/indumentaria. Pero post-derogación Ahora 12, el costo es del merchant. |
| **Ticket promedio** | ¿ARS 5k? ¿50k? ¿500k? | Bajo ticket → QR/débito. Alto ticket → cuotas + Naranja. |
| **Marketplace** | ¿Necesitás split payments o escrow? | Sólo MP Marketplace API tiene split nativo serio en AR. |
| **Cross-border / USD** | ¿Vendés a clientes fuera de AR? ¿Necesitás cobrar en USD? | Cepo cambiario: sin estructura offshore + dLocal/Stripe, USD no llega. |
| **Bancarización del target** | ¿Tu cliente target tiene cuenta bancaria/MP? | Si sí → QR interoperable es el rail moderno barato. Si no → Rapipago/Pago Fácil es obligatorio. |
| **Geografía del target** | ¿CABA/GBA? ¿Interior (Córdoba, NOA)? | Interior prefiere Naranja. CABA premium prefiere MODO. |
| **Volumen mensual** | ARS 0-500k, 500k-5M, 5M+ | Sobre ARS 5M/mes negociás todos los fees con MP/Decidir. |

Si el usuario no aporta esta info, **preguntale antes de recomendar**. Una recomendación sin estos datos en AR es ruido (la diferencia entre MP inmediato 6.29% y 35d 1.49% es 4x).

### Paso 2 — Carga los datos

Leé `data/gateways.json` y `data/methods.json`. NO los pegues completos al usuario — extraé lo relevante.

Para preguntas de comparación rápida usá la sección `comparison_quick` de `gateways.json` y `vertical_recommendations` de `methods.json`.

### Paso 3 — Aplicá el árbol de decisión

```
¿Necesitás cobrar en USD desde entidad AR?
├── SÍ
│   ├── ¿Tenés estructura offshore (LLC, Stripe, etc.)?
│   │   ├── SÍ → Stripe + Wise/Mercury, ignorá este skill
│   │   └── NO → **dLocal Pay-outs** (sólo opción legal con cepo)
│   └── ¿Es informal/freelance?
│       └── **Binance Pay QR** o USDT P2P (asumir compliance propia)
│
├── NO (cobro en ARS)
│   │
│   ├── ¿Marketplace con sellers múltiples?
│   │   └── **Mercado Pago Marketplace API** — único stack serio en AR
│   │
│   ├── ¿Vertical retail electro/indumentaria/muebles?
│   │   └── **MP + Naranja Plan Z + cuotas** (las cuotas son el producto)
│   │
│   ├── ¿Ticket bajo y target bancarizado (gastro, retail físico)?
│   │   └── **MP QR interoperable + MODO** como secundario (0.80%)
│   │
│   ├── ¿SaaS B2B AR puro?
│   │   └── **Decidir débito (0.80%) + MP a 35d (1.49%)** para tarjeta
│   │
│   ├── ¿PyME local / freelance con link de pago?
│   │   └── **Ualá Bis (4.9% inmediato)** o MP Link de Pago (6.60% inmediato)
│   │
│   └── ¿Ya estás en LATAM-wide PayU?
│       └── **PayU AR** (mismo stack, pricing decente)
```

### Paso 4 — Métodos a aceptar (por vertical)

Para cada vertical, leé `vertical_recommendations` en `methods.json` y devolvé must-have + nice-to-have + skip con la razón.

**Reglas universales AR 2026:**
- **Tarjeta crédito** siempre (~65% del e-commerce)
- **Cuotas** casi siempre en B2C — pero modeladas como costo del merchant post-Ahora 12 derogado
- **QR interoperable / Transferencia 3.0** — rail moderno, 0.80% imbatible, alta adopción 2026
- **Rapipago / Pago Fácil** si tu target incluye no bancarizados (~25% del público) — equivalente al OXXO de MX
- **Saldo MP** default-on si usás MP (15-20% de usuarios pagan con saldo)
- **Mercado Crédito** activar como flag en checkout MP — BNPL embebido
- **Naranja Plan Z** si vendés electro/indumentaria/interior
- **MODO** como complemento si target premium bancarizado
- **USDT/Binance Pay** sólo para servicios cross-border o cripto-friendly
- **dLocal** si necesitás USD o entrás desde afuera de AR

### Paso 5 — Devolvé la recomendación

Estructura del output:

```markdown
## Recomendación para {{caso}}

**Gateway principal:** {{nombre}} — {{razón en una línea}}
**Métodos a aceptar:** {{list}}
**Fee efectivo estimado:** {{X}}% sobre tu ticket promedio de ARS {{ticket}}, con tu mix asumido de ({{cuotas/contado}})

### Por qué
- {{razón 1 — fee/método específico con número}}
- {{razón 2 — capacidad marketplace/cuotas/etc.}}
- {{razón 3 — gotcha de AR evitado (cepo, hold, surcharge)}}

### Métodos por prioridad
| Método | Por qué | Fee efectivo |
| Tarjeta crédito + cuotas | 65% del mercado, cuotas culturales | X% |
| QR interoperable | Rail moderno, 0.80% | 0.80% |
| Rapipago / Pago Fácil | Captura no bancarizados | X% |
| Saldo MP | UX 1-tap | X% |

### Gotchas a evitar (específicos de AR)
- {{gotcha del gateway elegido — del JSON}}
- {{gotcha del método}}
- Cepo / cuotas / inflación si aplica

### Stack alternativo (si {{condición}})
{{nombre alternativo}} — {{cuándo conviene}}

### Próximos pasos
1. Crear cuenta sandbox en {{url}}
2. {{paso técnico}}
3. ⚠️ AFIP: definir régimen fiscal del vendedor (Monotributo, Régimen Simplificado, IVA) — fuera de scope, consultar contador AR
```

### Paso 6 — Referencia fiscal ligera

Si el caso incluye facturación, advertí SIEMPRE:

> ⚠️ Cada cobro requiere **Factura Electrónica con CAE de AFIP** (Resolución 4291/2026). Esto NO lo emite el gateway — lo emitís vos vía Web Services AFIP, Tango Gestión, Contabilium, Bill.com.ar o equivalente. Para Monotributo + venta con cuotas, la factura es por el monto total, no por la cuota. Detalle fuera del scope de este skill — futuro skill `afip-ar`.

---

## Cuotas en AR — el tema más importante post-2026

**Estado a junio 2026:**

- Plan **Ahora 12 / Ahora 18 / Ahora 24** OFICIAL fue **derogado en junio 2026** por el gobierno actual
- Programa sigue existiendo técnicamente, sin subsidio estatal — el costo financiero pasa al merchant o al cliente
- CFT referenciales 2026: 3 cuotas 5.39% · 6 cuotas 10.82% · 12 cuotas 22.22%

**Tres patrones de cómo manejarlo:**

| Patrón | Cómo | Tradeoff |
|---|---|---|
| **A. Trasladar al cliente** | Mostrar "12 cuotas de ARS X" con interés incluido en la cuota | Conversión cae (cliente ve precio más alto) pero margen intacto |
| **B. Absorber el merchant** | Mostrar "12 cuotas sin interés" — el CFT lo pagás vos | Conversión alta pero margen ~22% menor en 12 cuotas |
| **C. Híbrido** | Sin interés en 3 cuotas (absorber), con interés en 6+ | Equilibrio típico de retail AR post-derogación |

**Caso especial — Naranja Plan Z:**
- Plan Z permite al cliente decidir AL CIERRE DE TARJETA si paga 1, 2 o 3 cuotas sin interés
- El costo lo absorbe Naranja, NO el merchant
- Si tu cliente target tiene Naranja, activá Plan Z — es upside puro

**Caso especial — Mercado Crédito:**
- BNPL embebido en MP — el usuario ve "comprar en cuotas" sin necesitar tarjeta
- El costo lo modela MP en la comisión, ~5-25% sobre el monto según plazo
- Activá como flag en preferencia MP — default-on en checkout moderno

---

## Cepo cambiario — heurística rápida

Si te tienen que pagar en USD desde fuera de AR:

| Situación | Solución |
|---|---|
| Tenés LLC US o estructura offshore | Stripe + Wise / Mercury directo. Olvidate de AR. |
| Sos PyME AR, querés cobrar a clientes US/EU | **dLocal Pay-outs** — recibís USD en cuenta US controlada, conversión a ARS por MEP. Único legal. |
| Sos freelance, monto bajo, baja regularidad | **Binance Pay QR** o USDT P2P (cliente paga en USDT, vos vendés en MEP) |
| Querés que tu cliente AR te pague pero "pegarle al MEP" | Imposible legalmente para el merchant — el cliente lo hace de su lado. |

**Regla:** nunca prometás USD payout desde entidad AR sin estructura especial. AFIP + BCRA persiguen.

---

## Marco regulatorio (resumen)

| Tema | Regulador | Aplica si |
|---|---|---|
| **BCRA Com 'A' 8432/2026** | BCRA | Sos PSP, billetera tercerizada o agregás sub-merchants — KYC/AML reforzado |
| **Régimen de Cuotas** | BCRA + Ministerio Economía | Ofrecés cuotas — post-Ahora 12 derogado, sin subsidio estatal |
| **CVU/CBU + Transferencia 3.0** | BCRA | Cualquier cuenta digital — interoperabilidad universal mandatoria |
| **AFIP Factura Electrónica + CAE** | AFIP | Cualquier cobro a contribuyente AR |
| **PSP / PSPCP / ATM** | BCRA | Registrarte como PSP si procesás fondos de terceros — licencia obligatoria |
| **PLD/CFT** | UIF | Procesás cualquier monto recurrente o > umbrales |

**Heurística:** si sólo orquestás vía MP/dLocal y NO retenés fondos de terceros >24h, NO sos PSP y no necesitás licencia BCRA. Si tu marketplace retiene fondos del comprador y libera al seller en > 24h (escrow), consultá abogado fintech AR (no es un argumento de manual — Com 8432 lo aprieta).

---

## Comisiones cheat sheet (ARS, excluyen IVA 21%)

| Método | MP AR | Decidir | dLocal | MODO | PayU | Ualá Bis | Naranja X |
|---|---|---|---|---|---|---|---|
| Tarjeta crédito 1 pago | 1.49-6.29% (según plan) | 1.80% reg | ~4% | via Payway | 3.99% + $3 | 4.9% | 1.19-9.99% (según plazo) |
| Débito | hereda | **0.80%** | ~4% | — | hereda | 4.9% | — |
| QR interoperable | **0.80%** | — | — | **0.80%** | — | 4.9% | — |
| Rapipago/Pago Fácil | sí | — | sí | — | sí | — | — |
| Cuotas (CFT al merchant) | escala | 1.80% T+2 | sí | via Payway | sí | 3/6/12 | escala |
| Marketplace split | **Nativo** | No | Limitado | No | LATAM-wide | No | No |
| Payout default | configurable | T+8 a T+18 (Cat BCRA) | variable | hereda | T+? | Inmediato | configurable |

**Negrita = ganador en esa categoría.**

---

## Lo que SÍ y NO hace este skill

**SÍ:**
- Recomienda gateway y métodos según vertical, ticket, cuotas, marketplace, geografía y bancarización
- Da comisiones reales 2026 verificadas (con el cuidado de que MP cambia seguido)
- Explica el estado actual de cuotas post-derogación Ahora 12
- Explica el cepo y cómo cobrar USD desde AR legalmente
- Advierte de gotchas operativos (holds anti-fraude, surcharge internacional, categoría BCRA cambiante)
- Apunta al marco regulatorio relevante (Com 8432, AFIP)

**NO:**
- No reemplaza a un contador o abogado fintech AR
- No emite Factura Electrónica con CAE (eso es AFIP + un emisor)
- No genera código de integración listo para producción — da patrones; los snippets viven en `examples/`
- No predice cambios de fees ni del marco cuotas
- No cubre pagos en otros países LATAM (cada uno tiene su skill `payments-{cc}`)
- No es asesor de USDT/cripto — sólo lo lista como contexto cuando aplica

---

## Cómo refrescar los datos

Las comisiones de MP AR cambian seguido por inflación + regulación. Antes de una decisión grande:

```bash
cat ~/sistemia-skills-mx/skills/payments-ar/data/gateways.json | jq -r '.gateways[] | "\(.name): \(.pricing_url)"'
```

Si detectás un cambio, edití `data/gateways.json` y actualizá `_meta.as_of`.

---

## Fuentes

- **Gateways:** páginas oficiales de pricing + secundarias (jonatanalmeira, calcularsueldo, iproup) cuando MP bloquea WebFetch
- **Adopción:** BCRA Informe de Pagos Minoristas feb-2026 (89.9M ops PCT QR), BCRA Comunicaciones
- **Cuotas:** Infobae 9-jun-2026 (derogación Ahora 12), Argentina.gob.ar/economia/comercio/ahora12
- **BNPL:** GlobeNewswire AR BNPL Report 2026
- **Marco regulatorio:** BCRA Com 'A' 8432/2026, AFIP Resolución 4291/2026
- Investigación curada por Sistemia Skills MX al `2026-06-10`.
