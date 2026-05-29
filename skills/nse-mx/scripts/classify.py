#!/usr/bin/env python3
"""
nse-mx: Clasificador NSE AMAI 2024 (implementación abierta).

Uso:
  classify.py --educ profesional_completa --banos 2 --autos 1 --internet si --ocupados 2 --dormitorios 3
  classify.py --json '{"educacion_jefe":"secundaria_completa","banos_completos":1,"autos":0,"internet":"si","ocupados":1,"dormitorios":2}'
  echo '{...}' | classify.py --stdin

Devuelve JSON con: nivel, puntos, percentil_aprox, desglose.
"""
import argparse
import json
import os
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "puntos_amai_2024.json"


def load_rules():
    with open(DATA_PATH) as f:
        return json.load(f)


def normalize_int_bucket(value, valid_keys):
    """Map integer 0..N to '0'/'1'/'2'/'3+' style keys."""
    if isinstance(value, str):
        return value
    value = int(value)
    keys_int = []
    has_plus = None
    for k in valid_keys:
        if k.endswith("+"):
            has_plus = k
        else:
            try:
                keys_int.append(int(k))
            except ValueError:
                pass
    keys_int.sort()
    if value >= max(keys_int) and has_plus:
        return has_plus
    return str(min(max(value, min(keys_int)), max(keys_int)))


def score_household(h, rules):
    """Score a household dict against AMAI rules. Returns (total, desglose)."""
    vars_rules = rules["variables"]
    desglose = []
    total = 0

    educ = h.get("educacion_jefe", "secundaria_completa")
    p = vars_rules["educacion_jefe"]["puntos"].get(educ, 0)
    desglose.append(("Educación jefe", educ, p))
    total += p

    banos = normalize_int_bucket(h.get("banos_completos", 1), vars_rules["banos_completos"]["puntos"].keys())
    p = vars_rules["banos_completos"]["puntos"][banos]
    desglose.append(("Baños completos", banos, p))
    total += p

    autos = normalize_int_bucket(h.get("autos", 0), vars_rules["autos"]["puntos"].keys())
    p = vars_rules["autos"]["puntos"][autos]
    desglose.append(("Autos", autos, p))
    total += p

    inet = h.get("internet", "no")
    if isinstance(inet, bool):
        inet = "si" if inet else "no"
    p = vars_rules["internet"]["puntos"].get(inet.lower(), 0)
    desglose.append(("Internet", inet, p))
    total += p

    ocup = normalize_int_bucket(h.get("ocupados", 1), vars_rules["ocupados"]["puntos"].keys())
    p = vars_rules["ocupados"]["puntos"][ocup]
    desglose.append(("Ocupados", ocup, p))
    total += p

    dorm = normalize_int_bucket(h.get("dormitorios", 1), vars_rules["dormitorios"]["puntos"].keys())
    p = vars_rules["dormitorios"]["puntos"][dorm]
    desglose.append(("Dormitorios", dorm, p))
    total += p

    return total, desglose


def puntos_to_nivel(puntos, rules):
    for n in rules["niveles"]:
        if n["min"] <= puntos <= n["max"]:
            return n
    return rules["niveles"][-1]


def aprox_percentil(puntos, rules):
    """Cumulative percentile (% de hogares con NSE ≤ este)."""
    cum = 0
    for n in rules["niveles"]:
        if puntos > n["max"]:
            cum += n["pct_nacional"]
        elif n["min"] <= puntos <= n["max"]:
            ratio = (puntos - n["min"]) / max(n["max"] - n["min"], 1)
            cum += n["pct_nacional"] * ratio
            return round(cum, 1)
    return round(cum, 1)


def classify(hogar):
    rules = load_rules()
    puntos, desglose = score_household(hogar, rules)
    nivel = puntos_to_nivel(puntos, rules)
    pct = aprox_percentil(puntos, rules)
    return {
        "nivel": nivel["nivel"],
        "label": nivel["label"],
        "puntos": puntos,
        "puntos_max": rules["escala_max"],
        "percentil_aprox": pct,
        "porcentaje_hogares_mx_en_este_nivel": nivel["pct_nacional"],
        "desglose": [{"variable": v, "respuesta": r, "puntos": p} for v, r, p in desglose],
    }


def main():
    ap = argparse.ArgumentParser(description="nse-mx — Clasificador NSE AMAI 2024")
    ap.add_argument("--educ", help="educacion_jefe (sin_instruccion..posgrado)")
    ap.add_argument("--banos", help="baños completos 0/1/2/3+")
    ap.add_argument("--autos", help="autos 0/1/2/3+")
    ap.add_argument("--internet", help="si/no")
    ap.add_argument("--ocupados", help="0/1/2/3+")
    ap.add_argument("--dormitorios", help="0/1/2/3/4+")
    ap.add_argument("--json", help="JSON inline con todas las variables")
    ap.add_argument("--stdin", action="store_true", help="Lee JSON de stdin")
    args = ap.parse_args()

    if args.stdin:
        hogar = json.load(sys.stdin)
    elif args.json:
        hogar = json.loads(args.json)
    else:
        hogar = {
            "educacion_jefe": args.educ or "secundaria_completa",
            "banos_completos": args.banos or "1",
            "autos": args.autos or "0",
            "internet": args.internet or "no",
            "ocupados": args.ocupados or "1",
            "dormitorios": args.dormitorios or "1",
        }

    result = classify(hogar)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
