# Unidad 010 — Transfer learning

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

En esta unidad pasamos de usar modelos preentrenados a adaptarlos a una tarea y a un dominio. Exploramos cuatro tareas de procesamiento de lenguaje, ajustamos un clasificador de textos y adaptamos BETO a estrofas del *Martín Fierro*. La pregunta que guía el recorrido es cuándo alcanza un modelo disponible y cuándo conviene ajustarlo.

## Recorrido

| Cuaderno | Tema | Recorrido |
|---|---|---|
| [`01_explorar_tareas.ipynb`](01_explorar_tareas.ipynb) | Modelos preentrenados | Exploramos clasificación, reconocimiento de entidades, preguntas y respuestas, y traducción con `pipeline`. |
| [`02_ajustar_una_tarea.ipynb`](02_ajustar_una_tarea.ipynb) | Ajuste de una tarea | Comparamos una referencia basada en TF-IDF con BETO ajustado para clasificar textos. |
| [`03_adaptar_un_dominio.ipynb`](03_adaptar_un_dominio.ipynb) | Adaptación de dominio | Adaptamos BETO con estrofas del *Martín Fierro* y comparamos sus propuestas antes y después. |

Las extensiones de esta unidad pasaron a otras: el ajuste eficiente con LoRA y Unsloth, a `012_large_language_models/extensiones/`.

## Cómo se trabaja

Cada cuaderno combina código ejecutable, explicaciones breves y notas **Para mirar** que orientan la lectura de las salidas. Al final de cada tema hay microlaboratorios con líneas para completar y una comprobación automática. El recorrido termina con una decisión sobre las condiciones en que sería razonable usar cada modelo.

## Configurar el entorno local

La unidad requiere Python 3.12 y `uv`. Instalá `uv` siguiendo las instrucciones de su [documentación oficial](https://docs.astral.sh/uv/).

Desde una terminal abierta en esta carpeta, creá el entorno:

```bash
uv venv --python 3.12
```

Activá el entorno. En macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows, desde PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalá las dependencias de los tres cuadernos centrales:

```bash
uv pip install -r requirements.txt
```

No instales JupyterLab ni `notebook`: en VS Code, abrí la carpeta, instalá las extensiones de Python y Jupyter si hace falta, y elegí como kernel el entorno `.venv`.

Al terminar, desactivá el entorno con `deactivate`. Para volver a trabajar, no hace falta crearlo de nuevo: activalo e iniciá VS Code con ese entorno seleccionado.

Los modelos no se instalan con `pip`. Antes de la clase, descargalos y verificá el entorno siguiendo [ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md). La descarga inicial ronda los 2,1 GB; reservá al menos 6 GB libres. 

## Ejecución remota desde VS Code

La extensión oficial de Google Colab permite elegir un kernel remoto desde VS Code. Este procedimiento no se probó en esta versión de la unidad.

- El kernel remoto no ve los archivos locales: copiá la carpeta de la unidad al entorno remoto para que estén disponibles `utils.py` y `datos/`.
- Los modelos se descargan de nuevo en cada sesión nueva.
- Instalá en el entorno remoto las dependencias de `requirements.txt`.

## Archivos de la unidad

| Archivo o carpeta | Contenido |
|---|---|
| `01_explorar_tareas.ipynb` a `03_adaptar_un_dominio.ipynb` | Recorrido central de la unidad. |
| `datos/` | Datos utilizados por los cuadernos. La procedencia y las condiciones de uso están en [`datos/LEEME.md`](datos/LEEME.md). |
| `utils.py` | Funciones auxiliares para datos, tablas, comprobaciones y gráficos compartidos. |
| `utils_visualizacion.py` | Funciones compartidas para dibujar los valores calculados en los cuadernos. |
| `requirements.txt` | Dependencias de los tres cuadernos centrales. |
| `ANTES_DE_LA_CLASE.md` | Preparación y descarga previa de los modelos. |

## Datos y licencias

- Los textos sintéticos incluidos en `datos/` se publican bajo CC0-1.0. Consultá [`datos/LEEME.md`](datos/LEEME.md) para su procedencia y condiciones de uso.
- *El gaucho Martín Fierro* (José Hernández, 1872) es de dominio público. Las estrofas utilizadas provienen del taller «Modelos de lenguaje a tu medida», publicado bajo licencia MIT. El archivo no incluye *La vuelta de Martín Fierro* (1879).
- `Helsinki-NLP/opus-mt-es-en` declara Apache-2.0 en su ficha de Hugging Face. Las fichas consultadas para `pysentimiento/robertuito-sentiment-analysis`, `mrm8488/bert-spanish-cased-finetuned-ner`, `mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es` y `dccuchile/bert-base-spanish-wwm-uncased` no informaban una licencia al momento de la revisión. Revisá las fichas antes de reutilizar esos modelos.

## Validación y límites

Las pruebas registradas el 22 de octubre de 2026 se hicieron en una Mac con chip Apple, Python 3.12, `torch` 2.14.1 y `transformers` 4.57.6. Los cuadernos 01, 02 y 03 se ejecutaron desde un kernel limpio; también se probaron copias resueltas de sus microlaboratorios. Las comprobaciones de esas copias terminaron con `Correcto.`. Los tiempos y resultados pueden variar según el equipo y las versiones de las dependencias.

No se probaron Windows, Linux, Colab remoto desde VS Code. Tampoco se midieron los tiempos en las computadoras del aula. La unidad fija `transformers<5.0`; no se validó con la serie 5.x.

En Mac con chip Apple, los cuadernos 02 y 03 usan `attn_implementation="eager"` porque la atención predeterminada presentó errores durante el entrenamiento en GPU. En el cuaderno 02, el F1 de BETO en validación varió entre CPU y GPU; por ese motivo no se presenta como una cifra estable.

## Descargar solo esta carpeta

Esta unidad forma parte de un repositorio más amplio. Para descargarla por separado:

1. Copiá el enlace de la carpeta en GitHub, pegalo en [Download Directory](https://download-directory.github.io/) y descargá el archivo `.zip`.
2. Como alternativa, pegá el mismo enlace en [DownGit](https://downgit.github.io/) y seleccioná **Download**.
