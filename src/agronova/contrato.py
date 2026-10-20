"""Contrato de datos mínimo para la capa Silver de líneas de OC.

Un contrato de datos es un acuerdo explícito sobre columnas, tipos, unidades y calidad entre quien
produce un dato y quien lo consume. Aquí se valida en código; en un proyecto real el contrato se
acuerda con el dueño de la fuente y se versiona.
"""
CONTRATO_SILVER_OC = {
    "columnas_obligatorias": ["id_oc", "linea", "id_proveedor", "unidad",
                              "fecha_emision", "fecha_prometida", "cantidad"],
    "no_nulos": ["id_oc", "linea", "id_proveedor", "fecha_prometida"],
    "unidades_validas": ["UN", "KG"],
    "cantidad_minima": 0,
}


def validar_contrato(df, contrato=CONTRATO_SILVER_OC):
    """Devuelve la lista de violaciones (vacía si el conjunto cumple el contrato)."""
    faltantes = [c for c in contrato["columnas_obligatorias"] if c not in df.columns]
    if faltantes:
        return [{"regla": "columnas_obligatorias", "detalle": faltantes, "filas": None}]
    violaciones = []
    for col in contrato["no_nulos"]:
        n = int(df[col].isna().sum())
        if n:
            violaciones.append({"regla": f"no_nulo:{col}", "detalle": "valores nulos", "filas": n})
    malas = df[~df["unidad"].isin(contrato["unidades_validas"])]
    if len(malas):
        violaciones.append({"regla": "unidad_valida", "detalle": sorted(malas["unidad"].astype(str).unique()),
                            "filas": len(malas)})
    bajas = df[df["cantidad"].notna() & (df["cantidad"] < contrato["cantidad_minima"])]
    if len(bajas):
        violaciones.append({"regla": "cantidad_minima", "detalle": contrato["cantidad_minima"], "filas": len(bajas)})
    return violaciones
