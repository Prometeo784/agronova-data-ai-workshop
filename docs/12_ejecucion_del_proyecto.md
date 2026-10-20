# Ejecución del proyecto: del problema a la medición

Marco práctico en seis fases, con plantillas en `../plantillas/`. Es una propuesta `[RECOMENDACIÓN]`: adáptala a tu organización.

| Fase | Pregunta central | Entregable | Plantilla |
|---|---|---|---|
| Definir | ¿Qué decisión mejora y cómo la mediremos? | Charter con línea base | `01_charter_del_mvp.md` |
| Diseñar | ¿Qué entra en el MVP y qué no? | Alcance, arquitectura y riesgos | `02`, `03`, `04` |
| Construir | ¿Funciona y se puede confiar? | Pipelines, pruebas y contrato de datos | `05` para cambios |
| Validar | ¿Quién confirma que las cifras son correctas? | Cifras conciliadas y aprobadas | `06_acta_de_aceptacion.md` |
| Desplegar | ¿Lo usarán? | Capacitación, alertas e integración al proceso | `07_plan_de_adopcion_y_medicion.md` |
| Operar y medir | ¿Generó valor? | Monitoreo y medición contra la línea base | `07` |

## Seis preguntas que un proyecto debe poder responder

1. **¿Qué significa que el MVP esté terminado?** Cifras conciliadas, aprobadas por el usuario y en uso (`03`).
2. **¿Qué entregables se necesitan en cada fase?** La matriz de fases (`02`).
3. **¿Cómo se controla el cambio de alcance?** Se registra, se estima su costo y fecha, y se decide (`05`).
4. **¿Cómo se detectan riesgos de calidad de datos?** Contrato, pruebas, reconciliación y alertas con umbral (`src/agronova/`).
5. **¿Qué pasa si el modelo funciona, pero nadie lo usa?** Es un fracaso de adopción: se diseña desde el inicio con usuarios clave y revisión semanal (`07`).
6. **¿Quién acepta formalmente?** Lo define la organización; el ejemplo usa al patrocinador (`06`).

## Qué demostrar con el código del repositorio

| Concepto | Dónde verlo | Qué demuestra y qué no |
|---|---|---|
| Línea base y valor | `src/agronova/valor.py` y su prueba | Los cálculos del caso con supuestos ficticios. No demuestra beneficios reales |
| Contrato de datos | `contrato.py` | Validación de columnas, unidades y cantidades sobre datos sintéticos |
| Reconciliación y umbral | `control.py`, `observabilidad.py` | Detección de una regla defectuosa en datos sintéticos |
| Cambios de alcance y aceptación | `plantillas/` | Solo son formatos; su uso depende de la organización |
