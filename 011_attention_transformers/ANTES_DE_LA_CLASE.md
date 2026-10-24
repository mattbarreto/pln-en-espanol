# Antes de la clase

**Tiempo estimado: 10 a 30 minutos, según tu conexión.** Hacelo antes de llegar al aula: PyTorch y los dos modelos pesan más de 1 GB y bajarlos en clase, con veinte personas en la misma red, no funciona.

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
| `DeepESP/gpt2-spanish` | 01, 02 y 03 | 250 MB |
| `dccuchile/bert-base-spanish-wwm-uncased` | 04 | 450 MB |

Quedan en el caché de Hugging Face: si ya hiciste la unidad 010 (BETO) o la 012 (GPT-2) en esta computadora, no hace falta bajarlos de nuevo. Si no, con el entorno activo:

```
python -c "from transformers import AutoTokenizer, GPT2LMHeadModel; M = 'DeepESP/gpt2-spanish'; AutoTokenizer.from_pretrained(M); GPT2LMHeadModel.from_pretrained(M); print('GPT-2 listo')"
python -c "from transformers import AutoModel, AutoTokenizer; M = 'dccuchile/bert-base-spanish-wwm-uncased'; AutoTokenizer.from_pretrained(M); AutoModel.from_pretrained(M); print('BETO listo')"
```

---

## 3. Verificar

Abrí `01_pesos_y_secuencias.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda: si imprime la versión de `numpy` sin error, el entorno está bien. Para comprobar los modelos, ejecutá el cuaderno 01 hasta la celda que carga GPT-2, y el 04 hasta la que carga BETO: si tardan unos segundos y no descargan nada, ya estaban en el caché.

---

## 4. Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError` | No estás usando el intérprete del entorno virtual: elegí el kernel `.venv` |
| La descarga se interrumpió | Volvé a correr el comando del paso 2: retoma desde donde quedó |
| Falta de memoria (`out of memory`) | Cerrá otras aplicaciones y reiniciá el kernel; cada cuaderno carga su modelo una sola vez |
| Error de atención en Mac con chip Apple | Ya está resuelto en 04 con `attn_implementation="eager"` |
| En Windows, PowerShell no deja activar el entorno | Corré `Set-ExecutionPolicy -Scope Process Bypass` en esa ventana y activá de nuevo |
| En Windows, aviso de Hugging Face sobre «symlinks» | Es inofensivo: el modelo funciona igual, solo ocupa algo más de disco |
| `python` no se reconoce en Windows | Con el entorno activado debería andar; si no, probá `py` en lugar de `python` |
| Los controles de 02 no aparecen | Es normal fuera de Jupyter: cada escena se dibuja primero como salida estática |

Si algo no anda, escribime antes de la clase, no el mismo día.
