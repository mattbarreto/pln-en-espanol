# Unidad 014 — Retrieval-Augmented Generation (RAG)

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

Un modelo no conoce los documentos de una organización. RAG (*Retrieval-Augmented Generation*) le acerca, para cada pregunta, los fragmentos pertinentes antes de responder. La pregunta que guía el recorrido es cómo sabemos que el sistema recuperó lo correcto y que la respuesta se apoya en eso.

**Competencia.** Construir sistemas que respondan con conocimiento externo.

**Recorrido.** Documentos → fragmentos → embeddings → base vectorial → recuperación → contexto → modelo → respuesta con fuentes → evaluación.

Viene después de `013_apis_llms`, que cierra con el problema del conocimiento congelado, y retoma de `009_representaciones_semanticas` los embeddings y la evaluación de un buscador (`05_recuperar_evaluar_visualizar`). El corpus de cuentos, las consultas y los juicios de relevancia son los de esa unidad.

## Herramientas y modelos

- **ChromaDB** (base vectorial) y **LangChain** (cargadores, cortadores, cadena): son las que se encuentran en un proyecto real. Cada cuaderno muestra primero qué entra y qué sale de cada pieza y recién después la conecta.
- **Embeddings:** `intfloat/multilingual-e5-small`, con los prefijos `query: ` y `passage: ` que exige la familia E5.
- **Generador:** Ollama con `granite4:latest` (local, sin costo). **Gemini** está integrado (plan gratuito) en el cuaderno 03; si falta la clave, esa parte avisa y el resto sigue.

## Recorrido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| [`01_documentos_a_fragmentos`](01_documentos_a_fragmentos.ipynb) | ¿Cómo convertimos un PDF, un Markdown y una tabla en la misma estructura, y cómo los partimos sin separar una regla de lo que la hace entendible? | `cargar_pdf`, `unir_palabras_cortadas`, los tres formatos como `Document` y una decisión sobre el tamaño del fragmento. |
| [`02_base_vectorial`](02_base_vectorial.ipynb) | ¿Cómo se guarda y se consulta el significado de un texto, y qué puede salir mal sin que el programa avise? | Una colección persistente de cuentos, la función `buscar` y una guarda contra la mezcla de modelos. |
| [`03_responder_con_fuentes`](03_responder_con_fuentes.ipynb) | ¿Cómo logramos que el asistente cite sus fuentes, admita lo que no sabe y no obedezca órdenes escondidas? | Un RAG con Ollama, siete casos de prueba, `formatear_contexto` y `diagnosticar`. |
| [`04_evaluar_la_recuperacion`](04_evaluar_la_recuperacion.ipynb) | ¿Cómo comparamos dos configuraciones de búsqueda con evidencia, y cuánto podemos creerle a esa comparación? | `precision_en_k`, `rango_reciproco`, tres configuraciones comparadas con un intervalo y una decisión con sus límites. |

Cada cuaderno se presenta en clase y después se explora por cuenta propia: el código viene escrito, las notas **Para mirar** orientan la lectura y los **microlaboratorios** piden completar líneas y comprueban el resultado. El hilo conductor es que **un sistema RAG puede sonar bien y estar mal**, y que se puede medir dónde falla.

## Decisiones de diseño

**Formatos: no es PDF contra JSON.** En un sistema real el formato es un detalle de ingesta; lo que no cambia es que toda fuente termina en un `Document` con texto y metadatos. El recorrido hace converger tres:

| Formato | Material | Qué enseña |
|---|---|---|
| PDF | Política de Acme (generado por computadora) y un artículo de revista del INTA (dos columnas) | La extracción pierde estructura: palabras cortadas, cabeceras y recuadros mezclados con el texto. |
| Markdown | Política de trabajo remoto | Se corta por títulos y el título pasa a ser metadato. |
| Tabla (CSV) | 137 fragmentos de cuentos de la unidad 009 | Un registro es un fragmento; los metadatos permiten filtrar y citar, y la tabla sirve para evaluar. |

**Modelo de embeddings.** Antes de escribir los cuadernos se probaron cinco modelos sobre el corpus de 009 (137 fragmentos, 10 consultas, 83 juicios). Con 10 consultas, las diferencias entre los mejores están dentro del ruido (el cuaderno 04 lo mide). Lo que sí se vio: `paraphrase-multilingual-MiniLM-L12-v2`, el modelo de 009, fue el más débil y solo lee 128 tokens; los modelos E5 pierden calidad sin sus prefijos.

| Modelo | Prefijos | Tokens máx. | P@3 (≥1) | RR (≥1) | nDCG@10 |
|---|---|---|---|---|---|
| `paraphrase-multilingual-MiniLM-L12-v2` | no | 128 | 0,43 | 0,75 | 0,46 |
| `paraphrase-multilingual-mpnet-base-v2` | no | 128 | 0,57 | 0,79 | 0,55 |
| `multilingual-e5-small` | sí | 512 | 0,57 | 0,88 | 0,56 |
| `multilingual-e5-large` | sí | 512 | 0,60 | 0,72 | 0,59 |
| `multilingual-e5-large` | no | 512 | 0,50 | 0,77 | 0,56 |

Se eligió `multilingual-e5-small` con prefijos: pesa lo mismo que el de 009, lee 512 tokens y rinde como el grande.

**Prompt.** Con una regla estricta («si falta evidencia, respondé que no»), el modelo local rechaza de más. El cuaderno 03 compara dos redacciones y separa las fallas de la búsqueda de las del modelo.

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_documentos_a_fragmentos.ipynb` a `04_evaluar_la_recuperacion.ipynb` | Recorrido de la unidad. |
| `datos/` | Documentos de Acme, artículo del INTA y cuentos de 009. La procedencia y las condiciones de uso están en [`datos/LEEME.md`](datos/LEEME.md). |
| `utils.py` | Configuración, comprobaciones, carga de datos y las versiones completas de las funciones que los cuadernos construyen paso a paso. |
| `utils_visualizacion.py` | Funciones que dibujan los valores calculados en los cuadernos. |
| `requirements.txt` | Dependencias de los cuatro cuadernos. |
| `ANTES_DE_LA_CLASE.md` | Modelos y claves que hay que preparar. |
| `.env.example` | Plantilla de variables de entorno. Copiala como `.env`. |
| `chroma_db/` | Se crea al ejecutar los cuadernos 02 y 03. Está excluida del repositorio mediante `.gitignore`. |

## Configurar el entorno local

La unidad requiere Python 3.12 y `uv`. Instalá `uv` siguiendo las instrucciones de su [documentación oficial](https://docs.astral.sh/uv/).

Desde una terminal abierta en esta carpeta:

```bash
uv venv --python 3.12
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

No instales JupyterLab ni `notebook`: en VS Code, abrí la carpeta, instalá las extensiones de Python y Jupyter si hace falta, y elegí como kernel el entorno `.venv`. Para unidades con `pyproject.toml` se usa `uv sync`; esta solo tiene `requirements.txt`.

Antes de la clase, seguí [ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md).

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).

## Validación y límites

Los cuadernos 01 a 04 se ejecutaron de arriba abajo desde un kernel limpio el 23 de octubre de 2026, en una Mac con chip Apple y macOS 27, con Python 3.12.13, `chromadb` 1.5.9, `sentence-transformers` 6.2.0, `langchain-core` 1.7.0, `langchain-ollama` 1.1.0, `pypdf` 6.21.2 y `granite4:latest`. También se probaron copias resueltas de sus microlaboratorios: todas las comprobaciones terminaron con `Correcto.`.

- **Gemini no se ejecutó.** La celda del cuaderno 03 que lo usa se escribió y se comprobó que, sin clave, avisa y sigue; con clave nunca corrió en esta versión.
- **Las respuestas del modelo local varían entre ejecuciones**, incluso con temperatura `0`. En el cuaderno 03 los casos que acertaron y fallaron coincidieron entre las ejecuciones que se hicieron, pero la redacción de las respuestas cambió. Las notas **Para mirar** citan resultados de conteo, no frases.
- **Evaluaciones chicas.** Siete casos de prueba en el cuaderno 03, diez consultas en el 04 y nueve preguntas sobre Acme: sirven para ver el mecanismo y detectar fallas, no para estimar un porcentaje de acierto.
- **Juicios de relevancia.** Los de la unidad 009 los redactó una persona, sin segunda evaluación; 39 de 83 están marcados como discutibles.
- **Licencias sin verificar:** el artículo del INTA y el compilado de cuentos. Ver `datos/LEEME.md`.
- No se probaron Windows, Linux ni equipos sin GPU. Las descargas previas rondan los 2,1 GB del modelo de Ollama y 470 MB por cada modelo de embeddings.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).
