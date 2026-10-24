# Unidad 011 — Attention y Transformers

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

La unidad abre la caja del Transformer que se usó como herramienta en 010, con los números reales de dos modelos entrenados. Primero GPT-2 en español, sobre el primer verso del *Martín Fierro*: embeddings, posición, una neurona, la atención con su máscara causal y el bloque completo hasta el próximo token, cada cuenta recalculada a mano y comprobada contra el modelo. Después BETO, para medir qué hacen sus cabezas de atención y qué no se puede concluir de ellas.

## Contenido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| `01_pesos_y_secuencias.ipynb` | ¿Qué recibe un modelo en lugar de una palabra, qué hace una neurona con eso, y qué cambia cuando puede conectar directamente dos palabras lejanas? | El vector real de un token con su posición, una neurona real calculada a mano y comprobada, y una medición de cuánto conecta la atención dos tokens lejanos. |
| `02_atencion.ipynb` | ¿Cómo calcula GPT-2 cuánto pesa cada token anterior, y qué se puede concluir de esos pesos? | La matriz de atención de GPT-2 en español sobre un verso, recalculada a mano y comprobada contra el modelo, y una medida propia de qué mira una cabeza. |
| `03_del_bloque_al_token.ipynb` | ¿Cómo se convierte lo que calcula la atención en una distribución sobre el próximo token, y qué parte de lo que «sabe» el modelo está en los pesos? | El primer bloque de GPT-2 recalculado pieza por pieza, la distribución real del próximo token, una tabla de aciertos sobre el verso y el contraste con el mismo modelo con pesos al azar. |
| `04_atencion_en_beto.ipynb` | ¿Qué se puede leer de la atención de un modelo real y qué sería una afirmación excesiva? | Una medida de las 144 cabezas de BETO sobre dos versos y una decisión sobre qué afirmar. |

## Datos y modelos

- Los cuadernos 01, 02 y 03 usan GPT-2 en español (`DeepESP/gpt2-spanish`, licencia MIT, el mismo de la unidad 012; entrenado con 11,5 GB de Wikipedia y libros en español, sin filtrar, según su ficha) y el primer verso de *El gaucho Martín Fierro* (1872), de José Hernández, en dominio público. No hay números inventados: cada cuenta usa los pesos reales del modelo y se comprueba contra la que hace él.
- En el cuaderno 03, la sección 7 arma el mismo modelo con **pesos al azar** (semilla fija), declarado como contraste: muestra qué parte del resultado es mecanismo y qué parte es aprendizaje.
- El cuaderno 04 usa BETO (`dccuchile/bert-base-spanish-wwm-uncased`, el de 010) y dos versos de *El gaucho Martín Fierro* (1872), de José Hernández, en dominio público, tomados de `martin_fierro_estrofas.csv`, de la unidad 010. Es una inspección de un solo ejemplo, no una evaluación.

## Recursos visuales

Los cuatro cuadernos comparten la paleta y las formas de visualización de la materia, definidas en `utils_visualizacion.py` (y reexportadas por `utils.py`). Tres recursos atraviesan la unidad: paneles de números con un color por tipo de dato (naranja y azul para vectores con signo, violeta y gris para puntajes, naranja para pesos de atención), un mapa de GPT-2 leído del modelo cargado, con «estamos acá», y en el 02, escenas con controles. Cada escena se dibuja primero como salida estática, para los visores que no muestran controles.

## Configuración del entorno local

Desde esta carpeta:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

En Windows, activá con `.venv\Scripts\Activate.ps1`. Abrí la carpeta en VS Code con las extensiones de Python y Jupyter y elegí el kernel del entorno. No hace falta instalar JupyterLab ni `notebook`.

La unidad instala PyTorch y Transformers por el cuaderno 04; el modelo no se instala con `pip`. Antes de la clase, seguí [ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md): si hiciste 010 en esta computadora, BETO ya está en el caché.

## Relación con el recorrido

La unidad sigue a `010_transfer_learning`: allí se usaron y ajustaron modelos preentrenados; acá se inspecciona la arquitectura que permite que esos modelos relacionen contexto. `012_large_language_models` continúa con GPT-2 como caso de un Transformer decoder-only que predice el próximo token.

## Estado de verificación

Los cuatro cuadernos se ejecutaron de arriba abajo con kernel limpio el 24/10/2026, en Windows 11 y en CPU, con Python 3.12.9, numpy 2.5.4, matplotlib 3.11.2, torch 2.14.1, transformers 4.57.6 e ipywidgets 8.1.9. Los cuadernos 01 a 03 se ejecutaron también con una copia resuelta de sus microlaboratorios: todas las comprobaciones dan `Correcto.`. Cada cuenta recalculada a mano coincide con la del modelo salvo redondeo (diferencias menores que 0,0001). La versión anterior de la unidad, con números sintéticos, se había probado en macOS; esta todavía no. `requirements.txt` fija solo versiones mínimas (y `transformers` por debajo de 5.0): antes de reutilizar la unidad en otro año, conviene volver a ejecutarla.
