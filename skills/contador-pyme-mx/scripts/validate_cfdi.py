#!/usr/bin/env python3
"""
contador-pyme-mx · validate_cfdi.py

Valida un CFDI 4.0 XML contra:
  1. Estructura XML básica + versión 4.0
  2. Catálogos vigentes (RegimenFiscal, UsoCFDI, FormaPago, MetodoPago)
  3. Compatibilidad régimen receptor vs uso CFDI
  4. Detección de complementos (Pagos 2.0, Nómina 1.2, Carta Porte 3.1, Retenciones)
  5. Reglas de retención obligatoria (honorarios/arrendamiento/RESICO)
  6. Cruce RFC emisor y receptor contra listas 69-B SAT (vía legal-pyme-mx)
  7. Alerta PUE timbrado en últimos 5 días del mes

Uso:
  validate_cfdi.py archivo.xml
  validate_cfdi.py archivo.xml --verbose
  validate_cfdi.py archivo.xml --skip-69b
  validate_cfdi.py - < archivo.xml         # stdin

Devuelve JSON con: veredicto, hallazgos[], data extraída.
"""
import argparse
import json
import sys
import subprocess
import re
from datetime import datetime, date
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).parent.parent
CATALOGOS = json.load(open(BASE / "data" / "catalogos_cfdi_resumen.json"))
RETENCIONES = json.load(open(BASE / "data" / "retenciones_pf.json"))

NS_CFDI = "http://www.sat.gob.mx/cfd/4"
NS_TFD = "http://www.sat.gob.mx/TimbreFiscalDigital"
NS_PAGOS20 = "http://www.sat.gob.mx/Pagos20"
NS_NOMINA12 = "http://www.sat.gob.mx/nomina12"
NS_CARTAPORTE31 = "http://www.sat.gob.mx/CartaPorte31"
NS_RETENCION = "http://www.sat.gob.mx/esquemas/retencionpago/2"

LEGAL_69B = BASE.parent / "legal-pyme-mx" / "scripts" / "validate_rfc.py"


def parse_cfdi(xml_str):
    root = ET.fromstring(xml_str)
    if not root.tag.endswith("Comprobante"):
        raise ValueError(f"raíz no es cfdi:Comprobante (es {root.tag})")
    return root


def get_attr(elem, name, default=None):
    return elem.get(name, default) if elem is not None else default


def extraer_datos(root):
    """Extrae los campos principales del CFDI 4.0."""
    emisor = root.find(f"{{{NS_CFDI}}}Emisor")
    receptor = root.find(f"{{{NS_CFDI}}}Receptor")
    impuestos = root.find(f"{{{NS_CFDI}}}Impuestos")
    complemento = root.find(f"{{{NS_CFDI}}}Complemento")
    conceptos = root.find(f"{{{NS_CFDI}}}Conceptos")

    data = {
        "version": get_attr(root, "Version"),
        "fecha": get_attr(root, "Fecha"),
        "subtotal": get_attr(root, "SubTotal"),
        "total": get_attr(root, "Total"),
        "moneda": get_attr(root, "Moneda"),
        "tipo_cambio": get_attr(root, "TipoCambio"),
        "tipo_comprobante": get_attr(root, "TipoDeComprobante"),
        "metodo_pago": get_attr(root, "MetodoPago"),
        "forma_pago": get_attr(root, "FormaPago"),
        "lugar_expedicion": get_attr(root, "LugarExpedicion"),
        "emisor": {
            "rfc": get_attr(emisor, "Rfc"),
            "nombre": get_attr(emisor, "Nombre"),
            "regimen": get_attr(emisor, "RegimenFiscal"),
        },
        "receptor": {
            "rfc": get_attr(receptor, "Rfc"),
            "nombre": get_attr(receptor, "Nombre"),
            "regimen": get_attr(receptor, "RegimenFiscalReceptor"),
            "domicilio_fiscal": get_attr(receptor, "DomicilioFiscalReceptor"),
            "uso_cfdi": get_attr(receptor, "UsoCFDI"),
        },
        "complementos_detectados": [],
        "tiene_retenciones": False,
        "retenciones": [],
        "conceptos_count": 0,
        "tfd_uuid": None,
    }

    # complementos
    if complemento is not None:
        for child in complemento:
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            ns = child.tag.split("}")[0].lstrip("{") if "}" in child.tag else ""
            if ns == NS_TFD:
                data["tfd_uuid"] = child.get("UUID")
            elif ns == NS_PAGOS20:
                data["complementos_detectados"].append("Pagos 2.0")
            elif ns == NS_NOMINA12:
                data["complementos_detectados"].append("Nómina 1.2")
            elif ns == NS_CARTAPORTE31:
                data["complementos_detectados"].append("Carta Porte 3.1")
            else:
                data["complementos_detectados"].append(f"{tag} ({ns})")

    # retenciones
    if impuestos is not None:
        retenciones_el = impuestos.find(f"{{{NS_CFDI}}}Retenciones")
        if retenciones_el is not None:
            data["tiene_retenciones"] = True
            for ret in retenciones_el.findall(f"{{{NS_CFDI}}}Retencion"):
                data["retenciones"].append({
                    "impuesto": get_attr(ret, "Impuesto"),
                    "importe": get_attr(ret, "Importe"),
                })

    if conceptos is not None:
        data["conceptos_count"] = len(conceptos.findall(f"{{{NS_CFDI}}}Concepto"))
        primer_concepto = conceptos.find(f"{{{NS_CFDI}}}Concepto")
        if primer_concepto is not None:
            data["primer_concepto_descripcion"] = get_attr(primer_concepto, "Descripcion", "")[:200]
            data["primer_concepto_clave_prodserv"] = get_attr(primer_concepto, "ClaveProdServ")

    return data


def validar(data, skip_69b=False):
    hallazgos = []

    # 1. Versión
    if data["version"] != "4.0":
        hallazgos.append({"sev": "🚨", "tipo": "estructura", "mensaje": f"Versión CFDI ≠ 4.0 (es {data['version']})"})

    # 2. Catálogos: régimen emisor
    reg_e = data["emisor"]["regimen"]
    if reg_e and reg_e not in CATALOGOS["regimenes_fiscales"]:
        hallazgos.append({"sev": "🚨", "tipo": "catalogo", "mensaje": f"Régimen emisor '{reg_e}' no está en catálogo SAT"})
    elif reg_e:
        nombre = CATALOGOS["regimenes_fiscales"][reg_e]
        hallazgos.append({"sev": "✓", "tipo": "info", "mensaje": f"Emisor régimen {reg_e}: {nombre}"})

    # 3. Catálogos: régimen receptor
    reg_r = data["receptor"]["regimen"]
    if reg_r and reg_r not in CATALOGOS["regimenes_fiscales"]:
        hallazgos.append({"sev": "🚨", "tipo": "catalogo", "mensaje": f"Régimen receptor '{reg_r}' no está en catálogo SAT"})

    # 4. Uso CFDI vs régimen receptor (compatibilidad)
    uso = data["receptor"]["uso_cfdi"]
    if uso and uso not in CATALOGOS["usos_cfdi"]:
        hallazgos.append({"sev": "🚨", "tipo": "catalogo", "mensaje": f"UsoCFDI '{uso}' no está en catálogo SAT"})
    else:
        compat = CATALOGOS.get("compatibilidad_regimen_uso_cfdi", {}).get("ejemplos", {})
        for grupo, regimenes in compat.items():
            if isinstance(regimenes, list) and uso in grupo.split("_") and reg_r and reg_r not in regimenes:
                hallazgos.append({
                    "sev": "⚠️", "tipo": "compatibilidad",
                    "mensaje": f"UsoCFDI {uso} típicamente NO es compatible con régimen receptor {reg_r}. Verificar."
                })
                break

    # 5. Método de pago + Forma de pago
    metodo = data["metodo_pago"]
    forma = data["forma_pago"]
    if metodo and metodo not in CATALOGOS["metodos_pago"]:
        hallazgos.append({"sev": "🚨", "tipo": "catalogo", "mensaje": f"MetodoPago '{metodo}' no es PUE ni PPD"})
    if forma and forma not in CATALOGOS["formas_pago"]:
        hallazgos.append({"sev": "🚨", "tipo": "catalogo", "mensaje": f"FormaPago '{forma}' no está en catálogo"})
    if metodo == "PUE" and forma == "99":
        hallazgos.append({"sev": "🚨", "tipo": "regla", "mensaje": "FormaPago 99 (Por definir) solo se usa con PPD, no con PUE"})

    # 6. Alerta PUE a fin de mes
    if metodo == "PUE" and data.get("fecha"):
        try:
            f = datetime.fromisoformat(data["fecha"].split("T")[0])
            # último día del mes
            from calendar import monthrange
            ultimo = monthrange(f.year, f.month)[1]
            if f.day >= ultimo - 4:
                hallazgos.append({
                    "sev": "⚠️", "tipo": "pue_fin_mes",
                    "mensaje": f"CFDI PUE timbrado el día {f.day} (a {ultimo-f.day} días del cierre de mes). "
                               f"Si NO se cobra antes del último día del mes, el SAT lo asume cobrado (ISR/IVA sobre ingreso fantasma). "
                               f"Acción: confirmar que el cobro entró al banco antes del {f.year}-{f.month:02d}-{ultimo}."
                })
        except Exception:
            pass

    # 7. Validar retenciones obligatorias (RESICO PF → PM = 1.25% ISR)
    es_emisor_resico = reg_e == "626"
    es_receptor_pm = reg_r in ["601", "603", "620", "623", "624"]
    if es_emisor_resico and es_receptor_pm and not data["tiene_retenciones"]:
        # validar si tiene retención ISR 1.25%
        ret_isr_resico_ok = False
        for r in data["retenciones"]:
            if r["impuesto"] == "001" and r["importe"]:
                # heurística: si importe ~= subtotal × 0.0125
                try:
                    subt = float(data["subtotal"])
                    imp = float(r["importe"])
                    if abs(imp - subt * 0.0125) < 0.01:
                        ret_isr_resico_ok = True
                except Exception:
                    pass
        if not ret_isr_resico_ok:
            hallazgos.append({
                "sev": "🚨", "tipo": "retencion_resico",
                "mensaje": "Emisor RESICO PF (régimen 626) factura a Persona Moral. "
                           "Falta retención ISR 1.25% (LISR Art. 113-J). "
                           "Sin esto: PM NO puede deducir el gasto + PF recibe requerimiento SAT."
            })

    # 8. Heurística honorarios/arrendamiento (PF → PM)
    desc = (data.get("primer_concepto_descripcion") or "").lower()
    palabras_honorarios = ["honorarios", "asesoría", "asesoria", "consultoría", "consultoria", "profesional"]
    palabras_arrendamiento = ["arrendamiento", "renta de", "renta del", "alquiler"]
    emisor_pf = reg_e in ["612", "606", "608"]  # PF act emp, arrendamiento, otros ingresos
    if emisor_pf and es_receptor_pm and not data["tiene_retenciones"]:
        if any(p in desc for p in palabras_honorarios):
            hallazgos.append({
                "sev": "⚠️", "tipo": "retencion_honorarios",
                "mensaje": "Concepto sugiere honorarios profesionales (emisor PF, receptor PM) sin retenciones. "
                           "Debe llevar ISR 10% (LISR Art. 106) + IVA 10.6667% (LIVA Art. 1-A)."
            })
        elif any(p in desc for p in palabras_arrendamiento):
            hallazgos.append({
                "sev": "⚠️", "tipo": "retencion_arrendamiento",
                "mensaje": "Concepto sugiere arrendamiento (emisor PF, receptor PM) sin retenciones. "
                           "Debe llevar ISR 10% (LISR Art. 116) + IVA 10.6667% (LIVA Art. 1-A)."
            })

    # 9. Total = subtotal coherente
    if data["subtotal"] and data["total"]:
        try:
            subt = float(data["subtotal"])
            tot = float(data["total"])
            if tot < subt * 0.5 or tot > subt * 2.5:
                hallazgos.append({
                    "sev": "⚠️", "tipo": "totales",
                    "mensaje": f"Total {tot} parece inconsistente con subtotal {subt} (diferencia mayor al rango normal)."
                })
        except Exception:
            pass

    # 10. Moneda extranjera sin tipo de cambio
    if data["moneda"] not in (None, "MXN", "XXX") and not data["tipo_cambio"]:
        hallazgos.append({
            "sev": "🚨", "tipo": "moneda",
            "mensaje": f"Moneda {data['moneda']} requiere TipoCambio (Art. 20 CFF)."
        })

    return hallazgos


def cruzar_69b(rfc, label="emisor"):
    """Llama al check 69-B de legal-pyme-mx."""
    if not LEGAL_69B.exists():
        return {"label": label, "status": "skip", "razon": f"legal-pyme-mx no encontrado en {LEGAL_69B}"}
    try:
        res = subprocess.run(
            ["python3", str(LEGAL_69B), rfc, "--check-69b"],
            capture_output=True, text=True, timeout=10
        )
        if res.returncode != 0:
            return {"label": label, "status": "error", "stderr": res.stderr[:200]}
        out = json.loads(res.stdout)
        return {
            "label": label,
            "rfc": rfc,
            "estructura_valida": out["estructura"].get("valido"),
            "riesgo_critico": out.get("riesgo_critico", False),
            "encontrado_en": [k for k, v in out.get("listas_sat", {}).items() if v.get("status") == "ENCONTRADO"],
        }
    except Exception as e:
        return {"label": label, "status": "error", "detail": str(e)}


def main():
    ap = argparse.ArgumentParser(description="Valida CFDI 4.0 (contador-pyme-mx)")
    ap.add_argument("xml", help="Path al XML del CFDI (o '-' para stdin)")
    ap.add_argument("--verbose", action="store_true", help="Imprime data extraída completa")
    ap.add_argument("--skip-69b", action="store_true", help="No cruzar contra listas SAT")
    args = ap.parse_args()

    if args.xml == "-":
        xml_str = sys.stdin.read()
    else:
        xml_str = Path(args.xml).read_text(encoding="utf-8")

    try:
        root = parse_cfdi(xml_str)
        data = extraer_datos(root)
    except Exception as e:
        print(json.dumps({"veredicto": "🚨 ERROR_PARSE", "mensaje": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    hallazgos = validar(data)

    # 69-B
    cruces_69b = []
    if not args.skip_69b:
        if data["emisor"]["rfc"]:
            cruces_69b.append(cruzar_69b(data["emisor"]["rfc"], "emisor"))
        if data["receptor"]["rfc"]:
            cruces_69b.append(cruzar_69b(data["receptor"]["rfc"], "receptor"))

        for cruce in cruces_69b:
            if cruce.get("riesgo_critico"):
                hallazgos.append({
                    "sev": "🚨", "tipo": "69-B",
                    "mensaje": f"RFC {cruce['label']} ({cruce['rfc']}) está en lista negra SAT: {', '.join(cruce['encontrado_en'])}. "
                               f"NO timbrar / NO deducir."
                })

    # veredicto
    severidades = [h["sev"] for h in hallazgos]
    if "🚨" in severidades:
        veredicto = "🚨 INVÁLIDO / NO_TIMBRAR"
    elif "⚠️" in severidades:
        veredicto = "⚠️ VÁLIDO_CON_ADVERTENCIAS"
    else:
        veredicto = "✅ VÁLIDO"

    output = {
        "veredicto": veredicto,
        "uuid": data["tfd_uuid"],
        "data": {
            "emisor": data["emisor"],
            "receptor": data["receptor"],
            "fecha": data["fecha"],
            "total": data["total"],
            "moneda": data["moneda"],
            "metodo_pago": data["metodo_pago"],
            "tipo_comprobante": data["tipo_comprobante"],
            "complementos": data["complementos_detectados"],
            "tiene_retenciones": data["tiene_retenciones"],
            "retenciones": data["retenciones"],
        },
        "hallazgos": hallazgos,
        "cruce_69b": cruces_69b if not args.skip_69b else "skipped",
    }
    if args.verbose:
        output["data_completa"] = data

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
