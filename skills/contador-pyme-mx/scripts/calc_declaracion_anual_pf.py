#!/usr/bin/env python3
"""
contador-pyme-mx · calc_declaracion_anual_pf.py

Calcula la declaración anual de Persona Física (LISR Art. 152) con
deducciones personales (Art. 151), aplicando tarifa anual 2026.

Maneja múltiples tipos de ingreso:
  - sueldos y salarios (Cap. I)
  - actividad empresarial y profesional (Cap. II Sec. I)
  - arrendamiento (Cap. III)
  - dividendos (Cap. IV)
  - intereses (Cap. VI)
  - otros (Cap. IX)

NO incluye RESICO PF (pagos mensuales son definitivos, no van al anual de tarifa).

Uso:
  calc_declaracion_anual_pf.py \\
    --ingresos-sueldos=300000 --retenciones-sueldos=21500 \\
    --ingresos-honorarios=85000 --retenciones-honorarios=8500 \\
    --gastos-medicos=12000 --colegiaturas=18000 --intereses-hipotecarios=24000 \\
    --pagos-provisionales=15000 \\
    --ejercicio=2025
"""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).parent.parent
TARIFAS = json.load(open(BASE / "data" / "tarifas_isr_2026.json"))
VALORES = json.load(open(BASE / "data" / "valores_vigentes_2026.json"))


def aplicar_tarifa_anual(base, rangos):
    if base <= 0:
        return 0.00
    for r in rangos:
        if base >= r["li"] and (r["ls"] is None or base <= r["ls"]):
            return round(r["cf"] + (base - r["li"]) * r["pct"] / 100, 2)
    return 0.00


def calcular_deducciones_personales(args):
    """Suma deducciones personales del Art. 151 LISR y aplica tope global."""
    items = [
        ("Gastos médicos, dentales, hospitalarios, psicológicos", args.gastos_medicos or 0),
        ("Gastos funerales", args.gastos_funerales or 0),
        ("Donativos autorizados", args.donativos or 0),
        ("Intereses reales hipotecarios", args.intereses_hipotecarios or 0),
        ("Aportaciones complementarias retiro", args.aportaciones_retiro or 0),
        ("Primas seguros gastos médicos mayores", args.primas_seguros or 0),
        ("Transporte escolar obligatorio", args.transporte_escolar or 0),
        ("Colegiaturas (preescolar a bachillerato)", args.colegiaturas or 0),
    ]
    total = sum(monto for _, monto in items)
    # Tope global: el menor entre 5 UMA anuales o 15% del ingreso total
    tope_uma = VALORES["topes_y_limites_fiscales"]["deduccion_personal_global_anual"]["tope_mxn_2026"]
    ingreso_total = (args.ingresos_sueldos or 0) + (args.ingresos_honorarios or 0) + (args.ingresos_arrendamiento or 0) + (args.otros_ingresos or 0)
    tope_15pct = ingreso_total * 0.15
    tope_aplicable = min(tope_uma, tope_15pct)
    total_topado = min(total, tope_aplicable)
    return {
        "items": items,
        "suma_sin_topar": round(total, 2),
        "tope_5_uma_anuales_mxn": tope_uma,
        "tope_15pct_ingreso": round(tope_15pct, 2),
        "tope_aplicable": round(tope_aplicable, 2),
        "deducciones_personales_aplicables": round(total_topado, 2),
        "monto_no_deducible_por_tope": round(max(0, total - total_topado), 2)
    }


def main():
    ap = argparse.ArgumentParser()
    # Ingresos
    ap.add_argument("--ingresos-sueldos", type=float, default=0)
    ap.add_argument("--retenciones-sueldos", type=float, default=0)
    ap.add_argument("--ingresos-honorarios", type=float, default=0)
    ap.add_argument("--retenciones-honorarios", type=float, default=0)
    ap.add_argument("--gastos-deducibles-honorarios", type=float, default=0, help="Gastos comprobables actividad profesional (Art. 100-103)")
    ap.add_argument("--ingresos-arrendamiento", type=float, default=0)
    ap.add_argument("--deducciones-arrendamiento", type=float, default=0, help="Comprobables o ciega 35 pct")
    ap.add_argument("--usar-deduccion-ciega-arrend", action="store_true")
    ap.add_argument("--ingresos-intereses", type=float, default=0)
    ap.add_argument("--retenciones-intereses", type=float, default=0)
    ap.add_argument("--otros-ingresos", type=float, default=0)
    # Deducciones personales (Art. 151)
    ap.add_argument("--gastos-medicos", type=float)
    ap.add_argument("--gastos-funerales", type=float)
    ap.add_argument("--donativos", type=float)
    ap.add_argument("--intereses-hipotecarios", type=float)
    ap.add_argument("--aportaciones-retiro", type=float)
    ap.add_argument("--primas-seguros", type=float)
    ap.add_argument("--transporte-escolar", type=float)
    ap.add_argument("--colegiaturas", type=float)
    # Otros
    ap.add_argument("--pagos-provisionales", type=float, default=0, help="ISR pagado en pagos provisionales del ejercicio")
    ap.add_argument("--ejercicio", type=int, default=2025, help="2025 o 2026")
    args = ap.parse_args()

    # Calcular ingresos acumulables
    util_sueldos = args.ingresos_sueldos  # Sueldos van íntegros como acumulable (los exentos no se incluyen como ingreso)
    util_honorarios = args.ingresos_honorarios - args.gastos_deducibles_honorarios
    if args.usar_deduccion_ciega_arrend:
        util_arrend = args.ingresos_arrendamiento * 0.65
    else:
        util_arrend = args.ingresos_arrendamiento - args.deducciones_arrendamiento

    # Intereses se acumulan netos
    util_intereses = args.ingresos_intereses

    ingresos_acumulables = round(util_sueldos + util_honorarios + util_arrend + util_intereses + args.otros_ingresos, 2)

    # Deducciones personales
    dp = calcular_deducciones_personales(args)
    deducciones_personales = dp["deducciones_personales_aplicables"]

    # Base gravable
    base_gravable = max(0, ingresos_acumulables - deducciones_personales)

    # Tarifa anual
    if args.ejercicio == 2026:
        rangos = TARIFAS["tarifa_anual_pf_2026"]["rangos"]
    else:
        rangos = TARIFAS["tarifa_anual_pf_2025"]["rangos"]
    isr_causado = aplicar_tarifa_anual(base_gravable, rangos)

    # Acreditamientos
    total_retenciones = args.retenciones_sueldos + args.retenciones_honorarios + args.retenciones_intereses
    diferencia = isr_causado - total_retenciones - args.pagos_provisionales

    out = {
        "ejercicio": args.ejercicio,
        "fundamento": "LISR Art. 152 — Declaración anual de personas físicas",
        "ingresos": {
            "sueldos_y_salarios": util_sueldos,
            "honorarios_neto_gastos": round(util_honorarios, 2),
            "arrendamiento_neto": round(util_arrend, 2),
            "intereses": util_intereses,
            "otros": args.otros_ingresos,
            "TOTAL_ACUMULABLE": ingresos_acumulables,
        },
        "deducciones_personales": dp,
        "base_gravable": round(base_gravable, 2),
        "isr_causado_segun_tarifa": isr_causado,
        "acreditamientos": {
            "retenciones_sueldos": args.retenciones_sueldos,
            "retenciones_honorarios": args.retenciones_honorarios,
            "retenciones_intereses": args.retenciones_intereses,
            "pagos_provisionales": args.pagos_provisionales,
            "TOTAL": round(total_retenciones + args.pagos_provisionales, 2),
        },
        "RESULTADO": {
            "diferencia": round(diferencia, 2),
            "veredicto": "ISR_A_PAGAR" if diferencia > 0 else "SALDO_A_FAVOR" if diferencia < 0 else "CERO",
            "monto_a_pagar": round(max(0, diferencia), 2),
            "saldo_a_favor": round(abs(diferencia), 2) if diferencia < 0 else 0,
        },
        "fecha_limite_presentacion": (
            "30 de abril de 2026" if args.ejercicio == 2025
            else "30 de abril de 2027"
        ),
        "notas": [
            "Declaración anual es OBLIGATORIA si: ingresos > $400K, dos o más patrones, ingresos por honorarios/arrendamiento/intereses/dividendos/extranjero, te lo indica el SAT.",
            "Saldo a favor: pídelo en automático marcando opción de devolución en la declaración. SAT abona a CLABE en 5-30 días naturales.",
            "Validar deducciones contra CFDI emitido a tu nombre con tu RFC, no recibos genéricos.",
        ]
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
