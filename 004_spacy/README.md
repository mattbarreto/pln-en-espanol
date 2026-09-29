# spaCy: análisis lingüístico de un corpus real

Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural · Unidad 4

---

## Qué vas a hacer acá

Tomar un corpus roto, entender qué se puede y qué no se puede preguntarle,
analizarlo con spaCy, corregir lo que la herramienta hace mal, y procesarlo
entero sin esperar dos minutos cada vez.

Una sola librería: `spacy`. Toda la unidad.

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)** y dejá el entorno instalado
con los tres modelos bajados. **Son 700 MB: no se bajan en clase.**

---

## El camino

Los cuadernos se hacen **en orden**. Cada uno usa lo que dejó el anterior.

### Antes de todo

| | cuaderno | tiempo | qué |
|---|---|---|---|
| — | `EMPEZAR_ACA` | 10 min | Dónde quedó text mining, contra qué chocó y qué abre spaCy. No instala ni procesa nada |

### Primer encuentro — qué ve el modelo

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 00 | `entorno_y_corpus` | 10 min | Verificar el entorno y auditar el corpus |
| 01 | `del_texto_plano_al_anotado` | 60 min | El pipeline, `Doc`, `Token`, `Span`, oraciones, leer documentación |
| 02 | `lema_pos_y_morfologia` | 50 min | Lemas, categorías gramaticales, `morph` |
| 03 | `sintaxis_y_entidades` | 55 min | Dependencias, grupos nominales, entidades |

### Segundo encuentro — configurar y escalar

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 04 | `el_modelo_no_es_neutro` | 50 min | Comparar `sm`/`md`/`lg`, auditar el NER, medir |
| 05 | `configurar_la_herramienta` | 60 min | `Matcher`, `PhraseMatcher`, `EntityRuler`, componentes propios |
| 06 | `escala_pipe_y_docbin` | 45 min | Procesar el corpus completo y guardarlo |
| 07 | `vectores_y_cierre` | 40 min | Vectores, similitud, cierre de la unidad |

### Trabajo práctico

| | cuaderno | qué |
|---|---|---|
| 08 | `trabajo_exploratorio` | Domiciliario y obligatorio. Elegís un material y documentás el recorrido. |

Del `02` en adelante, cada cuaderno empieza con una **celda de reanudación**: si
llegás tarde o se te reinicia el kernel, corrés esa celda y seguís sin perder el
hilo.

---

## Las carpetas

```
datos/
  blog/            los archivos originales, tal como llegaron. NO SE TOCAN.
  FUENTE.md        de dónde salió el corpus y qué se perdió. LEELO PRIMERO.
  corpus.jsonl     el corpus reconstruido: un párrafo por línea
  corpus.spacy     el corpus ya procesado (lo crea el cuaderno 06)
  personajes.txt   la lista del PhraseMatcher (la editás vos, en el 05)
  cuentos_latinoamericanos.csv   otro corpus, para el trabajo práctico

pipeline_propio/   la herramienta configurada (la crea el cuaderno 05)

componentes.py     los componentes propios del pipeline

EMPEZAR_ACA.ipynb  el cuaderno de apertura: se lee antes del 00

complementarios/   material para seguir, no entra en la cursada
  ner_personajes/  el modelo entrenado (lo crea el cuaderno 90)
```

---

## Complementarios

Fuera del camino obligatorio, para quien quiera seguir:

- **`90_entrenar_ner.ipynb`** — entrenar un modelo propio, y por qué un resultado
  perfecto suele ser una mala noticia.

---

## Las tres ideas que sostienen todo

1. **Un corpus se audita antes de usarlo.** No importa quién lo armó. Qué se
   capturó, qué se perdió, qué se puede preguntar y qué no: eso va escrito antes
   del primer conteo.

2. **El modelo no es neutro.** `es_core_news_lg` se entrenó con UD Spanish AnCora
   —prensa, mayoritariamente peninsular— y con WikiNER. Tu corpus no es eso. La
   herramienta trae supuestos adentro y hay que calibrarla, no obedecerla. Y no
   solo entiende peor el voseo: también reconoce peor unos nombres que otros.

3. **Lo que elegís es tu método, no tu configuración.** Qué modelo cargás, qué
   lemas corregís, quién entra en la lista de nombres, qué componentes apagás, a
   qué nivel agregás. Todo eso cambia el resultado, todo eso va anotado, y todo
   eso lo tenés que poder defender.

---

## Una advertencia sobre los errores

En cada cuaderno de esta unidad el modelo se equivoca. `EE.UU.` pegado a la
oración siguiente, *Editorial Orsai* clasificada como lugar, `¿` como lugar
treinta y tres veces, *tenés* con lema *tenés*, *manzana* y *pera* con el mismo
vector.

**Ninguno de esos errores hace saltar una excepción.** Todos devuelven un
resultado con buena cara. La única forma de encontrarlos es mirar la salida y
compararla con lo que sabés del texto.

Esa es, en el fondo, la única cosa que hay que aprender acá.

---

## Y después

Al terminar la unidad viene el **trabajo práctico integrador**, donde el corpus no lo da
la cátedra: lo armás vos, y partís de una afirmación concreta en vez de explorar a ver
qué sale.

El `EMPEZAR_ACA` lo anuncia y el `07` cierra con cómo se formula esa afirmación. El `08`
es el ensayo individual, antes de hacerlo en equipo.
