"""Comprobaciones de los módulos del curso.   python curso/checkpoint.py M3"""
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
UNITTEST = {
    "M2": ["tests.test_pipeline"],
    "M3": ["tests.test_upsert", "tests.test_plataforma", "tests.test_extras.PruebasExtras.test_silver_cumple_el_contrato",
           "tests.test_extras.PruebasExtras.test_regla_defectuosa_alerta_por_cuarentena"],
    "M4": ["tests.test_extras.PruebasExtras.test_exportacion_reproduce_el_otd",
           "tests.test_extras.PruebasExtras.test_otd_coincide_con_las_cifras_canonicas"],
    "M5": ["tests.test_rag"],
    "M6": ["tests.test_extras.PruebasExtras.test_valor_coincide_con_las_cifras_canonicas"],
}
EJERCICIOS = {"M3": True, "M4": True}   # módulos que también comprueban los ejercicios


def main():
    modulo = (sys.argv[1] if len(sys.argv) > 1 else "").upper()
    if modulo not in UNITTEST:
        print("Uso: python curso/checkpoint.py M2|M3|M4|M5|M6   (M1 se comprueba con docs/15_autoevaluacion.md)")
        return 2
    resultados = []
    r = subprocess.run([sys.executable, "-m", "unittest", *UNITTEST[modulo]], cwd=RAIZ, capture_output=True, text=True)
    print(("PASA   " if r.returncode == 0 else "FALLA  ") + f"{modulo}: pruebas ({len(UNITTEST[modulo])} grupos)")
    if r.returncode != 0:
        print(r.stderr[-1500:])
    resultados.append(r.returncode == 0)
    if EJERCICIOS.get(modulo):
        e = subprocess.run([sys.executable, "ejercicios/comprobar.py"], cwd=RAIZ, capture_output=True, text=True, env=dict(os.environ))
        print(e.stdout.rstrip())
        resultados.append(e.returncode == 0)
    return 0 if all(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())
