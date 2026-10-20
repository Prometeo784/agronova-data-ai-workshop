"""Reconciliación y alertas: lo que detecta un 'pipeline verde con dato incorrecto'."""
from .config import UMBRAL_CUARENTENA


def reconciliar(bronze, silver, cuarentena, umbral=UMBRAL_CUARENTENA):
    pct = len(cuarentena) / len(bronze) if len(bronze) else 0.0
    return {"bronze": len(bronze), "silver": len(silver), "cuarentena": len(cuarentena),
            "reconcilia": len(bronze) == len(silver) + len(cuarentena),
            "pct_cuarentena": pct, "alerta": pct > umbral}
