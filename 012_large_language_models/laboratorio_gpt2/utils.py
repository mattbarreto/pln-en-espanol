"""Experiencia visual del laboratorio GPT-2 (unidad de LLMs).

Este módulo NO contiene ningún algoritmo de la unidad: no tokeniza, no arma
bloques, no entrena ni genera. Solo dibuja. Recibe tablas, textos y números ya
calculados en el cuaderno y devuelve HTML o figuras.

Tres reglas de diseño:

1. Una paleta cálida y fija. Corpus, modelo base, modelo ajustado e
   intervención humana tienen cada uno su color en todo el cuaderno.
2. El color nunca va solo: cada actor lleva además un rótulo y una marca
   (■ ● ▲ ◆), y los tokens se separan con bordes y espacios.
3. Todo texto que viene del corpus o de una generación pasa por `escapar()`
   antes de entrar en HTML.
"""

import html
import io
import re

import matplotlib

matplotlib.use("Agg")  # figuras sin ventana: sirven también dentro de un hilo
from matplotlib.figure import Figure

# ─── Paleta ──────────────────────────────────────────────────────────────────
PAPEL = "#FBF5EA"        # fondo general, color de papel de libro
TARJETA = "#FFFDF8"      # fondo de cada panel
TINTA = "#2B2118"        # texto principal (marrón casi negro, no negro puro)
TINTA_SUAVE = "#6B5B4D"  # texto secundario
GRILLA = "#E6D9C3"       # líneas finas y bordes
AVISO_FONDO = "#FFF1CC"
AVISO_TINTA = "#5C4300"
ERROR_FONDO = "#FBDDD5"
ERROR_TINTA = "#7A2312"
OK_FONDO = "#DCEEE3"
OK_TINTA = "#1F5A3A"

COLOR_CORPUS = "#B8860B"     # mostaza oscura
COLOR_BASE = "#2F6F73"       # verde petróleo
COLOR_AJUSTADO = "#C8452B"   # terracota
COLOR_HUMANO = "#7A3E6E"     # ciruela

ACTORES = {
    "corpus": {"nombre": "Corpus", "color": COLOR_CORPUS, "marca": "■", "tinta": "#F6E7B4"},
    "base": {"nombre": "Modelo base", "color": COLOR_BASE, "marca": "●", "tinta": "#CFE5E3"},
    "ajustado": {"nombre": "Modelo ajustado", "color": COLOR_AJUSTADO, "marca": "▲", "tinta": "#F7D5CB"},
    "humano": {"nombre": "Intervención humana", "color": COLOR_HUMANO, "marca": "◆", "tinta": "#E8D3E3"},
}

# Tintas claras para colorear tokens (se repiten en ciclo). Texto siempre en TINTA.
TINTAS_DE_TOKENS = ["#F9D9C7", "#F6E7A6", "#CFE5DC", "#F4C9CF", "#D9D3F0", "#CDE3F0"]

FUENTE_TEXTO = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
FUENTE_UI = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
FUENTE_CODIGO = "ui-monospace, Menlo, Consolas, monospace"


def escapar(texto):
    """Convierte un texto cualquiera en texto seguro para meter dentro de HTML."""
    return html.escape(str(texto), quote=True)


def etiqueta_de_actor(actor):
    """Rótulo con marca y nombre: «▲ Modelo ajustado». Sirve sin ver el color."""
    datos = ACTORES[actor]
    return f"{datos['marca']} {datos['nombre']}"


def con_miles(número):
    """62904 → «62.904», como se escribe en español."""
    return f"{int(número):,}".replace(",", ".")


def en_porcentaje(proporción, decimales=1):
    """0.1234 → «12,3 %»."""
    return f"{proporción * 100:.{decimales}f}".replace(".", ",") + " %"


def con_coma(número, decimales=2):
    """3.14159 → «3,14»."""
    return f"{número:.{decimales}f}".replace(".", ",")


# ─── HTML básico ─────────────────────────────────────────────────────────────
def html_envoltorio(contenido):
    """Pone el contenido sobre fondo de papel, con la fuente de la unidad."""
    return (
        f"<div style=\"background:{PAPEL};color:{TINTA};font-family:{FUENTE_UI};"
        f"padding:10px 12px;border-radius:8px;line-height:1.45;\">{contenido}</div>"
    )


def html_tarjeta(título, cuerpo_html, actor=None):
    """Panel con borde izquierdo del color del actor. El cuerpo ya viene en HTML seguro."""
    color = ACTORES[actor]["color"] if actor else GRILLA
    rótulo = f"{escapar(etiqueta_de_actor(actor))} · " if actor else ""
    return html_envoltorio(
        f"<div style=\"background:{TARJETA};border:1px solid {GRILLA};border-left:6px solid {color};"
        f"border-radius:6px;padding:10px 14px;\">"
        f"<div style=\"font-weight:600;color:{TINTA};margin-bottom:6px;\">{rótulo}{escapar(título)}</div>"
        f"{cuerpo_html}</div>"
    )


def html_aviso(texto, tipo="aviso"):
    """Banda de aviso con texto (no solo color). tipo: aviso, error u ok."""
    fondos = {"aviso": (AVISO_FONDO, AVISO_TINTA, "Atención"),
              "error": (ERROR_FONDO, ERROR_TINTA, "Error"),
              "ok": (OK_FONDO, OK_TINTA, "Listo")}
    fondo, tinta, rótulo = fondos[tipo]
    return (
        f"<div style=\"background:{fondo};color:{tinta};border-radius:6px;padding:8px 12px;"
        f"font-family:{FUENTE_UI};margin:4px 0;\"><b>{rótulo}.</b> {escapar(texto)}</div>"
    )


ESTADOS = {
    "pendiente": ("#EFE6D2", TINTA_SUAVE, "Pendiente"),
    "ejecutando": (AVISO_FONDO, AVISO_TINTA, "Ejecutando"),
    "completado": (OK_FONDO, OK_TINTA, "Completado"),
    "falló": (ERROR_FONDO, ERROR_TINTA, "Falló"),
    "detenido": ("#E8D3E3", COLOR_HUMANO, "Detenido"),
}


def html_estado(estado, detalle=""):
    """Etiqueta de estado: pendiente, ejecutando, completado, falló o detenido."""
    fondo, tinta, rótulo = ESTADOS[estado]
    extra = f" <span style=\"font-weight:400;\">{escapar(detalle)}</span>" if detalle else ""
    return (
        f"<span style=\"display:inline-block;background:{fondo};color:{tinta};border-radius:12px;"
        f"padding:3px 12px;font-family:{FUENTE_UI};font-weight:600;\">{rótulo}{extra}</span>"
    )


def html_texto_con_continuación(entrada, continuación, actor):
    """Muestra una generación separando lo que escribiste de lo que agregó el modelo."""
    color = ACTORES[actor]["color"]
    tinta = ACTORES[actor]["tinta"]
    estilo_texto = f"font-family:{FUENTE_TEXTO};font-size:1.05em;white-space:pre-wrap;"
    return html_envoltorio(
        f"<div style=\"background:{TARJETA};border:1px solid {GRILLA};border-radius:6px;padding:10px 14px;\">"
        f"<div style=\"font-size:.8em;color:{TINTA_SUAVE};margin-bottom:2px;\">ENTRADA (la escribiste vos)</div>"
        f"<div style=\"{estilo_texto}color:{TINTA_SUAVE};border-bottom:1px dashed {GRILLA};padding-bottom:6px;\">"
        f"{escapar(entrada)}</div>"
        f"<div style=\"font-size:.8em;color:{color};margin:6px 0 2px;font-weight:600;\">"
        f"CONTINUACIÓN · {escapar(etiqueta_de_actor(actor))}</div>"
        f"<div style=\"{estilo_texto}background:{tinta};border-left:4px solid {color};padding:6px 10px;\">"
        f"{escapar(continuación)}</div></div>"
    )


def texto_con_espacios_visibles(texto):
    """Devuelve HTML donde se ven los espacios (·), los saltos de línea (↵) y las tabulaciones (⇥)."""
    partes = []
    for carácter in texto:
        if carácter == " ":
            partes.append(f"<span style=\"color:{TINTA_SUAVE};opacity:.6;\">·</span>")
        elif carácter == "\n":
            partes.append(f"<span style=\"color:{COLOR_HUMANO};\">↵</span>\n")
        elif carácter == "\t":
            partes.append(f"<span style=\"color:{COLOR_HUMANO};\">⇥</span>")
        else:
            partes.append(escapar(carácter))
    return (
        f"<pre style=\"font-family:{FUENTE_CODIGO};white-space:pre-wrap;background:{TARJETA};"
        f"border:1px solid {GRILLA};border-radius:6px;padding:8px 12px;color:{TINTA};margin:0;\">"
        + "".join(partes) + "</pre>"
    )


def pieza_visible(pieza):
    """Texto de un token listo para mostrar. Los bytes sueltos de un carácter partido se marcan."""
    if "�" in pieza:
        return "‹bytes›"
    return pieza.replace("\n", "↵").replace(" ", "·").replace("\t", "⇥")


def html_tokens(piezas, ids=None, resaltar=None):
    """Tokens como fichas coloreadas. `piezas` es el texto de cada token, `ids` sus identificadores.

    `resaltar` es un conjunto de posiciones que se marcan con borde grueso (por ejemplo, el objetivo).
    Cada ficha tiene borde propio y se numera, así no hace falta distinguir colores.
    """
    resaltar = resaltar or set()
    fichas = []
    for posición, pieza in enumerate(piezas):
        fondo = TINTAS_DE_TOKENS[posición % len(TINTAS_DE_TOKENS)]
        borde = f"2px solid {COLOR_AJUSTADO}" if posición in resaltar else f"1px solid {GRILLA}"
        identificador = (
            f"<div style=\"font-family:{FUENTE_CODIGO};font-size:.7em;color:{TINTA_SUAVE};\">{ids[posición]}</div>"
            if ids is not None else ""
        )
        fichas.append(
            f"<span style=\"display:inline-block;text-align:center;margin:2px;padding:2px 6px;"
            f"background:{fondo};border:{borde};border-radius:5px;color:{TINTA};vertical-align:top;\">"
            f"<div style=\"font-family:{FUENTE_CODIGO};\">{escapar(pieza_visible(pieza))}</div>{identificador}</span>"
        )
    return html_envoltorio("".join(fichas))


def html_tabla(columnas, filas, resaltar_fila=None):
    """Tabla simple. `filas` es una lista de listas; cada celda se escapa."""
    estilo_celda = f"padding:4px 10px;border-bottom:1px solid {GRILLA};text-align:left;"
    cabecera = "".join(
        f"<th style=\"{estilo_celda}background:{PAPEL};color:{TINTA_SUAVE};font-weight:600;\">{escapar(c)}</th>"
        for c in columnas
    )
    cuerpo = []
    for posición, fila in enumerate(filas):
        fondo = AVISO_FONDO if posición == resaltar_fila else TARJETA
        celdas = "".join(f"<td style=\"{estilo_celda}\">{escapar(valor)}</td>" for valor in fila)
        cuerpo.append(f"<tr style=\"background:{fondo};\">{celdas}</tr>")
    return html_envoltorio(
        f"<table style=\"border-collapse:collapse;width:100%;font-size:.92em;\">"
        f"<thead><tr>{cabecera}</tr></thead><tbody>{''.join(cuerpo)}</tbody></table>"
    )


# ─── Ayuda junto a los controles y comparación de textos ────────────────────
# Clases de control: la persona tiene que saber si mueve el experimento, su vista, los datos o solo anota.
# Cada etiqueta lleva su nombre escrito: el color acompaña, no reemplaza.
TIPOS_DE_CONTROL = {
    "experimento": ("Experimento", AVISO_FONDO, AVISO_TINTA, "cambia lo que se genera o se ajusta"),
    "vista": ("Vista", "#EFE6D2", TINTA_SUAVE, "solo cambia cómo se ve; el experimento queda igual"),
    "datos": ("Datos", OK_FONDO, OK_TINTA, "cambia los datos que se preparan"),
    "registro": ("Registro", "#E8D3E3", COLOR_HUMANO, "solo anota lo que pensás; no cambia el experimento"),
}


def html_ayuda_de_control(tipo, ayuda, prueba):
    """Línea breve bajo un control: su tipo (Experimento, Vista, Datos o Registro), qué hace y una propuesta para probarlo."""
    etiqueta = ""
    if tipo:
        rótulo, fondo, tinta, significado = TIPOS_DE_CONTROL[tipo]
        etiqueta = (
            f"<span title=\"{escapar(significado)}\" style=\"display:inline-block;background:{fondo};color:{tinta};"
            f"border-radius:10px;padding:0 8px;margin-right:6px;font-weight:600;\">{escapar(rótulo)}</span>"
        )
    partes = [escapar(ayuda)] if ayuda else []
    if prueba:
        partes.append(f"<i>Probá:</i> {escapar(prueba)}")
    return (
        f"<div style=\"font-family:{FUENTE_UI};font-size:.85em;color:{TINTA_SUAVE};line-height:1.4;"
        f"margin:-2px 0 8px 6px;\">{etiqueta}{' '.join(partes)}</div>"
    )


def html_comparación_de_textos(pares, largo_máximo=260):
    """Pares (antes, después) uno debajo del otro, con espacios y saltos de línea visibles.

    Sirve para ver qué hace una transformación de texto antes de aceptarla. Cada fragmento se recorta
    a `largo_máximo` caracteres y se avisa si se recortó.
    """
    if not pares:
        return html_aviso("Esta limpieza no cambia nada en este documento.")
    bloques = []
    for número, (antes, después) in enumerate(pares, start=1):
        recortes = ""
        if len(antes) > largo_máximo or len(después) > largo_máximo:
            recortes = f"<div style=\"font-size:.8em;color:{TINTA_SUAVE};\">(fragmentos recortados a {largo_máximo} caracteres)</div>"
        bloques.append(
            f"<div style=\"font-family:{FUENTE_UI};margin:6px 0;\">"
            f"<div style=\"font-weight:600;color:{TINTA_SUAVE};\">Cambio {número} · antes</div>"
            f"{texto_con_espacios_visibles(antes[:largo_máximo])}"
            f"<div style=\"font-weight:600;color:{COLOR_AJUSTADO};margin-top:4px;\">Cambio {número} · después</div>"
            f"{texto_con_espacios_visibles(después[:largo_máximo])}{recortes}</div>"
        )
    return html_envoltorio("".join(bloques))


# ─── Figuras ─────────────────────────────────────────────────────────────────
def nueva_figura(ancho=8.0, alto=3.6):
    """Figura sin pyplot (segura dentro de un hilo) con el estilo de la unidad."""
    figura = Figure(figsize=(ancho, alto), dpi=110, facecolor=PAPEL)
    eje = figura.subplots()
    eje.set_facecolor(TARJETA)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eje.spines[lado].set_color(GRILLA)
    eje.tick_params(colors=TINTA_SUAVE)
    eje.grid(True, color=GRILLA, linewidth=0.7, alpha=0.8)
    eje.set_axisbelow(True)
    eje.xaxis.label.set_color(TINTA_SUAVE)
    eje.yaxis.label.set_color(TINTA_SUAVE)
    return figura, eje


def figura_a_png(figura):
    """Convierte una figura en bytes PNG, para ponerla en un widget Image."""
    memoria = io.BytesIO()
    figura.savefig(memoria, format="png", facecolor=figura.get_facecolor(), bbox_inches="tight")
    return memoria.getvalue()


def suavizar(valores, ventana):
    """Media móvil simple. Con ventana 1 devuelve los valores sin tocar."""
    if ventana <= 1 or len(valores) == 0:
        return list(valores)
    suavizados = []
    for i in range(len(valores)):
        tramo = valores[max(0, i - ventana + 1): i + 1]
        suavizados.append(sum(tramo) / len(tramo))
    return suavizados


def figura_de_pérdidas(pasos_entrenamiento, pérdidas_entrenamiento, pasos_validación=(), pérdidas_validación=(),
                       ventana=1, título="Pérdida durante el ajuste"):
    """Curvas de pérdida. Valores originales en trazo fino; suavizado (si hay) en trazo grueso."""
    figura, eje = nueva_figura()
    eje.set_title(título, loc="left", color=TINTA, fontsize=11, fontweight="bold")
    eje.set_xlabel("Paso de actualización")
    eje.set_ylabel("Pérdida media por token (nats)")
    if len(pasos_entrenamiento):
        con_suavizado = ventana > 1
        eje.plot(pasos_entrenamiento, pérdidas_entrenamiento, color=COLOR_AJUSTADO,
                 alpha=0.35 if con_suavizado else 1.0, linewidth=1.0,
                 label="▲ Entrenamiento (valores originales)")
        if con_suavizado:
            eje.plot(pasos_entrenamiento, suavizar(pérdidas_entrenamiento, ventana), color=COLOR_AJUSTADO,
                     linewidth=2.4, label=f"▲ Entrenamiento (media móvil de {ventana})")
    if len(pasos_validación):
        eje.plot(pasos_validación, pérdidas_validación, color=COLOR_BASE, linewidth=2.0, marker="o",
                 markersize=5, label="● Validación (conjunto fijo)")
    if len(pasos_entrenamiento) or len(pasos_validación):
        eje.legend(frameon=False, labelcolor=TINTA, fontsize=9)
    else:
        eje.text(0.5, 0.5, "Todavía no hay pasos", transform=eje.transAxes, ha="center", color=TINTA_SUAVE)
    return figura


def figura_de_participación(nombres, tamaños, unidad="tokens", título="Qué tanto pesa cada documento"):
    """Barras horizontales con la participación de cada documento en el corpus."""
    total = sum(tamaños) or 1
    figura, eje = nueva_figura(8.0, max(2.0, 0.34 * len(nombres) + 1.2))
    posiciones = list(range(len(nombres)))
    eje.barh(posiciones, [t / total * 100 for t in tamaños], color=COLOR_CORPUS, edgecolor=TINTA, linewidth=0.5)
    eje.set_yticks(posiciones)
    eje.set_yticklabels(nombres, color=TINTA, fontsize=9)
    eje.invert_yaxis()
    eje.set_xlabel(f"Participación en el total de {unidad} (%)")
    eje.set_title(título, loc="left", color=TINTA, fontsize=11, fontweight="bold")
    eje.grid(False, axis="y")
    for i, t in enumerate(tamaños):
        eje.text(t / total * 100, i, f" {con_miles(t)} · {en_porcentaje(t / total)}", va="center", color=TINTA_SUAVE, fontsize=8)
    return figura


def figura_de_candidatos(paneles, título="Candidatos para el siguiente token"):
    """Barras de los principales candidatos.

    `paneles` es una lista de diccionarios con: actor, candidatos (lista de
    (texto, probabilidad_original, probabilidad_transformada)), masa_mostrada_original y
    masa_mostrada_transformada. Muestra las DOS distribuciones y avisa cuánto queda fuera.
    """
    figura = Figure(figsize=(8.0, 0.5 + 3.2 * len(paneles)), dpi=110, facecolor=PAPEL)
    ejes = figura.subplots(len(paneles), 1, squeeze=False)[:, 0]
    for eje, panel in zip(ejes, paneles):
        datos = ACTORES[panel["actor"]]
        candidatos = panel["candidatos"]
        eje.set_facecolor(TARJETA)
        for lado in ("top", "right"):
            eje.spines[lado].set_visible(False)
        posiciones = list(range(len(candidatos)))
        altura = 0.38
        eje.barh([p - altura / 2 for p in posiciones], [c[1] for c in candidatos], height=altura,
                 color=datos["color"], alpha=0.45, edgecolor=TINTA, linewidth=0.5,
                 label="Distribución original del modelo")
        eje.barh([p + altura / 2 for p in posiciones], [c[2] for c in candidatos], height=altura,
                 color=datos["color"], edgecolor=TINTA, linewidth=0.5, hatch="//",
                 label="Después de temperatura y filtros")
        eje.set_yticks(posiciones)
        eje.set_yticklabels([pieza_visible(c[0]) for c in candidatos], fontfamily="monospace", color=TINTA)
        eje.invert_yaxis()
        eje.set_xlabel("Probabilidad", color=TINTA_SUAVE)
        resto_original = max(0.0, 1 - panel["masa_mostrada_original"])
        resto_transformada = max(0.0, 1 - panel["masa_mostrada_transformada"])
        eje.set_title(
            f"{etiqueta_de_actor(panel['actor'])} · {len(candidatos)} candidatos mostrados\n"
            f"Masa que cubren: {en_porcentaje(panel['masa_mostrada_original'])} (original) y {en_porcentaje(panel['masa_mostrada_transformada'])} (transformada). "
            f"Sin mostrar: {en_porcentaje(resto_original)} y {en_porcentaje(resto_transformada)}.",
            loc="left", color=TINTA, fontsize=8.5)
        eje.legend(frameon=False, fontsize=8, labelcolor=TINTA, loc="lower right")
        eje.tick_params(colors=TINTA_SUAVE)
    figura.suptitle(título, x=0.01, ha="left", color=TINTA, fontsize=11, fontweight="bold")
    figura.tight_layout()
    return figura


def limpiar_para_nombre_de_archivo(texto):
    """Deja un nombre apto para carpeta: minúsculas, guiones bajos, conserva tildes y eñes."""
    limpio = re.sub(r"[^\wáéíóúüñ-]+", "_", texto.strip().lower())
    return limpio.strip("_") or "experimento"


def figura_de_puntos_por_valor(tabla, columna_valor, columna_medida, título, etiqueta_y, actor="base"):
    """Cada muestra es un punto; la media de cada valor es una raya. Sirve para ver la dispersión.

    `tabla` es un DataFrame con una fila por muestra. Con pocas muestras, las medias engañan:
    por eso se dibujan todas las muestras y no solo el promedio.
    """
    figura, eje = nueva_figura()
    color = ACTORES[actor]["color"]
    valores = list(dict.fromkeys(tabla[columna_valor].tolist()))
    for posición, valor in enumerate(valores):
        medidas = tabla[tabla[columna_valor] == valor][columna_medida].tolist()
        desplazamientos = [(i - (len(medidas) - 1) / 2) * 0.06 for i in range(len(medidas))]
        eje.scatter([posición + d for d in desplazamientos], medidas, color=color, edgecolor=TINTA,
                    linewidth=0.5, s=38, zorder=3, label="Una muestra" if posición == 0 else None)
        media = sum(medidas) / len(medidas)
        eje.hlines(media, posición - 0.25, posición + 0.25, color=TINTA, linewidth=2.2, zorder=4,
                   label="Media de las muestras" if posición == 0 else None)
    eje.set_xticks(range(len(valores)))
    eje.set_xticklabels([str(v) for v in valores], color=TINTA)
    eje.set_xlabel(columna_valor)
    eje.set_ylabel(etiqueta_y)
    eje.set_title(título, loc="left", color=TINTA, fontsize=11, fontweight="bold")
    eje.legend(frameon=False, labelcolor=TINTA, fontsize=9)
    return figura


# ─── Pequeños ayudantes de presentación ──────────────────────────────────────
def filas_de_diccionario(diccionario):
    """Convierte {clave: valor} en una lista de filas [clave, valor] como texto, lista para html_tabla."""
    filas = []
    for clave, valor in diccionario.items():
        filas.append([str(clave), str(valor)])
    return filas


def html_avisos(avisos):
    """Une varios avisos en un solo bloque HTML."""
    bloque = ""
    for aviso in avisos:
        bloque += html_aviso(aviso)
    return bloque


def líneas_con_texto(texto):
    """Las líneas de un texto que no están vacías ni son solo espacios."""
    líneas = []
    for línea in texto.split("\n"):
        if línea.strip():
            líneas.append(línea)
    return líneas
