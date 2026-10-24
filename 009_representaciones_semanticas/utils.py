"""Apoyos de la unidad 009: representaciones semanticas.

Este archivo reune solo lo que se repite en varios cuadernos: donde estan los
datos y los vectores, el coseno, el promedio de vectores, el ranking y las
metricas de recuperacion. Las operaciones que cada cuaderno ensena (ventanas,
PPMI, entrenamiento, comparaciones) se escriben en el propio cuaderno.

El codigo esta escrito sin tildes ni enies para evitar problemas de
codificacion. Las letras con tilde se escriben con su codigo (por ejemplo,
\\u00e1 es la a con tilde).

Las funciones dibujar_* son accesorias: dibujan, no calculan. Ninguna cambia
un resultado ni una decision del analisis; solo muestran lo que el cuaderno
ya calculo. Comparten la paleta de la unidad 008. El color nunca es el unico
canal: siempre hay un rotulo, un numero o una forma.
"""

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from utils_visualizacion import (
    AZUL,
    COLORES_DE_GRUPO,
    COLOR_POR_METODO,
    ESTILO,
    FONDO,
    FORMAS_DE_GRUPO,
    GRIS,
    LINEA,
    NARANJA,
    TINTA,
    TINTA_SUAVE,
    TINTAS,
    VERDE_AZULADO,
    VIOLETA,
    dibujar_barras,
    dibujar_barras_agrupadas,
    dibujar_dispersion,
    dibujar_fichas,
    dibujar_mapa_de_calor,
)

CARPETA_DE_LA_UNIDAD = Path(__file__).resolve().parent
CARPETA_DE_DATOS = CARPETA_DE_LA_UNIDAD / "datos"

# Los vectores preentrenados pesan varios GB y no se suben al repositorio.
# Por defecto se buscan en datos/vectors/. Con la variable de entorno
# LAB_VECTORES se puede apuntar a otra carpeta sin tocar los cuadernos.
CARPETA_DE_VECTORES = Path(
    os.environ.get("LAB_VECTORES", CARPETA_DE_DATOS / "vectors")
)
NOMBRE_VECTORES_WORD2VEC = "SBW-vectors-300-min5.bin.gz"
NOMBRE_VECTORES_FASTTEXT = "wiki.es.bin"

# Una palabra es una secuencia de letras: a-z, vocales con tilde, u con
# dieresis y enie (escritas con su codigo para que el archivo sea ASCII).
PATRON_DE_PALABRA = r"[a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00fc\u00f1]+"


# --- Datos ------------------------------------------------------------------

def cargar_fragmentos() -> pd.DataFrame:
    """Lee la tabla de fragmentos.

    Returns:
        Tabla con las columnas id, texto, autor, titulo, fuente y palabras.
    """
    return pd.read_csv(CARPETA_DE_DATOS / "fragmentos.csv")


def cargar_consultas() -> pd.DataFrame:
    """Lee la tabla de consultas.

    Returns:
        Tabla con las columnas id, consulta, tipo y criterio_de_relevancia.
    """
    return pd.read_csv(CARPETA_DE_DATOS / "consultas.csv")


def cargar_juicios() -> pd.DataFrame:
    """Lee los juicios de relevancia.

    Lo que no figura en la tabla se considera no relevante (0).

    Returns:
        Tabla con las columnas id_consulta, id_fragmento, relevancia (1 o 2),
        justificacion y discutible.
    """
    ruta = CARPETA_DE_DATOS / "juicios_de_relevancia.csv"
    return pd.read_csv(ruta, keep_default_na=False)


# --- Texto ------------------------------------------------------------------

def separar_palabras(texto: str) -> list:
    """Pasa el texto a minusculas y lo separa en palabras.

    Una palabra es una secuencia de letras (con tildes y enies). Se descartan
    numeros y signos. Es la misma regla para todos los metodos de la unidad.

    Args:
        texto: El texto a separar.

    Returns:
        Lista de palabras en minuscula.
    """
    return re.findall(PATRON_DE_PALABRA, texto.lower())


# --- Vectores ---------------------------------------------------------------

def coseno(vector_a, vector_b) -> float:
    """Calcula el coseno entre dos vectores. Va de -1 a 1.

    Si alguno de los dos es nulo (todo ceros) o falta, el angulo no esta
    definido: devuelve nan en lugar de inventar un valor.

    Args:
        vector_a: Primer vector (arreglo de numpy) o None.
        vector_b: Segundo vector (arreglo de numpy) o None.

    Returns:
        El coseno, o nan si no esta definido.
    """
    if vector_a is None or vector_b is None:
        return float("nan")
    norma_a = np.linalg.norm(vector_a)
    norma_b = np.linalg.norm(vector_b)
    if norma_a == 0 or norma_b == 0:
        return float("nan")
    producto = np.dot(vector_a, vector_b)
    return float(producto / (norma_a * norma_b))


def cosenos_contra_todas_las_filas(matriz, vector) -> np.ndarray:
    """Calcula el coseno entre un vector y cada fila de una matriz.

    Args:
        matriz: Matriz densa o esparsa, con una fila por elemento.
        vector: Vector con tantas columnas como la matriz.

    Returns:
        Arreglo con un valor por fila. Las filas nulas dan nan.
    """
    if hasattr(matriz, "toarray"):
        matriz = matriz.toarray()
    matriz = np.asarray(matriz, dtype=float)
    vector = np.asarray(vector, dtype=float).ravel()
    normas_de_filas = np.linalg.norm(matriz, axis=1)
    norma_del_vector = np.linalg.norm(vector)
    productos = matriz @ vector
    cosenos = np.full(len(matriz), np.nan)
    hay_dato = (normas_de_filas > 0) & (norma_del_vector > 0)
    divisor = normas_de_filas[hay_dato] * norma_del_vector
    cosenos[hay_dato] = productos[hay_dato] / divisor
    return cosenos


def promedio_de_vectores(palabras: list, vectores) -> tuple:
    """Promedia los vectores de las palabras que el modelo conoce.

    "Conocer" significa estar en el vocabulario explicito (key_to_index). Con
    fastText eso es distinto de poder fabricar un vector con subpalabras.

    Args:
        palabras: Lista de palabras.
        vectores: Modelo con vectores (gensim KeyedVectors).

    Returns:
        Una tupla (promedio, sin_cobertura). El promedio es None si ninguna
        palabra tiene vector. sin_cobertura es la lista de palabras que no
        estan en el vocabulario.
    """
    vectores_hallados = []
    palabras_sin_cobertura = []
    for palabra in palabras:
        if palabra in vectores.key_to_index:
            vectores_hallados.append(vectores[palabra])
        else:
            palabras_sin_cobertura.append(palabra)
    if len(vectores_hallados) == 0:
        return None, palabras_sin_cobertura
    promedio = np.mean(vectores_hallados, axis=0)
    return promedio, palabras_sin_cobertura


def cargar_vectores_word2vec(limite: int = None):
    """Carga los vectores Word2Vec en espanol (SBW, 300 dimensiones).

    Args:
        limite: Si se indica, carga solo las primeras palabras del archivo
            (estan ordenadas por frecuencia). Sirve para probar rapido con
            poca memoria.

    Returns:
        Un KeyedVectors de gensim.

    Raises:
        FileNotFoundError: Si el archivo no esta en la carpeta de vectores.
    """
    from gensim.models import KeyedVectors

    ruta = CARPETA_DE_VECTORES / NOMBRE_VECTORES_WORD2VEC
    if not ruta.exists():
        raise FileNotFoundError(
            f"No encontramos {ruta}. Ver datos/vectors/README.md."
        )
    return KeyedVectors.load_word2vec_format(
        str(ruta), binary=True, limit=limite
    )


def cargar_vectores_fasttext():
    """Carga solo los vectores fastText en espanol (wiki.es.bin).

    Usa load_facebook_vectors: conserva el vocabulario y los n-gramas de
    caracteres, y no carga las matrices que solo sirven para seguir entrenando.

    Returns:
        Un FastTextKeyedVectors de gensim.

    Raises:
        FileNotFoundError: Si el archivo no esta en la carpeta de vectores.
    """
    from gensim.models.fasttext import load_facebook_vectors

    ruta = CARPETA_DE_VECTORES / NOMBRE_VECTORES_FASTTEXT
    if not ruta.exists():
        raise FileNotFoundError(
            f"No encontramos {ruta}. Ver datos/vectors/README.md."
        )
    return load_facebook_vectors(str(ruta))


# --- Recuperacion -----------------------------------------------------------

def ordenar_por_puntaje(puntajes, indice_a_excluir: int = None) -> np.ndarray:
    """Ordena las posiciones de mayor a menor puntaje.

    Los valores nan van al final (un fragmento sin puntaje no compite). Los
    empates se resuelven por posicion (el primero de la tabla gana), asi el
    resultado no cambia entre ejecuciones.

    Args:
        puntajes: Un puntaje por fragmento.
        indice_a_excluir: Posicion que se saca del ranking. Sirve cuando la
            consulta es uno de los fragmentos de la coleccion.

    Returns:
        Arreglo con las posiciones ordenadas.
    """
    puntajes = np.asarray(puntajes, dtype=float)
    posiciones = np.arange(len(puntajes))
    para_ordenar = np.where(np.isnan(puntajes), -np.inf, puntajes)
    # lexsort ordena por la ultima clave primero: puntaje descendente y,
    # a igual puntaje, posicion ascendente.
    orden = np.lexsort((posiciones, -para_ordenar))
    if indice_a_excluir is not None:
        orden = orden[orden != indice_a_excluir]
    return orden


def relevancias_de_una_consulta(
    id_fragmentos: list, juicios: pd.DataFrame, id_consulta: str
) -> np.ndarray:
    """Arma la relevancia (0, 1 o 2) de cada fragmento para una consulta.

    Args:
        id_fragmentos: Ids de los fragmentos, en el orden de la coleccion.
        juicios: Tabla de juicios (ver cargar_juicios).
        id_consulta: Id de la consulta, por ejemplo "C01".

    Returns:
        Arreglo con un entero por fragmento.
    """
    de_la_consulta = juicios[juicios["id_consulta"] == id_consulta]
    relevancia_por_fragmento = dict(
        zip(de_la_consulta["id_fragmento"], de_la_consulta["relevancia"])
    )
    relevancias = []
    for id_fragmento in id_fragmentos:
        relevancias.append(int(relevancia_por_fragmento.get(id_fragmento, 0)))
    return np.array(relevancias)


def precision_en_k(relevancias_ordenadas, k: int, umbral: int = 1) -> float:
    """Calcula la proporcion de relevantes entre los primeros k resultados.

    Args:
        relevancias_ordenadas: Relevancia de cada resultado, en el orden del
            ranking.
        k: Cuantos resultados se miran.
        umbral: Desde que grado cuenta como relevante: 1 acepta parciales y
            totales; 2 exige solo los totales.

    Returns:
        Un numero entre 0 y 1.

    Raises:
        ValueError: Si k no es positivo.
    """
    if k <= 0:
        raise ValueError("k debe ser positivo")
    primeros = np.asarray(relevancias_ordenadas)[:k]
    return float(np.sum(primeros >= umbral) / k)


def rango_reciproco(relevancias_ordenadas, umbral: int = 1) -> float:
    """Calcula 1 dividido la posicion del primer relevante.

    Args:
        relevancias_ordenadas: Relevancia de cada resultado, en el orden del
            ranking.
        umbral: Desde que grado cuenta como relevante.

    Returns:
        1 si el primero es relevante, 0.5 si es el segundo, y asi; 0 si no
        aparece ninguno.
    """
    posicion = 1
    for relevancia in np.asarray(relevancias_ordenadas):
        if relevancia >= umbral:
            return 1.0 / posicion
        posicion += 1
    return 0.0


def total_de_relevantes(relevancias, umbral: int = 1) -> int:
    """Cuenta los fragmentos de toda la coleccion que son relevantes.

    Args:
        relevancias: Relevancia de cada fragmento para una consulta.
        umbral: Desde que grado cuenta como relevante.

    Returns:
        Cantidad de fragmentos relevantes.
    """
    return int(np.sum(np.asarray(relevancias) >= umbral))


# --- Microlaboratorios ------------------------------------------------------

def comprobar(condicion: bool, pista: str) -> None:
    """Dice si un ejercicio quedo bien.

    Si no quedo bien, muestra la pista y sigue: no corta el cuaderno.

    Args:
        condicion: True si el ejercicio esta resuelto.
        pista: Mensaje que ayuda a encontrar el error.
    """
    if condicion:
        print("Correcto.")
    else:
        print(f"Todavia falta. Pista: {pista}")

