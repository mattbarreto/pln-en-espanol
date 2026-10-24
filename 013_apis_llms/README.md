# Unidad 013 — Consumo de modelos mediante APIs

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

En esta unidad el modelo deja de ser nuestro: lo llamamos desde un servidor local o desde un servicio, sin entrenarlo. La pregunta que guía el recorrido es qué podemos pedirle, cómo recibimos su respuesta en una forma que un programa pueda usar y cuándo no corresponde confiar en ella.

**Competencia.** Diseñar aplicaciones basadas en modelos externos y evaluar críticamente sus capacidades y límites.

Viene después de `012_large_language_models` (cómo un modelo predice el próximo token) y antes de RAG y agentes. Los datos son los avisos sintéticos de `010_transfer_learning`.

## Modelos y proveedores

- **Ollama con `granite4:latest`** (IBM, 3B, 2,1 GB en disco), local y sin costo. Es la ruta con la que corre toda la unidad.
- **Gemini** y **SerpAPI** están integrados en los cuadernos y ambos tienen plan gratuito. Si falta la clave, la celda lo avisa y el cuaderno sigue con Ollama. Las claves se guardan en `.env`, nunca en un cuaderno.

## Recorrido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| [`01_llamar_un_modelo`](01_llamar_un_modelo.ipynb) | ¿Qué pasa exactamente cuando le pedimos algo a un modelo, y qué parte de la respuesta podemos controlar? | La función `preguntar`, una tabla de tiempos y tokens, y una decisión entre local y remoto. |
| [`02_pedir_con_criterio`](02_pedir_con_criterio.ipynb) | ¿Cómo sabemos que un pedido mejor es mejor, y qué cosas no arregla ningún pedido? | Cuatro variantes de pedido medidas contra 18 avisos con etiqueta, y una decisión sobre cuándo interviene una persona. |
| [`03_salida_estructurada`](03_salida_estructurada.ipynb) | ¿Cómo conseguimos que la respuesta sea un dato, y cómo sabemos que además es cierto? | Un esquema Pydantic, `leer_respuesta` y una decisión por campo: automatizar, revisar o descartar. |
| [`04_conocimiento_congelado`](04_conocimiento_congelado.ipynb) | ¿Qué hacemos cuando la respuesta depende de un dato que el modelo nunca vio? | `responder_con_documento`, una medición de cuándo el documento deja de alcanzar y una elección entre cuatro estrategias. |

Cada cuaderno se presenta en clase y después se explora por cuenta propia: el código viene escrito, las notas **Para mirar** orientan la lectura y los **microlaboratorios** piden completar líneas y comprueban el resultado. El hilo conductor es que **un resultado bien formado no es un resultado verdadero**.

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_llamar_un_modelo.ipynb` a `04_conocimiento_congelado.ipynb` | Recorrido de la unidad. |
| `datos/` | Datos de la unidad. La procedencia y las condiciones de uso están en [`datos/LEEME.md`](datos/LEEME.md). |
| `utils.py` | Configuración, comprobaciones, carga de datos y las funciones completas `preguntar`, `preguntar_a_gemini` y `responder_con_documento`. |
| `utils_visualizacion.py` | Funciones que dibujan los valores calculados en los cuadernos. |
| `requirements.txt` | Dependencias de los cuatro cuadernos. |
| `ANTES_DE_LA_CLASE.md` | Modelo local y claves que hay que preparar. |
| `.env.example` | Plantilla de variables de entorno. Copiala como `.env`. |

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

Los cuadernos 01 a 04 se ejecutaron de arriba abajo desde un kernel limpio el 23 de octubre de 2026, en una Mac con chip Apple y macOS 27, con Python 3.12.13, `ollama` 0.6.3, `pydantic` 2.14.1, `jinja2` 3.1.6, `pandas` 3.1.0 y `granite4:latest`. También se probaron copias resueltas de sus microlaboratorios: todas las comprobaciones terminaron con `Correcto.`.

- **Gemini y SerpAPI no se ejecutaron.** Las celdas que los usan se escribieron y se comprobó que, sin clave, avisan y siguen; con clave nunca corrieron en esta versión. En SerpAPI, sin clave se usan cuatro resultados sintéticos de `datos/busqueda_ejemplo.json`. El nombre del modelo de Gemini es `gemini-2.5-flash` y se puede cambiar con la variable `GEMINI_MODEL`.
- Los tiempos dependen de la computadora y cambian en cada ejecución. Las notas **Para mirar** citan cifras de conteo (aciertos, tokens) y órdenes de magnitud de tiempo.
- Las respuestas de un modelo cambian con otra versión de `granite4` o de Ollama. Las notas describen lo que salió en esta ejecución; si tu salida es distinta, no es necesariamente un error.
- No se probaron Windows, Linux ni equipos sin GPU. La sección 3 del cuaderno 04 hace cuatro llamadas de decenas de segundos cada una.
- Los datos de los cuadernos son sintéticos y pequeños. Las cifras comparan pedidos entre sí; no estiman cuánto acierta un modelo con avisos reales.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).
