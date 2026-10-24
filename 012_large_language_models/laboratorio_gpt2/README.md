# Laboratorio de ajuste fino con GPT-2 (unidad de Large Language Models, pieza 3)

**Laboratorio de PLN: Analítica, Textos y Cultura**  
Tecnicatura Superior en Ciencias de Datos e IA — IFTS N.º 24  
Matías Barreto, 2026  

Un laboratorio interactivo alrededor de una pregunta abierta: **¿podemos hacer que un modelo escriba un poco más como el autor que elegimos?** Se **ajusta** (*fine-tuning*) un modelo de lenguaje causal ya entrenado con un corpus propio, y se examina qué cambia en lo que genera y qué evidencia hay de ese cambio. El recorrido invita a probar: **elegir, cambiar un control, mirar, comparar y registrar**; el código siempre está disponible. No entrena un modelo desde cero ni configura un GPT dentro de ChatGPT.

Es la segunda pieza central de la unidad [Large Language Models](../README.md). Sigue a [Del texto de Borges al próximo token](../01_texto_a_proximo_token.ipynb) y retoma la adaptación de dominio de [transfer learning](../../010_transfer_learning/README.md).

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)**: instala el entorno con `uv` y baja el modelo (unos 250 MB) **antes de la clase**.

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

Después, en VS Code: abrí `01_laboratorio_gpt2.ipynb`, elegí el kernel `.venv` y ejecutá de arriba hacia abajo.

---

## Contenido

Un solo cuaderno con siete estaciones. Cada una empieza con un **desafío** breve y un **panel** con controles; las explicaciones vienen después, sobre lo que se acaba de ver. Los paneles tienen tres pestañas —**Explorar**, **Inspeccionar** y **Modificar**— y cada control lleva una etiqueta que dice si cambia el **experimento**, solo la **vista**, los **datos** o si solo **registra** una anotación. Una «vía con código» **alternativa** hace lo mismo sin controles; ningún panel exige haberla corrido.

| Estación | Desafío | Qué se hace |
|---|---|---|
| 1. Probá el modelo base | ¿Cómo continúa un texto el modelo antes de ajustar? | Generar con temperatura, `top_k`, `top_p` y semilla; comparar corridas; volver a una configuración anterior; actividad opcional de «una variable por vez» |
| 2. Elegí y revisá los textos | ¿Con qué textos ajustamos y qué problemas traen? | Mesa de trabajo del corpus: peso de cada texto y de cada grupo, incluir o excluir documentos, ver problemas concretos, **probar una limpieza con antes y después y aceptarla o descartarla**, volver al original, versiones con huella |
| 3. Mirá cómo el modelo lee | ¿Qué recibe realmente el modelo? | Vistas enlazadas de texto, tokens, bloques y documentos de origen; partición sin fuga; dónde se desplazan las etiquetas; qué es la pérdida |
| 4. Configurá el ajuste | ¿Qué cambiamos y por cuánto tiempo? | Configuración validada e inmutable, atada por huellas al corpus, la partición, el tokenizador y los bloques; lote efectivo y qué queda afuera de cada época; diagnóstico de hardware y ensayo de tiempo |
| 5. Observá el ajuste | ¿Qué pasa mientras se ajusta? | Ajuste en un hilo con progreso, pérdida de entrenamiento y validación, muestras fijas, checkpoints y **Detener** |
| 6. Compará y examiná la evidencia | ¿Qué cambió y con qué respaldo? | Comparador base y ajustado; inspector del siguiente token (con los números detrás del gráfico); ficha de lectura; pérdida y perplejidad; coincidencias con el corpus |
| 7. Guardá el experimento | ¿Cómo se vuelve sobre esto? | Exportar, recargar sin controles, reanudar verificando que los datos sean los mismos, ficha del experimento, bitácora con anotaciones identificadas |

### Cómo se recorre

1. De arriba hacia abajo, con `Restart Kernel and Run All Cells`. **No entrena**: las operaciones largas u opcionales están detrás de cuatro banderas `PERMITIR_...` de la celda de parámetros, todas en `False`. Con ese valor el cuaderno carga el modelo, el corpus y los datos, deja los paneles listos y no escribe experimentos.
   Los paneles de las estaciones 3 a 5 parten de dos pasos cortos (cargar el corpus y preparar los datos); ninguno parte de un entrenamiento previo. El panel de la estación 5 entrena cuando apretás **Iniciar ajuste**.
   Un ajuste de 60 pasos tardó unos 2 minutos en la Mac M2 con GPU `mps` donde se midió; en otra máquina puede variar mucho.
2. En cada estación: el desafío, la celda de **Preparación** (ejecutarla alcanza; su código aparece plegado si el entorno lo permite), el panel y, después, la explicación de lo observado. La profundización técnica está en bloques desplegables y la vía con código viene al final.
3. Anotar es opcional: la bitácora aparece en varios momentos del recorrido, con un registro más desarrollado al cerrar las estaciones 5 y 6.

### Limpieza de datos

En la estación 2 se transforman los textos del **corpus**. Es una decisión sobre los datos del experimento: se prueba, se compara y se acepta o se descarta, y el original se conserva.

---

## Datos de la unidad

- **Corpus principal:** 26 cuentos de Horacio Quiroga (dominio público), divididos en `adulto` (18) e `infantil` (8). Procedencia y limitaciones en [`datos/quiroga/FUENTE.md`](datos/quiroga/FUENTE.md). Los cuentos `adulto_07` e `infantil_04` quedan reservados para validación.
- **Textos propios:** 4 textos con derechos vigentes, solo para uso local. [`datos/textos/LEEME.md`](datos/textos/LEEME.md) explica las condiciones.
- **Modelo:** `DeepESP/gpt2-spanish` (MIT, 124 millones de parámetros). Ficha completa y criterio de elección en [`docs/MODELO.md`](docs/MODELO.md).

Para usar **tu corpus**, poné los archivos `.txt`, `.pdf` o `.epub` en una carpeta de la unidad y cargalos con `documento_desde_archivo(...)` en la estación 2. La celda de carga también suma un **texto de práctica inventado** (fuera del corpus) para probar limpiezas con cambios visibles.

---

## Qué ocupa lugar

Cada experimento se guarda en `experimentos/<nombre>/`. Un ajuste de 60 pasos con el último checkpoint completo ocupa **unos 2 GB**:

| Archivo | Tamaño aproximado |
|---|---|
| Checkpoint solo con pesos | 500 MB |
| Checkpoint con estado de optimizador | 1,5 GB |

Podés borrar la carpeta de un experimento cuando no la necesites. El cuaderno nunca borra ni pisa un experimento guardado. El comparador de la estación 6 guarda en memoria como máximo dos checkpoints (unos 500 MB cada uno) y tiene un botón **Liberar memoria**.

---

## Qué hay en la carpeta

| Archivo | Para qué |
|---|---|
| `01_laboratorio_gpt2.ipynb` | El laboratorio. La lógica central (tokenización, bloques, entrenamiento, evaluación, generación) está **a la vista** en las celdas |
| `utils.py` | Experiencia visual: paleta, estilo y gráficos. No contiene algoritmos de la unidad |
| `laboratorio.py` | Plomería: controles, estado de las estaciones, registro y archivos. Tampoco contiene algoritmos |
| `datos/` | Corpus y manifiestos |
| `docs/` | Ficha del modelo base |
| `experimentos/` | Salida de los experimentos |

---

## Límites

- **Dónde se probó:** el laboratorio se ejecutó, incluido un ajuste real, en una Mac con Apple Silicon (GPU `mps`), en octubre de 2026.
- **Dónde no se probó:** Google Colab (donde se usa `01_laboratorio_gpt2_colab.ipynb`), GPU NVIDIA, Linux ni Windows.
- **Uso con personas:** no se probó cómo se ven ni cómo se sienten los paneles en VS Code, ni cómo lo recorre un estudiante.

Las métricas del cuaderno describen cómo se comporta un modelo sobre un conjunto de texto. No miden calidad literaria, y las coincidencias con el corpus no prueban plagio ni su ausencia prueba originalidad.
