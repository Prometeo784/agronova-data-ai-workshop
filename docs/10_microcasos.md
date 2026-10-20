# Cinco microcasos comparativos

`[EJEMPLO ILUSTRATIVO]` Todos son **casos ficticios**; no son proyectos ejecutados por el autor ni muestran resultados reales. Sirven para ver cómo cambian los datos, la validación, el indicador y la limitación según el problema. No todos requieren IA.

| | **Compras** | **Inventarios** | **Finanzas** | **Mantenimiento** | **RAG documental** |
|---|---|---|---|---|---|
| **Problema** | Un proveedor falla sin aviso y la línea se detiene | Quiebres de stock en las bodegas | Las desviaciones de presupuesto se detectan tarde | Paros repetidos por la misma falla | Encontrar la cláusula o política correcta toma demasiado tiempo |
| **Usuario** | Gerencia de Compras | Jefe de bodega | Control presupuestario | Jefe de mantenimiento | Analista de compras |
| **Datos requeridos** | Órdenes de compra, recepciones, maestro de proveedores | Existencias, ventas, plazos de entrega | Presupuesto (Excel) y compras comprometidas | Órdenes de trabajo, paros y repuestos | Contratos y políticas con su nivel de acceso |
| **Solución propuesta** | Scorecard de OTD por proveedor | Cobertura en días y regla de reposición | Comprometido frente a presupuesto por mes, con reglas financieras | Tablero de tiempo entre fallas por equipo | Recuperación con filtro de permisos, cita y abstención |
| **Forma de validación** | Reconciliación con el ERP y aprobación de Compras | Conteo físico en una bodega | Conciliación con contabilidad | Comparación con el registro de turno | Conjunto de preguntas de prueba, incluidas algunas sin respuesta |
| **Indicador de éxito** | OTD correcto por proveedor | Quiebres de stock y días de cobertura | Desviación detectada con anticipación | Horas de paro por falla | Relevancia, fidelidad y abstención apropiada |
| **Limitación principal** | Cubre solo lo recibido o inspeccionado | No modela la estacionalidad de la demanda | El presupuesto en Excel tiene versiones paralelas | Registros incompletos de la causa de falla | No sustituye una cifra exacta; depende de que los documentos estén vigentes |
| **Decisión de negocio que habilita** | Exigir acción correctiva o renegociar | Cuánto reponer en cada bodega | Frenar o reasignar compras | Qué mantenimiento preventivo adelantar | Qué cláusula o política aplicar |
| **¿Necesita IA generativa?** | No | No | No | No (puede ayudar un modelo más adelante) | Sí, como complemento de la búsqueda |

El caso de Compras es el que se desarrolla completo en `01_caso_agronova.md` y en el código. Inventarios corresponde a la actividad de la Empresa B (`05_actividad_empresa_b.md`).
