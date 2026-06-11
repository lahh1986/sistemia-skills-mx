---
name: contador-pyme-mx
description: |
  Usar cuando el usuario sea CONTADOR de PyMEs MEXICANAS y necesite validar
  CFDI 4.0, detectar errores caros antes de timbrar/cancelar, cruzar
  proveedores contra listas 69-B, validar retenciones a personas físicas
  (honorarios, arrendamiento, RESICO 1.25%), aplicar reglas de cancelación
  (motivos 01-04), checar Carta Porte 3.1, alertar PUE timbrados a fin de
  mes que pueden quedar como ingreso fantasma. Anclado en corpus oficial
  (Anexos RMF 2026, XSDs SAT, listas 69-B, leyes federales).

  Triggers: "valida este CFDI", "este XML está bien", "el SAT lo va a rechazar",
  "PUE PPD", "cancelar CFDI motivo", "retención RESICO", "honorarios 10%",
  "arrendamiento 10.67% IVA", "Carta Porte", "complemento pagos", "régimen
  fiscal receptor", "uso CFDI", "metodo de pago", "factura electrónica",
  "Anexo 20", "validar nómina", "contador México", "contabilidad fiscal".
---

# contador-pyme-mx — Skill para contadores PyME (CFDI + validación)

> Familia de validadores y calculadoras para el contador mexicano de PyMEs.
> v1.0 = `cfdi-validator-mx` (núcleo). Siguientes módulos en backlog:
> `nomina-mx`, `declaraciones-mx`, `descarga-masiva-cfdi-mx`,
> `valores-vigentes-mx`, `opinion-32d-mx`.

## Cuándo activarte

- El usuario te pasa un XML de CFDI y pregunta si está bien armado
- El usuario está por cancelar/sustituir un CFDI y pregunta qué motivo poner
- El usuario tiene proveedores y quiere checar si alguno está en lista 69-B
- El usuario timbró PUE a fin de mes y se da cuenta que aún no le pagaron
- El usuario emitió CFDI a una PF en RESICO y olvidó la retención 1.25%
- El usuario mueve mercancía y pregunta sobre Carta Porte
- El usuario menciona régimen fiscal, uso CFDI, forma de pago, método de pago

**NO actives si:** el usuario quiere asesoría legal específica de un litigio fiscal — para eso refiere a abogado fiscalista.

## Módulos disponibles (v1.0)

### Bloque CFDI
| Módulo | Script | Resuelve |
|---|---|---|
| 1. Validador CFDI 4.0 estructural | `scripts/validate_cfdi.py` | XML válido contra XSD + catálogos vigentes (régimen, uso, forma pago, etc.) + retenciones obligatorias + cruce 69-B |
| 2. Check PUE/PPD cruce mes | `scripts/check_pue_ppd.py` | Alerta CFDIs PUE timbrados últimos 5 días del mes sin pago confirmado |
| 3. Validador motivo cancelación | `scripts/check_cancellation.py` | Determina motivo (01-04) correcto + valida folio sustituto si motivo 01 |

### Bloque Nómina
| Módulo | Script | Resuelve |
|---|---|---|
| 4. Calculadora de nómina | `scripts/calc_nomina.py` | ISR Art. 96 + subsidio empleo + 8 cuotas IMSS + INFONAVIT 5% + ISN estatal + costo total patrón |
| 5. Calculadora finiquito/liquidación | `scripts/calc_finiquito.py` | Aguinaldo + vacaciones (reforma 2023) + prima vacacional + indemnización + prima antigüedad bajo LFT |

### Bloque Declaraciones (nuevo)
| Módulo | Script | Resuelve |
|---|---|---|
| 6. Pago provisional ISR mensual | `scripts/calc_pago_provisional_isr.py` | PM Art. 14 (coef. utilidad) · PF Art. 106 · RESICO PF Art. 113-E (1-2.5%) · RESICO PM Art. 207 · Arrendamiento Art. 116 |
| 7. IVA mensual | `scripts/calc_iva_mensual.py` | LIVA Art. 5-D: trasladado cobrado - acreditable pagado - retenciones - saldos a favor |
| 8. Generador DIOT TXT | `scripts/gen_diot_txt.py` | Convierte CSV de proveedores en TXT pipe-delimited para plataforma nueva DIOT |
| 9. Declaración anual PF | `scripts/calc_declaracion_anual_pf.py` | LISR Art. 152 — múltiples ingresos + deducciones personales con tope global |

### Composables (delega a otros skills)
| Módulo | Script | Resuelve |
|---|---|---|
| 10. Checker 69-B (delega legal-pyme-mx) | `~/sistemia-skills-mx/skills/legal-pyme-mx/scripts/validate_rfc.py` | Cruza RFC vs 11 listas SAT |
| 11. ISN por estado (lee de legal-pyme-mx) | `~/sistemia-skills-mx/skills/legal-pyme-mx/data/isn_por_estado.json` | Tasa ISN 1.8-3.0% por entidad |

## Workflow

### Paso 1: Identifica intent

| Intent del usuario | Acción |
|---|---|
| "valida este CFDI" / "este XML está bien" | `validate_cfdi.py archivo.xml` |
| "el SAT rechazó" / "errores en CFDI" | `validate_cfdi.py archivo.xml --verbose` |
| "voy a cancelar CFDI" | `check_cancellation.py --uuid=... --motivo=01 --folio-sustituto=...` |
| "PUE pendientes" / "facturas no cobradas" | `check_pue_ppd.py --dir=cfdis/` |
| "calcular nómina" / "cuánto retengo de ISR" / "costo del empleado" | `calc_nomina.py --salario-mensual X --estado Y --clase-rt III` |
| "finiquito" / "indemnización" / "vacaciones pendientes" | `calc_finiquito.py --salario-diario X --fecha-alta Y --fecha-baja Z --tipo renuncia\|despido-injustificado` |
| "pago provisional ISR" / "RESICO mensual" / "PM coeficiente utilidad" | `calc_pago_provisional_isr.py --regimen=pm-general\|pf-act-emp\|resico-pf\|resico-pm\|arrendamiento` |
| "IVA del mes" / "IVA acreditable" / "saldo a favor IVA" | `calc_iva_mensual.py --iva-trasladado-cobrado X --iva-acreditable-pagado Y` |
| "generar DIOT" / "DIOT TXT" / "plataforma DIOT" | `gen_diot_txt.py --csv proveedores.csv --periodo 2026-05` |
| "declaración anual" / "deducciones personales" / "saldo a favor anual" | `calc_declaracion_anual_pf.py --ingresos-sueldos X --gastos-medicos Y --colegiaturas Z --ejercicio 2025` |
| "RESICO retención" / "honorarios 10%" | `validate_cfdi.py` (lo detecta automáticamente) |
| "este proveedor está en 69-B" | invoca `legal-pyme-mx/scripts/validate_rfc.py <RFC> --check-69b` |
| "Carta Porte" | `validate_cfdi.py archivo.xml` (detecta complemento Carta Porte 3.1 automáticamente) |

### Paso 2: Si es validación de CFDI, corre el flujo completo

```bash
~/sistemia-skills-mx/skills/contador-pyme-mx/scripts/validate_cfdi.py archivo.xml
```

El script valida en orden:
1. **Estructura XML** contra XSD `cfdv40.xsd`
2. **Catálogos** (RegimenFiscal, UsoCFDI, FormaPago, MetodoPago, ClaveProdServ, ClaveUnidad)
3. **Reglas de negocio** (régimen receptor compatible con uso CFDI, total = subtotal - descuentos + impuestos, etc.)
4. **Detección de complementos** (Pagos 2.0, Nómina 1.2, Carta Porte 3.1, Retenciones)
5. **Si tiene Retenciones**: valida monto contra tasas oficiales por concepto
6. **Si emisor es RESICO PF y receptor PM**: alerta si NO viene retención 1.25% ISR
7. **Cruce 69-B** del RFC emisor y receptor (delega a `legal-pyme-mx/check_69b.py`)

### Paso 3: Output al usuario

```markdown
## Validación CFDI {{folio/UUID}}

**Veredicto:** ✅ Válido / ⚠️ Válido con advertencias / 🚨 Inválido (no timbrar)

### Estructura XML
- [✓/✗] Pasa esquema XSD cfdv40
- [✓/✗] Versión 4.0

### Datos fiscales receptor
- RFC: {{rfc}} — {{vigente / cancelado / no encontrado}}
- Régimen fiscal: {{cod}} {{nombre}} — {{compatible con uso CFDI / INCOMPATIBLE}}
- CP fiscal: {{cp}} — {{coincide con datos SAT / por verificar manual}}
- Uso CFDI: {{cod}} {{nombre}}

### Catálogos
- Forma de pago: {{cod}} ({{descr}})
- Método de pago: {{cod}} (PUE/PPD)
- {{Si PUE y fecha emisión >25 del mes: alerta cruce mes}}

### Complementos detectados
- {{Pagos 2.0 / Nómina 1.2 / Carta Porte 3.1 / Retenciones v2.0}}

### Riesgos detectados
- {{Lista de hallazgos con su impacto en MXN si aplica}}

### Cruce 69-B
- RFC emisor en lista SAT: {{NO / 69-B Definitivos / 69 CFF / etc.}}
- RFC receptor en lista SAT: {{NO / ...}}

### Recomendación accionable
{{1-2 líneas}}
```

### Paso 4: Cierre

Siempre cierra con:
1. **Decisión binaria** (timbrar / cancelar / corregir y re-timbrar)
2. **Si hay riesgo**, cuál es la **multa potencial** en MXN
3. **Cuál es la fuente** (artículo LISR/LIVA/CFF o Anexo RMF)

## Los 5 errores más caros que este skill previene

| Error | Multa | Cómo lo detecta el skill |
|---|---|---|
| 1. CFDI con régimen receptor / uso CFDI / CP / nombre incorrectos | $400-15,000 por comprobante | `validate_cfdi.py` cruza datos receptor vs catálogos + Anexo 20 reglas |
| 2. PUE timbrado a fin de mes sin cobro real | Acumulación ISR/IVA sobre ingreso fantasma | `check_pue_ppd.py` alerta PUE de últimos 5 días sin Complemento Pagos posterior |
| 3. Cancelación CFDI sin motivo correcto (01-04) o sin folio sustituto | Bloqueo de cancelación + cliente sin poder deducir | `check_cancellation.py` aplica reglas Anexo 20 |
| 4. RESICO PF→PM sin retención 1.25% ISR | PM pierde deducibilidad, PF recibe requerimiento | `check_retenciones.py` detecta emisor RESICO + receptor PM |
| 5. Acreditar IVA de proveedor en lista 69-B | Pérdida acreditamiento + multa indirecta | Cruce automático contra `legal-pyme-mx/sat/listas-negras/` (14,436 RFCs) |

## Lo que NO hace este skill v1.0

- **No emite/timbra CFDI.** Solo valida XMLs ya generados o por generar.
- **No genera nómina.** Eso es módulo `nomina-mx` (v1.1).
- **No presenta declaraciones.** Eso es módulo `declaraciones-mx` (v1.1).
- **No descarga masivo del SAT.** Eso es módulo `descarga-masiva-cfdi-mx` (v1.1) — requiere FIEL.
- **No asesoría legal personalizada.** Información operacional basada en corpus oficial.

## Fuentes del corpus

Ver `research/fiscal-INDEX.md` para mapa temático completo. Resumen:

- **SAT esquemas:** 11 XSDs CFDI 4.0 (`research/contador-pyme-mx-corpus/esquemas-cfdi/`)
- **SAT contabilidad electrónica:** 6 XSDs (`/esquemas-contabilidad/`)
- **SAT RMF 2026:** Anexo 8 (tarifas ISR) + Anexo 24 (contabilidad) + Anexo 20 (guía CFDI) + Guía Nómina
- **SAT listas negras:** 11 CSVs en `research/sat/listas-negras/` (del skill legal-pyme-mx)
- **Diputados leyes:** CFF, LISR, LIVA, LIEPS, LFT, LSS (todas vigentes 2026)
- **INEGI:** INPC histórico CSV
- **Banxico SIE:** FIX `SF43718` via API con token
