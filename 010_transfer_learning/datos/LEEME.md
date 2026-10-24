# Procedencia de los datos

## Qué se usa en cada cuaderno

| Archivo | Cuaderno | Uso |
|---|---|---|
| `corpus.json`, `consultas.json` | 01 | Puente de la sección 1: búsqueda literal que falla con paráfrasis |
| `aviso_ner.txt` | 01 | Entidades nombradas (sección 3) |
| `politicas_biblioteca.md` | 01 | Pregunta-respuesta extractiva (sección 4) |
| `clasificacion.json` | 02 | Tres etiquetas, 36 avisos, particiones fijas |
| `martin_fierro.csv` | 03 | 2316 versos; comparación inicial de unidades |
| `martin_fierro_estrofas.csv` | 03 | 395 estrofas; unidad del entrenamiento y la prueba |

## Textos sintéticos (CC0-1.0)

`corpus.json`, `consultas.json`, `clasificacion.json`, `aviso_ner.txt` y `politicas_biblioteca.md` son textos sintéticos elaborados para esta unidad. No son documentos institucionales reales ni fragmentos de autores, no contienen datos personales y se ofrecen bajo CC0-1.0. Las personas, organizaciones y lugares de `aviso_ner.txt` y `politicas_biblioteca.md` son ficticios.

`politicas_biblioteca.md` no menciona multas ni costos a propósito: la pregunta sobre la multa, en el cuaderno 01, muestra que el modelo responde aunque el contexto no tenga la respuesta.

Las categorías educación, movilidad y salud son una convención didáctica. Hay casos fronterizos: vacunación en escuelas y actividades culturales. Los textos son pocos y no permiten estimar rendimiento productivo.

Las particiones de `clasificacion.json` están fijadas por ID antes del entrenamiento. Las respuestas relevantes de `consultas.json` están anotadas a mano. Las respuestas esperadas de QA y las entidades esperadas del aviso son decisiones didácticas, discutibles. No se deben cambiar después de mirar resultados sin registrar una nueva versión.

## *Martín Fierro*: dos unidades del mismo material

`martin_fierro.csv` contiene 2316 versos en minúsculas; `martin_fierro_estrofas.csv` contiene 395 estrofas reunidas, con otra capitalización y puntuación. Ambos tienen una columna `samples`. No son dos corpus independientes ni se deben mezclar entre train y test. El archivo comienza con «Aquí me pongo a cantar» y termina con «pero que naides contó»: corresponde a *El gaucho Martín Fierro* (1872), de José Hernández, en dominio público. No contiene *La vuelta de Martín Fierro* (1879).

Los dos CSV son copias sin editar de `datasets/martin_fierro.csv` y `datasets/martin_fierro_v2.csv` del taller «Modelos de lenguaje a tu medida» (2.º Workshop Argentino de NLP, FAMAF-UNC / Fundación Vía Libre, 2023; licencia MIT). No se cotejaron contra una edición impresa: la selección, transcripción, separación y puntuación pueden diferir de otras ediciones. En el cuaderno 03 se reservan 50 estrofas para prueba, se usan 200 para entrenamiento y 145 no intervienen.
