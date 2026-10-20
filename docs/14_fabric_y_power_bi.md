# Fabric y Power BI: correspondencia con el caso

Qué se afirma, con qué respaldo y qué falta verificar. Fabric se usa como **ejemplo ilustrativo**, sin compararlo con otras plataformas.

## 1. Medallion en Fabric `[DOCUMENTADO]`

Fuente: [Microsoft Learn, Understand medallion architecture for Fabric with OneLake](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture). Página leída completa el 13/10/2026 (actualización indicada: 17/07/2026).

| Capa lógica | Qué hace (según la página) | En AgroNova | Componente de Fabric mencionado |
|---|---|---|---|
| Bronze | Conserva los datos tal como llegan | Copia fiel del ERP y del Excel, con lote y fecha de carga | Lakehouse |
| Silver | Corrige errores, estandariza formatos y elimina duplicados | Tipado, unidades normalizadas, cuarentena | Lakehouse |
| Gold | Se organiza para reportes | Hechos y dimensiones, KPI definidos una vez | Lakehouse o warehouse |

- La página describe dos patrones: todas las capas como lakehouses, o Bronze y Silver como lakehouses y Gold como warehouse. La elección depende de la preferencia y de la experiencia del equipo.
- OneLake es un lago lógico único para la organización.
- Con lakehouses se puede consultar por el punto de acceso SQL (*SQL analytics endpoint*).
- La página **no afirma** que los nombres o el número de capas sean libres, ni que Medallion garantice calidad por sí solo. Esa advertencia es una `[RECOMENDACIÓN]` de este repositorio: la calidad la dan las validaciones de cada capa.

## 2. Lo que NO se ha verificado `[PENDIENTE]`

Data Factory y *pipelines*, *notebooks* y Spark, la seguridad y el gobierno de Fabric, *Direct Lake* y los modelos semánticos, y todo lo que dependa de licencias, capacidad, región o versión. Antes de afirmarlos en una presentación, consúltalos en la documentación oficial vigente.

## 3. Del indicador de negocio a la medida en Power BI

**Definición de negocio** (ver `01_caso_agronova.md`):
- Es a tiempo cuando la recepción ocurre en o antes de la fecha prometida.
- Es elegible la línea cuya fecha prometida venció en el periodo.
- El denominador son **todas** las líneas elegibles, incluidas las no recibidas.
- La granularidad es la línea de orden de compra.
- Parciales y cancelaciones: `[SUPUESTO]` que debe validarse con Compras. El ejemplo no los modela.

**Implementación**: `powerbi/medidas_otd.dax`. `DIVIDE` devuelve `BLANK()` si el denominador es cero, salvo que se indique un resultado alternativo [DOCUMENTADO: [Microsoft Learn, DIVIDE (DAX)](https://learn.microsoft.com/en-nz/dax/divide-function-dax)].

**Qué está verificado y qué no**
- `[VERIFICADO EXPERIMENTALMENTE]` La lógica del OTD (a tiempo ÷ vencidas) con pandas y con SQL sobre datos sintéticos (`tests/`), y que `data/exportadas/slv_oc_linea.csv` la reproduce.
- `[NO EJECUTADO]` Las medidas DAX en Power BI Desktop. Pruébalas siguiendo los pasos de abajo.

## 4. Cómo reproducirlo en Power BI Desktop (procedimiento, no probado aquí)

1. Ejecuta `python scripts/exportar_capas.py` para generar `data/exportadas/`.
2. En Power BI Desktop: *Obtener datos > Texto o CSV*. Importa `slv_oc_linea.csv` y `dim_proveedor.csv`.
3. Comprueba los tipos de columna: fechas como fecha y `Recibida`, `EsVencida` y `ATiempo` como número entero.
4. En la vista de modelo, relaciona `Proveedor[IdProveedor]` con `'Lineas OC'[IdProveedor]` (uno a muchos).
5. Crea las medidas de `powerbi/medidas_otd.dax`.
6. Añade una tabla o una matriz por proveedor con `[OTD %]` y `[OTD Ingenuo %]`.
7. **Resultado esperado** `[a verificar]`: A 95.0 %, B 80.0 %, C 70.0 % y, con la definición ingenua, 96.0 %, 85.7 % y 82.9 %. Si no coinciden, revisa los tipos y la relación.
