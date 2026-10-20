"""Ingesta incremental e idempotente hacia Bronze."""
import pandas as pd

from .config import CLAVE


def extraer_incremental(con, marca_de_agua):
    """Trae solo lo modificado después de la marca de agua. Sin marca = carga completa."""
    sql, params = "SELECT * FROM oc_linea", ()
    if marca_de_agua:
        sql += " WHERE fecha_modificacion > ?"
        params = (marca_de_agua,)
    return pd.read_sql_query(sql, con, params=params)


def cargar_bronze(bronze, nuevos, lote):
    """Bronze = copia fiel + trazabilidad (lote y fecha de carga).
    Deduplica por clave EN MEMORIA: evita filas repetidas al re-ejecutar este ejemplo.
    No equivale a una carga idempotente de producción (ver upsert.py: UPSERT atómico)."""
    nuevos = nuevos.assign(lote_carga=lote, fecha_carga=pd.Timestamp.now())
    combinado = pd.concat([bronze, nuevos], ignore_index=True)
    return combinado.drop_duplicates(subset=CLAVE, keep="last").reset_index(drop=True)
