"""Silver: limpia, tipa y valida. Lo que no pasa va a cuarentena, con su motivo."""
import pandas as pd

from .config import UNIDADES


def a_silver(bronze, regla_defectuosa=False):
    df = bronze.copy()
    df["id_proveedor"] = df["proveedor"].str.strip().str.replace("PROV ", "", regex=False)
    df["unidad"] = (df["unidad_txt"].str.strip().str.upper()
                    .str.replace(".", "", regex=False).map(UNIDADES))
    df["cantidad"] = pd.to_numeric(df["cantidad_txt"].str.replace(".", "", regex=False),
                                   errors="coerce")
    for col in ["fecha_emision", "fecha_prometida", "fecha_recepcion"]:
        df[col] = pd.to_datetime(df[col])

    recibida = df["fecha_recepcion"].notna()
    motivo = pd.Series("", index=df.index)
    motivo[df["id_proveedor"].eq("")] = "proveedor_nulo"
    motivo[recibida & (df["fecha_recepcion"] < df["fecha_emision"])] = "fecha_incoherente"
    motivo[df["unidad"].isna()] = "unidad_desconocida"
    motivo[recibida & (df["cantidad"].isna() | (df["cantidad"] < 0))] = "cantidad_invalida"
    if regla_defectuosa:
        # Error clásico: una recepción rechazada o parcial puede tener cantidad cero y ser válida.
        motivo[recibida & (df["cantidad"] <= 0)] = "cantidad_cero (regla defectuosa)"

    silver = df[motivo.eq("")].drop(columns=["proveedor", "unidad_txt", "cantidad_txt"])
    cuarentena = df[motivo.ne("")].assign(motivo=motivo[motivo.ne("")])
    return silver.reset_index(drop=True), cuarentena.reset_index(drop=True)
