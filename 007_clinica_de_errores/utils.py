"""Apoyos de gráficos para el cuaderno 01_clinica.ipynb.

Acá vive solo lo accesorio (colores, estilo, dibujo). Nada de este archivo cambia qué
entra al análisis ni cómo se interpreta: los conteos, las fórmulas y los parámetros
analíticos están a la vista en el cuaderno.
"""

import matplotlib.pyplot as plt
import numpy as np

from utils_visualizacion import (
    AZUL,
    FONDO,
    LINEA,
    NARANJA,
    TINTA,
    TINTA_SUAVE,
    dibujar_barras_agrupadas,
)

# Un color por grupo, el mismo en todos los gráficos del cuaderno.
COLOR_ADULTO = AZUL
COLOR_INFANTIL = NARANJA
COLORES_POR_GRUPO = {"adulto": COLOR_ADULTO, "infantil": COLOR_INFANTIL}
NOMBRES_DE_GRUPO = {
    "adulto": "Volumen adulto",
    "infantil": "Volumen infantil",
}

SUPERFICIE = FONDO
TINTA_SECUNDARIA = TINTA_SUAVE
GRILLA = LINEA


def aplicar_estilo():
    """Fija un estilo sobrio y legible para todos los gráficos del cuaderno."""
    plt.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "savefig.facecolor": SUPERFICIE,
        "axes.edgecolor": GRILLA,
        "axes.labelcolor": TINTA_SECUNDARIA,
        "axes.titlecolor": TINTA,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TINTA_SECUNDARIA,
        "ytick.color": TINTA_SECUNDARIA,
        "text.color": TINTA,
        "font.size": 10,
        "legend.frameon": False,
    })


def graficar_barras_por_grupo(tabla, titulo, etiqueta_y):
    """Dibuja barras agrupadas: una por palabra y grupo.

    Recibe una tabla con una columna 'palabra' y una columna por grupo
    ('adulto' y 'infantil'). Marca el valor sobre cada barra.
    """
    series = {}
    colores = {}
    for grupo in ["adulto", "infantil"]:
        nombre = NOMBRES_DE_GRUPO[grupo]
        series[nombre] = tabla[grupo].tolist()
        colores[nombre] = COLORES_POR_GRUPO[grupo]

    dibujar_barras_agrupadas(
        categorias=tabla["palabra"].tolist(),
        series=series,
        titulo=titulo,
        colores=colores,
        orientacion="vertical",
        etiqueta_valor=etiqueta_y,
    )


def graficar_puntos_por_cuento(tabla, columnas, titulos, titulo_general, semilla=42):
    """Dibuja un panel por medida: un punto por cuento y una línea con la mediana del grupo.

    Recibe una tabla con una columna 'grupo' y una columna por medida. Los puntos se
    desplazan un poco en horizontal (con una semilla fija) solo para que no se tapen.
    """
    aplicar_estilo()
    generador = np.random.default_rng(semilla)
    figura, paneles = plt.subplots(1, len(columnas), figsize=(4 * len(columnas), 4.2), squeeze=False)
    for numero_de_panel in range(len(columnas)):
        ejes = paneles[0][numero_de_panel]
        columna = columnas[numero_de_panel]
        for posicion_del_grupo in [0, 1]:
            grupo = ["adulto", "infantil"][posicion_del_grupo]
            valores = tabla.loc[tabla["grupo"] == grupo, columna]
            desvio = generador.uniform(-0.12, 0.12, size=len(valores))
            ejes.scatter(
                posicion_del_grupo + desvio,
                valores,
                s=70,
                color=COLORES_POR_GRUPO[grupo],
                edgecolor=SUPERFICIE,
                linewidth=1.5,
                zorder=3,
            )
            mediana = valores.median()
            ejes.hlines(
                mediana,
                posicion_del_grupo - 0.3,
                posicion_del_grupo + 0.3,
                color=TINTA,
                linewidth=2,
                zorder=4,
            )
        ejes.set_xticks([0, 1])
        ejes.set_xticklabels(["Adulto", "Infantil"])
        ejes.set_xlim(-0.6, 1.6)
        ejes.set_title(titulos[numero_de_panel], fontsize=11)
        ejes.grid(axis="x", visible=False)
    figura.suptitle(titulo_general, x=0.01, ha="left", fontsize=12, fontweight="bold")
    figura.text(
        0.01, 0.005,
        "Cada punto es un cuento. La línea negra marca la mediana de cada grupo.",
        fontsize=8.5, color=TINTA_SECUNDARIA,
    )
    figura.tight_layout(rect=(0, 0.03, 1, 0.95))
    plt.show()
