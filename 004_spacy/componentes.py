"""
Componentes propios del pipeline, definidos en un archivo aparte.

Por qué acá y no en el cuaderno: cuando spaCy guarda un pipeline con to_disk(),
anota QUÉ componentes lo forman pero NO guarda su código. Al volver a cargarlo,
ese código tiene que estar disponible. Si vive en una celda de un cuaderno, hay
que acordarse de correr esa celda; si vive acá, alcanza con:

    import componentes
"""

# Language: para registrar los componentes dentro de spaCy.
from spacy.language import Language

# Doc: la clase del documento, para agregarle atributos propios.
from spacy.tokens import Doc


# Formas del voseo que el lematizador de spaCy no resuelve.
# La lista está incompleta a propósito: ampliarla es parte del trabajo.
CORRECCIONES_VOSEO = {
    "tenés": "tener",
    "sabés": "saber",
    "sos": "ser",
    "querés": "querer",
    "podés": "poder",
    "venís": "venir",
    "hacés": "hacer",
    "decís": "decir",
    "andá": "andar",
    "mirá": "mirar",
    "vení": "venir",
}


@Language.component("corrector_voseo")
def corrector_voseo(doc):
    """Reemplaza el lema de las formas del voseo por su infinitivo."""
    for token in doc:
        minuscula = token.text.lower()
        if minuscula in CORRECCIONES_VOSEO:
            token.lemma_ = CORRECCIONES_VOSEO[minuscula]
    return doc


# Registramos el atributo propio una sola vez, al importar el módulo.
# Después se lee y se escribe como doc._.personajes
if not Doc.has_extension("personajes"):
    Doc.set_extension("personajes", default=None)


@Language.component("detector_personajes")
def detector_personajes(doc):
    """Guarda en doc._.personajes los nombres marcados como PERSONAJE.

    No busca nada por su cuenta: usa las entidades que ya dejó el
    entity_ruler. Por eso este componente tiene que ir después de él.
    """
    encontrados = []
    for entidad in doc.ents:
        if entidad.label_ != "PERSONAJE":
            continue
        if entidad.text in encontrados:
            continue
        encontrados.append(entidad.text)
    doc._.personajes = encontrados
    return doc
