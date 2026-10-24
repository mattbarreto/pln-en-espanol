# Unidad 015 — Agentes

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

Un modelo que solo responde es pasivo. Un agente decide qué herramienta usar, mira el resultado y vuelve a decidir. La pregunta que guía el recorrido es cuándo ese ciclo resuelve algo que un flujo fijo no resuelve, y qué controles hacen falta para poder confiar en lo que hace.

**Competencia.** Comprender cómo los LLM pueden coordinar herramientas para resolver tareas complejas.

Viene después de `014_rag`: la búsqueda en documentos pasa a ser una herramienta más del agente.

## Modelos y herramientas

- **Ollama con `granite4:latest`** (IBM, 3B, 2,1 GB en disco), local y sin costo. Es la ruta con la que corre toda la unidad. Se usa de dos maneras: la llamada nativa a herramientas de Ollama (cuaderno 01) y los agentes de código de `smolagents` (cuadernos 02 a 04).
- **Gemini** y **SerpAPI** están integrados en los cuadernos y ambos tienen plan gratuito. Si falta la clave, la celda lo avisa y el cuaderno sigue con Ollama. Las claves se guardan en `.env`, nunca en un cuaderno.
- **Datos:** ocho parcelas **sintéticas** (`datos/parcelas.csv`) y los documentos ficticios de Tintas Acme de la unidad 014.

## Recorrido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| [`01_herramientas`](01_herramientas.ipynb) | ¿Cómo se conecta un modelo con una función de Python, y por qué la descripción de la función importa tanto como su código? | El ciclo de una herramienta armado a mano, una medición de cómo la descripción cambia los argumentos y una descripción propia comprobada. |
| [`02_ciclo_del_agente`](02_ciclo_del_agente.ipynb) | ¿Cómo trabaja un agente por dentro, de qué depende que su ciclo funcione y cuándo conviene un flujo fijo? | La traza de un agente (`resumir_pasos`), la comparación de dos diseños de herramienta y una elección entre agente y flujo fijo. |
| [`03_agente_con_criterios`](03_agente_con_criterios.ipynb) | ¿Cómo hacemos que el trabajo de un agente se pueda verificar, y en qué punto tiene que intervenir una persona? | Una comparación entre pedido ambiguo y pedido con criterios, `comparar_con_la_regla` y una compuerta que guarda el informe solo si una persona lo aprueba. |
| [`04_practica_integradora`](04_practica_integradora.ipynb) | ¿Qué ganamos y qué perdemos al dejar que un agente elija entre herramientas, en lugar de un flujo fijo? | Dos herramientas (búsqueda y fechas), una comparación con el flujo fijo de 014 y una decisión sobre qué sistema poner a trabajar. |

Cada cuaderno se presenta en clase y después se explora por cuenta propia: el código viene escrito, las notas **Para mirar** orientan la lectura y los **microlaboratorios** piden completar líneas y comprueban el resultado. El hilo conductor es que **lo que un agente devuelve es una hipótesis**: se verifica contra una regla, se acota con un tope de pasos y, si tiene consecuencias, lo aprueba una persona.

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_herramientas.ipynb` a `04_practica_integradora.ipynb` | Recorrido de la unidad. |
| `datos/` | Parcelas sintéticas y documentos de Acme. La procedencia y las condiciones de uso están en [`datos/LEEME.md`](datos/LEEME.md). |
| `utils.py` | Configuración, comprobaciones, conexión con los modelos, una búsqueda sencilla sobre las políticas y las versiones completas de las funciones que los cuadernos construyen paso a paso. |
| `utils_visualizacion.py` | Funciones que dibujan los valores calculados en los cuadernos. |
| `requirements.txt` | Dependencias de los cuatro cuadernos. |
| `ANTES_DE_LA_CLASE.md` | Modelos y claves que hay que preparar. |
| `.env.example` | Plantilla de variables de entorno. Copiala como `.env`. |
| `salida/` | Se crea al ejecutar el cuaderno 03 con el informe que una persona aprobó. Se puede borrar. |

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

Los cuadernos 01 a 04 se ejecutaron de arriba abajo desde un kernel limpio el 23 de octubre de 2026, en una Mac con chip Apple y macOS 27, con Python 3.12.13, `smolagents` 1.26.0, `ollama` 0.6.3, `sentence-transformers` 6.2.0 y `granite4:latest`. También se probaron copias resueltas de sus microlaboratorios: todas las comprobaciones terminaron con `Correcto.`.

- **Gemini y SerpAPI no se ejecutaron.** Las celdas que los usan se escribieron y se comprobó que, sin clave, avisan y siguen; con clave nunca corrieron en esta versión.
- **Los agentes son variables.** Aun con temperatura `0` o con semilla, un agente local puede resolver una tarea en un paso en una ejecución y agotar sus pasos en otra. Las notas **Para mirar** citan resultados de conteo (corridas acertadas, pasos) de la ejecución guardada; si tu salida es distinta, no es necesariamente un error.
- **Un modelo chico.** Con `granite4` (3B), el diseño de la herramienta decide si el ciclo funciona; con un modelo más grande el contraste puede ser menor. Es un resultado de este modelo y estas tareas, no de los agentes en general.
- **Tiempos.** El cuaderno 02 tarda unos ocho minutos porque los agentes que fallan agotan sus pasos. Los tiempos dependen de la computadora.
- **Seguridad.** Un `CodeAgent` ejecuta en tu computadora el código que escribe el modelo. El intérprete restringido de `smolagents` filtra los módulos que se pueden importar, pero no es una barrera de seguridad; el aislamiento fuerte requiere otro ejecutor (por ejemplo, Docker), que esta unidad no usa. Las herramientas de los cuadernos solo leen y calculan.
- **Datos sintéticos.** Las ocho parcelas son inventadas. Las cifras comparan diseños entre sí; no describen ninguna explotación real.
- No se probaron Windows, Linux ni equipos sin GPU.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).
