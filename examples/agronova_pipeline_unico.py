"""
AgroNova (EMPRESA FICTICIA): pipeline didáctico de punta a punta.
Todos los datos son SIMULADOS. Requiere Python 3.9+ y pandas. No necesita cuentas ni red.

Flujo:  ERP (SQL) -> ingesta incremental -> Bronze -> Silver (+ cuarentena)
        -> reconciliación y alerta -> Gold (KPI)
"""
import io
import sqlite3
from datetime import date, timedelta

import pandas as pd

CORTE = pd.Timestamp("2026-10-01")   # fecha de corte del periodo
UMBRAL_CUARENTENA = 0.01             # ejemplo: alerta si más del 1 % va a cuarentena
CLAVE = ["id_oc", "linea"]
UNIDADES = {"UN": "UN", "UNI": "UN", "KG": "KG"}


# ---------------------------------------------------------------- 1. FUENTES
def crear_erp_simulado() -> sqlite3.Connection:
    """Simula el ERP con SQLite. En la vida real sería SQL Server, Oracle, etc."""
    # (proveedor, a tiempo, tarde, abiertas, recepciones con cantidad cero)
    plan = [("A", 190, 8, 2, 10), ("B", 240, 40, 20, 20), ("C", 350, 72, 78, 32)]
    filas, n = [], 0
    for prov, a_tiempo, tarde, abiertas, ceros in plan:
        estados = ["a_tiempo"] * a_tiempo + ["tarde"] * tarde + ["abierta"] * abiertas
        recibidas_vistas = 0
        for i, estado in enumerate(estados):
            n += 1
            prometida = date(2026, 9, 1) + timedelta(days=n % 28)
            recibida = None
            if estado == "a_tiempo":
                recibida = prometida
            elif estado == "tarde":
                recibida = prometida + timedelta(days=1 + n % 5)
            cantidad = None
            if recibida:
                recibidas_vistas += 1
                q = 0 if recibidas_vistas <= ceros else 1000 + 100 * (n % 40)
                cantidad = f"{q:,}".replace(",", ".")          # formato "5.000"
            filas.append((
                100000 + n, 1, f"PROV {prov} ", ["uni.", "UN ", "kg"][n % 3],
                (prometida - timedelta(days=10)).isoformat(), prometida.isoformat(),
                recibida.isoformat() if recibida else None, cantidad,
                "2026-10-01 05:00:00",
            ))
    con = sqlite3.connect(":memory:")
    con.execute("""CREATE TABLE oc_linea (id_oc INT, linea INT, proveedor TEXT, unidad_txt TEXT,
                   fecha_emision TEXT, fecha_prometida TEXT, fecha_recepcion TEXT,
                   cantidad_txt TEXT, fecha_modificacion TEXT)""")
    con.executemany("INSERT INTO oc_linea VALUES (?,?,?,?,?,?,?,?,?)", filas)
    return con


INSPECCIONES_CSV = "lote,unidades_inspeccionadas,unidades_rechazadas\n" + "\n".join(
    f"L{i:03d},500,15" for i in range(100))   # 100 lotes x 500 = 50,000 unidades


# --------------------------------------------------- 2. INGESTA INCREMENTAL
def extraer_incremental(con, marca_de_agua):
    """Trae solo lo modificado después de la marca de agua (carga incremental)."""
    sql = "SELECT * FROM oc_linea"
    params = ()
    if marca_de_agua:
        sql += " WHERE fecha_modificacion > ?"
        params = (marca_de_agua,)
    return pd.read_sql_query(sql, con, params=params)


def cargar_bronze(bronze, nuevos, lote):
    """Bronze: copia fiel + trazabilidad. Idempotente: re-ejecutar no duplica."""
    nuevos = nuevos.assign(lote_carga=lote, fecha_carga=pd.Timestamp.now())
    combinado = pd.concat([bronze, nuevos], ignore_index=True)
    return combinado.drop_duplicates(subset=CLAVE, keep="last").reset_index(drop=True)


# ------------------------------------------------------------------ 3. SILVER
def a_silver(bronze, regla_defectuosa=False):
    """Limpia, tipa y valida. Lo que no pasa va a cuarentena con su motivo."""
    df = bronze.copy()
    df["id_proveedor"] = df["proveedor"].str.strip().str.replace("PROV ", "", regex=False)
    df["unidad"] = (df["unidad_txt"].str.strip().str.upper()
                    .str.replace(".", "", regex=False).map(UNIDADES))
    df["cantidad"] = pd.to_numeric(
        df["cantidad_txt"].str.replace(".", "", regex=False), errors="coerce")
    for col in ["fecha_emision", "fecha_prometida", "fecha_recepcion"]:
        df[col] = pd.to_datetime(df[col])

    recibida = df["fecha_recepcion"].notna()
    motivo = pd.Series("", index=df.index)
    motivo[df["id_proveedor"].eq("")] = "proveedor_nulo"
    motivo[recibida & (df["fecha_recepcion"] < df["fecha_emision"])] = "fecha_incoherente"
    motivo[df["unidad"].isna()] = "unidad_desconocida"
    motivo[recibida & (df["cantidad"].isna() | (df["cantidad"] < 0))] = "cantidad_invalida"
    if regla_defectuosa:
        # Error típico: una recepción rechazada o parcial puede tener cantidad cero y ser válida.
        motivo[recibida & (df["cantidad"] <= 0)] = "cantidad_cero (regla defectuosa)"

    silver = df[motivo.eq("")].drop(columns=["proveedor", "unidad_txt", "cantidad_txt"])
    cuarentena = df[motivo.ne("")].assign(motivo=motivo[motivo.ne("")])
    return silver.reset_index(drop=True), cuarentena.reset_index(drop=True)


# ---------------------------------------------------- 4. RECONCILIACIÓN Y ALERTA
def reconciliar(bronze, silver, cuarentena):
    ok = len(bronze) == len(silver) + len(cuarentena)
    pct = len(cuarentena) / len(bronze)
    print(f"  Bronze {len(bronze):,} | Silver {len(silver):,} | Cuarentena {len(cuarentena):,}"
          f" ({pct:.1%})  reconcilia: {'sí' if ok else 'NO'}")
    if pct > UMBRAL_CUARENTENA:
        print(f"  ALERTA: la cuarentena supera el umbral de {UMBRAL_CUARENTENA:.0%}."
              " El proceso terminó sin errores, pero el dato puede estar mal.")
    return ok


# -------------------------------------------------------------------- 5. GOLD
def a_gold(silver):
    """Gold: el KPI se define UNA sola vez. OTD = a tiempo / TODAS las líneas vencidas."""
    s = silver[silver["fecha_prometida"] <= CORTE].copy()
    s["recibida"] = s["fecha_recepcion"].notna()
    s["a_tiempo"] = s["recibida"] & (s["fecha_recepcion"] <= s["fecha_prometida"])
    g = s.groupby("id_proveedor").agg(
        vencidas=("id_oc", "size"), a_tiempo=("a_tiempo", "sum"), recibidas=("recibida", "sum"))
    g["tarde"] = g["recibidas"] - g["a_tiempo"]
    g["sin_recibir"] = g["vencidas"] - g["recibidas"]
    g["otd_ingenuo"] = (g["a_tiempo"] / g["recibidas"] * 100).round(1)
    g["otd_correcto"] = (g["a_tiempo"] / g["vencidas"] * 100).round(1)
    total = g[["vencidas", "a_tiempo", "recibidas", "tarde", "sin_recibir"]].sum()
    g.loc["Total"] = [*total[["vencidas", "a_tiempo", "recibidas", "tarde", "sin_recibir"]],
                      round(total["a_tiempo"] / total["recibidas"] * 100, 1),
                      round(total["a_tiempo"] / total["vencidas"] * 100, 1)]
    cuentas = ["vencidas", "a_tiempo", "tarde", "sin_recibir"]
    g[cuentas] = g[cuentas].astype(int)
    return g[cuentas + ["otd_ingenuo", "otd_correcto"]]


def calidad(csv_texto):
    """Excel/CSV de inspecciones. En la práctica: pd.read_excel('inspecciones.xlsx')."""
    d = pd.read_csv(io.StringIO(csv_texto))
    inspeccionadas = d["unidades_inspeccionadas"].sum()
    aceptadas = inspeccionadas - d["unidades_rechazadas"].sum()
    return aceptadas, inspeccionadas, aceptadas / inspeccionadas


# ------------------------------------------------------------------ EJECUCIÓN
if __name__ == "__main__":
    erp = crear_erp_simulado()
    bronze = pd.DataFrame()

    print("1) Carga inicial (sin marca de agua)")
    nuevos = extraer_incremental(erp, None)
    bronze = cargar_bronze(bronze, nuevos, "lote-001")
    marca = nuevos["fecha_modificacion"].max()
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,} | marca de agua {marca}")

    print("2) Segunda corrida: nada cambió en el ERP")
    nuevos = extraer_incremental(erp, marca)
    bronze = cargar_bronze(bronze, nuevos, "lote-002")
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,}")

    print("3) Re-ejecución con la marca reiniciada (idempotencia)")
    nuevos = extraer_incremental(erp, None)
    bronze = cargar_bronze(bronze, nuevos, "lote-003")
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,}  (sin duplicados)")

    print("4) Silver con la regla DEFECTUOSA (pipeline verde, dato incorrecto)")
    silver_mal, cuar_mal = a_silver(bronze, regla_defectuosa=True)
    reconciliar(bronze, silver_mal, cuar_mal)

    print("5) Silver con la regla CORREGIDA")
    silver, cuarentena = a_silver(bronze)
    reconciliar(bronze, silver, cuarentena)

    print("6) Gold: OTD por proveedor")
    print(a_gold(silver).to_string())

    ac, ins, yld = calidad(INSPECCIONES_CSV)
    print(f"7) Calidad: {ac:,} aceptadas / {ins:,} inspeccionadas = {yld:.1%}")
