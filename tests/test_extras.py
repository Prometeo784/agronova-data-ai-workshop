import json
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from agronova.contrato import validar_contrato  # noqa: E402
from agronova.control import reconciliar  # noqa: E402
from agronova.fuentes import crear_erp_simulado, generar_inspecciones  # noqa: E402
from agronova.gold import a_gold, calidad  # noqa: E402
from agronova.ingesta import cargar_bronze, extraer_incremental  # noqa: E402
from agronova.observabilidad import metricas_corrida  # noqa: E402
from agronova.silver import a_silver  # noqa: E402
from agronova.valor import calcular_valor  # noqa: E402

CIFRAS = json.loads((RAIZ / "data" / "cifras_canonicas.json").read_text(encoding="utf-8"))


class PruebasExtras(unittest.TestCase):
    def setUp(self):
        self.bronze = cargar_bronze(pd.DataFrame(), extraer_incremental(crear_erp_simulado(), None), "l1")
        self.silver, self.cuar = a_silver(self.bronze)

    # ---- contrato de datos
    def test_silver_cumple_el_contrato(self):
        self.assertEqual(validar_contrato(self.silver), [])

    def test_contrato_detecta_unidad_invalida(self):
        malo = self.silver.copy()
        malo.loc[0, "unidad"] = "CAJA"
        self.assertEqual(validar_contrato(malo)[0]["regla"], "unidad_valida")

    def test_contrato_detecta_columna_faltante(self):
        self.assertEqual(validar_contrato(self.silver.drop(columns=["unidad"]))[0]["regla"], "columnas_obligatorias")

    def test_contrato_detecta_cantidad_negativa(self):
        malo = self.silver.copy()
        malo.loc[0, "cantidad"] = -5
        self.assertIn("cantidad_minima", [v["regla"] for v in validar_contrato(malo)])

    # ---- observabilidad
    def test_corrida_sana_sin_alertas(self):
        m = metricas_corrida(self.bronze, self.silver, self.cuar, "2026-10-01 05:00:00", "2026-10-01 11:00:00")
        self.assertEqual((m["frescura_horas"], m["alertas"]), (6.0, []))

    def test_datos_viejos_alertan_por_frescura(self):
        m = metricas_corrida(self.bronze, self.silver, self.cuar, "2026-10-01 05:00:00", "2026-10-03 05:00:00")
        self.assertIn("frescura", m["alertas"])

    def test_regla_defectuosa_alerta_por_cuarentena(self):
        s, c = a_silver(self.bronze, regla_defectuosa=True)
        m = metricas_corrida(self.bronze, s, c, "2026-10-01 05:00:00", "2026-10-01 11:00:00")
        self.assertEqual(m["alertas"], ["cuarentena"])

    # ---- sincronía con las cifras canónicas (evita que el código y los documentos se desalineen)
    def test_otd_coincide_con_las_cifras_canonicas(self):
        g = a_gold(self.silver)
        for prov, esperado in CIFRAS["otd_correcto"].items():
            self.assertEqual(g.loc[prov, "otd_correcto"], esperado)
        for prov, esperado in CIFRAS["otd_ingenuo"].items():
            self.assertEqual(g.loc[prov, "otd_ingenuo"], esperado)

    def test_regla_defectuosa_coincide_con_las_cifras_canonicas(self):
        s, c = a_silver(self.bronze, regla_defectuosa=True)
        r = reconciliar(self.bronze, s, c)
        esperado = CIFRAS["regla_defectuosa"]
        self.assertEqual((r["bronze"], r["silver"], r["cuarentena"]), (esperado["bronze"], esperado["silver"], esperado["cuarentena"]))
        self.assertAlmostEqual(r["pct_cuarentena"], esperado["pct_cuarentena"])

    def test_calidad_coincide(self):
        self.assertAlmostEqual(calidad(generar_inspecciones())[2], CIFRAS["quality_yield"])

    def test_valor_coincide_con_las_cifras_canonicas(self):
        v = calcular_valor()
        for clave, esperado in CIFRAS["valor"].items():
            self.assertAlmostEqual(v[clave], esperado, places=2)
        self.assertFalse(v["capital_cubre_operacion"])    # 4,800 < 6,000: sin los paros no se paga

    # ---- exportaciones para Power BI
    def test_exportacion_reproduce_el_otd(self):
        d = pd.read_csv(RAIZ / "data" / "exportadas" / "slv_oc_linea.csv")
        g = d[d["EsVencida"] == 1].groupby("IdProveedor").agg(v=("IdOC", "size"), a=("ATiempo", "sum"))
        self.assertEqual(round(100 * g.loc["C", "a"] / g.loc["C", "v"], 1), CIFRAS["otd_correcto"]["C"])


if __name__ == "__main__":
    unittest.main()
