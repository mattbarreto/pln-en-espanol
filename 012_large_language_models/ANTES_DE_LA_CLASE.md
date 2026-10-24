# Antes de la clase

La unidad tiene dos piezas con **entornos separados**. Prepará las dos antes de llegar: las dos usan GPT-2 en español, un modelo de unos 250 MB, y bajarlo en clase, con veinte personas en la misma red, no funciona. Se descarga una sola vez y las dos piezas comparten la copia.

---

## 1. Pieza 1: del texto al próximo token

**Tiempo estimado: 10 a 20 minutos, según tu conexión.** En esta carpeta (`012_large_language_models/`):

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

Después activá el entorno (`source .venv/bin/activate` en macOS o Linux; `.venv\Scripts\activate` en Windows). En VS Code, abrí esta carpeta, abrí `01_texto_a_proximo_token.ipynb` y elegí el kernel `.venv`.

El cuaderno usa el tokenizador y la tabla de posiciones de `DeepESP/gpt2-spanish`. Si ya hiciste la unidad 011 en esta computadora, el modelo ya está en el caché de Hugging Face. Si no, con el entorno activo:

```
python -c "from transformers import AutoTokenizer, GPT2LMHeadModel; M = 'DeepESP/gpt2-spanish'; AutoTokenizer.from_pretrained(M); GPT2LMHeadModel.from_pretrained(M); print('GPT-2 listo')"
```

---

## 2. Pieza 2: laboratorio GPT-2

El laboratorio tiene su propio entorno y su propia guía: seguí [`laboratorio_gpt2/ANTES_DE_LA_CLASE.md`](laboratorio_gpt2/ANTES_DE_LA_CLASE.md). Ahí se descarga el modelo.

---

## 3. Verificar

Ejecutá la primera celda de `01_texto_a_proximo_token.ipynb`: si carga el modelo en unos segundos, sin descargar nada y sin error, la pieza 1 está lista. Para la pieza 2, la verificación está en la guía del laboratorio.

---

## 4. Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError` | No estás usando el intérprete del entorno virtual: elegí el kernel `.venv` de la pieza que estás corriendo |
| `No module named 'visualizacion_texto'` | Abrí VS Code sobre `012_large_language_models/`, no sobre el archivo suelto |
| Error de conexión al cargar el modelo | Hace falta internet la primera vez; corré el comando del paso 1 con conexión |
| En Windows, PowerShell no deja activar el entorno | Corré `Set-ExecutionPolicy -Scope Process Bypass` en esa ventana y activá de nuevo |
| `python` no se reconoce en Windows | Con el entorno activado debería andar; si no, probá `py` en lugar de `python` |

Si algo no anda, escribime antes de la clase, no el mismo día.
