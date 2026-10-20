def validar_proveedores(df, validos):
    malos = df[~df["id_proveedor"].isin(validos)]
    if malos.empty:
        return []
    return [{"regla": "proveedor_valido", "detalle": sorted(malos["id_proveedor"].astype(str).unique()),
             "filas": len(malos)}]
