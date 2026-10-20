# Para seguir estudiando

La sesión en vivo se centra en un hilo: **problema → datos → arquitectura → ejecución → validación → adopción → valor**. Lo que no cabe en 90 minutos queda aquí, para estudiarlo con calma. El camino ordenado está en [`../curso/README.md`](../curso/README.md). Hay también un **anexo de diapositivas** con los temas que no se presentan en vivo.

## Qué queda para estudiar por tu cuenta

| Tema | Por qué importa | Dónde estudiarlo | Ejercicio para practicar |
|---|---|---|---|
| Usuarios y decisiones | Sin una decisión clara, cualquier herramienta es una apuesta | `01_caso_agronova.md` (§1), `plantillas/01_charter_del_mvp.md` | Escribe el charter de un problema de tu entorno |
| ETL y ELT, batch y streaming | Define dónde se transforma el dato y cada cuánto se necesita | `02_arquitectura_y_tradeoffs.md` | Para tu caso, escribe qué frescura necesita la decisión y justifica ETL o ELT |
| Carga completa, incremental y CDC | Evita dañar el sistema fuente | `02_arquitectura_y_tradeoffs.md`, `src/agronova/ingesta.py` | Ejecuta el pipeline dos veces y observa la marca de agua |
| Deduplicar, idempotencia y atomicidad | Repetir una carga no debe cambiar el resultado | `src/agronova/upsert.py`, `tests/test_upsert.py` | Añade una prueba para un caso nuevo, por ejemplo un dato más reciente que llega tarde |
| Contratos, pruebas, reconciliación y alertas | Un pipeline en verde no prueba que el dato sea correcto | `contrato.py`, `control.py`, `observabilidad.py` | Añade una regla de calidad y su prueba |
| Dashboard, producto de datos, modelo y RAG | Cada uno exige calidad y evaluación distintas | `04_rag_y_gobernanza.md`, `06_glosario.md` | Clasifica cinco necesidades de tu trabajo en estas cuatro categorías |
| Microcasos comparativos | Cada problema cambia datos, indicador y límites | `10_microcasos.md` | Escribe un sexto microcaso con las mismas ocho filas |
| Aceptación formal y riesgos | Un proyecto no termina cuando el código corre | `12_ejecucion_del_proyecto.md`, `plantillas/04` y `06` | Completa el registro de riesgos de un proyecto tuyo |
| Casos reales | Los mismos errores ocurren fuera del aula | `11_casos_reales.md` | Elige uno y señala qué control lo habría hecho visible |
| Power BI y DAX | Traducir una definición de negocio en una medida | `14_fabric_y_power_bi.md`, `powerbi/medidas_otd.dax` | Reproduce el OTD con `data/exportadas/` y compara con las cifras esperadas |
| Seguridad y costos | Decisiones que se toman al diseñar, no al final | `13_seguridad_y_costos.md` | Aplica la tabla a un proyecto tuyo y marca qué te falta |

## Una ruta posible `[RECOMENDACIÓN]`

1. Lee `01_caso_agronova.md` y ejecuta `python scripts/ejecutar_pipeline.py`.
2. Abre el cuaderno `notebooks/01_pipeline_paso_a_paso.ipynb` y ejecútalo celda por celda.
3. Ejecuta las pruebas (`python -m unittest discover -s tests -v`) y rompe una regla a propósito para ver cómo falla.
4. Practica en Power BI con los CSV exportados y compara tus resultados con `data/cifras_canonicas.json`.
5. Aplica las plantillas de `plantillas/` a un problema real de tu entorno.
6. Lee los casos reales y discute con otras personas qué control faltó.

No hay un plazo: avanza a tu ritmo. Todo el material usa datos y casos **ficticios** con fines didácticos; el código es demostrativo, no está listo para producción.
