# Ejercicios

Tres ejercicios para practicar lo visto en la sesión. Cada uno tiene un archivo inicial con una función por completar; **la solución está en `soluciones/`**, pero intenta resolverlos antes de mirarla.

| Ejercicio | Qué practicas | Archivo |
|---|---|---|
| 1. Tolerancia | Cambiar la definición de un KPI sin romper la regla del denominador | `ejercicio_01_tolerancia.py` |
| 2. Alerta por volumen | Detectar una carga que trae muy pocas o demasiadas filas | `ejercicio_02_alerta_volumen.py` |
| 3. Proveedores válidos | Añadir una regla de contrato de datos | `ejercicio_03_proveedores_validos.py` |

## Cómo comprobar tu solución

```bash
python ejercicios/comprobar.py                       # comprueba tus funciones
USAR_SOLUCIONES=1 python ejercicios/comprobar.py     # comprueba las soluciones de referencia
```

Mientras una función siga sin completar, el comprobador la marca como pendiente. No hay una única forma correcta de escribirla: se comprueba el resultado, no el estilo.

Los datos son sintéticos. Que tu código pase estas comprobaciones no demuestra que sea válido para datos reales.
