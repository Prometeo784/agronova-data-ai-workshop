# Preguntas frecuentes

Respuestas de conocimiento técnico general `[RECOMENDACIÓN]`, salvo donde se indica.

**¿Necesito dominar Fabric o Databricks para ser Data Engineer?** No. SQL, Python, modelado, calidad y orquestación se transfieren entre plataformas. Conviene aprenderlos primero y luego profundizar en una.

**¿Cuándo sí necesito streaming?** Cuando una decisión pierde valor en minutos y alguien actuará en ese plazo. Si la decisión es diaria, batch es más simple y barato.

**¿Medallion es obligatorio?** Es un patrón de diseño, no una garantía automática de calidad. Microsoft lo describe como el enfoque recomendado para organizar datos en un lakehouse de Fabric `[DOCUMENTADO]`. Si conviene aplicarlo en un caso concreto es criterio profesional `[RECOMENDACIÓN]`; la fuente consultada no afirma que los nombres o el número de capas sean libres.

**¿RAG o ajuste del modelo?** Resuelven problemas distintos. RAG aporta conocimiento externo y actualizable, con citas. El ajuste modifica el comportamiento del modelo. Pueden combinarse.

**¿RAG elimina las alucinaciones?** No. Puede reducirlas si la recuperación es buena, pero hay que evaluar fidelidad y abstención.

**¿Qué hago si el ERP no me deja extraer datos?** Negocia con TI una réplica o vista de solo lectura, extrae fuera del horario pico y usa carga incremental.

**¿Cómo sé que un pipeline mintió?** Con reconciliación de conteos y totales, umbrales de cuarentena y comparación contra la fuente.

**¿Dónde se define un KPI?** Una sola vez, en la capa Gold o semántica, con un dueño.

**¿Cómo estimo el retorno?** Con línea base, costos de construcción y operación, separando beneficio estimado de realizado. El ejemplo del caso es ficticio.

**¿Y si nadie usa el dashboard?** Revisa la adopción: validación con usuarios, integración al proceso y capacitación. Agregar funciones rara vez lo resuelve.
