# Encuentro 8 — Sentimiento en español: reglas, aprendizaje y modelos preentrenados

**Laboratorio de PLN: Analítica, Textos y Cultura**  
Tecnicatura Superior en Ciencias de Datos e IA — IFTS N.º 24  
Matías Barreto, 2026  

Este encuentro recorre tres maneras de asignar una valoración (positiva, negativa o neutra) a un texto en español: con reglas escritas a mano, con un clasificador que aprende de ejemplos y con un modelo que otros entrenaron. En los tres casos el foco no está en cuál acierta más, sino en **qué decisiones quedan a la vista, dónde falla cada uno y qué no se puede afirmar** a partir de sus resultados.

---

## Contenido

| Cuaderno | Tema |
|---|---|
| `01_lexico_y_reglas.ipynb` | Un analizador hecho a mano: léxico de palabras con valor, tokenización y una regla de negación. Se mide con una prueba fácil y se rompe con desafíos. |
| `02_aprender_de_ejemplos.ipynb` | TF-IDF y regresión logística: separar entrenamiento y prueba, leer coeficientes, probar bigramas y ver cuánta seguridad tiene el modelo. |
| `03_modelo_preentrenado.ipynb` | Inferencia con un modelo de sentimiento para español: registrar qué se usa y auditarlo con desafíos, preprocesamiento y contexto. |
| `04_comparar_y_auditar.ipynb` | Cierre de la unidad: los tres métodos aplicados a un mismo corpus **auténtico** (titulares de 2019), con anotación humana previa, evaluación sobre las mismas filas, auditoría de casos y contraste de una hipótesis. |

Los cuadernos 01 a 03 usan el mismo corpus construido y los mismos desafíos, para poder comparar los enfoques entre sí. El 04 los aplica a un corpus auténtico. Se recomienda hacerlos en orden.

---

## Datos del encuentro

* **Origen:** ejemplos construidos por el docente para esta actividad. **No son testimonios reales** ni una muestra de ningún corpus.
* **Archivos:**
  * `datos/corpus_sentimiento.csv`: 33 textos (24 de entrenamiento y 9 de prueba), repartidos en partes iguales entre `POS`, `NEG` y `NEU`.
  * `datos/desafios.csv`: 8 textos que ponen a prueba a los métodos (negación, ironía, dos objetos de valoración, voces ajenas, información desfavorable, uso coloquial, valoración mixta). No tienen etiqueta de referencia.
* **Columnas del corpus:** `id`, `partición`, `texto`, `etiqueta_referencia`.
* **Límites:** las etiquetas son propuestas docentes que requieren discusión. La prueba es deliberadamente fácil y comparte vocabulario con el entrenamiento: sirve para comparar mecanismos, no para estimar rendimiento. Los resultados no describen cómo opina ninguna población.

### Corpus auténtico del cuaderno 04

* **Archivo:** `datos/titulares_2019.csv` (48 titulares, columnas `id`, `texto`, `fuente`, `id_documento`, `objeto_valorado`).
* **Origen:** dataset [`pysentimiento/spanish-targeted-sentiment-headlines`](https://huggingface.co/datasets/pysentimiento/spanish-targeted-sentiment-headlines) (Hugging Face), descripto en [arXiv 2208.13947](https://arxiv.org/abs/2208.13947): titulares de medios argentinos sobre las elecciones presidenciales de 2019.
* **Recorte:** selección docente con semilla declarada, hecha con `datos/preparar_titulares.py`. Es una escala para leer y revisar, no una muestra representativa.
* **Unidad de análisis:** un titular y un objeto valorado (valoración dirigida). Los tres métodos clasifican el titular completo y no ven el objeto.
* **Etiqueta original:** `datos/_referencia_corpus_original.csv`. El cuaderno solo la lee en su sección 10, después de que el grupo anotó.
* **Licencia y anotación:** el repositorio de Hugging Face no tiene ficha de datos. La licencia (CC BY 4.0) figura en el artículo. Tampoco está detallado quién anotó las etiquetas originales ni con qué acuerdo.
* **Otro corpus:** `datos/plantilla_corpus.csv` tiene solo los encabezados del contrato de entrada (`id`, `texto`, `fuente`, `id_documento`; opcionales `fecha`, `contexto`, `objeto_valorado`). Si se cambia `RUTA_CORPUS` en el cuaderno 04, no hace falta tocar nada más.

**Regenerar el recorte (solo docentes, necesita Internet):**

```bash
uv run --with pyarrow --with huggingface_hub python datos/preparar_titulares.py
```

**Anotaciones del grupo:** el cuaderno 04 genera `salidas/anotaciones_plantilla.csv`. Cada pareja lo completa y guarda la versión acordada como `anotaciones/anotaciones_acordadas.csv`.

---

## Configuración del entorno local

**Hacelo antes de la clase**: ver `ANTES_DE_LA_CLASE.md`. El cuaderno 03 descarga un modelo de unos 416 MB.

1. **Crear y activar el entorno virtual con `uv`:**
   ```bash
   uv venv --python 3.12
   source .venv/bin/activate        # En Linux/macOS
   # .venv\Scripts\activate         # En Windows
   ```

2. **Instalar las dependencias:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Descargar el modelo del cuaderno 03** (una sola vez, con conexión):
   ```bash
   python -c "from pysentimiento import create_analyzer; create_analyzer(task='sentiment', lang='es')"
   ```

4. **Iniciar JupyterLab o abrir en VS Code:**
   ```bash
   jupyter lab
   ```

| Escenario | Comando |
|---|---|
| Proyecto con `pyproject.toml` | `uv sync` |
| Proyecto solo con `requirements.txt` (este caso) | `uv pip install -r requirements.txt` |

> **Si lo abrís en Colab:** subí la carpeta completa (los cuadernos,
> `utils.py`, `utils_visualizacion.py` y `datos/`) al mismo directorio, porque
> los cuadernos importan los módulos locales y leen `datos/` con rutas relativas.
> En Colab hay que instalar `pysentimiento` en una celda aparte.

---

## Qué generan los cuadernos 03 y 04

El cuaderno 03 crea la carpeta `salidas/` con dos CSV (resultados de la prueba y de los desafíos) y un JSON con las versiones y el modelo usados. El 04 guarda ahí la plantilla de anotación, la tabla de comparación y su propio registro de entorno. Los archivos del 04 incluyen los textos del corpus: no los compartas si trabajás con textos sensibles.

---

## Estructura de la carpeta

```
008_sentimiento/
├── README.md                        ← este documento
├── ANTES_DE_LA_CLASE.md             ← lo que hay que bajar e instalar antes de llegar
├── requirements.txt                 ← dependencias del encuentro
├── .python-version                  ← versión de Python (3.12)
├── utils.py                         ← lógica propia del encuentro y gráficos específicos
├── utils_visualizacion.py           ← dibujos compartidos; no calcula resultados
├── datos/
│   ├── corpus_sentimiento.csv       ← 33 textos etiquetados (entrenamiento y prueba)
│   ├── desafios.csv                 ← 8 textos para auditar los métodos
│   ├── titulares_2019.csv           ← corpus auténtico del cuaderno 04 (48 titulares, sin etiqueta)
│   ├── _referencia_corpus_original.csv ← etiqueta original, que el 04 lee al final
│   ├── plantilla_corpus.csv         ← solo encabezados, para usar otro corpus
│   └── preparar_titulares.py        ← script docente que arma el recorte (necesita Internet)
├── 01_lexico_y_reglas.ipynb
├── 02_aprender_de_ejemplos.ipynb
├── 03_modelo_preentrenado.ipynb
├── 04_comparar_y_auditar.ipynb
├── anotaciones/                     ← la crea el grupo con anotaciones_acordadas.csv
└── salidas/                         ← se crea al ejecutar los cuadernos 03 y 04
```
