# M2. Arquitectura y Medallion

**Objetivo.** Entender cómo viaja el dato de las fuentes a la decisión y qué hace cada capa de Medallion, sin confundir un patrón con una garantía de calidad.

**Prerrequisitos.** M1.

**Lee.** `docs/02_arquitectura_y_tradeoffs.md`, `docs/14_fabric_y_power_bi.md` (§1), `docs/diagramas.md`.

**Haz.**
1. Ejecuta `python scripts/ejecutar_pipeline.py` y sigue la orden 100245 por Bronze, Silver y Gold en el cuaderno `notebooks/01_pipeline_paso_a_paso.ipynb`.
2. Escribe, para tu caso del M1, qué guardaría cada capa y quién la usaría.
3. Decide si tu caso necesita el volumen y la complejidad que sugiere una plataforma grande (`docs/02`, «Dos escalas»).

**Comprobación.** `python curso/checkpoint.py M2`

**Errores comunes.** Pensar que Medallion garantiza calidad; elegir la plataforma antes que los requisitos.

**Siguiente.** M3.
