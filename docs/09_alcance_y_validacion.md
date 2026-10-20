# Alcance y validación

Este documento separa **lo que se probó**, **lo que esas pruebas demuestran** y **lo que sigue pendiente**.

## Qué demuestran las pruebas (y qué no)

| Prueba | Qué demuestra | Qué NO demuestra |
|---|---|---|
| `test_pipeline.py` (8 pruebas) | Con datos sintéticos construidos para reproducir las cifras del caso, el código produce esas cifras (938/62, OTD 78.0 %, calidad 97.0 %) | Que las reglas o el KPI sean válidos para una empresa real, ni que el código escale |
| Equivalencia SQL y pandas | Dos implementaciones del OTD coinciden sobre los mismos datos sintéticos | Corrección de la definición de negocio |
| `test_upsert.py` (4 pruebas) | En SQLite: ejecutar dos veces deja el mismo estado, un cambio actualiza sin duplicar, un dato más antiguo no pisa a uno reciente y una carga fallida se revierte | Comportamiento con concurrencia, un motor productivo o Delta MERGE |
| `test_extras.py` (12 pruebas) | Contrato de datos, alertas de observabilidad, cálculo de valor, sincronía con `cifras_canonicas.json` y exportación para Power BI | Que las reglas y umbrales sean adecuados para datos reales |
| `test_plataforma.py` (10 pruebas) | En SQLite y con datos sintéticos: persistencia entre conexiones, marca de agua, actualización sin duplicar, atomicidad (un fallo a mitad no deja nada y la marca no avanza), idempotencia al reiniciar la marca, reproceso desde Bronze y cambios de esquema de la fuente | Concurrencia, escala, un orquestador, programación de corridas ni el comportamiento de un motor productivo |
| `test_curso.py` (2 pruebas) | Que las comprobaciones de los módulos M2 a M6 pasan con las soluciones de referencia | Que el material enseñe bien: no se probó con estudiantes |
| `test_ejercicios.py` (2 pruebas) | Las soluciones de referencia pasan el comprobador y los ejercicios sin completar figuran como pendientes. El valor esperado del ejercicio 1 se verificó con un cálculo independiente | Que un código distinto del de referencia sea correcto en otros casos |
| `test_rag.py` (5 pruebas) | Funcionamiento de permisos, cita y abstención en un recuperador por coincidencia de términos | Efectividad de un RAG real: son 7 preguntas escritas contra 3 documentos creados para la prueba. No hay embeddings, modelo ni evaluación de respuestas generadas |

Una cosa es que el código se ejecute, otra que el resultado sea reproducible, otra que la lógica sea correcta y otra que sea válida en un contexto empresarial. Estas pruebas cubren las dos primeras y parte de la tercera.

## Estado de las validaciones

| Validación | Estado | Detalle |
|---|---|---|
| Pruebas con Python 3.12.3, pandas 3.0.2, SQLite 3.45.1 | EJECUTADA (43 pruebas, OK) | 16/10/2026, entorno local de preparación |
| Cuaderno `notebooks/01_pipeline_paso_a_paso.ipynb` | EJECUTADO (celdas de código, con Python) | No se abrió en Jupyter |
| Medidas DAX (`powerbi/medidas_otd.dax`) | NO EJECUTADAS | La lógica equivalente se verifica con pandas y SQL; falta probarlas en Power BI Desktop |
| Instalación con `pip install` (a un directorio temporal) y comando `agronova` | VERIFICADA | Solo en este entorno (setuptools 68.1.2) |
| `.devcontainer`, matriz de GitHub Actions y diagramas Mermaid de `docs/16` | NO COMPROBADOS | Requieren publicar el repositorio |
| Cifras del caso frente a `data/cifras_canonicas.json` | VERIFICADO EXPERIMENTALMENTE | Una prueba compara el código con la fuente de verdad de las cifras |
| Sintaxis compatible con Python 3.9 (34 archivos `.py`, con `ast`) | VERIFICADA (solo sintaxis) | No prueba que las librerías ni el comportamiento sean iguales |
| Ejecución en Python 3.9 a 3.11 | PENDIENTE | Ejecutar `python -m unittest discover -s tests` en cada versión |
| pandas 2.x | PENDIENTE | Declarado `pandas>=2.0` sin haberse probado |
| GitHub Actions | PENDIENTE | El flujo no se ha ejecutado. Subir el repositorio y revisar la pestaña Actions |
| Renderizado de diagramas Mermaid | PENDIENTE | Abrir `docs/diagramas.md` en GitHub y comprobar los tres diagramas |
| Plantillas de `examples/` | NO PROBADAS | Dependen de un ERP, un Excel y una API reales |
| Búsqueda de credenciales | REALIZADA | Búsqueda de patrones (clave, token, contraseña) sin coincidencias. No sustituye una herramienta dedicada |
| Datos sensibles | SIN DATOS REALES | Todos los datos son sintéticos |
| Licencia | PENDIENTE | La define el autor antes de publicar |

## Qué requeriría una implementación productiva

Almacenamiento persistente y transaccional de las tres capas; MERGE o sobrescritura de particiones con manejo de reprocesos; orquestación con reintentos y dependencias; registro, observabilidad y alertas hacia un responsable; pruebas de calidad de datos en la propia plataforma; control de versiones, ambientes y despliegue; gestión de secretos; control de acceso de mínimo privilegio; y monitoreo de costos.
