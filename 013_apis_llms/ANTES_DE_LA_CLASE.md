# Antes de la clase

Son unos 15 minutos y casi todo es esperar una descarga. **Hacelo en tu casa**: descargar modelos con veinte personas en la misma red en el aula no funciona.

---

## 1. Entorno

Seguí [README.md](README.md), sección «Configurar el entorno local».

## 2. Ollama y el modelo (obligatorio)

Instalá [Ollama](https://ollama.com), abrilo y descargá el modelo de la unidad:

```
ollama pull granite4:latest
```

Pesa 2,1 GB y ocupa unos 2,7 GB de memoria mientras está cargado. Si Ollama no responde, abrí la aplicación o ejecutá `ollama serve` en una terminal.

## 3. Claves de API (gratuitas)

Los cuadernos usan dos servicios con plan gratuito. Sin clave, esas celdas avisan y el resto sigue funcionando.

| Servicio | Para qué | Cuaderno | Dónde se obtiene |
|---|---|---|---|
| Gemini | Comparar con un modelo remoto | 01, 02, 03, 04 | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| SerpAPI | Búsqueda web | 04 | [serpapi.com](https://serpapi.com) |

Copiá `.env.example` como `.env` y completá `GEMINI_API_KEY` y `SERPAPI_API_KEY`. Nunca subas `.env` ni pegues una clave dentro de un cuaderno. Los planes gratuitos tienen límites de pedidos; si superás el límite de Gemini, la celda muestra el error y sigue.

## 4. Verificación

Abrí `01_llamar_un_modelo.ipynb`, elegí el kernel `.venv` y ejecutá la primera celda de código. Tiene que decir `Ollama responde en ... y tiene granite4:latest.`
