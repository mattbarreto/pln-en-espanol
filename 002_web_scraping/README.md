# Obtención de textos y formación de corpus

Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural · Unidad 2

---

## Qué vas a hacer acá

Construir un corpus: bajar textos de la web, extraerlos limpios, guardarlos con
sus datos de procedencia y dejarlos listos para analizar.

Tres herramientas, nada más: `requests` para pedir, `BeautifulSoup` para leer la
estructura, `trafilatura` para extraer artículos.

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)** y dejá el entorno instalado.
Son 15 minutos.

---

## Instalación

```powershell
# 1) Instalar uv (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2) En la carpeta de la unidad (002_web_scraping)
uv venv --python 3.12
uv pip install -r requirements.txt

# 3) En VS Code: Ctrl+Shift+P → "Python: Select Interpreter" → elegir .venv
```

`uv` baja Python 3.12 solo. **No hace falta instalar Python aparte.**

Los dos comandos del paso 2 hacen dos cosas distintas, y conviene tenerlas claras:

- `uv venv` crea el **entorno virtual**: una carpeta `.venv` con un Python propio
  de este proyecto. Lo que instales acá no se mezcla con el resto de la máquina.
- `uv pip install -r requirements.txt` instala adentro de ese entorno las librerías
  listadas en **`requirements.txt`**. Abrí ese archivo: son seis líneas, una por
  librería, con la versión mínima y para qué sirve cada una.

En macOS o Linux el paso 1 es:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Activar el entorno

Crear el entorno no es lo mismo que estar adentro. Para que la terminal use el
Python del proyecto y no el de la máquina, hay que activarlo.

Activar **no crea nada**: entra a algo que ya existe. Si `uv venv` no corrió todavía,
vas a ver `no such file or directory: .venv/bin/activate`.

| Sistema | Terminal | Comando |
|---|---|---|
| **Windows** | PowerShell | `.venv\Scripts\Activate.ps1` |
| **Windows** | CMD | `.venv\Scripts\activate.bat` |
| **macOS / Linux** | bash o zsh | `source .venv/bin/activate` |

El prompt pasa a empezar con `(.venv)`. Para salir: `deactivate`.

Si PowerShell lo bloquea por *execution policies*, corré una vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Para correr las notebooks en VS Code no hace falta activar nada: alcanza con elegir
el kernel `.venv`. Activar sirve para trabajar desde la terminal.

### Cuando armes un proyecto tuyo desde cero

En una carpeta vacía, `uv` puede llevar la lista de librerías por vos en lugar de
que la escribas a mano:

```powershell
uv init --python 3.12
uv add requests beautifulsoup4 trafilatura pandas matplotlib ipykernel
```

`uv add` instala y anota. Es más cómodo, pero primero conviene entender qué es lo
que se está anotando — por eso acá arrancamos con el `requirements.txt` a la vista.

Ojo con una diferencia que confunde: **`uv init` no crea el entorno**. Solo arma el
andamiaje del proyecto (`pyproject.toml`, `main.py`, `.python-version`). La carpeta
`.venv` recién aparece cuando corrés `uv venv` o el primer `uv add`.

### Empezar de cero

Si el entorno quedó roto, se rehace en tres pasos. Conviene hacerlos **en este
orden**.

**1. Ver si registraste algún kernel** *(con el entorno todavía activo)*

```
jupyter kernelspec list
```

Instalando como acá, VS Code encuentra el `.venv` solo y **no queda ningún kernel
registrado**: al borrar la carpeta desaparece todo. Pero si alguna vez corriste
`python -m ipykernel install --user --name algo`, va a aparecer en esa lista.
Sacalo por nombre:

```
jupyter kernelspec uninstall nombre-del-kernel
```

Los que dicen `python3` o vienen del sistema, dejalos donde están.

**2. Salir del entorno**

```
deactivate
```

Es el mismo comando en Windows, macOS y Linux. Vas a ver que al prompt se le cae
el `(.venv)` de adelante. Hacelo **antes** de borrar: si no, quedás parado adentro
de una carpeta que dejó de existir.

**3. Borrar la carpeta `.venv`**

| Sistema | Terminal | Comando |
|---|---|---|
| **Windows** | PowerShell | `Remove-Item -Recurse -Force .venv` |
| **Windows** | CMD | `rmdir /s /q .venv` |
| **macOS / Linux** | bash o zsh | `rm -rf .venv` |

Se borra sin miedo: adentro no hay nada tuyo. Son librerías descargadas, y
`requirements.txt` sabe exactamente cuáles volver a poner.

**Para rearmarlo**, los mismos dos comandos del principio:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

> Si borraste el `.venv` primero y ahora `jupyter` no responde, no pasa nada: un
> registro huérfano no molesta a nadie. Lo podés sacar más adelante desde cualquier
> entorno que tenga `jupyter` instalado.

---

## El camino

Las notebooks se hacen **en orden**. Cada una usa lo que dejó la anterior.

| | Notebook | Tiempo | Qué |
|---|---|---|---|
| 00 | `00_entorno.ipynb` | 5 min | Confirmar que todo funciona |
| 01 | `01_requests_http.ipynb` | 30 min | Pedir una página. Estados, cabeceras, `robots.txt`, cortesía |
| 02 | `02_beautifulsoup.ipynb` | 35 min | Leer la estructura del HTML. Etiquetas, `find`, `find_all` |
| 03 | `03_trafilatura_corpus.ipynb` | 40 min | Extraer artículos, guardarlos como corpus, primeras cuentas |

Las notebooks 02 y 03 empiezan con una **celda de reanudación**: si llegás tarde o
se te reinicia el kernel, corrés esa celda y seguís sin perder el hilo.

---

## Las carpetas

```
datos/           todo lo que produzcas sale acá
  stopwords_es.txt   lista de palabras vacías en español (abrila, es un .txt)
  odisea.html        la página guardada (la crea la notebook 01)
  corpus.jsonl       tu corpus (lo crea la notebook 03)

complementarios/ material para profundizar, no entra en la clase de hoy
```

---

## Complementarios

Fuera del camino obligatorio, para quien quiera seguir:

- **`03_proyecto_agenda_medios.ipynb`** — proyecto integrador sobre la portada de
  un diario.

Acá había dos cuadernos más, sobre Whisper y sobre Gradio. Dejaron de ser
complementarios: son la **unidad 5**, en `005_asr_lab/`. El audio como fuente de
corpus es el mismo problema de esta unidad —conseguir material y registrar su
procedencia— y por eso ahora tiene su propio recorrido, con la transcripción y la
interfaz incluidas.

No hace falta nada de esto para aprobar la parte obligatoria.

---

## Las tres ideas que sostienen todo

1. **Pedí con cortesía.** Identificate, poné `timeout`, esperá entre pedidos, leé
   el `robots.txt`. Y antes de scrapear, fijate si no hay una API, un RSS o un
   dataset que te ahorre el trabajo.

2. **Un corpus es texto más procedencia.** URL, medio, título, autoría, fecha de
   publicación y fecha de captura. Sin eso no es un corpus, es una carpeta con
   archivos de texto.

3. **Un error nunca se guarda como si fuera un dato.** Las capturas que fallan van
   a un informe de fallas, no a la columna de texto.
