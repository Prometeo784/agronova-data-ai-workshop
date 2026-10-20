"""Gold: los KPI se definen UNA sola vez. OTD = a tiempo / TODAS las líneas vencidas."""
import pandas as pd

from .config import CORTE

CUENTAS = ["vencidas", "a_tiempo", "tarde", "sin_recibir"]


def a_gold(silver, corte=CORTE):
    s = silver[silver["fecha_prometida"] <= corte].copy()
    s["recibida"] = s["fecha_recepcion"].notna()
    s["a_tiempo"] = s["recibida"] & (s["fecha_recepcion"] <= s["fecha_prometida"])
    g = s.groupby("id_proveedor").agg(vencidas=("id_oc", "size"), a_tiempo=("a_tiempo", "sum"),
                                      recibidas=("recibida", "sum"))
    g.loc["Total"] = g.sum()
    g["tarde"] = g["recibidas"] - g["a_tiempo"]
    g["sin_recibir"] = g["vencidas"] - g["recibidas"]
    g["otd_ingenuo"] = (g["a_tiempo"] / g["recibidas"] * 100).round(1)   # incorrecto
    g["otd_correcto"] = (g["a_tiempo"] / g["vencidas"] * 100).round(1)   # correcto
    g[CUENTAS] = g[CUENTAS].astype(int)
    return g[CUENTAS + ["otd_ingenuo", "otd_correcto"]]


def calidad(inspecciones: pd.DataFrame):
    """Quality Yield = unidades aceptadas / unidades inspeccionadas (solo cubre lo inspeccionado)."""
    inspeccionadas = int(inspecciones["unidades_inspeccionadas"].sum())
    aceptadas = inspeccionadas - int(inspecciones["unidades_rechazadas"].sum())
    return aceptadas, inspeccionadas, aceptadas / inspeccionadas
