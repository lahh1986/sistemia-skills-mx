# Caso: marketplace B2C estilo eltianguis

> Marketplace que conecta vendedores chicos con compradores en MX. Cobra al
> buyer, paga al seller, retiene comisión de la plataforma. Cero booking,
> cero CMS para el seller — todo via WhatsApp o app ligera.

## Diagnóstico

| Variable | Valor |
|---|---|
| Vertical | Marketplace B2C |
| Ticket promedio estimado | $250–$2,500 MXN |
| Sellers | Personas físicas + pymes mexicanas |
| Buyers | Consumidor final MX, clase media |
| Cross-border | No (MX-only fase 1) |
| Recurrencia | No (transaccional) |
| Captar clientes sin tarjeta | Sí — OXXO obligatorio |
| Volumen mensual proyectado | $50k–500k MXN primeros 6 meses |

## Recomendación

**Stack principal:** **Mercado Pago Marketplace API**

**Por qué:**
1. Único stack que combina **split payments nativo + OXXO Pay end-to-end + saldo MP** sin cableado custom
2. Onboarding del seller con OAuth (no implementas KYC propio fase 1)
3. La marca MP da confianza al buyer mexicano — reduce fricción en checkout
4. Lock-in es real pero aceptable mientras MVP valide demanda

**Alternativa si después necesitas cross-border o sellers de US:** migrar a **Stripe Connect** — re-onboarding pesado pero técnicamente más flexible.

## Métodos a aceptar

| Método | Por qué | Fee MP |
|---|---|---|
| Tarjeta crédito/débito | 60% del e-commerce MX | 3.49% + $4 (instant) |
| OXXO Pay | 10% del mercado sin tarjeta | 3.79% + $4 |
| SPEI | Tickets > $500 | 3.49% + $4 |
| Saldo Mercado Pago | 15% de usuarios ya tienen saldo, conversión 1-tap | 3.49% + $4 |

Skip CoDi, DiMo, BNPL en fase 1.

## Arquitectura de fondos

```
Buyer paga $1,000 MXN
        ↓
Mercado Pago retiene comisión: ~3.49% + $4 = $39 + IVA = $45
Quedan: $955
        ↓
Plataforma (eltianguis) cobra application_fee: 10% = $100
Seller recibe: $855 vía transfer automático a su cuenta MP
        ↓
Liberación: configurable con release_date (escrow opcional)
```

## Flujo de implementación (MVP en 2 semanas)

### Semana 1 — Onboarding seller

1. Seller llega via WhatsApp / página landing
2. Eltianguis crea sub-cuenta MP via OAuth
3. Seller autoriza acceso → eltianguis guarda `access_token` y `user_id` de MP
4. Validación de RFC contra SAT (skill `sat-mx`)
5. Seller ya puede recibir pagos

```javascript
// Pseudo
const oauthUrl = `https://auth.mercadopago.com.mx/authorization?client_id=${MP_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}`
// → buyer authoriza → callback con code → exchange por access_token
```

### Semana 2 — Checkout buyer + split

1. Buyer elige producto → eltianguis crea `preference` con MP usando `access_token` del seller
2. `marketplace_fee` = 10% del total (la comisión plataforma)
3. Buyer va a Checkout Pro de MP, paga con método elegido
4. MP cobra al buyer, transfiere al seller, deposita comisión a plataforma
5. Webhook a eltianguis confirma pago → notifica a seller via WhatsApp

```javascript
// Preference base
const preference = {
  items: [{ title, quantity, unit_price }],
  marketplace_fee: amount * 0.10,  // comisión eltianguis
  collector_id: seller_mp_user_id,
  notification_url: 'https://eltianguis.sistemia.mx/api/mp-webhook',
  external_reference: order_id
}
```

## Gotchas específicos

1. **Webhooks duplicados** — MP envía el mismo webhook 3-5 veces. Implementa idempotencia con `external_reference` + `status`.

2. **Estados de pago MP** — pending, approved, in_process, rejected, refunded. Solo `approved` libera al seller. `in_process` = revisión manual MP (puede tardar 24h).

3. **OXXO Pay drop-off** — el buyer recibe voucher pero no paga hasta 24-72h después. Tu UI debe mostrar "pago pendiente" claramente y notificar cuando MP confirme.

4. **Disputas y chargebacks** — MP carga $300 MXN por dispute. Tu T&C debe definir quién absorbe: plataforma o seller. Recomendación: seller, con seguro de plataforma capeado.

5. **CFDI** — MP NO emite CFDI. Eltianguis (o el seller, según modelo de negocio) debe emitirlo al buyer. Define quién factura ANTES de operar — si plataforma factura por seller, necesitas figura de comisionista mercantil con contrato.

6. **PLD/CFT** — sobre cierto volumen mensual (~12,500 UMAs ≈ $1.6M MXN/mes) entras a Régimen 1 de PLD. Manda mensual a CNBV. Skill `legal-pyme-mx` cubre detalle.

## Costos estimados primer año

Asumiendo $200k MXN/mes en GMV, mix típico (60% tarjeta, 25% OXXO, 15% otros):

| Concepto | Monto MXN/año |
|---|---|
| Fees MP (4.0% efectivo blended) | $96,000 |
| IVA fees | $15,360 |
| Disputas (estimadas 1%) | $7,200 |
| **Total operación pagos** | **~$118,560/año** |

Tu margen plataforma a 10% application_fee: $240,000/año bruto antes de fees MP.

**Margen neto después de fees:** $121,440/año = ~5% del GMV.

## Cuándo replantear

Si llegas a uno de estos disparadores, considera migrar a Stripe Connect:
- Sellers internacionales (US/LATAM no-MX)
- Buyers internacionales (USD)
- Volumen > $5M MXN/mes y MP no negocia tarifa
- Quieres control fino de UX en checkout (MP Checkout Pro es opinionado)

## Próximos pasos concretos

1. Crear cuenta MP Developers MX y obtener `client_id` / `client_secret`
2. Implementar OAuth flow del seller (1-2 días)
3. Implementar `preference` con `marketplace_fee` (1 día)
4. Implementar webhook receiver con idempotencia (1 día)
5. Implementar pantalla "pago pendiente OXXO" con polling (medio día)
6. Pruebas en sandbox con test users (2-3 días)
7. Acordar con contador modelo CFDI (plataforma vs seller emite) — bloqueador legal antes de producción

---

**Sub-skill futuro:** `payments-mx-mp-marketplace` con código de integración listo para producir.
