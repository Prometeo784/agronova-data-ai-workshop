# M5. IA y RAG con criterio

**Objetivo.** Decidir cuándo una pregunta necesita IA, entender el flujo de RAG y evaluar un recuperador con sus límites.

**Prerrequisitos.** M3.

**Lee.** `docs/04_rag_y_gobernanza.md`, `docs/11_casos_reales.md` (Air Canada), `docs/13_seguridad_y_costos.md`.

**Haz.**
1. Clasifica diez preguntas de tu trabajo entre «SQL o BI» y «RAG».
2. Ejecuta `python scripts/evaluar_rag.py`, añade una pregunta a `rag/preguntas_prueba.csv` que debería abstenerse y comprueba si lo hace.
3. Escribe qué no demuestra esa evaluación (pista: `docs/09_alcance_y_validacion.md`).

**Comprobación.** `python curso/checkpoint.py M5`

**Errores comunes.** Usar IA para cifras exactas; filtrar los permisos después de generar la respuesta; presentar un 100 % de siete preguntas como evidencia.

**Siguiente.** M6.
