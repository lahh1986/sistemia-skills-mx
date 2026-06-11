# Caso: e-commerce de electrónicos en Argentina con cuotas

> Tienda online que vende celulares, notebooks y electrodomésticos en
> Argentina. Cliente target: CABA + GBA + Córdoba + Rosario. Ticket promedio
> ARS 250,000–800,000. Necesita cuotas sí o sí — sin cuotas no se vende
> electro en AR. Post-derogación Ahora 12 (junio 2026), las cuotas ya no son
> "gratis" — hay que modelar el costo financiero.

## Diagnóstico

| Variable | Valor |
|---|---|
| Vertical | E-commerce retail electro |
| Ticket promedio | ARS 250,000–800,000 |
| Cuotas culturales | Sí, 3/6/12/18 obligatorio |
| Marketplace | No (vendor único) |
| Cross-border | No (MX-only) |
| Recurrencia | No (transaccional) |
| Bancarización del target | Alta (75-80%) |
| Geografía | CABA/GBA + Córdoba + Rosario (alto Naranja en Córdoba) |
| Volumen mensual proyectado | ARS 5M–20M GMV |

## Recomendación

**Stack principal:** **Mercado Pago Checkout API + Decidir como secundario**

**Por qué:**
1. MP cubre el 80% del flujo: tarjeta + cuotas + saldo MP + QR + Mercado Crédito. Un solo SDK, un solo onboarding.
2. Decidir como secundario para clientes premium bancarizados que prefieren débito (0.80% regulado) y para cuando MP haga hold.
3. Naranja Plan Z se aprovecha vía MP — no necesitás integrar Naranja directo.
4. QR interoperable activado para tickets medios — 0.80% es regalo.

**Plan de acreditación MP:** Empezar con **14 días (3.49%)** — balance entre fee bajo y flujo de caja. Migrar a 35d (1.49%) cuando tengas runway de 35 días asumido.

## Métodos a aceptar y prioridad

| Prioridad | Método | Por qué | Fee efectivo MP 14d |
|---|---|---|---|
| 1 | Tarjeta crédito 3/6/12 cuotas | Default cultural electro | 3.49% + CFT cuotas |
| 2 | Mercado Crédito (BNPL embebido) | Captura no-tarjeta | ~5-15% según plazo |
| 3 | Saldo Mercado Pago | UX 1-tap | 3.49% |
| 4 | Tarjeta crédito 1 pago | Alto ticket sin cuotas | 3.49% |
| 5 | QR interoperable / Transferencia 3.0 | Cliente avanzado, fee bajísimo | 0.80% |
| 6 | Débito Decidir | Premium bancarizado | 0.80% |
| 7 | Rapipago / Pago Fácil | 8% del mercado sin tarjeta | 3.49% + 24-72h hold |

Skip: USDT, Binance Pay (no aplica retail B2C electro), Wibond/WIPEI (mercado_credito de MP los come).

## Estrategia de cuotas post-Ahora 12

Modelo recomendado: **Híbrido**

| Plazo | Quién absorbe | UI al cliente |
|---|---|---|
| 1 pago contado | — | "Precio: ARS 500.000" |
| 3 cuotas | Merchant (5.39% CFT) | "3 cuotas SIN INTERÉS de ARS 166.667" |
| 6 cuotas | Híbrido (merchant 6%, cliente 4.82%) | "6 cuotas de ARS 87.500" |
| 12 cuotas | Cliente (22.22% CFT) | "12 cuotas de ARS 50.000 (Total financiado: ARS 600.000)" |

**Justificación:** 3 cuotas las absorbe el merchant porque es el plazo que más convierte. 12 cuotas las traslada porque sino el margen se evapora (22% CFT = sin ganancia).

**Naranja Plan Z bonus:** activá Plan Z para que clientes con tarjeta Naranja vean "1 ó 3 cuotas sin interés" al cierre — Naranja absorbe ese costo, no vos.

## Arquitectura del checkout

```
Cliente entra al checkout
        ↓
Detecta si tiene cuenta MP (via cookie/login)
   ├── Sí: muestra saldo MP + Mercado Crédito como botones top
   └── No: muestra tarjeta + QR + cuotas
        ↓
Cliente elige medio + plazo
        ↓
Si elige cuotas:
   ├── 3 cuotas → MP cobra 3.49% + CFT 5.39% absorbido al merchant
   ├── 6 cuotas → CFT 10.82% repartido (config preferencia MP)
   └── 12 cuotas → CFT 22.22% al cliente (preferencia "interest_free": false)
        ↓
MP procesa → webhook → tu sistema confirma orden
        ↓
Hold MP de 7-21 días si cuenta nueva — flag en sistema "pending_payout"
```

## Flujo de implementación (MVP en 2 semanas)

### Semana 1 — Setup MP + tarjeta + cuotas básicas

1. Crear cuenta MP Developers AR — `client_id` + `client_secret`
2. Implementar Checkout API con `preference`:
   ```javascript
   const preference = {
     items: [{ title, quantity, unit_price }],
     payment_methods: {
       installments: 12,  // max
       default_installments: 3,
       excluded_payment_types: []  // dejar todos para AR
     },
     notification_url: 'https://tu-tienda.ar/api/mp-webhook',
     external_reference: order_id
   };
   ```
3. Implementar webhook receiver con idempotencia
4. Test sandbox con test users AR

### Semana 2 — Plan de acreditación + cuotas avanzadas

1. Cambiar plan de acreditación a 14d en panel MP (default es inmediato 6.29%)
2. Configurar costo por cuota en panel "Costos y cuotas" — decidir qué plazos sin interés (3) vs con interés (6, 12)
3. Activar Mercado Crédito como flag — `purpose: "wallet_purchase"` en preferencia
4. UI del checkout muestra simulador de cuotas con CFT real al cliente
5. Onboardear a Decidir como segundo gateway para débito (paralelo, no reemplazo)

## Gotchas específicos AR

1. **Hold anti-fraude MP** — cuenta nueva tiene hold de 7-21 días en el 100% de las ventas. Acumulá runway de ARS 5M antes de lanzar.

2. **Plan de acreditación** — default es 6.29% inmediato. Cambialo a 14d (3.49%) en panel apenas tengas cuenta. Diferencia de 2.8% = ARS 140k por ARS 5M facturado.

3. **CFT cuotas en panel MP** — revisá quincenalmente. MP los actualiza con BCRA y cambia tu costo silenciosamente.

4. **Surcharge tarjeta internacional +3%** — si vendés a turistas o expat, agregá filtro: tarjeta no-AR → mostrar "fee de servicio internacional" o desactivar cuotas.

5. **Naranja Plan Z** — activación requiere que tu seller esté en categoría compatible. Pedile a MP que confirme.

6. **Facturación AFIP** — la factura es por el monto TOTAL (no por cuota). Si vendés a Monotributo, controlá los topes de categoría. Skill `afip-ar` futuro.

7. **Inflación crónica** — tu pricing necesita lógica de revaluación semanal o quincenal. No fijés precios para un mes.

## Costos estimados primer año

Asumiendo ARS 10M/mes GMV, mix típico (60% cuotas, 30% contado, 10% otros):

| Concepto | Monto ARS/año |
|---|---|
| Fees MP (4.5% efectivo blended) | 5,400,000 |
| IVA fees | 1,134,000 |
| CFT cuotas absorbido (3 cuotas) | 3,200,000 |
| Disputas + holds estimados | 600,000 |
| **Total operación pagos** | **~10,334,000/año** |

A 10M/mes = 120M/año GMV. Costo total = 8.6% del GMV. Margen bruto del electro típico AR 25-35% — pagos se llevan ~30% de tu margen.

**Implicación:** los electros muy commodity (celulares mainstream) no funcionan en este stack — el margen post-fees es muy fino. Funciona en electro premium o nichos.

## Cuándo replantear

Si llegás a uno de estos disparadores, considerá ajustar:

- **Volumen > ARS 50M/mes:** negociá fee con MP, podés bajar de 3.49% a ~2.5% con cierto volumen
- **Hold MP crónico:** considerá Decidir como gateway principal (tarjeta) + MP secundario (cuotas + QR)
- **Inflación dispara CFT cuotas > 30%:** trasladá 100% al cliente o reducí plazos máximos a 6 cuotas
- **Buyers internacionales:** agregá Stripe con estructura US (no podés hacerlo desde entidad AR puro)

## Próximos pasos concretos

1. Crear cuenta MP Developers AR — `developers.mercadopago.com.ar` (1 día)
2. Implementar OAuth + Checkout API con cuotas (3-4 días)
3. Configurar plan acreditación 14d en panel MP (10 min)
4. Configurar "Costos y cuotas" con tu estrategia híbrida (1 día)
5. Implementar webhook receiver idempotente (1 día)
6. UI simulador de cuotas con CFT visible al cliente (1 día)
7. Decidir si sumás Decidir como gateway secundario (decisión, no implementación urgente)
8. Coordinar con contador AR — Factura Electrónica + Monotributo/IVA + cuándo emitís CAE — bloqueador legal antes de producción

---

**Sub-skill futuro:** `payments-ar-cuotas-calculator` que dado tu ticket, mix esperado y plazo te devuelve fee efectivo + margen post-financiero.
