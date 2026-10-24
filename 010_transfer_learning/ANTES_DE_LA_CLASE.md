# Antes de la clase

**Tiempo estimado: 20 a 40 minutos, según tu conexión.** Hacelo antes de llegar al aula: los modelos pesan unos 2,1 GB y bajarlos en clase, con veinte personas en la misma red, no funciona.

---

## 1. Entorno

En la carpeta de la unidad:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

Si no tenés `uv`, en macOS o Linux:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows, PowerShell:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después activá el entorno (`source .venv/bin/activate` en macOS o Linux; `.venv\Scripts\activate` en Windows). En VS Code, abrí un cuaderno y elegí el kernel `.venv`.

---

## 2. Los modelos

| Modelo | Uso | Descarga aproximada |
|---|---|---|
| `pysentimiento/robertuito-sentiment-analysis` | 01 | 450 MB |
| `mrm8488/bert-spanish-cased-finetuned-ner` | 01 | 450 MB |
| `mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es` | 01 | 450 MB |
| `Helsinki-NLP/opus-mt-es-en` | 01 | 300 MB |
| `dccuchile/bert-base-spanish-wwm-uncased` | 02 y 03 | 450 MB |

Total aproximado: **2,1 GB** de modelos, más PyTorch. Recomendamos **6 GB libres**.

Se bajan una sola vez, con el entorno activo, con este script:

```
python -c "
from transformers import pipeline, AutoModelForMaskedLM
pipeline('text-classification', model='pysentimiento/robertuito-sentiment-analysis')
pipeline('token-classification', model='mrm8488/bert-spanish-cased-finetuned-ner')
pipeline('question-answering', model='mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es')
pipeline('translation', model='Helsinki-NLP/opus-mt-es-en')
AutoModelForMaskedLM.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
print('Modelos listos')
"
```

Quedan en el caché de Hugging Face y los cuadernos los encuentran solos. La extensión 04 no se hace en tu computadora: corre en Google Colab con GPU y baja su propio modelo.

---

## 3. Verificar

Abrí `01_explorar_tareas.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda: si no da error, el entorno está bien. Los modelos se cargan recién cuando el cuaderno los usa; si ya están en el caché, no vuelven a descargarse.

---

## 4. Ruta remota: VS Code y Google Colab

Si tu computadora no alcanza, podés usar un entorno de Colab desde VS Code. Según las guías públicas de la extensión: instalá la extensión oficial de Google Colab (y la de Jupyter, si te la pide), abrí un cuaderno, elegí **Select Kernel > Colab** e iniciá sesión con tu cuenta de Google.

- **El kernel remoto no ve automáticamente los archivos locales.** `utils.py` y `datos/` tienen que estar en el entorno remoto: copiá o cloná la carpeta de la unidad allí, o subí un `.zip` y descomprimilo. Los cuadernos importan `utils` y leen `datos/` con rutas relativas.
- Los modelos se descargan de nuevo en cada sesión nueva.
- Mantené la sesión abierta durante la clase: si se cierra, se pierde el entorno.
- Instalá las librerías de `requirements.txt` en el entorno remoto, y `sentencepiece` si el entorno no lo trae.

Este procedimiento **no se probó** en esta versión de la unidad (ver el README).

---

## 5. Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError` | No estás usando el intérprete del entorno virtual: elegí el kernel `.venv` |
| La descarga se interrumpió | Volvé a correr el script del paso 2: retoma desde donde quedó |
| Falta de memoria (`out of memory`) | Cerrá otras aplicaciones y reiniciá el kernel; los cuadernos 02 y 03 cargan BETO una vez por corrida |
| `No module named 'utils'` o no encuentra `datos/` | El kernel remoto no tiene la carpeta: ver el paso 4 |
| Error de atención en Mac con chip Apple | Ya está resuelto en 02 y 03 con `attn_implementation="eager"`; si aparece en otro cuaderno, usá lo mismo |

Si algo no anda, escribime antes de la clase, no el mismo día.
