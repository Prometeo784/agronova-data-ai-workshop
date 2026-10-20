"""Cálculo de valor del caso. TODOS los supuestos son FICTICIOS (no son un benchmark)."""


def calcular_valor(inventario=400_000, reduccion=0.10, costo_capital=0.12,
                   horas_paro_evitadas=3, costo_hora_paro=3_000,
                   operacion_anual=6_000, construccion=30_000):
    capital_liberado = inventario * reduccion                 # capital liberado, NO es ahorro
    beneficio_capital = capital_liberado * costo_capital      # beneficio financiero: costo de capital
    beneficio_paros = horas_paro_evitadas * costo_hora_paro   # paros evitados
    beneficio_total = beneficio_capital + beneficio_paros
    neto = beneficio_total - operacion_anual
    return {
        "capital_liberado": round(capital_liberado, 2),
        "beneficio_capital": round(beneficio_capital, 2),
        "beneficio_paros": round(beneficio_paros, 2),
        "beneficio_total": round(beneficio_total, 2),
        "neto_anual": round(neto, 2),
        "recuperacion_anos": round(construccion / neto, 2) if neto > 0 else None,
        "capital_cubre_operacion": beneficio_capital >= operacion_anual,
    }
