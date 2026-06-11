# payments-mx

> Skill de Claude Code para decidir, comparar e integrar **métodos de pago en México** sin perder media tarde leyendo páginas de pricing.

Parte de [El Tianguis](https://eltianguis.sistemia.mx) — catálogo abierto de skills de Claude Code para México y Latinoamérica.

---

## Qué hace

Le dices a Claude:

> "Voy a vender suscripciones a $499 MXN/mes para pymes. ¿Qué gateway uso?"

Y te responde con:

- **Gateway recomendado** y por qué (no copia-pega de marketing)
- **Métodos a aceptar** (tarjeta sí, OXXO depende, CoDi/DiMo no en 2026)
- **Fee efectivo estimado** sobre tu ticket promedio
- **Gotchas operativos** que no están en docs (payout T+10 del primer pago, webhooks duplicados, drop-off de OXXO, etc.)
- **Próximos pasos concretos** para implementar

Cubre las decisiones que más rompen pyme y startup en MX:

- Conekta vs Mercado Pago vs Stripe MX vs Openpay vs Clip — comisiones reales 2026
- Tarjeta, SPEI, OXXO Pay, CoDi/DiMo, retailers, Apple/Google Pay, BNPL (Kueski/Aplazo/Atrato), domiciliación CLABE
- Patrones de **marketplace**: split payments, escrow, KYC del seller, payouts
- Marco regulatorio ligero (CNBV, Banxico, Ley Fintech)
- Referencia ligera a CFDI 4.0 + complemento de pagos (link al skill `sat-mx`)

---

## Por qué este skill existe

Las páginas de pricing de los gateways te mienten con "desde 2.9%". El **fee efectivo real** depende de tu mix de métodos, payout schedule y vertical. Y los gotchas (primer payout a 10 días, OXXO Pay con tope de $12,000, SPEI a $12.50 flat vs %, marketplace de Conekta no público) no están en docs.

Este skill consolida:

- Investigación de fees publicada al **2026-06-10**
- Adopción real de métodos (AMVO, Banxico, INEGI)
- Patrones de marketplace probados (Stripe Connect, MP Marketplace API)
- Decisiones por vertical (B2C, SaaS, marketplace, retail alto ticket, B2B)

---

## Instalación

```bash
# Copia el skill donde tu Claude Code lo lea
cp -r payments-mx/ ~/.claude/skills/payments-mx/
```

No hay setup. Es un skill de conocimiento — no ejecuta nada en tu máquina.

---

## Uso

Activa el skill mencionando cualquier de estos triggers:

- "¿Qué gateway uso para mi tienda en línea?"
- "Compara Conekta vs Mercado Pago para marketplace"
- "Comisiones reales de Stripe en México"
- "¿Cómo integro OXXO Pay?"
- "Voy a hacer un marketplace, ¿cómo cobro?"
- "BNPL en México 2026"
- "Pagos recurrentes domiciliación CLABE"

Claude te preguntará por tu vertical, ticket promedio y necesidad de marketplace, y devolverá una recomendación accionable.

---

## Estructura

```
payments-mx/
├── SKILL.md              # Cuándo activarse + workflow + árbol de decisión
├── README.md             # Esto que estás leyendo
├── data/
│   ├── gateways.json     # 5 gateways: fees, payout, marketplace, gotchas
│   └── methods.json      # 11 métodos: adopción, settle, recomendaciones por vertical
└── examples/
    └── eltianguis-marketplace.md  # Caso end-to-end de marketplace
```

---

## Frescura

Datos verificados al `2026-06-10`. Las comisiones de los gateways cambian — antes de firmar contrato, valida contra el campo `pricing_url` de `data/gateways.json`. Cada gateway publica fees en su página de pricing.

Si detectas un cambio, edita `data/gateways.json` y actualiza `_meta.as_of`.

---

## Lo que NO hace

- No reemplaza a un abogado fintech para casos de IFPE/ITF (licencia CNBV)
- No emite CFDI ni hace facturación — eso es `sat-mx` o un PAC
- No genera código de producción listo para deploy — da patrones y los snippets viven en `examples/`
- No predice cambios futuros en comisiones
- No cubre pagos en otros países LATAM (cada uno tiene su skill: `payments-ar`, `payments-co`, `payments-pe`, `payments-cl`, `payments-br`, `payments-es`)

---

## Cómo aportar

Issues y PRs bienvenidos:

- https://github.com/lahh1986/sistemia-skills-mx/issues

Si trabajas con un gateway que no está cubierto (Kushki, dLocal, Belvo, Prosa, Bambora), abre PR con un objeto siguiendo el shape de `data/gateways.json`.

---

## Licencia

MIT. Skill mantenido por [Sistemia](https://sistemia.mx).
