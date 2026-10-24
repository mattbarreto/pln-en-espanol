"""Plomería del laboratorio GPT-2 (unidad de LLMs): widgets, registro y archivos.

Este módulo NO contiene ningún algoritmo de la unidad: no tokeniza, no arma
bloques, no entrena, no evalúa ni genera. Esas funciones viven, a la vista, en
las celdas del cuaderno (las que llevan la marca «lógica»). Acá solo está lo
que se repite en todas las estaciones:

- Estación: guarda los controles, observadores y botones de una estación para
  poder desmontarlos al reejecutar la celda (sin callbacks duplicados ni
  controles conectados a un modelo viejo).
- control() y botón(): controles con rótulo claro, el argumento de Python que
  manejan y, debajo, una ayuda breve (de qué tipo es, qué hace y qué probar).
- Estación.recordar_valores_iniciales(): permite volver a los valores de
  partida sin tocar lo que ya se produjo (corridas, resultados, archivos).
- texto_de_llamada(): la llamada de Python equivalente a lo que se eligió.
- Ocupado: desactiva botones mientras corre algo costoso y mide el tiempo.
- RegistroJSONL y Bitácora: registro persistente en archivos abiertos. No
  depende de ningún widget: el panel de la bitácora es solo una vista.
- información_del_entorno(), escribir_json(), leer_json(): archivos y datos del
  entorno que se guardan junto a cada experimento.

Cómo se usa, en cada estación:

    estación = laboratorio.nueva_estación("1-explorar")
    deslizador = estación.agregar(widgets.FloatSlider(value=0.8, min=0.1, max=2.0))
    laboratorio.control(deslizador, "Temperatura", "temperatura")
    estación.al_hacer_clic(botón_generar, al_generar)

Si la celda se vuelve a ejecutar, nueva_estación() con el mismo nombre desmonta
la anterior. Así un clic produce una sola operación.
"""

import datetime
import hashlib
import json
import platform
import time
import uuid
from pathlib import Path

import ipywidgets as widgets

import utils

# ─── Registro de estaciones ──────────────────────────────────────────────────
# Diccionario global del módulo: nombre de la estación -> Estación viva. Sobrevive
# a la reejecución de las celdas porque el módulo se importa una sola vez por
# kernel. Si se reinicia el kernel, empieza vacío.
_ESTACIONES = {}


class Estación:
    """Lleva la cuenta de todo lo que una estación conectó, para poder desconectarlo."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.widgets = []
        self.observadores = []       # tríos (widget, función, nombres observados)
        self.funciones_de_clic = []  # pares (botón, función)
        self.valores_iniciales = []  # pares (control, valor de partida)
        self.desmontada = False

    def agregar(self, widget):
        """Registra un widget de la estación y lo devuelve."""
        self.widgets.append(widget)
        return widget

    def observar(self, widget, función, nombres="value"):
        """Llama a 'función' cuando cambia el valor del widget, y lo deja anotado."""
        widget.observe(función, names=nombres)
        self.observadores.append((widget, función, nombres))

    def al_hacer_clic(self, botón, función):
        """Llama a 'función' cuando se aprieta el botón, y lo deja anotado."""
        botón.on_click(función)
        self.funciones_de_clic.append((botón, función))

    def recordar_valores_iniciales(self, *controles):
        """Anota el valor actual de cada control, en este orden, como valor de partida."""
        for control_ in controles:
            self.valores_iniciales.append((control_, control_.value))

    def restaurar_valores_iniciales(self):
        """Devuelve cada control a su valor de partida. No borra corridas, resultados ni archivos.

        Solo mueve controles: los observadores que reaccionan a un cambio (por ejemplo, recalcular
        un texto de ayuda) corren, pero ninguna operación costosa se dispara desde acá.
        """
        for control_, valor in self.valores_iniciales:
            control_.value = valor

    def desmontar(self):
        """Retira observadores y funciones de botón, y cierra los widgets."""
        for widget, función, nombres in self.observadores:
            widget.unobserve(función, names=nombres)
        for botón, función in self.funciones_de_clic:
            botón.on_click(función, remove=True)
        for widget in self.widgets:
            widget.close()
        self.observadores = []
        self.funciones_de_clic = []
        self.valores_iniciales = []
        self.widgets = []
        self.desmontada = True


def nueva_estación(nombre):
    """Crea una estación. Si ya había una con ese nombre (celda reejecutada), la desmonta antes."""
    if nombre in _ESTACIONES:
        _ESTACIONES[nombre].desmontar()
    estación = Estación(nombre)
    _ESTACIONES[nombre] = estación
    return estación


def estaciones_vivas():
    """Nombres de las estaciones montadas (útil para las pruebas)."""
    return [nombre for nombre, estación in _ESTACIONES.items() if not estación.desmontada]


# ─── Controles ───────────────────────────────────────────────────────────────

def control(widget, texto, argumento, ancho="100%", tipo=None, ayuda="", prueba=""):
    """Pone al control un rótulo claro y el nombre del argumento de Python que maneja.

    Por ejemplo, texto="Temperatura" y argumento="temperatura" se ven como
    «Temperatura · temperatura =». El valor actual lo muestra el propio control.

    Opcionalmente anota qué es el control, para mostrarlo debajo con `fila_de_control`:
    - tipo: "experimento" (cambia lo que se genera o se ajusta), "vista" (solo cambia cómo se ve),
      "datos" (cambia los datos que se preparan) o "registro" (solo anota);
    - ayuda: qué hace, en una frase;
    - prueba: una propuesta concreta para probarlo y ver el cambio.
    """
    if tipo is not None and tipo not in utils.TIPOS_DE_CONTROL:
        raise ValueError(f"tipo de control desconocido: {tipo!r}. Usá uno de {list(utils.TIPOS_DE_CONTROL)}.")
    widget.description = f"{texto} · {argumento} ="
    widget.style = {"description_width": "initial"}
    widget.layout = widgets.Layout(width=ancho, max_width="46em")
    widget._ayuda_del_control = {"tipo": tipo, "ayuda": ayuda, "prueba": prueba}
    return widget


def fila_de_control(widget):
    """El control con su ayuda debajo (tipo, qué hace, qué probar). Sin ayuda anotada, devuelve el control tal cual."""
    datos = getattr(widget, "_ayuda_del_control", None)
    if not datos or not (datos["tipo"] or datos["ayuda"] or datos["prueba"]):
        return widget
    return widgets.VBox([widget, widgets.HTML(utils.html_ayuda_de_control(datos["tipo"], datos["ayuda"], datos["prueba"]))])


def botón(texto, explicación="", tipo=""):
    """Botón con texto visible y ayuda al pasar el puntero. tipo: '', 'primary', 'success', 'warning', 'danger'."""
    nuevo = widgets.Button(description=texto, tooltip=explicación or texto, button_style=tipo)
    nuevo.layout = widgets.Layout(width="auto")
    return nuevo


class Código:
    """Un argumento que se escribe tal cual en la llamada, sin comillas: una expresión, no un texto.

    Código("modelo_base") se muestra como modelo_base, no como 'modelo_base'.
    """

    def __init__(self, expresión):
        self.expresión = expresión

    def __repr__(self):
        return self.expresión


def texto_de_llamada(nombre_de_la_función, argumentos, resultado="resultado"):
    """Escribe la llamada de Python equivalente a la configuración del panel.

    'argumentos' es un diccionario {nombre: valor}. Los valores se escriben con
    repr(), así un texto lleva sus comillas y se puede copiar tal cual.
    """
    líneas = [f"{resultado} = {nombre_de_la_función}("]
    for nombre, valor in argumentos.items():
        líneas.append(f"    {nombre}={valor!r},")
    líneas.append(")")
    return "\n".join(líneas)


# ─── Operaciones costosas ────────────────────────────────────────────────────

class Ocupado:
    """Administrador de contexto para una operación costosa.

        with laboratorio.Ocupado([botón_a, botón_b], estado_html, "Generando") as ocupado:
            ...  # lo costoso
        ocupado.segundos  # lo que tardó

    Desactiva los botones, muestra «ejecutando», y al terminar muestra «completado»
    o «falló» con el mensaje del error (que además se re-lanza en `ocupado.error`
    en lugar de romper la interfaz).
    """

    def __init__(self, botones, estado, nombre, dibujar_estado=None):
        self.botones = list(botones)
        self.estado = estado          # widget HTML donde se escribe el estado
        self.nombre = nombre
        self.dibujar_estado = dibujar_estado
        self.segundos = 0.0
        self.error = None

    def _mostrar(self, estado, detalle=""):
        if self.dibujar_estado is not None:
            self.estado.value = self.dibujar_estado(estado, detalle)
        else:
            self.estado.value = f"{estado}: {detalle}" if detalle else estado

    def __enter__(self):
        self._t0 = time.perf_counter()
        for botón_ in self.botones:
            botón_.disabled = True
        self._mostrar("ejecutando", self.nombre)
        return self

    def __exit__(self, tipo, excepción, traza):
        self.segundos = time.perf_counter() - self._t0
        for botón_ in self.botones:
            botón_.disabled = False
        if excepción is not None:
            self.error = excepción
            self._mostrar("falló", f"{self.nombre}: {type(excepción).__name__}: {excepción}")
            return True  # el error queda a la vista en el estado; no se rompe el panel
        self._mostrar("completado", f"{self.nombre} ({self.segundos:.1f} s)")
        return False


# ─── Archivos y registro persistente ─────────────────────────────────────────

def ahora():
    """Fecha y hora local en formato ISO, sin fracciones."""
    return datetime.datetime.now().isoformat(timespec="seconds")


def huella_de_texto(texto):
    """SHA-256 de un texto (en UTF-8). Sirve como huella de un documento."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def huella_de_json(datos):
    """SHA-256 de un dato JSON (diccionarios, listas, textos, números) en una forma canónica.

    Las claves se ordenan y no hay espacios de más, así dos datos iguales dan siempre la misma
    huella. Sirve para identificar bloques, particiones y configuraciones.
    """
    texto = json.dumps(datos, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return huella_de_texto(texto)


def escribir_json(ruta, datos):
    """Guarda un diccionario como JSON legible, con tildes y eñes tal cual."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2, sort_keys=False)
    return ruta


def leer_json(ruta):
    """Lee un JSON guardado con escribir_json()."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


class RegistroJSONL:
    """Registro de una línea JSON por entrada, en un archivo. Solo se agrega al final.

    No depende de widgets: lo que se registra queda en el archivo aunque la
    interfaz no exista. Es el formato de las métricas, muestras y anotaciones.
    """

    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def agregar(self, entrada):
        entrada = dict(entrada)
        entrada.setdefault("hora", ahora())
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta, "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        return entrada

    def leer(self):
        if not self.ruta.exists():
            return []
        with open(self.ruta, encoding="utf-8") as archivo:
            return [json.loads(línea) for línea in archivo if línea.strip()]

    def __len__(self):
        return len(self.leer())


TIPOS_DE_ANOTACIÓN = ("observado", "interpretación", "limitación", "hipótesis pendiente")


class Bitácora(RegistroJSONL):
    """Anotaciones de la persona que experimenta, con su contexto.

    Cada entrada separa lo que se OBSERVÓ de lo que se INTERPRETA, de las
    LIMITACIONES y de las HIPÓTESIS pendientes (ver TIPOS_DE_ANOTACIÓN).
    Guarda además la estación y los datos que la sitúan (corrida, semilla, etc.).

    Cada anotación lleva un `id` propio y, si se refiere a experimentos, sus nombres en
    `experimentos`. Esos dos datos (y no la fecha) son los que asocian una anotación con un
    experimento: dos anotaciones con el mismo texto o la misma hora siguen siendo distintas.
    """

    def anotar(self, estación, tipo, texto, predicción="", contexto=None, experimentos=()):
        if tipo not in TIPOS_DE_ANOTACIÓN:
            raise ValueError(f"tipo de anotación desconocido: {tipo!r}. Usá uno de {TIPOS_DE_ANOTACIÓN}.")
        if not texto.strip():
            raise ValueError("La anotación está vacía.")
        return self.agregar({
            "id": uuid.uuid4().hex,
            "estación": estación,
            "tipo": tipo,
            "predicción": predicción,
            "texto": texto,
            "contexto": contexto or {},
            "experimentos": sorted(set(experimentos)),
        })

    def de_experimento(self, nombre_del_experimento):
        """Las anotaciones que declaran referirse a ese experimento (por su nombre de carpeta)."""
        elegidas = []
        for entrada in self.leer():
            if nombre_del_experimento in entrada.get("experimentos", []):
                elegidas.append(entrada)
        return elegidas


def información_del_entorno():
    """Versiones y condiciones relevantes. Se guarda junto a cada experimento.

    Dos corridas con la misma semilla pueden dar textos distintos si cambian
    estas condiciones (versión de torch, dispositivo, hilos), por eso se registran.
    """
    import importlib.metadata as versiones

    paquetes = {}
    for nombre in ("torch", "transformers", "numpy", "pandas", "matplotlib", "ipywidgets"):
        try:
            paquetes[nombre] = versiones.version(nombre)
        except versiones.PackageNotFoundError:
            paquetes[nombre] = "no instalado"
    dispositivos = {}
    try:
        import torch

        dispositivos["cuda"] = bool(torch.cuda.is_available())
        dispositivos["mps"] = bool(torch.backends.mps.is_available())
        dispositivos["hilos_de_cpu"] = torch.get_num_threads()
    except ImportError:
        pass
    return {
        "python": platform.python_version(),
        "sistema": platform.platform(),
        "procesador": platform.machine(),
        "paquetes": paquetes,
        "dispositivos": dispositivos,
        "fecha": ahora(),
    }


def listar_experimentos(raíz):
    """Carpetas de experimentos guardados (las que tienen configuración.json), de la más nueva a la más vieja."""
    raíz = Path(raíz)
    if not raíz.exists():
        return []
    carpetas = [c for c in raíz.iterdir() if (c / "configuración.json").exists()]
    return sorted(carpetas, key=lambda c: (c / "configuración.json").stat().st_mtime, reverse=True)


# ─── Diseño de los paneles ───────────────────────────────────────────────────

def panel_de_tres_niveles(explorar, inspeccionar, modificar):
    """Organiza una estación en tres pestañas: Explorar, Inspeccionar y Modificar.

    Explorar: controles y resultados. Inspeccionar: configuración, datos
    intermedios y mecanismos. Modificar: el código equivalente y los parámetros.
    """
    pestañas = widgets.Tab(children=[explorar, inspeccionar, modificar])
    pestañas.set_title(0, "Explorar")
    pestañas.set_title(1, "Inspeccionar")
    pestañas.set_title(2, "Modificar")
    return pestañas


def sección_plegable(título, contenido, abierta=False):
    """Panel avanzado plegable."""
    plegable = widgets.Accordion(children=[contenido], selected_index=0 if abierta else None)
    plegable.set_title(0, título)
    return plegable
