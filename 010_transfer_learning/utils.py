"""Utilidades accesorias de la unidad 010: Transfer learning.

Reune funciones para datos, tablas y comprobaciones, y expone los dibujos
compartidos. La logica de los modelos se escribe en cada cuaderno.
"""
import json
from importlib import metadata
from pathlib import Path

import pandas as pd

from utils_visualizacion import dibujar_barras, dibujar_mapa_de_calor

RUTA_DATOS = Path(__file__).resolve().parent / "datos"

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
        print(f"Todavía no: {pista}")


def cargar_json(nombre: str) -> list[dict]:
    """Lee un JSON de datos/ y devuelve su contenido.

    Args:
        nombre: Nombre del archivo dentro de datos/, por ejemplo
            "clasificacion.json".

    Returns:
        Lista de diccionarios con el contenido del archivo.
    """
    with open(RUTA_DATOS / nombre, encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_texto(nombre: str) -> str:
    """Lee un archivo de texto de datos/.

    Args:
        nombre: Nombre del archivo dentro de datos/, por ejemplo
            "aviso_ner.txt".

    Returns:
        El contenido del archivo como una sola cadena.
    """
    return (RUTA_DATOS / nombre).read_text(encoding="utf-8").strip()


def cargar_versos() -> pd.DataFrame:
    """Lee martin_fierro.csv y devuelve una columna llamada verso.

    Returns:
        Tabla con una fila por verso y una sola columna, verso.
    """
    versos = pd.read_csv(RUTA_DATOS / "martin_fierro.csv")
    versos = versos.rename(columns={"samples": "verso"})
    return versos[["verso"]]


def tabla(filas: list[dict]) -> pd.DataFrame:
    """Convierte una lista de diccionarios en una tabla para mostrar.

    Args:
        filas: Lista de diccionarios con las mismas claves.

    Returns:
        Tabla de pandas con una fila por diccionario.
    """
    return pd.DataFrame(filas)


def mostrar_tokens(tokens: list[str]) -> None:
    """Imprime tokens separados por espacios, sin interpretarlos.

    Args:
        tokens: Lista de tokens tal como los devolvio el tokenizador.

    Returns:
        None. Imprime los tokens en una sola linea.
    """
    print(" ".join(tokens))


def versiones() -> dict[str, str]:
    """Devuelve las versiones de las librerias criticas.

    Returns:
        Diccionario con el nombre de cada libreria y su version.
    """
    resultado = {}
    for nombre in ("torch", "transformers", "scikit-learn", "pandas"):
        resultado[nombre] = metadata.version(nombre)
    return resultado


def resumen_particiones(registros: list[dict]) -> pd.DataFrame:
    """Cuenta ejemplos por particion y etiqueta.

    Args:
        registros: Lista de diccionarios con las claves split y etiqueta.

    Returns:
        Tabla con una fila por etiqueta y una columna por particion.
    """
    filas = pd.DataFrame(registros)
    return pd.crosstab(filas["etiqueta"], filas["split"])


def separar(registros: list[dict], particion: str) -> tuple[list, list]:
    """Separa los textos y las etiquetas de una particion.

    Args:
        registros: Lista de diccionarios con texto, etiqueta y split.
        particion: Nombre de la particion: train, val o test.

    Returns:
        Una lista de textos y una lista de etiquetas, en el mismo orden.
    """
    textos = []
    etiquetas = []
    for registro in registros:
        if registro["split"] == particion:
            textos.append(registro["texto"])
            etiquetas.append(registro["etiqueta"])
    return textos, etiquetas
