"""Comprobaciones, carga del modelo y funciones visuales de la unidad 011.

Las funciones de dibujo viven en utils_visualizacion.py y se reexportan
aca: en los cuadernos se llaman como utils.dibujar_...

El codigo va en ASCII.
"""

import numpy as np
import torch

from utils_visualizacion import (  # noqa: F401
    AZUL,
    ESTILO,
    FONDO,
    GRAMATICA,
    GRIS,
    LINEA,
    NARANJA,
    TINTA,
    TINTA_SUAVE,
    VERDE_AZULADO,
    VIOLETA,
    armar_panel_interactivo,
    dibujar_barras,
    dibujar_barras_agrupadas,
    dibujar_bloque_transformer,
    dibujar_dispersion,
    dibujar_fichas,
    dibujar_mapa_de_calor,
    dibujar_mapa_del_modelo,
    dibujar_mapas_lado_a_lado,
    dibujar_paneles,
)

MODELO_GPT2 = "DeepESP/gpt2-spanish"


def comprobar(condicion: bool, pista: str) -> None:
    """Informa si una comprobacion de microlaboratorio es correcta.

    Args:
        condicion: Resultado de la comprobacion.
        pista: Orientacion para revisar si la condicion no se cumple.
    """
    if condicion:
        print("Correcto.")
    else:
        print(f"Todavia no. {pista}")


def softmax(puntajes: np.ndarray) -> np.ndarray:
    """Convierte puntajes en pesos positivos que suman uno por fila.

    Es la softmax del cuaderno 02, aplicada a todas las filas a la vez.

    Args:
        puntajes: Vector, o matriz con un vector de puntajes por fila.

    Returns:
        Pesos con la misma forma, normalizados sobre el ultimo eje.
    """
    estables = puntajes - puntajes.max(axis=-1, keepdims=True)
    exponenciales = np.exp(estables)
    return exponenciales / exponenciales.sum(axis=-1, keepdims=True)


def normalizar_como_gpt2(
    vectores: np.ndarray, capa: torch.nn.Module,
) -> np.ndarray:
    """Normaliza cada fila como lo hace GPT-2 (cuaderno 03, seccion 3).

    Resta la media y divide por el desvio de cada fila; despues multiplica
    por la ganancia y suma el sesgo que la capa aprendio.

    Args:
        vectores: Un vector por fila.
        capa: Capa de normalizacion del modelo, como bloque.ln_1.

    Returns:
        Los vectores normalizados, con la misma forma.
    """
    ganancia = capa.weight.detach().numpy()
    sesgo = capa.bias.detach().numpy()
    medias = vectores.mean(axis=1, keepdims=True)
    desvios = np.sqrt(vectores.var(axis=1, keepdims=True) + capa.eps)
    centrados = (vectores - medias) / desvios
    return centrados * ganancia + sesgo


def gelu_como_gpt2(valores: np.ndarray) -> np.ndarray:
    """Aplica el filtro GELU con la formula que usa GPT-2.

    Deja casi igual lo positivo y achica mucho lo negativo (cuaderno 01).

    Args:
        valores: Numeros de cualquier forma.

    Returns:
        Los valores filtrados, con la misma forma.
    """
    interior = np.sqrt(2.0 / np.pi) * (valores + 0.044715 * valores ** 3)
    return 0.5 * valores * (1.0 + np.tanh(interior))


def cargar_gpt2(nombre: str = MODELO_GPT2) -> tuple:
    """Carga el tokenizador y el modelo GPT-2 en espanol, listos para leer.

    La primera vez descarga unos 250 MB; despues usa la copia guardada en
    la computadora (ver ANTES_DE_LA_CLASE.md).

    Args:
        nombre: Nombre del modelo en Hugging Face.

    Returns:
        El tokenizador y el modelo, en modo evaluacion.
    """
    from transformers import AutoTokenizer, GPT2LMHeadModel
    from transformers.utils import logging as registro

    registro.set_verbosity_error()
    tokenizador = AutoTokenizer.from_pretrained(nombre)
    # "eager" calcula la atencion paso a paso y permite pedir sus pesos.
    modelo = GPT2LMHeadModel.from_pretrained(
        nombre, attn_implementation="eager",
    )
    modelo.eval()
    return tokenizador, modelo
