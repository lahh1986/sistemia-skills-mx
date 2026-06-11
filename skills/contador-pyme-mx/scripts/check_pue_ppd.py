#!/usr/bin/env python3
"""
contador-pyme-mx · check_pue_ppd.py

Recorre un directorio de XMLs CFDI y alerta CFDIs de tipo Ingreso (I) con
MetodoPago=PUE timbrados en los últimos 5 días del mes. Si NO existe un
Complemento de Pagos posterior cobrando ese UUID, el SAT asume cobrado y
el contribuyente debe pagar ISR/IVA sobre ingreso fantasma.

Uso:
  check_pue_ppd.py --dir cfdis/
  check_pue_ppd.py --dir cfdis/ --mes 2026-05
  check_pue_ppd.py --dir cfdis/ --days-before-eom 5 --include-pagos
"""
import argparse
import json
from calendar import monthrange
from datetime import datetime, date
from pathlib import Path
import xml.etree.ElementTree as ET

NS_CFDI = "http://www.sat.gob.mx/cfd/4"
NS_TFD = "http://www.sat.gob.mx/TimbreFiscalDigital"
NS_PAGOS = "http://www.sat.gob.mx/Pagos20"


def parse_cfdi(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if not root.tag.endswith("Comprobante"):
            return None

        tfd = root.find(f".//{{{NS_TFD}}}TimbreFiscalDigital")
        uuid = tfd.get("UUID") if tfd is not None else None

        # ¿Es un complemento de pagos?
        pagos = root.find(f".//{{{NS_PAGOS}}}Pagos")
        pagos_uuids = []
        if pagos is not None:
            for doctorel in pagos.findall(f".//{{{NS_PAGOS}}}DoctoRelacionado"):
                doc_uuid = doctorel.get("IdDocumento")
                if doc_uuid:
                    pagos_uuids.append(doc_uuid)

        emisor = root.find(f"{{{NS_CFDI}}}Emisor")
        receptor = root.find(f"{{{NS_CFDI}}}Receptor")
        return {
            "path": str(path),
            "uuid": uuid,
            "tipo": root.get("TipoDeComprobante"),
            "metodo": root.get("MetodoPago"),
            "fecha": root.get("Fecha"),
            "total": root.get("Total"),
            "moneda": root.get("Moneda"),
            "emisor_rfc": emisor.get("Rfc") if emisor is not None else None,
            "receptor_rfc": receptor.get("Rfc") if receptor is not None else None,
            "es_complemento_pagos": pagos is not None,
            "uuids_relacionados_pagos": pagos_uuids,
        }
    except ET.ParseError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="Directorio con XMLs CFDI")
    ap.add_argument("--mes", help="Filtra por mes YYYY-MM (default: todos)")
    ap.add_argument("--days-before-eom", type=int, default=5, help="Días antes del fin de mes para alertar (default: 5)")
    ap.add_argument("--include-pagos", action="store_true", help="Incluir también CFDIs sin complemento de pagos posterior")
    args = ap.parse_args()

    root_dir = Path(args.dir)
    if not root_dir.exists():
        print(json.dumps({"error": f"directorio no existe: {root_dir}"}))
        return

    todos = []
    for p in root_dir.rglob("*.xml"):
        d = parse_cfdi(p)
        if d:
            todos.append(d)

    # filtrar por mes si aplica
    if args.mes:
        try:
            year, month = map(int, args.mes.split("-"))
        except Exception:
            print(json.dumps({"error": f"--mes formato YYYY-MM: {args.mes}"}))
            return
        todos = [d for d in todos if d["fecha"] and d["fecha"].startswith(args.mes)]

    # PUEs en últimos N días del mes
    sospechosos = []
    for d in todos:
        if d["tipo"] != "I" or d["metodo"] != "PUE" or not d["fecha"]:
            continue
        try:
            f = datetime.fromisoformat(d["fecha"].split("T")[0]).date()
        except Exception:
            continue
        ultimo = monthrange(f.year, f.month)[1]
        dias_para_eom = ultimo - f.day
        if dias_para_eom <= args.days_before_eom:
            d["dias_para_fin_mes"] = dias_para_eom
            sospechosos.append(d)

    # cruzar contra complementos de pagos
    pagos_uuids_pagados = set()
    for d in todos:
        if d["es_complemento_pagos"]:
            pagos_uuids_pagados.update(d["uuids_relacionados_pagos"])

    sin_pago = []
    con_pago = []
    for d in sospechosos:
        if d["uuid"] in pagos_uuids_pagados:
            con_pago.append(d)
        else:
            sin_pago.append(d)

    out = {
        "directorio": str(root_dir),
        "mes_filtro": args.mes,
        "total_cfdis_revisados": len(todos),
        "pues_fin_mes_total": len(sospechosos),
        "pues_fin_mes_SIN_PAGO": len(sin_pago),
        "pues_fin_mes_con_pago_posterior": len(con_pago),
        "alerta": (
            f"🚨 {len(sin_pago)} CFDIs PUE timbrados los últimos {args.days_before_eom} días del mes "
            f"NO tienen complemento de pagos posterior. El SAT puede asumirlos cobrados y exigir "
            f"ISR/IVA sobre ingreso fantasma. Acción: confirmar cobro real o cancelar/re-emitir como PPD."
        ) if sin_pago else "✅ Ningún CFDI PUE de fin de mes sin pago posterior",
        "cfdis_sin_pago": [
            {
                "uuid": d["uuid"],
                "fecha": d["fecha"],
                "dias_para_fin_mes": d["dias_para_fin_mes"],
                "total": d["total"],
                "moneda": d["moneda"],
                "receptor": d["receptor_rfc"],
                "path": d["path"],
            }
            for d in sin_pago
        ],
    }
    if args.include_pagos:
        out["cfdis_con_pago"] = con_pago

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
