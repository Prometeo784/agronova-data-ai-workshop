"""Genera los CSV de ejemplo (para abrirlos en Excel, Power BI, Fabric, etc.)."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from agronova.fuentes import generar_inspecciones, generar_lineas  # noqa: E402

destino = RAIZ / "data"
generar_lineas().to_csv(destino / "erp_oc_linea.csv", index=False, encoding="utf-8")
generar_inspecciones().to_csv(destino / "inspecciones.csv", index=False, encoding="utf-8")
print("Archivos generados en", destino)
