"""Funciones para dibujar resultados que el cuaderno ya calculo.

El modulo se ocupa de la presentacion. Los valores se calculan antes, en el
cuaderno o en una funcion analitica visible para el estudiante.
"""

from collections.abc import Mapping, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
from numpy.typing import ArrayLike

AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#8b8b86"
VIOLETA = "#4a3aa7"
VERDE_AZULADO = "#2a9d8f"

TINTAS = {
    AZUL: "#cfe0f6",
    NARANJA: "#fbd9cc",
    GRIS: "#ececea",
    VIOLETA: "#dcd6f2",
    VERDE_AZULADO: "#cfe9e5",
}

TINTA = "#0b0b0b"
TINTA_SUAVE = "#52514e"
LINEA = "#c3c2b7"
FONDO = "#ffffff"

COLOR_POR_METODO = {
    "conteo": GRIS,
    "TF-IDF": GRIS,
    "promedio": AZUL,
    "promedio de vectores": AZUL,
    "oracion": NARANJA,
    "embedding de oracion": NARANJA,
}
COLORES_DE_GRUPO = [AZUL, NARANJA, VIOLETA, VERDE_AZULADO]
FORMAS_DE_GRUPO = ["o", "s", "^", "D"]

ESTILO = {
    "figure.dpi": 110,
    "figure.facecolor": FONDO,
    "axes.facecolor": FONDO,
    "savefig.facecolor": FONDO,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "axes.edgecolor": LINEA,
    "axes.labelcolor": TINTA_SUAVE,
    "xtick.color": TINTA_SUAVE,
    "ytick.color": TINTA_SUAVE,
    "text.color": TINTA,
    "font.size": 10,
    "axes.titlelocation": "left",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "legend.frameon": False,
}


def dibujar_fichas(
    piezas: Sequence[str],
    clases: Sequence[str],
    estilos: Mapping[str, tuple[str, str, str]],
    titulo: str = "",
    notas: Sequence[str] | None = None,
    por_fila: int = 12,
) -> None:
    """Dibuja cada pieza como una ficha y agrega una leyenda.

    Args:
        piezas: Textos que se muestran, uno por ficha.
        clases: Clase de cada pieza, en el mismo orden que piezas.
        estilos: Diccionario de clase a (color, nombre, significado).
        titulo: Titulo del grafico.
        notas: Texto opcional que aparece debajo de cada ficha.
        por_fila: Ancho aproximado de cada fila, medido en unidades de texto.

    Raises:
        ValueError: Si las listas no tienen el mismo largo o por_fila no es
            positivo.
        KeyError: Si una clase no tiene un estilo definido.
    """
    if len(piezas) != len(clases):
        raise ValueError("piezas y clases deben tener el mismo largo.")
    if notas is not None and len(notas) != len(piezas):
        raise ValueError("notas debe tener el mismo largo que piezas.")
    if por_fila < 1:
        raise ValueError("por_fila debe ser mayor que cero.")
    if len(piezas) == 0:
        raise ValueError("Hace falta al menos una pieza para dibujar fichas.")

    anchos = []
    for lugar in range(len(piezas)):
        ancho_pieza = max(1.2, len(piezas[lugar]) / 8 + 0.45)
        if notas is not None:
            ancho_nota = len(notas[lugar]) / 8 + 0.45
            ancho_pieza = max(ancho_pieza, ancho_nota)
        anchos.append(ancho_pieza)
        if clases[lugar] not in estilos:
            raise KeyError(f"No hay un estilo para la clase {clases[lugar]}.")

    filas = []
    fila_actual = []
    ancho_actual = 0.0
    for lugar in range(len(piezas)):
        if fila_actual and ancho_actual + anchos[lugar] > por_fila:
            filas.append(fila_actual)
            fila_actual = []
            ancho_actual = 0.0
        fila_actual.append(lugar)
        ancho_actual += anchos[lugar]
    if fila_actual:
        filas.append(fila_actual)

    ancho_total = 1.0
    for fila in filas:
        ancho_fila = 0.0
        for lugar in fila:
            ancho_fila += anchos[lugar]
        ancho_total = max(ancho_total, ancho_fila)

    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(
                min(max(7.5, ancho_total * 0.8), 16),
                0.55 * len(filas) + 1.2,
            )
        )
        ejes.set_xlim(0, ancho_total)
        ejes.set_ylim(-0.2, len(filas) + 0.4)
        ejes.set_axis_off()

        for numero_fila in range(len(filas)):
            x = 0.0
            y = len(filas) - numero_fila - 0.1
            for lugar in filas[numero_fila]:
                color = estilos[clases[lugar]][0]
                color_fondo = TINTAS.get(color, "#f2f2f0")
                centro = x + anchos[lugar] / 2
                ejes.text(
                    centro,
                    y,
                    piezas[lugar],
                    ha="center",
                    va="center",
                    bbox={
                        "boxstyle": "round,pad=0.35",
                        "fc": color_fondo,
                        "ec": color,
                        "lw": 1,
                    },
                )
                if notas is not None and notas[lugar]:
                    ejes.text(
                        centro,
                        y - 0.32,
                        notas[lugar],
                        ha="center",
                        va="center",
                        fontsize=8.5,
                        fontweight="bold",
                    )
                x += anchos[lugar]

        if titulo:
            ejes.set_title(titulo, loc="left", pad=12)

        leyenda = []
        for clase in estilos:
            nombre = estilos[clase][1]
            significado = estilos[clase][2]
            leyenda.append(f"{nombre}: {significado}")
        ejes.text(
            0,
            0,
            " | ".join(leyenda),
            ha="left",
            va="bottom",
            fontsize=8.5,
            color=TINTA_SUAVE,
        )
        plt.show()


def dibujar_barras(
    nombres: Sequence[str],
    valores: ArrayLike,
    titulo: str = "",
    color: str = AZUL,
    formato: str = "{:.2f}",
    colores: Sequence[str] | None = None,
) -> None:
    """Dibuja barras horizontales con el valor escrito al final.

    Args:
        nombres: Rotulo de cada barra.
        valores: Valor ya calculado que corresponde a cada rotulo.
        titulo: Titulo del grafico.
        color: Color unico para las barras si no se pasa colores.
        formato: Formato del numero, por ejemplo "{:.2f}".
        colores: Color de cada barra, en el mismo orden que nombres.

    Raises:
        ValueError: Si faltan nombres o los largos no coinciden.
    """
    if len(nombres) == 0:
        raise ValueError("Hace falta al menos una barra.")
    datos = np.asarray(valores, dtype=float)
    if datos.ndim != 1:
        raise ValueError("valores debe ser una lista de numeros.")
    if not np.all(np.isfinite(datos)):
        raise ValueError("valores debe contener solo numeros finitos.")
    if len(nombres) != len(datos):
        raise ValueError("nombres y valores deben tener el mismo largo.")
    if colores is not None and len(colores) != len(nombres):
        raise ValueError("colores debe tener el mismo largo que nombres.")

    colores_de_barras = [color] * len(nombres)
    if colores is not None:
        colores_de_barras = list(colores)

    maximo = float(np.max(np.abs(datos)))
    margen = max(maximo * 0.02, 0.001)

    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(7, 0.32 * len(nombres) + 1.0)
        )
        lugares = list(range(len(nombres)))
        ejes.barh(lugares, datos, color=colores_de_barras, height=0.62)
        ejes.set_yticks(lugares, nombres)
        ejes.invert_yaxis()
        ejes.axvline(0, color=LINEA, linewidth=1)
        for lugar in lugares:
            valor = float(datos[lugar])
            if valor >= 0:
                x = valor + margen
                alineacion = "left"
            else:
                x = valor - margen
                alineacion = "right"
            ejes.text(
                x,
                lugar,
                formato.format(valor),
                va="center",
                ha=alineacion,
                fontsize=9,
                color=TINTA_SUAVE,
            )
        ejes.set_title(titulo)
        ejes.spines["left"].set_visible(False)
        ejes.tick_params(axis="y", length=0)
        plt.show()


def dibujar_barras_agrupadas(
    categorias: Sequence[str],
    series: Mapping[str, ArrayLike],
    titulo: str = "",
    maximo: float | None = None,
    colores: Mapping[str, str] | None = None,
    orientacion: str = "horizontal",
    etiqueta_valor: str = "",
) -> None:
    """Dibuja varias series para cada categoria.

    Args:
        categorias: Rotulo de cada categoria.
        series: Valores ya calculados, agrupados por nombre de serie.
        titulo: Titulo del grafico.
        maximo: Limite superior del eje de valores, si hace falta.
        colores: Color opcional por nombre de serie.
        orientacion: "horizontal" o "vertical".
        etiqueta_valor: Nombre del eje que contiene los valores.

    Raises:
        ValueError: Si no hay series, los largos no coinciden o la
            orientacion no es valida.
    """
    if len(categorias) == 0:
        raise ValueError("Hace falta al menos una categoria.")
    if not series:
        raise ValueError("Hace falta al menos una serie.")
    if orientacion not in ("horizontal", "vertical"):
        raise ValueError("orientacion debe ser horizontal o vertical.")

    nombres_de_series = list(series)
    valores_por_serie = {}
    for nombre in nombres_de_series:
        valores = np.asarray(series[nombre], dtype=float)
        if valores.ndim != 1:
            raise ValueError(
                f"La serie {nombre} debe ser una lista de numeros."
            )
        if not np.all(np.isfinite(valores)):
            raise ValueError(f"La serie {nombre} debe tener numeros finitos.")
        if len(valores) != len(categorias):
            raise ValueError(
                f"La serie {nombre} no coincide con la cantidad de categorias."
            )
        valores_por_serie[nombre] = valores

    cantidad_de_series = len(nombres_de_series)
    alto_de_barra = 0.8 / cantidad_de_series

    with plt.rc_context(ESTILO):
        if orientacion == "horizontal":
            figura, ejes = plt.subplots(
                figsize=(8, 0.32 * len(categorias) * cantidad_de_series + 1.4)
            )
        else:
            figura, ejes = plt.subplots(
                figsize=(max(6, 1.1 * len(categorias)), 4.5)
            )

        for orden in range(cantidad_de_series):
            nombre = nombres_de_series[orden]
            color = COLOR_POR_METODO.get(
                nombre,
                COLORES_DE_GRUPO[orden % len(COLORES_DE_GRUPO)],
            )
            if colores is not None and nombre in colores:
                color = colores[nombre]

            for lugar in range(len(categorias)):
                valor = float(valores_por_serie[nombre][lugar])
                if orientacion == "horizontal":
                    posicion = (
                        lugar - 0.4 + alto_de_barra * (orden + 0.5)
                    )
                    ejes.barh(
                        posicion,
                        valor,
                        height=alto_de_barra * 0.92,
                        color=color,
                        label=nombre if lugar == 0 else None,
                    )
                    if valor >= 0:
                        x = valor + 0.01
                        alineacion = "left"
                    else:
                        x = valor - 0.01
                        alineacion = "right"
                    ejes.text(
                        x,
                        posicion,
                        f"{valor:.2f}",
                        va="center",
                        ha=alineacion,
                        fontsize=7.5,
                        color=TINTA_SUAVE,
                    )
                else:
                    posicion = (
                        lugar - 0.4 + alto_de_barra * (orden + 0.5)
                    )
                    ejes.bar(
                        posicion,
                        valor,
                        width=alto_de_barra * 0.92,
                        color=color,
                        label=nombre if lugar == 0 else None,
                    )
                    ejes.text(
                        posicion,
                        valor,
                        f"{valor:.2f}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                        color=TINTA_SUAVE,
                    )

        if orientacion == "horizontal":
            ejes.set_yticks(list(range(len(categorias))), categorias)
            ejes.invert_yaxis()
            ejes.axvline(0, color=LINEA, linewidth=1)
            ejes.set_xlabel(etiqueta_valor)
            ejes.spines["left"].set_visible(False)
            ejes.tick_params(axis="y", length=0)
            if maximo is not None:
                ejes.set_xlim(right=maximo)
            ejes.legend(
                ncol=cantidad_de_series,
                loc="lower left",
                bbox_to_anchor=(0, 1.0),
            )
            ejes.set_title(titulo, pad=30)
        else:
            ejes.set_xticks(list(range(len(categorias))), categorias)
            ejes.set_ylabel(etiqueta_valor)
            ejes.set_ylim(bottom=0)
            if maximo is not None:
                ejes.set_ylim(top=maximo)
            ejes.set_title(titulo)
            ejes.legend(loc="upper left")

        figura.tight_layout()
        plt.show()


def dibujar_mapa_de_calor(
    matriz: ArrayLike,
    filas: Sequence[str],
    columnas: Sequence[str],
    titulo: str = "",
    formato: str = "{:g}",
    anotar: bool = True,
    color: str = AZUL,
    etiqueta_filas: str = "",
    etiqueta_columnas: str = "",
) -> None:
    """Dibuja una matriz recibida, sin calcular sus valores.

    Args:
        matriz: Valores ya calculados, organizados por fila.
        filas: Rotulos de las filas.
        columnas: Rotulos de las columnas.
        titulo: Titulo del grafico.
        formato: Formato para escribir cada valor.
        anotar: Si es True, escribe valores en matrices chicas.
        color: Color de mayor intensidad.
        etiqueta_filas: Descripcion opcional de las filas.
        etiqueta_columnas: Descripcion opcional de las columnas.

    ValueError: Si las dimensiones no coinciden.
    """
    datos = np.asarray(matriz, dtype=float)
    if len(filas) == 0 or len(columnas) == 0:
        raise ValueError("Hace falta al menos una fila y una columna.")
    if datos.shape != (len(filas), len(columnas)):
        raise ValueError("La matriz no coincide con sus rotulos.")
    if not np.all(np.isfinite(datos)):
        raise ValueError("La matriz debe contener solo numeros finitos.")
    minimo = float(np.min(datos))
    maximo = float(np.max(datos))
    if minimo < 0:
        limite = max(abs(minimo), abs(maximo))
        escala = TwoSlopeNorm(vmin=-limite, vcenter=0, vmax=limite)
        mapa = LinearSegmentedColormap.from_list(
            "paleta_divergente", [NARANJA, FONDO, AZUL]
        )
    else:
        limite = max(maximo, 1e-9)
        escala = Normalize(vmin=0, vmax=limite)
        mapa = LinearSegmentedColormap.from_list(
            "paleta_compartida", [FONDO, color]
        )
    ancho = min(max(0.55 * len(columnas) + 2.5, 4.5), 7.5)
    alto = min(max(0.45 * len(filas) + 1.5, 3.5), 6.5)
    anotar_valores = anotar and len(filas) <= 15 and len(columnas) <= 15

    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(ancho, alto))
        ejes.imshow(datos, cmap=mapa, norm=escala)
        letra = 9 if len(columnas) <= 15 else 6.5
        ejes.set_xticks(
            list(range(len(columnas))),
            columnas,
            rotation=45,
            ha="left",
            fontsize=letra,
        )
        ejes.set_yticks(list(range(len(filas))), filas, fontsize=letra)
        ejes.xaxis.tick_top()
        if etiqueta_filas:
            ejes.set_ylabel(etiqueta_filas)
        if etiqueta_columnas:
            ejes.set_xlabel(etiqueta_columnas)
            ejes.xaxis.set_label_position("top")

        if anotar_valores:
            for fila in range(len(filas)):
                for columna in range(len(columnas)):
                    valor = datos[fila, columna]
                    color_texto = FONDO if abs(valor) > 0.6 * limite else TINTA
                    if valor == 0:
                        color_texto = LINEA
                    ejes.text(
                        columna,
                        fila,
                        formato.format(valor),
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color=color_texto,
                    )

        for borde in ejes.spines.values():
            borde.set_visible(False)
        ejes.tick_params(length=0)
        if titulo:
            espacios = 55 if etiqueta_columnas else 40
            ejes.set_title(titulo, pad=espacios)
        figura.tight_layout()
        plt.show()


def dibujar_dispersion(
    coordenadas: ArrayLike,
    grupos: Sequence[str],
    titulo: str = "",
    etiqueta_x: str = "",
    etiqueta_y: str = "",
) -> None:
    """Dibuja puntos con una forma y un color por grupo.

    Args:
        coordenadas: Dos valores ya calculados por punto.
        grupos: Grupo correspondiente a cada punto.
        titulo: Titulo del grafico.
        etiqueta_x: Nombre del eje horizontal.
        etiqueta_y: Nombre del eje vertical.

    Raises:
        ValueError: Si las coordenadas no tienen dos columnas o no coinciden
            con la cantidad de grupos.
    """
    puntos = np.asarray(coordenadas, dtype=float)
    if puntos.ndim != 2 or puntos.shape[1] != 2:
        raise ValueError("Cada punto debe tener dos coordenadas.")
    if not np.all(np.isfinite(puntos)):
        raise ValueError("Las coordenadas deben ser numeros finitos.")
    if len(puntos) != len(grupos):
        raise ValueError("grupos debe tener un valor por punto.")
    if len(grupos) == 0:
        raise ValueError("Hace falta al menos un punto.")

    nombres = sorted(set(grupos))
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(6.5, 4.2))
        for orden in range(len(nombres)):
            lugares = []
            for lugar in range(len(grupos)):
                if grupos[lugar] == nombres[orden]:
                    lugares.append(lugar)
            ejes.scatter(
                puntos[lugares, 0],
                puntos[lugares, 1],
                s=46,
                color=COLORES_DE_GRUPO[orden % len(COLORES_DE_GRUPO)],
                marker=FORMAS_DE_GRUPO[orden % len(FORMAS_DE_GRUPO)],
                edgecolor=FONDO,
                linewidth=0.8,
                label=nombres[orden],
            )
        ejes.set_title(titulo)
        ejes.set_xlabel(etiqueta_x)
        ejes.set_ylabel(etiqueta_y)
        ejes.legend(title="Grupo")
        plt.show()
