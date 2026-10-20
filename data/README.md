# Datos de ejemplo (100 % simulados)

Generados con `python scripts/generar_datos.py`. Puedes abrirlos en Excel, Power BI, Fabric o cualquier herramienta para practicar el flujo Bronze → Silver → Gold.

**`erp_oc_linea.csv`** (1,000 filas). Simula la salida cruda de un ERP, con defectos típicos a propósito.

| Columna | Descripción |
|---|---|
| `id_oc`, `linea` | Clave de negocio de la línea de orden de compra |
| `proveedor` | Texto con espacios, por ejemplo `"PROV C "` |
| `unidad_txt` | Unidad escrita de varias formas (`uni.`, `UN `, `kg`) |
| `fecha_emision`, `fecha_prometida`, `fecha_recepcion` | Texto ISO. La recepción es vacía si la línea sigue abierta |
| `cantidad_txt` | Texto con punto de miles, por ejemplo `"5.000"`. `"0"` en recepciones rechazadas |
| `fecha_modificacion` | Base de la marca de agua de la carga incremental |

**`inspecciones.csv`** (100 lotes). `unidades_inspeccionadas` y `unidades_rechazadas`; suma 50,000 y 1,500.
