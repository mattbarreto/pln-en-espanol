# Unidad 016 — Modelos de decisión

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

En la unidad 015, el agente decidía qué herramienta usar escribiendo texto, y en la 013 la salida estructurada había que pedirla y validarla. Muchas veces el programa solo necesita **una decisión entre opciones conocidas**. Para eso apareció en 2026 una familia de modelos que no escriben: reciben un texto, una pregunta y las respuestas posibles, y devuelven una elección y una probabilidad para cada opción. TypeSafe los llama modelos *System One* y ofrece **Jev** como servicio pago; **Julia-1**, de Supersonic Labs, es un modelo gratuito con la misma interfaz.

La pregunta que guía la unidad es **qué cambia cuando un modelo elige entre opciones que define el programa, en lugar de escribir una respuesta, y cuándo conviene confiar en su elección**.

**Competencia.** Comprender cómo los LLM pueden coordinar herramientas para resolver tareas complejas, y qué modelos más chicos y controlables pueden tomar las decisiones de un sistema.

Es la continuación inmediata de `015_agentes`.

## Modelo y datos

- **Julia-1** ([SupersonicLabs/Julia-1](https://huggingface.co/SupersonicLabs/Julia-1)): licencia Apache 2.0, 144,3 millones de parámetros, construido sobre el codificador multilingüe mmBERT-small. Corre en la CPU. La primera celda del cuaderno lo descarga (unos 590 MB) en la carpeta `modelo/`, en una **revisión fija**.
- **Ollama con `granite4:latest`** (opcional): el mismo modelo de las unidades 013 a 015, para comparar en la sección 6. Si falta, la sección se saltea.
- **Datos:** ocho reseñas breves de películas imaginarias, escritas para el curso, dentro del cuaderno.

## Recorrido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| [`01_modelos_de_decision`](01_modelos_de_decision.ipynb) | ¿Qué cambia cuando un modelo elige entre opciones en lugar de escribir, y cuándo conviene confiar en su elección? | Una pregunta con opciones respondida por Julia-1, softmax hecho a mano, preguntas de los tres tipos combinadas en el código, una compuerta por confianza y una comparación con `granite4`. |

El cuaderno se presenta en clase y después se explora por cuenta propia: el código viene escrito, las notas **Para mirar** orientan la lectura y los dos **microlaboratorios** piden completar líneas y comprueban el resultado. El hilo conductor es que **una probabilidad no es una garantía**: el programa decide qué hacer con cada respuesta, y antes de dejar que un modelo decida solo hay que medir con casos propios si sus probabilidades separan los aciertos de los errores.

## Para seguir leyendo

- Documentación de TypeSafe ([docs.typesafe.ai](https://docs.typesafe.ai/introduction)): los tipos de pregunta, la confianza y los patrones de uso (enrutar por intención, compuerta por confianza, puntaje compuesto).
- `jev-benchmarks` ([github.com/AbdelStark/jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks)): cómo evaluar un modelo de decisión más allá de los aciertos (calibración y cobertura con un margen de error fijo).

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_modelos_de_decision.ipynb` | Recorrido de la unidad. |
| `utils.py` | Comprobaciones, descarga de Julia-1 en una revisión fija, la consulta a Ollama y las tablas y gráficos de probabilidades. |
| `utils_visualizacion.py` | Funciones que dibujan los valores calculados en el cuaderno (las mismas del resto de la materia). |
| `requirements.txt` | Dependencias del cuaderno. |
| `ANTES_DE_LA_CLASE.md` | Qué descargar antes de la clase. |
| `.env.example` | Plantilla para cambiar el modelo o la dirección de Ollama (opcional). |
| `modelo/` | Se crea al ejecutar la primera celda, con Julia-1. No sube al repositorio. Se puede borrar: se vuelve a descargar. |

## Configurar el entorno local

La unidad requiere Python 3.12 y `uv`. Instalá `uv` siguiendo las instrucciones de su [documentación oficial](https://docs.astral.sh/uv/).

Desde una terminal abierta en esta carpeta:

```bash
uv venv --python 3.12
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

No instales JupyterLab ni `notebook`: en VS Code, abrí la carpeta, instalá las extensiones de Python y Jupyter si hace falta, y elegí como kernel el entorno `.venv`.

Antes de la clase, seguí [ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md).

## Validación y límites

El cuaderno se ejecutó de arriba abajo desde un kernel limpio el 26 de octubre de 2026, en una Mac con chip Apple M2 y macOS 27, con Python 3.12.13, `torch` 2.14.1, `transformers` 5.0.0, `huggingface_hub` 1.33.0, `pandas` 3.1.0 y `granite4:latest`. Con el modelo ya descargado tarda menos de un minuto. También se ejecutó una copia resuelta de los dos microlaboratorios: las dos comprobaciones dieron `Correcto.`.

- **Julia-1 es un primer lanzamiento.** Su ficha lo presenta como la primera prueba del sistema de entrenamiento de Supersonic Labs. Fue evaluado con estados en JSON de flujos de trabajo sintéticos y con clasificación de noticias y emociones, y su desempeño en español no está medido por separado. Antes de armar el cuaderno se probó con 38 consultas sintéticas a un instituto (a qué área derivarlas) y acertó entre 14 y 17, en español y también en inglés, a menudo con probabilidades de 0,9 o más. Con la misma configuración, el benchmark oficial reproduce exactamente las cifras de la ficha: no es un error de instalación.
- **Ocho reseñas.** Muestran mecanismos y tipos de error; no estiman el desempeño de ningún modelo. Las cifras de `granite4` pueden cambiar entre versiones del modelo.
- **Jev no se probó**: requiere una clave paga.
- **Seguridad.** El paquete `julia/` viene dentro del repositorio del modelo y se ejecuta al importarlo. `utils.preparar_julia()` lo descarga en la revisión `a85b127` y lo agrega a la ruta de Python, sin instalarlo con pip.
- **Versión de `transformers`.** Julia-1 pide `transformers` 5.0 (y menor que 5.1). Si usás el entorno de otra unidad, instalar estos requisitos puede cambiarle la versión.
- No se probaron Windows, Linux ni la Lenovo con GPU.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).
