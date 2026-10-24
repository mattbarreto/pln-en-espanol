# Procedencia de los datos

## Qué se usa en cada cuaderno

| Archivo | Cuaderno | Uso |
|---|---|---|
| `politica_interna_tintas_acme.pdf` | 01, 03, 04 | PDF limpio de dos páginas: carga, fragmentos y RAG con fuentes. |
| `politica_trabajo_remoto_tintas_acme.md` | 01, 03 | Markdown con títulos: corte por secciones y actualización del índice. |
| `ria_semillas_conservadas.pdf` | 01 | PDF real de revista, de cuatro páginas y dos columnas: palabras cortadas, cabeceras y recuadros. |
| `cuentos/fragmentos.csv` | 01, 02, 04 | 137 fragmentos de cuentos con autor y título. |
| `cuentos/consultas.csv` y `cuentos/juicios_de_relevancia.csv` | 02, 04 | 10 consultas y 83 juicios de relevancia para evaluar la recuperación. |
| `cuentos/FUENTE.md` | (lectura) | Procedencia, transformaciones y límites de los cuentos, tal como los documenta la unidad 009. |

## Documentos de Tintas Acme (ficticios)

La política interna (PDF) y la de trabajo remoto (Markdown) describen una empresa que no existe, «Tintas Acme S.A.», y las creó el equipo del curso con fines educativos. No contienen datos personales. El PDF está escrito sin tildes porque así se generó. **Pendiente:** definir y declarar la licencia de estos dos archivos.

## Artículo del INTA

`ria_semillas_conservadas.pdf` es una copia local de «Semillas conservadas para un futuro sostenible», de Laura Pérez Casar, publicado en *RIA. Revista de Investigaciones Agropecuarias* (INTA), vol. 42, n.º 1, abril de 2016, pp. 19 a 22. El nombre original del archivo es `RIA_2016_VOLUMEN 42_Nº1_p.19-22.pdf`. Se usa para mostrar cómo se ve un PDF maquetado al extraer su texto. **La licencia de redistribución no está verificada:** antes de publicar el repositorio hay que confirmarla o reemplazar el archivo por uno con licencia abierta.

## Cuentos (unidad 009)

`cuentos/` es una copia sin cambios de `009_representaciones_semanticas/datos/`: fragmentos de 34 cuentos y minicuentos latinoamericanos, compilados a partir de ciudadseva.com. Los derechos de los textos pertenecen a sus autores o a sus herederos, y los extractos son breves y con fines didácticos. **La licencia de redistribución del compilado no está verificada.** Los juicios de relevancia los redactó una persona con asistencia de un modelo de lenguaje, sin segunda evaluación; 39 de 83 son discutibles. Todo está explicado en `cuentos/FUENTE.md`.

## Archivos que genera la unidad

`chroma_db/` (cuadernos 02 y 03) es la base vectorial persistente. Se puede borrar: los cuadernos la recrean.
