"""Arma datos/fragmentos.csv a partir de cuentos_latinoamericanos.csv.

Uso, desde la carpeta de la unidad:
    python datos/construir_fragmentos.py
    python datos/construir_fragmentos.py ruta/a/cuentos_latinoamericanos.csv

Qué hace:
    1. Elige 34 textos por su identificador en ciudadseva.com (lista TEXTOS_ELEGIDOS).
    2. Parte cada texto en oraciones y junta oraciones consecutivas hasta llegar
       a PALABRAS_MINIMAS palabras. Cada grupo es un fragmento.
    3. Guarda un fragmento por fila, con su procedencia.

Los textos originales vienen en una sola línea, sin párrafos. Por eso el corte
por oraciones es un criterio nuestro y no una división del autor.
"""

import re
import sys
from pathlib import Path

import pandas as pd

CARPETA_DE_DATOS = Path(__file__).resolve().parent
RUTA_POR_DEFECTO = CARPETA_DE_DATOS.parent.parent / "006_sintesis" / "datos" / "cuentos_latinoamericanos.csv"
RUTA_DE_SALIDA = CARPETA_DE_DATOS / "fragmentos.csv"

PREFIJO_DE_ENLACE = "https://ciudadseva.com/texto/"
PALABRAS_MINIMAS = 45

# Identificador final del enlace de cada texto elegido.
TEXTOS_ELEGIDOS = [
    "la-mosca-que-sonaba-que-era-un-aguila",
    "la-rana-que-queria-ser-una-rana-autentica",
    "la-jirafa-que-de-pronto-comprendio-que-todo-es-relativo",
    "la-jirafa",
    "la-boa",
    "el-rinoceronte-2",
    "una-plaza-en-el-cielo",
    "la-foto",
    "la-muerte-anderson",
    "el-suicida",
    "suicidio-2",
    "danza-macabra-iii",
    "la-melancolia-del-viajero",
    "romance-viejo",
    "noctilucas",
    "en-el-frente",
    "la-cocinera",
    "tres-cocineros-y-un-huevo-frito",
    "el-cocinero",
    "almuerzos",
    "literatura",
    "parabola-de-cervantes-y-de-quijote",
    "un-problema",
    "alguien-sonara",
    "traducciones",
    "del-perfecto-gobernante",
    "la-salvacion",
    "el-entierro-de-henri-christophe",
    "los-dos-reyes-y-los-dos-laberintos",
    "instrucciones-para-llorar",
    "instrucciones-para-subir-una-escalera",
    "conservacion-de-los-recuerdos",
    "soledad-mutis",
    "el-eclipse",
]


def partir_en_oraciones(texto):
    """Devuelve la lista de oraciones de un texto.

    Corta después de un punto, signo de cierre o puntos suspensivos cuando
    sigue un espacio. No es perfecto: 'Sr. Pérez' se corta mal.
    """
    texto = re.sub(r"\s+", " ", texto).strip()
    oraciones = re.split(r"(?<=[\.\?\!…])\s+(?=[¿¡\"«\-—A-ZÁÉÍÓÚÑ])", texto)
    return oraciones


def armar_fragmentos(texto):
    """Junta oraciones consecutivas hasta alcanzar PALABRAS_MINIMAS."""
    fragmentos = []
    grupo = []
    palabras_del_grupo = 0
    for oracion in partir_en_oraciones(texto):
        grupo.append(oracion)
        palabras_del_grupo = palabras_del_grupo + len(oracion.split())
        if palabras_del_grupo >= PALABRAS_MINIMAS:
            fragmentos.append(" ".join(grupo))
            grupo = []
            palabras_del_grupo = 0
    if grupo:
        if fragmentos and palabras_del_grupo < PALABRAS_MINIMAS / 2:
            fragmentos[-1] = fragmentos[-1] + " " + " ".join(grupo)
        else:
            fragmentos.append(" ".join(grupo))
    return fragmentos


def main():
    ruta_de_entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_POR_DEFECTO
    cuentos = pd.read_csv(ruta_de_entrada)
    cuentos["identificador"] = cuentos["link"].str.replace(PREFIJO_DE_ENLACE, "", regex=False)
    cuentos["identificador"] = cuentos["identificador"].str.strip("/")

    filas = []
    for identificador in TEXTOS_ELEGIDOS:
        coincidencias = cuentos[cuentos["identificador"] == identificador]
        if len(coincidencias) != 1:
            raise SystemExit(f"El texto '{identificador}' aparece {len(coincidencias)} veces; se esperaba 1.")
        cuento = coincidencias.iloc[0]
        numero = 0
        for fragmento in armar_fragmentos(cuento["text"]):
            numero = numero + 1
            filas.append(
                {
                    "id": f"{identificador}-{numero:02d}",
                    "texto": fragmento,
                    "autor": cuento["author"],
                    "titulo": cuento["title"],
                    "fuente": cuento["link"],
                    "palabras": len(fragmento.split()),
                }
            )

    tabla = pd.DataFrame(filas)
    tabla.to_csv(RUTA_DE_SALIDA, index=False, encoding="utf-8")
    print(f"{len(tabla)} fragmentos de {len(TEXTOS_ELEGIDOS)} textos guardados en {RUTA_DE_SALIDA.name}")
    print(tabla["palabras"].describe().round(1).to_string())


if __name__ == "__main__":
    main()
