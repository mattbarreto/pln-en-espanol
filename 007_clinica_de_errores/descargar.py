"""Descarga el HTML de cada cuento desde es.wikisource.org (una vez) y lo guarda en crudo/."""
import json, time, urllib.request, urllib.parse
from pathlib import Path

API = "https://es.wikisource.org/w/api.php"

ADULTO = ["A la deriva", "El alambre de púa", "El almohadón de pluma", "El infierno artificial",
          "El perro rabioso", "El solitario", "La gallina degollada", "La insolación",
          "La meningitis y su sombra", "La miel silvestre", "La muerte de Isolda (Quiroga)",
          "Los buques suicidantes", "Los mensú", "Los ojos sombríos", "Los pescadores de vigas",
          "Nuestro primer cigarro", "Una estación de amor", "Yaguaí"]
SELVA = ["El loro pelado", "El paso del Yabebirí",
         "Historia de dos cachorros de coatí y de dos cachorros de hombre", "La abeja haragana",
         "La gama ciega", "La guerra de los yacarés", "La tortuga gigante",
         "Las medias de los flamencos"]


def pedir(**parametros):
    parametros["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(parametros)
    pedido = urllib.request.Request(url, headers={"User-Agent": "corpus-quiroga/1.0 (uso educativo)"})
    for intento in range(5):
        try:
            time.sleep(1.5)
            return json.load(urllib.request.urlopen(pedido, timeout=60))
        except Exception as error:
            ultimo = error
            time.sleep(5 * (intento + 1))
    raise ultimo


carpeta = Path(__file__).parent / "crudo"
for volumen, titulos in (("adulto", ADULTO), ("infantil", SELVA)):
    for numero, titulo in enumerate(titulos, start=1):
        destino = carpeta / f"{volumen}_{numero:02d}.json"
        if destino.exists():
            continue
        respuesta = pedir(action="parse", page=titulo, prop="text|revid", redirects=1)
        pagina = respuesta["parse"]
        destino.write_text(json.dumps({"volumen": volumen, "titulo_pedido": titulo,
                                       "titulo": pagina["title"], "revid": pagina["revid"],
                                       "html": pagina["text"]["*"]}, ensure_ascii=False),
                           encoding="utf-8")
        print("ok", destino.name, flush=True)
