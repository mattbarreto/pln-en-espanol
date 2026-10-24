# Unidad 011 — Attention y Transformers

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

La unidad abre la caja del Transformer que se usó como herramienta en 010. Primero con vectores sintéticos pequeños, para volver visibles los pesos, la atención, la máscara causal y el bloque completo hasta el próximo token. Después con BETO, para medir qué hacen sus cabezas de atención sobre dos versos del *Martín Fierro* y qué no se puede concluir de ellas.

## Contenido

| Cuaderno | Pregunta | Producto |
|---|---|---|
| `01_pesos_y_secuencias.ipynb` | ¿Qué cambia cuando una red puede conectar directamente partes relevantes de una secuencia? | Explicación visual de una neurona y comparación entre lectura secuencial y atención. |
| `02_atencion.ipynb` | ¿Cómo calcula un Transformer qué contexto usar y por qué GPT no mira el futuro? | Matriz de atención, máscara causal y explicación de un bloque decoder-only. |
| `03_del_bloque_al_token.ipynb` | ¿Cómo se convierte el contexto que calcula la atención en una distribución sobre la palabra que sigue? | Un bloque Transformer calculado de punta a punta y la lectura de su salida como distribución del próximo token. |
| `04_atencion_en_beto.ipynb` | ¿Qué se puede leer de la atención de un modelo real y qué sería una afirmación excesiva? | Una medida de las 144 cabezas de BETO sobre dos versos y una decisión sobre qué afirmar. |

## Datos y modelos

- Los cuadernos 01, 02 y 03 usan números **sintéticos**, declarados como tales: muestran el mecanismo, no evalúan la calidad de un modelo de lenguaje. En 03 los pesos son al azar y sin entrenar.
- El cuaderno 04 usa BETO (`dccuchile/bert-base-spanish-wwm-uncased`, el de 010) y dos versos de *El gaucho Martín Fierro* (1872), de José Hernández, en dominio público, tomados de `martin_fierro_estrofas.csv`, de la unidad 010. Es una inspección de un solo ejemplo, no una evaluación.

## Recursos visuales

Los cuatro cuadernos comparten la paleta y las formas de visualización de la materia (fichas, barras, barras agrupadas, mapas de calor, dispersión y el diagrama del bloque), definidas en `utils.py`. El 02 incluye un selector interactivo de filas de atención y conserva una salida estática equivalente para visores sin widgets.

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

Ejecutada de arriba abajo con kernel limpio, y con una copia resuelta de los microlaboratorios, el 23/10/2026 en macOS con Python 3.12, numpy 2.5.4, matplotlib 3.11.2, torch 2.14.1 y transformers 4.57.6. **No se probó en Windows.** `requirements.txt` fija solo versiones mínimas (y `transformers` por debajo de 5.0): antes de reutilizar la unidad en otro año, conviene volver a ejecutarla.
