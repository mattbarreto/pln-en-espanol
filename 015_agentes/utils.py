"""Utilidades accesorias de la unidad 015: Agentes.

Reune configuracion, comprobaciones, carga de datos, la conexion con los
modelos y una busqueda sencilla sobre las politicas de Tintas Acme. La
logica de cada agente y de cada herramienta se escribe en los cuadernos.
"""
import csv
import datetime
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

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import ollama  # noqa: E402
import requests  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from pypdf import PdfReader  # noqa: E402
from smolagents import LiteLLMModel, tool  # noqa: E402

from utils_visualizacion import (  # noqa: E402, F401
    dibujar_barras,
    dibujar_barras_agrupadas,
    dibujar_mapa_de_calor,
)

RUTA_DATOS = Path(__file__).resolve().parent / "datos"

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


def crear_modelo_local(
    contexto: int = 8192,
    temperatura: float = 0.0,
    semilla: int | None = None,
) -> LiteLLMModel:
    """Conecta smolagents con el modelo local de Ollama.

    Args:
        contexto: Tokens que el modelo puede leer en total (num_ctx).
        temperatura: Cuanto se aparta el modelo de la palabra mas probable.
        semilla: Numero que fija el azar de la generacion, si se pasa.

    Returns:
        Modelo listo para pasarle a un agente.
    """
    opciones = {}
    if semilla is not None:
        opciones["seed"] = semilla
    return LiteLLMModel(
        model_id=f"ollama_chat/{MODELO_LOCAL}",
        api_base=URL_OLLAMA,
        api_key="ollama",
        num_ctx=contexto,
        temperature=temperatura,
        **opciones,
    )


def crear_modelo_gemini() -> LiteLLMModel:
    """Conecta smolagents con Gemini. Necesita GEMINI_API_KEY.

    Returns:
        Modelo listo para pasarle a un agente.
    """
    return LiteLLMModel(
        model_id=f"gemini/{MODELO_GEMINI}",
        api_key=os.getenv("GEMINI_API_KEY"),
    )


def cargar_parcelas() -> list[dict]:
    """Lee las mediciones de las parcelas de datos/parcelas.csv.

    Returns:
        Un diccionario por parcela, con numeros ya convertidos.
    """
    filas = []
    with open(RUTA_DATOS / "parcelas.csv", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            filas.append({
                "parcela": fila["parcela"],
                "temperatura_c": float(fila["temperatura_c"]),
                "humedad_pct": float(fila["humedad_pct"]),
                "lluvia_mm": float(fila["lluvia_mm"]),
                "estado_cultivo": fila["estado_cultivo"],
            })
    return filas


_BUSCADOR = {}


def _preparar_buscador() -> None:
    """Carga el modelo de embeddings y los fragmentos de las politicas."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from sentence_transformers import SentenceTransformer

    textos = []
    fuentes = []
    lector = PdfReader(str(RUTA_DATOS / "politica_interna_tintas_acme.pdf"))
    numero_de_pagina = 0
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=80
    )
    for pagina in lector.pages:
        numero_de_pagina += 1
        for trozo in divisor.split_text(pagina.extract_text() or ""):
            textos.append(trozo)
            fuentes.append(
                f"politica_interna_tintas_acme.pdf, pagina {numero_de_pagina}"
            )
    markdown = (RUTA_DATOS / "politica_trabajo_remoto_tintas_acme.md")
    for trozo in divisor.split_text(markdown.read_text(encoding="utf-8")):
        textos.append(trozo)
        fuentes.append("politica_trabajo_remoto_tintas_acme.md")
    modelo = SentenceTransformer(MODELO_EMBEDDINGS)
    pasajes = []
    for texto in textos:
        pasajes.append("passage: " + texto)
    _BUSCADOR["modelo"] = modelo
    _BUSCADOR["textos"] = textos
    _BUSCADOR["fuentes"] = fuentes
    _BUSCADOR["matriz"] = modelo.encode(
        pasajes, normalize_embeddings=True
    )


def buscar_en_politicas(consulta: str, cantidad: int = 3) -> list[dict]:
    """Busca los fragmentos de las politicas de Acme mas cercanos.

    Es la version resumida del recorrido de la unidad 014: embeddings
    multilingual-e5-small con prefijos y orden por similitud coseno.

    Args:
        consulta: Texto de la consulta.
        cantidad: Cuantos fragmentos devolver.

    Returns:
        Lista de diccionarios con "fuente" y "texto".
    """
    if not _BUSCADOR:
        _preparar_buscador()
    vector = _BUSCADOR["modelo"].encode(
        "query: " + consulta, normalize_embeddings=True
    )
    similitudes = _BUSCADOR["matriz"] @ vector
    orden = np.argsort(-similitudes)[:cantidad]
    resultados = []
    for posicion in orden:
        resultados.append({
            "fuente": _BUSCADOR["fuentes"][posicion],
            "texto": _BUSCADOR["textos"][posicion],
        })
    return resultados


def resolver_con_herramientas(pregunta: str, herramientas: list) -> dict:
    """Responde una pregunta dejando que el modelo pida herramientas.

    Es la version completa de la funcion que se escribe en el cuaderno 01.
    Hace una sola ronda: el modelo pide, el programa ejecuta y el modelo
    redacta la respuesta final.

    Args:
        pregunta: Pregunta de la persona.
        herramientas: Funciones de Python con descripcion (docstring).

    Returns:
        Diccionario con "respuesta" (texto final), "historial" (todos los
        mensajes) y "llamadas" (nombre y argumentos de cada pedido).
    """
    disponibles = {}
    for funcion in herramientas:
        disponibles[funcion.__name__] = funcion
    historial = [{"role": "user", "content": pregunta}]
    primera = ollama.chat(
        model=MODELO_LOCAL,
        messages=historial,
        tools=herramientas,
        options={"temperature": 0},
    )
    historial.append(primera.message)
    llamadas = []
    for pedido in primera.message.tool_calls or []:
        nombre = pedido.function.name
        argumentos = dict(pedido.function.arguments)
        llamadas.append({"herramienta": nombre, "argumentos": argumentos})
        resultado = disponibles[nombre](**argumentos)
        historial.append({
            "role": "tool",
            "content": str(resultado),
            "tool_name": nombre,
        })
    if not llamadas:
        return {
            "respuesta": primera.message.content,
            "historial": historial,
            "llamadas": llamadas,
        }
    final = ollama.chat(
        model=MODELO_LOCAL,
        messages=historial,
        tools=herramientas,
        options={"temperature": 0},
    )
    return {
        "respuesta": final.message.content,
        "historial": historial,
        "llamadas": llamadas,
    }


def resumir_pasos(agente) -> list[dict]:
    """Resume los pasos de accion que dio un agente.

    Es la version completa de la funcion del cuaderno 02.

    Args:
        agente: Agente de smolagents que ya ejecuto una tarea.

    Returns:
        Una fila por paso, con el numero, lo que escribio el modelo, lo
        que volvio de ejecutarlo y si hubo un error.
    """
    filas = []
    for paso in agente.memory.steps:
        if type(paso).__name__ == "ActionStep":
            escrito = " ".join((paso.model_output or "").split())
            devuelto = " ".join((paso.observations or "").split())
            filas.append({
                "paso": paso.step_number,
                "escribio el modelo": escrito[:70],
                "volvio": devuelto[:70],
                "error": paso.error is not None,
            })
    return filas


def comparar_con_la_regla(
    del_agente: list[str], correctas: list[str]
) -> dict:
    """Compara las parcelas que dijo el agente con las de la regla.

    Es la version completa de la funcion del cuaderno 03.

    Args:
        del_agente: Letras de parcela que devolvio el agente.
        correctas: Letras que da la regla calculada con codigo comun.

    Returns:
        Diccionario con "faltan" (las que la regla marca y el agente no),
        "sobran" (las que el agente marca y la regla no) y "coincide".
    """
    faltan = []
    for letra in correctas:
        if letra not in del_agente:
            faltan.append(letra)
    sobran = []
    for letra in del_agente:
        if letra not in correctas:
            sobran.append(letra)
    return {
        "faltan": sorted(faltan),
        "sobran": sorted(sobran),
        "coincide": len(faltan) == 0 and len(sobran) == 0,
    }


def guardar_si_se_aprueba(
    informe: str,
    del_agente: list[str],
    correctas: list[str],
    decision: str,
    nombre: str,
) -> str:
    """Guarda un informe solo si una persona lo aprobo y coincide.

    Es la version completa de la funcion del cuaderno 03.

    Args:
        informe: Texto del informe.
        del_agente: Letras de parcela que dijo el agente.
        correctas: Letras que da la regla calculada con codigo comun.
        decision: "aprobar" o cualquier otra palabra.
        nombre: Nombre del archivo, dentro de la carpeta salida.

    Returns:
        Un mensaje que dice si se guardo y por que.
    """
    comparacion = comparar_con_la_regla(del_agente, correctas)
    if decision != "aprobar":
        return "no se guardo: falta la aprobacion de una persona"
    if not comparacion["coincide"]:
        return "no se guardo: las parcelas no coinciden con la regla"
    carpeta = Path("salida")
    carpeta.mkdir(exist_ok=True)
    (carpeta / nombre).write_text(informe, encoding="utf-8")
    return f"guardado en salida/{nombre}"


@tool
def fecha_limite(fecha_de_inicio: str, dias_corridos: int) -> str:
    """Calcula la ultima fecha para presentar una solicitud.

    Es la version completa de la funcion del cuaderno 04, ya convertida
    en herramienta.

    Args:
        fecha_de_inicio: Fecha de inicio prevista, en formato AAAA-MM-DD
            (por ejemplo 2027-03-01).
        dias_corridos: Dias corridos de anticipacion que exige la
            politica; son dias de calendario, sin descontar fines de
            semana.

    Returns:
        La fecha limite, en formato AAAA-MM-DD.
    """
    inicio = datetime.date.fromisoformat(fecha_de_inicio)
    limite = inicio - datetime.timedelta(days=dias_corridos)
    return limite.isoformat()
