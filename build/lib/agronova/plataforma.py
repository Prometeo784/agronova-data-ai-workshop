"""Mini plataforma de datos PERSISTENTE (SQLite). Didáctica: ilustra principios, NO es código de producción.

Qué demuestra, a diferencia de las funciones sueltas del resto del paquete:
  * El estado vive en un archivo (marca de agua, tres capas, cuarentena y registro de corridas).
  * Cada corrida es ATÓMICA: si falla a mitad, no queda nada a medias y la marca de agua NO avanza.
  * Es IDEMPOTENTE: repetir una corrida, o reiniciar la marca, deja el mismo estado.
  * Se puede REPROCESAR Silver desde Bronze sin volver a la fuente (por ejemplo, tras corregir una regla).
  * Detecta cambios en el esquema de la fuente: las columnas nuevas se avisan; las que faltan detienen la carga.
"""
import sqlite3

import pandas as pd

from .gold import a_gold
from .ingesta import extraer_incremental
from .observabilidad import metricas_corrida
from .silver import a_silver
from .upsert import COLUMNAS as COLUMNAS_ORIGEN
from .upsert import DDL as DDL_BRONZE
from .upsert import UPSERT as UPSERT_BRONZE

DDL = [
    DDL_BRONZE,
    """CREATE TABLE IF NOT EXISTS slv_oc_linea (
        id_oc INTEGER NOT NULL, linea INTEGER NOT NULL, id_proveedor TEXT NOT NULL, unidad TEXT,
        fecha_emision TEXT, fecha_prometida TEXT, fecha_recepcion TEXT, cantidad REAL, lote_carga TEXT,
        PRIMARY KEY (id_oc, linea))""",
    """CREATE TABLE IF NOT EXISTS slv_oc_linea_cuarentena (
        id_oc INTEGER NOT NULL, linea INTEGER NOT NULL, motivo TEXT, lote_carga TEXT,
        PRIMARY KEY (id_oc, linea))""",
    """CREATE TABLE IF NOT EXISTS gld_otd_proveedor (
        id_proveedor TEXT PRIMARY KEY, vencidas INTEGER, a_tiempo INTEGER, tarde INTEGER,
        sin_recibir INTEGER, otd_ingenuo REAL, otd_correcto REAL)""",
    "CREATE TABLE IF NOT EXISTS ctl_marca_agua (tabla TEXT PRIMARY KEY, valor TEXT)",
    """CREATE TABLE IF NOT EXISTS ctl_corridas (
        lote TEXT, ahora TEXT, estado TEXT, filas_leidas INTEGER, bronze_total INTEGER, silver_total INTEGER,
        cuarentena_total INTEGER, pct_cuarentena REAL, alertas TEXT, error TEXT)""",
]


class EsquemaOrigenError(RuntimeError):
    """La fuente cambió de forma que impide cargar (faltan columnas que el contrato exige)."""


def abrir(ruta=":memory:"):
    con = sqlite3.connect(ruta)
    for sentencia in DDL:
        con.execute(sentencia)
    con.commit()
    return con


def marca_de_agua(dw):
    fila = dw.execute("SELECT valor FROM ctl_marca_agua WHERE tabla='oc_linea'").fetchone()
    return fila[0] if fila else None


def _columnas_origen(erp):
    return [f[1] for f in erp.execute("PRAGMA table_info(oc_linea)")]


def _validar_esquema_origen(erp):
    """Devuelve las columnas nuevas (se avisan y se ignoran). Lanza error si falta alguna requerida."""
    actuales = _columnas_origen(erp)
    faltan = [c for c in COLUMNAS_ORIGEN if c not in actuales]
    if faltan:
        raise EsquemaOrigenError(f"faltan columnas en la fuente: {faltan}")
    return [c for c in actuales if c not in COLUMNAS_ORIGEN]


def _valor(v):
    if v is None or (not isinstance(v, str) and pd.isna(v)):
        return None
    return v.strftime("%Y-%m-%d") if isinstance(v, pd.Timestamp) else (v.item() if hasattr(v, "item") else v)


def _filas(df, columnas):
    return [tuple(_valor(v) for v in fila) for fila in df[columnas].itertuples(index=False, name=None)]


def _reconstruir_silver(dw, bronze, lote, regla_defectuosa, parcial=True):
    """Recalcula Silver y cuarentena para las filas dadas (o para todo Bronze). Sin commit: lo gestiona quien llama."""
    if not parcial:
        dw.execute("DELETE FROM slv_oc_linea")
        dw.execute("DELETE FROM slv_oc_linea_cuarentena")
    if bronze.empty:
        return 0, 0
    silver, cuarentena = a_silver(bronze, regla_defectuosa=regla_defectuosa)
    claves = [(int(a), int(b)) for a, b in bronze[["id_oc", "linea"]].itertuples(index=False, name=None)]
    if parcial:
        dw.executemany("DELETE FROM slv_oc_linea WHERE id_oc=? AND linea=?", claves)
        dw.executemany("DELETE FROM slv_oc_linea_cuarentena WHERE id_oc=? AND linea=?", claves)
    cols = ["id_oc", "linea", "id_proveedor", "unidad", "fecha_emision", "fecha_prometida",
            "fecha_recepcion", "cantidad", "lote_carga"]
    dw.executemany("INSERT INTO slv_oc_linea VALUES (?,?,?,?,?,?,?,?,?)", _filas(silver.assign(lote_carga=lote), cols))
    dw.executemany("INSERT INTO slv_oc_linea_cuarentena VALUES (?,?,?,?)",
                   _filas(cuarentena.assign(lote_carga=lote), ["id_oc", "linea", "motivo", "lote_carga"]))
    return len(silver), len(cuarentena)


def _recalcular_gold(dw):
    silver = pd.read_sql_query("SELECT * FROM slv_oc_linea", dw,
                               parse_dates=["fecha_emision", "fecha_prometida", "fecha_recepcion"])
    dw.execute("DELETE FROM gld_otd_proveedor")
    if silver.empty:
        return
    g = a_gold(silver).reset_index().rename(columns={"index": "id_proveedor"})
    dw.executemany("INSERT INTO gld_otd_proveedor VALUES (?,?,?,?,?,?,?)",
                   _filas(g, ["id_proveedor", "vencidas", "a_tiempo", "tarde", "sin_recibir", "otd_ingenuo", "otd_correcto"]))


def _total(dw, tabla):
    return dw.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]


def _registrar(dw, lote, ahora, estado, leidas, pct, alertas, error=None):
    dw.execute("INSERT INTO ctl_corridas VALUES (?,?,?,?,?,?,?,?,?,?)",
               (lote, str(ahora), estado, leidas, _total(dw, "brz_oc_linea"), _total(dw, "slv_oc_linea"),
                _total(dw, "slv_oc_linea_cuarentena"), pct, ",".join(alertas), error))


def ejecutar_corrida(erp, dw, lote, ahora, regla_defectuosa=False, falla_en=None):
    """Una corrida incremental completa. Todo o nada: ante un fallo se revierte y la marca no avanza."""
    marca = marca_de_agua(dw)
    try:
        nuevas = _validar_esquema_origen(erp)
        nuevos = extraer_incremental(erp, marca)
        with dw:                                            # una sola transacción
            if len(nuevos):
                filas = [(*(_valor(v) for v in f), lote)
                         for f in nuevos[COLUMNAS_ORIGEN].itertuples(index=False, name=None)]
                dw.executemany(UPSERT_BRONZE, filas)
            if falla_en == "despues_bronze":
                raise RuntimeError("fallo simulado después de cargar Bronze")
            lote_df = pd.read_sql_query("SELECT * FROM brz_oc_linea WHERE lote_carga=?", dw, params=(lote,))
            n_silver, n_cuar = _reconstruir_silver(dw, lote_df, lote, regla_defectuosa)
            _recalcular_gold(dw)
            nueva_marca = nuevos["fecha_modificacion"].max() if len(nuevos) else marca
            if nueva_marca:
                dw.execute("INSERT OR REPLACE INTO ctl_marca_agua VALUES ('oc_linea', ?)", (nueva_marca,))
            pct = n_cuar / len(lote_df) if len(lote_df) else 0.0
            alertas = metricas_corrida(lote_df, lote_df.iloc[:n_silver] if n_silver else lote_df.iloc[0:0],
                                       lote_df.iloc[:n_cuar] if n_cuar else lote_df.iloc[0:0],
                                       nueva_marca or ahora, ahora)["alertas"]
            if nuevas:
                alertas.append("columnas_nuevas_en_la_fuente")
            _registrar(dw, lote, ahora, "OK", len(nuevos), pct, alertas)
    except Exception as e:                                  # el rollback ya ocurrió al salir del `with`
        with dw:
            _registrar(dw, lote, ahora, "FALLA", 0, 0.0, [], f"{type(e).__name__}: {e}")
        raise
    return {"lote": lote, "estado": "OK", "leidas": len(nuevos), "bronze": _total(dw, "brz_oc_linea"),
            "silver": _total(dw, "slv_oc_linea"), "cuarentena": _total(dw, "slv_oc_linea_cuarentena"),
            "pct_cuarentena": pct, "alertas": alertas, "marca_de_agua": marca_de_agua(dw)}


def reprocesar_silver(dw, lote, ahora, regla_defectuosa=False):
    """Reconstruye Silver, cuarentena y Gold desde Bronze, sin volver a la fuente. Atómico."""
    with dw:
        bronze = pd.read_sql_query("SELECT * FROM brz_oc_linea", dw)
        n_silver, n_cuar = _reconstruir_silver(dw, bronze, lote, regla_defectuosa, parcial=False)
        _recalcular_gold(dw)
        pct = n_cuar / len(bronze) if len(bronze) else 0.0
        _registrar(dw, lote, ahora, "REPROCESO", len(bronze), pct, ["cuarentena"] if pct > 0.01 else [])
    return {"lote": lote, "estado": "REPROCESO", "silver": n_silver, "cuarentena": n_cuar, "pct_cuarentena": pct}


def gold(dw):
    return pd.read_sql_query("SELECT * FROM gld_otd_proveedor ORDER BY id_proveedor", dw).set_index("id_proveedor")
