import sqlite3
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from agronova.control import reconciliar  # noqa: E402
from agronova.fuentes import crear_erp_simulado, generar_inspecciones  # noqa: E402
from agronova.gold import a_gold, calidad  # noqa: E402
from agronova.ingesta import cargar_bronze, extraer_incremental  # noqa: E402
from agronova.silver import a_silver  # noqa: E402


class PruebasPipeline(unittest.TestCase):
    def setUp(self):
        self.erp = crear_erp_simulado()
        self.bronze = cargar_bronze(pd.DataFrame(), extraer_incremental(self.erp, None), "l1")

    def test_carga_inicial(self):
        self.assertEqual(len(self.bronze), 1000)

    def test_incremental_sin_cambios_no_trae_nada(self):
        marca = self.bronze["fecha_modificacion"].max()
        self.assertEqual(len(extraer_incremental(self.erp, marca)), 0)

    def test_reejecutar_no_duplica_por_clave(self):
        otra = cargar_bronze(self.bronze, extraer_incremental(self.erp, None), "l2")
        self.assertEqual(len(otra), 1000)

    def test_regla_defectuosa_pasa_reconciliacion_pero_dispara_alerta(self):
        silver, cuar = a_silver(self.bronze, regla_defectuosa=True)
        r = reconciliar(self.bronze, silver, cuar)
        self.assertEqual((r["silver"], r["cuarentena"]), (938, 62))
        self.assertTrue(r["reconcilia"])      # los conteos cuadran...
        self.assertTrue(r["alerta"])          # ...pero el umbral delata el problema

    def test_regla_corregida_conserva_recepciones_con_cantidad_cero(self):
        silver, cuar = a_silver(self.bronze)
        self.assertEqual((len(silver), len(cuar)), (1000, 0))

    def test_otd_correcto_frente_a_ingenuo(self):
        silver, _ = a_silver(self.bronze)
        g = a_gold(silver)
        self.assertEqual(g.loc["C", "otd_ingenuo"], 82.9)
        self.assertEqual(g.loc["C", "otd_correcto"], 70.0)
        self.assertEqual(g.loc["Total", "otd_correcto"], 78.0)
        self.assertEqual(int(g.loc["Total", "sin_recibir"]), 100)

    def test_calidad(self):
        self.assertAlmostEqual(calidad(generar_inspecciones())[2], 0.97)

    def test_sql_equivalente_coincide_con_pandas(self):
        silver, _ = a_silver(self.bronze)
        s = silver.copy()
        for col in ["fecha_emision", "fecha_prometida", "fecha_recepcion"]:
            s[col] = s[col].dt.strftime("%Y-%m-%d")
        con = sqlite3.connect(":memory:")
        s[["id_oc", "linea", "id_proveedor", "fecha_prometida", "fecha_recepcion"]].to_sql(
            "slv_oc_linea", con, index=False)
        sql = (RAIZ / "sql" / "02_otd_por_proveedor.sql").read_text(encoding="utf-8")
        filas = con.execute(sql, {"corte": "2026-10-01"}).fetchall()
        g = a_gold(silver)
        for prov, vencidas, a_tiempo, otd in filas:
            self.assertEqual(vencidas, g.loc[prov, "vencidas"])
            self.assertEqual(otd, g.loc[prov, "otd_correcto"])


if __name__ == "__main__":
    unittest.main()
