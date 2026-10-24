# Clínica de errores

**Auditar una medición antes de creerle: el corpus Quiroga (volumen adulto vs. volumen infantil)**

26 cuentos de Horacio Quiroga (dominio público) tomados de es.wikisource.org.

| Grupo | Volumen (según Wikisource) | Cuentos | Palabras |
|---|---|---|---|
| `adulto` | Cuentos de amor de locura y de muerte | 18 (el volumen completo) | 49.271 |
| `infantil` | Cuentos de la selva para los niños | 8 (el volumen completo) | 17.625 |

El criterio de agrupación es **externo**: lo define el volumen y su destinatario, no el vocabulario.

## Cuaderno

| Cuaderno | Tema |
|---|---|
| `01_clinica.ipynb` | Clínica de errores: cinco mediciones sobre este corpus, cada una con un error para encontrar, probar y corregir |

Para correrlo hacen falta, en la misma carpeta, `corpus.jsonl`, `utils.py` y
`utils_visualizacion.py`. En Colab, subí esos archivos junto con el cuaderno.
Dependencias en `requirements.txt` (`uv pip install -r requirements.txt`).

## Reproducir
```
python descargar.py          # baja el HTML a crudo/ (1,5 s de pausa por pedido)
python construir_corpus.py   # genera corpus.jsonl
```

## Limpieza aplicada
- Se conservan solo los párrafos (`<p>`) del cuerpo; se descartan navegación, metadatos y pie de página.
- La letra capital viene como imagen (`<img alt="H">`): se restituye desde el atributo `alt`.
- Se separan los párrafos con línea en blanco.

## Limitaciones conocidas
- Se pierden los subtítulos y numeraciones internas (por ejemplo, "Primavera", "II") y algunas líneas de cartas dentro de los cuentos (*Una estación de amor*).
- Ortografía de época (`fué`, `dió`) sin normalizar.
- Wikisource fecha ambos volúmenes en 1918; no se verificó la fecha de primera edición.
- Cada cuento guarda el `revid` de Wikisource con el que se descargó.
