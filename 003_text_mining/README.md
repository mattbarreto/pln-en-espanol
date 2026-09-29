# Text mining: de contar palabras a analizar un corpus

Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural · Unidad 3

---

## Qué vas a hacer acá

Convertir textos en números, contar, y después desconfiar de lo que contaste.

La unidad recorre una operación completa:

> datos → pregunta → afirmación → representación → interpretación → **auditoría**

Y vuelve una y otra vez sobre la misma pregunta:

> **¿La imagen sostiene lo que estamos afirmando?**

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)** y dejá el entorno instalado.

---

## El camino

Los cuadernos se hacen **en orden**. Cada uno usa lo que dejó el anterior.

### Teórico · 95 minutos

Cuatro oraciones inventadas, chicas, que se pueden seguir a mano.

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 00 | `de_palabras_a_numeros` | 20 min | Token, vocabulario, vector. Todo a mano, sin librerías. |
| 01 | `bag_of_words` | 25 min | `CountVectorizer`, matriz documento-término, stopwords, qué se pierde. |
| 02 | `tfidf_y_ngramas` | 25 min | TF-IDF a mano y con la librería. N-gramas. |
| 03 | `lo_que_no_se_puede_contar` | 25 min | Similitud coseno. Sinonimia, polisemia y campo semántico: dónde bag of words deja de servir, con número. |

### Práctico · 140 minutos

El corpus real: doce años de textos de Hernán Casciari.

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 00 | `el_corpus` | 30 min | Qué son estos archivos. Reconstruir el corpus y escribir su procedencia. |
| 01 | `limpieza_y_frecuencias` | 35 min | Limpiar, contar, y descubrir por qué el conteo crudo miente. |
| 02 | `vectorizar_el_corpus` | 35 min | BoW y TF-IDF sobre el corpus real. Dónde deja de servir y qué se usa en su lugar. |
| 03 | `visualizacion` | 40 min | Mostrar resultados sin mentir. |

### Anexo · 90 minutos

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 00 | `el_proceso_completo` | 90 min | Todo el proceso junto, de punta a punta, en un solo cuaderno. Y las tres operaciones que faltaban: la **concordancia**, el **análisis de sentimiento** y el **modelado de tópicos**. |

Se hace **al final**, cuando ya pasaste por los cuatro cuadernos del práctico. Antes no
tiene gracia: lo que muestra es que esas cuatro partes eran una sola cosa.

Es el cuaderno que integra la unidad. Recorre el pipeline completo —corpus, limpieza,
conteo, matriz, keyness, nubes, series temporales— y después va tres pasos más allá:

- **La concordancia** (sección 10): cómo se vuelve del número al texto. Es la operación con
  la que empezaron las humanidades computacionales, en 1949.
- **El sentimiento** (sección 11): con un lexicón escrito a mano que está en `datos/` y se
  puede discutir. Se mide su cobertura real y se lo rompe a propósito.
- **Los tópicos** (sección 12): NMF sobre los párrafos, con los temas nombrados a mano.

Las tres coinciden en el mismo hallazgo por caminos distintos, y el cuaderno discute por
qué esa coincidencia no alcanza para dar nada por cierto.

---

## Las carpetas

```
teorico/           los cuatro cuadernos del teórico

anexo/
  00_el_proceso_completo.ipynb   el proceso entero, de punta a punta
  utils.py                       las trece funciones, en orden. Se lee de arriba a abajo
  datos/
    lexicon_afectivo_es.csv      polaridad de 291 palabras, escrita a mano. Abrila
  analisis_del_corpus.py         lo crea la sección 13 del cuaderno

practico/
  datos/
    blog/                los doce archivos originales. NO SE TOCAN.
    corpus.jsonl         lo crea el cuaderno 00
    corpus_limpio.jsonl  lo crea el cuaderno 01
    FUENTE.md            lo escriben ustedes en el 00
    stopwords_es.txt     lista de palabras vacías. Abrila: es un .txt
```

---

## Las tres ideas que sostienen todo

1. **Convertir texto en números destruye información.** Bag of words pierde el
   orden; la limpieza pierde la puntuación y las mayúsculas; una lista de
   stopwords pierde lo que esa lista haya decidido que sobra. Todo eso se hace a
   propósito, y hay que saber qué se perdió.

2. **Un conteo crudo compara tamaños de archivo.** Cada vez que compares grupos de
   distinto tamaño —años, autores, secciones— la pregunta es la misma: ¿estoy
   comparando la cosa o la cantidad de datos que tengo de cada una?

3. **Una imagen convence más rápido que una tabla, y por eso hay que auditarla.**
   Un gráfico puede tener todos los números correctos y afirmar algo falso.

---

## Lo que viene después

En la unidad siguiente entra spaCy, y la computadora empieza a saber que `padre`
es un sustantivo, que `escribía` viene de `escribir` y que `Mercedes` puede ser
una ciudad o una persona.

Todo lo de esta unidad se hizo sin saber nada de eso.
