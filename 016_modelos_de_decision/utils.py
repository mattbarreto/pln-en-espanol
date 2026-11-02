"""Utilidades accesorias de la unidad 016: Modelos de decision.

Reune las comprobaciones, la descarga de Julia-1 en una revision fija, la
consulta a Ollama y las tablas y graficos de probabilidades. Lo que el
cuaderno estudia (las preguntas, el mecanismo, la confianza y la decision)
esta escrito en el cuaderno.
"""
import os
import sys
from importlib import metadata
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from huggingface_hub import snapshot_download

from utils_visualizacion import dibujar_barras

RUTA_UNIDAD = Path(__file__).resolve().parent

# Julia-1 se descarga en una revision fija: si el repositorio cambia, el
# cuaderno sigue usando el mismo codigo y los mismos pesos.
REPO_JULIA = "SupersonicLabs/Julia-1"
REVISION_JULIA = "a85b127321d580d65176c89ced8273f305745d85"
RUTA_JULIA = RUTA_UNIDAD / "modelo" / "Julia-1"

# El modelo de Ollama se puede cambiar desde el archivo .env, si existe.
load_dotenv()
URL_OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODELO_LOCAL = os.getenv("OLLAMA_MODEL", "granite4:latest")

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


def preparar_julia() -> Path:
    """Descarga Julia-1 (una sola vez) y deja importable su paquete.

    La primera vez baja unos 590 MB; despues usa la copia de la carpeta
    modelo/. El paquete julia/ viene dentro del repositorio del modelo:
    se agrega a la ruta de Python en lugar de instalarlo con pip.

    Returns:
        Ruta de la carpeta del modelo.
    """
    ruta = snapshot_download(
        repo_id=REPO_JULIA,
        revision=REVISION_JULIA,
        local_dir=str(RUTA_JULIA),
    )
    ruta = Path(ruta).resolve()
    if not (ruta / "julia" / "__init__.py").exists():
        raise RuntimeError(
            f"La descarga en {ruta} no tiene el paquete julia/. "
            "Borra la carpeta modelo/ y volve a ejecutar la celda."
        )
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))
    return ruta


def ollama_disponible() -> bool:
    """Dice si Ollama responde y tiene el modelo de la unidad.

    Returns:
        True si se puede usar el modelo local; False si no, con un aviso.
    """
    try:
        respuesta = requests.get(f"{URL_OLLAMA}/api/tags", timeout=5)
        respuesta.raise_for_status()
    except requests.RequestException:
        print(f"Ollama no responde en {URL_OLLAMA}: se saltea la seccion.")
        return False
    nombres = []
    for modelo in respuesta.json()["models"]:
        nombres.append(modelo["name"])
    if MODELO_LOCAL not in nombres:
        print(f"Falta {MODELO_LOCAL} (ollama pull {MODELO_LOCAL}).")
        return False
    print(f"Ollama responde y tiene {MODELO_LOCAL}.")
    return True


def tabla_de_probabilidades(respuesta: dict) -> pd.DataFrame:
    """Ordena las probabilidades de una respuesta de mayor a menor.

    Args:
        respuesta: Una respuesta de Julia con la clave "probabilities".

    Returns:
        Tabla con una fila por opcion.
    """
    filas = []
    for opcion, probabilidad in respuesta["probabilities"].items():
        filas.append({"opcion": opcion, "probabilidad": probabilidad})
    tabla = pd.DataFrame(filas)
    tabla = tabla.sort_values("probabilidad", ascending=False)
    return tabla.reset_index(drop=True).round(4)


def dibujar_probabilidades(respuesta: dict, titulo: str = "") -> None:
    """Dibuja las probabilidades de una respuesta, en el orden de la pregunta.

    Args:
        respuesta: Una respuesta de Julia con la clave "probabilities".
        titulo: Titulo del grafico.
    """
    opciones = list(respuesta["probabilities"].keys())
    valores = list(respuesta["probabilities"].values())
    dibujar_barras(opciones, valores, titulo=titulo, formato="{:.3f}")
