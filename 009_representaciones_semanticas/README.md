# Encuentro 9 — Representaciones semánticas: de contar palabras a aprender del contexto

**Laboratorio de PLN: Analítica, Textos y Cultura**
Tecnicatura Superior en Ciencias de Datos e IA — IFTS N.º 24
Matías Barreto, 2026

La pregunta que atraviesa la unidad:

> **¿Qué relaciones entre palabras y textos permite construir cada representación, qué evidencia tenemos de que son útiles y qué diferencias importantes dejan afuera?**

Venimos de contar palabras (unidad 003) y de anotarlas con spaCy (unidad 004). Acá se pone a prueba
qué significa que dos textos "se parezcan": se comparan las representaciones que ya conocés con
otras que se aprenden del contexto, y se las evalúa con consultas y juicios definidos de antemano.
La unidad no promete que las representaciones aprendidas sean mejores: mide qué ve y qué borra cada una.

---

## Contenido

| Cuaderno | Pregunta | Producto del estudiante |
|---|---|---|
| `01_representar_es_elegir.ipynb` | ¿Por qué dos fragmentos que una persona acerca pueden quedar lejos para un contador de palabras, y qué hay que cambiar? | `cercania_de_un_par`, `construir_coocurrencias` y un par propio medido con cuatro variantes |
| `02_aprender_del_contexto_word2vec.ipynb` | Cuando un modelo devuelve las palabras más cercanas a otra, ¿de qué está hecha esa cercanía y cuándo es evidencia? | `pares_centro_contexto`, `vecinos_de`, `analogia`, vecinos clasificados y una decisión de uso |
| `03_cobertura_no_es_calidad_fasttext.ipynb` | Cuando fastText fabrica un vector para una palabra que no vio, ¿cuándo es útil y cuándo solo parece una respuesta? | `n_gramas_de`, `vector_por_n_gramas`, un informe de cobertura de tres palabras y una decisión argumentada |
| `04_de_palabras_a_textos.ipynb` | ¿Qué distinciones sobreviven cuando una oración se resume en un único vector y cuáles desaparecen? | Promedio sin palabras vacías, embedding de oración, tres pares propios comparados con tres métodos y una decisión |
| `05_recuperar_evaluar_visualizar.ipynb` | ¿Cómo sabemos qué método ordena mejor los resultados de un buscador, y cuánto podemos creerle a esa respuesta? | Ranking, precisión@k y rango recíproco escritos por la persona, evaluación de una consulta propia con juicios previos y una decisión |

**Extensiones opcionales** (`extensiones/`): A) más modelos y sus protocolos; B) t-SNE y por qué un mapa no es una medida; C) WEAT: medir una asociación sin sobreinterpretarla; D) clasificar sin fuga de información.

### Cómo se trabaja cada cuaderno

1. **Explorás** un tema con el código ya escrito y las notas **Para mirar**.
2. Al final del tema, un **microlaboratorio** te dice en una tabla qué líneas completar (marcadas `COMPLETAR`) y con qué función o argumentos, con dos ayudas graduadas.
3. La celda siguiente **comprueba** y dice `Correcto.` o te da una pista. Si todavía no completaste una línea, el cuaderno igual corre de punta a punta.

El código está escrito sin tildes ni eñes (solo los textos de datos las llevan), con docstrings estilo Google, anotaciones de tipo y sin comprensiones.

### Orden y conexión

```
01 representar es elegir ──> 02 aprender del contexto ──> 03 cobertura y calidad
          │                                                         │
          └────────────────────> 04 de palabras a textos <──────────┘
                                          │
                                          v
                        05 recuperar, evaluar y visualizar (ensayo final)
```

* El 01 deja instalada la idea de **perfil de contexto**; el 02 la convierte en un método.
* El 02 y el 03 trabajan con palabras sueltas; el 04 pasa a oraciones; el 05 junta todo en una evaluación.
* Cada cuaderno es autónomo en lo técnico, pero el 03 y el 05 se apoyan en lo visto en el 02 y el 04.

### Prerrequisitos reales

Se verificaron mirando los cuadernos de las unidades anteriores, no sus README.

| Se asume | Dónde se vio |
|---|---|
| Bolsa de palabras, TF-IDF y n-gramas | 003 |
| Coseno entre vectores y por qué falla con sinonimia y polisemia | 003, cuaderno 03 ("lo que no se puede contar") |
| Vectores de spaCy y el promedio de un `Doc` | 004, cuaderno 07 |
| `Pipeline`, `train_test_split`, regresión logística | 006 |

**No se asume:** Word2Vec, gensim, PCA, sentence embeddings ni métricas de recuperación.

---

## Datos del encuentro

Detalle en [`datos/FUENTE.md`](datos/FUENTE.md). Resumen:

| Archivo | Qué es |
|---|---|
| `datos/fragmentos.csv` | 137 fragmentos de 34 textos literarios (12 autores), de `cuentos_latinoamericanos.csv` (Karen Palacio, ciudadseva.com). Selección nuestra, no al azar. |
| `datos/consultas.csv` | 10 consultas con criterio de relevancia |
| `datos/juicios_de_relevancia.csv` | 83 juicios (relevante = 2, parcial = 1). Los redactó quien armó la unidad, sin segunda evaluación. Fijados antes de calcular rankings. |
| `datos/stopwords_es.txt` | Lista de palabras vacías de 003 |

**Derechos:** los textos pertenecen a sus autores o a sus herederos; los extractos son breves y con fines didácticos.

---

## Configuración del entorno local

Cada unidad tiene su propio entorno. Parate en esta carpeta:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

| Recurso | Necesidad |
|---|---|
| Memoria | Cuaderno 01: poca (no carga modelos). Cuadernos 02, 04 y 05: ~3 GB (Word2Vec ~2 GB + modelo de oraciones). Cuaderno 03 completo: ~8 GB (el pico medido al cargar `wiki.es.bin` fue 7,2 GB); con menos, hasta la sección 4. |
| Disco | ~7 GB de vectores + ~0,5 GB del modelo de oraciones. La extensión A suma ~4,5 GB. |
| Descargas | Los vectores y el modelo se bajan **antes de la clase**: ver [`ANTES_DE_LA_CLASE.md`](ANTES_DE_LA_CLASE.md). |
| GPU | No hace falta. |
| Tiempo | En una Mac con 24 GB y vectores ya en la caché del sistema, cada cuaderno corrió de punta a punta entre 2 s (01) y alrededor de un minuto y medio (03). La primera carga de los vectores y las descargas tardan más; en otras máquinas, esperen varias veces más. |

**Entorno y Colab.** La unidad se probó en local. **No se probó en Colab**: los vectores pesan varios GB,
Drive no es una dependencia y no se certifica su funcionamiento allí. Quien quiera intentarlo tiene que
subir los vectores a la sesión y apuntar `LAB_VECTORES` a esa carpeta.

---

## Qué generan los cuadernos

Los cuadernos del estudiante guardan sus salidas (resultado de una ejecución real). No escriben archivos
en `datos/` ni en otro lugar. Los modelos descargados quedan en la memoria caché de Hugging Face
(`~/.cache/huggingface`, fuera del proyecto).

---

## Estructura de la carpeta

```
009_representaciones_semanticas/
├── README.md, ANTES_DE_LA_CLASE.md
├── requirements.txt              <- estudiantes
├── utils.py                      <- datos, coseno, ranking y métricas
├── utils_visualizacion.py        <- gráficos compartidos; recibe resultados ya calculados
├── 01_ ... 05_*.ipynb            <- recorrido del estudiante
├── datos/                        <- fragmentos, consultas, juicios, FUENTE.md, vectors/ (los vectores no se suben)
└── extensiones/                  <- A, B, C, D (opcionales)
```

**Regla de oro.** No edites los cuadernos originales: duplicá el cuaderno y agregale `_mio` al nombre.
