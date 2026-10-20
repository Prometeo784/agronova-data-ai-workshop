# M3. Un pipeline en el que se puede confiar

**Objetivo.** Distinguir deduplicar de ser idempotente, reconocer una carga atómica, y detectar un «pipeline verde con dato incorrecto».

**Prerrequisitos.** M2.

**Lee.** `docs/16_plataforma_persistente.md`, `docs/11_casos_reales.md`, `src/agronova/plataforma.py`.

**Haz.**
1. Ejecuta `python scripts/simular_plataforma.py --dias 6` y explica qué pasó cada día y por qué.
2. Ejecuta `python scripts/simular_plataforma.py --dias 1 --regla-defectuosa --reprocesar` y compara antes y después.
3. Rompe algo a propósito (por ejemplo, la regla de cantidad en `silver.py`) y observa qué prueba falla.
4. Haz los ejercicios 2 y 3 de `ejercicios/`.

**Comprobación.** `python curso/checkpoint.py M3`

**Errores comunes.** Actualizar la marca de agua antes de confirmar la carga; confiar en que los conteos cuadran.

**Siguiente.** M4.
