import pandas as pd


def otd_con_tolerancia(silver, dias=1, corte=pd.Timestamp("2026-10-01")):
    s = silver[silver["fecha_prometida"] <= corte]
    limite = s["fecha_prometida"] + pd.Timedelta(days=dias)
    a_tiempo = s["fecha_recepcion"].notna() & (s["fecha_recepcion"] <= limite)
    por_prov = a_tiempo.groupby(s["id_proveedor"]).sum() / s.groupby("id_proveedor").size()
    return (por_prov * 100).round(1)
