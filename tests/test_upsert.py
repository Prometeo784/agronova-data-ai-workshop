import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agronova.fuentes import generar_lineas  # noqa: E402
from agronova.upsert import upsert_bronze  # noqa: E402


def contar(con):
    return con.execute("SELECT COUNT(*) FROM brz_oc_linea").fetchone()[0]


class PruebasUpsert(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(":memory:")
        self.df = generar_lineas()

    def test_ejecutar_dos_veces_deja_el_mismo_estado(self):
        upsert_bronze(self.con, self.df, "l1")
        antes = self.con.execute("SELECT * FROM brz_oc_linea ORDER BY id_oc").fetchall()
        upsert_bronze(self.con, self.df, "l1")
        despues = self.con.execute("SELECT * FROM brz_oc_linea ORDER BY id_oc").fetchall()
        self.assertEqual(contar(self.con), 1000)
        self.assertEqual(antes, despues)

    def test_un_cambio_en_el_origen_actualiza_sin_duplicar(self):
        upsert_bronze(self.con, self.df, "l1")
        cambio = self.df.copy()
        i = cambio.index[cambio["fecha_recepcion"].isna()][0]
        cambio.loc[i, "fecha_recepcion"] = "2026-09-30"
        cambio.loc[i, "fecha_modificacion"] = "2026-10-02 05:00:00"
        upsert_bronze(self.con, cambio, "l2")
        self.assertEqual(contar(self.con), 1000)
        fila = self.con.execute("SELECT fecha_recepcion, lote_carga FROM brz_oc_linea WHERE id_oc=?",
                                (int(cambio.loc[i, "id_oc"]),)).fetchone()
        self.assertEqual(fila, ("2026-09-30", "l2"))

    def test_un_dato_mas_antiguo_no_pisa_a_uno_mas_reciente(self):
        upsert_bronze(self.con, self.df, "l1")
        viejo = self.df.copy()
        viejo["fecha_modificacion"] = "2026-09-01 00:00:00"
        viejo["proveedor"] = "CAMBIADO"
        upsert_bronze(self.con, viejo, "l0")
        self.assertEqual(self.con.execute(
            "SELECT COUNT(*) FROM brz_oc_linea WHERE proveedor='CAMBIADO'").fetchone()[0], 0)

    def test_fallo_a_mitad_de_la_carga_no_deja_datos_a_medias(self):
        upsert_bronze(self.con, self.df.iloc[:10], "l1")
        roto = self.df.iloc[10:20].copy()
        roto.iloc[5, roto.columns.get_loc("id_oc")] = None     # viola NOT NULL
        with self.assertRaises(sqlite3.IntegrityError):
            upsert_bronze(self.con, roto, "l2")
        self.assertEqual(contar(self.con), 10)                 # nada de l2 quedó escrito


if __name__ == "__main__":
    unittest.main()
