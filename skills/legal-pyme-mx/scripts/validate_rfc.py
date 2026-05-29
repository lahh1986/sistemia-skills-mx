#!/usr/bin/env python3
"""
legal-pyme-mx · validate_rfc.py
Valida estructura de RFC mexicano + opcionalmente lo busca en listas SAT.

Uso:
  validate_rfc.py <RFC>
  validate_rfc.py <RFC> --check-69b
  validate_rfc.py <RFC> --all-lists
  echo "RFC" | validate_rfc.py --stdin

Devuelve JSON.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent.parent.parent / "research"
LISTAS = {
    "69-B_Listado_Completo": "sat/listas-negras/69-B_Listado_Completo.csv",
    "69-B_Definitivos":      "sat/listas-negras/69-B_Definitivos.csv",
    "69-B_Presuntos":        "sat/listas-negras/69-B_Presuntos.csv",
    "69-B_Desvirtuados":     "sat/listas-negras/69-B_Desvirtuados.csv",
    "69-B_SentenciasFav":    "sat/listas-negras/69-B_Sentencias_Favorables.csv",
    "69CFF_Cancelados":      "sat/listas-negras/69CFF_Cancelados.csv",
    "69CFF_Firmes":          "sat/listas-negras/69CFF_Firmes.csv",
    "69CFF_Exigibles":       "sat/listas-negras/69CFF_Exigibles.csv",
    "69CFF_No_localizados":  "sat/listas-negras/69CFF_No_localizados.csv",
    "69CFF_Sentencias":      "sat/listas-negras/69CFF_Sentencias.csv",
    "69CFF_CSD_sin_efectos": "sat/listas-negras/69CFF_CSD_sin_efectos.csv",
}

# RFC persona física: 4 letras + 6 dígitos (AAMMDD) + 3 alfanuméricos
# RFC persona moral:  3 letras + 6 dígitos (AAMMDD) + 3 alfanuméricos
RE_RFC_FISICA = re.compile(r"^([A-ZÑ&]{4})(\d{2})(\d{2})(\d{2})([A-Z0-9]{2})([A-Z0-9])$")
RE_RFC_MORAL  = re.compile(r"^([A-ZÑ&]{3})(\d{2})(\d{2})(\d{2})([A-Z0-9]{2})([A-Z0-9])$")
RE_RFC_GENERICO_NAC = re.compile(r"^XAXX010101000$")  # RFC genérico nacional para CFDI público gral
RE_RFC_GENERICO_EXT = re.compile(r"^XEXX010101000$")  # RFC genérico extranjero


def validar_estructura(rfc: str):
    rfc = rfc.strip().upper()
    if not rfc:
        return {"valido": False, "razon": "RFC vacío"}

    if RE_RFC_GENERICO_NAC.match(rfc):
        return {"valido": True, "tipo": "generico_nacional", "nota": "RFC público en general MX (XAXX010101000)"}
    if RE_RFC_GENERICO_EXT.match(rfc):
        return {"valido": True, "tipo": "generico_extranjero", "nota": "RFC público en general extranjero (XEXX010101000)"}

    m = RE_RFC_FISICA.match(rfc)
    if m:
        letras, aa, mm, dd, homo, dv = m.groups()
        fecha_ok = validar_fecha(aa, mm, dd)
        return {
            "valido": fecha_ok["ok"],
            "tipo": "persona_fisica",
            "longitud": 13,
            "fecha_nacimiento": f"{aa}-{mm}-{dd}" if fecha_ok["ok"] else None,
            "fecha_warning": None if fecha_ok["ok"] else fecha_ok["razon"],
            "homoclave": homo + dv,
        }

    m = RE_RFC_MORAL.match(rfc)
    if m:
        letras, aa, mm, dd, homo, dv = m.groups()
        fecha_ok = validar_fecha(aa, mm, dd)
        return {
            "valido": fecha_ok["ok"],
            "tipo": "persona_moral",
            "longitud": 12,
            "fecha_constitucion": f"{aa}-{mm}-{dd}" if fecha_ok["ok"] else None,
            "fecha_warning": None if fecha_ok["ok"] else fecha_ok["razon"],
            "homoclave": homo + dv,
        }

    return {"valido": False, "razon": "no_match", "longitud": len(rfc), "esperado": "12 (moral) o 13 (física)"}


def validar_fecha(aa, mm, dd):
    try:
        mm_i, dd_i = int(mm), int(dd)
        if not (1 <= mm_i <= 12):
            return {"ok": False, "razon": f"mes inválido: {mm}"}
        if not (1 <= dd_i <= 31):
            return {"ok": False, "razon": f"día inválido: {dd}"}
        return {"ok": True}
    except ValueError:
        return {"ok": False, "razon": "AAMMDD no numérico"}


def buscar_en_listas(rfc: str, all_lists: bool = False):
    """Busca el RFC en las listas SAT descargadas."""
    rfc = rfc.strip().upper()
    encontrado = {}

    listas_target = LISTAS if all_lists else {
        "69-B_Definitivos": LISTAS["69-B_Definitivos"],
        "69-B_Presuntos":   LISTAS["69-B_Presuntos"],
        "69CFF_CSD_sin_efectos": LISTAS["69CFF_CSD_sin_efectos"],
    }

    for nombre, rel_path in listas_target.items():
        path = BASE / rel_path
        if not path.exists():
            encontrado[nombre] = {"status": "lista_no_descargada", "path_esperado": str(path)}
            continue
        try:
            with open(path, encoding="latin-1") as f:
                content = f.read()
            if rfc in content.upper():
                # encontrar la línea
                for line in content.split("\n"):
                    if rfc in line.upper():
                        encontrado[nombre] = {"status": "ENCONTRADO", "linea": line[:300]}
                        break
            else:
                encontrado[nombre] = {"status": "no_encontrado"}
        except Exception as e:
            encontrado[nombre] = {"status": "error", "detail": str(e)}

    return encontrado


def main():
    ap = argparse.ArgumentParser(description="Valida estructura RFC + opcionalmente busca en listas SAT")
    ap.add_argument("rfc", nargs="?", help="RFC a validar")
    ap.add_argument("--stdin", action="store_true", help="Lee RFC de stdin")
    ap.add_argument("--check-69b", action="store_true", help="Busca en listas 69-B (prioritarias)")
    ap.add_argument("--all-lists", action="store_true", help="Busca en todas las listas SAT")
    args = ap.parse_args()

    if args.stdin:
        rfc = sys.stdin.read().strip()
    elif args.rfc:
        rfc = args.rfc
    else:
        ap.error("RFC requerido (positional o --stdin)")

    resultado = {"rfc_input": rfc, "estructura": validar_estructura(rfc)}

    if args.check_69b or args.all_lists:
        resultado["listas_sat"] = buscar_en_listas(rfc, all_lists=args.all_lists)
        # bandera resumida
        encontrado_critico = any(
            v.get("status") == "ENCONTRADO"
            for k, v in resultado["listas_sat"].items()
            if "Definitivos" in k or "CSD" in k
        )
        resultado["riesgo_critico"] = encontrado_critico
        resultado["recomendacion"] = (
            "NO facturar a/desde este RFC. Riesgo de no deducibilidad y auditoría."
            if encontrado_critico
            else "RFC no aparece en listas críticas descargadas. Validar también con SAT online si es operación grande."
        )

    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
