# Unidad 017 — Laboratorio de agentes

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

En la unidad 015 las herramientas de los agentes leían y calculaban. Este laboratorio da el paso siguiente: un asistente de biblioteca que **actúa en nombre de una persona** (renueva préstamos) y que **lee textos escritos por terceros** (las notas del catálogo). La pregunta que guía el recorrido es qué reglas se le pueden confiar al modelo y cuáles tiene que hacer cumplir el programa, y cómo se mide si una defensa funciona.

**Competencia.** Comprender cómo los LLM pueden coordinar herramientas para resolver tareas complejas, y qué controles hacen falta para que un agente actúe con consecuencias.

Es un anexo práctico de `015_agentes`. Conviene haber hecho al menos los cuadernos 01 y 03 de esa unidad.

## Modelo y datos

- **Ollama con `granite4:latest`** (IBM, 3B, 2,1 GB en disco), local y sin costo. Se usa con la llamada nativa a herramientas de Ollama, como en el cuaderno 01 de la unidad 015. No hace falta ninguna clave.
- **Datos sintéticos:** una biblioteca popular inventada, con seis personas socias, ocho préstamos y un catálogo de ocho libros (`datos/biblioteca.json`). Una de las notas del catálogo contiene un ataque escrito para el cuaderno 02.

## Recorrido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| [`01_un_agente_que_actua`](01_un_agente_que_actua.ipynb) | ¿Qué reglas se le pueden confiar al modelo y cuáles tiene que hacer cumplir el programa? | Un agente con una herramienta que renueva préstamos, una confirmación que decide el programa y una herramienta que no deja consultar los datos de otra persona. |
| [`02_atacar_y_medir`](02_atacar_y_medir.ipynb) | ¿Cómo sabemos si una defensa funciona, y cuál no depende de que el modelo obedezca? | Casos de prueba con chequeos en código, la medición de un ataque escondido en el catálogo frente a cuatro defensas y una decisión sobre cuáles usar. |

Cada cuaderno se presenta en clase y después se explora por cuenta propia: el código viene escrito, las notas **Para mirar** orientan la lectura y los **microlaboratorios** piden completar líneas y comprueban el resultado. El hilo conductor es que **una regla escrita en las instrucciones es un pedido, y una regla escrita en el código es una condición**: lo que tiene consecuencias se controla en el código, y lo que dice el agente se contrasta con el registro de lo que hizo.

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_un_agente_que_actua.ipynb` y `02_atacar_y_medir.ipynb` | Recorrido de la unidad. |
| `datos/` | Datos sintéticos de la biblioteca. La procedencia está en [`datos/LEEME.md`](datos/LEEME.md). |
| `utils.py` | Configuración, comprobaciones, carga de datos y las versiones completas de las herramientas, el ciclo y la confirmación que construye el cuaderno 01 (el 02 las usa desde ahí). |
| `utils_visualizacion.py` | Funciones que dibujan los valores calculados en los cuadernos (las mismas del resto de la materia). |
| `requirements.txt` | Dependencias de los dos cuadernos. |
| `ANTES_DE_LA_CLASE.md` | El modelo que hay que descargar. |
| `.env.example` | Plantilla para cambiar el modelo o la dirección de Ollama (opcional). |

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

## Validación y límites

Los cuadernos 01 y 02 se ejecutaron de arriba abajo desde un kernel limpio el 26 de octubre de 2026, en una Mac con chip Apple M2 y macOS 27, con Python 3.12.13, `ollama` 0.6.3 (biblioteca de Python), `pandas` 3.1.0 y `granite4:latest`. El 01 tardó alrededor de un minuto y el 02 unos cinco. También se ejecutaron copias resueltas de los cinco microlaboratorios: todas las comprobaciones terminaron con `Correcto.`.

- **Las cifras cambian con detalles chicos.** Con el mismo modelo y las mismas semillas, cambiar la dirección de correo de la nota del ataque movió las caídas sin defensa de 6 a 4 de 9, y las de «avisar en las instrucciones» de 2 a 4. Las notas **Para mirar** citan la ejecución guardada; si tu salida es distinta, no es necesariamente un error. Que las defensas que dependen del modelo sean inestables es parte de lo que muestra el cuaderno 02.
- **Un modelo chico.** Con `granite4` (3B) el agente se equivoca seguido al leer datos (por ejemplo, confunde renovaciones usadas con renovaciones disponibles). Con un modelo más grande los errores pueden ser menos frecuentes, pero las reglas que importan siguen yendo en el código.
- **Marcas internas.** A veces aparece en una respuesta una marca del formato del modelo, como `<|start_of_role>` o `<|end_of_role>`. No es un error del cuaderno.
- **Seguridad.** Las herramientas solo modifican datos en memoria: nada se escribe en disco y `utils.cargar_biblioteca()` vuelve todo al estado inicial. El correo y el teléfono del ataque no pueden pertenecer a nadie: el correo usa un dominio reservado para ejemplos y el número no está asignado.
- **Datos sintéticos.** La biblioteca y sus personas son inventadas. Las cifras comparan diseños entre sí con este modelo; no describen ningún sistema real.
- No se probaron Windows, Linux ni la Lenovo con GPU.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado, copiá el enlace de la carpeta en GitHub y pegalo en [Download Directory](https://download-directory.github.io/) o en [DownGit](https://downgit.github.io/).
