# -*- coding: utf-8 -*-
"""Prepara el corpus del cuaderno 04 a partir de los titulares electorales de 2019.

Uso docente. Los estudiantes NO corren este archivo: reciben los CSV ya hechos.

Qué hace:
    1. Baja de Hugging Face la partición elegida del dataset
       pysentimiento/spanish-targeted-sentiment-headlines (necesita Internet y pyarrow).
    2. Toma un recorte de CANTIDAD filas, con una semilla declarada.
    3. Escribe dos archivos en esta carpeta:
       - titulares_2019.csv: lo que ven los estudiantes (sin la etiqueta del corpus).
       - _referencia_corpus_original.csv: la etiqueta original, que el cuaderno solo
         lee en su bloque final, después de que el grupo anotó.

Uso:
    uv run --with pyarrow --with huggingface_hub python datos/preparar_titulares.py

El recorte es una selección para lectura y revisión. No garantiza representatividad
ni validez estadística. Si preferís elegir los titulares a mano, reemplazá
titulares_2019.csv conservando las columnas y no corras este script.

Procedencia del dataset: ver la ficha de datos del cuaderno 04. El repositorio de
Hugging Face no tiene ficha propia; la descripción está en el artículo
https://arxiv.org/abs/2208.13947 (la licencia indicada allí debe verificarse antes
de redistribuir los textos).
"""
import pathlib

import pandas as pd
from huggingface_hub import HfApi, hf_hub_download

REPOSITORIO = "pysentimiento/spanish-targeted-sentiment-headlines"
PARTICION = "test"
CANTIDAD = 48
SEMILLA = 2019

CARPETA = pathlib.Path(__file__).parent.resolve()
NOMBRES_DE_ETIQUETA = {0: "NEG", 1: "NEU", 2: "POS"}


def buscar_archivo_de_la_particion(particion):
    """Devuelve la ruta, dentro del repositorio, del parquet de una partición."""
    archivos = HfApi().list_repo_files(repo_id=REPOSITORIO, repo_type="dataset")
    candidatos = []
    for archivo in archivos:
        if archivo.startswith(f"data/{particion}-") and archivo.endswith(".parquet"):
            candidatos.append(archivo)
    if len(candidatos) != 1:
        raise RuntimeError(f"Se esperaba un parquet para '{particion}' y hay {len(candidatos)}: {candidatos}")
    return candidatos[0]


def main():
    nombre_en_el_repositorio = buscar_archivo_de_la_particion(PARTICION)
    ruta_local = hf_hub_download(
        repo_id=REPOSITORIO, repo_type="dataset", filename=nombre_en_el_repositorio
    )
    completo = pd.read_parquet(ruta_local)
    print(f"Partición '{PARTICION}': {len(completo)} filas, columnas {list(completo.columns)}")

    assert CANTIDAD <= len(completo), "El recorte pedido es mayor que la partición."
    recorte = completo.sample(n=CANTIDAD, random_state=SEMILLA)
    recorte = recorte.sort_values(by=["id_noticia", "target"]).reset_index(drop=True)

    recorte["id"] = [f"T{numero:02d}" for numero in range(1, len(recorte) + 1)]
    recorte["etiqueta_corpus"] = recorte["label"].map(NOMBRES_DE_ETIQUETA)
    assert recorte["etiqueta_corpus"].notna().all(), "Hay etiquetas del corpus que no se pudieron traducir."

    fuente = (
        f"{REPOSITORIO} (Hugging Face), partición {PARTICION}; titulares de medios "
        f"argentinos, elecciones presidenciales 2019; recorte de {CANTIDAD} filas, semilla {SEMILLA}"
    )
    corpus = pd.DataFrame({
        "id": recorte["id"],
        "texto": recorte["titulo"],
        "fuente": fuente,
        "id_documento": recorte["id_noticia"],
        "objeto_valorado": recorte["target"],
    })
    referencia = recorte[["id", "etiqueta_corpus"]]

    corpus.to_csv(CARPETA / "titulares_2019.csv", index=False, encoding="utf-8")
    referencia.to_csv(CARPETA / "_referencia_corpus_original.csv", index=False, encoding="utf-8")

    print(f"Filas del recorte: {len(corpus)}")
    print(f"Titulares distintos (id_documento): {corpus['id_documento'].nunique()}")
    print("Escritos: titulares_2019.csv y _referencia_corpus_original.csv")


if __name__ == "__main__":
    main()
