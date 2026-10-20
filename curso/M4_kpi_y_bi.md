# M4. KPI y BI

**Objetivo.** Pasar de una definición de negocio a una medida, distinguiendo definición e implementación, y comprobar el resultado.

**Prerrequisitos.** M3.

**Lee.** `docs/01_caso_agronova.md` (§8), `docs/14_fabric_y_power_bi.md` (§3 y §4), `powerbi/medidas_otd.dax`.

**Haz.**
1. Ejecuta `python scripts/exportar_capas.py` y abre `data/exportadas/` en Power BI o Excel (procedimiento en `docs/14`).
2. Reproduce el OTD correcto y el ingenuo; explica por qué difieren para el proveedor C.
3. Resuelve el ejercicio 1 (`ejercicios/ejercicio_01_tolerancia.py`) y explica qué cambia en la definición.

**Comprobación.** `python curso/checkpoint.py M4` (usa las soluciones de referencia si todavía no completaste el ejercicio: `USAR_SOLUCIONES=1`).

**Errores comunes.** Dejar fuera del denominador lo que no llegó; cambiar la definición en un solo reporte.

**Siguiente.** M5.
