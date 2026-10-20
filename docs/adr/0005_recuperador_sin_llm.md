# 0005. Un recuperador sin modelo de lenguaje

**Contexto.** Un RAG real exige un modelo de lenguaje y un índice de embeddings, con costos, cuentas y resultados no deterministas.

**Decisión.** `rag.py` implementa solo la recuperación por coincidencia de términos, con filtro de permisos antes de ordenar, cita de la fuente, abstención y una evaluación mínima. Se declara que **no es un RAG completo**.

**Alternativas.** Integrar un modelo (más realista, pero no reproducible ni gratuito); omitir el ejemplo (se perdería la demostración de permisos y abstención).

**Consecuencias.**
- (+) Es determinista, gratuito y comprobable.
- (−) No puede evaluar fidelidad de respuestas generadas, ni resistencia a *prompt injection*, ni calidad de embeddings.
- (−) Sus siete preguntas contra tres documentos escritos para la prueba no son evidencia de efectividad.
