# 0004. Mantener las cifras en un archivo con una prueba de sincronía

**Contexto.** Las mismas cifras (OTD, cuarentena, valor) viven en el código, los documentos, las diapositivas y los ejercicios. Cambiar una en un sitio y olvidar otro es fácil.

**Decisión.** `data/cifras_canonicas.json` es la fuente de verdad. Una prueba compara el código con ese archivo; los documentos se revisan contra él.

**Alternativas.** Generar los documentos desde el archivo (más robusto, pero añade herramientas); confiar en la disciplina (no escala).

**Consecuencias.**
- (+) Si el código cambia una cifra, una prueba falla.
- (−) Los documentos y las diapositivas **no** se validan automáticamente: sigue haciendo falta una comprobación cruzada manual.
