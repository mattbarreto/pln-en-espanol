# Antes de la clase

**Tiempo estimado: 5 a 15 minutos, según tu conexión.** Esta unidad no descarga modelos: solo hay que crear el entorno e instalar las dependencias.

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

Después activá el entorno (`source .venv/bin/activate` en macOS o Linux; `.venv\Scripts\activate` en Windows). En VS Code, abrí la carpeta de la unidad, abrí `01_clinica.ipynb` y elegí el kernel `.venv`.

---

## 2. Los archivos

El cuaderno necesita, en la misma carpeta, `corpus.jsonl`, `utils.py` y `utils_visualizacion.py`. Ya vienen en la unidad: no hay que descargar nada más.

**En Colab:** subí esos tres archivos junto con el cuaderno, en la misma carpeta de la sesión.

---

## 3. Verificar

Abrí `01_clinica.ipynb`, elegí el kernel `.venv` y ejecutá la celda de importaciones: si termina sin error, el entorno está bien.

---

## 4. Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError` | No estás usando el intérprete del entorno virtual: elegí el kernel `.venv` |
| `No module named 'utils'` | El cuaderno no está en la misma carpeta que `utils.py`: abrí VS Code sobre la carpeta de la unidad |
| `FileNotFoundError: corpus.jsonl` | Lo mismo: `corpus.jsonl` tiene que estar junto al cuaderno |
| En Windows, PowerShell no deja activar el entorno | Corré `Set-ExecutionPolicy -Scope Process Bypass` en esa ventana y activá de nuevo |
| `python` no se reconoce en Windows | Con el entorno activado debería andar; si no, probá `py` en lugar de `python` |

Si algo no anda, escribime antes de la clase, no el mismo día.
