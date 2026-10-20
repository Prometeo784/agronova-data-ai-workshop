# Arquitectura y trade-offs

No existe una opción ganadora sin condiciones `[RECOMENDACIÓN]`. Plataformas como Microsoft Fabric o Databricks son **ejemplos ilustrativos**: la arquitectura se explica primero desde los requerimientos.

## Dos escalas para el mismo caso

| | Escala A: AgroNova hoy | Escala B: 100 veces el volumen |
|---|---|---|
| Volumen | ~12,000 líneas de OC al año | ~1,200,000 líneas al año, más eventos de transporte |
| Procesamiento | Un motor SQL con transformaciones programadas | Motor distribuido (por ejemplo Spark) |
| Almacenamiento | Warehouse o Lakehouse pequeño | Lakehouse en formato de tabla abierta |
| Orquestación | Programador simple con dependencias | Orquestador con monitoreo y reintentos |
| Equipo | 1 a 2 personas | Equipo de plataforma |
| Riesgo | Sobrecosto de complejidad | Cuellos de botella y costos de cómputo |

## Comparaciones

| Decisión | Opciones y cuándo conviene cada una | Evidencia que falta para decidir |
|---|---|---|
| ETL o ELT | ETL si hay que enmascarar o filtrar antes de aterrizar. ELT si el destino es potente y se quiere conservar el dato crudo | Política de datos sensibles y plataforma elegida |
| Batch o streaming | Batch si la decisión es por turno o por día. Streaming solo si cambia en minutos y alguien actuará en ese plazo | Si Operaciones necesita menos de un día |
| Lakehouse o Data Warehouse | Lakehouse con datos variados y varios usos. Warehouse con datos estructurados, SQL y reportes estables. Pueden combinarse | Habilidades del equipo, formatos y licenciamiento |
| Administrado o autogestionado | Administrado reduce operación en equipos pequeños. Autogestionado da más control y exige más mantenimiento | Costo total y restricciones de nube |
| Plataforma integrada o componentes | Integrada reduce integración. Componentes dan flexibilidad y complejidad | Dependencia de proveedor aceptable |
| SQL o recuperación semántica | SQL para cifras exactas. Recuperación semántica para texto no estructurado | Proporción de preguntas documentales |
| RAG u otras adaptaciones | RAG si el conocimiento cambia y se requieren citas. Ajustar el modelo cuando se busca cambiar su comportamiento o estilo | Volumen y estabilidad de los documentos |

## Carga completa, incremental y CDC

- **Completa:** copia todo en cada corrida. Simple, pero pesada para el ERP.
- **Incremental:** trae solo lo nuevo o modificado con una marca de agua (por ejemplo, fecha de modificación). Es lo que implementa `src/agronova/ingesta.py`.
- **CDC (captura de cambios):** lee los cambios del registro del sistema. Es una evolución si se exige baja latencia y requiere acceso técnico al ERP. CDC no implica streaming: puede aplicarse en lotes.

## Qué le falta al código de este repositorio para producción

Almacenamiento persistente de las tres capas y de la marca de agua; orquestación con reintentos; registro de eventos y alertas hacia un responsable; control de versiones y ambientes separados; gestión de secretos; y revisión de permisos y datos sensibles.
