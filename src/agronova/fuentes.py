"""Fuentes simuladas: un ERP (SQLite) y un archivo de inspecciones de calidad."""
import sqlite3
from datetime import date, timedelta

import pandas as pd

# (proveedor, a tiempo, tarde, abiertas, recepciones rechazadas con cantidad cero)
PLAN = [("A", 190, 8, 2, 10), ("B", 240, 40, 20, 20), ("C", 350, 72, 78, 32)]
COLUMNAS = ["id_oc", "linea", "proveedor", "unidad_txt", "fecha_emision", "fecha_prometida",
            "fecha_recepcion", "cantidad_txt", "fecha_modificacion"]


def generar_lineas() -> pd.DataFrame:
    """1,000 líneas de OC con defectos típicos de un origen real: texto con espacios,
    unidades escritas de varias formas y cantidades con punto de miles."""
    filas, n = [], 0
    for prov, a_tiempo, tarde, abiertas, ceros in PLAN:
        estados = ["a_tiempo"] * a_tiempo + ["tarde"] * tarde + ["abierta"] * abiertas
        vistas = 0
        for estado in estados:
            n += 1
            prometida = date(2026, 9, 1) + timedelta(days=n % 28)
            recibida, cantidad = None, None
            if estado == "a_tiempo":
                recibida = prometida
            elif estado == "tarde":
                recibida = prometida + timedelta(days=1 + n % 5)
            if recibida:
                vistas += 1
                q = 0 if vistas <= ceros else 1000 + 100 * (n % 40)
                cantidad = f"{q:,}".replace(",", ".")
            filas.append((100000 + n, 1, f"PROV {prov} ", ["uni.", "UN ", "kg"][n % 3],
                          (prometida - timedelta(days=10)).isoformat(), prometida.isoformat(),
                          recibida.isoformat() if recibida else None, cantidad,
                          "2026-10-01 05:00:00"))
    return pd.DataFrame(filas, columns=COLUMNAS)


def crear_erp_simulado(lineas=None) -> sqlite3.Connection:
    """Carga las líneas en SQLite. En la vida real sería SQL Server, Oracle, PostgreSQL..."""
    con = sqlite3.connect(":memory:")
    (generar_lineas() if lineas is None else lineas).to_sql("oc_linea", con, index=False)
    return con


def generar_inspecciones() -> pd.DataFrame:
    """100 lotes x 500 unidades = 50,000 inspeccionadas; 15 rechazadas por lote."""
    return pd.DataFrame({"lote": [f"L{i:03d}" for i in range(100)],
                         "unidades_inspeccionadas": 500, "unidades_rechazadas": 15})
