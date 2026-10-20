"""PLANTILLA (no probada aquí): leer el Excel de inspecciones. Requiere openpyxl."""
import pandas as pd

inspecciones = pd.read_excel("inspecciones.xlsx", sheet_name="Lotes")
# Buenas prácticas: una plantilla con listas desplegables en el origen evita limpiar errores después.
print(inspecciones.head())
