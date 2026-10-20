-- Esquema ilustrativo (SQL estándar; ajusta tipos al motor que uses). Datos ficticios.
-- Bronze: copia fiel del origen, todo como texto, más trazabilidad.
CREATE TABLE brz_erp_oc_linea (
    id_oc INT, linea INT, proveedor TEXT, unidad_txt TEXT,
    fecha_emision TEXT, fecha_prometida TEXT, fecha_recepcion TEXT,
    cantidad_txt TEXT, fecha_modificacion TEXT,
    lote_carga TEXT, fecha_carga TIMESTAMP
);

-- Silver: tipado, normalizado y validado. Lo rechazado vive en cuarentena con su motivo.
CREATE TABLE slv_oc_linea (
    id_oc INT NOT NULL, linea INT NOT NULL, id_proveedor TEXT NOT NULL, unidad TEXT,
    fecha_emision DATE, fecha_prometida DATE, fecha_recepcion DATE, cantidad NUMERIC,
    PRIMARY KEY (id_oc, linea)
);
CREATE TABLE slv_oc_linea_cuarentena (
    id_oc INT, linea INT, motivo TEXT, lote_carga TEXT
);
