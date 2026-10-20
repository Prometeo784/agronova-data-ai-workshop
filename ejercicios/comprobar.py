"""Comprueba las funciones de los ejercicios. USAR_SOLUCIONES=1 usa las soluciones de referencia."""
import importlib.util
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "src"))
import pandas as pd  # noqa: E402

from agronova.fuentes import crear_erp_simulado  # noqa: E402
from agronova.ingesta import cargar_bronze, extraer_incremental  # noqa: E402
from agronova.silver import a_silver  # noqa: E402


def cargar(nombre_ejercicio, nombre_solucion):
    ruta = (AQUI / "soluciones" / nombre_solucion) if os.environ.get("USAR_SOLUCIONES") else (AQUI / nombre_ejercicio)
    spec = importlib.util.spec_from_file_location(ruta.stem, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def intentar(nombre, comprobacion):
    try:
        comprobacion()
        print(f"OK         {nombre}")
        return True
    except NotImplementedError:
        print(f"PENDIENTE  {nombre}")
    except AssertionError as e:
        print(f"FALLA      {nombre}: {e}")
    return False


silver, _ = a_silver(cargar_bronze(pd.DataFrame(), extraer_incremental(crear_erp_simulado(), None), "e"))


def c1():
    f = cargar("ejercicio_01_tolerancia.py", "solucion_01.py").otd_con_tolerancia
    r = f(silver, 1)
    esperado = {"A": 95.5, "B": 82.7, "C": 72.8}
    for prov, v in esperado.items():
        assert round(float(r[prov]), 1) == v, f"proveedor {prov}: {r[prov]} en lugar de {v}"
    assert round(float(f(silver, 0)["C"]), 1) == 70.0, "con 0 días de tolerancia el OTD de C debe ser 70.0"


def c2():
    f = cargar("ejercicio_02_alerta_volumen.py", "solucion_02.py").alerta_volumen
    assert f(400, [1000, 1010, 990]) is True, "400 filas debe alertar"
    assert f(1020, [1000, 1010, 990]) is False, "1020 filas no debe alertar"
    assert f(2000, [1000, 1010, 990]) is True, "2000 filas debe alertar"


def c3():
    f = cargar("ejercicio_03_proveedores_validos.py", "solucion_03.py").validar_proveedores
    assert f(silver, ["A", "B", "C"]) == [], "con A, B y C no debe haber violaciones"
    r = f(silver, ["A", "B"])
    assert r and r[0]["regla"] == "proveedor_valido" and r[0]["detalle"] == ["C"] and r[0]["filas"] == 500, f"resultado: {r}"


resultados = [intentar("Ejercicio 1: tolerancia", c1), intentar("Ejercicio 2: alerta por volumen", c2),
              intentar("Ejercicio 3: proveedores válidos", c3)]
sys.exit(0 if all(resultados) else 1)
