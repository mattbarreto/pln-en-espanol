# Antes de la clase — 15 minutos

> Hacé esto **antes** de conectarte al Meet. Si algo no sale, avisá por el canal de
> la materia y lo resolvemos antes, no durante.

---

## 1. Visual Studio Code

Descargalo de <https://code.visualstudio.com> e instalalo.

Abrilo y andá a Extensiones (`Ctrl+Shift+X`). Instalá **solo estas dos**:

- **Python** (de Microsoft)
- **Jupyter** (de Microsoft)

No hace falta ninguna más. En serio.

---

## 2. uv y el entorno

`uv` maneja Python y las librerías por vos. **No hace falta instalar Python
aparte**: uv lo baja solo.

Estos son los tres pasos completos:

```powershell
# 1) Instalar uv (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2) En la carpeta de la unidad (002_web_scraping)
uv venv --python 3.12
uv pip install -r requirements.txt

# 3) En VS Code: Ctrl+Shift+P → "Python: Select Interpreter" → elegir .venv
```

Ahora, con más detalle:

### 2.1 Instalar uv

**Windows** — abrí PowerShell y pegá la línea del paso 1.

**macOS o Linux** — abrí la terminal y pegá:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Cerrá la terminal y abrí una nueva.** Después comprobá:

```
uv --version
```

Si responde con un número de versión, listo.

### 2.2 La carpeta de la unidad

Descargá la carpeta `002_web_scraping` y ponela en un lugar **sin espacios ni acentos
en la ruta**. Por ejemplo `C:\lab-pln\002_web_scraping`. Rutas como
`C:\Users\Ana\Mi Documentación\...` traen problemas.

Abrí una terminal **dentro de esa carpeta**.

### 2.3 Crear el entorno e instalar las librerías

```
uv venv --python 3.12
```

Eso baja Python 3.12 y crea una carpeta `.venv`: un Python propio de este
proyecto, separado del resto de la máquina. Tarda unos minutos la primera vez.

```
uv pip install -r requirements.txt
```

Eso instala, adentro de ese entorno, las librerías que están listadas en
**`requirements.txt`**.

> **Abrí `requirements.txt` antes de correr el comando.** Son seis líneas: una por
> librería, con la versión mínima y para qué sirve. No hay nada mágico en instalar
> dependencias — es una lista de nombres en un archivo de texto.

### 2.4 Activar el entorno

Crear el entorno no es lo mismo que estar adentro. Para que la terminal use el
Python del proyecto en vez del de la máquina, hay que **activarlo**.

> **Primero tiene que existir.** Activar no crea nada: entra a algo que ya está.
> Si todavía no corriste `uv venv` (paso 2.3), vas a ver esto:
>
> ```
> source: no such file or directory: .venv/bin/activate
> ```
>
> No es un error tuyo: es que la carpeta `.venv` todavía no existe. Volvé al 2.3.

El comando cambia según el sistema:

| Sistema | Terminal | Comando |
|---|---|---|
| **Windows** | PowerShell | `.venv\Scripts\Activate.ps1` |
| **Windows** | CMD (símbolo del sistema) | `.venv\Scripts\activate.bat` |
| **macOS / Linux** | bash o zsh | `source .venv/bin/activate` |

Sabés que funcionó porque el prompt de la terminal pasa a empezar con `(.venv)`:

```
(.venv) PS C:\lab-pln\web-scrapping>
```

Para salir, en cualquier sistema:

```
deactivate
```

> **Si PowerShell no te deja** y dice algo sobre *execution policies*, corré esto
> una sola vez y volvé a intentar:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**¿Hace falta activarlo para la clase de hoy?** Para correr las notebooks dentro de
VS Code, no: alcanza con elegir el kernel `.venv` (paso 3). Activar el entorno sirve
cuando trabajás **desde la terminal** — por ejemplo para instalar una librería nueva
o correr un script suelto. Conviene saber hacerlo igual: es la diferencia entre
instalar algo en tu proyecto o instalarlo suelto en la máquina.

---

## 3. Comprobación final

1. En VS Code: `Archivo → Abrir carpeta` y elegí la carpeta de la unidad (`002_web_scraping`).
   **Abrí la carpeta, no un archivo suelto.**
2. Abrí `00_entorno.ipynb`.
3. Arriba a la derecha, donde dice *Select Kernel*, elegí el que dice **`.venv`**.
4. Corré todas las celdas (`Ctrl+Alt+Enter` o el botón ▶▶).

**Si las cinco celdas dan verde, estás listo.**

---

## Si algo falla

| Lo que ves | Qué hacer |
|---|---|
| `uv: command not found` | Cerrá y volvé a abrir la terminal |
| `no such file or directory: .venv/bin/activate` | El entorno todavía no existe: corré `uv venv --python 3.12` primero |
| `Project is already initialized` | Estás corriendo `uv init`, que acá no hace falta. Usá `uv venv` + `uv pip install -r requirements.txt` |
| `ModuleNotFoundError` | Volvé a correr `uv pip install -r requirements.txt` y reelegí el kernel `.venv` |
| No aparece `.venv` en la lista de kernels | `Ctrl+Shift+P` → `Python: Select Interpreter` → `Enter interpreter path` → buscá `.venv` |
| La versión de Python no es 3.12 | Estás en el kernel equivocado, elegí el `.venv` |

Si el entorno quedó hecho un desastre, en el README está el procedimiento para
borrarlo y rearmarlo desde cero. No es grave: se rehace en dos comandos.

Escribí en el canal de la materia con **una captura de pantalla del error
completo**. Con "no me anda" no se puede ayudar.
