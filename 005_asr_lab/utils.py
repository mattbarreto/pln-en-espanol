"""
Andamiaje de la unidad. Acá vive lo accesorio, no lo que se aprende.

Por qué está en un archivo aparte y no en una celda: ubicar el ejecutable de
FFmpeg en tres sistemas operativos distintos es un problema de plomería, no de
procesamiento del lenguaje. Ocupa media pantalla, no se entiende leyéndolo y no
hay nada que aprender ahí. El cuaderno 00 lo usa así:

    import utils
    carpeta_ffmpeg = utils.preparar_ffmpeg()

Lo que sí importa —cómo se baja un audio, qué procedencia se registra, qué
decide el modelo— está en los cuadernos, a la vista.
"""

# os: para leer variables de entorno y armar rutas.
import os

# shutil: 'which' busca un ejecutable en el PATH del sistema.
import shutil


# Caracteres que Windows no acepta en un nombre de archivo.
# macOS y Linux aceptan casi todo, pero conviene un único criterio para los tres.
CARACTERES_INVALIDOS = '<>:"/\\|?*'


def preparar_ffmpeg():
    """Devuelve la carpeta donde vive el ejecutable de FFmpeg.

    'yt-dlp' necesita FFmpeg para convertir el audio descargado a MP3. FFmpeg no
    se instala con pip: es un programa del sistema operativo. Si no aparece, esta
    función corta con un mensaje que dice cómo instalarlo.
    """
    # Primero la variable de entorno, por si alguien lo instaló en un lugar raro.
    ruta_declarada = os.environ.get("FFMPEG_PATH")

    if ruta_declarada and os.path.exists(ruta_declarada):
        return os.path.dirname(ruta_declarada)

    # 'which' devuelve la ruta del ejecutable si está en el PATH, o None si no está.
    ruta_encontrada = shutil.which("ffmpeg")

    if ruta_encontrada is None:
        raise FileNotFoundError(
            "No se encontró FFmpeg en el sistema.\n"
            "FFmpeg no se instala con pip: es un programa aparte.\n"
            "  Windows:  winget install Gyan.FFmpeg\n"
            "  macOS:    brew install ffmpeg\n"
            "  Linux:    sudo apt install ffmpeg\n"
            "Después de instalarlo hay que reiniciar el kernel.\n"
            "Está explicado en ANTES_DE_LA_CLASE.md."
        )

    return os.path.dirname(ruta_encontrada)


def sanitizar_nombre_archivo(nombre, largo_maximo=80):
    """Convierte un título en un nombre de archivo que funcione en cualquier sistema.

    Los títulos de video traen dos puntos, barras y signos de pregunta, que en
    Windows rompen el guardado. Cada carácter problemático se reemplaza por un
    guion bajo.
    """
    caracteres_limpios = []

    for caracter in nombre:
        if caracter in CARACTERES_INVALIDOS:
            caracteres_limpios.append("_")
        elif ord(caracter) < 32:
            # Caracteres de control: saltos de línea, tabulaciones y compañía.
            caracteres_limpios.append("_")
        else:
            caracteres_limpios.append(caracter)

    nombre_limpio = "".join(caracteres_limpios)
    nombre_limpio = nombre_limpio.strip()
    nombre_recortado = nombre_limpio[:largo_maximo]

    # Windows tampoco acepta que un nombre termine en punto o espacio.
    nombre_recortado = nombre_recortado.rstrip(". ")

    if nombre_recortado == "":
        return "audio_sin_titulo"

    return nombre_recortado
