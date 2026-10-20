# 0003. Presentar Medallion como patrón, no como garantía

**Contexto.** Medallion se suele presentar como sinónimo de «datos de calidad». La página oficial de Microsoft lo describe como un patrón de diseño y el enfoque recomendado para Fabric, pero no afirma que garantice calidad ni que sus capas sean intercambiables.

**Decisión.** Se usa Medallion para organizar el caso y se afirma solo lo que la fuente respalda. La advertencia de que la calidad la dan las validaciones es una recomendación propia, y está etiquetada como tal.

**Alternativas.** Presentarlo como estándar universal (no está respaldado); no usarlo (perdería su valor didáctico).

**Consecuencias.** Se evitó una afirmación errónea que sí apareció en una versión anterior del material (ver `CHANGELOG.md`). Quien consulte la fuente verá que el texto coincide.
