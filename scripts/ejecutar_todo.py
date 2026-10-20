"""Ejecuta, en orden, todo lo ejecutable del repositorio y resume el resultado.  python scripts/ejecutar_todo.py"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PASOS = [("Pipeline de punta a punta", ["scripts/ejecutar_pipeline.py"]),
         ("Evaluación del recuperador", ["scripts/evaluar_rag.py"]),
         ("Exportación para Power BI", ["scripts/exportar_capas.py"]),
         ("Simulación de 6 días", ["scripts/simular_plataforma.py", "--dias", "6"]),
         ("Pruebas", ["-m", "unittest", "discover", "-s", "tests"])]
resumen = []
for nombre, args in PASOS:
    r = subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True)
    resumen.append((nombre, r.returncode == 0))
    print(f"{'OK ' if r.returncode == 0 else 'FALLA'}  {nombre}")
    if r.returncode != 0:
        print(r.stdout[-800:], r.stderr[-800:])
sys.exit(0 if all(ok for _, ok in resumen) else 1)
