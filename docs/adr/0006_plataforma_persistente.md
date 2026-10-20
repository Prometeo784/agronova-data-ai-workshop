# 0006. Una mini plataforma persistente además de funciones sueltas

**Contexto.** Las funciones sueltas (`ingesta.py`, `silver.py`, `gold.py`) enseñan cada paso, pero trabajan en memoria: no muestran estado entre corridas, marca de agua guardada, fallos a mitad ni reproceso.

**Decisión.** `plataforma.py` compone esas funciones sobre SQLite: tablas por capa, tabla de control, registro de corridas, transacción única por corrida y reproceso desde Bronze. `simulador.py` hace evolucionar la fuente durante varios días.

**Alternativas.** Dejar solo las funciones (más simple, menos realista); usar un orquestador como Airflow (más realista, mucho más pesado).

**Consecuencias.**
- (+) Se pueden demostrar con pruebas la atomicidad, la idempotencia, el reproceso y los cambios de esquema.
- (−) SQLite no es un motor distribuido y la simulación es una sola persona sin concurrencia.
- (−) Aumenta el código que hay que mantener (ver `docs/09_alcance_y_validacion.md`).
