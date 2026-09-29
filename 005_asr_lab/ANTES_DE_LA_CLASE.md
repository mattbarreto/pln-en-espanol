# Antes de la clase

Esta unidad se puede hacer de dos maneras, y **conviene que elijas antes de llegar**.

| | Dónde | Cuándo te conviene |
|---|---|---|
| **Local** | Tu máquina, VS Code | El camino de la materia. Igual que las unidades 2, 3 y 4 |
| **Colab** | Navegador | Si tu máquina no da, o si querés GPU y no tenés |

Los cuadernos son los mismos en las dos carpetas, `local/` y `colab/`. Cambian cinco
celdas: cómo se instala, de dónde sale el audio, dónde quedan las salidas, si hay GPU y
cómo se lanza la interfaz. Está escrito en cada cuaderno dónde cambia y por qué.

**Si vas por Colab, saltá al punto 4.**

---

## 1. Entorno

Igual que en las unidades anteriores. Parado **dentro** de `005_asr_lab/`:

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

---

## 2. FFmpeg

**Esto es lo único nuevo de la unidad, y es lo que más se rompe.**

FFmpeg no se instala con `pip`: es un programa del sistema operativo, aparte de Python.
Lo necesita `yt-dlp` para convertir a MP3 el audio que baja.

| Sistema | Comando |
|---|---|
| **Windows** | `winget install Gyan.FFmpeg` |
| **macOS** | `brew install ffmpeg` |
| **Linux** (Debian/Ubuntu) | `sudo apt install ffmpeg` |

Después de instalarlo, **cerrá y volvé a abrir la terminal**. Si no, el sistema sigue sin
encontrarlo.

> **Solo hace falta para el cuaderno 00.** Transcribir no lo usa: `faster-whisper`
> decodifica el audio por su cuenta. Si FFmpeg se te resiste, podés hacer los cuadernos 01
> y 02 igual, con un audio que ya tengas.

---

## 3. Verificar

Con el entorno activo, en una terminal. Si las tres líneas imprimen sin error, estás listo.

```
ffmpeg -version
uv run python -c "import faster_whisper; print('faster-whisper OK')"
uv run python -c "import gradio; print('gradio OK')"
```

Si `ffmpeg -version` dice que no se encuentra el comando, volvé al punto 2 y fijate que
hayas reabierto la terminal.

---

## 4. Si vas por Colab

No hay nada que instalar antes. Solo dos cosas:

1. Una cuenta de Google.
2. Activar la GPU al abrir cada cuaderno: **Entorno de ejecución → Cambiar tipo de entorno
   de ejecución → T4 GPU**. Sin GPU funciona igual, con un modelo más chico y más lento.

Colab ya trae FFmpeg instalado, así que el punto 2 no te corresponde.

> **Lo que bajes en Colab se borra.** El disco de la sesión es prestado: cuando se cierra,
> se pierde el corpus de audio. Para conservar algo, descargalo o trabajá en local.

---

## 5. Espacio y paciencia

El modelo **no viene con la instalación**: se baja solo, la primera vez que lo cargás, y
queda en caché para las veces siguientes.

| Modelo | Cuándo se usa | Pesa |
|---|---|---|
| `small` | por defecto sin GPU | ~0,5 GB |
| `large-v3-turbo` | por defecto con GPU | ~1,6 GB |

Calculá **3 GB libres** contando el entorno, el modelo y los audios que bajes.

Esa primera descarga tarda. Si podés, abrí el cuaderno 01 una vez en tu casa y dejá que
baje el modelo: en clase, con veinte personas en la misma red, no funciona.

---

## Si algo no anda

Escribime **antes** de la clase, no el mismo día. Con veinte personas resolviendo
instalaciones no se puede dar clase.
