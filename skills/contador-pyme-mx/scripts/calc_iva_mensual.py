#!/usr/bin/env python3
"""
contador-pyme-mx · calc_iva_mensual.py

Calcula el pago definitivo mensual de IVA (LIVA Art. 5-D).

Mecánica:
  IVA trasladado cobrado en el mes
  - IVA acreditable efectivamente pagado en el mes (con requisitos Art. 5 LIVA)
  - IVA retenido a tu cargo (cuando un cliente te retuvo IVA)
  + IVA que retuviste a terceros (cuando tu retuviste a un proveedor)
  - Saldos a favor de meses anteriores aplicados
  = IVA a pagar o saldo a favor del mes

Uso:
  calc_iva_mensual.py \\
    --iva-trasladado-cobrado=15000 \\
    --iva-acreditable-pagado=8500 \\
    --iva-retenido-a-mi=200 \\
    --iva-que-retuve=350 \\
    --saldo-favor-anterior=1200
"""
import argparse
import json


def calc(args):
    trasladado = args.iva_trasladado_cobrado or 0
    acreditable = args.iva_acreditable_pagado or 0
    retenido_a_mi = args.iva_retenido_a_mi or 0
    que_retuve = args.iva_que_retuve or 0
    saldo_anterior = args.saldo_favor_anterior or 0

    # IVA causado neto
    iva_causado = trasladado - acreditable
    # Resta retenciones que me hicieron (ya las pagó el cliente al SAT por mí)
    iva_causado_neto = iva_causado - retenido_a_mi
    # Suma lo que yo retuve a otros (lo debo enterar)
    iva_a_enterar = iva_causado_neto + que_retuve
    # Aplica saldo a favor anterior
    iva_a_pagar = iva_a_enterar - saldo_anterior

    return {
        "calculo": {
            "iva_trasladado_cobrado": trasladado,
            "menos_iva_acreditable_pagado": acreditable,
            "iva_causado": round(iva_causado, 2),
            "menos_iva_retenido_a_mi": retenido_a_mi,
            "mas_iva_que_retuve_a_otros": que_retuve,
            "iva_a_enterar_antes_compensacion": round(iva_a_enterar, 2),
            "menos_saldo_favor_anterior_aplicado": saldo_anterior,
            "RESULTADO": round(iva_a_pagar, 2),
        },
        "verdict": (
            "PAGAR" if iva_a_pagar > 0
            else "SALDO_A_FAVOR" if iva_a_pagar < 0
            else "CERO"
        ),
        "monto_a_pagar": round(max(0, iva_a_pagar), 2),
        "saldo_a_favor_para_proximos_meses": round(abs(iva_a_pagar), 2) if iva_a_pagar < 0 else 0,
        "fundamento": "LIVA Art. 5-D: cálculo del pago definitivo mensual. La acreditación requiere cumplir todos los requisitos del Art. 5 LIVA (efectivamente pagado, CFDI válido, estricta indispensabilidad, traslado expreso).",
        "validaciones_skill": [
            "IVA acreditable: solo el del mes efectivamente pagado (no devengado).",
            "Si tienes operaciones exentas, aplica proporción de acreditable (LIVA Art. 5-A).",
            "Saldo a favor: puede compensarse en meses siguientes, devolución en línea, o compensación universal (limitada desde 2019).",
            "Si tu saldo a favor lleva 5+ meses sin moverse, considera solicitar devolución (formato A-29).",
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iva-trasladado-cobrado", type=float, required=True, help="IVA cobrado a clientes en el mes")
    ap.add_argument("--iva-acreditable-pagado", type=float, required=True, help="IVA pagado a proveedores en el mes (con CFDI válido y requisitos Art. 5 LIVA)")
    ap.add_argument("--iva-retenido-a-mi", type=float, help="IVA que me retuvieron clientes PM")
    ap.add_argument("--iva-que-retuve", type=float, help="IVA que retuve a proveedores PF (honorarios/arrendamiento)")
    ap.add_argument("--saldo-favor-anterior", type=float, help="Saldo a favor de meses anteriores a aplicar")
    args = ap.parse_args()
    print(json.dumps(calc(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
