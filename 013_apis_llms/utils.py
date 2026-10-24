"""Utilidades accesorias de la unidad 013: Consumo de modelos por API.

Reune configuracion, comprobaciones, carga de datos y tablas. La logica de
cada llamada a un modelo se escribe en los cuadernos.
"""
import json
import os
import sys
import time
from importlib import metadata
from pathlib import Path

import ollama
import pandas as pd
import requests
from dotenv import load_dotenv

from utils_visualizacion import (  # noqa: F401
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

NANOSEGUNDOS_POR_SEGUNDO = 1_000_000_000

# Las tablas muestran los textos completos, sin cortarlos con puntos.
pd.set_option("display.max_colwidth", None)


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


def cargar_json(nombre: str) -> list[dict]:
    """Lee un JSON de datos/ y devuelve su contenido.

    Args:
        nombre: Nombre del archivo dentro de datos/.

    Returns:
        Lista de diccionarios con el contenido del archivo.
    """
    with open(RUTA_DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_texto(nombre: str) -> str:
    """Lee un archivo de texto de datos/.

    Args:
        nombre: Nombre del archivo dentro de datos/.

    Returns:
        El contenido del archivo como una sola cadena.
    """
    return (RUTA_DATOS / nombre).read_text(encoding="utf-8").strip()


def tabla(filas: list[dict]) -> pd.DataFrame:
    """Convierte una lista de diccionarios en una tabla para mostrar.

    Args:
        filas: Lista de diccionarios con las mismas claves.

    Returns:
        Tabla de pandas con una fila por diccionario.
    """
    return pd.DataFrame(filas)


def modelos_locales() -> list[str]:
    """Pide a Ollama la lista de modelos descargados.

    Returns:
        Nombres de los modelos instalados.

    Raises:
        RuntimeError: Si el servidor de Ollama no responde.
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
    return nombres


def comprobar_modelo_local() -> None:
    """Verifica que Ollama responda y que el modelo de la unidad exista.

    Raises:
        RuntimeError: Si falta el servidor o el modelo.
    """
    nombres = modelos_locales()
    if MODELO_LOCAL not in nombres:
        raise RuntimeError(
            f"Falta el modelo {MODELO_LOCAL}. "
            f"Descargalo con: ollama pull {MODELO_LOCAL}"
        )
    print(f"Ollama responde en {URL_OLLAMA} y tiene {MODELO_LOCAL}.")


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


def preguntar(
    mensajes: list[dict],
    temperatura: float = 0.0,
    maximo_tokens: int | None = None,
    semilla: int | None = None,
    contexto: int | None = None,
) -> dict:
    """Hace una llamada al modelo local y devuelve texto y mediciones.

    Es la version completa de la funcion que se escribe en el cuaderno 01.

    Args:
        mensajes: Lista de mensajes con "role" y "content".
        temperatura: Cuanto se aparta el modelo de la palabra mas probable.
        maximo_tokens: Largo maximo de la respuesta; None no lo limita.
        semilla: Numero que fija el azar de la generacion; None no lo fija.
        contexto: Tokens que el modelo puede leer en total (num_ctx); None
            usa el valor por defecto de Ollama.

    Returns:
        Diccionario con texto, segundos, segundos_carga, tokens_entrada
        y tokens_salida.
    """
    opciones = {"temperature": temperatura}
    if contexto is not None:
        opciones["num_ctx"] = contexto
    if maximo_tokens is not None:
        opciones["num_predict"] = maximo_tokens
    if semilla is not None:
        opciones["seed"] = semilla
    respuesta = ollama.chat(
        model=MODELO_LOCAL,
        messages=mensajes,
        options=opciones,
    )
    return {
        "texto": respuesta.message.content.strip(),
        "segundos": respuesta.total_duration / NANOSEGUNDOS_POR_SEGUNDO,
        "segundos_carga": respuesta.load_duration / NANOSEGUNDOS_POR_SEGUNDO,
        "tokens_entrada": respuesta.prompt_eval_count or 0,
        "tokens_salida": respuesta.eval_count,
    }


def preguntar_a_gemini(sistema: str, consulta: str) -> dict:
    """Hace una llamada a Gemini y devuelve texto y mediciones.

    Es la version completa de la funcion del cuaderno 01. Necesita la
    variable GEMINI_API_KEY.

    Args:
        sistema: Instruccion fija, equivalente al rol system.
        consulta: Pedido concreto, equivalente al rol user.

    Returns:
        Diccionario con texto, segundos, tokens_entrada y tokens_salida.
        Si la llamada falla, el texto describe el error.
    """
    from google import genai
    from google.genai import types

    cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    inicio = time.perf_counter()
    try:
        respuesta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=consulta,
            config=types.GenerateContentConfig(
                system_instruction=sistema,
                temperature=0.0,
            ),
        )
    except genai.errors.APIError as error:
        return {
            "texto": f"Error de la API: {error}",
            "segundos": 0.0,
            "tokens_entrada": 0,
            "tokens_salida": 0,
        }
    uso = respuesta.usage_metadata
    return {
        "texto": (respuesta.text or "").strip(),
        "segundos": time.perf_counter() - inicio,
        "tokens_entrada": uso.prompt_token_count or 0,
        "tokens_salida": uso.candidates_token_count or 0,
    }


REGLA_DE_DOCUMENTO = (
    "Sos un asistente de la biblioteca. Respondé solo con la información "
    "del documento. Si la respuesta no figura en el documento, respondé "
    "exactamente: No figura en el documento."
)


def responder_con_documento(
    documento: str,
    pregunta: str,
    contexto: int | None = None,
    maximo_tokens: int | None = None,
) -> dict:
    """Responde una pregunta usando solo el texto de un documento.

    Es la version completa de la funcion que se escribe en el cuaderno 04.

    Args:
        documento: Texto que se pega en el pedido.
        pregunta: Pregunta de la persona.
        contexto: Tokens que el modelo puede leer en total (num_ctx).
        maximo_tokens: Largo maximo de la respuesta.

    Returns:
        El diccionario que devuelve preguntar.
    """
    mensajes = [
        {"role": "system", "content": REGLA_DE_DOCUMENTO},
        {
            "role": "user",
            "content": f"Documento:\n{documento}\n\nPregunta: {pregunta}",
        },
    ]
    return preguntar(
        mensajes, contexto=contexto, maximo_tokens=maximo_tokens
    )
