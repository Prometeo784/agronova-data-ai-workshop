# Seguridad, costos y operación

Recomendaciones generales `[RECOMENDACIÓN]`. Los detalles dependen de la plataforma, la normativa y el presupuesto de cada organización; no sustituyen la documentación oficial de tu proveedor.

| Tema | Qué significa | Ejemplo en AgroNova | Cómo se verifica | Error frecuente |
|---|---|---|---|---|
| Mínimo privilegio | Cada persona accede solo a lo necesario | Operaciones no ve precios; Compras y Finanzas sí | Revisión periódica de roles | Dar acceso total «por rapidez» |
| Secretos | Las credenciales no viven en el código | `ERP_DB_URL` y `LOGISTICA_TOKEN` en variables de entorno o un gestor de secretos | Búsqueda de credenciales en el repositorio y en el historial | Subir un `.env` o una clave |
| Ambientes | Desarrollo, pruebas y producción separados | Las pruebas usan datos sintéticos, nunca los del ERP productivo | Datos y permisos distintos por ambiente | Probar contra producción |
| Datos sensibles | Se minimizan, enmascaran o excluyen | Se excluyen datos personales de contactos del proveedor | Inventario de campos sensibles | Copiar tablas completas «por si acaso» |
| Auditoría | Quién consultó o cambió qué y cuándo | Registro de acceso a Gold y a los documentos del RAG | Revisión de registros y alertas | No registrar nada |
| Permisos en RAG | Los fragmentos heredan los permisos del documento | El filtro actúa antes de ordenar (ver `src/agronova/rag.py`) | Pruebas con usuarios sin permiso: no debe aparecer ningún fragmento restringido | Filtrar después de generar la respuesta |
| Costos de cómputo y almacenamiento | Se miden y se comparan con lo previsto | Alerta si el consumo mensual supera el presupuesto | Panel de consumo y revisión mensual | Descubrir el costo en la factura |
| Costo de inferencia | Costo por consulta de un modelo de lenguaje | Medir el costo por consulta antes de lanzar | Pruebas con consultas reales | Suponerlo en lugar de medirlo |

## Ejemplo del costo de inferencia `[EJEMPLO ILUSTRATIVO]`

Costo mensual = consultas al mes × costo por consulta. Con 10,000 consultas y un costo supuesto de USD 0.002 por consulta, el total sería USD 20. Con 1,000,000 de consultas sería USD 2,000. Las cifras son supuestos: se miden con el modelo y el volumen reales antes de lanzar.

## Límites de gasto y optimización

- Define un presupuesto y una alerta antes del despliegue.
- Optimiza con el uso real: revisa qué cargas y consultas consumen más antes de cambiar la arquitectura.
- Revisa el costo de operación en cada decisión de diseño: una solución más compleja cuesta más de mantener.
