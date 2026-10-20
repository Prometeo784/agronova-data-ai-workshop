# 0001. Usar solo datos y casos sintéticos

**Contexto.** El material nace de una experiencia profesional con datos empresariales confidenciales. Publicarlos, o algo que permita reconstruirlos, es inaceptable.

**Decisión.** Todos los datos, empresas y cifras son inventados y se declaran así. Los datos se generan con código determinista (`fuentes.py`) para que cualquiera obtenga los mismos resultados.

**Alternativas.** Anonimizar datos reales (riesgo de reidentificación y de revelar reglas de negocio); usar un conjunto público (no encaja con el caso).

**Consecuencias.**
- (+) No hay riesgo de fuga y todo es reproducible.
- (−) Las pruebas demuestran que el código hace lo que dice, **no** que sea válido en una empresa real. Está declarado en `docs/09_alcance_y_validacion.md`.
- (−) Los datos se diseñaron para reproducir las cifras del caso, así que las pruebas son en parte circulares.
