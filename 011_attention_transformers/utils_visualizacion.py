"""Funciones para dibujar resultados que el cuaderno ya calculo.

El modulo se ocupa de la presentacion: muestra, pero no decide ni transforma
los datos del analisis. Los valores se calculan antes, a la vista, en el
cuaderno. utils.py reexporta estas funciones: en los cuadernos se llaman
como utils.dibujar_...

El codigo va en ASCII. Los rotulos que lee el estudiante llevan sus tildes
escapadas con la barra invertida y el codigo de la letra.
"""

from collections.abc import Mapping, Sequence

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
from matplotlib.patches import (
    FancyArrowPatch,
    FancyBboxPatch,
    Patch,
    Rectangle,
)
from matplotlib.ticker import FuncFormatter

AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#8b8b86"
VIOLETA = "#4a3aa7"
VERDE_AZULADO = "#2a9d8f"
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
    "axes.titlepad": 12,
    "legend.frameon": False,
}

MAXIMO_CON_NUMEROS = 10


def _con_coma(valor: float, posicion: int) -> str:
    """Escribe una marca de eje con coma decimal.

    Args:
        valor: Valor de la marca.
        posicion: Lugar de la marca; matplotlib lo pasa y no se usa.

    Returns:
        El valor como texto, con coma.
    """
    return f"{valor:g}".replace(".", ",")


def dibujar_fichas(
    piezas: Sequence[str],
    clases: Sequence[str],
    estilos: Mapping[str, tuple[str, str]],
    titulo: str,
    notas: Sequence[str] | None = None,
    por_fila: int | None = None,
) -> None:
    """Dibuja palabras o vectores como fichas rotuladas.

    Args:
        piezas: Textos de las fichas.
        clases: Clase de cada ficha.
        estilos: Clase a par de color y etiqueta.
        titulo: Titulo del grafico.
        notas: Texto breve debajo de cada ficha.
        por_fila: Fichas por fila. Con None van todas en una fila.
    """
    if len(piezas) != len(clases):
        raise ValueError("piezas y clases deben tener el mismo largo.")
    if notas is not None and len(notas) != len(piezas):
        raise ValueError("notas debe tener el mismo largo que piezas.")
    cantidad = len(piezas)
    por_fila = por_fila or cantidad
    filas = -(-cantidad // por_fila)
    alto_de_fila = 1.0 if notas is None else 1.25
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(
            figsize=(max(6.5, por_fila * 1.2), 0.8 + alto_de_fila * filas),
        )
        ejes.set_xlim(-0.6, por_fila - 0.4)
        ejes.set_ylim(-filas + 0.2, 0.65)
        ejes.set_axis_off()
        for posicion in range(cantidad):
            fila, columna = divmod(posicion, por_fila)
            color, _ = estilos[clases[posicion]]
            ejes.text(
                columna, -fila * 1.0, piezas[posicion], ha="center",
                va="center", fontsize=11,
                bbox={"boxstyle": "round,pad=0.5", "fc": FONDO,
                      "ec": color, "lw": 2},
            )
            if notas is not None:
                ejes.text(columna, -fila * 1.0 - 0.38, notas[posicion],
                          ha="center", va="center", fontsize=9,
                          color=TINTA_SUAVE)
        muestras = []
        for clase in estilos:
            color, etiqueta = estilos[clase]
            muestras.append(Patch(facecolor=FONDO, edgecolor=color,
                                  linewidth=2, label=etiqueta))
        ejes.legend(handles=muestras, loc="lower left",
                    bbox_to_anchor=(0, -0.02 - 0.12 / filas),
                    ncol=len(muestras), fontsize=8.5, handlelength=1.4)
        ejes.set_title(titulo)
        figura.tight_layout()
        plt.show()


def dibujar_barras(
    nombres: Sequence[str],
    valores: Sequence[float],
    titulo: str,
    color: str = AZUL,
) -> None:
    """Dibuja barras horizontales y escribe cada valor.

    Args:
        nombres: Rotulos de las barras.
        valores: Valores ya calculados.
        titulo: Titulo del grafico.
        color: Color de las barras.
    """
    datos = np.asarray(valores, dtype=float)
    if len(nombres) != len(datos):
        raise ValueError("nombres y valores deben tener el mismo largo.")
    minimo = min(0.0, float(datos.min()))
    maximo = max(0.0, float(datos.max()))
    tramo = (maximo - minimo) or 1.0
    holgura = 0.02 * tramo
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(7, len(nombres) * 0.45 + 1.1))
        posiciones = list(range(len(nombres)))
        ejes.barh(posiciones, datos, color=color, height=0.72)
        ejes.set_yticks(posiciones, nombres)
        ejes.invert_yaxis()
        ejes.axvline(0, color=LINEA, linewidth=1)
        for posicion in posiciones:
            valor = datos[posicion]
            escrito = f"{valor:.2f}".replace(".", ",").replace("-", "\u2212")
            if valor >= 0:
                ejes.text(valor + holgura, posicion, escrito, va="center",
                          ha="left", fontsize=9, color=TINTA_SUAVE)
            else:
                ejes.text(valor - holgura, posicion, escrito, va="center",
                          ha="right", fontsize=9, color=TINTA_SUAVE)
        izquierda = minimo - 0.14 * tramo if minimo < 0 else 0.0
        ejes.set_xlim(izquierda, maximo + 0.14 * tramo)
        ejes.xaxis.set_major_formatter(FuncFormatter(_con_coma))
        ejes.set_title(titulo)
        ejes.spines["left"].set_visible(False)
        ejes.tick_params(axis="y", length=0)
        figura.tight_layout()
        plt.show()


def dibujar_barras_agrupadas(
    categorias: Sequence[str],
    series: Mapping[str, Sequence[float]],
    titulo: str,
    etiqueta_y: str = "Valor",
) -> None:
    """Dibuja series comparables para las mismas categorias.

    Args:
        categorias: Rotulos compartidos por las series.
        series: Nombre de serie a valores ya calculados.
        titulo: Titulo del grafico.
        etiqueta_y: Que mide el eje vertical.
    """
    colores = [GRIS, NARANJA, AZUL, VIOLETA]
    ancho = 0.8 / len(series)
    todos = []
    for nombre in series:
        if len(series[nombre]) != len(categorias):
            raise ValueError("Cada serie necesita un valor por categoria.")
        todos.extend(series[nombre])
    minimo = min(0.0, float(min(todos)))
    maximo = max(0.0, float(max(todos)))
    tramo = (maximo - minimo) or 1.0
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(7.5, 4.4), layout="constrained")
        for orden, nombre in enumerate(series):
            valores = np.asarray(series[nombre], dtype=float)
            desplazamiento = (orden - (len(series) - 1) / 2) * ancho
            posiciones = np.arange(len(categorias)) + desplazamiento
            ejes.bar(posiciones, valores, width=ancho * 0.94, label=nombre,
                     color=colores[orden % len(colores)])
            for lugar in range(len(valores)):
                valor = valores[lugar]
                escrito = f"{valor:.2f}".replace(".", ",")
                escrito = escrito.replace("-", "\u2212")
                if valor >= 0:
                    ejes.text(posiciones[lugar], valor + 0.015 * tramo,
                              escrito, ha="center", va="bottom",
                              fontsize=8.5, color=TINTA_SUAVE)
                else:
                    ejes.text(posiciones[lugar], valor - 0.015 * tramo,
                              escrito, ha="center", va="top",
                              fontsize=8.5, color=TINTA_SUAVE)
        ejes.set_xticks(np.arange(len(categorias)), categorias)
        ejes.axhline(0, color=LINEA, linewidth=1)
        abajo = minimo - 0.12 * tramo if minimo < 0 else 0.0
        ejes.set_ylim(abajo, maximo + 0.12 * tramo)
        ejes.yaxis.set_major_formatter(FuncFormatter(_con_coma))
        ejes.set_ylabel(etiqueta_y)
        ejes.tick_params(axis="x", length=0)
        figura.legend(loc="outside lower center", ncol=len(series))
        ejes.set_title(titulo)
        plt.show()


def _dibujar_celdas(
    ejes: plt.Axes,
    datos: np.ndarray,
    filas: Sequence[str],
    columnas: Sequence[str],
    color: str,
    maximo: float,
    anotar: bool,
) -> None:
    """Dibuja las celdas de una matriz sobre unos ejes ya creados.

    Args:
        ejes: Ejes donde se dibuja.
        datos: Matriz ya calculada.
        filas: Rotulos de las filas.
        columnas: Rotulos de las columnas.
        color: Color para los valores mas altos.
        maximo: Valor que recibe el color pleno.
        anotar: Si se escribe el numero en cada celda.
    """
    mapa = LinearSegmentedColormap.from_list("celdas", [FONDO, color])
    ejes.imshow(datos, cmap=mapa, norm=Normalize(vmin=0, vmax=maximo))
    ejes.set_xticks(range(len(columnas)), columnas)
    ejes.set_yticks(range(len(filas)), filas)
    ejes.set_xticks(np.arange(-0.5, len(columnas)), minor=True)
    ejes.set_yticks(np.arange(-0.5, len(filas)), minor=True)
    ejes.grid(which="minor", color=FONDO, linewidth=1.5)
    ejes.tick_params(which="both", length=0)
    for lado in ejes.spines.values():
        lado.set_visible(False)
    if not anotar:
        return
    letra = 9 if len(filas) <= MAXIMO_CON_NUMEROS else 6.5
    for fila in range(len(filas)):
        for columna in range(len(columnas)):
            valor = datos[fila, columna]
            if np.isclose(valor, 0.0):
                tinta = LINEA
            elif valor > 0.55 * maximo:
                tinta = FONDO
            else:
                tinta = TINTA
            ejes.text(columna, fila, f"{valor:.2f}", ha="center",
                      va="center", color=tinta, fontsize=letra)


def dibujar_mapa_de_calor(
    matriz: Sequence[Sequence[float]],
    filas: Sequence[str],
    columnas: Sequence[str],
    titulo: str,
    color: str = NARANJA,
    etiqueta_x: str = "Token considerado",
    etiqueta_y: str = "Token que consulta",
    maximo: float = 1.0,
) -> None:
    """Dibuja una matriz con el numero en cada celda.

    Con mas de 10 filas se omiten los numeros, porque ya no se leen, y se
    agrega una escala de color.

    Args:
        matriz: Valores ya calculados por fila y columna.
        filas: Rotulos de las filas.
        columnas: Rotulos de las columnas.
        titulo: Titulo del grafico.
        color: Color para los valores mas altos.
        etiqueta_x: Que representan las columnas.
        etiqueta_y: Que representan las filas.
        maximo: Valor que recibe el color pleno. Con 1.0 todos los mapas
            de atencion de la unidad se comparan en la misma escala.
    """
    dibujar_mapas_lado_a_lado(
        matrices={titulo: matriz}, filas=filas, columnas=columnas,
        titulo="", color=color, etiqueta_x=etiqueta_x,
        etiqueta_y=etiqueta_y, maximo=maximo,
    )


def dibujar_mapas_lado_a_lado(
    matrices: Mapping[str, Sequence[Sequence[float]]],
    filas: Sequence[str],
    columnas: Sequence[str],
    titulo: str,
    color: str = NARANJA,
    etiqueta_x: str = "Token considerado",
    etiqueta_y: str = "Token que consulta",
    maximo: float = 1.0,
) -> None:
    """Dibuja una o varias matrices de la misma forma, en la misma escala.

    Con mas de 10 filas se omiten los numeros y se agrega una escala de
    color compartida.

    Args:
        matrices: Nombre de cada matriz a sus valores ya calculados.
        filas: Rotulos de las filas, compartidos.
        columnas: Rotulos de las columnas, compartidos.
        titulo: Titulo general del grafico. Si es vacio y hay una sola
            matriz, el nombre de la matriz hace de titulo.
        color: Color para los valores mas altos.
        etiqueta_x: Que representan las columnas.
        etiqueta_y: Que representan las filas.
        maximo: Valor que recibe el color pleno, igual para todas.
    """
    anotar = len(filas) <= MAXIMO_CON_NUMEROS
    cantidad = len(matrices)
    celda = 0.62 if anotar else 0.3
    ancho = celda * len(columnas) * cantidad + 1.4 + (0 if anotar else 1.2)
    alto = celda * len(filas) + (1.5 if anotar else 2.4)
    with plt.rc_context(ESTILO):
        figura, todos = plt.subplots(
            1, cantidad, figsize=(max(ancho, 4.2), alto), sharey=True,
            layout="constrained", squeeze=False,
        )
        ejes_de_la_fila = todos[0]
        for ejes, nombre in zip(ejes_de_la_fila, matrices):
            datos = np.asarray(matrices[nombre], dtype=float)
            if datos.shape != (len(filas), len(columnas)):
                raise ValueError("Cada matriz debe coincidir con sus "
                                 "rotulos.")
            _dibujar_celdas(ejes, datos, filas, columnas, color, maximo,
                            anotar)
            ejes.set_title(nombre, fontsize=10, loc="left")
            ejes.set_xlabel(etiqueta_x)
            if not anotar:
                plt.setp(ejes.get_xticklabels(), rotation=90)
        ejes_de_la_fila[0].set_ylabel(etiqueta_y)
        if not anotar:
            escala = figura.colorbar(ejes_de_la_fila[0].images[0],
                                     ax=list(ejes_de_la_fila), shrink=0.7,
                                     pad=0.02)
            escala.set_label("Peso (color pleno = "
                             f"{maximo:.2f})".replace(".", ","))
            escala.outline.set_visible(False)
        if titulo:
            figura.suptitle(titulo, x=0.0, ha="left", fontsize=11,
                            fontweight="bold")
        plt.show()


def dibujar_dispersion(
    coordenadas: Sequence[Sequence[float]],
    grupos: Sequence[str],
    etiquetas: Sequence[str],
    titulo: str,
) -> None:
    """Dibuja vectores bidimensionales con color y forma por grupo.

    Args:
        coordenadas: Dos coordenadas por punto.
        grupos: Grupo de cada punto.
        etiquetas: Texto junto a cada punto.
        titulo: Titulo del grafico.
    """
    puntos = np.asarray(coordenadas, dtype=float)
    if puntos.shape != (len(grupos), 2) or len(etiquetas) != len(grupos):
        raise ValueError("Cada punto necesita grupo, etiqueta y dos "
                         "coordenadas.")
    estilos = {"contexto A": (AZUL, "o"), "contexto B": (NARANJA, "s")}
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(6, 4.4))
        ya_rotulados = []
        for lugar in range(len(puntos)):
            color, forma = estilos[grupos[lugar]]
            rotulo = None
            if grupos[lugar] not in ya_rotulados:
                rotulo = grupos[lugar]
                ya_rotulados.append(grupos[lugar])
            ejes.scatter(puntos[lugar, 0], puntos[lugar, 1], color=color,
                         marker=forma, s=70, label=rotulo, zorder=3)
            ejes.annotate(etiquetas[lugar], puntos[lugar], xytext=(7, 6),
                          textcoords="offset points")
        ejes.axhline(0, color=LINEA, linewidth=1)
        ejes.axvline(0, color=LINEA, linewidth=1)
        ejes.margins(0.18)
        ejes.set_xlabel("Dimensi\u00f3n 1 del ejemplo")
        ejes.set_ylabel("Dimensi\u00f3n 2 del ejemplo")
        ejes.legend(title="Grupo", loc="upper right")
        ejes.set_title(titulo)
        figura.tight_layout()
        plt.show()


def dibujar_bloque_transformer(
    resaltar: str | tuple[str, ...] | None = None,
) -> None:
    """Dibuja el recorrido de un bloque decoder-only y la capa de salida.

    Args:
        resaltar: Parte o partes que se quieren mirar: "entrada",
            "atencion", "residual", "feed-forward" o "salida". Las demas
            quedan atenuadas. Con None se dibuja todo con su color.
    """
    if isinstance(resaltar, str):
        resaltar = (resaltar,)
    cajas = [
        ("entrada", "Embeddings de\ntoken + posici\u00f3n", AZUL),
        ("atencion", "Atenci\u00f3n causal\nmulti-cabeza", NARANJA),
        ("residual", "Suma residual\ny normalizaci\u00f3n", VERDE_AZULADO),
        ("feed-forward", "Red\nfeed-forward", VIOLETA),
        ("residual", "Suma residual\ny normalizaci\u00f3n", VERDE_AZULADO),
        ("salida", "Capa de salida\n(un puntaje por\npalabra)", GRIS),
        ("salida", "Softmax\n(probabilidades)", GRIS),
    ]
    ancho, separacion, base = 1.5, 0.42, 0.34
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(11, 3.3))
        ejes.set_xlim(-0.2, len(cajas) * (ancho + separacion) - 0.1)
        ejes.set_ylim(0, 1.08)
        ejes.set_axis_off()
        centros = []
        for orden in range(len(cajas)):
            clave, texto, color = cajas[orden]
            izquierda = orden * (ancho + separacion)
            activa = resaltar is None or clave in resaltar
            borde = color if activa else LINEA
            letra = TINTA if activa else GRIS
            ejes.add_patch(FancyBboxPatch(
                (izquierda, base), ancho, 0.36, boxstyle="round,pad=0.02",
                facecolor=FONDO, edgecolor=borde, linewidth=2,
            ))
            ejes.text(izquierda + ancho / 2, base + 0.18, texto,
                      ha="center", va="center", fontsize=9, color=letra)
            centros.append(izquierda + ancho / 2)
            if orden < len(cajas) - 1:
                ejes.add_patch(FancyArrowPatch(
                    (izquierda + ancho + 0.03, base + 0.18),
                    (izquierda + ancho + separacion - 0.03, base + 0.18),
                    arrowstyle="-|>", mutation_scale=11, color=TINTA_SUAVE,
                    linewidth=1.3,
                ))
        for inicio, fin in ((0, 2), (2, 4)):
            ejes.add_patch(FancyArrowPatch(
                (centros[inicio] + 0.55, base - 0.04),
                (centros[fin] - 0.55, base - 0.04),
                connectionstyle="arc3,rad=0.28", arrowstyle="-|>",
                mutation_scale=10, color=VERDE_AZULADO, linewidth=1.3,
            ))
            medio = (centros[inicio] + centros[fin]) / 2
            ejes.text(medio, 0.04, "conexi\u00f3n residual", ha="center",
                      fontsize=8, color=TINTA_SUAVE)
        izquierda_bloque = centros[1] - ancho / 2 - 0.1
        derecha_bloque = centros[4] + ancho / 2 + 0.1
        ejes.plot([izquierda_bloque, izquierda_bloque, derecha_bloque,
                   derecha_bloque], [0.84, 0.9, 0.9, 0.84],
                  color=TINTA_SUAVE, linewidth=1.2)
        ejes.text((izquierda_bloque + derecha_bloque) / 2, 0.96,
                  "un bloque; el modelo apila varios", ha="center",
                  fontsize=9, color=TINTA)
        ejes.set_title("Un Transformer decoder-only")
        figura.tight_layout()
        plt.show()


# ---------------------------------------------------------------------------
# Atlas visual: paneles con gramatica de colores, mapa del modelo y escenas
# con controles.
# ---------------------------------------------------------------------------

# Gramatica de colores: un tipo de dato, un color, en toda la unidad.
# "vector": numeros con signo (embeddings, consultas, claves).
# "puntaje": productos punto, antes de softmax.
# "atencion": pesos entre 0 y 1 que suman 1 por fila.
GRAMATICA = {
    "vector": {"negativo": AZUL, "positivo": NARANJA},
    "puntaje": {"negativo": GRIS, "positivo": VIOLETA},
    "atencion": {"negativo": FONDO, "positivo": NARANJA},
}

RAYADO = "////"


def _mapa_de_colores(tipo: str) -> LinearSegmentedColormap:
    """Devuelve la escala de colores de un tipo de dato.

    Args:
        tipo: "vector", "puntaje" o "atencion".

    Returns:
        Escala de colores de matplotlib.
    """
    colores = GRAMATICA[tipo]
    if tipo == "atencion":
        return LinearSegmentedColormap.from_list(
            tipo, [FONDO, colores["positivo"]],
        )
    return LinearSegmentedColormap.from_list(
        tipo, [colores["negativo"], FONDO, colores["positivo"]],
    )


def _dibujar_un_panel(ejes: plt.Axes, panel: Mapping) -> None:
    """Dibuja un panel sobre unos ejes ya creados.

    Args:
        ejes: Ejes donde se dibuja.
        panel: Diccionario con las claves que documenta dibujar_paneles.
    """
    datos = np.atleast_2d(np.asarray(panel["matriz"], dtype=float))
    tipo = panel.get("tipo", "vector")
    mascara = panel.get("mascara")
    if mascara is not None:
        mascara = np.atleast_2d(np.asarray(mascara, dtype=bool))
    if tipo == "atencion":
        norma = Normalize(vmin=0.0, vmax=panel.get("maximo", 1.0))
    else:
        limite = float(np.nanmax(np.abs(datos))) if np.any(
            np.isfinite(datos)) else 1.0
        limite = panel.get("maximo", limite) or 1.0
        norma = TwoSlopeNorm(vmin=-limite, vcenter=0.0, vmax=limite)
    visibles = np.ma.masked_invalid(datos)
    if mascara is not None:
        visibles = np.ma.masked_where(mascara, visibles)
    escala = _mapa_de_colores(tipo)
    escala.set_bad(FONDO)
    ejes.imshow(visibles, cmap=escala, norm=norma, aspect="equal")
    alto, ancho = datos.shape
    if mascara is not None:
        for fila in range(alto):
            for columna in range(ancho):
                if mascara[fila, columna]:
                    ejes.add_patch(Rectangle(
                        (columna - 0.5, fila - 0.5), 1, 1, facecolor=FONDO,
                        edgecolor=LINEA, hatch=RAYADO, linewidth=0,
                    ))
    filas = panel.get("filas")
    columnas = panel.get("columnas")
    if filas is None:
        ejes.set_yticks([])
    else:
        ejes.set_yticks(range(alto), filas)
    if columnas is None:
        ejes.set_xticks([])
    else:
        ejes.set_xticks(range(ancho), columnas, rotation=90)
    ejes.set_xticks(np.arange(-0.5, ancho), minor=True)
    ejes.set_yticks(np.arange(-0.5, alto), minor=True)
    ejes.grid(which="minor", color=FONDO, linewidth=1.2)
    ejes.tick_params(which="both", length=0)
    for lado in ejes.spines.values():
        lado.set_visible(False)
    if panel.get("numeros", False):
        decimales = panel.get("decimales", 2)
        for fila in range(alto):
            for columna in range(ancho):
                valor = datos[fila, columna]
                tapada = mascara is not None and mascara[fila, columna]
                if tapada or not np.isfinite(valor):
                    continue
                escrito = f"{valor:.{decimales}f}"
                escrito = escrito.replace(".", ",").replace("-", "\u2212")
                intensidad = abs(norma(valor) - norma(0.0))
                if abs(valor) < 0.5 * 10 ** -decimales:
                    tinta = LINEA
                elif intensidad > 0.55:
                    tinta = FONDO
                else:
                    tinta = TINTA
                ejes.text(columna, fila, escrito, ha="center", va="center",
                          fontsize=8, color=tinta)
    marco = panel.get("marco")
    if marco is not None:
        fila, columna, alto_marco, ancho_marco = marco
        ejes.add_patch(Rectangle(
            (columna - 0.5, fila - 0.5), ancho_marco, alto_marco,
            fill=False, edgecolor=TINTA, linewidth=2.2,
        ))
    ejes.set_title(panel.get("titulo", ""), fontsize=10, loc="left")


def dibujar_paneles(paneles: Sequence[Mapping], titulo: str = "") -> None:
    """Dibuja uno o varios paneles de numeros, uno al lado del otro.

    El color depende del tipo de dato (ver GRAMATICA). Las celdas que valen
    nan ("todavia no calculado") quedan en blanco. Las celdas marcadas en
    "mascara" se rayan: el modelo las tapa a proposito.

    Args:
        paneles: Lista de diccionarios. Claves: "matriz" (obligatoria),
            "titulo", "tipo" ("vector", "puntaje" o "atencion"), "filas" y
            "columnas" (rotulos), "numeros" (escribir el valor en cada
            celda), "decimales", "mascara" (celdas tapadas), "marco"
            (fila, columna, alto, ancho de un recuadro) y "maximo" (valor
            que recibe el color pleno).
        titulo: Titulo general.
    """
    anchos = []
    altos = []
    for panel in paneles:
        forma = np.atleast_2d(np.asarray(panel["matriz"])).shape
        altos.append(forma[0])
        anchos.append(forma[1])
    columnas_totales = sum(anchos)
    celda = 0.55
    if columnas_totales > 24:
        celda = max(0.13, 12.5 / columnas_totales)
    ancho_total = celda * columnas_totales + 1.4 * len(paneles) + 0.6
    alto_total = celda * max(altos) + 1.9
    hay_mascara = False
    for panel in paneles:
        if panel.get("mascara") is not None:
            hay_mascara = True
    with plt.rc_context(ESTILO):
        figura, todos = plt.subplots(
            1, len(paneles), figsize=(max(ancho_total, 4.5), alto_total),
            squeeze=False, layout="constrained",
            gridspec_kw={"width_ratios": anchos},
        )
        for lugar in range(len(paneles)):
            _dibujar_un_panel(todos[0][lugar], paneles[lugar])
        if hay_mascara:
            muestras = [
                Patch(facecolor=FONDO, edgecolor=LINEA, hatch=RAYADO,
                      label="rayado: tapado por la m\u00e1scara causal"),
                Patch(facecolor=FONDO, edgecolor=LINEA,
                      label="en blanco: todav\u00eda no calculado"),
            ]
            figura.legend(handles=muestras, loc="outside lower left",
                          ncol=2, fontsize=8.5)
        if titulo:
            figura.suptitle(titulo, x=0.0, ha="left", fontsize=11,
                            fontweight="bold")
        plt.show()


def _contar_parametros(modulo) -> int:
    """Cuenta los numeros que aprende un modulo de PyTorch.

    Args:
        modulo: Parte del modelo.

    Returns:
        Cantidad total de parametros.
    """
    total = 0
    for parametro in modulo.parameters():
        total = total + parametro.numel()
    return total


def _escribir_millones(cantidad: int) -> str:
    """Escribe una cantidad en millones, con coma decimal.

    Args:
        cantidad: Numero entero.

    Returns:
        Texto como "38,6 M".
    """
    return f"{cantidad / 1e6:.1f} M".replace(".", ",")


def dibujar_mapa_del_modelo(modelo, estamos_aca: str = "") -> None:
    """Dibuja el recorrido de GPT-2 leyendo las piezas del modelo real.

    Las medidas y la cantidad de parametros salen del modelo cargado, no de
    un texto escrito a mano: el mapa no puede diferir del modelo.

    Args:
        modelo: Modelo GPT2LMHeadModel ya cargado.
        estamos_aca: Pieza que se marca: "tokens", "embeddings",
            "atencion", "mlp", "bloques" o "salida". Vacio: ninguna.
    """
    nucleo = modelo.transformer
    vocabulario, dimension = nucleo.wte.weight.shape
    posiciones = nucleo.wpe.weight.shape[0]
    bloques = len(nucleo.h)
    cabezas = modelo.config.n_head
    intermedia = nucleo.h[0].mlp.c_fc.weight.shape[1]
    en_atencion = _contar_parametros(nucleo.h[0].attn)
    en_mlp = _contar_parametros(nucleo.h[0].mlp)
    en_embeddings = _contar_parametros(nucleo.wte)
    en_embeddings = en_embeddings + _contar_parametros(nucleo.wpe)
    por_cabeza = dimension // cabezas
    cajas = [
        ("tokens", "Tokens\n(vocabulario de\n" + f"{vocabulario:,}".replace(
            ",", ".") + ")", GRIS, "fuera"),
        ("embeddings", f"Embedding de\ntoken + posici\u00f3n\n{dimension} "
         f"n\u00fameros\n({_escribir_millones(en_embeddings)})", AZUL,
         "fuera"),
        ("normalizacion", "Normali-\nzaci\u00f3n", LINEA, "dentro"),
        ("atencion", f"Atenci\u00f3n\n{cabezas} cabezas\nde {por_cabeza}\n"
         f"({_escribir_millones(en_atencion)})", NARANJA, "dentro"),
        ("suma", "Suma", VERDE_AZULADO, "dentro"),
        ("normalizacion", "Normali-\nzaci\u00f3n", LINEA, "dentro"),
        ("mlp", f"MLP\n{dimension}\u2192{intermedia}\u2192{dimension}\n"
         f"({_escribir_millones(en_mlp)})", VIOLETA, "dentro"),
        ("suma", "Suma", VERDE_AZULADO, "dentro"),
        ("salida", f"Salida al\nvocabulario\n+ softmax", GRIS, "fuera"),
    ]
    ancho, separacion, base, alto = 1.25, 0.32, 0.30, 0.42
    with plt.rc_context(ESTILO):
        figura, ejes = plt.subplots(figsize=(12.5, 3.4))
        total = len(cajas) * (ancho + separacion)
        ejes.set_xlim(-0.2, total)
        ejes.set_ylim(-0.05, 1.12)
        ejes.set_axis_off()
        izquierdas = []
        for orden in range(len(cajas)):
            clave, texto, color, lugar = cajas[orden]
            izquierda = orden * (ancho + separacion)
            izquierdas.append(izquierda)
            marcada = clave == estamos_aca
            if estamos_aca == "bloques" and lugar == "dentro":
                marcada = True
            ejes.add_patch(FancyBboxPatch(
                (izquierda, base), ancho, alto, boxstyle="round,pad=0.02",
                facecolor=FONDO, edgecolor=color,
                linewidth=4.0 if marcada else 1.6,
            ))
            ejes.text(izquierda + ancho / 2, base + alto / 2, texto,
                      ha="center", va="center", fontsize=8.3, color=TINTA)
            if marcada:
                ejes.text(izquierda + ancho / 2, base - 0.12,
                          "estamos ac\u00e1", ha="center", fontsize=9,
                          fontweight="bold", color=TINTA)
            if orden < len(cajas) - 1:
                ejes.add_patch(FancyArrowPatch(
                    (izquierda + ancho + 0.02, base + alto / 2),
                    (izquierda + ancho + separacion - 0.02, base + alto / 2),
                    arrowstyle="-|>", mutation_scale=10, color=TINTA_SUAVE,
                    linewidth=1.2,
                ))
        inicio = izquierdas[2] - 0.12
        fin = izquierdas[7] + ancho + 0.12
        ejes.plot([inicio, inicio, fin, fin], [0.82, 0.88, 0.88, 0.82],
                  color=TINTA_SUAVE, linewidth=1.2)
        ejes.text((inicio + fin) / 2, 0.95,
                  f"un bloque; el modelo apila {bloques} iguales, "
                  "cada uno con sus propios pesos", ha="center",
                  fontsize=9, color=TINTA)
        ejes.set_title(f"GPT-2 en espa\u00f1ol, le\u00eddo del modelo: "
                       f"{bloques} bloques, hasta {posiciones} tokens")
        figura.tight_layout()
        plt.show()


def armar_panel_interactivo(
    funcion_de_escena,
    controles: Mapping,
) -> None:
    """Conecta una escena con sus controles.

    Primero dibuja la escena con los valores iniciales, como salida comun:
    esa version estatica se ve aunque los controles no funcionen (GitHub,
    PDF). Debajo quedan los controles y una segunda copia que se redibuja
    cada vez que se mueve un control.

    Args:
        funcion_de_escena: Funcion que dibuja; recibe un argumento por
            control, con el mismo nombre.
        controles: Nombre del argumento a control de ipywidgets.
    """
    valores_iniciales = {}
    for nombre in controles:
        valores_iniciales[nombre] = controles[nombre].value
    print("Escena inicial (est\u00e1tica):")
    funcion_de_escena(**valores_iniciales)
    salida = widgets.Output()

    def redibujar(cambio) -> None:
        """Vuelve a dibujar la escena con los valores actuales.

        Args:
            cambio: Aviso de ipywidgets; no se usa su contenido.
        """
        valores = {}
        for nombre in controles:
            valores[nombre] = controles[nombre].value
        with salida:
            clear_output(wait=True)
            funcion_de_escena(**valores)

    for nombre in controles:
        controles[nombre].observe(redibujar, names="value")
    fila_de_controles = widgets.HBox(list(controles.values()))
    display(widgets.VBox([
        widgets.HTML("<b>Con controles</b> (mov\u00e9 los valores):"),
        fila_de_controles,
        salida,
    ]))
