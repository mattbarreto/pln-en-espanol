# datos

Acá sale todo lo que produzca el cuaderno `00`.

```
audios/                    los MP3 que bajes
corpus_audio.jsonl         el corpus: un registro por línea
corpus_audio_indice.csv    lo mismo, para abrir en una planilla
```

La carpeta llega vacía a propósito: **el material lo elegís vos**. No hay un corpus
de cátedra para esta unidad, y esa es parte de la consigna.

---

## Qué guarda cada registro

Los mismos seis campos que usaste en la unidad 2, más tres que solo tienen sentido
para audio.

| campo | qué es |
|---|---|
| `url` | De dónde salió |
| `medio` | El canal o programa |
| `titulo` | Tal como figura en la fuente |
| `autoria` | Quién lo publicó |
| `fecha_publicacion` | Cuándo se publicó |
| `fecha_captura` | Cuándo lo bajaste vos |
| `duracion_segundos` | Cuánto dura |
| `licencia` | **Lo completás a mano.** `yt-dlp` no lo sabe |
| `archivo` | El MP3 correspondiente |

La columna `licencia` llega diciendo *"revisar en la fuente"*. Completarla es
trabajo tuyo, audio por audio. Si no podés determinarla para alguno, sacalo del
corpus y anotá por qué.

---

## Los audios no se comparten

Un MP3 bajado de una plataforma **no es tuyo para redistribuir**, aunque lo hayas
usado para un trabajo. Lo que se comparte es el `corpus_audio_indice.csv`: con las
URLs y las fechas, cualquiera puede rehacer la descarga.

Por eso `audios/` conviene que quede fuera del repositorio.
