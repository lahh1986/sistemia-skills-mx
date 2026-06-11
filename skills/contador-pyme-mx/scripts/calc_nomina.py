#!/usr/bin/env python3
"""
contador-pyme-mx · calc_nomina.py

Calcula nómina completa para 1 trabajador:
  - ISR a retener (Art. 96 LISR + Anexo 8 RMF 2026)
  - Subsidio para el empleo (Decreto DOF 31-12-2025)
  - Cuotas obrero-patronales IMSS (8 seguros LSS arts 25, 71, 106, 107, 147, 168, 211)
  - Aportación INFONAVIT 5%
  - ISN estatal
  - Neto del trabajador
  - Costo total del patrón

Uso:
  calc_nomina.py --salario-diario 500 --periodo mensual --estado "Michoacán" --clase-rt III
  calc_nomina.py --salario-mensual 15000 --periodo mensual --estado "Ciudad de México"
  calc_nomina.py --salario-diario 315.04 --periodo semanal --estado "Jalisco" --dias-trabajados 7
  echo '{"salario_diario":500,"periodo":"mensual",...}' | calc_nomina.py --stdin

Devuelve JSON con percepciones, deducciones, neto y costo patrón.
"""
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
TARIFAS = json.load(open(BASE / "data" / "tarifas_isr_2026.json"))
SUBSIDIO = json.load(open(BASE / "data" / "subsidio_empleo_2026.json"))
CUOTAS = json.load(open(BASE / "data" / "cuotas_imss_2026.json"))
VALORES = json.load(open(BASE / "data" / "valores_vigentes_2026.json"))

# ISN por estado — leer desde legal-pyme-mx
ISN_PATH = BASE.parent / "legal-pyme-mx" / "data" / "isn_por_estado.json"
ISN_POR_ESTADO = json.load(open(ISN_PATH))["estados"] if ISN_PATH.exists() else {}

DIAS_POR_PERIODO = {"diaria": 1, "semanal": 7, "decenal": 10, "quincenal": 15, "mensual": 30.4}


def calc_isr(base_gravable, periodo):
    """Aplica tarifa Art. 96 LISR según periodo."""
    if periodo not in TARIFAS["tarifas_retencion_periodicas"]:
        raise ValueError(f"Periodo '{periodo}' no soportado")
    tarifa = TARIFAS["tarifas_retencion_periodicas"][periodo]["rangos"]
    for rango in tarifa:
        if base_gravable >= rango["li"] and (rango["ls"] is None or base_gravable <= rango["ls"]):
            excedente = base_gravable - rango["li"]
            isr = rango["cf"] + (excedente * rango["pct"] / 100)
            return round(isr, 2)
    return 0.00


def calc_subsidio_empleo(base_gravable_mensual, periodo, es_enero=False):
    """Calcula subsidio del periodo. Si base > tope, no aplica."""
    if base_gravable_mensual > SUBSIDIO["tope_ingreso_mensual_gravable"]:
        return 0.00
    monto_mensual = (SUBSIDIO["monto_2026"]["enero_transicion"]["monto_mxn"] if es_enero
                     else SUBSIDIO["monto_2026"]["feb_a_dic"]["monto_mxn"])
    if periodo == "mensual":
        return round(monto_mensual, 2)
    dias = DIAS_POR_PERIODO[periodo]
    return round(monto_mensual * dias / 30.4, 2)


def calc_imss(sbc_diario, dias_periodo):
    """Calcula cuotas IMSS por seguro. Devuelve dict con patrón y obrero."""
    uma_d = VALORES["uma_2026"]["diaria_mxn"]
    tope_sbc = VALORES["uma_2026"]["diaria_mxn"] * 25
    sbc_diario = min(sbc_diario, tope_sbc)

    detalle = {}
    total_patron = 0.0
    total_obrero = 0.0

    # 1. EyM cuota fija (LSS 106-I): patrón 20.40% × UMA diaria × días
    base = uma_d * dias_periodo
    pat = base * 0.2040
    detalle["eym_cuota_fija"] = {"patron": round(pat, 2), "obrero": 0.00, "base": round(base, 2)}
    total_patron += pat

    # 2. EyM excedente (LSS 106-II): solo si SBC > 3 UMA
    if sbc_diario > 3 * uma_d:
        exc = (sbc_diario - 3 * uma_d) * dias_periodo
        pat = exc * 0.0110
        obr = exc * 0.0040
        detalle["eym_excedente"] = {"patron": round(pat, 2), "obrero": round(obr, 2), "base": round(exc, 2)}
        total_patron += pat
        total_obrero += obr
    else:
        detalle["eym_excedente"] = {"patron": 0.00, "obrero": 0.00, "nota": "SBC ≤ 3 UMA, no aplica"}

    # 3. EyM prestaciones en dinero (LSS 107): patrón 0.70%, obrero 0.25% sobre SBC
    base = sbc_diario * dias_periodo
    pat = base * 0.0070
    obr = base * 0.0025
    detalle["eym_prestaciones_dinero"] = {"patron": round(pat, 2), "obrero": round(obr, 2), "base": round(base, 2)}
    total_patron += pat
    total_obrero += obr

    # 4. EyM gastos médicos pensionados (LSS 25): patrón 1.05%, obrero 0.375%
    pat = base * 0.0105
    obr = base * 0.00375
    detalle["eym_gastos_pensionados"] = {"patron": round(pat, 2), "obrero": round(obr, 2)}
    total_patron += pat
    total_obrero += obr

    # 5. Invalidez y Vida (LSS 147): patrón 1.75%, obrero 0.625%
    pat = base * 0.0175
    obr = base * 0.00625
    detalle["invalidez_vida"] = {"patron": round(pat, 2), "obrero": round(obr, 2)}
    total_patron += pat
    total_obrero += obr

    # 6. Guarderías y Prestaciones Sociales (LSS 211): patrón 1.00%, obrero 0%
    pat = base * 0.0100
    detalle["guarderias_ps"] = {"patron": round(pat, 2), "obrero": 0.00}
    total_patron += pat

    # 7. Retiro (LSS 168-I): patrón 2.00% — bimestral pero se prorratea mensual
    pat = base * 0.0200
    detalle["retiro"] = {"patron": round(pat, 2), "obrero": 0.00, "nota": "bimestral, aquí prorrateado"}
    total_patron += pat

    # 8. CEAV (LSS 168-II): patrón según rango SBC en UMAs, obrero 1.125%
    sbc_en_umas = sbc_diario / uma_d
    pat_pct = 6.361  # default para SBC ≥ 4 UMA
    for r in CUOTAS["seguros"]["cesantia_vejez_2026"]["tabla_cuota_patronal_por_rango_sbc_uma"]:
        if r["sbc_uma_min"] <= sbc_en_umas and (r["sbc_uma_max"] is None or sbc_en_umas < r["sbc_uma_max"]):
            pat_pct = r["patron_pct"]
            break
    pat = base * pat_pct / 100
    obr = base * 0.01125
    detalle["cesantia_vejez"] = {
        "patron": round(pat, 2), "obrero": round(obr, 2),
        "patron_pct_aplicado": pat_pct, "sbc_en_umas": round(sbc_en_umas, 3),
        "nota": "bimestral, aquí prorrateado"
    }
    total_patron += pat
    total_obrero += obr

    detalle["TOTAL"] = {
        "patron": round(total_patron, 2),
        "obrero": round(total_obrero, 2)
    }
    return detalle


def calc_rt(sbc_diario, dias_periodo, clase_rt, prima_custom=None):
    """Cuota Riesgos de Trabajo (LSS 71). Si no se pasa prima, usa prima media de la clase."""
    if prima_custom is not None:
        prima = float(prima_custom) / 100
    else:
        clase_info = CUOTAS["seguros"]["riesgos_de_trabajo"]["clases_de_riesgo"].get(clase_rt.upper())
        if not clase_info:
            return {"patron": 0.0, "error": f"Clase RT '{clase_rt}' inválida (debe ser I-V)"}
        prima = clase_info["prima_media_pct"] / 100
    base = sbc_diario * dias_periodo
    return {
        "patron": round(base * prima, 2),
        "obrero": 0.00,
        "base": round(base, 2),
        "prima_pct_aplicada": round(prima * 100, 5),
        "clase_rt": clase_rt
    }


def calc_infonavit(sbc_diario, dias_periodo):
    """Aportación patronal INFONAVIT 5% (bimestral, prorrateado)."""
    tope_sbc = VALORES["uma_2026"]["diaria_mxn"] * 25
    sbc_diario = min(sbc_diario, tope_sbc)
    base = sbc_diario * dias_periodo
    return {
        "patron": round(base * 0.05, 2),
        "obrero": 0.00,
        "base": round(base, 2),
        "nota": "bimestral, aquí prorrateado mensual"
    }


def calc_isn(salario_periodo, estado):
    """Impuesto Sobre Nómina estatal."""
    if not ISN_POR_ESTADO:
        return {"isn": 0.0, "error": "JSON ISN no disponible"}
    estado_info = ISN_POR_ESTADO.get(estado)
    if not estado_info:
        return {"isn": 0.0, "error": f"Estado '{estado}' no encontrado en tabla ISN"}
    tasa = estado_info["tasa_pct"] / 100
    return {
        "isn": round(salario_periodo * tasa, 2),
        "tasa_pct": estado_info["tasa_pct"],
        "estado": estado,
        "fundamento": estado_info.get("notas", "")
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salario-diario", type=float, help="Salario diario integrado (SBC)")
    ap.add_argument("--salario-mensual", type=float, help="Salario mensual (calcula diario)")
    ap.add_argument("--periodo", choices=["diaria", "semanal", "decenal", "quincenal", "mensual"], default="mensual")
    ap.add_argument("--dias-trabajados", type=float, help="Días trabajados en el periodo (default: días del periodo)")
    ap.add_argument("--estado", required=True, help="Estado (para ISN). Ej: 'Michoacán', 'Ciudad de México', 'Jalisco'")
    ap.add_argument("--clase-rt", default="III", help="Clase Riesgo Trabajo I-V (default III)")
    ap.add_argument("--prima-rt", type=float, help="Prima RT específica determinada en DPRT febrero (override clase)")
    ap.add_argument("--es-enero", action="store_true", help="Cálculo de enero 2026 (subsidio usa UMA 2025)")
    ap.add_argument("--json", help="Inputs en JSON")
    ap.add_argument("--stdin", action="store_true")
    args = ap.parse_args()

    if args.stdin:
        d = json.load(sys.stdin)
    elif args.json:
        d = json.loads(args.json)
    else:
        if args.salario_diario:
            sbc = args.salario_diario
        elif args.salario_mensual:
            sbc = args.salario_mensual / 30.4
        else:
            ap.error("--salario-diario o --salario-mensual requerido")
        d = {
            "salario_diario": sbc,
            "periodo": args.periodo,
            "estado": args.estado,
            "clase_rt": args.clase_rt,
            "prima_rt": args.prima_rt,
            "dias_trabajados": args.dias_trabajados,
            "es_enero": args.es_enero,
        }

    sbc = d["salario_diario"]
    periodo = d["periodo"]
    dias = d.get("dias_trabajados") or DIAS_POR_PERIODO[periodo]
    estado = d["estado"]

    # Salario del periodo (lo que el trabajador gana en el periodo)
    salario_periodo = sbc * dias

    # ISR — base gravable simplificada = salario del periodo
    isr = calc_isr(salario_periodo, periodo)

    # Subsidio
    subsidio = calc_subsidio_empleo(sbc * 30.4, periodo, d.get("es_enero", False))

    # ISR neto a retener (resta subsidio; nunca negativo a favor del trabajador en este nivel)
    isr_neto = max(0, isr - subsidio)
    subsidio_pagado = min(subsidio, isr) if subsidio > 0 else 0
    subsidio_a_entregar_efectivo = max(0, subsidio - isr)  # patrón acredita después

    # IMSS
    imss = calc_imss(sbc, dias)
    rt = calc_rt(sbc, dias, d.get("clase_rt", "III"), d.get("prima_rt"))
    infonavit = calc_infonavit(sbc, dias)
    isn = calc_isn(salario_periodo, estado)

    # Sumarios
    deducciones_obrero = round(isr_neto + imss["TOTAL"]["obrero"], 2)
    neto_trabajador = round(salario_periodo - deducciones_obrero + subsidio_a_entregar_efectivo, 2)

    costo_patron = round(
        salario_periodo
        + imss["TOTAL"]["patron"]
        + rt["patron"]
        + infonavit["patron"]
        + isn["isn"],
        2
    )

    out = {
        "input": {
            "sbc_diario": sbc,
            "periodo": periodo,
            "dias": dias,
            "estado": estado,
            "es_enero": d.get("es_enero", False),
        },
        "percepciones": {
            "salario_periodo": round(salario_periodo, 2),
        },
        "isr": {
            "isr_calculado_tarifa": isr,
            "subsidio_empleo": subsidio,
            "subsidio_aplicado_contra_isr": round(subsidio_pagado, 2),
            "subsidio_entregado_efectivo_al_trabajador": round(subsidio_a_entregar_efectivo, 2),
            "isr_neto_a_retener": isr_neto,
        },
        "deducciones_obrero": {
            "isr_neto": isr_neto,
            "imss_obrero": imss["TOTAL"]["obrero"],
            "total": deducciones_obrero,
            "desglose_imss_obrero": {k: v["obrero"] for k, v in imss.items() if k != "TOTAL"}
        },
        "cuotas_patron": {
            "imss_total": imss["TOTAL"]["patron"],
            "riesgos_trabajo": rt["patron"],
            "infonavit": infonavit["patron"],
            "isn_estatal": isn["isn"],
            "total": round(imss["TOTAL"]["patron"] + rt["patron"] + infonavit["patron"] + isn["isn"], 2),
            "desglose_imss_patron": {k: v["patron"] for k, v in imss.items() if k != "TOTAL"},
            "rt_detalle": rt,
            "isn_detalle": isn,
        },
        "RESUMEN": {
            "que_paga_trabajador_al_fisco": deducciones_obrero,
            "neto_trabajador": neto_trabajador,
            "costo_total_para_el_patron": costo_patron,
            "factor_costo_patron_vs_salario_bruto": round(costo_patron / salario_periodo, 4),
        }
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
