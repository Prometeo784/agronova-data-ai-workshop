"""Métricas de una corrida y alertas. Los umbrales son EJEMPLOS, no benchmarks."""
import pandas as pd

from .config import UMBRAL_CUARENTENA


def metricas_corrida(bronze, silver, cuarentena, ultima_carga, ahora=None,
                     umbral_frescura_horas=26, umbral_cuarentena=UMBRAL_CUARENTENA):
    ahora = pd.Timestamp.now() if ahora is None else pd.Timestamp(ahora)
    frescura = (ahora - pd.Timestamp(ultima_carga)).total_seconds() / 3600
    pct = len(cuarentena) / len(bronze) if len(bronze) else 0.0
    alertas = []
    if len(bronze) == 0:
        alertas.append("sin_datos")
    if frescura > umbral_frescura_horas:
        alertas.append("frescura")
    if pct > umbral_cuarentena:
        alertas.append("cuarentena")
    if len(bronze) != len(silver) + len(cuarentena):
        alertas.append("reconciliacion")
    return {"filas_bronze": len(bronze), "filas_silver": len(silver), "filas_cuarentena": len(cuarentena),
            "frescura_horas": round(frescura, 1), "pct_cuarentena": pct, "alertas": alertas}
