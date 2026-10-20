# Métricas y cómo calcularlas

No hace falta usarlas todas. Elige las pertinentes y define su método. Los umbrales son **ejemplos**, no benchmarks.

| Categoría | Métrica | Método de cálculo |
|---|---|---|
| Ingeniería | Frescura | Hora actual menos hora de la última carga exitosa |
| Ingeniería | Tasa de fallos | Corridas fallidas ÷ corridas totales |
| Ingeniería | Cuarentena | Registros rechazados ÷ registros cargados |
| Ingeniería | Reconciliación | Diferencia entre el total de Gold y el de la fuente ÷ total de la fuente |
| BI y productos | Usuarios activos | Usuarios distintos por semana |
| BI y productos | Tiempo para obtener información | Tiempo medido antes y después, con la misma tarea |
| BI y productos | Uso en decisiones | Decisiones que citan el scorecard en las reuniones de revisión |
| IA y RAG | Relevancia de la recuperación | Proporción de preguntas de prueba cuyo fragmento correcto fue recuperado |
| IA y RAG | Fidelidad | Proporción de afirmaciones respaldadas por las fuentes citadas |
| IA y RAG | Abstención apropiada | Proporción de preguntas sin respuesta en los documentos que el sistema declina responder |
| IA y RAG | Latencia y costo por consulta | Tiempo y costo promedio medidos en pruebas |
| IA y RAG | Acceso no autorizado | Pruebas con usuarios sin permiso: ningún fragmento restringido debe aparecer |
| Negocio | Horas de paro por abastecimiento | Horas registradas antes y después |
| Negocio | Inventario de seguridad | Valor medido contra la línea base |
| Negocio | Beneficio realizado | Diferencia medida contra la línea base, menos costos de construcción y operación |

## Cuatro niveles

1. **Actividad:** qué se produjo (informes publicados).
2. **Técnicos:** cómo funciona (frescura, fallos, reconciliación).
3. **Adopción:** quién lo usa (usuarios activos, decisiones que citan el producto).
4. **Impacto:** qué cambió en el negocio (paros, inventario, costo de capital).

Horas liberadas no equivalen a ahorro realizado, y correlación no equivale a causalidad.
