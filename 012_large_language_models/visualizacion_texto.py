"""Visualizaciones del cuaderno local de texto a proximo token."""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

AZUL = "#2a78d6"
NARANJA = "#eb6834"
VIOLETA = "#4a3aa7"
GRIS = "#8b8b86"
TINTA = "#0b0b0b"
TINTA_SUAVE = "#52514e"
LINEA = "#c3c2b7"
FONDO = "#ffffff"

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


def comprobar(condicion: bool, pista: str) -> None:
    """Informa el resultado de una comprobacion del cuaderno.

    Args:
        condicion: Resultado esperado de la practica.
        pista: Orientacion si la condicion no se cumple.
    """
    if condicion:
        print("Correcto.")
    else:
        print(f"Todavia no. {pista}")


def dibujar_fichas(
    piezas: Sequence[str],
    titulo: str,
    colores: Sequence[str] | None = None,
    notas: Sequence[str] | None = None,
) -> None:
    """Dibuja tokens o identificadores como fichas.

    Args:
        piezas: Textos de las fichas.
        titulo: Titulo del grafico.
        colores: Un color por ficha.
        notas: Texto opcional debajo de cada ficha.
    """
    colores_finales = list(colores or [AZUL] * len(piezas))
    if len(colores_finales) != len(piezas):
        raise ValueError("colores debe tener una entrada por pieza.")
    por_fila = 8
    cantidad_de_filas = (len(piezas) + por_fila - 1) // por_fila
    columnas = min(len(piezas), por_fila)
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(max(6.5, columnas * 1.1), 1.3 * cantidad_de_filas + 0.9)
        )
        ejes.set_xlim(-0.5, columnas - 0.5)
        ejes.set_ylim(-cantidad_de_filas + 0.4, 0.6)
        ejes.set_axis_off()
        for lugar in range(len(piezas)):
            fila = lugar // por_fila
            columna = lugar % por_fila
            ejes.text(
                columna, -fila, piezas[lugar], ha="center", va="center",
                bbox={"boxstyle": "round,pad=0.35", "fc": FONDO,
                      "ec": colores_finales[lugar], "lw": 2},
            )
            if notas is not None:
                ejes.text(columna, -fila - 0.32, notas[lugar], ha="center",
                           va="center", fontsize=8, color=TINTA_SUAVE)
        ejes.set_title(titulo, pad=12)
        figura.tight_layout()
        plt.show()


def _con_coma(valor: float, posicion: int) -> str:
    """Escribe una marca de eje con coma decimal.

    Args:
        valor: Valor de la marca.
        posicion: Lugar de la marca; matplotlib lo pasa y no se usa.

    Returns:
        El valor como texto, con coma.
    """
    return f"{valor:g}".replace(".", ",")


def dibujar_barras(
    nombres: Sequence[str],
    valores: Sequence[float],
    titulo: str,
    color: str = NARANJA,
) -> None:
    """Dibuja barras con el valor escrito.

    Args:
        nombres: Rotulos de las barras.
        valores: Valores ya calculados.
        titulo: Titulo del grafico.
        color: Color de las barras.
    """
    datos = np.asarray(valores, dtype=float)
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(7, len(nombres) * 0.42 + 1.1))
        posiciones = list(range(len(nombres)))
        ejes.barh(posiciones, datos, color=color)
        ejes.set_yticks(posiciones, nombres)
        ejes.invert_yaxis()
        maximo = float(datos.max()) or 1.0
        decimales = 3 if maximo < 0.1 else 2
        for lugar in posiciones:
            escrito = f"{datos[lugar]:.{decimales}f}".replace(".", ",")
            ejes.text(datos[lugar] + 0.015 * maximo, lugar, escrito,
                      va="center", fontsize=9, color=TINTA_SUAVE)
        ejes.set_xlim(0, maximo * 1.15)
        ejes.xaxis.set_major_formatter(FuncFormatter(_con_coma))
        ejes.set_title(titulo)
        ejes.spines["left"].set_visible(False)
        ejes.tick_params(axis="y", length=0)
        figura.tight_layout()
        plt.show()


def dibujar_mapa(
    matriz: Sequence[Sequence[float]],
    filas: Sequence[str],
    columnas: Sequence[str],
    titulo: str,
) -> None:
    """Dibuja una matriz chica con valores visibles.

    Args:
        matriz: Valores ya calculados por fila y columna.
        filas: Rotulos de fila.
        columnas: Rotulos de columna.
        titulo: Titulo del grafico.
    """
    datos = np.asarray(matriz, dtype=float)
    if datos.shape != (len(filas), len(columnas)):
        raise ValueError("La matriz no coincide con sus rotulos.")
    mapa = LinearSegmentedColormap.from_list("tokens", [FONDO, VIOLETA])
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(0.9 * len(columnas) + 1.8, 0.7 * len(filas) + 1.8)
        )
        ejes.imshow(datos, cmap=mapa, norm=Normalize(vmin=0, vmax=1))
        ejes.set_xticks(range(len(columnas)), columnas, rotation=25, ha="left")
        ejes.set_yticks(range(len(filas)), filas)
        ejes.xaxis.tick_top()
        for fila in range(len(filas)):
            for columna in range(len(columnas)):
                valor = datos[fila, columna]
                tinta = FONDO if valor > 0.55 else TINTA
                ejes.text(columna, fila, f"{valor:.0f}", ha="center",
                           va="center", color=tinta, fontweight="bold")
        ejes.set_title(titulo, pad=30, loc="left")
        figura.tight_layout()
        plt.show()


def dibujar_ciclo() -> None:
    """Dibuja el ciclo causal que usa un modelo generativo."""
    pasos = [
        ("Prefijo", AZUL),
        ("Logits", VIOLETA),
        ("Probabilidades", NARANJA),
        ("Token elegido", AZUL),
        ("Nuevo prefijo", GRIS),
    ]
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(8.5, 2.8))
        ejes.set_xlim(0, len(pasos))
        ejes.set_ylim(0, 1)
        ejes.set_axis_off()
        for lugar in range(len(pasos)):
            texto, color = pasos[lugar]
            caja = FancyBboxPatch(
                (lugar + 0.08, 0.4), 0.84, 0.25,
                boxstyle="round,pad=0.03", facecolor=FONDO,
                edgecolor=color, linewidth=2,
            )
            ejes.add_patch(caja)
            ejes.text(lugar + 0.5, 0.52, texto, ha="center", va="center")
            if lugar < len(pasos) - 1:
                ejes.annotate("", xy=(lugar + 1.04, 0.52),
                              xytext=(lugar + 0.92, 0.52),
                              arrowprops={"arrowstyle": "->", "color": LINEA})
        ejes.set_title("El ciclo de predecir un token y continuar", pad=12)
        figura.tight_layout()
        plt.show()


def dibujar_mapa_con_signo(
    matriz: Sequence[Sequence[float]],
    filas: Sequence[str],
    columnas: Sequence[str],
    titulo: str,
    decimales: int = 3,
) -> None:
    """Dibuja una matriz con valores positivos y negativos, con su numero.

    Naranja es positivo y azul, negativo, como en la unidad 011.

    Args:
        matriz: Valores ya calculados por fila y columna.
        filas: Rotulos de fila.
        columnas: Rotulos de columna.
        titulo: Titulo del grafico.
        decimales: Decimales que se escriben en cada celda.
    """
    datos = np.asarray(matriz, dtype=float)
    if datos.shape != (len(filas), len(columnas)):
        raise ValueError("La matriz no coincide con sus rotulos.")
    limite = float(np.abs(datos).max()) or 1.0
    mapa = LinearSegmentedColormap.from_list("signo", [AZUL, FONDO, NARANJA])
    norma = TwoSlopeNorm(vmin=-limite, vcenter=0.0, vmax=limite)
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(0.9 * len(columnas) + 1.8, 0.7 * len(filas) + 1.8)
        )
        ejes.imshow(datos, cmap=mapa, norm=norma)
        ejes.set_xticks(range(len(columnas)), columnas)
        ejes.set_yticks(range(len(filas)), filas)
        ejes.xaxis.tick_top()
        for fila in range(len(filas)):
            for columna in range(len(columnas)):
                valor = datos[fila, columna]
                escrito = f"{valor:.{decimales}f}".replace(".", ",")
                escrito = escrito.replace("-", "\u2212")
                intensidad = abs(norma(valor) - 0.5)
                tinta = FONDO if intensidad > 0.3 else TINTA
                ejes.text(columna, fila, escrito, ha="center", va="center",
                          color=tinta, fontsize=8)
        ejes.set_title(titulo, pad=30, loc="left")
        figura.tight_layout()
        plt.show()
