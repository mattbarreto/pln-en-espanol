# FUENTE — datos de la unidad 009

Leelo antes de usar los archivos de esta carpeta. Ningún número que salga de ellos significa nada
si no sabés qué tenés entre manos.

## Qué hay acá

| Archivo | Qué es |
|---|---|
| `fragmentos.csv` | 137 fragmentos de 34 textos literarios (cuentos y minicuentos). Columnas: `id`, `texto`, `autor`, `titulo`, `fuente`, `palabras`. |
| `consultas.csv` | 10 consultas con su tipo y su criterio de relevancia. |
| `juicios_de_relevancia.csv` | 83 juicios: `id_consulta`, `id_fragmento`, `relevancia` (2 = relevante, 1 = parcial), `justificacion`, `discutible`. Lo que no figura vale 0. |
| `stopwords_es.txt` | Lista de 260 palabras vacías de la unidad 003 (`003_text_mining/practico/datos/`). |
| `construir_fragmentos.py` | En la unidad 009: regenera `fragmentos.csv` a partir de `cuentos_latinoamericanos.csv`. |

## Procedencia de los textos

* **Compilado:** `cuentos_latinoamericanos.csv`, de Karen Palacio (<https://github.com/karen-pal/borges>), que a su vez proviene de ciudadseva.com. Es la misma copia que usan las unidades 004 y 006; la unidad 009 la incluye en `datos/` para poder regenerar `fragmentos.csv`.
* **Selección:** 34 textos que elegimos nosotros entre los cuentos y minicuentos de entre 140 y 420 palabras que no tenían un duplicado exacto, para cubrir temas que permitieran armar consultas con relevancia comprobable. **No es una muestra al azar.** Los criterios se pueden leer en `construir_fragmentos.py`.
* **Fecha de acceso:** octubre de 2026 (copia local ya existente en la unidad 006). No volvimos a consultar ciudadseva.com.
* **Cada fragmento** guarda en `fuente` el enlace del texto original.

## Qué se transformó

* Los textos originales vienen en una sola línea, sin párrafos. Los partimos en oraciones con una expresión regular y juntamos oraciones consecutivas hasta llegar a 45 palabras o más. **El corte es nuestro**, no del autor. La expresión regular puede cortar mal en abreviaturas.
* No se corrigió ortografía de época ni errores de transcripción. Algunos textos conservan marcas del sitio (por ejemplo `FIN`, o notas de edición al final).
* Un fragmento puede empezar o terminar en medio de una escena.

## Los juicios de relevancia

* **Quién:** los redactó quien armó la unidad, leyendo los 137 fragmentos. **No hubo segunda evaluación.** No hay medida de acuerdo entre evaluadores.
* **Cuándo:** se fijaron el 7 de octubre de 2026 (17:24 UTC) y no se modificaron después de calcular ningún ranking. Los primeros 16 caracteres del SHA-256 del archivo, a esa fecha, son `9e217d46f9337000`; el cuaderno 05 imprime el valor actual para poder compararlo.
* **Qué significan:** 2 = el fragmento responde a la consulta según el criterio escrito en `consultas.csv`; 1 = parcialmente; 0 (sin fila) = no.
* **`discutible = sí`:** 39 de los 83 juicios están marcados así. No indican un error: indican que una persona razonable podría decidir otra cosa.
* **Si se modifican:** el hash cambia. Hay que registrar la fecha y la razón del cambio, y no comparar con resultados anteriores como si fueran lo mismo.

## Límites conocidos

* **Autores:** 12, todos varones. La colección de origen incluye autoras (por ejemplo, Clarice Lispector) que no entraron en nuestra selección. La colección no es representativa de la literatura latinoamericana ni de ninguna otra cosa.
* **Géneros:** muchos textos son humorísticos, alegóricos o experimentales. Una colección así hace difícil la consulta literal y favorece la figurada.
* **Tamaño:** con 10 consultas y 137 fragmentos no se pueden establecer diferencias generales entre representaciones.
* **Truncamiento:** 10 de los 137 fragmentos superan los 128 tokens que lee el modelo de oraciones del cuaderno 04.

## Licencia y derechos

* Los derechos de los textos pertenecen a sus autores o a sus herederos. Los fragmentos son extractos breves con fines didácticos.
* `fragmentos.csv` se puede regenerar con `construir_fragmentos.py` a partir de la copia local del compilado.
* `fragmentos.csv`, `consultas.csv` y `juicios_de_relevancia.csv` son material del curso, de uso educativo.

## Vectores y modelos que usa la unidad

Ver `datos/vectors/README.md` para los archivos. Fichas verificadas el 7 de octubre de 2026:

| Recurso | Quién | Licencia | Dato clave |
|---|---|---|---|
| Spanish Billion Words Corpus and Embeddings | Cristian Cardellino, marzo de 2016 | CC BY-SA 4.0 | Skip-gram, 300 dimensiones, ~1.500 millones de palabras |
| Vectores fastText de Wikipedia (`wiki.es`) | Facebook AI Research (Bojanowski y otros, 2017) | CC BY-SA 3.0 | Skip-gram con subpalabras, 300 dimensiones, entrenados en Wikipedia |
| `paraphrase-multilingual-MiniLM-L12-v2` | Proyecto Sentence-Transformers | Apache 2.0 | 384 dimensiones, 128 tokens, sin prefijos |
| `intfloat/multilingual-e5-large` (extensión A) | Wang y otros | MIT | 1024 dimensiones, 512 tokens, prefijos obligatorios |
| `BAAI/bge-m3` (extensión A) | BAAI | MIT | 1024 dimensiones, 8192 tokens, sin instrucciones |
