# Vectores preentrenados

Esta carpeta está **vacía a propósito**: los archivos pesan varios GB y no se incluyen
en la unidad.

| Archivo | Para qué cuaderno | Tamaño | Memoria al cargarlo | De dónde |
|---|---|---|---|---|
| `SBW-vectors-300-min5.bin.gz` | 02, 03, 04, 05 y extensiones C y D | 1,9 GB | ~2 GB | <https://cs.famaf.unc.edu.ar/~ccardellino/SBWCE/SBW-vectors-300-min5.bin.gz> (ficha: <https://crscardellino.net/SBWCE/>). Licencia CC BY-SA 4.0. |
| `wiki.es.bin` | 03 | 4,8 GB | ~7 GB | Dentro de <https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.es.zip> (ficha: <https://fasttext.cc/docs/en/pretrained-vectors.html>). Licencia CC BY-SA 3.0. |

Se descomprime el `.zip` de fastText y se deja `wiki.es.bin` en esta carpeta. El `.gz` de SBW **no se
descomprime**: gensim lo lee directamente.

## Si los archivos están en otra carpeta

No hace falta copiarlos. Se define la variable de entorno `LAB_VECTORES` con la carpeta donde están:

```
export LAB_VECTORES=/ruta/a/la/carpeta     # macOS / Linux
$env:LAB_VECTORES = "C:\ruta\a\la\carpeta"  # Windows (PowerShell)
```

Hay que definirla **antes** de abrir VS Code o Jupyter desde esa misma terminal.

## Cómo verificar que están bien

```
python -c "from utils import cargar_vectores_word2vec; v = cargar_vectores_word2vec(limite=1000); print(len(v.key_to_index), 'palabras OK')"
```

Un `FileNotFoundError` con la ruta completa indica dónde los busca el cuaderno.
