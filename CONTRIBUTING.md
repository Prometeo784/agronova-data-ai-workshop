# Cómo contribuir

Este repositorio es material didáctico. Las contribuciones más útiles son **dudas, errores y mejoras de claridad**.

## Qué puedes aportar
- Un error en un documento, una cifra o una prueba (usa la plantilla «Error en el material»).
- Una duda que el material no resolvió (plantilla «Pregunta»). Si algo te confundió, probablemente confundirá a otros.
- Un ejercicio nuevo, con comprobación y solución de referencia.

## Reglas
1. **Solo datos y casos sintéticos o ficticios.** Nunca subas datos reales, nombres de empresas reales ni información confidencial.
2. **Distingue la evidencia.** Usa las etiquetas del README (`[DOCUMENTADO]`, `[RECOMENDACIÓN]`, `[EJEMPLO ILUSTRATIVO]`...). No afirmes como documentado lo que no leíste en la fuente.
3. **No inventes referencias ni resultados.** Si citas una fuente, enlázala y di cuándo la consultaste.
4. **Cada cambio de código lleva su prueba**, y `python scripts/ejecutar_todo.py` debe terminar en verde.
5. **Si cambias una cifra**, actualiza `data/cifras_canonicas.json` y busca todas sus apariciones (ver `docs/adr/0004_cifras_canonicas.md`).
