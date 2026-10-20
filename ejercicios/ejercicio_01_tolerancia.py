"""Ejercicio 1. Compras acepta un día de tolerancia: una entrega cuenta como a tiempo si llega
hasta `dias` días después de la fecha prometida. El denominador sigue siendo TODAS las líneas vencidas.

Completa la función. Debe devolver una serie con el OTD en % (un decimal) por proveedor."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agronova.config import CORTE  # noqa: E402,F401


def otd_con_tolerancia(silver, dias=1, corte=CORTE):
    raise NotImplementedError("Completa este ejercicio")
