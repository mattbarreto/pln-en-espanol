# Del audio al texto: Whisper y una interfaz para usarlo

Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural · Unidad 5

---

## Qué vas a hacer acá

Ir a buscar audio, convertirlo en texto con un modelo neuronal que ya existe, y
después envolver todo eso en una herramienta que pueda usar alguien que no
programa.

Es la primera unidad donde el resultado no es un análisis: es **algo que
funciona**. Termina con un archivo `.py` que corre sin Jupyter.

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)**. Tiene dos caminos y hay que
elegir uno antes de llegar.

Lo único que se rompe seguido es **FFmpeg**, y solo hace falta para el cuaderno
`00`. Dejalo andando en tu casa.

---

## Local o Colab

Esta es la única unidad que viene por duplicado.

| | Para quién | Qué cambia |
|---|---|---|
| `local/` | El camino de la materia, igual que las unidades 2, 3 y 4 | Nada que instalar en cada sesión, los archivos quedan |
| `colab/` | Si tu máquina no da, o si querés GPU | El modelo anda mucho más rápido, pero al cerrar la sesión se borra todo |

**Los cuadernos son los mismos.** Cambian cinco celdas: cómo se instala, de dónde
sale el audio, dónde quedan las salidas, si hay GPU y cómo se lanza la interfaz.
En cada una está escrito qué cambia y por qué.

Que la unidad 1 fuera en Colab y esta se pueda hacer en local no es un detalle:
la materia va **hacia** trabajar en tu propia máquina, y esto es lo más cerca que
vamos a estar de un proyecto de software real.

---

## El camino

Los cuadernos se hacen **en orden**. Cada uno usa lo que dejó el anterior.

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 00 | `conseguir_audio` | 40 min | `yt-dlp`, licencias, y un corpus de audio con procedencia |
| 01 | `transcribir_una_voz` | 60 min | Whisper, segmentos con tiempos, TXT / SRT / JSON |
| 02 | `una_interfaz_para_otros` | 60 min | Gradio, decisiones de diseño, y salir del cuaderno con `app.py` |

El `02` empieza con una **celda de reanudación**: si se te reinicia el kernel o
llegás tarde, corrés esa celda y seguís.

Si FFmpeg no te anda, podés saltear el `00` y hacer el `01` y el `02` con
cualquier audio que ya tengas.

---

## Las carpetas

```
local/           los tres cuadernos, para tu máquina
colab/           los mismos tres, para Google Colab

datos/           acá van los audios que bajes
  audios/                    los MP3
  corpus_audio.jsonl         el corpus, un registro por línea
  corpus_audio_indice.csv    lo mismo, para abrir en una planilla

salidas/         las transcripciones que produzcas
complementarios/ material para seguir, no entra en la cursada
utils.py         el andamiaje de FFmpeg. No es lo que se aprende acá
app.py           lo escribe el cuaderno 02. No está hasta que lo corras
```

---

## Complementarios

Fuera del camino obligatorio, para quien quiera seguir. **No entra en la evaluación.**

- **`90_del_audio_al_analisis.ipynb`** — pasarle la transcripción a spaCy, que es lo que
  esta unidad promete al final y no hace. El NER se equivoca, y lo interesante es que el
  error no es suyo: lo hereda de la transcripción. Termina comparando tres formas de
  corregir el mismo error, en tres capas distintas, y armando una red de quién aparece con
  quién.

**Solo Colab**, y se hace después del `02`.

---

## Las tres ideas que sostienen todo

1. **Una transcripción es una hipótesis, no un registro.** El modelo devuelve lo
   más probable, no lo que se dijo. Y nunca avisa cuando se equivoca: la salida
   siempre tiene buena cara. Es exactamente el mismo problema que tenías con
   spaCy en la unidad anterior.

2. **Convertir voz en texto cambia las condiciones de circulación de lo dicho.**
   Un audio hay que escucharlo; una transcripción se busca, se copia y se cita
   fuera de contexto. Eso recae sobre personas que hablaron sin imaginar que
   las estaban transcribiendo. Por eso la parte de licencias y consentimiento del
   `00` no es un trámite.

3. **Una interfaz decide por quien la usa.** Qué se puede tocar, qué queda fijo,
   qué se informa y qué se calla. No hay forma de que una herramienta no tome
   esas decisiones: solo hay formas de tomarlas sin darse cuenta.

---

## Y después

El texto que salga de acá vuelve a ser insumo de todo lo que ya sabés hacer:
frecuencias, TF-IDF, lemas, entidades, concordancias.

Con una diferencia que vas a poder comprobar: el texto transcripto **no se parece
al escrito**. Tiene otra puntuación —la inventó el modelo—, repeticiones,
muletillas y cortes. `es_core_news_lg` se entrenó con prensa. Pasale una
transcripción y mirá qué hace.
