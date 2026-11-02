# Antes de la clase

Son unos 10 minutos si ya preparaste la unidad 015, y unos 20 si no. **Hacelo en tu casa**: descargar el modelo con veinte personas en la misma red en el aula no funciona.

---

## 1. Entorno

Seguí [README.md](README.md), sección «Configurar el entorno local». Esta unidad no usa `smolagents` ni modelos de embeddings: el entorno es liviano.

## 2. Ollama y el modelo de lenguaje (obligatorio)

Es el mismo modelo de las unidades 013 a 015. Si ya lo tenés, pasá al punto 3.

Instalá [Ollama](https://ollama.com), abrilo y descargá el modelo:

```
ollama pull granite4:latest
```

Pesa 2,1 GB. Si Ollama no responde, abrí la aplicación o ejecutá `ollama serve` en una terminal.

## 3. Verificación

Abrí `01_un_agente_que_actua.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda de código: tiene que decir `Ollama responde en ... y tiene granite4:latest.`

No hacen falta claves de API.
