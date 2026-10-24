# Antes de la clase

Son unos 30 minutos de trabajo y casi todo es esperar descargas. **Hacelo en tu casa**: los archivos
pesan varios GB y bajarlos en el aula, con veinte personas en la misma red, no funciona.

---

## 1. Entorno

En la carpeta de la unidad:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

En macOS o Linux, si no tenés `uv`:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows, PowerShell:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después, en VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → elegí `.venv`.

Usá Python 3.12. `sentence-transformers` trae `torch`, que es grande (más de 1 GB): la instalación puede tardar.

---

## 2. Los vectores preentrenados

Hay dos archivos y no hace falta tener los dos para todos los cuadernos.

| Archivo | Lo necesitan | Tamaño | Memoria |
|---|---|---|---|
| `SBW-vectors-300-min5.bin.gz` | cuadernos 02, 04, 05 (y parte del 03) | 1,9 GB | ~2 GB |
| `wiki.es.bin` | cuaderno 03 (sección 5 en adelante) | 4,8 GB | ~7 GB |

Descargalos desde las direcciones de [`datos/vectors/README.md`](datos/vectors/README.md) y dejalos en
`datos/vectors/`. **No descomprimas el `.gz`.** El `wiki.es.bin` está dentro de un `.zip`: descomprimí
el zip y quedate con ese archivo.

Si tu compu tiene **menos de 8 GB libres**, salteá `wiki.es.bin`: el cuaderno 03 se puede hacer hasta la
sección 4 sin él, y el resto de la unidad no lo necesita.

---

## 3. El modelo de oraciones

Los cuadernos 04 y 05 usan un modelo que se descarga de Internet la primera vez (~470 MB). Bajalo ahora,
con el entorno activo:

```
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); print('modelo OK')"
```

Es normal que aparezcan barras de progreso y avisos. Queda guardado en `~/.cache/huggingface`, fuera del
proyecto, y no se vuelve a bajar.

---

## 4. Verificar

Con el entorno activo, parado en la carpeta de la unidad:

```
python -c "import numpy, pandas, sklearn, matplotlib, gensim, sentence_transformers; print('librerías OK')"
python -c "from utils import cargar_vectores_word2vec; v = cargar_vectores_word2vec(limite=1000); print(len(v.key_to_index), 'palabras OK')"
python -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); print('modelo OK, dimensiones:', len(m.encode(['hola'])[0]))"
```

Si las tres imprimen `OK` sin error, estás listo. Si el segundo falla con `FileNotFoundError`, el mensaje
dice en qué carpeta busca los vectores: movelos ahí o definí `LAB_VECTORES`
(ver [`datos/vectors/README.md`](datos/vectors/README.md)).

---

## 5. Espacio y avisos

* Necesitás unos **7 GB libres** en disco para los vectores y **1 GB** para el modelo y `torch`.
* Los cuadernos muestran avisos de la librería (por ejemplo, el de longitud máxima en el cuaderno 04):
  forman parte de lo que se analiza y no indican un error.

Si algo no anda, escribime antes de la clase.
