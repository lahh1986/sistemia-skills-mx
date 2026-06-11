#!/usr/bin/env python3
"""
contador-pyme-mx · calc_finiquito.py

Calcula finiquito o liquidación de un trabajador según LFT:
  - Aguinaldo proporcional (Art. 87 LFT)
  - Vacaciones proporcionales + prima vacacional (Arts. 76-81, reforma 2023 "vacaciones dignas")
  - Salarios pendientes
  - PTU proporcional (Arts. 117-131)
  - Indemnización (Arts. 48-50) — si despido injustificado
  - Prima de antigüedad (Art. 162) — si ≥15 años o aplica

Uso:
  calc_finiquito.py --salario-diario 500 --fecha-alta 2022-01-15 --fecha-baja 2026-05-30 --tipo renuncia
  calc_finiquito.py --salario-diario 800 --fecha-alta 2020-03-01 --fecha-baja 2026-05-30 --tipo despido-injustificado --motivo "rescision sin causa"
  calc_finiquito.py --json '{"salario_diario":500,...}'
"""
import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
VALORES = json.load(open(BASE / "data" / "valores_vigentes_2026.json"))

# Días por año de antigüedad según LFT reformada 2023 ("vacaciones dignas")
# (top_aniversarios_cumplidos, dias_vacaciones_anuales)
# Año 1=12, 2=14, 3=16, 4=18, 5=20, 6=22, ..., +2 cada año hasta 32 (año 12+)
TABLA_VACACIONES_LFT = [
    (1, 12),
    (2, 14),
    (3, 16),
    (4, 18),
    (5, 20),
    (6, 22),   # corrigió tabla: 6° aniversario = 22 (no 22 hasta 10°)
    (7, 24),   # 7°-12° = +2 progresivo (no 24 fijo)
    (8, 26),
    (9, 28),
    (10, 30),
    (11, 32),
    # Después de 11+ años queda en 32 días
]


def años_aniversarios_cumplidos(fecha_alta, fecha_baja):
    """Cuenta aniversarios completos entre 2 fechas (interpretación correcta LFT).
    Ejemplo: 2020-05-31 → 2026-05-31 = 6 aniversarios."""
    años = fecha_baja.year - fecha_alta.year
    if (fecha_baja.month, fecha_baja.day) < (fecha_alta.month, fecha_alta.day):
        años -= 1
    return max(0, años)


def dias_vacaciones_por_antiguedad(años_aniversarios):
    """Devuelve días de vacaciones anuales según LFT Art. 76 (reforma 2023).
    Recibe años de aniversarios CUMPLIDOS (no fracción)."""
    if años_aniversarios < 1:
        return 0  # menos de 1 año no da vacaciones aún
    for top, dias in TABLA_VACACIONES_LFT:
        if años_aniversarios <= top:
            return dias
    return TABLA_VACACIONES_LFT[-1][1]  # 32 días para 12+ años


def calc_finiquito(d):
    # Cuota diaria (lo que recibe el trabajador) vs Salario integrado (SBC con prima vac y aguinaldo).
    # LFT Art. 84 + 89: indemnizaciones se calculan con SALARIO INTEGRADO, no cuota diaria.
    cuota_diaria = float(d["salario_diario"])
    sbc = d.get("salario_integrado")
    if sbc is None:
        # Si no se proporciona, lo calculamos: cuota + prima aguinaldo + prima vacacional
        dias_agui = float(d.get("dias_aguinaldo_anual", 15))
        # Para el factor de integración necesitamos saber años pero antes los calculamos abajo.
        # Aproximación conservadora: usar 12 días vacaciones (año 1) si no sabemos antigüedad.
        # El llamador puede pasar salario_integrado explícito para precisión.
        factor_agui = dias_agui / 365  # ej. 15/365 = 0.0411
        factor_prima_vac = 12 * 0.25 / 365  # mín año 1: 12 días × 25% / 365 = 0.00822
        factor_integracion = 1 + factor_agui + factor_prima_vac  # ej 1.0493
        sbc = round(cuota_diaria * factor_integracion, 2)
        sbc_calculado_auto = True
    else:
        sbc = float(sbc)
        sbc_calculado_auto = False

    f_alta = datetime.fromisoformat(d["fecha_alta"]).date()
    f_baja = datetime.fromisoformat(d["fecha_baja"]).date()
    tipo = d.get("tipo", "renuncia")  # renuncia | despido-injustificado | termino-contrato | mutuo-consentimiento
    años_servicio_aniv = años_aniversarios_cumplidos(f_alta, f_baja)
    años_servicio_decimal = (f_baja - f_alta).days / 365.25  # para prorrateos
    dias_servicio_total = (f_baja - f_alta).days

    # Días trabajados en el año en curso (para prorrateos)
    inicio_año = date(f_baja.year, 1, 1)
    if f_alta > inicio_año:
        inicio_año = f_alta
    dias_año_curso = (f_baja - inicio_año).days + 1

    breakdown = []

    # 1. Aguinaldo proporcional (Art. 87 LFT: mín 15 días/año)
    # Se calcula con cuota diaria (no SBC) según práctica común
    dias_aguinaldo_anual = float(d.get("dias_aguinaldo_anual", 15))
    aguinaldo_proporcional = cuota_diaria * dias_aguinaldo_anual * (dias_año_curso / 365.25)
    breakdown.append({
        "concepto": "Aguinaldo proporcional",
        "fundamento": "LFT Art. 87",
        "calculo": f"{cuota_diaria} × {dias_aguinaldo_anual} × ({dias_año_curso}/365.25 días año)",
        "monto": round(aguinaldo_proporcional, 2),
    })

    # 2. Vacaciones no disfrutadas del último año (LFT Art. 76)
    dias_vac_anual = dias_vacaciones_por_antiguedad(años_servicio_aniv)
    # Asume que tiene pendientes las del año en curso proporcional
    raw_vac = d.get("dias_vacaciones_pendientes")
    if raw_vac is None:
        dias_vac_no_disfrutadas = dias_vac_anual * (dias_año_curso / 365.25)
    else:
        dias_vac_no_disfrutadas = float(raw_vac)
    vacaciones = sbc * dias_vac_no_disfrutadas
    breakdown.append({
        "concepto": "Vacaciones pendientes",
        "fundamento": "LFT Art. 76 (reforma 2023 'vacaciones dignas')",
        "calculo": f"{sbc} × {round(dias_vac_no_disfrutadas, 2)} días",
        "monto": round(vacaciones, 2),
        "nota_vacaciones_anuales_segun_antiguedad": f"{dias_vac_anual} días/año (con {años_servicio_aniv} aniversarios cumplidos)"
    })

    # 3. Prima vacacional (Art. 80: 25% mín del salario de los días de vacaciones)
    prima_vac_pct = float(d.get("prima_vacacional_pct", 25)) / 100
    prima_vacacional = vacaciones * prima_vac_pct
    breakdown.append({
        "concepto": "Prima vacacional",
        "fundamento": "LFT Art. 80 (25% mínimo)",
        "calculo": f"{round(vacaciones,2)} × {prima_vac_pct*100:.0f}%",
        "monto": round(prima_vacacional, 2),
    })

    # 4. Salarios pendientes (días trabajados no pagados del periodo en curso)
    dias_pendientes = float(d.get("dias_salario_pendiente", 0))
    salario_pendiente = sbc * dias_pendientes
    if salario_pendiente > 0:
        breakdown.append({
            "concepto": "Salario pendiente",
            "fundamento": "LFT Art. 84",
            "calculo": f"{sbc} × {dias_pendientes} días no pagados",
            "monto": round(salario_pendiente, 2),
        })

    # 5. PTU proporcional (si el patrón generó utilidades — se asume conocido por contador)
    # Default: NO incluir salvo que se especifique
    if d.get("ptu_anual_estimado"):
        ptu = float(d["ptu_anual_estimado"]) * (dias_año_curso / 365.25)
        breakdown.append({
            "concepto": "PTU proporcional",
            "fundamento": "LFT Arts. 117-131",
            "calculo": f"{d['ptu_anual_estimado']} × {dias_año_curso}/365.25",
            "monto": round(ptu, 2),
        })

    subtotal_finiquito = sum(b["monto"] for b in breakdown)

    # 6. Indemnización (solo despido injustificado o rescisión sin causa)
    indemnizacion_breakdown = []
    if tipo == "despido-injustificado":
        # Art. 48: 3 meses de salario
        ind_3_meses = sbc * 90
        indemnizacion_breakdown.append({
            "concepto": "Indemnización constitucional (3 meses)",
            "fundamento": "LFT Art. 48 + Constitución Art. 123",
            "calculo": f"{sbc} × 90 días",
            "monto": round(ind_3_meses, 2),
        })
        # Art. 50: 20 días por año (si optó por indemnización en vez de reinstalación)
        ind_20_por_año = sbc * 20 * años_servicio_decimal
        indemnizacion_breakdown.append({
            "concepto": "Indemnización 20 días por año (opción reinstalación)",
            "fundamento": "LFT Art. 50",
            "calculo": f"{sbc} × 20 × {round(años_servicio_decimal,2)} años",
            "monto": round(ind_20_por_año, 2),
            "nota": "Solo aplica si trabajador optó por indemnización en lugar de reinstalación"
        })
        # Salarios caídos limitados a 12 meses (reforma 2012)
        # No los calculo automático porque dependen del proceso laboral

    # 7. Prima de antigüedad (Art. 162: 12 días por año, tope SBC = 2 SMG)
    # Aplica: al término por jubilación, retiro voluntario con ≥15 años, despido justificado o muerte
    prima_antiguedad = 0
    aplica_prima_antig = False
    if tipo == "despido-injustificado":
        aplica_prima_antig = True
    elif tipo == "renuncia" and años_servicio_decimal >= 15:
        aplica_prima_antig = True
    elif tipo in ("jubilacion", "muerte", "incapacidad-permanente"):
        aplica_prima_antig = True

    if aplica_prima_antig:
        # Tope: SBC máximo = 2 × salario mínimo de la zona
        raw_sm = d.get("salario_minimo_zona")
        sm_zona = float(raw_sm) if raw_sm is not None else VALORES["salario_minimo_2026"]["zona_general_diario_mxn"]
        tope_sbc_prima = 2 * sm_zona
        sbc_topado = min(sbc, tope_sbc_prima)
        prima_antiguedad = sbc_topado * 12 * años_servicio_decimal
        indemnizacion_breakdown.append({
            "concepto": "Prima de antigüedad",
            "fundamento": "LFT Art. 162",
            "calculo": f"min({sbc}, 2×{sm_zona}={tope_sbc_prima}) × 12 días × {round(años_servicio_decimal,2)} años",
            "monto": round(prima_antiguedad, 2),
            "nota_tope": f"SBC topado a 2× SM zona = ${tope_sbc_prima:.2f}",
        })

    subtotal_indemnizacion = sum(b["monto"] for b in indemnizacion_breakdown)
    total = subtotal_finiquito + subtotal_indemnizacion

    uma_2026 = VALORES["uma_2026"]["diaria_mxn"]
    out = {
        "input": {
            "cuota_diaria": cuota_diaria,
            "salario_integrado_sbc": sbc,
            "sbc_calculado_auto": sbc_calculado_auto,
            "fecha_alta": d["fecha_alta"],
            "fecha_baja": d["fecha_baja"],
            "tipo_termino": tipo,
            "años_servicio_aniversarios": años_servicio_aniv,
            "años_servicio_decimal": round(años_servicio_decimal, 2),
            "dias_año_curso": dias_año_curso,
        },
        "finiquito": {
            "conceptos": breakdown,
            "subtotal": round(subtotal_finiquito, 2),
        },
        "indemnizacion": {
            "aplica": len(indemnizacion_breakdown) > 0,
            "conceptos": indemnizacion_breakdown,
            "subtotal": round(subtotal_indemnizacion, 2),
        },
        "TOTAL": round(total, 2),
        "notas": [
            "Cálculo orientativo basado en LFT vigente con reforma 2023 ('vacaciones dignas').",
            "INDEMNIZACIONES se calculan con SALARIO INTEGRADO (LFT Art. 84+89), no cuota diaria. " +
                ("SBC calculado automáticamente con factor de integración mínimo. Para precisión, pasa --salario-integrado." if sbc_calculado_auto else f"Usaste SBC explícito: ${sbc:.2f}."),
            "NO calcula salarios caídos (despido injustificado, máx 12 meses por reforma 2012).",
            f"ISR sobre indemnización: exentos LISR Art. 93 fr. XIII = 90 UMAs × años trabajados. UMA 2026 = ${uma_2026:.2f} diaria.",
            "Para casos contenciosos refiere a abogado laboral.",
        ]
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salario-diario", type=float, help="Cuota diaria del trabajador (sin prima aguinaldo/vac)")
    ap.add_argument("--salario-integrado", type=float, help="SBC (cuota + factor integración). Si no se pasa se calcula auto.")
    ap.add_argument("--fecha-alta")
    ap.add_argument("--fecha-baja")
    ap.add_argument("--tipo", choices=["renuncia", "despido-injustificado", "termino-contrato",
                                       "mutuo-consentimiento", "jubilacion", "muerte", "incapacidad-permanente"],
                    default="renuncia")
    ap.add_argument("--dias-aguinaldo-anual", type=float, default=15)
    ap.add_argument("--dias-vacaciones-pendientes", type=float)
    ap.add_argument("--prima-vacacional-pct", type=float, default=25)
    ap.add_argument("--dias-salario-pendiente", type=float, default=0)
    ap.add_argument("--ptu-anual-estimado", type=float)
    ap.add_argument("--salario-minimo-zona", type=float)
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.json:
        d = json.loads(args.json)
    else:
        if not all([args.salario_diario, args.fecha_alta, args.fecha_baja]):
            ap.error("--salario-diario, --fecha-alta y --fecha-baja requeridos")
        d = {
            "salario_diario": args.salario_diario,
            "salario_integrado": args.salario_integrado,
            "fecha_alta": args.fecha_alta,
            "fecha_baja": args.fecha_baja,
            "tipo": args.tipo,
            "dias_aguinaldo_anual": args.dias_aguinaldo_anual,
            "dias_vacaciones_pendientes": args.dias_vacaciones_pendientes,
            "prima_vacacional_pct": args.prima_vacacional_pct,
            "dias_salario_pendiente": args.dias_salario_pendiente,
            "ptu_anual_estimado": args.ptu_anual_estimado,
            "salario_minimo_zona": args.salario_minimo_zona,
        }

    print(json.dumps(calc_finiquito(d), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
