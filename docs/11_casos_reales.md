# Tres casos reales documentados

Casos públicos que ilustran, con evidencia, lo que este repositorio enseña con datos ficticios. Consultados el 16 de octubre de 2026. **Las etiquetas distinguen lo que dicen las fuentes de lo que se infiere de ellas.** Nada de esto es experiencia propia del autor.

| Caso | Lo que ilustra | Control equivalente en AgroNova |
|---|---|---|
| Mars Climate Orbiter (1999) | Un desajuste de unidades entre sistemas | Contrato de datos y normalización de unidades (`contrato.py`, Silver) |
| Casos de COVID-19 no incluidos en Inglaterra (2020) | Una pérdida silenciosa de registros en una carga | Reconciliación de conteos y alertas (`control.py`, `observabilidad.py`) |
| Air Canada y su chatbot (2024) | Responsabilidad por lo que responde un asistente | Cita, abstención y responsabilidad humana (`rag.py`) |

## 1. Mars Climate Orbiter: la unidad es parte del contrato

**Qué ocurrió** `[DOCUMENTADO · informe de la junta de investigación de la NASA]`
- La sonda se perdió el 23 de septiembre de 1999, al entrar en la atmósfera de Marte en una trayectoria más baja de lo previsto.
- La junta determinó como causa raíz que un archivo de software en tierra entregaba datos de impulso en libras-fuerza por segundo, cuando la especificación de interfaz exigía newton por segundo. El procesamiento posterior subestimó el efecto por un factor de 4.45.
- El informe también señala, entre las causas que contribuyeron, que la verificación y validación no abordó de forma adecuada el software de tierra, que no se hizo una prueba de extremo a extremo de ese software y que las discrepancias se reportaron por correo y no por el proceso formal de anomalías.

**Lección técnica** `[INFERENCIA]` Los sistemas no solo intercambian valores: intercambian unidades, formatos y supuestos. Si el contrato de la interfaz no se valida en código y con pruebas de extremo a extremo, un error pequeño y constante se acumula sin que nada falle.

**En AgroNova** La unidad llega como `"uni."`, `"UN "` o `"kg"` y se normaliza en Silver. `contrato.py` valida que solo existan unidades válidas, y una unidad desconocida va a cuarentena.

**Límites** Es un caso aeroespacial, no empresarial. La analogía es sobre interfaces y unidades; no permite estimar costos ni frecuencia de este tipo de error en proyectos de datos.

**Fuente** [NASA, Mars Climate Orbiter Mishap Investigation Board, Phase I Report, 10/11/1999](https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf). Documento leído completo.

## 2. Casos de COVID-19 no incluidos: el dato que se pierde sin error

**Qué ocurrió**
- `[DOCUMENTADO · declaración de Public Health England, reproducida por la prensa]` Un problema técnico en el proceso de carga hizo que 15,841 casos, entre el 25 de septiembre y el 2 de octubre de 2020, no se incluyeran en las cifras diarias. Los casos pendientes se transfirieron a los rastreadores de contactos a la 1:00 del 3 de octubre.
- `[REPORTADO POR MEDIOS, no confirmado en un informe oficial que haya leído]` La causa habría sido que archivos de resultados de laboratorio superaron el límite de filas del formato Excel antiguo (.xls, 65,536 filas) usado en la carga. Se informó que la solución fue dividir los archivos en lotes más pequeños. La declaración oficial habló de un problema de «tamaño de archivo».

**Lección técnica** `[INFERENCIA]` Una carga puede terminar sin error y descartar datos. Comparar los conteos del origen con los del destino, y alertar por volumen, habría hecho visible la pérdida. Los formatos con límites implícitos son un riesgo en una carga automática.

**En AgroNova** Es el mismo patrón de «pipeline verde, dato incorrecto»: `reconciliar` compara Bronze con Silver más cuarentena, y `metricas_corrida` alerta cuando la cuarentena supera un umbral.

**Límites** El detalle técnico proviene de la prensa. No se conoce el diseño completo del sistema y no debe usarse para afirmar qué proceso exacto falló.

**Fuentes** [The Register, 5/10/2020](https://www.theregister.com/2020/10/05/excel_england_coronavirus_contact_error/) y [Digital Health, 8/10/2020](https://digitalhealth.net/?p=108775). Ambas son secundarias.

## 3. Air Canada y su chatbot: quien publica es responsable

**Qué ocurrió** `[DOCUMENTADO · decisión del Civil Resolution Tribunal de Columbia Británica, 14/02/2024]`
- Un chatbot del sitio de Air Canada indicó a un cliente que podía solicitar una tarifa por duelo de forma retroactiva. Otra página del mismo sitio decía que esa política no aplicaba a solicitudes posteriores al viaje.
- Air Canada sostuvo que no era responsable de lo que dijera el chatbot. El tribunal lo rechazó: consideró que el chatbot es parte del sitio y que la empresa es responsable de toda la información que publica. Concluyó que no tomó el cuidado razonable para asegurar que su chatbot fuera exacto, y ordenó pagar en total 812.02 dólares canadienses.

**Lección técnica** `[INFERENCIA]` Un asistente que responde con información de la empresa compromete a la empresa. Hace falta coherencia entre las fuentes, citas verificables, abstención cuando no hay evidencia y una persona responsable de la calidad.

**En AgroNova** `rag.py` cita la fuente y se abstiene sin evidencia suficiente; el documento `04_rag_y_gobernanza.md` insiste en que una alerta o una respuesta automática no sustituye la responsabilidad humana.

**Límites** La decisión indica que Air Canada no aportó información sobre la naturaleza de su chatbot: **no se sabe si usaba RAG**. Es un caso de responsabilidad legal, no una evaluación técnica de ningún sistema.

**Fuente** [Moffatt v. Air Canada, 2024 BCCRT 149](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do). Decisión leída completa.

## Cómo usarlos en una discusión

1. ¿Qué control habría hecho visible el problema antes de que causara daño?
2. ¿Quién era el dueño del dato, de la interfaz o de la respuesta?
3. ¿Qué evidencia falta para afirmar la causa con certeza?
