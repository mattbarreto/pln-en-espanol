# Antes de la clase

Son unos 20 minutos y casi todo es esperar descargas. **Hacelo en tu casa**: descargar modelos con veinte personas en la misma red en el aula no funciona.

---

## 1. Entorno

Seguí [README.md](README.md), sección «Configurar el entorno local».

## 2. Modelos de embeddings

Con el entorno activo, descargá los dos modelos que usa la unidad (unos 470 MB cada uno; el segundo es el de la unidad 009 y quizá ya lo tengas):

```
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-small'); SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"
```

`intfloat/multilingual-e5-small` es el modelo de la unidad. Usa los prefijos `query: ` y `passage: `.

## 3. Ollama y el modelo de lenguaje (obligatorio)

Instalá [Ollama](https://ollama.com), abrilo y descargá el modelo de la unidad:

```
ollama pull granite4:latest
```

Pesa 2,1 GB y ocupa unos 2,7 GB de memoria mientras está cargado. Es el modelo con el que se probaron los cuadernos 03.

## 4. Clave de API (gratuita, opcional)

El cuaderno 03 puede comparar con Gemini. Copiá `.env.example` como `.env` y completá `GEMINI_API_KEY` (se obtiene en [aistudio.google.com/apikey](https://aistudio.google.com/apikey)). Nunca subas `.env` ni pegues una clave dentro de un cuaderno. Sin clave, esa parte avisa y el resto sigue funcionando.

## 5. Verificación

Abrí `02_base_vectorial.ipynb`, elegí el kernel `.venv` y ejecutá hasta la sección 1: tiene que imprimir `Largo del vector: 384`. Abrí `03_responder_con_fuentes.ipynb` y ejecutá la primera celda de código: tiene que decir `Ollama responde en ... y tiene granite4:latest.`
