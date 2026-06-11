# contador-pyme-mx — Ejemplos

## Ejemplo 1: Validar un CFDI sospechoso (RESICO PF a PM)

**Usuario:** "Mi cliente PM compró servicios de un freelancer RESICO y el XML no trae retención. ¿Está bien?"

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/validate_cfdi.py /ruta/al/cfdi.xml
```

**Output esperado:**

```json
{
  "veredicto": "🚨 INVÁLIDO / NO_TIMBRAR",
  "hallazgos": [
    {"sev":"🚨","tipo":"retencion_resico",
     "mensaje":"Emisor RESICO PF (régimen 626) factura a Persona Moral.
                Falta retención ISR 1.25% (LISR Art. 113-J). Sin esto:
                PM NO puede deducir el gasto + PF recibe requerimiento SAT."}
  ]
}
```

**Lectura para el usuario:**
> 🚨 **NO aceptes ese CFDI.** Pídele al freelancer que lo re-emita con la
> retención ISR 1.25% en el nodo `cfdi:Impuestos/cfdi:Retenciones`. Sin esa
> retención NO puedes deducir el gasto. Para un servicio de $10,000 + IVA
> (PM general 30% ISR + 16% IVA), perdiendo deducibilidad pierdes ~$4,600
> en ISR + IVA.

---

## Ejemplo 2: Auditar PUEs a fin de mes (cierre fiscal)

**Usuario:** "Cierre de mes mayo. Quiero ver qué CFDIs PUE timbré los últimos 5 días que NO se han cobrado todavía."

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/check_pue_ppd.py \
  --dir ~/contabilidad/cliente_x/cfdis/2026/ \
  --mes 2026-05 \
  --days-before-eom 5
```

**Output:**

```json
{
  "total_cfdis_revisados": 142,
  "pues_fin_mes_total": 8,
  "pues_fin_mes_SIN_PAGO": 3,
  "pues_fin_mes_con_pago_posterior": 5,
  "alerta": "🚨 3 CFDIs PUE timbrados los últimos 5 días del mes NO tienen complemento de pagos posterior...",
  "cfdis_sin_pago": [
    {"uuid": "abc-123", "fecha": "2026-05-29", "total": "45000.00", "receptor": "XYZ123"},
    {"uuid": "def-456", "fecha": "2026-05-30", "total": "12500.00", "receptor": "ABC789"},
    {"uuid": "ghi-789", "fecha": "2026-05-31", "total": "78000.00", "receptor": "MNO345"}
  ]
}
```

**Decisión accionable:**

Para cada uno de los 3, hoy mismo (último día del mes):

1. **Confirmar con tu cliente cuáles SÍ se cobraron en banco** → si entró el cobro entre el timbrado y el día 31, generar Complemento Pagos AHORA con fecha del día efectivo de pago.
2. **Los que NO se cobraron** → 2 opciones:
   - Cancelar (motivo 03) y re-emitir como PPD
   - Solicitar al receptor que pague antes del cierre y emitir complemento de pago el día efectivo

Si no haces nada, el SAT asume los 3 como cobrados ($135,500) → ISR + IVA sobre ese fantasma = ~$60K en impuestos que el cliente NO recibió.

---

## Ejemplo 3: Cancelar un CFDI mal emitido

**Usuario:** "Emití un CFDI a un cliente con CP mal. Voy a cancelar y re-emitir. ¿Qué motivo uso?"

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/check_cancellation.py \
  --uuid="aaaa-1111-2222-3333-444444444444" \
  --motivo=01 \
  --folio-sustituto="bbbb-5555-6666-7777-888888888888" \
  --fecha-original=2026-05-28 \
  --tipo=I \
  --total=23500
```

**Output:**

```json
{
  "veredicto": "✅ OK_PARA_CANCELAR",
  "hallazgos": [
    {"sev":"ℹ️", "mensaje":"Motivo 01: Comprobante emitido con errores con relación"}
  ]
}
```

**Si te equivocas y NO emites el sustituto primero:**

```bash
./check_cancellation.py --uuid=... --motivo=01  # sin --folio-sustituto
```

→ `🚨 NO CANCELAR: Motivo 01 REQUIERE FolioSustitucion. El PAC va a rechazar la cancelación.`

**Flujo correcto:**
1. Emite el CFDI nuevo (con datos corregidos) → obtienes UUID nuevo
2. Cancela el CFDI viejo con motivo=01 + folio-sustituto=UUID nuevo
3. El sistema SAT vincula ambos automáticamente

---

## Ejemplo 4: Auditoría completa de un mes (composable)

**Usuario:** "Quiero el cierre completo de cliente Radecom mayo 2026 — válida CFDIs, cruza 69-B, alerta PUEs, lista retenciones."

```bash
DIR=~/contabilidad/radecom/cfdis/2026/05/

# 1. Validar todos los CFDIs (uno por uno con paralelismo)
find $DIR -name "*.xml" | xargs -P 4 -I {} \
  ~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/validate_cfdi.py {} \
  > /tmp/validations.jsonl

# 2. Filtrar solo los INVÁLIDOS
jq -c 'select(.veredicto | startswith("🚨"))' /tmp/validations.jsonl

# 3. Auditar PUEs fin de mes
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/check_pue_ppd.py \
  --dir $DIR --mes 2026-05

# 4. Listar proveedores en lista negra (de las validaciones)
jq -r '.cruce_69b[] | select(.riesgo_critico) | .rfc' /tmp/validations.jsonl | sort -u
```

**Salida típica para Radecom (140 CFDIs/mes):**
```
Validaciones: 140 total
  ✅ Válidos:                 132
  ⚠️ Con advertencias:          5  (PUE fin mes, mayoría)
  🚨 Inválidos:                3  (1 RESICO sin retención, 2 régimen receptor mal)

PUEs fin mes sin pago:        2  ($45K en riesgo)

Proveedores en 69-B:          0  ✅ limpio
```

---

## Ejemplo 5: Checker rápido por la terminal (pipe)

**Usuario:** "Quiero validar el último XML que me llegó por correo sin descargarlo."

```bash
# pegar el XML directo a stdin
pbpaste | ~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/validate_cfdi.py -
```

O desde un archivo XML descargado:
```bash
cat factura.xml | ~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/validate_cfdi.py -
```

---

## Ejemplo 6: Calcular nómina completa (módulo nuevo)

**Usuario:** "Cliente en Michoacán quiere contratar a una recepcionista por $15,000 mensuales. ¿Cuánto cuesta realmente y cuánto se lleva neto la trabajadora?"

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/calc_nomina.py \
  --salario-mensual 15000 \
  --periodo mensual \
  --estado "Michoacán" \
  --clase-rt III
```

**Output (real, probado):**

| Concepto | Monto |
|---|---|
| **Salario bruto** | $15,000.00 |
| ISR retenido (Art. 96, neto de subsidio) | $1,402.82 |
| IMSS obrero (suma 8 seguros) | $373.46 |
| **Neto trabajadora** | **$13,223.72** |
| | |
| Cuotas patronales IMSS | $2,703.97 |
| Riesgos de Trabajo (clase III, prima media 2.60%) | $389.76 |
| INFONAVIT 5% | $750.00 |
| ISN Michoacán 3% | $450.00 |
| **Costo total para el patrón** | **$19,293.73** |
| Factor costo vs bruto | **1.286×** |

**Lectura accionable:**
> Contratar a la recepcionista cuesta 28.6% más que el sueldo nominal. Para 12
> meses: $231,524 anuales (+ aguinaldo $7,400 mín + vacaciones + prima vac).
> Considera presupuestar **$245,000-260,000 anuales** para esa plaza, no $180,000.

### Variaciones útiles

```bash
# Salario mínimo $315.04 diario en Jalisco, pago semanal
calc_nomina.py --salario-diario 315.04 --periodo semanal --estado "Jalisco" --clase-rt I

# Salario alto en BCN (ISN 1.8% — el más bajo del país)
calc_nomina.py --salario-mensual 50000 --periodo mensual --estado "Baja California" --clase-rt II

# Comparativa: el mismo $25K en CDMX vs Aguascalientes (ISN 3% vs 2.5%)
for ESTADO in "Ciudad de México" "Aguascalientes"; do
  echo "=== $ESTADO ==="
  calc_nomina.py --salario-mensual 25000 --periodo mensual --estado "$ESTADO" --clase-rt III \
    | python3 -c "import json,sys; r=json.load(sys.stdin); print('Costo patrón:', r['RESUMEN']['costo_total_para_el_patron'])"
done
```

---

## Ejemplo 7: Finiquito por renuncia (4 años de antigüedad)

**Usuario:** "Mi trabajador renunció después de 4 años y 4 meses. Ganaba $500 diarios. ¿Cuánto le pago?"

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/calc_finiquito.py \
  --salario-diario 500 \
  --fecha-alta 2022-01-15 \
  --fecha-baja 2026-05-30 \
  --tipo renuncia
```

**Output:**

| Concepto | Monto | Fundamento |
|---|---|---|
| Aguinaldo proporcional (150 días año en curso) | $3,080.08 | LFT Art. 87 |
| Vacaciones pendientes (7.39 días — 18 al año por 5° aniv) | $3,696.10 | LFT Art. 76 (reforma 2023) |
| Prima vacacional 25% | $924.02 | LFT Art. 80 |
| **TOTAL FINIQUITO** | **$7,700.20** | |

Renuncia simple = SIN indemnización ni prima de antigüedad (porque <15 años).

---

## Ejemplo 8: Despido injustificado (6 años, $800 diarios)

**Usuario:** "Voy a despedir sin causa a un empleado de 6 años que gana $800 diarios. ¿Cuánto me cuesta?"

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/calc_finiquito.py \
  --salario-diario 800 \
  --fecha-alta 2020-03-01 \
  --fecha-baja 2026-05-30 \
  --tipo despido-injustificado
```

**Output desglosado:**

```
Finiquito (igual que renuncia):
  Aguinaldo proporcional             $4,928.13
  Vacaciones (9.03 días, 22/año)     $7,227.93
  Prima vacacional                   $1,806.98
  ──────────────────────────────────
  Subtotal finiquito:               $13,963.04

Indemnización (porque es injustificado):
  3 meses constitucional (Art. 48)              $72,000.00
  20 días por año (Art. 50, opción reinstal.)   $99,920.60
  Prima antigüedad (12 días/año × 6.25)         $47,218.48
    (topada a 2× SM zona = $630.08/día)
  ──────────────────────────────────────────
  Subtotal indemnización:                       $219,139.08

TOTAL: $233,102.12 MXN
```

**Lectura para el patrón:**
> Despedir sin causa a este empleado cuesta $233K MXN, **17× su salario mensual**.
> Si la relación está mal, considera (a) negociar mutuo consentimiento (~$50-80K),
> (b) construir expediente con causales justificadas Art. 47 LFT, o (c) ofrecer
> reinstalación. **NO despidas verbalmente** — sin acta circunstanciada, el juez
> laboral lo declara automáticamente injustificado.

---

## Ejemplo 9: Para una contadora en Michoacán (caso de tu amiga)

**Setup:** Tiene 25 clientes pequeños en Morelia / Apatzingán / Huetamo.

```bash
# Para cada cliente, una carpeta
~/contabilidad/
├── cliente_dental_morelia/
│   └── cfdis/2026/05/...
├── cliente_papeleria_apatzingan/
│   └── cfdis/2026/05/...
└── cliente_huertero_huetamo/
    └── cfdis/2026/05/...

# Script de auditoría mensual por cliente
for CLIENTE in ~/contabilidad/*/; do
  echo "=== $(basename $CLIENTE) ==="
  ~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/check_pue_ppd.py \
    --dir $CLIENTE/cfdis/2026/05/ --mes 2026-05 | \
    jq '{cliente: "'$(basename $CLIENTE)'", alerta: .alerta, monto_riesgo: ([.cfdis_sin_pago[].total | tonumber] | add)}'
done
```

**Lo Michoacán-específico:**
- Cálculo nómina: ISN Michoacán **3.0%** (ya en `legal-pyme-mx/data/isn_por_estado.json`)
- Todo lo demás: **idéntico al resto de MX** (federal)
- No hay regla fiscal especial estatal Michoacán que cambie día a día contable
