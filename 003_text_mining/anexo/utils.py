# -*- coding: utf-8 -*-
"""El proceso completo de la unidad, en un solo archivo.

Esto que estás leyendo es lo mismo que hiciste en los cuatro cuadernos del
práctico más el anexo, junto y en orden. Se lee de arriba a abajo y cada
función es una etapa:

    1. del archivo al corpus         cargar_anio, cortar_en_parrafos, armar_corpus
    2. del corpus al texto limpio    limpiar, cargar_palabras_vacias
    3. del texto limpio a la cuenta  agrupar_por_anio, frecuencias_de
    4. de la cuenta a la comparación contar_con_contenido, conteos_de_contenido,
                                     caracteristicas_de
    5. de la comparación al texto    concordancia_de
    6. del texto a un signo          cargar_lexicon, puntuar_texto

Las cuatro primeras etapas van del texto al número. La quinta va en la otra
dirección: es la que te devuelve al texto para ver si el número decía lo que
parecía decir. La sexta le pone un signo, y solo se puede leer junto con la
quinta.

Las funciones son las mismas que están definidas en el cuaderno
00_el_proceso_completo.ipynb, y el cuaderno tiene una celda de aserciones que
lo comprueba. Si tocás una de las dos, esa celda falla.
"""
import pathlib
import pickle
import re
from collections import Counter

import pandas as pd

# El corpus vive en el práctico. El anexo no lo duplica: lo lee de ahí.
CARPETA_DATOS = pathlib.Path("..") / "practico" / "datos"

# Los datos propios del anexo.
CARPETA_ANEXO = pathlib.Path("datos")

# Los signos que saca limpiar(). No incluye números: en este corpus los años son datos.
SIGNOS = "¡!\"#$%&'()*+,-./:;<=>¿?@[\\]^_`{|}~«»…—–“”‘’"
PATRON_DE_SIGNOS = "[" + re.escape(SIGNOS) + "]"

# Los negadores dan vuelta el signo de lo que viene después.
NEGADORES = ["no", "nunca", "nada", "ni", "jamás", "tampoco"]

# Cuántas palabras hacia atrás se busca un negador.
VENTANA_DE_NEGACION = 3


# ══════════════════════════════════════════════════ 1 · del archivo al corpus

def cargar_anio(anio):
    """Lee uno de los archivos de blog/. No son texto: son objetos pickle."""
    ruta = CARPETA_DATOS / "blog" / (str(anio) + ".txt")
    archivo = open(ruta, "rb")
    texto = pickle.load(archivo)
    archivo.close()
    return texto


def cortar_en_parrafos(texto):
    """Corta el bloque de un año en párrafos, donde un punto pega con una mayúscula."""
    # El punto NO se consume: por eso cada párrafo conserva su puntuación final.
    marca = r'(?<=[a-záéíóúñ0-9\)\!\?\»"])\.(?=[A-ZÁÉÍÓÚÑ¿«"])'
    partes = re.split(marca, texto)

    parrafos = []
    for parte in partes:
        limpio = parte.strip()
        if len(limpio) < 2:
            continue
        if not limpio.endswith((".", "!", "?", "…", "»", '"')):
            limpio = limpio + "."
        parrafos.append(limpio)
    return parrafos


def armar_corpus(anios):
    """Devuelve una tabla con un párrafo por fila, y de qué año es cada uno."""
    filas = []
    for anio in anios:
        texto_del_anio = cargar_anio(anio)
        for parrafo in cortar_en_parrafos(texto_del_anio):
            filas.append({"anio": anio, "texto": parrafo})
    return pd.DataFrame(filas)


# ════════════════════════════════════════════ 2 · del corpus al texto limpio

def limpiar(texto):
    """Pasa a minúsculas, saca la puntuación y unifica los espacios."""
    en_minusculas = texto.lower()
    sin_signos = re.sub(PATRON_DE_SIGNOS, " ", en_minusculas)
    sin_espacios_de_mas = re.sub(r"\s+", " ", sin_signos)
    return sin_espacios_de_mas.strip()


def cargar_palabras_vacias():
    """La lista de palabras vacías. En el práctico se carga una vez por cuaderno."""
    ruta = CARPETA_DATOS / "stopwords_es.txt"
    archivo = open(ruta, encoding="utf-8")
    contenido = archivo.read()
    archivo.close()
    return contenido.split()


# ═════════════════════════════════════════ 3 · del texto limpio a la cuenta

def agrupar_por_anio(corpus):
    """Junta las palabras limpias de cada año. Devuelve un diccionario por año."""
    palabras_por_anio = {}
    for anio in sorted(corpus["anio"].unique()):
        parrafos_del_anio = corpus[corpus["anio"] == anio]
        texto_del_anio = " ".join(parrafos_del_anio["texto_limpio"])
        palabras_por_anio[anio] = texto_del_anio.split()
    return palabras_por_anio


def frecuencias_de(palabras_por_anio, palabra_buscada):
    """Para cada año: cuántas veces aparece la palabra, cruda y por cada 10.000."""
    filas = []
    for anio in sorted(palabras_por_anio):
        palabras = palabras_por_anio[anio]
        veces = palabras.count(palabra_buscada)
        por_diez_mil = 10000 * veces / len(palabras)
        filas.append({"anio": anio, "veces": veces, "por_10k": round(por_diez_mil, 2)})
    return pd.DataFrame(filas)


# ══════════════════════════════════════════ 4 · de la cuenta a la comparación

def contar_con_contenido(palabras, palabras_vacias, largo_minimo=3):
    """Cuenta las palabras de un año, salteando las vacías y las muy cortas."""
    conteo = Counter()
    for palabra in palabras:
        if palabra in palabras_vacias:
            continue
        if len(palabra) < largo_minimo:
            continue
        conteo[palabra] = conteo[palabra] + 1
    return conteo


def conteos_de_contenido(palabras_por_anio, palabras_vacias):
    """Aplica contar_con_contenido a los doce años.

    Es el paso que en el cuaderno ocupa una celda. Devuelve un diccionario con
    los conteos de cada año y con los totales, que es lo que necesita
    caracteristicas_de.
    """
    conteos = {}
    totales = {}
    for anio in palabras_por_anio:
        conteo_del_anio = contar_con_contenido(palabras_por_anio[anio], palabras_vacias)
        conteos[anio] = conteo_del_anio
        totales[anio] = sum(conteo_del_anio.values())
    return {"conteos": conteos, "totales": totales}


def caracteristicas_de(conteos_por_anio, totales, anio_elegido,
                       minimo_de_apariciones=10, cuantas=10):
    """Qué palabras distinguen a un año del resto del corpus.

    Es la medida que la lingüística de corpus llama keyness: compara la
    frecuencia relativa de cada palabra en un año contra la del resto juntos.

    En el práctico esta función está escrita dos veces: como
    palabras_caracteristicas en el cuaderno 02 y como caracteristicas_de en el
    03. Son la misma operación sobre datos armados de dos maneras distintas.
    """
    conteo_del_resto = Counter()
    total_del_resto = 0
    for anio in conteos_por_anio:
        if anio == anio_elegido:
            continue
        conteo_del_resto.update(conteos_por_anio[anio])
        total_del_resto = total_del_resto + totales[anio]

    filas = []
    for palabra in conteos_por_anio[anio_elegido]:
        veces = conteos_por_anio[anio_elegido][palabra]
        if veces < minimo_de_apariciones:
            continue
        aca = 10000 * veces / totales[anio_elegido]
        alla = 10000 * conteo_del_resto[palabra] / total_del_resto
        # El 0,5 evita dividir por cero cuando la palabra no está en el resto.
        filas.append({"palabra": palabra, "veces": veces,
                      "por_10k_este_anio": round(aca, 1),
                      "por_10k_el_resto": round(alla, 1),
                      "cuantas_veces_mas": round(aca / (alla + 0.5), 1)})

    tabla = pd.DataFrame(filas)
    tabla = tabla.sort_values(by="cuantas_veces_mas", ascending=False)
    return tabla.head(cuantas).reset_index(drop=True)


# ═══════════════════════════════════════════ 5 · de la comparación al texto

def concordancia_de(corpus, termino, ventana=45):
    """Todas las apariciones de un término, con su cotexto a cada lado.

    El término puede ser una palabra, un bigrama o un trigrama.

    Busca sobre el texto ORIGINAL, no sobre el limpio: la limpieza destruye
    justamente la puntuación y las mayúsculas que hacen legible una cita.
    """
    patron = r"\b" + re.escape(termino.lower()) + r"\b"

    filas = []
    for fila in corpus.itertuples():
        for hallazgo in re.finditer(patron, fila.texto.lower()):
            desde = hallazgo.start()
            hasta = hallazgo.end()
            filas.append({
                "anio": fila.anio,
                "izquierda": fila.texto[max(0, desde - ventana):desde],
                "nodo": "[" + fila.texto[desde:hasta] + "]",
                "derecha": fila.texto[hasta:hasta + ventana],
            })
    return pd.DataFrame(filas)


# ══════════════════════════════════════════════ 6 · del texto a un signo

def cargar_lexicon():
    """El lexicón afectivo de la cátedra, como diccionario palabra -> polaridad.

    Las líneas que empiezan con # son la documentación del archivo: quién lo
    armó, con qué criterio y qué límites tiene. Conviene leerlas.
    """
    ruta = CARPETA_ANEXO / "lexicon_afectivo_es.csv"
    lexicon = pd.read_csv(ruta, comment="#")

    polaridad_de_palabra = {}
    for fila in lexicon.itertuples():
        polaridad_de_palabra[fila.palabra] = fila.polaridad
    return polaridad_de_palabra


def puntuar_texto(texto_limpio, polaridad_de_palabra, con_negacion=True):
    """Suma la polaridad de las palabras del texto que están en el lexicón.

    Recibe el lexicón como diccionario: así se puede correr la misma función con
    dos lexicones distintos y comparar.

    Devuelve un diccionario con la suma, cuántas palabras afectivas encontró y
    cuántas palabras tiene el texto en total. Ojo con la suma en cero: puede
    querer decir "neutral" o puede querer decir "no vi ninguna palabra".
    """
    palabras = texto_limpio.split()
    suma = 0
    afectivas = 0
    posicion = 0

    for palabra in palabras:
        if palabra in polaridad_de_palabra:
            valor = polaridad_de_palabra[palabra]
            if con_negacion:
                desde = max(0, posicion - VENTANA_DE_NEGACION)
                for anterior in palabras[desde:posicion]:
                    if anterior in NEGADORES:
                        valor = -valor
                        break
            suma = suma + valor
            afectivas = afectivas + 1
        posicion = posicion + 1

    return {"suma": suma, "afectivas": afectivas, "palabras": len(palabras)}
