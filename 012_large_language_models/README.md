# Unidad 012 — Large Language Models: GPT-2 como caso de estudio

**Materiales desarrollados por Matías Barreto, 2026**

**Tecnicatura Superior en Ciencias de Datos e IA, IFTS N.º 24**
* **Nomenclatura oficial:** Procesamiento de Lenguaje Natural
* **Nombre de trabajo:** Laboratorio de PLN: Analítica, Textos y Cultura

---

Un modelo generativo no escribe un texto de una vez: predice un próximo token, lo incorpora al
prefijo y vuelve a predecir. Esta unidad sigue ese mecanismo desde un fragmento de Borges hasta el
ajuste y la evaluación de GPT-2.

Viene después de Attention y Transformers, y antes de consumir modelos por API, RAG y agentes.

## Recorrido central

| Orden | Pieza | Pregunta | Qué se hace |
|---|---|---|---|
| 1 | [texto local](01_texto_a_proximo_token.ipynb) | ¿Cómo se transforma un texto en ejemplos de próximo token? | BPE, IDs, ventanas, objetivo desplazado y posición, con el texto Tlön, Uqbar, Orbis Tertius. |
| 2 | [laboratorio GPT-2](laboratorio_gpt2/README.md) | ¿Qué cambia tras ajustar un modelo generativo y qué evidencia tenemos? | Corpus, bloques, configuración, ajuste, comparación, evaluación y bitácora. |

La primera pieza se ejecuta **solo en computadora local**. El laboratorio tiene su propio entorno y
sus instrucciones de preparación; consultá su README y
[ANTES_DE_LA_CLASE.md](laboratorio_gpt2/ANTES_DE_LA_CLASE.md).

## Hilo conceptual

    Borges
      -> BPE y tokens
      -> ventanas de entrada y objetivo desplazado
      -> embeddings de token y posición
      -> Transformer causal de 011
      -> logits y distribución del próximo token
      -> GPT-2 base
      -> ajuste, comparación y evidencia

La unidad 011 explica por qué el Transformer causal no mira tokens futuros. La primera pieza de
esta unidad muestra cómo se construyen los pares que permiten aprender esa tarea. El laboratorio
usa bloques de ese tipo para ajustar DeepESP/gpt2-spanish y examinar el resultado sin equiparar
pérdida, coincidencia o fluidez con calidad literaria.

## Extensión

[`extensiones/04_ajuste_eficiente_unsloth.ipynb`](extensiones/04_ajuste_eficiente_unsloth.ipynb): ajuste eficiente con LoRA y Unsloth (Llama 3.2). Es opcional; corre solo en Google Colab con GPU, instala sus propias dependencias y no se ejecutó en esta versión del repositorio. Viene de la unidad 010. El modelo declara la licencia Llama 3.2: consultá sus condiciones antes de reutilizarlo.

## Configuración de la pieza 1

Desde esta carpeta:

    uv venv --python 3.12
    source .venv/bin/activate
    uv pip install -r requirements.txt

En Windows, activá con .venv\Scripts\Activate.ps1. Abrí esta carpeta en VS Code, elegí el kernel
del entorno y ejecutá el cuaderno de arriba hacia abajo. No hace falta instalar JupyterLab ni
notebook.

