"""Funciones visuales y comprobaciones de la unidad 011.

Las funciones reciben resultados ya calculados: muestran, pero no deciden ni
transforman los datos del analisis.

El codigo va en ASCII. Los rotulos que lee el estudiante llevan sus tildes
escapadas con la barra invertida y el codigo de la letra.
"""

from collections.abc import Mapping, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

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
            escrito = f"{valor:.2f}".replace("-", "\u2212")
            if valor >= 0:
                ejes.text(valor + holgura, posicion, escrito, va="center",
                          ha="left", fontsize=9, color=TINTA_SUAVE)
            else:
                ejes.text(valor - holgura, posicion, escrito, va="center",
                          ha="right", fontsize=9, color=TINTA_SUAVE)
        izquierda = minimo - 0.14 * tramo if minimo < 0 else 0.0
        ejes.set_xlim(izquierda, maximo + 0.14 * tramo)
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
                escrito = f"{valor:.2f}".replace("-", "\u2212")
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
    color: str = AZUL,
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
    color: str = AZUL,
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
