"""Carga idempotente con UPSERT atómico (SQLite). Ilustra el principio; NO es código de producción.

Diferencias que conviene distinguir:
  * Eliminar duplicados en un DataFrame (ingesta.cargar_bronze): limpia filas repetidas en memoria.
  * Carga idempotente: ejecutar el MISMO proceso varias veces deja el MISMO estado en el destino.
    Aquí se logra con una clave primaria y un UPSERT (INSERT ... ON CONFLICT DO UPDATE).
  * Atomicidad: si falla a mitad de la carga, no queda nada a medias (todo o nada).
"""
import sqlite3

COLUMNAS = ["id_oc", "linea", "proveedor", "unidad_txt", "fecha_emision", "fecha_prometida",
            "fecha_recepcion", "cantidad_txt", "fecha_modificacion"]

DDL = """CREATE TABLE IF NOT EXISTS brz_oc_linea (
    id_oc INTEGER NOT NULL, linea INTEGER NOT NULL, proveedor TEXT, unidad_txt TEXT,
    fecha_emision TEXT, fecha_prometida TEXT, fecha_recepcion TEXT, cantidad_txt TEXT,
    fecha_modificacion TEXT, lote_carga TEXT,
    PRIMARY KEY (id_oc, linea))"""

UPSERT = f"""INSERT INTO brz_oc_linea ({", ".join(COLUMNAS)}, lote_carga)
VALUES ({", ".join("?" * (len(COLUMNAS) + 1))})
ON CONFLICT (id_oc, linea) DO UPDATE SET
    {", ".join(f"{c} = excluded.{c}" for c in COLUMNAS[2:])}, lote_carga = excluded.lote_carga
WHERE excluded.fecha_modificacion >= brz_oc_linea.fecha_modificacion"""


def upsert_bronze(con: sqlite3.Connection, df, lote: str) -> None:
    """Todo o nada: `with con` hace commit si termina bien y rollback si hay una excepción."""
    con.execute(DDL)
    filas = [(*(None if v != v else v for v in fila), lote)
             for fila in df[COLUMNAS].itertuples(index=False, name=None)]
    with con:
        con.executemany(UPSERT, filas)
