# Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural

**IFTS N.º 24 · Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial**  
Profesor Matías Barreto · Ciclo lectivo 2026  
Repositorio: [`pln-en-espanol`](https://github.com/mattbarreto/pln-en-espanol)

---

## Empezá acá

### 1. Cómo descargar una carpeta individual
Cada unidad es autónoma y se puede trabajar por separado. Para descargar únicamente la carpeta de la semana sin clonar todo el repositorio, podés usar cualquiera de estas opciones (las dos primeras son herramientas web gratuitas y no requieren registro):

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
     ↓
     ● Auditar una medición antes de creerle ........ 007_clinica_de_errores
     ↓
     ● Sentimiento: reglas, aprendizaje, preentrenado 008_sentimiento

 TRAMO D · REPRESENTACIONES APRENDIDAS Y EMBEDDINGS
     ↓
     ● Word2Vec → fastText → embeddings de oración
       y búsqueda semántica ......................... 009_representaciones_semanticas

 TRAMO E · MODELOS PREENTRENADOS Y ARQUITECTURAS
     ↓
     ● Transfer learning: usar, ajustar y adaptar ... 010_transfer_learning
     ↓
     ● Atención y Transformers por dentro .......... 011_attention_transformers
     ↓
     ● LLMs: del texto al próximo token y GPT-2 .... 012_large_language_models

 TRAMO F · MODELOS GENERATIVOS, RAG Y AGENTES
     ↓
     ● Consumo de modelos mediante APIs ............ 013_apis_llms
     ↓
     ● RAG: responder con fuentes y evaluarlo ...... 014_rag
     ↓
     ● Agentes: herramientas, ciclo y controles .... 015_agentes
```

---

## Las unidades

| | Carpeta | Qué cubre | Entorno / Ejecución | Librerías clave |
|---|---|---|---|---|
| 1 | [`001_python/`](001_python/) | Terminal, rutas, Python para textos | Colab + terminal local | ninguna (estándar) |
| 2 | [`002_web_scraping/`](002_web_scraping/) | Obtener textos y formar un corpus | Local en VS Code | `requests`, `bs4`, `trafilatura`, `pandas` |
| 3 | [`003_text_mining/`](003_text_mining/) | De palabras a números: BoW, TF-IDF | Local en VS Code | `pandas`, `scikit-learn`, `matplotlib` |
| 4 | [`004_spacy/`](004_spacy/) | Análisis lingüístico morfosintáctico | Local en VS Code | `spacy` + modelos en español |
| 5 | [`005_asr_lab/`](005_asr_lab/) | Del audio al texto: Whisper y Gradio | Local **o** Colab con GPU | `faster-whisper`, `gradio`, `yt-dlp` |
| 6 | [`006_sintesis/`](006_sintesis/) | Integración, polaridad y clasificación | Local en VS Code | `spacy`, `scikit-learn`, `pandas` |
| 7 | [`007_clinica_de_errores/`](007_clinica_de_errores/) | Auditar una medición antes de creerle | Local en VS Code o Colab | `pandas`, `scikit-learn`, `matplotlib` |
| 8 | [`008_sentimiento/`](008_sentimiento/) | Sentimiento: reglas, aprendizaje y modelo preentrenado | Local en VS Code | `scikit-learn`, `pysentimiento`, `pandas` |
| 9 | [`009_representaciones_semanticas/`](009_representaciones_semanticas/) | De contar palabras a aprender del contexto: Word2Vec, fastText y embeddings de oración | Local en VS Code (vectores de varios GB) | `gensim`, `sentence-transformers`, `scikit-learn` |
| 10 | [`010_transfer_learning/`](010_transfer_learning/) | Usar modelos preentrenados, ajustar un clasificador y adaptar BETO a un dominio | Local en VS Code | `transformers`, `torch`, `datasets`, `scikit-learn` |
| 11 | [`011_attention_transformers/`](011_attention_transformers/) | Atención, máscara causal y bloque Transformer; las cabezas de BETO | Local en VS Code | `numpy`, `torch`, `transformers` |
| 12 | [`012_large_language_models/`](012_large_language_models/) | Del texto al próximo token; ajuste y evaluación de GPT-2 | Local en VS Code (el laboratorio GPT-2 tiene versión para Colab) | `transformers`, `torch` |
| 13 | [`013_apis_llms/`](013_apis_llms/) | Llamar a un modelo, pedir con criterio y obtener salida estructurada | Local con Ollama (`granite4`); Gemini y SerpAPI opcionales | `ollama`, `google-genai`, `pydantic` |
| 14 | [`014_rag/`](014_rag/) | De documentos a fragmentos, base vectorial, respuestas con fuentes y evaluación | Local con Ollama; Gemini opcional | `chromadb`, `langchain`, `sentence-transformers`, `pypdf` |
| 15 | [`015_agentes/`](015_agentes/) | Herramientas, ciclo del agente, criterios de verificación y aprobación humana | Local con Ollama; Gemini y SerpAPI opcionales | `smolagents`, `ollama`, `sentence-transformers` |

### Material transversal

* [`guias/`](guias/): Herramientas de soporte para la cursada (entornos virtuales con `uv`, Git y GitHub, Docker con apps de PLN, Hugging Face Spaces y n8n).
* [`MAPA_DE_LA_MATERIA.md`](MAPA_DE_LA_MATERIA.md): el recorrido completo, con la relación entre unidades.

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

Las unidades 013, 014 y 015 usan claves de servicios externos (opcionales). Copiá `.env.example` como `.env` dentro de la carpeta de la unidad y completá las claves ahí, nunca en un cuaderno.

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
| 6 | Reseñas de polaridad (`opiniones_polaridad.csv`) | Subconjunto balanceado de reseñas en español extraídas de repositorios abiertos de evaluación de polaridad. |
| 7 | 26 cuentos de Horacio Quiroga (volumen adulto e infantil) | Dominio público, tomados de es.wikisource.org. |
| 8 | Textos de ejemplo y titulares de 2019 | Los textos los construyó el docente; los titulares vienen de [`pysentimiento/spanish-targeted-sentiment-headlines`](https://huggingface.co/datasets/pysentimiento/spanish-targeted-sentiment-headlines). |
| 9 | Fragmentos literarios, consultas y juicios de relevancia | Ver [FUENTE.md](009_representaciones_semanticas/datos/FUENTE.md). Los vectores preentrenados (SBW, `wiki.es`) se descargan aparte y no se redistribuyen. |
| 10 y 11 | Avisos y textos sintéticos | Elaborados para la unidad, bajo CC0-1.0 ([LEEME.md](010_transfer_learning/datos/LEEME.md)). |
| 10 y 11 | *El gaucho Martín Fierro* (1872), de José Hernández | Dominio público; versión del taller «Modelos de lenguaje a tu medida» (FAMAF-UNC / Fundación Vía Libre, 2023, licencia MIT). |
| 12 | 26 cuentos de Horacio Quiroga | Dominio público ([FUENTE.md](012_large_language_models/laboratorio_gpt2/datos/quiroga/FUENTE.md)). |
| 13 | Avisos sintéticos | Los de la unidad 10 ([LEEME.md](013_apis_llms/datos/LEEME.md)). |
| 14 | Políticas de «Tintas Acme», artículo de *RIA* (INTA) y fragmentos de cuentos | Empresa ficticia creada para el curso; artículo de Laura Pérez Casar (2016); cuentos de la unidad 9 ([LEEME.md](014_rag/datos/LEEME.md)). |
| 15 | Parcelas agrícolas y políticas de «Tintas Acme» | Datos sintéticos y documentos ficticios creados para el curso ([LEEME.md](015_agentes/datos/LEEME.md)). |

---

## Licencia

* **Contenidos educativos y cuadernos:** Distribuido bajo licencia [Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0)](LICENSE).
* **Código fuente y utilidades:** Distribuido bajo [Licencia MIT](LICENSE-CODIGO).
