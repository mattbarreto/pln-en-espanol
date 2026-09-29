# Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural

**IFTS N.º 24 · Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial**  
Profesor Matías Barreto · Ciclo lectivo 2026  
Repositorio: [`pln-en-espanol`](https://github.com/mattbarreto/pln-en-espanol)

---

## Empezá acá

### 1. Cómo descargar una carpeta individual
Cada unidad es autónoma y se puede trabajar por separado. Para descargar únicamente la carpeta de la semana sin clonar todo el repositorio, podés usar cualquiera de estas dos herramientas web gratuitas (no requieren registro):

* **Opción 1 — Download Directory:**
  1. Copiá el enlace de la carpeta en GitHub (por ejemplo, `https://github.com/mattbarreto/pln-en-espanol/tree/main/003_text_mining`).
  2. Entrá en [download-directory.github.io](https://download-directory.github.io).
  3. Pegá la URL en el cuadro y presioná `Enter`. Se descargará automáticamente un archivo `.zip` con solo esa carpeta.
* **Opción 2 — DownGit:**
  1. Entrá en [downgit.github.io](https://downgit.github.io).
  2. Pegá el enlace de la carpeta en el campo *GitHub URL*.
  3. Hacé clic en **Download**.
* **Opción 3 — Git clone (para quienes ya usan Git):**
  ```bash
  git clone https://github.com/mattbarreto/pln-en-espanol.git
  ```
  Y luego `git pull` cada semana para bajar las actualizaciones.

---

### 2. Regla de oro para trabajar en los cuadernos

> **No edites los cuadernos originales.**  
> Antes de resolver las consignas, duplicá el cuaderno y agregale `_mio` al nombre (por ejemplo: `02_lema_pos_y_morfologia_mio.ipynb`) dentro de la misma carpeta.  
> El repositorio ignora automáticamente todos los archivos `*_mio.ipynb`, lo que te permite actualizar el material con `git pull` o sobreescribir la carpeta sin perder tus notas ni generar conflictos.

---

## El recorrido de la materia

La pregunta de fondo que articula todo el laboratorio:

> **¿Qué se pierde en cada paso, y qué queda justificado afirmar con lo que quedó?**

```
 ● armado      ○ en desarrollo

 TRAMO A · CORPUS Y REPRESENTACIONES EXPLÍCITAS
     ● Terminal y Python para textos ................ 001_python
     ↓
     ● Obtención de textos y scraping ............... 002_web_scraping
     ↓
     ● BoW → TF → DF → TF-IDF ....................... 003_text_mining
     ↓
     ● spaCy: lema, POS, sintaxis, entidades ........ 004_spacy

 TRAMO B · DEL AUDIO AL TEXTO
     ↓
     ● ASR: Whisper y transcripción situada ......... 005_asr_lab

 TRAMO C · INTEGRACIÓN Y SÍNTESIS
     ↓
     ● Síntesis de técnicas y clasificación ......... 006_sintesis

 TRAMO D · REPRESENTACIONES APRENDIDAS Y EMBEDDINGS
     ↓
     ○ Word2Vec → GloVe → fastText
     ↓
     ○ Sentence embeddings y búsqueda semántica

 TRAMO E · ARQUITECTURAS Y MODELOS DEL LENGUAJE
     ↓
     ○ RNN → LSTM → Transformers
     ↓
     ○ Transfer learning y modelos preentrenados

 TRAMO F · MODELOS GENERATIVOS, RAG Y AGENTIC AI
     ↓
     ○ LLMs, contexto y prompting
     ↓
     ○ RAG (Retrieval-Augmented Generation)
     ↓
     ○ Sistemas de agentes autónomos (Agentic AI)
```

---

## Las unidades armadas

| | Carpeta | Qué cubre | Entorno / Ejecución | Librerías clave |
|---|---|---|---|---|
| 1 | [`001_python/`](001_python/) | Terminal, rutas, Python para textos | Colab + terminal local | ninguna (estándar) |
| 2 | [`002_web_scraping/`](002_web_scraping/) | Obtener textos y formar un corpus | Local en VS Code | `requests`, `bs4`, `trafilatura`, `pandas` |
| 3 | [`003_text_mining/`](003_text_mining/) | De palabras a números: BoW, TF-IDF | Local en VS Code | `pandas`, `scikit-learn`, `matplotlib` |
| 4 | [`004_spacy/`](004_spacy/) | Análisis lingüístico morfosintáctico | Local en VS Code | `spacy` + modelos en español |
| 5 | [`005_asr_lab/`](005_asr_lab/) | Del audio al texto: Whisper y Gradio | Local **o** Colab con GPU | `faster-whisper`, `gradio`, `yt-dlp` |
| 6 | [`006_sintesis/`](006_sintesis/) | Integración, polaridad y clasificación | Local en VS Code | `spacy`, `scikit-learn`, `pandas` |

### Material transversal y entregas

* [`guias/`](guias/): Herramientas de soporte para la cursada (entornos virtuales con `uv`, Git y GitHub, Docker con apps de PLN, Hugging Face Spaces y n8n).
* [`trabajos/`](trabajos/): Trabajos prácticos integradores y consignas evaluativas (TPI 1: El corpus como decisión, Pair Programming con IA).

---

## Cómo se trabaja

Todas las carpetas de las unidades siguen un estándar común:

| Archivo | Para qué sirve |
|---|---|
| `README.md` | Qué se hace en la unidad, en qué orden y las ideas pedagógicas centrales. |
| `ANTES_DE_LA_CLASE.md` | Guía de instalación previa paso a paso. Se hace en casa antes del aula. |
| `requirements.txt` | Lista limpia de dependencias para recrear el entorno. |

### Cada unidad tiene su propio entorno virtual

No hay un entorno único gigante para toda la materia: cada carpeta se aísla con su propio `.venv`.

Para crearlo, parate en la terminal **dentro de la carpeta de la unidad**:

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

Luego, abrís la carpeta en **Visual Studio Code**, abrís el cuaderno y elegís el kernel correspondiente a `.venv/`.

> **La carpeta `.venv` no se sube ni se comparte.**  
> Ocupa cientos de megabytes y contiene rutas absolutas de tu máquina. Lo que se comparte es `requirements.txt`.

---

## Los corpus: procedencia y autoría

| Unidad | Corpus / Dataset | Origen y autoría |
|---|---|---|
| 1 | *La Odisea* | Dominio público (se descarga en el cuaderno 01). |
| 2 | Medios digitales | Construido por cada estudiante mediante scraping ético con `trafilatura`. |
| 3 y 4 | Blog de Hernán Casciari (2004–2015) | Entradas públicas del blog del autor ([FUENTE.md](004_spacy/datos/FUENTE.md)). |
| 4 y 6 | Cuentos latinoamericanos (`cuentos_latinoamericanos.csv`) | Compilado abierto por **Karen Palacio** ([karen-pal/borges](https://github.com/karen-pal/borges)). |
| 5 | Audios para ASR | Seleccionados por cada estudiante; los audios MP3 no se redistribuyen en el repo. |
| 6 | Prensa argentina (`ar_muestra_5k.parquet`) | Subconjunto representativo de `LeoCordoba/CC-NEWS-ES` (Common Crawl News). |
| 6 | Reseñas de polaridad (`opiniones_polaridad.csv`) | Dataset sintético balanceado generado con `Faker`. |

---

## Licencia

* **Contenidos educativos y cuadernos:** Distribuido bajo licencia [Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0)](LICENSE).
* **Código fuente y utilidades:** Distribuido bajo [Licencia MIT](LICENSE-CODIGO).
