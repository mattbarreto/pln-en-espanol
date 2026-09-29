# Antes de la clase

Diez minutos, y conviene hacerlos antes de llegar.

---

## 1. Entorno

En la carpeta de la unidad (`003_text_mining/`):

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

Activá el entorno:

```
# Windows, PowerShell
.venv\Scripts\Activate.ps1

# macOS o Linux
source .venv/bin/activate
```

Si no tenés `uv`:

```
# macOS o Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows, PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después, en VS Code: `Ctrl+Shift+P` → _Python: Select Interpreter_ → elegí `.venv`.

---

## 2. Verificar

Con el entorno activo:

```
python -c "import pandas, sklearn, matplotlib, wordcloud; print('todo OK')"
```

Si falla con `ModuleNotFoundError`, no estás usando el intérprete del entorno
virtual.

---

## 3. El corpus

Está en `practico/datos/blog/`. Son doce archivos y pesan 2,3 MB en total: ya
vienen con el material, no hay que descargar nada.

**No los abras todavía.** Lo primero que hacemos en el práctico es averiguar qué
son.

---
