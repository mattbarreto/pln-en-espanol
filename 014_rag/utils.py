"""Utilidades accesorias de la unidad 014: RAG.

Reune configuracion, comprobaciones, carga de datos y las versiones
completas de funciones que los cuadernos construyen paso a paso.
"""
import json
import logging
import os
import sys
from importlib import metadata
from pathlib import Path

# Silencian avisos y barras de progreso que no aportan al aprendizaje. Tienen
# que definirse antes de importar torch y transformers.
os.environ.setdefault("TQDM_DISABLE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
logging.getLogger(
    "torch.distributed.elastic.multiprocessing.redirects"
).setLevel(logging.ERROR)

import pandas as pd  # noqa: E402
import requests  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from utils_visualizacion import (  # noqa: F401
    dibujar_barras,
    dibujar_barras_agrupadas,
    dibujar_mapa_de_calor,
)

RUTA_DATOS = Path(__file__).resolve().parent / "datos"
RUTA_CHROMA = Path(__file__).resolve().parent / "chroma_db"

# Las claves y el modelo local se leen del archivo .env, si existe.
load_dotenv()

URL_OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODELO_LOCAL = os.getenv("OLLAMA_MODEL", "granite4:latest")
MODELO_GEMINI = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MODELO_EMBEDDINGS = "intfloat/multilingual-e5-small"

# Las tablas muestran los textos completos, sin cortarlos con puntos.
pd.set_option("display.max_colwidth", None)

TILDES = str.maketrans("áéíóú", "aeiou")


def comprobar(condicion: bool, pista: str) -> None:
    """Informa si una condicion se cumplio, sin cortar el cuaderno.

    Args:
        condicion: Resultado de la comparacion que se quiere comprobar.
        pista: Mensaje que ayuda a revisar el paso si no se cumplio.

    Returns:
        None. Imprime "Correcto." o "Todavia no: <pista>".
    """
    if condicion:
        print("Correcto.")
    else:
        print(f"Todavia no: {pista}")


def versiones(paquetes: list[str]) -> dict[str, str]:
    """Devuelve la version de Python y la de cada paquete pedido.

    Args:
        paquetes: Nombres de los paquetes, como aparecen en pip.

    Returns:
        Diccionario de nombre a version.
    """
    resultado = {"python": sys.version.split()[0]}
    for nombre in paquetes:
        resultado[nombre] = metadata.version(nombre)
    return resultado


def tabla(filas: list[dict]) -> pd.DataFrame:
    """Convierte una lista de diccionarios en una tabla para mostrar.

    Args:
        filas: Lista de diccionarios con las mismas claves.

    Returns:
        Tabla de pandas con una fila por diccionario.
    """
    return pd.DataFrame(filas)


def normalizar(texto: str) -> str:
    """Pasa a minusculas y quita tildes para comparar textos.

    Args:
        texto: Texto a normalizar.

    Returns:
        El texto en minusculas y sin tildes.
    """
    return texto.lower().translate(TILDES)


def hay_clave(nombre: str) -> bool:
    """Indica si una variable de entorno con una clave esta definida.

    Args:
        nombre: Nombre de la variable, por ejemplo "GEMINI_API_KEY".

    Returns:
        True si tiene contenido.
    """
    return bool(os.getenv(nombre, "").strip())


def avisar_sin_clave(nombre: str) -> None:
    """Explica que una celda opcional se omite porque falta una clave.

    Args:
        nombre: Nombre de la variable que falta.
    """
    print(
        f"Sin {nombre}: se omite esta parte. Copia .env.example como .env, "
        "completa la clave y reinicia el kernel."
    )


def comprobar_modelo_local() -> None:
    """Verifica que Ollama responda y que el modelo de la unidad exista.

    Raises:
        RuntimeError: Si falta el servidor o el modelo.
    """
    try:
        respuesta = requests.get(f"{URL_OLLAMA}/api/tags", timeout=5)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(
            f"No hay respuesta de Ollama en {URL_OLLAMA}. "
            "Abri la aplicacion o ejecuta 'ollama serve' en una terminal."
        ) from error
    nombres = []
    for modelo in respuesta.json()["models"]:
        nombres.append(modelo["name"])
    if MODELO_LOCAL not in nombres:
        raise RuntimeError(
            f"Falta el modelo {MODELO_LOCAL}. "
            f"Descargalo con: ollama pull {MODELO_LOCAL}"
        )
    print(f"Ollama responde en {URL_OLLAMA} y tiene {MODELO_LOCAL}.")


def crear_embeddings(con_prefijos: bool = True) -> HuggingFaceEmbeddings:
    """Crea el modelo de embeddings de la unidad.

    Args:
        con_prefijos: Si es True, agrega "passage: " a los fragmentos y
            "query: " a las consultas, como exige la familia E5.

    Returns:
        Objeto de LangChain con embed_documents y embed_query.
    """
    if con_prefijos:
        para_fragmentos = {"prompt": "passage: ", "normalize_embeddings": True}
        para_consultas = {"prompt": "query: ", "normalize_embeddings": True}
    else:
        para_fragmentos = {"normalize_embeddings": True}
        para_consultas = {"normalize_embeddings": True}
    return HuggingFaceEmbeddings(
        model_name=MODELO_EMBEDDINGS,
        encode_kwargs=para_fragmentos,
        query_encode_kwargs=para_consultas,
    )


def unir_palabras_cortadas(texto: str) -> str:
    """Une las palabras que un PDF corta con guion al final de un renglon.

    Es la version completa de la funcion del cuaderno 01.

    Args:
        texto: Texto extraido de un PDF.

    Returns:
        El texto con las palabras cortadas unidas.
    """
    texto_reparado = texto.replace(" -\n", "")
    return texto_reparado.replace("-\n", "")


def cargar_pdf(ruta: Path, fuente: str) -> list[Document]:
    """Lee un PDF y devuelve un Document por pagina.

    Es la version completa de la funcion del cuaderno 01.

    Args:
        ruta: Ubicacion del archivo PDF.
        fuente: Nombre que se guarda como procedencia.

    Returns:
        Lista de Document con "fuente" y "pagina" (desde 1) como metadatos.
    """
    lector = PdfReader(str(ruta))
    paginas = []
    numero_de_pagina = 0
    for pagina in lector.pages:
        numero_de_pagina += 1
        paginas.append(
            Document(
                page_content=pagina.extract_text() or "",
                metadata={"fuente": fuente, "pagina": numero_de_pagina},
            )
        )
    return paginas


def cargar_documentos_de_acme(
    tamano: int = 500, solapamiento: int = 80
) -> list[Document]:
    """Carga y fragmenta las dos politicas de Tintas Acme.

    Es la version completa del recorrido del cuaderno 01 para el PDF y el
    Markdown de la empresa.

    Args:
        tamano: Largo maximo de cada fragmento, en caracteres.
        solapamiento: Caracteres que se repiten entre fragmentos vecinos.

    Returns:
        Fragmentos con metadatos de procedencia.
    """
    paginas = cargar_pdf(
        RUTA_DATOS / "politica_interna_tintas_acme.pdf",
        "politica_interna_tintas_acme.pdf",
    )
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=tamano, chunk_overlap=solapamiento
    )
    fragmentos = divisor.split_documents(paginas)
    fragmentos += cargar_politica_remota(tamano, solapamiento)
    return fragmentos


def cargar_politica_remota(
    tamano: int = 500, solapamiento: int = 80
) -> list[Document]:
    """Carga y fragmenta la politica de trabajo remoto de Acme.

    Args:
        tamano: Largo maximo de cada fragmento, en caracteres.
        solapamiento: Caracteres que se repiten entre fragmentos vecinos.

    Returns:
        Fragmentos con la fuente y la seccion como metadatos.
    """
    texto = (RUTA_DATOS / "politica_trabajo_remoto_tintas_acme.md").read_text(
        encoding="utf-8"
    )
    cortador = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "titulo"), ("##", "seccion")]
    )
    secciones = cortador.split_text(texto)
    for seccion in secciones:
        seccion.metadata["fuente"] = "politica_trabajo_remoto_tintas_acme.md"
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=tamano, chunk_overlap=solapamiento
    )
    return divisor.split_documents(secciones)


def cargar_cuentos() -> pd.DataFrame:
    """Lee los fragmentos de cuentos de la unidad 009.

    Returns:
        Tabla con id, texto, autor, titulo, fuente y palabras.
    """
    return pd.read_csv(RUTA_DATOS / "cuentos" / "fragmentos.csv")


def cargar_json(nombre: str) -> list[dict]:
    """Lee un JSON de datos/ y devuelve su contenido.

    Args:
        nombre: Nombre del archivo dentro de datos/.

    Returns:
        Contenido del archivo.
    """
    with open(RUTA_DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def formatear_contexto(documentos: list[Document]) -> str:
    """Convierte fragmentos en un texto con etiquetas de procedencia.

    Es la version completa de la funcion del cuaderno 03.

    Args:
        documentos: Fragmentos recuperados, con "fuente" y "pagina" o
            "seccion" en los metadatos.

    Returns:
        Texto con una etiqueta entre corchetes antes de cada fragmento.
    """
    bloques = []
    for documento in documentos:
        metadatos = documento.metadata
        if "pagina" in metadatos:
            lugar = f"pagina {metadatos['pagina']}"
        else:
            lugar = f"seccion {metadatos.get('seccion', '(portada)')}"
        etiqueta = f"[{metadatos['fuente']}, {lugar}]"
        bloques.append(f"{etiqueta}\n{documento.page_content}")
    return "\n\n".join(bloques)


def diagnosticar(fila: dict) -> str:
    """Clasifica una fila de la evaluacion del cuaderno 03.

    Es la version completa de la funcion que se escribe en el cuaderno.

    Args:
        fila: Fila con "acierta" y "evidencia en el contexto".

    Returns:
        "ok", "fallo la busqueda", "fallo el modelo" o "revisar a mano".
    """
    if fila["acierta"]:
        return "ok"
    if fila["evidencia en el contexto"] is False:
        return "fallo la busqueda"
    if fila["evidencia en el contexto"] and not fila["acierta"]:
        return "fallo el modelo"
    return "revisar a mano"


def precision_en_k(relevancias: list[int], k: int) -> float:
    """Calcula que proporcion de los k primeros resultados es relevante.

    Es la version completa de la funcion del cuaderno 04. Un resultado
    cuenta como relevante si su relevancia es 1 o 2.

    Args:
        relevancias: Relevancia de cada resultado, en el orden del ranking.
        k: Cuantos resultados se miran.

    Returns:
        Un numero entre 0 y 1.
    """
    aciertos = 0
    for relevancia in relevancias[:k]:
        if relevancia >= 1:
            aciertos += 1
    return aciertos / k


def rango_reciproco(relevancias: list[int]) -> float:
    """Calcula 1 dividido la posicion del primer resultado relevante.

    Es la version completa de la funcion del cuaderno 04.

    Args:
        relevancias: Relevancia de cada resultado, en el orden del ranking.

    Returns:
        Un numero entre 0 y 1; 0 si ningun resultado es relevante.
    """
    posicion = 0
    for relevancia in relevancias:
        posicion += 1
        if relevancia >= 1:
            return 1 / posicion
    return 0.0
