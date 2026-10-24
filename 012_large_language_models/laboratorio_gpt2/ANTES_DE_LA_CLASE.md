# Antes de la clase

El laboratorio se hace **en tu máquina, con VS Code**, igual que las unidades 2, 3, 4, 8 y 12. El modelo pesa unos 250 MB: bajarlo en clase, con veinte personas en la misma red, no funciona. Hacé estos pasos **antes de llegar**.

También puede correr en una máquina con GPU NVIDIA o en Google Colab (con `01_laboratorio_gpt2_colab.ipynb`, que se sube solo): el cuaderno no averigua dónde está; usa lo que haya. Eso **no se probó**.

---

## 1. Entorno

Parado **dentro** de `laboratorio_gpt2/`:

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

En macOS o Linux, si no tenés `uv`:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

En Windows, PowerShell:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después, en VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → elegí `.venv`. Y al abrir el cuaderno, *Select Kernel* → `.venv`.

Usá Python 3.12. Con versiones muy nuevas, `torch` puede no tener todavía paquetes listos. Este laboratorio se probó con `torch` 2.14, `transformers` 5.19 e `ipywidgets` 8.1.

---

## 2. El modelo

Bajalo ahora, en tu casa, con el entorno activado:

```
.venv/bin/python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; m='DeepESP/gpt2-spanish'; r='1b935e39cf9893108bd2f4fb5317f48ae1c3ab5e'; AutoTokenizer.from_pretrained(m, revision=r); AutoModelForCausalLM.from_pretrained(m, revision=r); print('Modelo listo')"
```

En Windows reemplazá `.venv/bin/python` por `.venv\Scripts\python`. Tiene que terminar en `Modelo listo`. Si lo bajaste para la unidad de transfer learning, ya está en la caché de Hugging Face y tarda un segundo. El aviso sobre `masked_bias` es normal.

---

## 3. Espacio en disco

Cada experimento ocupa hasta unos 2 GB (ver el README). Reservá al menos 5 GB libres.

---

## 4. Prueba rápida

Abrí `01_laboratorio_gpt2.ipynb` y ejecutá hasta la celda «Cargar el modelo base y su tokenizador». Tiene que mostrar 124.439.808 parámetros y un vocabulario de 50.257 tokens. Si ves eso, estás listo.

Con las banderas `PERMITIR_...` en `False` (el valor de entrada), `Run All` no entrena y tarda poco: en la Mac M2 donde se midió, menos de un minuto. Con todo habilitado, el cuaderno entero llevó unos 2 a 3 minutos de cómputo en esa Mac; en CPU suele ser bastante más (la estación 4 puede medir el tiempo en tu máquina).

---

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| `No module named torch` | El kernel no es el de `.venv`: volvé a elegirlo |
| La carga del modelo se queda esperando | No hay conexión o el modelo no está en la caché: repetí el paso 2 con internet |
| La pérdida aparece como `nan` | No cambies la precisión: el cuaderno usa `float32` por una razón (ver `docs/MODELO.md`) |
| «Ya existe …» al consolidar | Elegí otro nombre de experimento: nunca se pisa uno guardado |
