# Registro de cambios

## 2.0.0 (17/10/2026)
- **Mini plataforma persistente** (`plataforma.py`, `simulador.py`, `cli.py`): estado en SQLite, corridas atómicas e idempotentes, marca de agua guardada, registro de corridas, reproceso desde Bronze y detección de cambios de esquema. Simulación de seis días.
- **Curso autoguiado** de seis módulos con comprobaciones ejecutables (`curso/`).
- **Decisiones de diseño** explicadas (`docs/adr/`) y documento de la plataforma (`docs/16`).
- **Paquete instalable** (`pyproject.toml`), comando `agronova`, guía de contribución, plantillas de incidencias, `.devcontainer` y matriz de CI para Python 3.9 a 3.12 (aún sin ejecutar).
- README reescrito: qué es, qué no es, qué podrás hacer, por dónde empezar y estado de validación.
- Pruebas: 43 en total.

## 1.1 (16/10/2026)
- Casos reales documentados (`docs/11`), ejecución del proyecto y plantillas, seguridad y costos, Fabric y Power BI.
- Contrato de datos, observabilidad, cálculo de valor, cifras canónicas y exportaciones para Power BI.
- Cuaderno paso a paso, tres ejercicios con comprobador y soluciones, autoevaluación y guía de estudio.
- Pruebas: 31 en total. Ver `docs/09_alcance_y_validacion.md` para lo que demuestran y lo que no.

## 1.0 (13/10/2026)
- Versión inicial: caso AgroNova, pipeline Bronze/Silver/Gold, SQL, mini recuperador y diagramas.
