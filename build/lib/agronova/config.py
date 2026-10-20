"""Parámetros del caso. Todo es SIMULADO."""
import pandas as pd

CORTE = pd.Timestamp("2026-10-01")   # fecha de corte del periodo analizado
UMBRAL_CUARENTENA = 0.01             # ejemplo: alertar si más del 1 % va a cuarentena
CLAVE = ["id_oc", "linea"]           # clave de negocio de una línea de orden de compra
UNIDADES = {"UN": "UN", "UNI": "UN", "KG": "KG"}
