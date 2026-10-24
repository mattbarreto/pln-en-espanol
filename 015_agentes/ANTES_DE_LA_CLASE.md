# Antes de la clase

Son unos 20 minutos y casi todo es esperar descargas. **Hacelo en tu casa**: descargar modelos con veinte personas en la misma red en el aula no funciona.

---

## 1. Entorno

Seguí [README.md](README.md), sección «Configurar el entorno local».

## 2. Ollama y el modelo de lenguaje (obligatorio)

Instalá [Ollama](https://ollama.com), abrilo y descargá el modelo de la unidad:

```
ollama pull granite4:latest
```

Pesa 2,1 GB y ocupa unos 3,3 GB de memoria mientras está cargado con la ventana de contexto de los agentes. Si Ollama no responde, abrí la aplicación o ejecutá `ollama serve` en una terminal.

## 3. Modelo de embeddings (cuaderno 04)

Con el entorno activo, descargá el modelo con el que busca la herramienta de políticas (unos 470 MB):

```
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-small')"
```

## 4. Claves de API (gratuitas, opcionales)

Sin clave, esas celdas avisan y el resto sigue funcionando. Nunca subas `.env` ni pegues una clave dentro de un cuaderno.

| Servicio | Para qué | Cuaderno | Dónde se obtiene |
|---|---|---|---|
| Gemini | Usar un modelo remoto como cerebro del agente | 02, 03, 04 | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| SerpAPI | Una herramienta de búsqueda web | 04 | [serpapi.com](https://serpapi.com) |

Copiá `.env.example` como `.env` y completá `GEMINI_API_KEY` y `SERPAPI_API_KEY`. Los planes gratuitos tienen límites de pedidos; si los superás, la celda muestra el error y sigue.

## 5. Verificación

Abrí `01_herramientas.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda de código: tiene que decir `Ollama responde en ... y tiene granite4:latest.`
