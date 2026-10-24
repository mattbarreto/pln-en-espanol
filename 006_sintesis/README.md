# Encuentro 6 — Síntesis e Integración de Técnicas de PLN

**Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural**  
Tecnicatura Superior en Ciencias de Datos e IA — IFTS N.º 24  
Matías Barreto, 2026  

Este encuentro funciona como un laboratorio de integración y cierre de la primera mitad de la materia. Conectamos los métodos de extracción y normalización de textos, las representaciones matriciales explícitas (Bolsa de Palabras y TF-IDF), el análisis lingüístico guiado por modelos morfosintácticos (spaCy) y la clasificación supervisada de documentos de extremo a extremo.

---

## Contenido

| Cuaderno | Tema |
|---|---|
| `001_sintesis.ipynb` | Recorrido integrador: desde el texto crudo y la normalización hasta la clasificación supervisada, inspección de dependencias y análisis de probabilidades. |

---

## Datasets del encuentro: Procedencia, descarga y uso

Para garantizar que los ejercicios trabajen con lenguaje natural auténtico, regional y con ruido real de redacción, utilizamos dos corpus complementarios:

### 1. Corpus de Prensa en Español (`CC-NEWS-ES`)

* **Origen y autoría:** Repositorio abierto de Hugging Face [`LeoCordoba/CC-NEWS-ES`](https://huggingface.co/datasets/LeoCordoba/CC-NEWS-ES), curado por Leo Córdoba sobre el archivo global de Common Crawl News (noticias periodísticas publicadas entre 2019 y 2020 en dominios de países hispanohablantes).
* **Alcance regional:** El corpus original está dividido por dominios de nivel superior (TLD). Para nuestro laboratorio utilizamos el subconjunto de Argentina (`ar.zip`), que en bruto contiene **532.703 artículos** de medios digitales argentinos.
* **Muestra distribuida en el repositorio:** Para que el repositorio sea liviano y no requiera clonar cientos de megabytes, se incluye directamente una muestra representativa de 5.000 artículos en formato Parquet:  
  `datos/cc-news-es/ar_muestra_5k.parquet` (**6,0 MB**, carga en memoria en 0,05 segundos).
* **Estructura de columnas:**
  * `country`: código de dominio regional (`ar`).
  * `id`: identificador numérico único del documento.
  * `text`: cuerpo completo del artículo periodístico.

#### ¿Cómo se descarga y procesa el corpus original desde cero?
Si querés reproducir la descarga y extracción directa desde Hugging Face en tu máquina sin recurrir a scripts antiguos ni descargar todo el repositorio:

```python
from huggingface_hub import hf_hub_download
from pathlib import Path
from zipfile import ZipFile
import json
import pandas as pd

# 1. Descargamos exclusivamente el archivo comprimido de Argentina (ar.zip, ~330 MB)
archivo_zip = hf_hub_download(
    repo_id="LeoCordoba/CC-NEWS-ES",
    repo_type="dataset",
    filename="ar.zip",
    local_dir="datos/cc-news-es"
)

# 2. Leemos el archivo JSON interno sin descomprimir en disco
with ZipFile(archivo_zip) as z:
    with z.open("ar.json") as f:
        datos = json.load(f)

# 3. Convertimos a tabla y filtramos textos sustantivos (>= 500 caracteres)
df_noticias = pd.DataFrame(datos)
df_filtrado = df_noticias[df_noticias["text"].str.len() >= 500]

# 4. Extraemos una muestra estratificada y reproducible de 5.000 artículos
muestra_5k = df_filtrado.sample(n=5000, random_state=42)

# 5. Guardamos en formato columnar Parquet (óptimo para Pandas)
muestra_5k.to_parquet("datos/cc-news-es/ar_muestra_5k.parquet", index=False)
```

#### ¿Cómo se utiliza en el cuaderno?
```python
import pandas as pd

corpus_noticias = pd.read_parquet("datos/cc-news-es/ar_muestra_5k.parquet")
print(f"Artículos cargados: {len(corpus_noticias):,}")
```

---

### 2. Corpus de Reseñas para Clasificación Supervisada (`opiniones_polaridad.csv`)

* **Origen:** Subconjunto balanceado de reseñas de servicios y experiencias en idioma español extraídas de repositorios abiertos de evaluación de polaridad (*Sentiment Analysis*).
* **Volumen:** **1.600 textos** distribuidos de forma simétrica:
  * 800 opiniones con valoración **Positiva**.
  * 800 opiniones con valoración **Negativa**.
* **Ubicación:** `datos/opiniones_polaridad.csv` (800 KB).
* **Estructura de columnas:**
  * `texto`: cuerpo de la reseña redactada por el usuario.
  * `sentimiento`: etiqueta categórica objetivo (`Positivo` o `Negativo`).

#### ¿Cómo se utiliza en el cuaderno?
```python
import pandas as pd

df_polaridad = pd.read_csv("datos/opiniones_polaridad.csv")
print(df_polaridad["sentimiento"].value_counts())
```

---

## Política de aislamiento del entorno (NLTK y spaCy)

Para evitar que la ejecución de los cuadernos contamine el directorio personal del usuario (`~/nltk_data` o `~/.cache`), el cuaderno sigue una política estricta de aislamiento dentro del entorno virtual:

1. **Datos de NLTK en el entorno virtual:**  
   Los paquetes de tokenización (`punkt`, `punkt_tab`) y palabras vacías (`stopwords`) se descargan automáticamente dentro de la carpeta del propio entorno virtual:  
   `Path(sys.prefix) / "nltk_data"`  
   NLTK reconoce esta ruta de manera nativa sin necesidad de configuraciones globales en el sistema operativo.

2. **Modelo de lenguaje de spaCy:**  
   El modelo `es_core_news_lg` se instala como un paquete Python dentro de `.venv/`. En máquinas con recursos de memoria reducidos (< 8 GB RAM), se puede sustituir en la celda de configuración por `es_core_news_md`.

---

## Configuración del entorno local

Para trabajar con este material de forma autónoma:

1. **Crear y activar el entorno virtual con `uv`:**
   ```bash
   uv venv
   source .venv/bin/activate        # En Linux/macOS
   # .venv\Scripts\activate         # En Windows
   ```

2. **Instalar las dependencias:**
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Descargar el modelo avanzado en español de spaCy:**
   ```bash
   python -m spacy download es_core_news_lg
   ```

4. **Iniciar JupyterLab o abrir en VS Code:**
   ```bash
   jupyter lab
   ```

---

## Estructura de la carpeta

```
006_sintesis/
├── README.md               ← este documento (documentación, origen de datos y entorno)
├── requirements.txt        ← dependencias del encuentro
├── datos/
│   ├── cc-news-es/
│   │   └── ar_muestra_5k.parquet ← muestra de prensa en español (5.000 artículos, 6 MB)
│   ├── opiniones_polaridad.csv   ← corpus balanceado de reseñas (1.600 textos, 800 KB)
│   └── cuentos_latinoamericanos.csv ← corpus literario de consulta complementaria
├── salidas/                ← gráficos y artefactos generados
└── 001_sintesis.ipynb      ← cuaderno integrador principal
```
