"""PLANTILLA (no probada aquí): extracción incremental desde un ERP o base SQL.
Requiere: pandas, sqlalchemy y el controlador de tu motor (p. ej. pyodbc para SQL Server).
Las credenciales NUNCA van en el código: variables de entorno o un gestor de secretos."""
import os

import pandas as pd
from sqlalchemy import create_engine, text

# Formato de ejemplo: "mssql+pyodbc://usuario:clave@servidor/base?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(os.environ["ERP_DB_URL"])

marca = "2026-10-01 05:00:00"   # última carga exitosa (guárdala en una tabla de control)
consulta = text("SELECT * FROM oc_linea WHERE fecha_modificacion > :marca")
df = pd.read_sql_query(consulta, engine, params={"marca": marca})
print(f"{len(df):,} filas nuevas o modificadas")
