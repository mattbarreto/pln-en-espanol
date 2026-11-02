# Antes de la clase

Son unos 15 minutos. **Hacelo en tu casa**: descargar el modelo con veinte personas en la misma red en el aula no funciona.

---

## 1. Entorno

Seguí [README.md](README.md), sección «Configurar el entorno local». Esta unidad tiene su propio entorno: Julia-1 pide una versión fija de `transformers`.

## 2. Julia-1 (obligatorio)

Abrí `01_modelos_de_decision.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda de código. La primera vez descarga el modelo, unos 590 MB, en la carpeta `modelo/`; las siguientes usa esa copia.

Tiene que terminar mostrando las versiones de `torch`, `transformers`, `huggingface_hub` y `pandas`. Después ejecutá la segunda celda: tiene que decir `Modelo cargado.`

## 3. Ollama (opcional)

Solo para la sección 6. Si ya preparaste las unidades 013 a 015, no hace falta nada más. Si no, instalá [Ollama](https://ollama.com) y descargá el modelo:

```
ollama pull granite4:latest
```

No hacen falta claves de API.
