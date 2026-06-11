#!/usr/bin/env python3
"""
contador-pyme-mx · gen_diot_txt.py

Genera el archivo TXT pipe-delimited para carga batch en la plataforma DIOT
(pstcdi.clouda.sat.gob.mx, vigente desde 1-ago-2025).

Acepta CSV de entrada con columnas:
  rfc_proveedor, tipo_tercero, tipo_operacion, valor_actos_16, iva_retenido,
  (opcionales: valor_actos_8, valor_actos_0, valor_actos_exentos, importacion_16, etc.)

Uso:
  gen_diot_txt.py --csv proveedores.csv --periodo 2026-05 --out diot_202605.txt
  gen_diot_txt.py --json '[{"rfc":"...","valor_actos_16":10000,...}]' --periodo 2026-05

Output: TXT UTF-8 pipe-delimited + reporte JSON con resumen.

Layout simplificado — 17 campos. Para layout completo del SAT (54 campos)
descarga el ejemplo oficial desde la plataforma DIOT con tu e.firma.
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
LAYOUT = json.load(open(BASE / "data" / "diot_layout.json"))


def to_diot_line(row):
    """Convierte un dict en una línea pipe-delimited del DIOT."""
    fields = [
        str(row.get("tipo_tercero", "01")),
        str(row.get("tipo_operacion", "85")),
        row.get("rfc_proveedor", ""),
        row.get("id_fiscal_extranjero", ""),
        row.get("nombre_extranjero", ""),
        row.get("pais_residencia", ""),
        row.get("nacionalidad", ""),
        f"{float(row.get('valor_actos_16', 0)):.2f}",
        f"{float(row.get('valor_actos_8', 0)):.2f}",
        f"{float(row.get('importacion_16', 0)):.2f}",
        f"{float(row.get('importacion_8', 0)):.2f}",
        f"{float(row.get('importacion_exentos', 0)):.2f}",
        f"{float(row.get('valor_actos_0', 0)):.2f}",
        f"{float(row.get('valor_actos_exentos', 0)):.2f}",
        f"{float(row.get('valor_actos_no_objeto', 0)):.2f}",
        f"{float(row.get('iva_retenido', 0)):.2f}",
        f"{float(row.get('iva_devuelto_descuentos', 0)):.2f}",
    ]
    return "|".join(fields)


def validar_row(row, idx):
    errores = []
    tt = str(row.get("tipo_tercero", "01"))
    rfc = row.get("rfc_proveedor", "").strip().upper()

    if tt in ("01", "02", "03"):
        # nacional → RFC requerido
        if not rfc:
            errores.append(f"renglón {idx}: RFC requerido para TipoTercero {tt}")
        elif len(rfc) not in (12, 13):
            errores.append(f"renglón {idx}: RFC '{rfc}' longitud inválida ({len(rfc)}, debe ser 12 o 13)")

    if tt in ("04", "05"):
        # extranjero
        if not row.get("nombre_extranjero"):
            errores.append(f"renglón {idx}: nombre_extranjero requerido para TipoTercero {tt}")

    # Suma de valores debe ser >0
    suma = sum(float(row.get(k, 0) or 0) for k in [
        "valor_actos_16", "valor_actos_8", "importacion_16", "importacion_8",
        "importacion_exentos", "valor_actos_0", "valor_actos_exentos", "valor_actos_no_objeto"
    ])
    if suma <= 0:
        errores.append(f"renglón {idx}: suma de valores = 0, no enviar renglones vacíos")

    return errores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="Archivo CSV de proveedores")
    ap.add_argument("--json", help="JSON array inline")
    ap.add_argument("--periodo", required=True, help="Periodo YYYY-MM (ej 2026-05)")
    ap.add_argument("--out", help="Archivo de salida TXT (default: diot_<periodo>.txt)")
    ap.add_argument("--encoding", default="utf-8", help="Default: utf-8 sin BOM")
    args = ap.parse_args()

    if args.csv:
        with open(args.csv, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    elif args.json:
        rows = json.loads(args.json)
    else:
        ap.error("--csv o --json requerido")

    # Validar
    todos_errores = []
    for i, row in enumerate(rows, 1):
        todos_errores.extend(validar_row(row, i))

    if todos_errores:
        print(json.dumps({
            "veredicto": "🚨 INVALIDO",
            "errores": todos_errores,
            "renglones_revisados": len(rows),
            "no_se_genero_archivo": True
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Generar TXT
    out_path = args.out or f"diot_{args.periodo.replace('-', '')}.txt"
    lines = [to_diot_line(r) for r in rows]
    Path(out_path).write_text("\n".join(lines), encoding=args.encoding)

    # Resumen por tipo de tercero
    by_tt = {}
    total_16 = 0
    for r in rows:
        tt = str(r.get("tipo_tercero", "01"))
        by_tt[tt] = by_tt.get(tt, 0) + 1
        total_16 += float(r.get("valor_actos_16", 0) or 0)

    print(json.dumps({
        "veredicto": "✅ ARCHIVO_GENERADO",
        "periodo": args.periodo,
        "archivo_salida": out_path,
        "renglones": len(rows),
        "por_tipo_tercero": by_tt,
        "total_valor_actos_16_pct_iva": round(total_16, 2),
        "iva_acreditable_calculado_16": round(total_16 * 0.16, 2),
        "siguiente_paso": f"Sube {out_path} a https://pstcdi.clouda.sat.gob.mx (requiere e.firma para PM o Contraseña para PF). Plazo: día 17 del mes siguiente.",
        "alerta_validacion_final": "Confirma que tus proveedores NO están en lista 69-B antes de subir (usa legal-pyme-mx/scripts/validate_rfc.py --check-69b por cada RFC). Si alguno está en 69-B, no acredites IVA y reporta en sección separada."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
