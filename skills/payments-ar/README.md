# payments-ar

> Skill de Claude Code para decidir, comparar e integrar **métodos de pago en Argentina** sin perder media tarde leyendo páginas de pricing que cambian cada mes por inflación.

Parte de [El Tianguis](https://eltianguis.sistemia.mx) — catálogo abierto de skills de Claude Code para México y Latinoamérica. Sister skill de `payments-mx`.

---

## Qué hace

Le decís a Claude:

> "Voy a abrir un e-commerce de notebooks en Argentina, ¿qué gateway uso y cómo armo las cuotas?"

Y te responde con:

- **Gateway recomendado** y por qué (no copia-pega de marketing)
- **Métodos a aceptar** (tarjeta sí, cuotas sí pero con qué modelo post-Ahora 12 derogado, QR interoperable obligatorio, Rapipago/Pago Fácil si tu target incluye no-bancarizados)
- **Fee efectivo estimado** sobre tu ticket promedio y plan de acreditación elegido
- **Estrategia de cuotas** post-derogación Ahora 12 (junio 2026) — absorber merchant vs trasladar cliente vs híbrido
- **Gotchas operativos** que no están en docs (hold anti-fraude MP de 7-21 días, surcharge +3% a tarjetas internacionales, categoría BCRA cambiante en Decidir, etc.)
- **Próximos pasos concretos** para implementar

Cubre las decisiones que más rompen pyme y startup en AR:

- Mercado Pago AR (con sus 4 planes de acreditación: inmediato 6.29% → 35d 1.49%) vs Decidir/Prisma (1.80% regulado) vs dLocal (USD payouts) vs MODO vs PayU vs Ualá Bis vs Naranja X Toque
- Tarjeta, débito, cuotas (3/6/12/18/24), QR interoperable/Transferencia 3.0, Rapipago, Pago Fácil, saldo MP, MODO, Mercado Crédito, Plan Z Naranja, Binance Pay/USDT
- Patrones de **marketplace** con MP Marketplace API (el único stack serio en AR)
- Estado actual de **Ahora 12** (DEROGADO junio 2026) y cómo modelar cuotas sin subsidio estatal
- Cepo cambiario — cómo cobrar USD desde AR legalmente (dLocal Pay-outs vs estructura offshore vs USDT)
- Marco regulatorio: BCRA Com 'A' 8432/2026, AFIP Factura Electrónica con CAE

---

## Por qué este skill existe

Las páginas de pricing de los gateways en AR mienten más que en cualquier otro país LATAM:

- Mercado Pago muestra "desde 1.49%" pero el default de la cuenta nueva es 6.29%
- Decidir cambia tu plazo de cobro de T+8 a T+18 sin avisar cuando te reclasifica de categoría
- "Cuotas sin interés" ya no son gratis — Ahora 12 fue derogado en junio 2026
- Cuotas con CFT 22% destruyen tu margen si no las modelás bien
- Y todo cambia con la próxima Comunicación BCRA

Este skill consolida:

- Investigación de fees publicada al **2026-06-10**
- Adopción real de métodos (BCRA Informe de Pagos Minoristas, Infobae, secundarias serias)
- Patrones de marketplace y cuotas probados
- Decisiones por vertical (e-commerce general, marketplace, SaaS B2B, retail alto ticket, freelance cross-border, gastro físico)

---

## Instalación

```bash
# Copiá el skill donde tu Claude Code lo lea
cp -r payments-ar/ ~/.claude/skills/payments-ar/
```

No hay setup. Es un skill de conocimiento — no ejecuta nada en tu máquina.

---

## Uso

Activá el skill mencionando cualquier de estos triggers:

- "¿Qué gateway uso para mi tienda en Argentina?"
- "Compará Mercado Pago vs Decidir para electro"
- "Comisiones reales de MP Argentina 2026"
- "¿Cómo integro Rapipago / Pago Fácil?"
- "Voy a hacer un marketplace en AR, ¿cómo cobro?"
- "Cuotas sin interés post-Ahora 12"
- "Cobrar en dólares desde Argentina con cepo"
- "QR interoperable / Transferencia 3.0"
- "Naranja Plan Z"

Claude te preguntará por tu vertical, ticket promedio, si necesitás cuotas, marketplace, cross-border, y devolverá una recomendación accionable.

---

## Estructura

```
payments-ar/
├── SKILL.md              # Cuándo activarse + workflow + árbol de decisión + cuotas + cepo
├── README.md             # Esto que estás leyendo
├── data/
│   ├── gateways.json     # 7 gateways: fees, payout, marketplace, gotchas
│   └── methods.json      # 14 métodos: adopción, settle, recomendaciones por vertical
└── examples/
    └── ecommerce-electro-cuotas.md  # Caso end-to-end electro con cuotas post-Ahora 12
```

---

## Frescura

Datos verificados al `2026-06-10`. **Importante:** las comisiones de MP AR cambian seguido por inflación + decisiones regulatorias. Antes de firmar contrato o decisión de pricing, validá contra el campo `pricing_url` de `data/gateways.json`.

Si detectás un cambio, edití `data/gateways.json` y actualizá `_meta.as_of`.

---

## Lo que NO hace

- No reemplaza a un contador ni abogado fintech AR
- No emite Factura Electrónica con CAE — eso es AFIP + un emisor (Tango, Contabilium, etc.)
- No predice cambios futuros en fees ni del marco regulatorio cuotas
- No genera código de producción listo para deploy — da patrones; los snippets viven en `examples/`
- No cubre pagos en otros países LATAM (cada uno tiene su skill: `payments-mx`, `payments-co`, `payments-pe`, `payments-cl`, `payments-br`, `payments-es`)
- No es asesor de USDT/cripto — lo lista como contexto cuando aplica

---

## Cómo aportar

Issues y PRs bienvenidos:

- https://github.com/lahh1986/sistemia-skills-mx/issues

Si trabajás con un gateway que no está cubierto (Brubank Empresas, Modo White Label, etc.) o ves un fee que ya no cuadra, abrí PR con un objeto siguiendo el shape de `data/gateways.json`.

---

## Licencia

MIT. Skill mantenido por [Sistemia](https://sistemia.mx).
