import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from agronova.fuentes import crear_erp_simulado  # noqa: E402
from agronova.plataforma import (EsquemaOrigenError, abrir, ejecutar_corrida, gold,  # noqa: E402
                                 marca_de_agua, reprocesar_silver)
from agronova.simulador import ahora_simulado, avanzar_dia  # noqa: E402

CIFRAS = json.loads((RAIZ / "data" / "cifras_canonicas.json").read_text(encoding="utf-8"))


def tabla(dw, nombre, orden):
    return dw.execute(f"SELECT * FROM {nombre} ORDER BY {orden}").fetchall()


def estado(dw):
    """Instantánea comparable del estado (sin el lote, que cambia en cada corrida)."""
    silver = [f[:-1] for f in tabla(dw, "slv_oc_linea", "id_oc, linea")]
    cuar = [f[:-1] for f in tabla(dw, "slv_oc_linea_cuarentena", "id_oc, linea")]
    return silver, cuar, tabla(dw, "gld_otd_proveedor", "id_proveedor"), marca_de_agua(dw)


class PruebasPlataforma(unittest.TestCase):
    def setUp(self):
        self.erp, self.dw = crear_erp_simulado(), abrir()

    def corrida(self, dia, **kw):
        if dia > 1:
            avanzar_dia(self.erp, dia)
        return ejecutar_corrida(self.erp, self.dw, f"dia-{dia}", ahora_simulado(dia), **kw)

    def test_carga_inicial_reproduce_las_cifras_canonicas(self):
        r = self.corrida(1)
        self.assertEqual((r["bronze"], r["silver"], r["cuarentena"]), (1000, 1000, 0))
        g = gold(self.dw)
        for prov, esperado in CIFRAS["otd_correcto"].items():
            self.assertEqual(g.loc[prov, "otd_correcto"], esperado)

    def test_segunda_corrida_sin_cambios_no_lee_nada(self):
        self.corrida(1)
        r = ejecutar_corrida(self.erp, self.dw, "repeticion", ahora_simulado(1))
        self.assertEqual(r["leidas"], 0)
        self.assertEqual(r["bronze"], 1000)

    def test_evolucion_diaria_incremental(self):
        self.assertEqual(self.corrida(1)["bronze"], 1000)
        r2 = self.corrida(2)
        self.assertEqual((r2["leidas"], r2["bronze"]), (50, 1020))        # 30 actualizadas + 20 nuevas
        r3 = self.corrida(3)
        self.assertEqual((r3["leidas"], r3["bronze"]), (5, 1020))         # corrección tardía: actualiza, no duplica
        corregidas = self.dw.execute("SELECT COUNT(*) FROM slv_oc_linea WHERE cantidad=250").fetchone()[0]
        self.assertEqual(corregidas, 5)

    def test_columna_nueva_se_avisa_y_no_detiene(self):
        for d in (1, 2, 3):
            self.corrida(d)
        r = self.corrida(4)
        self.assertIn("columnas_nuevas_en_la_fuente", r["alertas"])
        self.assertEqual(r["bronze"], 1030)

    def test_cambio_que_rompe_el_contrato_falla_sin_tocar_el_estado(self):
        for d in (1, 2, 3, 4):
            self.corrida(d)
        antes = estado(self.dw)
        with self.assertRaises(EsquemaOrigenError):
            self.corrida(5)
        self.assertEqual(estado(self.dw), antes)
        ultimo = self.dw.execute("SELECT estado FROM ctl_corridas ORDER BY rowid DESC LIMIT 1").fetchone()[0]
        self.assertEqual(ultimo, "FALLA")
        r6 = self.corrida(6)                                              # la fuente se restaura: se recupera
        self.assertEqual((r6["estado"], r6["bronze"]), ("OK", 1035))

    def test_un_fallo_a_mitad_revierte_todo_y_la_marca_no_avanza(self):
        self.corrida(1)
        avanzar_dia(self.erp, 2)
        antes = estado(self.dw)
        with self.assertRaises(RuntimeError):
            ejecutar_corrida(self.erp, self.dw, "dia-2", ahora_simulado(2), falla_en="despues_bronze")
        self.assertEqual(estado(self.dw), antes)
        self.assertEqual(self.dw.execute("SELECT COUNT(*) FROM brz_oc_linea").fetchone()[0], 1000)
        r = ejecutar_corrida(self.erp, self.dw, "dia-2-reintento", ahora_simulado(2))   # el reintento sí carga
        self.assertEqual((r["leidas"], r["bronze"]), (50, 1020))

    def test_reiniciar_la_marca_y_repetir_deja_el_mismo_estado(self):
        for d in (1, 2):
            self.corrida(d)
        antes = estado(self.dw)
        self.dw.execute("DELETE FROM ctl_marca_agua")
        self.dw.commit()
        r = ejecutar_corrida(self.erp, self.dw, "recarga", ahora_simulado(2))
        self.assertEqual(r["leidas"], 1020)                               # releyó todo
        self.assertEqual(estado(self.dw), antes)                          # y el estado es idéntico

    def test_reprocesar_corrige_una_regla_defectuosa_sin_volver_a_la_fuente(self):
        r = self.corrida(1, regla_defectuosa=True)
        self.assertEqual((r["silver"], r["cuarentena"]), (938, 62))
        self.assertIn("cuarentena", r["alertas"])
        rp = reprocesar_silver(self.dw, "reproceso", ahora_simulado(1))
        self.assertEqual((rp["silver"], rp["cuarentena"]), (1000, 0))
        g = gold(self.dw)
        for prov, esperado in CIFRAS["otd_correcto"].items():
            self.assertEqual(g.loc[prov, "otd_correcto"], esperado)

    def test_datos_viejos_alertan_por_frescura(self):
        r = ejecutar_corrida(self.erp, self.dw, "tarde", pd.Timestamp("2026-10-05 06:00:00"))
        self.assertIn("frescura", r["alertas"])

    def test_el_estado_persiste_entre_conexiones(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "estado.db")
            dw = abrir(ruta)
            ejecutar_corrida(self.erp, dw, "dia-1", ahora_simulado(1))
            dw.close()
            dw2 = abrir(ruta)
            self.assertEqual(marca_de_agua(dw2), "2026-10-01 05:00:00")
            r = ejecutar_corrida(self.erp, dw2, "dia-1b", ahora_simulado(1))
            self.assertEqual((r["leidas"], r["bronze"]), (0, 1000))
            dw2.close()


if __name__ == "__main__":
    unittest.main()
