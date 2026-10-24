# Antes de la clase

**Tiempo estimado: 10 a 30 minutos, según tu conexión.** Hacelo antes de llegar al aula: PyTorch y el modelo pesan más de 1 GB y bajarlos en clase, con veinte personas en la misma red, no funciona.

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

## 2. El modelo

Solo el cuaderno 04 usa un modelo: BETO, el mismo de la unidad 010.

| Modelo | Uso | Descarga aproximada |
|---|---|---|
| `dccuchile/bert-base-spanish-wwm-uncased` | 04 | 450 MB |

Si ya hiciste la unidad 010 en esta computadora, ya lo tenés: queda en el caché de Hugging Face y no hace falta bajarlo de nuevo. Si no, con el entorno activo:

```
python -c "from transformers import AutoModel, AutoTokenizer; M = 'dccuchile/bert-base-spanish-wwm-uncased'; AutoTokenizer.from_pretrained(M); AutoModel.from_pretrained(M); print('Modelo listo')"
```

Los cuadernos 01, 02 y 03 no descargan nada.

---

## 3. Verificar

Abrí `01_pesos_y_secuencias.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda: si imprime la versión de `numpy` sin error, el entorno está bien. Para comprobar BETO, ejecutá el cuaderno 04 hasta la celda que lo carga: si tarda unos segundos y no descarga nada, ya estaba en el caché.

---

## 4. Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError` | No estás usando el intérprete del entorno virtual: elegí el kernel `.venv` |
| La descarga se interrumpió | Volvé a correr el comando del paso 2: retoma desde donde quedó |
| Falta de memoria (`out of memory`) | Cerrá otras aplicaciones y reiniciá el kernel; el cuaderno 04 carga BETO una sola vez |
| Error de atención en Mac con chip Apple | Ya está resuelto en 04 con `attn_implementation="eager"` |
| En Windows, PowerShell no deja activar el entorno | Corré `Set-ExecutionPolicy -Scope Process Bypass` en esa ventana y activá de nuevo |
| En Windows, aviso de Hugging Face sobre «symlinks» | Es inofensivo: el modelo funciona igual, solo ocupa algo más de disco |
| `python` no se reconoce en Windows | Con el entorno activado debería andar; si no, probá `py` en lugar de `python` |
| El selector de 02 no aparece | Es normal fuera de Jupyter: el cuaderno incluye la versión estática debajo |

Si algo no anda, escribime antes de la clase, no el mismo día.
