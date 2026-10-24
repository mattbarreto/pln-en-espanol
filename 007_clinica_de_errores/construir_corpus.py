"""Convierte el HTML crudo de Wikisource en corpus.jsonl (un cuento por línea)."""
import json, re
from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup

CARPETA = Path(__file__).parent
VOLUMENES = {
    "adulto": "Cuentos de amor de locura y de muerte",
    "infantil": "Cuentos de la selva para los niños",
}


def extraer_cuento(html):
    """Devuelve (párrafos, bloques_no_párrafo) del cuerpo del cuento."""
    sopa = BeautifulSoup(html, "html.parser")
    for etiqueta in sopa(["style", "script"]):
        etiqueta.decompose()
    # La letra capital viene como imagen con la letra en el atributo alt.
    for imagen in sopa.find_all("img"):
        if len(imagen.get("alt", "")) == 1:
            imagen.replace_with(imagen["alt"])
    raiz = sopa.find("div", class_="prp-pages-output") or sopa
    parrafos, otros = [], []
    for bloque in raiz.find_all(["p", "div", "h2", "h3", "h4", "pre", "center", "table"]):
        if bloque.find(["p", "div", "table"]):
            continue
        texto = re.sub(r"\s+", " ", bloque.get_text("")).strip()
        if not texto:
            continue
        (parrafos if bloque.name == "p" else otros).append(texto)
    return parrafos, otros


if __name__ == "__main__":
    filas = []
    for ruta in sorted((CARPETA / "crudo").glob("*.json")):
        crudo = json.loads(ruta.read_text(encoding="utf-8"))
        parrafos, otros = extraer_cuento(crudo["html"])
        texto = "\n\n".join(parrafos)
        filas.append({
            "id": ruta.stem,
            "titulo": crudo["titulo"],
            "autor": "Horacio Quiroga",
            "volumen": VOLUMENES[crudo["volumen"]],
            "grupo": crudo["volumen"],
            "fuente": "Wikisource",
            "fuente_url": "https://es.wikisource.org/wiki/" + quote(crudo["titulo"].replace(" ", "_")),
            "revid": crudo["revid"],
            "palabras": len(texto.split()),
            "texto": texto,
        })
    with open(CARPETA / "corpus.jsonl", "w", encoding="utf-8") as salida:
        for fila in filas:
            salida.write(json.dumps(fila, ensure_ascii=False) + "\n")
    for f in filas:
        print(f"{f['id']:10} {f['titulo'][:34]:34} {f['palabras']:5}  {f['texto'][:30]!r} ... {f['texto'][-25:]!r}")
