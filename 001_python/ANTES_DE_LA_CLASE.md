# Antes de la clase — 10 minutos

> Hacé esto **antes** de conectarte. Si algo no sale, avisá por el canal de la
> materia y lo resolvemos antes, no durante.

En esta unidad **no se instala nada**. Solo hay que tener dos cosas abiertas y
comprobar que funcionan.

---

## 1. Una cuenta de Google

Los cuadernos se abren en **Google Colab**: <https://colab.research.google.com>

Entrá con tu cuenta de Google. Si ya usás Gmail, ya tenés cuenta.

Colab corre Python en una máquina de Google, así que no necesitás instalar Python
para esta clase. Dos cosas que conviene saber desde ahora:

- **Lo que subas a Colab se borra.** Cada sesión arranca de cero. Lo que quieras
  conservar, descargalo.
- **Guardá tu copia.** `Archivo → Guardar una copia en Drive`. Si trabajás sobre el
  cuaderno original, tus cambios no se guardan en ningún lado.

---

## 2. Una terminal

El primer cuaderno se **lee** en Colab, pero los comandos se **escriben en una
terminal de tu computadora**. Necesitás saber abrirla.

| Sistema | Cómo abrirla |
|---|---|
| **Windows** | Menú Inicio → escribí `PowerShell` → *Windows PowerShell* |
| **macOS** | `Cmd+Espacio` → escribí `Terminal` → Enter |
| **Linux** | `Ctrl+Alt+T` |

> **En Windows, usá PowerShell, no CMD.** Se parecen, pero los comandos del cuaderno
> son de PowerShell. Si la ventana dice `C:\Users\...>` sin el `PS` adelante, estás
> en CMD: cerrala y abrí PowerShell.

---

## 3. Comprobación final

Abrí la terminal y escribí estos tres comandos, uno por vez, apretando Enter:

```
pwd
ls
mkdir prueba_pln
```

Tenés que ver: la ruta de tu carpeta personal, una lista de carpetas, y ninguna
queja después del tercero.

Después, borrá la carpeta de prueba:

| Sistema | Comando |
|---|---|
| **Windows** (PowerShell) | `Remove-Item prueba_pln` |
| **macOS / Linux** | `rmdir prueba_pln` |

**Si los tres comandos anduvieron, estás listo.**

---

## Si algo falla

| Lo que ves | Qué hacer |
|---|---|
| `pwd` no hace nada o da error | Estás en CMD, no en PowerShell. Cerrá y abrí *Windows PowerShell* |
| `ls` no se reconoce | Lo mismo: es CMD. En CMD el comando sería `dir`, pero abrí PowerShell |
| No puedo entrar a Colab | Probá en una ventana de incógnito. Suele ser una sesión de Google vieja |
| Colab dice que no puede guardar | `Archivo → Guardar una copia en Drive` y trabajá sobre esa copia |
| La terminal está en otro idioma | No importa, los comandos son los mismos |

Escribí en el canal de la materia con **una captura de pantalla del error
completo**. Con "no me anda" no se puede ayudar.

---

## Para la clase que viene

La unidad 2 sí instala cosas —`uv`, un entorno virtual, librerías— y lleva más
tiempo. Su `ANTES_DE_LA_CLASE.md` es de 15 minutos y conviene no dejarlo para el
último día.
