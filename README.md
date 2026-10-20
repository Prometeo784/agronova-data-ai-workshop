# Del dato al valor: curso y repositorio de apoyo

**Workshop Data & AI 2026 · Programa Data Engineer 2026 · Data Science Research Perú**
Autor: [Marco Antonio Costa Sierra](https://www.linkedin.com/in/marco-antonio-costa-sierra-b733a2240)

> **Aviso.** AgroNova y la Empresa B son empresas **ficticias**. Todos los datos, nombres y cifras son **sintéticos**. Este material no refleja datos, sistemas ni reglas de ningún empleador.

## Qué es y qué no es

**Es** un caso didáctico de principio a fin para aprender a **diseñar, construir, validar y adoptar** un proyecto de datos e IA: un curso autoguiado de seis módulos, una mini plataforma de datos que puedes ejecutar y romper, SQL, un recuperador con permisos, plantillas de proyecto, casos reales con fuente y ejercicios con comprobación.

**No es** una librería, una plataforma de producción ni una referencia de cómo construir una en la nube. El código es **demostrativo** y los datos son **sintéticos**: las pruebas demuestran que el código hace lo que dice, no que el resultado sea válido en una empresa real.

La idea central: *una solución de datos no empieza eligiendo una herramienta; empieza por la decisión que se quiere mejorar.*

```
problema → requerimientos → fuentes → arquitectura → ingeniería de datos
→ productos de datos → BI e IA → gobernanza → adopción → valor
```

## Qué podrás hacer al terminar
- Convertir una solicitud como «un dashboard con IA» en una decisión, una métrica con línea base y un alcance de MVP.
- Explicar qué hace cada capa de Medallion y por qué **no** garantiza calidad por sí sola.
- Distinguir deduplicar, ser idempotente y ser atómico, y comprobarlo con pruebas.
- Detectar un «pipeline verde con dato incorrecto» con reconciliación y umbrales, y corregirlo **reprocesando desde Bronze**.
- Definir un indicador (OTD) con precisión y traducirlo a SQL y a una medida de Power BI.
- Decidir cuándo una pregunta necesita IA y evaluar un recuperador con sus límites.
- Gestionar un cambio de alcance, aceptar una entrega, diseñar la adopción y separar valor estimado de realizado.

## Empieza aquí

| Tienes | Haz esto |
|---|---|
| **15 minutos** | `python scripts/simular_plataforma.py --dias 6` y lee `docs/16_plataforma_persistente.md` |
| **Un par de horas** | Ejecuta `python scripts/ejecutar_todo.py`, abre `notebooks/01_pipeline_paso_a_paso.ipynb` y lee `docs/01_caso_agronova.md` |
| **Varias semanas, a tu ritmo** | Sigue el [curso](curso/README.md): seis módulos, cada uno con una comprobación ejecutable |

Requiere Python 3.9 o superior y pandas (`pip install -r requirements.txt`). No necesita cuentas ni internet. Opcional: `pip install -e .` y luego `agronova simular --dias 6`.

## Mapa del repositorio

| Carpeta o archivo | Qué contiene |
|---|---|
| `curso/` | Seis módulos autoguiados con objetivo, práctica y comprobación (`python curso/checkpoint.py M3`) |
| `src/agronova/` | Código: fuentes, ingesta, Silver, Gold, contrato de datos, observabilidad, valor, recuperador y la **mini plataforma persistente** |
| `docs/` | Caso completo, arquitectura, métricas, RAG y gobernanza, glosario, casos reales, Fabric y Power BI, seguridad y costos, autoevaluación y **decisiones de diseño** (`docs/adr/`) |
| `ejercicios/` | Tres ejercicios con comprobador y soluciones de referencia |
| `plantillas/` | Siete plantillas de proyecto: charter, fases, «terminado», riesgos, cambios, aceptación y adopción |
| `sql/`, `powerbi/`, `data/` | SQL, medidas DAX y datos sintéticos (incluye CSV para practicar en Power BI) |
| `rag/` | Corpus ficticio con permisos y preguntas de prueba |
| `notebooks/` | Cuaderno paso a paso del pipeline |
| `examples/` | Plantillas de conexión a un ERP SQL, un Excel y una API REST |
| `tests/` | 43 pruebas |

## Estado de validación (honesto)

| Qué | Estado |
|---|---|
| 43 pruebas con Python 3.12.3, pandas 3.0.2 y SQLite 3.45.1 | **Ejecutadas y en verde** (16/10/2026) |
| Instalación del paquete (`pip install`) y ejecución del comando `agronova` desde la copia instalada | **Verificadas** en un directorio temporal |
| Sintaxis compatible con Python 3.9 | Verificada con `ast`; **la ejecución en 3.9 a 3.11 y con pandas 2.x no se ha probado** |
| GitHub Actions (matriz 3.9 a 3.12) | **Sin ejecutar** hasta publicar el repositorio |
| Diagramas Mermaid y Codespaces (`.devcontainer`) | **Sin comprobar** |
| Medidas DAX | **No ejecutadas** en Power BI Desktop |
| Plantillas de `examples/` | **No ejecutadas** (dependen de tu entorno) |

Detalle de lo que demuestra cada prueba, y lo que no, en [`docs/09_alcance_y_validacion.md`](docs/09_alcance_y_validacion.md).

## Límites que conviene conocer
- El **recuperador** (`rag.py`) no es un RAG completo: no usa embeddings ni un modelo de lenguaje. Sus siete preguntas contra tres documentos escritos para la prueba son una prueba funcional inicial, **no evidencia de efectividad**.
- La **mini plataforma** usa SQLite en un solo proceso: no demuestra concurrencia, escala ni comportamiento de un motor productivo.
- Las fuentes de terceros se verificaron solo en parte (`docs/08_fuentes.md`).

## Cómo leer las etiquetas de evidencia
`[DOCUMENTADO]` (respaldado por una fuente), `[VERIFICADO EXPERIMENTALMENTE]` (comprobado con una prueba), `[EJEMPLO ILUSTRATIVO]`, `[RECOMENDACIÓN]`, `[SUPUESTO]`, `[PENDIENTE]`.

## Contribuir
Lee [`CONTRIBUTING.md`](CONTRIBUTING.md). Las dudas y los errores son la aportación más útil.

## Licencia
**Pendiente de definir por el autor antes de publicar.** Mientras no haya licencia, el código y los documentos no se pueden reutilizar legalmente.
