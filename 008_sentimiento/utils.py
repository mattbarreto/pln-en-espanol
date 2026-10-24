# -*- coding: utf-8 -*-
"""Apoyos visuales del encuentro 8: sentimiento en español.

Los gráficos generales delegan el dibujo a utils_visualizacion.py. Este
archivo conserva adaptaciones propias del análisis de sentimiento, como el
recuento de la matriz de confusión. Los cuadernos lo importan con:

    from utils import ETIQUETAS, dibujar_matriz_de_confusión

Colores (validados con la skill de visualización, sobre fondo claro):
    POS azul · NEG naranja · NEU gris.
El color nunca es el único canal: siempre hay un rótulo con la clase o el signo.
"""
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.metrics import confusion_matrix

from utils_visualizacion import (
    AZUL,
    FONDO,
    GRIS,
    LINEA,
    NARANJA,
    TINTA,
    TINTA_SUAVE,
    TINTAS as TINTAS_POR_COLOR,
    VIOLETA,
    dibujar_barras as _dibujar_barras_compartidas,
    dibujar_fichas as _dibujar_fichas_compartidas,
    dibujar_mapa_de_calor as _dibujar_mapa_compartido,
)

ETIQUETAS = ["NEG", "NEU", "POS"]
NOMBRES = {"NEG": "Negativo", "NEU": "Neutro", "POS": "Positivo"}
COLORES = {"NEG": NARANJA, "NEU": GRIS, "POS": AZUL}
COLOR_GENERAL = VIOLETA
TINTAS = {
    "NEG": TINTAS_POR_COLOR[NARANJA],
    "NEU": TINTAS_POR_COLOR[GRIS],
    "POS": TINTAS_POR_COLOR[AZUL],
}

ESTILO = {
    "figure.dpi": 110,
    "figure.facecolor": FONDO,
    "axes.facecolor": FONDO,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": LINEA,
    "axes.labelcolor": TINTA_SUAVE,
    "xtick.color": TINTA_SUAVE,
    "ytick.color": TINTA_SUAVE,
    "text.color": TINTA,
    "font.size": 10,
    "axes.titlelocation": "left",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
}


def _acortar(texto, ancho=64):
    """Recorta un texto largo para que quepa como rótulo de un eje."""
    return textwrap.shorten(texto, width=ancho, placeholder="…")


def _signo(valor):
    """Escribe un numero con su signo: +1, -2 o 0."""
    if valor > 0:
        return f"+{valor:g}"
    if valor < 0:
        return f"-{abs(valor):g}"
    return "0"


def dibujar_tokens_con_valor(tabla, columna_valor="valor", título=""):
    """Dibuja una oración como una fila de fichas, una por token.

    Recibe una tabla con una columna 'token' y una columna numérica.
    Azul suma, naranja resta, gris no aporta. Debajo de cada ficha con
    valor distinto de cero se escribe el número con su signo.
    """
    piezas = tabla["token"].tolist()
    clases = []
    notas = []
    for valor in tabla[columna_valor]:
        if valor > 0:
            clases.append("POS")
        elif valor < 0:
            clases.append("NEG")
        else:
            clases.append("NEU")
        notas.append(_signo(valor) if valor != 0 else "")

    estilos = {
        "POS": (COLORES["POS"], "Azul", "suma"),
        "NEG": (COLORES["NEG"], "Naranja", "resta"),
        "NEU": (COLORES["NEU"], "Gris", "sin valor en el lexico"),
    }
    _dibujar_fichas_compartidas(
        piezas=piezas,
        clases=clases,
        estilos=estilos,
        titulo=título,
        notas=notas,
        por_fila=64,
    )


def dibujar_barras(tabla, columna_nombre, columna_valor, título="", color=None):
    """Dibuja barras horizontales con el valor escrito al final de cada una.

    Si 'color' es None, las barras positivas van en azul y las negativas
    en naranja. Si se indica un color, todas las barras lo usan.
    """
    datos = tabla.sort_values(columna_valor, ascending=True)
    nombres = datos[columna_nombre].tolist()
    valores = datos[columna_valor].tolist()
    colores = []
    for valor in valores:
        if color is not None:
            colores.append(color)
        elif valor >= 0:
            colores.append(COLORES["POS"])
        else:
            colores.append(COLORES["NEG"])

    _dibujar_barras_compartidas(
        nombres=nombres,
        valores=valores,
        titulo=título,
        colores=colores,
        formato="{:.2f}",
    )


def dibujar_matriz_de_confusión(referencia, predicción, título="",
                                nombre_filas="Referencia (protocolo)",
                                nombre_columnas="Predicción del método"):
    """Dibuja la matriz de confusión como un mapa de calor con los conteos.

    Las filas son lo que dice el protocolo (referencia) y las columnas lo
    que respondió el método (predicción). La diagonal son los aciertos.
    Los nombres de los ejes se pueden cambiar si se comparan otras dos cosas.
    """
    conteos = confusion_matrix(y_true=referencia, y_pred=predicción, labels=ETIQUETAS)
    nombres = [NOMBRES[clase] for clase in ETIQUETAS]
    _dibujar_mapa_compartido(
        matriz=conteos,
        filas=nombres,
        columnas=nombres,
        titulo=título,
        formato="{:g}",
        color=COLORES["POS"],
        etiqueta_filas=nombre_filas,
        etiqueta_columnas=nombre_columnas,
    )


def dibujar_coeficientes(tablas_por_clase, columna_nombre="característica",
                         columna_valor="coeficiente"):
    """Dibuja, lado a lado, las palabras más asociadas a cada clase.

    Recibe un diccionario {"NEG": tabla, "NEU": tabla, "POS": tabla}. Cada
    tabla ya viene ordenada y recortada a las palabras que se quieren mostrar.
    """
    with plt.rc_context(ESTILO):
        figura, ejes_por_clase = plt.subplots(1, 3, figsize=(11, 3.4), sharex=True)
        for ejes, clase in zip(ejes_por_clase, ETIQUETAS):
            datos = tablas_por_clase[clase].iloc[::-1]
            ejes.barh(datos[columna_nombre], datos[columna_valor],
                      color=COLORES[clase], height=0.62)
            for posición, valor in enumerate(datos[columna_valor]):
                ejes.text(valor + 0.005, posición, f"{valor:.2f}",
                          va="center", fontsize=8.5, color=TINTA_SUAVE)
            ejes.set_title(NOMBRES[clase])
            ejes.spines["left"].set_visible(False)
            ejes.tick_params(axis="y", length=0)
        figura.tight_layout()
        plt.show()


def dibujar_probabilidades(tabla, columna_texto="texto", título=""):
    """Dibuja, para cada texto, cómo reparte el modelo su 100 % entre clases.

    Recibe una tabla con las columnas prob_NEG, prob_NEU y prob_POS. Cada
    barra suma 100 %. Se escribe el porcentaje en los tramos de 12 % o más.
    """
    textos = [_acortar(texto) for texto in tabla[columna_texto]]
    cantidad = len(textos)

    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(9, 0.42 * cantidad + 1.3))
        inicio = [0.0] * cantidad
        for clase in ETIQUETAS:
            largos = tabla[f"prob_{clase}"].tolist()
            ejes.barh(range(cantidad), largos, left=inicio, color=COLORES[clase],
                      edgecolor=FONDO, linewidth=1.5, height=0.7)
            tinta = "#ffffff" if clase == "POS" else TINTA
            for posición, largo in enumerate(largos):
                if largo >= 0.12:
                    ejes.text(inicio[posición] + largo / 2, posición, f"{largo:.0%}",
                              ha="center", va="center", fontsize=8.5, color=tinta)
            inicio = [a + b for a, b in zip(inicio, largos)]
        ejes.set_yticks(range(cantidad), textos)
        ejes.invert_yaxis()
        ejes.set_xlim(0, 1)
        ejes.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0 %", "25 %", "50 %", "75 %", "100 %"])
        ejes.spines["left"].set_visible(False)
        ejes.tick_params(axis="y", length=0)
        ejes.legend(
            handles=[Patch(facecolor=COLORES[c], label=NOMBRES[c]) for c in ETIQUETAS],
            ncol=3, loc="lower left", bbox_to_anchor=(0, 1.0), frameon=False,
        )
        if título:
            figura.suptitle(título, x=0.02, ha="left", fontsize=11, fontweight="bold", y=1.1)
        plt.show()
