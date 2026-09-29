# Antes de la clase

Son 20 minutos, y **hay que hacerlos antes de llegar al aula**. Uno de los
modelos pesa 631 MB: bajarlo en clase, con veinte personas en la misma red,
no funciona.

---

## 1. Entorno

Igual que en las unidades anteriores. Parate dentro de la carpeta de la unidad (`004_spacy/`):

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

---

## 2. Los modelos

spaCy no sabe español por sí solo: hace falta un modelo entrenado. Vamos a usar
**los tres**, porque compararlos es parte del contenido.

```
python -m spacy download es_core_news_sm
python -m spacy download es_core_news_md
python -m spacy download es_core_news_lg
```

| modelo | tamaño | para qué lo usamos |
|---|---|---|
| `es_core_news_sm` | 16 MB | Para comparar. Es el que peor anda. |
| `es_core_news_md` | 54 MB | Para comparar. |
| `es_core_news_lg` | **631 MB** | El que usamos todo el tiempo. |

Sí, son 700 MB. Bajalos en tu casa.

---

## 3. Verificar

Corré esto en una terminal con el entorno activo. Si imprime las tres líneas sin
error, estás listo.

```
python -c "import spacy; nlp = spacy.load('es_core_news_lg'); print('lg OK', nlp.pipe_names)"
python -c "import spacy; spacy.load('es_core_news_md'); print('md OK')"
python -c "import spacy; spacy.load('es_core_news_sm'); print('sm OK')"
```

Si alguno falla con `OSError: Can't find model`, volvé al paso 2. Si falla con
`ModuleNotFoundError: No module named 'spacy'`, no estás usando el intérprete
del entorno virtual.

---

## 4. Espacio en disco

Contando los tres modelos, las librerías y los archivos que vamos a generar
durante la clase, calculá **1,5 GB libres**.

---

## Si algo no anda

Escribime antes de la clase, no el mismo día. Con veinte personas resolviendo
instalaciones no se puede dar clase.
