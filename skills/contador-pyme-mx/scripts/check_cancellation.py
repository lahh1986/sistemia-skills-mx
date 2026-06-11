#!/usr/bin/env python3
"""
contador-pyme-mx · check_cancellation.py

Valida que la cancelación de un CFDI cumpla las reglas SAT vigentes desde 2022:
  - Motivo 01-04 correcto
  - Si motivo=01 (error con relación), debe llevar folio sustituto
  - Alerta cancelaciones de ejercicio anterior
  - Alerta cancelaciones de nómina ya pagada

Uso:
  check_cancellation.py --uuid=<UUID> --motivo=01 --folio-sustituto=<UUID-nuevo> [--fecha-original=YYYY-MM-DD] [--tipo=I|E|N|P|T] [--total=MXN]
  check_cancellation.py --json '{"uuid":"...","motivo":"01",...}'
"""
import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
MOTIVOS = json.load(open(BASE / "data" / "motivos_cancelacion.json"))["motivos"]
REGLAS = json.load(open(BASE / "data" / "motivos_cancelacion.json"))["reglas_generales"]


def validar(req):
    hallazgos = []
    motivo = str(req.get("motivo", "")).zfill(2)

    if motivo not in MOTIVOS:
        return [{"sev": "🚨", "mensaje": f"Motivo '{motivo}' inválido. Debe ser 01, 02, 03 o 04."}]

    info = MOTIVOS[motivo]
    hallazgos.append({
        "sev": "ℹ️",
        "mensaje": f"Motivo {motivo}: {info['descripcion_corta']}"
    })

    # Regla 1: motivo 01 requiere FolioSustitucion
    if info["requiere_folio_sustituto"]:
        if not req.get("folio_sustituto"):
            hallazgos.append({
                "sev": "🚨",
                "mensaje": f"Motivo {motivo} ({info['descripcion_corta']}) REQUIERE FolioSustitucion. "
                           f"El PAC va a rechazar la cancelación. Debes haber emitido el CFDI corregido primero "
                           f"y poner aquí su UUID."
            })
        else:
            # validar UUID format
            uuid = req["folio_sustituto"]
            if len(uuid) != 36 or uuid.count("-") != 4:
                hallazgos.append({
                    "sev": "🚨",
                    "mensaje": f"FolioSustitucion '{uuid}' no tiene formato UUID válido (debe ser 36 chars con 4 guiones)."
                })

    # Regla 2: cancelación de ejercicio anterior
    if req.get("fecha_original"):
        try:
            f_orig = datetime.fromisoformat(req["fecha_original"]).date()
            hoy = date.today()
            if f_orig.year < hoy.year:
                if motivo in ("02", "03"):
                    hallazgos.append({
                        "sev": "⚠️",
                        "mensaje": f"CFDI de ejercicio anterior ({f_orig.year}) cancelado con motivo {motivo}. "
                                   f"Esto genera diferencia entre contabilidad y declaración anual ya presentada. "
                                   f"Riesgo de auditoría. Considera amparo o reclasificación contable."
                    })
                if motivo == "01" and not req.get("folio_sustituto"):
                    hallazgos.append({
                        "sev": "🚨",
                        "mensaje": "Sustituir CFDI de ejercicio anterior es complicado. Verifica que el CFDI sustituto "
                                   "también sea del ejercicio anterior o ajusta deducciones/ingresos."
                    })

            # Regla 3: cancelación libre solo hasta fin del mes
            if hoy.year == f_orig.year and hoy.month != f_orig.month:
                hallazgos.append({
                    "sev": "⚠️",
                    "mensaje": f"Han pasado más de un mes desde emisión ({f_orig.isoformat()}). "
                               f"La cancelación ya NO es libre — requiere aceptación expresa del receptor "
                               f"vía Buzón Tributario en 72 hrs (salvo excepciones: monto ≤$1,000, nómina, "
                               f"egreso, traslado, RFC genérico, enajenación bienes, prima vacacional)."
                })
        except Exception:
            pass

    # Regla 4: cancelación de nómina
    tipo = req.get("tipo")
    if tipo == "N":
        hallazgos.append({
            "sev": "⚠️",
            "mensaje": "Cancelar CFDI de nómina YA pagada al trabajador: el SAT asume la retención ISR fue "
                       "entregada al trabajador (no enterada al fisco). Genera diferencias en declaración "
                       "informativa y posibles requerimientos. Considera re-emitir como sustitución (motivo 01)."
        })

    # Regla 5: monto pequeño = cancelación libre
    if req.get("total"):
        try:
            t = float(req["total"])
            if t <= 1000:
                hallazgos.append({
                    "sev": "ℹ️",
                    "mensaje": f"Total ${t:.2f} ≤ $1,000: la cancelación NO requiere aceptación del receptor "
                               f"(excepción Regla 2.7.1.39 RMF)."
                })
        except Exception:
            pass

    return hallazgos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uuid", help="UUID del CFDI a cancelar")
    ap.add_argument("--motivo", choices=["01", "02", "03", "04"], help="Motivo de cancelación")
    ap.add_argument("--folio-sustituto", help="UUID del CFDI sustituto (requerido para motivo 01)")
    ap.add_argument("--fecha-original", help="Fecha de emisión original YYYY-MM-DD")
    ap.add_argument("--tipo", choices=["I", "E", "T", "N", "P"], help="Tipo de comprobante")
    ap.add_argument("--total", help="Monto total del CFDI")
    ap.add_argument("--json", help="Pasa todos los inputs como JSON")
    args = ap.parse_args()

    if args.json:
        req = json.loads(args.json)
    else:
        req = {
            "uuid": args.uuid,
            "motivo": args.motivo,
            "folio_sustituto": args.folio_sustituto,
            "fecha_original": args.fecha_original,
            "tipo": args.tipo,
            "total": args.total,
        }

    if not req.get("motivo"):
        ap.error("--motivo requerido")

    hallazgos = validar(req)
    severidades = [h["sev"] for h in hallazgos]
    if "🚨" in severidades:
        veredicto = "🚨 NO CANCELAR (corregir primero)"
    elif "⚠️" in severidades:
        veredicto = "⚠️ CANCELAR_CON_PRECAUCION"
    else:
        veredicto = "✅ OK_PARA_CANCELAR"

    out = {
        "veredicto": veredicto,
        "uuid": req.get("uuid"),
        "motivo": req.get("motivo"),
        "hallazgos": hallazgos,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
