# 0002. SQLite y pandas en lugar de una plataforma en la nube

**Contexto.** La audiencia está aprendiendo y no puede depender de cuentas, licencias ni conexión.

**Decisión.** El código usa pandas y SQLite, que vienen con Python o se instalan en segundos. Fabric y Power BI aparecen como correspondencia documentada (`docs/14`), no como requisito.

**Alternativas.** Spark o una base en la nube (más realistas, pero excluyen a quien no tiene acceso); contenedores con una base real (más pesados).

**Consecuencias.**
- (+) Cualquiera ejecuta todo en minutos.
- (−) No demuestra concurrencia, escala ni comportamiento de un motor productivo.
- (−) Los conceptos se transfieren, pero el código no es una referencia de producción.
