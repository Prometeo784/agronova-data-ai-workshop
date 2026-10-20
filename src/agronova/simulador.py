"""Simula la evolución del ERP día a día para ver cargas incrementales, correcciones tardías y cambios de esquema.
Todos los datos son SINTÉTICOS."""
import pandas as pd

COLUMNAS = "id_oc, linea, proveedor, unidad_txt, fecha_emision, fecha_prometida, fecha_recepcion, cantidad_txt, fecha_modificacion"

DESCRIPCIONES = {
    1: "Carga inicial: 1,000 líneas",
    2: "30 líneas abiertas se reciben (tarde) y llegan 20 líneas nuevas",
    3: "Corrección tardía: 5 recepciones con cantidad cero se corrigen",
    4: "El ERP agrega una columna nueva (se avisa y se ignora) y llegan 10 líneas",
    5: "Cambio que rompe el contrato: se renombra una columna requerida (la carga debe fallar)",
    6: "Se restaura la columna y llegan 5 líneas: la carga se recupera",
}


def ahora_simulado(dia):
    return pd.Timestamp(f"2026-10-{dia:02d} 06:00:00")


def _nuevas(c, desde, n, prov, dia):
    c.executemany(f"INSERT INTO oc_linea ({COLUMNAS}) VALUES (?,?,?,?,?,?,?,?,?)",
                  [(desde + i, 1, f"PROV {prov} ", "UN ", "2026-09-30", "2026-10-10", None, None,
                    f"2026-10-{dia:02d} 05:00:00") for i in range(n)])


def avanzar_dia(erp, dia):
    """Modifica el ERP simulado como lo haría un día de operación."""
    c = erp.cursor()
    sello = f"2026-10-{dia:02d} 05:00:00"
    if dia == 2:
        ids = [r[0] for r in c.execute("SELECT id_oc FROM oc_linea WHERE fecha_recepcion IS NULL ORDER BY id_oc LIMIT 30")]
        c.executemany("UPDATE oc_linea SET fecha_recepcion='2026-10-02', cantidad_txt='1.200', fecha_modificacion=? WHERE id_oc=?",
                      [(sello, i) for i in ids])
        _nuevas(c, 200001, 20, "A", dia)
    elif dia == 3:
        ids = [r[0] for r in c.execute("SELECT id_oc FROM oc_linea WHERE cantidad_txt='0' ORDER BY id_oc LIMIT 5")]
        c.executemany("UPDATE oc_linea SET cantidad_txt='250', fecha_modificacion=? WHERE id_oc=?", [(sello, i) for i in ids])
    elif dia == 4:
        c.execute("ALTER TABLE oc_linea ADD COLUMN comentario TEXT")
        _nuevas(c, 200101, 10, "B", dia)
    elif dia == 5:
        c.execute("ALTER TABLE oc_linea RENAME COLUMN unidad_txt TO unidad")
    elif dia == 6:
        c.execute("ALTER TABLE oc_linea RENAME COLUMN unidad TO unidad_txt")
        _nuevas(c, 200201, 5, "C", dia)
    erp.commit()
