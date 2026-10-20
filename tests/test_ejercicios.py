import os
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


class PruebasEjercicios(unittest.TestCase):
    def ejecutar(self, usar_soluciones):
        entorno = dict(os.environ)
        entorno.pop("USAR_SOLUCIONES", None)
        if usar_soluciones:
            entorno["USAR_SOLUCIONES"] = "1"
        return subprocess.run([sys.executable, str(RAIZ / "ejercicios" / "comprobar.py")],
                              capture_output=True, text=True, env=entorno)

    def test_las_soluciones_de_referencia_pasan(self):
        r = self.ejecutar(True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(r.stdout.count("OK "), 3)

    def test_los_ejercicios_sin_completar_figuran_como_pendientes(self):
        r = self.ejecutar(False)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout.count("PENDIENTE"), 3)


if __name__ == "__main__":
    unittest.main()
