"""Exporta Silver, Gold y la cuarentena a CSV para practicar en Power BI, Fabric o Excel.
Nombres de columna en PascalCase para que coincidan con docs/14_fabric_y_power_bi.md."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
import pandas as pd  # noqa: E402

from agronova.config import CORTE  # noqa: E402
from agronova.fuentes import crear_erp_simulado  # noqa: E402
from agronova.gold import a_gold  # noqa: E402
from agronova.ingesta import cargar_bronze, extraer_incremental  # noqa: E402
from agronova.silver import a_silver  # noqa: E402

destino = RAIZ / "data" / "exportadas"
destino.mkdir(exist_ok=True)
bronze = cargar_bronze(pd.DataFrame(), extraer_incremental(crear_erp_simulado(), None), "export")
silver, _ = a_silver(bronze)
_, cuarentena_mala = a_silver(bronze, regla_defectuosa=True)

s = silver.copy()
s["Recibida"] = s["fecha_recepcion"].notna().astype(int)
s["EsVencida"] = (s["fecha_prometida"] <= CORTE).astype(int)
s["ATiempo"] = (s["Recibida"].eq(1) & (s["fecha_recepcion"] <= s["fecha_prometida"])).astype(int)
s = s.rename(columns={"id_oc": "IdOC", "linea": "Linea", "id_proveedor": "IdProveedor", "unidad": "Unidad",
                      "fecha_emision": "FechaEmision", "fecha_prometida": "FechaPrometida",
                      "fecha_recepcion": "FechaRecepcion", "cantidad": "Cantidad"})
cols = ["IdOC", "Linea", "IdProveedor", "Unidad", "FechaEmision", "FechaPrometida", "FechaRecepcion",
        "Cantidad", "Recibida", "EsVencida", "ATiempo"]
s[cols].to_csv(destino / "slv_oc_linea.csv", index=False, date_format="%Y-%m-%d")
a_gold(silver).reset_index().rename(columns={"id_proveedor": "IdProveedor"}).to_csv(
    destino / "gold_otd_por_proveedor.csv", index=False)
cuarentena_mala[["id_oc", "linea", "proveedor", "cantidad_txt", "motivo"]].to_csv(
    destino / "cuarentena_regla_defectuosa.csv", index=False)
pd.DataFrame({"IdProveedor": ["A", "B", "C"], "Nombre": ["Proveedor A", "Proveedor B", "Proveedor C"]}).to_csv(
    destino / "dim_proveedor.csv", index=False)
print("Exportado en", destino)
