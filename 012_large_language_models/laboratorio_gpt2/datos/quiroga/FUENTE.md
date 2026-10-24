# Fuente del corpus de Quiroga

`corpus.jsonl` es una copia, sin cambios, del corpus de una unidad optativa de cursadas anteriores. Suma de verificación `shasum`: `4317786c2fe696b96302a2a12da1550d6ffe9d99`.

## Qué contiene

26 cuentos de Horacio Quiroga tomados de es.wikisource.org. Cada línea es un cuento con los campos `id`, `titulo`, `autor`, `volumen`, `grupo`, `fuente`, `fuente_url`, `revid`, `palabras` y `texto`.

| Grupo | Volumen (según Wikisource) | Cuentos | Palabras |
|---|---|---|---|
| `adulto` | Cuentos de amor de locura y de muerte | 18 (el volumen completo) | 49.271 |
| `infantil` | Cuentos de la selva para los niños | 8 (el volumen completo) | 17.625 |

El criterio de agrupación es **externo**: lo define el volumen y su destinatario, no el vocabulario.

## Condiciones de uso

**Dominio público.** Quiroga murió en 1937, así que su obra está en dominio público. La transcripción de Wikisource es una edición colaborativa: la fidelidad al original depende de quienes la transcribieron. Cada cuento guarda el `revid` de Wikisource con el que se descargó.

## Cuentos reservados

Dos cuentos, uno por grupo, se apartan para **validación** y no los ve el ajuste:

| Grupo | `id` | Cuento |
|---|---|---|
| `adulto` | `adulto_07` | La gallina degollada |
| `infantil` | `infantil_04` | La abeja haragana |

Se eligieron en esa unidad **antes de mirar ningún resultado**: el cuento cuyo largo en palabras queda más cerca de la mediana de su grupo (desempate: el más largo). Si se cambian, hay que decidirlo antes de ver cualquier medida.

## Limitaciones conocidas

- Se pierden los subtítulos y numeraciones internas y algunas líneas de cartas dentro de los cuentos.
- Ortografía de época (`fué`, `dió`) sin normalizar.
- Wikisource fecha ambos volúmenes en 1918; no se verificó la fecha de primera edición.
- Es poco texto (unas 67.000 palabras, unos 95.000 tokens) y de un solo autor, de una época y una región (el Litoral rioplatense de principios del siglo XX). Lo que se genere con él hereda esa voz y no representa «el español».

## Cómo se obtuvo

Los scripts de descarga y construcción (`descargar.py`, `construir_corpus.py`) están en `012_maquinas_que_escriben/datos/`. Esta unidad no vuelve a descargar nada.
