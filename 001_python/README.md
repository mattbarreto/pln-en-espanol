# Primeros pasos: la terminal y Python para textos

Laboratorio de Tecnologías del Procesamiento del Lenguaje Natural · Unidad 1

---

## Qué vas a hacer acá

Dos cosas que después no se vuelven a explicar.

Primero, moverte por tu propia máquina desde la terminal: saber dónde estás, crear
una carpeta de trabajo, bajar una página web y mirarla por dentro. Segundo, Python
aplicado a texto: variables, strings, listas, bucles, diccionarios, funciones.

**No se instala ninguna librería.** Todo lo de esta unidad sale con Python solo.
`pandas`, `requests` y compañía entran recién en la unidad 2.

---

## Antes de empezar

Leé **[ANTES_DE_LA_CLASE.md](ANTES_DE_LA_CLASE.md)**. Son 10 minutos y no hay nada
que instalar.

---

## Dónde se corre

**En Google Colab.** No hace falta instalar Python ni VS Code para esta unidad.

Con una salvedad importante, y conviene entenderla ahora:

| | dónde se lee | dónde se ejecuta |
|---|---|---|
| `01_terminal_y_la_odisea` | Colab | **En una terminal de tu máquina** |
| `02_python_para_textos` | Colab | Colab |

El cuaderno 01 es una guía: los comandos se escriben en una ventana de terminal
tuya, no en una celda. Eso es a propósito. La terminal de tu computadora es la que
vas a usar el resto de la materia; la de Colab es prestada y desaparece.

---

## El camino

| | cuaderno | tiempo | qué |
|---|---|---|---|
| 01 | `01_terminal_y_la_odisea` | 50 min | Terminal, rutas, crear un proyecto, bajar *La Odisea*, buscar dentro del HTML |
| 02 | `02_python_para_textos` | 110 min | Variables, tipos, strings, slicing, listas, bucles, condicionales, diccionarios, funciones |

El cuaderno 02 cierra con un ejercicio integrador: contar frecuencias de palabras
sobre un texto, a mano, sin librerías. Ese ejercicio es el que se va a rehacer —con
herramientas— en las unidades 3 y 4.

---

## Los mismos comandos en cada sistema

El cuaderno 01 está escrito en PowerShell porque es lo que trae Windows. Si estás
en macOS o Linux, la lógica es idéntica y varios comandos son literalmente iguales.

| qué hace | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Dónde estoy | `pwd` o `Get-Location` | `pwd` |
| Qué hay acá | `ls` o `Get-ChildItem` | `ls` |
| Entrar a una carpeta | `cd nombre` | `cd nombre` |
| Subir un nivel | `cd ..` | `cd ..` |
| Crear carpeta | `mkdir nombre` | `mkdir nombre` |
| Copiar / mover | `cp` / `mv` | `cp` / `mv` |
| Ver un archivo | `Get-Content archivo` | `cat archivo` |
| Ver las primeras líneas | `Get-Content archivo -Head 20` | `head -20 archivo` |
| Buscar texto adentro | `Select-String "palabra" archivo` | `grep "palabra" archivo` |
| Bajar una página | `curl.exe -o salida.html URL` | `curl -o salida.html URL` |
| Limpiar la pantalla | `clear` | `clear` |

Las diferencias reales son tres: `Get-Content` vs `cat`, `Select-String` vs `grep`,
y el `.exe` de `curl` en Windows (sin el `.exe`, PowerShell usa otra cosa).

---

## Si querés correrlo en tu máquina

No hace falta, pero se puede. El `requirements.txt` de esta unidad tiene una sola
línea —`ipykernel`, para que VS Code pueda abrir los cuadernos— porque el código no
usa ninguna librería externa.

```
uv venv --python 3.12
uv pip install -r requirements.txt
```

En la unidad 2 esto pasa a ser obligatorio y está explicado con detalle.

---

## Las tres ideas que sostienen todo

1. **La computadora no adivina dónde estás parado.** Casi todo lo que falla en las
   primeras semanas —un archivo que "no aparece", un comando que no encuentra
   nada— es estar en otra carpeta. `pwd` y `ls` antes de cada cosa.

2. **Un texto es una secuencia de caracteres, no palabras.** Python no sabe qué es
   una palabra hasta que vos definís el corte. `"La Odisea"[0]` es `L`, no `La`.
   Todo el procesamiento de lenguaje empieza en esa decisión.

3. **El error no es un castigo, es información.** `NameError`, `TypeError`,
   `IndexError`: cada uno dice exactamente qué pasó y en qué línea. Leerlos completos
   —no solo la última línea— es la habilidad que más rinde de acá en adelante.

---

## Lo que viene después

En la unidad 2 se automatiza lo que acá hiciste a mano: en lugar de bajar una página
con `curl` y mirarla con `Select-String`, `requests` y `BeautifulSoup` bajan muchas y
extraen lo que importa. El corpus deja de ser un archivo suelto y pasa a ser texto
con procedencia.
