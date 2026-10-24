# Antes de la clase

Son 15 minutos, y **hay que hacerlos antes de llegar al aula**. El modelo del
cuaderno 03 pesa unos 416 MB, y las librerías que lo corren, bastante más:
bajarlos en clase, con veinte personas en la misma red, no funciona.

---

## 1. Entorno

En la carpeta del encuentro:

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

Usá Python 3.12. Con versiones muy nuevas, las librerías del cuaderno 03 pueden
no tener todavía paquetes listos.

---

## 2. El modelo

El cuaderno 03 usa un modelo de sentimiento que se descarga de Internet la
primera vez. Bajalo ahora, en tu casa, con el entorno activo:

```
python -c "from pysentimiento import create_analyzer; create_analyzer(task='sentiment', lang='es'); print('modelo OK')"
```

Tarda varios minutos la primera vez. Es normal que aparezcan barras de progreso y
algunos avisos. Queda guardado en tu computadora (en la carpeta
`~/.cache/huggingface`, fuera de este proyecto), así que no se vuelve a bajar.

---

## 3. Verificar

Corré esto con el entorno activo. Si imprime las tres líneas sin error, estás
listo.

```
python -c "import pandas, sklearn, matplotlib; print('librerías OK')"
python -c "from pysentimiento import create_analyzer; a = create_analyzer(task='sentiment', lang='es'); print('modelo OK:', a.predict('Muy buena clase').output)"
```

Si falla con `ModuleNotFoundError`, no estás usando el intérprete del entorno
virtual. Si falla con un error de red, volvé al paso 2 con buena conexión.

---

## 4. Espacio en disco

Entre las librerías (alrededor de 1,2 GB) y el modelo (416 MB), calculá
**2 GB libres**.

---

## Si algo no anda

Escribime antes de la clase, no el mismo día. Con veinte personas resolviendo
instalaciones no se puede dar clase.
