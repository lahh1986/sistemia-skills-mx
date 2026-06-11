---
name: payments-mx
description: |
  Usar cuando el usuario quiera elegir, integrar o comparar métodos de pago y
  gateways en México. Cubre las comisiones reales 2026 de Conekta, Mercado Pago,
  Stripe MX, Openpay y Clip; los métodos disponibles (tarjeta, SPEI, OXXO Pay,
  CoDi/DiMo, retailers, BNPL Kueski/Aplazo/Atrato, domiciliación CLABE, wallets);
  patrones de marketplace (split, escrow, KYC del seller); marco regulatorio
  (CNBV, Banxico, Ley Fintech) y referencia ligera a CFDI 4.0 con complemento
  de pagos. Devuelve una recomendación accionable, no una lista neutral.

  Triggers: "qué gateway uso en México", "comparar Conekta vs Mercado Pago vs
  Stripe", "comisiones reales MX", "cómo cobro con OXXO", "integrar SPEI",
  "cuánto cobra Conekta", "marketplace split payments México", "CoDi DiMo",
  "BNPL México", "Kueski Aplazo Atrato", "domiciliación CLABE", "pagos
  recurrentes México", "checkout México", "PSP México", "CNBV fintech",
  "qué métodos de pago acepto", "cobranza México".
---

# payments-mx — Pagos digitales en México (gateways, métodos, marketplace)

> Wrapper de Claude Code que conoce las comisiones reales 2026, los métodos
> de pago con su adopción real, el marco regulatorio, y los patrones de
> marketplace. Sirve para decidir qué stack usar, no para repetir docs.

**Fuente de verdad:**
- `data/gateways.json` — 5 gateways con fees, payout, marketplace, gotchas
- `data/methods.json` — 11 métodos con adopción, settlement, recomendaciones por vertical

**Frescura:** datos verificados al `2026-06-10`. Comisiones cambian — antes de firmar contrato, revalidar con el campo `pricing_url` del gateway.

---

## Cuándo activarte

- El usuario pregunta qué gateway/PSP usar en México
- El usuario compara comisiones entre Conekta, Mercado Pago, Stripe, Openpay, Clip
- El usuario quiere integrar OXXO Pay, SPEI, CoDi, DiMo o tarjeta en MX
- El usuario construye marketplace y necesita split payments / escrow / payouts a sellers
- El usuario pregunta sobre BNPL en México (Kueski, Aplazo, Atrato)
- El usuario menciona domiciliación CLABE, cargo recurrente, suscripciones MX
- El usuario pregunta sobre Ley Fintech, CNBV, Banxico relacionado con pagos
- El usuario menciona checkout, pasarela, PSP, gateway, pagos online en MX

**NO actives si:**
- El usuario pide ayuda con **CFDI / facturación electrónica** propiamente — eso es otro skill (`sat-mx` o futuro `facturacion-mx`). Aquí solo damos pointers ligeros.
- El usuario quiere integrar **POS físico** sin componente online — eso es Clip/Bbva/Banorte directo, no este skill.
- El usuario pregunta por pagos en otro país LATAM (AR, CO, CL, PE, BR) — referir al skill `payments-{cc}` cuando exista.

---

## Workflow

### Paso 1 — Diagnóstico del caso

Antes de recomendar, identifica:

| Variable | Pregunta a hacer | Por qué importa |
|---|---|---|
| **Vertical** | ¿B2C masivo? ¿SaaS? ¿Marketplace? ¿B2B? ¿Retail alto ticket? | Define qué métodos son obligatorios (ver `vertical_recommendations` en `methods.json`) |
| **Ticket promedio** | ¿$50? ¿$500? ¿$5,000? ¿$50,000? | Tickets bajos → Clip (sin fijo). Tickets altos B2B → Conekta SPEI ($12.50 flat) |
| **Marketplace** | ¿Necesitas split payments o escrow? | Solo MP Marketplace API y Stripe Connect lo soportan publicamente |
| **Cross-border** | ¿Vendes a clientes US/internacional? ¿Cobras en USD? | Stripe MX es el único stack maduro |
| **Recurrencia** | ¿Suscripciones? ¿Cargo periódico? | Tarjeta tokenizada + domiciliación CLABE como fallback |
| **Volumen mensual** | $0-50k, $50k-500k, $500k+ MXN | Sobre $500k MXN/mes los gateways negocian fees |
| **Quiere captar clientes sin tarjeta** | Sí/no | Si sí → OXXO obligatorio (10% del e-commerce MX) |

Si el usuario no aporta esta info, **pregunta antes de recomendar**. Una recomendación sin estos datos es ruido.

### Paso 2 — Carga los datos

Lee `data/gateways.json` y `data/methods.json`. NO los pegues completos al usuario — extrae lo relevante.

**Para preguntas de comparación rápida**, usa la sección `comparison_quick` de `gateways.json` y la sección `vertical_recommendations` de `methods.json`.

### Paso 3 — Aplica el árbol de decisión

```
¿Marketplace con sellers múltiples?
├── SÍ
│   ├── ¿Necesitas cross-border (sellers o buyers internacionales)?
│   │   ├── SÍ → **Stripe Connect**
│   │   └── NO → **Mercado Pago Marketplace API** (single stack con OXXO incluido)
│   └── (Si tu MVP es pequeño y solo MX) → MP por simplicidad
├── NO
│   ├── ¿Vertical es SaaS / suscripción?
│   │   └── **Stripe MX** (Billing recurrente al 0.7%, tokenización de tarjeta sólida)
│   ├── ¿Tickets altos B2B con SPEI?
│   │   └── **Conekta** ($12.50 flat es imbatible) o **Openpay** (T+1 mismo día si BBVA)
│   ├── ¿B2C masivo MX clase media?
│   │   └── **Conekta** (tarifa balanceada + mejor fee OXXO + DX bueno)
│   ├── ¿Tickets bajos / link de pago para pyme?
│   │   └── **Clip** (sin fijo, link simple)
│   └── ¿Ya eres cliente BBVA con volumen?
│       └── **Openpay** (2.9% tarjeta nacional, dispersión SPEI mismo día)
```

### Paso 4 — Métodos a aceptar (por vertical)

Para cada vertical, lee `vertical_recommendations` en `methods.json` y devuelve must-have + nice-to-have + skip con la razón.

**Regla universal MX 2026:**
- **Tarjeta** siempre (~60% del mercado)
- **SPEI** casi siempre (~22%, sube en B2B)
- **OXXO Pay** si tu cliente target incluye clase media-baja o sin tarjeta (~10% del e-commerce, 25% si cuentas a quien preferiría efectivo)
- **CoDi/DiMo** = ignorar 2026 (adopción <2%, esperar a ver si Mundial los escala)
- **BNPL** solo si ticket promedio > $1,000 MXN

### Paso 5 — Devuelve la recomendación

Estructura del output al usuario:

```markdown
## Recomendación para {{caso}}

**Gateway principal:** {{nombre}} — {{razón en una línea}}
**Métodos a aceptar:** {{list}}
**Fee efectivo estimado:** {{X}}% sobre tu ticket promedio de ${{ticket}}

### Por qué
- {{razón 1 — fee/método específico}}
- {{razón 2 — capacidad marketplace/SPEI/etc.}}
- {{razón 3 — gotcha evitado}}

### Métodos por prioridad
| Método | Por qué |
| Tarjeta | 60% del mercado MX |
| SPEI | ... |
| OXXO | ... |

### Gotchas a evitar
- {{gotcha del gateway elegido — del JSON}}
- {{gotcha del método}}

### Stack alternativo (si {{condición}})
{{nombre alternativo}} — {{cuándo conviene}}

### Próximos pasos
1. Crear cuenta sandbox en {{url}}
2. {{paso técnico}}
3. {{paso fiscal — referencia ligera CFDI/SAT}}
```

### Paso 6 — Referencia fiscal ligera

Si el caso incluye facturación, advertir SIEMPRE:

> ⚠️ Cada cobro requiere **CFDI** (factura electrónica) y, cuando aplica, **complemento de pagos** (CFDI 4.0). Esto NO lo emite el gateway — lo emites tú o un PAC (Facturama, SW Sapien, etc.). Detalle fuera del scope de este skill — ver `sat-mx` o consultar con contador.

---

## Patrones de marketplace (eltianguis y similares)

### Split payments

Tres patrones según gateway:

**A. Stripe Connect — Destination Charges (recomendado)**
- Carga única al buyer, transfer automático al seller con `application_fee_amount`
- Stripe maneja KYC del seller via Connect Onboarding
- Soporta cross-border
- DX: el más maduro
- Costo extra: 0.25% + $0.25 USD por payout cross-border

**B. Mercado Pago Marketplace API**
- Setup de sub-cuentas seller con OAuth
- `marketplace_fee` se cobra automático
- Funciona end-to-end en MX con OXXO incluido
- Lock-in mayor (migrar fuera de MP es complejo)

**C. Conekta — workaround manual**
- No hay split nativo público
- Patrón: cobras al buyer en cuenta plataforma, luego SPEI manual o vía Conekta a seller
- Riesgo regulatorio: si retienes fondos > 24h sin contrato escrito, podrías caer en figura de IFPE (Institución de Fondos de Pago Electrónico) que requiere licencia CNBV
- **Recomendación:** no usar Conekta para marketplace serio

### Escrow / hold

Para "dinero retenido hasta entrega confirmada":

- **Stripe Connect:** usa `transfer_data.destination` con delay manual o `on_behalf_of` + transfer programado
- **MP:** `release_date` en marketplace API permite hold automático
- **Custom (no recomendado):** retener tú los fondos en cuenta plataforma — pisa territorio IFPE/CNBV

### KYC del seller

Obligatorio antes de payout. Datos mínimos MX:
- RFC (validar contra SAT con `sat-mx` skill si está disponible)
- CURP (persona física)
- Constancia de Situación Fiscal vigente
- Comprobante de domicilio (< 3 meses)
- Identificación oficial vigente
- CLABE bancaria a nombre del seller (validar coincide con RFC)

Stripe Connect y MP Marketplace API tienen wizard de onboarding. Si vas custom, NO te saltes este paso — PLD/CFT (Prevención de Lavado de Dinero) lo exige.

---

## Marco regulatorio (resumen — ver fuentes para detalle)

| Tema | Regulador | Aplica si |
|---|---|---|
| **Ley Fintech 2018** | CNBV | Eres ITF, IFPE, o procesas fondos de terceros |
| **PLD/CFT** | CNBV + UIF | Procesas cualquier monto recurrente o > umbral UMAs |
| **3DS Secure 2** | CNBV | Tarjeta no presente (e-commerce) — desde 2022 obligatorio |
| **SPEI** | Banxico | Reglas operativas; 24/7 desde 2024 |
| **CFDI 4.0 + complemento pagos** | SAT | Cualquier cobro a contribuyente; complemento si pago en parcialidades o diferido |
| **NOM-151** | Economía | Firma electrónica de mandatos (domiciliación) |

**Heurística:** si solo conectas a un gateway y no retienes fondos de terceros > 24h, NO eres IFPE y no necesitas licencia CNBV. Si tu marketplace retiene fondos del buyer y los libera al seller en > 24h (escrow), consulta abogado fintech.

---

## Comisiones cheat sheet (MXN, excluyen IVA)

| Método | Conekta | MP MX | Stripe MX | Openpay | Clip |
|---|---|---|---|---|---|
| Tarjeta nacional | 3.4% + $3 | 3.49% + $4 (instant) | 3.6% + $3 | **2.9% + $2.50** | 3.6% |
| OXXO Pay | **2.6% + $3** | 3.79% + $4 | 4.0% + $3 | $14.66 fijo | — |
| SPEI | **$12.50 flat** | 3.49% + $4 | 4.0% + $3 | $8 mín | — |
| Tarjeta internacional | — | — | 4.1% + $3 | 3.7% | 3.6% |
| Marketplace split | Manual ⚠️ | **Nativo** | **Connect** | Limitado | No |
| Payout default | T+10 (1ro) → T+1 | Instantáneo | T+7 (1ro) → T+2 | T+1 | Mismo día |

**Negrita = ganador en esa categoría.**

---

## Lo que SÍ y NO hace este skill

**SÍ:**
- Recomienda gateway y métodos según vertical, ticket, marketplace, recurrencia
- Da comisiones reales 2026 verificadas
- Explica patrones de marketplace (split, escrow, KYC seller)
- Advierte de gotchas operativos (payout inicial, webhooks duplicados, 3DS, etc.)
- Apunta al marco regulatorio relevante

**NO:**
- No reemplaza a un abogado fintech para casos de IFPE/ITF
- No emite CFDI (eso es `sat-mx` o un PAC)
- No genera código de integración listo para producción — da patrones y los snippets viven en `examples/`
- No predice cambios en comisiones — los gateways las actualizan unilateralmente
- No cubre pagos en otros países LATAM (cada uno tiene su skill `payments-{cc}`)

---

## Cómo refrescar los datos

Las comisiones cambian. Antes de una decisión grande:

```bash
# Verifica las páginas oficiales contra tu data/gateways.json
cat ~/sistemia-skills-mx/skills/payments-mx/data/gateways.json | jq -r '.gateways[] | "\(.name): \(.pricing_url)"'
```

Si detectas un cambio, edita `data/gateways.json` y actualiza el campo `as_of` en `_meta`.

---

## Fuentes

- **Gateways:** páginas oficiales de pricing (links en `data/gateways.json`)
- **Adopción:** AMVO Estudio Venta Online 2025, Banxico, INEGI ENIF 2024
- **BNPL:** GlobeNewswire MX BNPL Report 2026, Marketing4eCommerce
- **Marco regulatorio:** CNBV (Ley Fintech), Banxico (SPEI/CoDi), SAT (CFDI 4.0)
- Investigación curada por Sistemia Skills MX al `2026-06-10`.
