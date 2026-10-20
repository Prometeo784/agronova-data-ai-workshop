# RAG y gobernanza

## Qué es y qué no es RAG

**RAG** (Retrieval-Augmented Generation) hace que un modelo de lenguaje responda apoyándose en fragmentos recuperados de fuentes autorizadas. **No** reentrena el modelo (eso sería *fine-tuning*) y **no** elimina las alucinaciones: las puede reducir si la recuperación es buena, y hay que evaluarlo.

Flujo conceptual: documentos autorizados → extracción → limpieza → fragmentación (*chunking*) → metadatos y permisos → *embeddings* → índice → recuperación con filtro de permisos → contexto → respuesta con citas o abstención → evaluación y monitoreo (ver `diagramas.md`).

## ¿Esta pregunta necesita IA?

| Pregunta | Herramienta | Por qué |
|---|---|---|
| ¿Cuánto hemos comprometido frente al presupuesto de empaques? | SQL y reglas financieras (Gold) | Cifra exacta y reproducible |
| ¿Qué proveedores están bajo 80 % de OTD? | BI o SQL | Cálculo determinista |
| ¿Qué dice el contrato del proveedor C sobre penalidades por retraso? | RAG | La respuesta está en un documento |
| ¿Qué política aplica a una recepción rechazada? | RAG | Política en texto, con cita |

## Dónde falla un RAG

Fuentes desactualizadas o duplicadas; fragmentos que separan una cláusula de su excepción; recuperar documentos que el usuario no debería ver; respuestas sin evidencia suficiente.

## Mini sistema de recuperación de este repositorio

`src/agronova/rag.py` **no es un RAG completo** (sin embeddings ni LLM). Muestra con código:

1. el **filtro de permisos antes de ordenar** y de armar el contexto;
2. la **cita** de la fuente;
3. la **abstención** cuando no hay evidencia suficiente;
4. la **evaluación** con preguntas de prueba (`rag/preguntas_prueba.csv`): relevancia, abstención apropiada y fugas de permisos.

El corpus (`rag/corpus/`) es ficticio. El umbral de similitud (`UMBRAL = 0.34`) es un ejemplo: en un sistema real se calibra con tus propios documentos y preguntas. Ejecuta `python scripts/evaluar_rag.py`.

**Alcance de la evaluación incluida.** Son 7 preguntas escritas contra 3 documentos creados para la prueba. Es una **prueba funcional inicial de alcance limitado**: un 100 % aquí no es evidencia de efectividad general. Tampoco evalúa respuestas generadas (no hay modelo de lenguaje), ni embeddings, ni ataques reales de *prompt injection*. Recuperar un documento no garantiza que la respuesta generada sea correcta: el recuperador y las respuestas generadas se evalúan por separado.

**Con un LLM real** habría que añadir: embeddings, un índice vectorial (con el mismo filtro de permisos), la construcción del prompt solo con fragmentos autorizados, y la evaluación de fidelidad de las respuestas generadas.

## Riesgos específicos de los sistemas con modelos de lenguaje

- **Prompt injection (inyección de instrucciones).** Un texto que llega como dato (un documento, un correo, una página) puede incluir instrucciones dirigidas al modelo, por ejemplo «ignora las reglas anteriores». Si el sistema mezcla instrucciones y datos, el modelo puede obedecerlas. Mitigaciones habituales `[RECOMENDACIÓN]`: tratar el contenido recuperado como dato y no como instrucción, limitar lo que el modelo puede hacer (mínimo privilegio y sin acciones irreversibles automáticas), filtrar por permisos antes de recuperar, revisar con una persona las acciones de consecuencia y probar el sistema con intentos de ataque.
- **Fuga de información sensible.** Un fragmento restringido que llega al contexto puede aparecer en la respuesta. Por eso el filtro de permisos actúa antes de construir el contexto.
- **Alcance de este repositorio.** `rag.py` no usa un modelo de lenguaje, así que **no puede demostrar** resistencia a la inyección de instrucciones. Solo prueba que un usuario sin permiso no recupera un documento restringido.

## Gobernanza como capacidad transversal

| Capacidad | En el caso |
|---|---|
| Responsables | Cada fuente y cada KPI tiene un dueño con nombre y rol |
| Catálogo y linaje | Definición única de OTD y trazabilidad hasta el reporte |
| Control de acceso | Roles para Compras, Operaciones y Finanzas. Costos y precios restringidos |
| Datos sensibles | Se enmascaran o excluyen los datos personales de contactos |
| Retención y auditoría | Se conservan las cargas y se registra quién consultó qué |
| Permisos en RAG | Cada fragmento hereda los permisos de su documento |
| Responsabilidad humana | Una alerta automática no ordena por sí sola una acción correctiva |
