# Autoevaluación

Quince preguntas para comprobar lo aprendido. Responde primero por tu cuenta y despliega la respuesta después. Las respuestas resumen lo que dicen los demás documentos; si dudas, vuelve a ellos.

**1. ¿Por qué «un dashboard con IA» no es un problema?**
<details><summary>Respuesta</summary>Es una solicitud. El problema es una decisión que hoy se toma mal o tarde. Se aclara con tres preguntas: qué decisión se quiere mejorar, quién la toma y con qué datos.</details>

**2. ¿De dónde sale la frecuencia con que debe actualizarse un dato?**
<details><summary>Respuesta</summary>De la decisión que apoya, no de la tecnología. Si la decisión se toma por turno o por día, un proceso diario por lotes suele bastar.</details>

**3. ¿Qué diferencia hay entre capital liberado y ahorro?**
<details><summary>Respuesta</summary>El capital liberado es dinero que deja de estar inmovilizado. El beneficio financiero es solo el costo de capital de ese dinero. Confundirlos exagera el valor.</details>

**4. ¿Qué significa que un MVP esté «terminado»?**
<details><summary>Respuesta</summary>Que las cifras están conciliadas con la fuente, aprobadas por el usuario y en uso, con alertas y línea base. No basta con que el código corra.</details>

**5. ¿Qué hace cada capa de Medallion?**
<details><summary>Respuesta</summary>Bronze conserva los datos como llegan, Silver corrige, estandariza y elimina duplicados, y Gold se organiza para reportes. Es un patrón de diseño; la calidad la dan las validaciones, no los nombres de las capas.</details>

**6. ¿Qué diferencia hay entre deduplicar y ser idempotente?**
<details><summary>Respuesta</summary>Deduplicar quita filas repetidas de un conjunto. Idempotente es que ejecutar el mismo proceso varias veces deje el mismo resultado en el destino. Una carga seria también necesita ser atómica: si falla a mitad, no queda nada a medias.</details>

**7. ¿Por qué pueden cuadrar los conteos y aun así estar mal el dato?**
<details><summary>Respuesta</summary>Si una regla errónea envía registros válidos a cuarentena, Bronze sigue siendo igual a Silver más cuarentena. Lo delata el porcentaje en cuarentena frente a su valor habitual (umbral).</details>

**8. ¿Por qué el OTD debe incluir las líneas vencidas que aún no llegaron?**
<details><summary>Respuesta</summary>Si no, el indicador solo mira lo que llegó y resulta más optimista de lo real. En el ejemplo, el proveedor C pasa de 82.9 % a 70.0 %.</details>

**9. ¿Qué enseña el caso de Mars Climate Orbiter?**
<details><summary>Respuesta</summary>Que la unidad es parte del contrato de datos y que las interfaces deben validarse con pruebas de extremo a extremo. El error fue un desajuste de unidades, no un fallo de cálculo.</details>

**10. ¿Qué no se sabe del caso de Air Canada?**
<details><summary>Respuesta</summary>No se sabe si su chatbot usaba RAG: la decisión del tribunal no da información sobre su tecnología. Lo documentado es que el tribunal responsabilizó a la empresa por lo que dijo el chatbot.</details>

**11. ¿Cuándo usar SQL y cuándo RAG?**
<details><summary>Respuesta</summary>SQL o BI para cifras exactas y reproducibles; RAG para encontrar y citar texto en documentos.</details>

**12. ¿Garantiza RAG una respuesta correcta?**
<details><summary>Respuesta</summary>No. Recuperar un documento no garantiza una respuesta correcta, y RAG no elimina las alucinaciones. Se evalúan por separado el recuperador y la respuesta, y el sistema debe abstenerse sin evidencia.</details>

**13. ¿Por qué el filtro de permisos va antes de construir el contexto?**
<details><summary>Respuesta</summary>Porque un fragmento restringido que llega al contexto puede filtrarse en la respuesta. Filtrar después ya es tarde.</details>

**14. ¿Cómo se controla un cambio de alcance?**
<details><summary>Respuesta</summary>Se registra, se estima su costo y su fecha, y se decide quién lo aprueba. Si no entra ahora, va al backlog.</details>

**15. Un modelo funciona, pero nadie lo usa. ¿Qué falló?**
<details><summary>Respuesta</summary>La adopción. Entregar no es adoptar: hay que diseñarla desde el inicio con usuarios clave, validación de cifras, capacitación, integración al proceso y una revisión periódica, y medir el uso.</details>
