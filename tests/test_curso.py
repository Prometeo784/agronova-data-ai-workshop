import os
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


class PruebasCurso(unittest.TestCase):
    def comprobar(self, modulo, soluciones=False):
        entorno = dict(os.environ)
        entorno.pop("USAR_SOLUCIONES", None)
        if soluciones:
            entorno["USAR_SOLUCIONES"] = "1"
        return subprocess.run([sys.executable, str(RAIZ / "curso" / "checkpoint.py"), modulo],
                              capture_output=True, text=True, env=entorno)

    def test_los_modulos_con_comprobacion_pasan_con_las_soluciones_de_referencia(self):
        for modulo in ("M2", "M3", "M4", "M5", "M6"):
            r = self.comprobar(modulo, soluciones=True)
            self.assertEqual(r.returncode, 0, f"{modulo}\n{r.stdout}\n{r.stderr}")

    def test_un_modulo_inexistente_se_rechaza(self):
        self.assertEqual(self.comprobar("M9").returncode, 2)


if __name__ == "__main__":
    unittest.main()
