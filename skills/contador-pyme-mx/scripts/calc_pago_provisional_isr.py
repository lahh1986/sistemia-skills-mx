#!/usr/bin/env python3
"""
contador-pyme-mx · calc_pago_provisional_isr.py

Calcula el pago provisional mensual de ISR para los regímenes más comunes:

  --regimen=pm-general    LISR Art. 14: ingresos × coeficiente_utilidad × 30%
  --regimen=pf-act-emp    LISR Art. 106: utilidad fiscal acumulada × tarifa mes
  --regimen=resico-pf     LISR Art. 113-E: ingresos cobrados × tasa 1-2.5%
  --regimen=resico-pm     LISR Art. 207: utilidad fiscal flujo × 30%
  --regimen=arrendamiento LISR Art. 116: ingreso del mes × tarifa mensual (con deducción 35% opcional)

Uso ejemplos:
  # PM General — coeficiente 0.0825, ingresos acumulados mes 5 $1,500,000
  calc_pago_provisional_isr.py --regimen=pm-general \\
    --coeficiente-utilidad=0.0825 --ingresos-acumulados=1500000 \\
    --mes=5 --pagos-anteriores=22500 --retenciones-intereses=0

  # RESICO PF — ingresos cobrados del mes
  calc_pago_provisional_isr.py --regimen=resico-pf \\
    --ingresos-mes=45000 --retenciones-pm=562.50

  # PF actividad empresarial — utilidad acumulada
  calc_pago_provisional_isr.py --regimen=pf-act-emp \\
    --utilidad-acumulada=380000 --mes=5 --pagos-anteriores=15000
"""
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
TARIFAS = json.load(open(BASE / "data" / "tarifas_isr_2026.json"))
RESICO = json.load(open(BASE / "data" / "tarifas_resico_2026.json"))


def aplicar_tarifa(base_gravable, rangos):
    """Aplica tarifa estilo SAT (cuota fija + % excedente)."""
    if base_gravable <= 0:
        return 0.00
    for r in rangos:
        if base_gravable >= r["li"] and (r["ls"] is None or base_gravable <= r["ls"]):
            excedente = base_gravable - r["li"]
            return round(r["cf"] + excedente * r["pct"] / 100, 2)
    return 0.00


def pm_general(args):
    """LISR Art. 14: utilidad estimada × tasa 30% - pagos anteriores - retenciones."""
    coef = args.coeficiente_utilidad
    ing_acum = args.ingresos_acumulados
    utilidad_estimada = ing_acum * coef
    isr_acumulado = utilidad_estimada * 0.30
    pago_provisional = isr_acumulado - (args.pagos_anteriores or 0) - (args.retenciones_intereses or 0)
    return {
        "regimen": "PM Régimen General — LISR Art. 14",
        "ingresos_nominales_acumulados": ing_acum,
        "coeficiente_utilidad": coef,
        "utilidad_fiscal_estimada": round(utilidad_estimada, 2),
        "tasa_pct": 30.00,
        "isr_acumulado_del_ejercicio": round(isr_acumulado, 2),
        "menos_pagos_provisionales_anteriores": args.pagos_anteriores or 0,
        "menos_retenciones_intereses": args.retenciones_intereses or 0,
        "ISR_DEL_MES_A_PAGAR": round(max(0, pago_provisional), 2),
        "es_a_favor": pago_provisional < 0,
        "saldo_a_favor": round(abs(pago_provisional), 2) if pago_provisional < 0 else 0,
        "fundamento": "LISR Art. 14. Pago provisional mensual = (ingresos nominales acumulados × coef. utilidad del ejercicio anterior) × 30% - pagos provisionales del propio ejercicio - retenciones."
    }


def pf_act_emp(args):
    """LISR Art. 106: utilidad fiscal acumulada × tarifa acumulada del mes."""
    util_acum = args.utilidad_acumulada
    rangos = TARIFAS["tarifa_anual_pf_2026"]["rangos"]
    # Para mes acumulado proporcional: dividir anual entre 12 × meses, pero LISR aplica tarifa anual sobre acumulado
    isr_acumulado = aplicar_tarifa(util_acum, rangos)
    # Si quisieras proporcionar mensual exacto usar tarifas del Apartado B.VI (no las tengo en JSON aún)
    # Aquí simplificamos: aplicar tarifa anual sobre acumulado y restar pagos anteriores
    pago = isr_acumulado - (args.pagos_anteriores or 0) - (args.retenciones_anteriores or 0)
    return {
        "regimen": "PF con Actividad Empresarial y Profesional — LISR Art. 106",
        "utilidad_fiscal_acumulada": util_acum,
        "isr_acumulado_segun_tarifa": isr_acumulado,
        "menos_pagos_provisionales_anteriores": args.pagos_anteriores or 0,
        "menos_retenciones_anteriores_acumuladas": args.retenciones_anteriores or 0,
        "ISR_DEL_MES_A_PAGAR": round(max(0, pago), 2),
        "saldo_a_favor": round(abs(pago), 2) if pago < 0 else 0,
        "fundamento": "LISR Art. 106. Se aplica la tarifa del ejercicio sobre la utilidad fiscal acumulada del periodo y se restan los pagos provisionales anteriores.",
        "advertencia": "Para mayor precisión usar las tarifas mensuales acumuladas del Apartado B.VI del Anexo 8 RMF (ene, feb, mar...). Esta función usa la tarifa anual sobre acumulado — exacto para mes 12 (dic) pero requiere ajuste para meses anteriores. Verificar con contador."
    }


def resico_pf(args):
    """LISR Art. 113-E: ingresos del mes × tasa según rango."""
    ing = args.ingresos_mes
    if ing > 3500000 / 12:
        return {"error": "Ingresos mensuales superan tope mensual proporcional. Verifica ingresos acumulados; tope anual es $3.5M."}
    tabla = RESICO["resico_pf"]["tabla_tasas_mensuales"]
    tasa = None
    for r in tabla:
        if ing >= r["li"] and (r["ls"] is None or ing <= r["ls"]):
            tasa = r["tasa_pct"]
            break
    if tasa is None:
        tasa = tabla[-1]["tasa_pct"]
    isr = ing * tasa / 100
    pago = isr - (args.retenciones_pm or 0)
    return {
        "regimen": "RESICO Personas Físicas — LISR Art. 113-E",
        "ingresos_efectivamente_cobrados_mes": ing,
        "tasa_aplicada_pct": tasa,
        "isr_del_mes": round(isr, 2),
        "menos_retenciones_pm_1_25": args.retenciones_pm or 0,
        "ISR_DEL_MES_A_PAGAR": round(max(0, pago), 2),
        "saldo_a_favor": round(abs(pago), 2) if pago < 0 else 0,
        "fundamento": "LISR Art. 113-E. Pago mensual definitivo sin deducciones. Retenciones del 1.25% por PM son acreditables.",
        "nota_resico_pf": "RESICO PF tiene pago mensual DEFINITIVO (no provisional). No acumula al anual — el resultado del mes es el final."
    }


def resico_pm(args):
    """LISR Art. 207: utilidad fiscal × 30% (base flujo de efectivo)."""
    util = args.utilidad_acumulada
    isr_acum = util * 0.30
    pago = isr_acum - (args.pagos_anteriores or 0)
    return {
        "regimen": "RESICO Personas Morales — LISR Art. 207",
        "utilidad_fiscal_acumulada_flujo": util,
        "tasa_pct": 30.00,
        "isr_acumulado_ejercicio": round(isr_acum, 2),
        "menos_pagos_anteriores": args.pagos_anteriores or 0,
        "ISR_DEL_MES_A_PAGAR": round(max(0, pago), 2),
        "fundamento": "LISR Art. 207. Misma tasa que PM General pero base flujo de efectivo."
    }


def arrendamiento(args):
    """LISR Art. 116: ingreso del mes con opción deducción 35% ciega."""
    ing = args.ingresos_mes
    if args.usar_deduccion_ciega:
        # Art. 115 LISR: deducción opcional 35% del ingreso sin comprobantes
        deduccion = ing * 0.35
        # Más impuesto predial (asumido cero por simplicidad o usar arg)
        base_gravable = ing - deduccion - (args.predial or 0)
    else:
        # Deducciones reales (servicios, mantenimiento, comprobables)
        base_gravable = ing - (args.deducciones_comprobables or 0)
    # Aplica tarifa mensual ISR
    isr = aplicar_tarifa(base_gravable, TARIFAS["tarifas_retencion_periodicas"]["mensual"]["rangos"])
    pago = isr - (args.retenciones_anteriores or 0)
    return {
        "regimen": "Arrendamiento PF — LISR Art. 116",
        "ingresos_del_mes": ing,
        "opcion_deduccion": "ciega 35%" if args.usar_deduccion_ciega else "deducciones comprobables",
        "deduccion": round(ing * 0.35 if args.usar_deduccion_ciega else (args.deducciones_comprobables or 0), 2),
        "base_gravable": round(base_gravable, 2),
        "isr_calculado": isr,
        "menos_retenciones_pm": args.retenciones_anteriores or 0,
        "ISR_DEL_MES_A_PAGAR": round(max(0, pago), 2),
        "fundamento": "LISR Art. 116 + Art. 115 (deducción opcional 35%)"
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regimen", choices=["pm-general", "pf-act-emp", "resico-pf", "resico-pm", "arrendamiento"], required=True)
    # PM
    ap.add_argument("--coeficiente-utilidad", type=float, help="Coef. utilidad del ejercicio anterior (PM)")
    ap.add_argument("--ingresos-acumulados", type=float, help="Ingresos nominales acumulados del ejercicio (PM)")
    ap.add_argument("--mes", type=int, help="Mes que se declara (1-12)")
    ap.add_argument("--pagos-anteriores", type=float, help="Pagos provisionales anteriores del mismo ejercicio")
    ap.add_argument("--retenciones-intereses", type=float, help="Retenciones por intereses (PM)")
    # PF
    ap.add_argument("--utilidad-acumulada", type=float, help="Utilidad fiscal acumulada (PF act. emp. o RESICO PM)")
    ap.add_argument("--retenciones-anteriores", type=float, help="Retenciones acumuladas (PF / arrendamiento)")
    # RESICO PF
    ap.add_argument("--ingresos-mes", type=float, help="Ingresos efectivamente cobrados del mes (RESICO PF o arrendamiento)")
    ap.add_argument("--retenciones-pm", type=float, help="Retenciones 1.25% recibidas de PM (RESICO PF)")
    # Arrendamiento
    ap.add_argument("--usar-deduccion-ciega", action="store_true", help="Aplicar deduccion opcional 35 pct")
    ap.add_argument("--deducciones-comprobables", type=float, help="Deducciones comprobables (arrendamiento)")
    ap.add_argument("--predial", type=float, help="Predial pagado (arrendamiento)")
    args = ap.parse_args()

    funcs = {
        "pm-general": pm_general,
        "pf-act-emp": pf_act_emp,
        "resico-pf": resico_pf,
        "resico-pm": resico_pm,
        "arrendamiento": arrendamiento,
    }
    print(json.dumps(funcs[args.regimen](args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
