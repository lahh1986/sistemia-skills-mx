#!/usr/bin/env python3
"""
parse_pdf.py — Extrae datos estructurados de PDFs del SAT.

Soporta:
  - Constancia de Situación Fiscal (CSF)
  - Opinión de Cumplimiento (32-D)

Detecta el tipo automáticamente leyendo el encabezado del PDF.

Uso:
  python3 parse_pdf.py <ruta_pdf>

Salida:
  JSON en stdout. Errores van a stderr con código de salida != 0.

Requiere:
  - pdftotext (poppler-utils)

Si un campo no se puede extraer, sale como null — nunca falla por un campo faltante.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def pdf_to_text(pdf_path: Path) -> str:
    if not shutil.which("pdftotext"):
        fail(
            "pdftotext no está instalado. Instala con `brew install poppler` (Mac) "
            "o `sudo apt install poppler-utils` (Linux)."
        )
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        fail(f"pdftotext falló: {e.stderr.strip()}")
    return result.stdout


def detect_type(text: str) -> str:
    upper = text.upper()
    if "OPINIÓN DEL CUMPLIMIENTO" in upper or "OPINION DEL CUMPLIMIENTO" in upper:
        return "opinion_cumplimiento"
    if "CONSTANCIA DE SITUACIÓN FISCAL" in upper or "CEDULA DE IDENTIFICACIÓN" in upper or "CÉDULA DE IDENTIFICACIÓN" in upper:
        return "constancia_situacion_fiscal"
    return "desconocido"


def find_one(pattern: str, text: str, flags: int = re.IGNORECASE) -> str | None:
    m = re.search(pattern, text, flags)
    if not m:
        return None
    return m.group(1).strip()


def find_all_after(label: str, text: str) -> list[str]:
    """Encuentra todas las líneas no vacías inmediatamente después de la primera línea con la etiqueta."""
    lines = text.splitlines()
    out: list[str] = []
    capture = False
    for line in lines:
        if not capture and label.lower() in line.lower():
            capture = True
            continue
        if capture:
            stripped = line.strip()
            if not stripped:
                if out:
                    break
                continue
            if stripped.isupper() and len(stripped) < 80 and not any(c.isdigit() for c in stripped[:3]):
                break
            out.append(stripped)
    return out


def parse_csf(text: str) -> dict[str, Any]:
    rfc = find_one(r"RFC[:\s]+([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})", text)
    curp = find_one(r"CURP[:\s]+([A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d)", text)

    nombre = find_one(r"(?:Nombre|Denominaci[oó]n[/ ]?Raz[oó]n Social)[:\s]+([^\n]+?)(?:\s{2,}|$)", text)

    regimen = find_one(r"R[eé]gimen[s ]*(?:Fiscal|Capital)?[:\s]+([^\n]+?)(?:\s{2,}|$)", text)

    fecha_emision = find_one(r"Fecha de [Ee]misi[oó]n[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if not fecha_emision:
        fecha_emision = find_one(r"Lugar y [Ff]echa de [Ee]misi[oó]n[^\d]+(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})", text)

    domicilio = {
        "calle": find_one(r"(?:Nombre de )?[Vv]ialidad[:\s]+([^\n]+?)(?:\s{2,}|$)", text),
        "numero_exterior": find_one(r"N[uú]mero [Ee]xterior[:\s]+([^\n\s]+)", text),
        "numero_interior": find_one(r"N[uú]mero [Ii]nterior[:\s]+([^\n\s]+)", text),
        "colonia": find_one(r"(?:Nombre de la )?[Cc]olonia[:\s]+([^\n]+?)(?:\s{2,}|$)", text),
        "municipio": find_one(r"(?:Nombre del )?[Mm]unicipio(?:\s+o\s+[Dd]elegaci[oó]n)?[:\s]+([^\n]+?)(?:\s{2,}|$)", text),
        "entidad_federativa": find_one(r"(?:Nombre de la )?[Ee]ntidad [Ff]ederativa[:\s]+([^\n]+?)(?:\s{2,}|$)", text),
        "codigo_postal": find_one(r"C[oó]digo [Pp]ostal[:\s]+(\d{5})", text),
    }

    obligaciones: list[str] = []
    obl_section = re.search(
        r"(?:Obligaciones|Regímenes)\s*\n(.+?)(?:\n\s*\n|Fecha de [Ee]misi[oó]n|$)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if obl_section:
        for line in obl_section.group(1).splitlines():
            line = line.strip()
            if line and len(line) > 10 and not line.startswith("Régimen"):
                obligaciones.append(line)

    return {
        "tipo": "constancia_situacion_fiscal",
        "rfc": rfc,
        "curp": curp,
        "nombre": nombre,
        "regimen_fiscal": regimen,
        "domicilio": domicilio,
        "obligaciones": obligaciones,
        "fecha_emision": fecha_emision,
    }


def parse_opinion(text: str) -> dict[str, Any]:
    rfc = find_one(r"RFC[:\s]+([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})", text)
    nombre = find_one(r"(?:Nombre|Denominaci[oó]n[/ ]?Raz[oó]n Social|Contribuyente)[:\s]+([^\n]+?)(?:\s{2,}|$)", text)
    folio = find_one(r"Folio[:\s]+([A-Z0-9\-]+)", text)

    sentido: str | None = None
    upper = text.upper()
    if "OPINIÓN POSITIVA" in upper or "OPINION POSITIVA" in upper:
        sentido = "POSITIVA"
    elif "OPINIÓN NEGATIVA" in upper or "OPINION NEGATIVA" in upper:
        sentido = "NEGATIVA"
    elif "SIN OPINIÓN" in upper or "SIN OPINION" in upper or "NO INSCRITO" in upper:
        sentido = "SIN_OPINION"

    fecha_emision = find_one(r"Fecha[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if not fecha_emision:
        fecha_emision = find_one(r"(\d{1,2}\s+DE\s+\w+\s+DE\s+\d{4})", text)

    return {
        "tipo": "opinion_cumplimiento",
        "rfc": rfc,
        "nombre": nombre,
        "sentido": sentido,
        "folio": folio,
        "fecha_emision": fecha_emision,
    }


def main() -> None:
    if len(sys.argv) != 2:
        fail("Uso: python3 parse_pdf.py <ruta_pdf>")

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        fail(f"El archivo no existe: {pdf_path}")
    if not pdf_path.is_file():
        fail(f"No es un archivo: {pdf_path}")

    text = pdf_to_text(pdf_path)
    tipo = detect_type(text)

    if tipo == "constancia_situacion_fiscal":
        data = parse_csf(text)
    elif tipo == "opinion_cumplimiento":
        data = parse_opinion(text)
    else:
        fail("No se pudo detectar el tipo de PDF (¿es realmente del SAT?)")

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
