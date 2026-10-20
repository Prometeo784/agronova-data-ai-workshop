# Caso integrador: AgroNova (empresa ficticia)

> **Aviso.** AgroNova es una empresa **ficticia** `[ELEMENTO FICTICIO PARA EL CASO]`. Todas las cifras son **simuladas** `[DATO SIMULADO PARA EJERCICIO]`. No reflejan datos, sistemas ni reglas de ningún empleador.

## 1. Problema y usuarios

**Solicitud superficial:** "Necesitamos un dashboard con IA para los proveedores".

**Problema real:** la planta se entera de que un proveedor falló cuando la línea ya se detuvo, y Finanzas compensa con inventario de seguridad que inmoviliza capital. No existe una vista confiable y única del desempeño de cada proveedor.

| Usuario | Decisión que debe mejorar | Pregunta concreta |
|---|---|---|
| Gerencia de Compras | A qué proveedor exigir acción correctiva o renegociar | ¿Quiénes cumplen y quiénes no, y por qué? |
| Operaciones y planta | Qué producción reprogramar | ¿Qué órdenes abiertas están en riesgo esta semana? |
| Finanzas | Cuánto inventario de seguridad mantener | ¿Dónde el colchón no se justifica por el riesgo real? |
| Control presupuestario (extensión) | Qué desviaciones anticipar | ¿Cuánto hemos comprometido frente al presupuesto? |

## 2. Requerimientos derivados de las decisiones

| Requerimiento | Valor propuesto | Se deriva de |
|---|---|---|
| Frescura de OC y recepciones | Diaria, antes de las 6:00 a. m. | La reprogramación se decide por turno o por día |
| Estado del transporte | Cada hora, si la API lo permite | Es la señal más temprana de retraso |
| Volumen | ~1,000 líneas de OC al mes, 35 proveedores | Dato simulado |
| Calidad | Cada KPI reconciliable con el ERP | Un número que Compras no reconoce no se usa |
| Seguridad | Costos y precios solo para Compras y Finanzas | Información comercial sensible |

`[RECOMENDACIÓN]` La frescura sale de la decisión, no de la moda tecnológica. Si Operaciones demuestra que necesita menos de un día, se revisa.

## 3. Fuentes

| Fuente | Formato | Frecuencia | Riesgo | Ingesta |
|---|---|---|---|---|
| ERP: OC, recepciones, maestros | Tablas SQL | Diaria | Impacto en el sistema productivo | Carga incremental por marca de agua |
| Inspecciones de calidad | Excel o CSV | Por lote | Duplicados y formatos libres | Plantilla única con validación |
| Portal logístico | API REST | Horaria | Límites de frecuencia y caídas | Paginación y reintentos |
| Presupuesto (extensión) | Excel de Finanzas | Mensual | Versiones paralelas | Carga controlada, con dueño |
| Contratos y políticas (extensión) | PDF o Word | Eventual | Versiones vigentes y permisos | Ver `04_rag_y_gobernanza.md` |

## 4. Arquitectura

La arquitectura se dimensiona por volumen, latencia, equipo y riesgo (ver `diagramas.md` y `02_arquitectura_y_tradeoffs.md`). AgroNova mueve unas 12,000 líneas de OC al año: cabe en un motor SQL o un warehouse pequeño.

**Medallion** es un patrón de diseño para organizar los datos por calidad creciente; Microsoft lo describe como el enfoque recomendado para Fabric `[DOCUMENTADO]`. No garantiza calidad por sí solo: la calidad depende de las validaciones que se implementen en cada capa `[RECOMENDACIÓN]`.

| Capa | Tablas de ejemplo | Reglas clave |
|---|---|---|
| Bronze | `brz_erp_oc_linea` | Copia fiel, sin corregir. Se añaden lote, fecha de carga y archivo de origen |
| Silver | `slv_oc_linea`, cuarentena | Tipado, deduplicación, unidades normalizadas, rechazos con motivo |
| Gold | hechos y dimensiones | Los KPI se definen una vez para que todos los reportes calculen igual |

## 5. Registro viajero: OC 100245, línea 1 `[REGISTRO FICTICIO]`

| Campo | Bronze (tal cual) | Silver (normalizado) | Gold (KPI) |
|---|---|---|---|
| Proveedor | "PROV C " | C | Dimensión proveedor C |
| Cantidad | "5.000" (texto) | 5000 | Suma de cantidades |
| Unidad | "uni." | UN | UN |
| Fecha prometida | 15/10/2026 | 2026-10-15 | 2026-10-15 |
| Fecha de recepción | 16/10/2026 | 2026-10-16 | 2026-10-16 |
| Resultado | n/d | válido | 1 día de retraso: no cuenta como a tiempo |

## 6. Reglas de calidad en Silver `[RECOMENDACIÓN]`

| Regla | Acción | Por qué |
|---|---|---|
| `id_proveedor` no nulo | Cuarentena | Sin proveedor no se atribuye el desempeño |
| Recepción posterior o igual a la emisión | Cuarentena | Una recepción no puede ocurrir antes de la orden |
| Cantidad recibida negativa | Cuarentena | Error de captura |
| Cantidad recibida igual a cero | **Conservar** y marcar | Una recepción rechazada o parcial puede tener cantidad cero |
| Unidad fuera de la lista válida | Normalizar o cuarentena | Una unidad cambiada distorsiona la calidad |
| Duplicado por OC, línea y recepción | Conservar el más reciente | Evita contar dos veces |

## 7. Pipeline verde, dato incorrecto

Con la regla defectuosa `cantidad > 0`, el proceso termina sin errores y los conteos reconcilian (938 + 62 = 1,000), pero 62 recepciones válidas quedan fuera. Lo delata el umbral de cuarentena: 6.2 % frente a un 0.3 % habitual. Pruébalo con `python scripts/ejecutar_pipeline.py`.

## 8. KPI: OTD correcto frente a ingenuo `[DATO SIMULADO PARA EJERCICIO]`

**OTD = líneas a tiempo ÷ todas las líneas vencidas del periodo, incluidas las que aún no llegaron.**

| Proveedor | Vencidas | A tiempo | Tarde | Sin recibir | OTD ingenuo | OTD correcto |
|---|---|---|---|---|---|---|
| A | 200 | 190 | 8 | 2 | 96.0 % | 95.0 % |
| B | 300 | 240 | 40 | 20 | 85.7 % | 80.0 % |
| C | 500 | 350 | 72 | 78 | 82.9 % | 70.0 % |
| Total | 1,000 | 780 | 120 | 100 | 86.7 % | 78.0 % |

Calidad (Quality Yield): 48,500 ÷ 50,000 = 97.0 %. Cubre solo lo inspeccionado.

## 9. Valor `[TODO ES SUPUESTO FICTICIO, NO UN BENCHMARK]`

| Supuesto o cálculo | Valor |
|---|---|
| Inventario de seguridad (línea base) | USD 400,000 |
| Reducción objetivo del 10 %: capital liberado | USD 40,000 |
| Beneficio anual por costo de capital (12 %): 40,000 × 12 % | USD 4,800 |
| Paros evitados: 3 h × USD 3,000 | USD 9,000 |
| Beneficio total anual estimado | USD 13,800 |
| Costo de operación anual | USD 6,000 |
| Beneficio neto anual estimado | USD 7,800 |
| Costo de construcción (una vez) | USD 30,000 |
| Recuperación: 30,000 ÷ 7,800 | ≈ 3.8 años |

Los USD 40,000 son **capital liberado, no ahorro**. Sin los paros evitados, USD 4,800 no cubren los USD 6,000 de operación. Todo es **estimado**: solo se vuelve realizado si se mide contra la línea base. Una mejora posterior no prueba causalidad.
