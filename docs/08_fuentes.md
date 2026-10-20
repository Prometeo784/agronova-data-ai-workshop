# Fuentes y estado de verificación

Verificado el 13 de octubre de 2026. Las cifras de terceros **no** se usan como resultados esperados para AgroNova.

| Fuente | Estado | Qué respalda | Observación |
|---|---|---|---|
| [Atlan, 5 Unity Catalog Limitations to Overcome in 2026](https://atlan.com/know/databricks-unity-catalog-limitations/) | Verificada (página abierta) | ABAC, RLS y enmascaramiento exigen DBR 16.4 o superior, o cómputo serverless. Iceberg administrado disponible desde mayo de 2026 y OpenSharing desde junio de 2026 | Fuente de un proveedor |
| [Flexera, comunicado del State of the Cloud 2026](https://www.flexera.com/about-us/press-center/flexera-finds-cloud-value-is-rising-while-ai-waste-grows) | Parcial (comunicado en resultados de búsqueda) | El 29 % del gasto IaaS y PaaS se estima desperdiciado, según 753 encuestados | Estimación de los encuestados, no porcentaje del presupuesto total de TI |
| [Block, historia de cliente de Databricks](https://www.databricks.com/br/customers/block/unity-catalog) | Parcial (resultados de búsqueda) | Reducción de 12 veces en cómputo por migrar casos de grafos y 20 % menos de egreso entre nubes | Material comercial del proveedor. El 12x no proviene de Unity Catalog |
| [Kanerika, AI in Supply Chain](https://kanerika.com/blogs/ai-in-supply-chain/) | Parcial (otro artículo del mismo sitio) | Atribuye a McKinsey 15 %, 35 % y 65 % de mejoras logísticas, de inventario y de servicio | Según fuentes secundarias, vienen de un artículo de 2021 que compara con competidores más lentos. No usar como resultado esperado |
| [Microsoft Learn, Understand medallion architecture for Fabric with OneLake](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture) | Verificada (página completa leída el 13/10/2026; actualización indicada: 17/07/2026) | Medallion es un patrón de diseño para organizar datos en un lakehouse y el enfoque recomendado para Fabric. Bronze conserva los datos como llegan; Silver corrige errores, estandariza formatos y elimina duplicados; Gold se organiza para reportes. Describe dos patrones: todas las capas como lakehouses, o Bronze y Silver como lakehouses y Gold como warehouse, según preferencia y experiencia del equipo | La página **no** afirma que los nombres o el número de capas sean flexibles. Dice que ayuda a mantener los datos precisos y fiables según ACID, lo que no equivale a garantizar su calidad |
| Practical Logix | No verificada | Sin contrastar | Falta el archivo original |
| Lasso (caso de proveedores) | No localizada | Sin contrastar | Falta el archivo original |
| "Compendio Técnico y Base de Conocimiento Enterprise" | No identificable | Sin contrastar | Sin autor, fecha ni localizador |

No se han fabricado referencias bibliográficas. Cuando se confirmen autor, año y enlace de cada fuente, se prepararán las referencias en el formato que se requiera.

## Fuentes de los casos reales y de DAX (consultadas el 16/10/2026)

| Fuente | Estado | Qué respalda | Observación |
|---|---|---|---|
| [NASA, Mars Climate Orbiter Mishap Investigation Board, Phase I Report (10/11/1999)](https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf) | Verificada (documento leído completo) | Causa raíz: unidades inglesas en lugar de métricas en un archivo de software en tierra; factor 4.45; causas contribuyentes | Fuente primaria |
| [Moffatt v. Air Canada, 2024 BCCRT 149](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do) | Verificada (decisión leída completa) | El tribunal responsabilizó a Air Canada por la información de su chatbot; pago total de 812.02 CAD | No indica qué tecnología usaba el chatbot |
| [The Register, 5/10/2020](https://www.theregister.com/2020/10/05/excel_england_coronavirus_contact_error/) y [Digital Health, 8/10/2020](https://digitalhealth.net/?p=108775) | Parcial (fuentes secundarias, vistas en resultados de búsqueda) | 15,841 casos no incluidos entre el 25/9 y el 2/10/2020; explicación atribuida al límite de filas del formato .xls | La causa técnica no está confirmada en un informe oficial leído |
| [Microsoft Learn, DIVIDE (DAX)](https://learn.microsoft.com/en-nz/dax/divide-function-dax) | Verificada (resultado de búsqueda con el texto de la página) | Devuelve `BLANK()` si el denominador es cero, salvo que se indique un resultado alternativo | |

