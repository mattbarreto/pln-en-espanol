"""
Reconstruye el corpus de párrafos a partir de los archivos de datos/blog/.

Los archivos de blog/ tienen extensión .txt pero NO son texto: son objetos
pickle de Python, cada uno con un único string que contiene todos los textos
de ese año pegados uno detrás de otro.

Al pegarlos se borraron los saltos de línea, pero quedó una marca:
donde terminaba un párrafo hay un punto seguido de mayúscula SIN espacio.
Ese es el corte que usamos para reconstruir los párrafos.

Produce datos/corpus.jsonl con un párrafo por línea.
"""

# pickle: para abrir los archivos de blog/, que son objetos serializados.
import pickle

# re: expresiones regulares, para encontrar la marca de corte de párrafo.
import re

# json: para escribir el corpus, una línea por párrafo.
import json

# pathlib: para armar rutas de archivo que funcionen en cualquier sistema.
from pathlib import Path


# La carpeta donde está este archivo.
AQUI = Path(__file__).parent

# De dónde leemos y adónde escribimos.
ORIGEN = AQUI / "blog"
DESTINO = AQUI / "corpus.jsonl"

# La marca de corte de párrafo.
#   (?<=...)  mirá que ANTES del punto haya una letra, un número o un cierre
#   \.        el punto
#   (?=...)   mirá que DESPUÉS venga una mayúscula, una apertura o una comilla
# El punto NO se consume: por eso cada párrafo conserva su puntuación final.
MARCA_DE_PARRAFO = r'(?<=[a-záéíóúñ0-9\)\!\?\»"])\.(?=[A-ZÁÉÍÓÚÑ¿«"])'


def leer_anio(ruta):
    """Abre un archivo de blog/ y devuelve su texto."""
    archivo = open(ruta, "rb")
    texto = pickle.load(archivo)
    archivo.close()
    return texto


def partir_en_parrafos(texto):
    """Corta el texto de un año en párrafos y les devuelve el punto final."""
    partes = re.split(MARCA_DE_PARRAFO, texto)
    parrafos = []
    for parte in partes:
        limpio = parte.strip()
        if len(limpio) < 2:
            continue
        if not limpio.endswith((".", "!", "?", "…", "»", '"')):
            limpio = limpio + "."
        parrafos.append(limpio)
    return parrafos


def main():
    registros = []
    for ruta in sorted(ORIGEN.glob("*.txt")):
        anio = int(ruta.stem)
        texto = leer_anio(ruta)
        parrafos = partir_en_parrafos(texto)
        numero = 0
        for parrafo in parrafos:
            numero = numero + 1
            registro = {
                "anio": anio,
                "parrafo": numero,
                "caracteres": len(parrafo),
                "texto": parrafo,
            }
            registros.append(registro)

    salida = open(DESTINO, "w", encoding="utf-8")
    for registro in registros:
        linea = json.dumps(registro, ensure_ascii=False)
        salida.write(linea + "\n")
    salida.close()

    print(f"párrafos escritos: {len(registros)}")
    print(f"archivo: {DESTINO}")


if __name__ == "__main__":
    main()
