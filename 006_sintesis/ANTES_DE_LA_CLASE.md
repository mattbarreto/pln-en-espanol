# Antes de la clase — Encuentro 6 (Síntesis)

**Tiempo estimado:** 15 minutos.  
Conviene dejar el entorno preparado antes de comenzar la sesión de trabajo.

---

## 1. Entorno de ejecución

Desde la terminal, posicionate dentro de la carpeta `006_sintesis/`:

```bash
cd 006_sintesis
uv venv --python 3.12
```

Activá el entorno virtual:
* **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
* **macOS / Linux:** `source .venv/bin/activate`

Instalá las librerías necesarias:
```bash
uv pip install -r requirements.txt
```

---

## 2. Descargar el modelo de lenguaje

Descargá el modelo avanzado de spaCy en español (si ya lo descargaste en la unidad 4, el instalador lo reutiliza de la caché):

```bash
python -m spacy download es_core_news_lg
```

> **Nota para equipos con memoria reducida (< 8 GB RAM):** Podés optar por `es_core_news_md` para un menor consumo de memoria durante la práctica.

---

## 3. Verificar en VS Code

1. Abrí la carpeta `006_sintesis/` en **Visual Studio Code**.
2. Abrí el cuaderno `001_sintesis.ipynb`.
3. En la esquina superior derecha, hacé clic en **Select Kernel** y elegí el kernel de Python dentro de `.venv/`.
4. Ejecutá la primera celda para corroborar que las importaciones de `pandas`, `sklearn` y `spacy` funcionen correctamente.
