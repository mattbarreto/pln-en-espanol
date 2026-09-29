# FUENTE — corpus de textos de Hernán Casciari

Este archivo dice de dónde salió el corpus, qué se perdió en el camino y qué
se reconstruyó. **Leelo antes de usar `corpus.jsonl`.** Ningún número que saques
de este corpus significa nada si no sabés qué tenés entre manos.

---

## Qué hay acá

| archivo | qué es |
|---|---|
| `blog/*.txt` | Los datos primarios, tal como llegaron. **No se tocan.** |
| `reconstruir_corpus.py` | El script que produce `corpus.jsonl` a partir de `blog/`. |
| `corpus.jsonl` | El corpus reconstruido: un párrafo por línea. |

---

## Procedencia

**Textos:** entradas del blog de Hernán Casciari publicadas entre 2004 y 2015.

**Captura:** no la hicimos nosotros. Los archivos provienen del ejercicio de NLP
publicado en *Aprende Machine Learning*
(<https://www.aprendemachinelearning.com/ejercicio-nlp-cuentos-de-hernan-casciari-python-espanol/>),
que scrapeó **386 textos** del sitio de Editorial Orsai con `BeautifulSoup` y
`requests`, con pausas de 0,75 segundos entre pedidos.

**Fecha de los archivos:** enero de 2019.

**Estado de la fuente:** los textos **ya no están disponibles** en línea. No se
pueden volver a bajar ni verificar contra el original. Lo que hay en `blog/` es
todo lo que queda.

**Uso:** material de trabajo para una materia. Los textos son de su autor.

---

## Qué son realmente los archivos de `blog/`

Tienen extensión `.txt` pero **no son texto**. Son objetos `pickle` de Python.
Si los abrís con un editor vas a ver `\x80\x03X` y después caracteres rotos.

Se leen así:

```python
import pickle
archivo = open("blog/2004.txt", "rb")
texto = pickle.load(archivo)
archivo.close()
```

Cada archivo contiene **un único string** con todos los textos de ese año
pegados uno detrás de otro.

### La carpeta `cuentos_casciari/` es la misma cosa

Si tenés las dos carpetas, no son dos versiones: son el mismo archivo copiado.
Verificado con MD5, los doce años coinciden. Comprobalo vos:

```
md5sum blog/2004.txt cuentos_casciari/2004.txt
```

---

## Qué se perdió

Esto es lo importante, y no tiene arreglo.

**Los límites de cada texto.** El scraping bajó 386 textos por separado y
después los concatenó por año antes de guardarlos. Los 386 existieron y se
descartaron. En `blog/` quedaron 12 strings, uno por año.

**Los títulos.** No están en ninguna parte del archivo.

**Las fechas de publicación.** Solo sobrevive el año, y porque es el nombre del
archivo.

**Las URLs.** No hay ni una.

**Los saltos de línea.** El archivo de 2004 tiene **un** salto de línea en
190.786 caracteres.

Buscamos marcas que permitieran recuperar los límites de texto —títulos en
mayúsculas, fechas, separadores, líneas cortas— y no hay ninguna. Los bloques
cortos que parecían títulos son líneas de diálogo (`LUCAS.- Eso ya sé`).

**Consecuencia práctica: con este corpus no se puede preguntar nada sobre un
texto individual.** No se puede comparar un texto con otro, ni contar cuántos
textos mencionan algo, ni medir el largo típico de un texto. Si tu pregunta
necesita eso, este corpus no sirve y hay que buscar otro.

---

## Qué se pudo reconstruir

Los párrafos, y con bastante confianza.

Al concatenar los textos se borró el salto de línea pero **no** el punto final
del párrafo. Eso dejó una marca inconfundible: un punto seguido inmediatamente
de mayúscula, **sin espacio en el medio**.

```
...compartir algunos detalles con el lector.La idea nació como un juego...
                                           ↑
                                    acá terminaba un párrafo
```

Un punto normal de fin de oración va seguido de espacio (`lector. La idea`).
Los dos casos se distinguen sin ambigüedad, y en el corpus hay 5.416 del
segundo tipo.

### Criterio aplicado

- Se corta en cada punto seguido de mayúscula sin espacio.
- El punto se le devuelve al párrafo que termina.
- Se descartan los bloques de menos de 2 caracteres.
- **No se descarta nada más.** Los bloques cortos —líneas de diálogo de doce
  caracteres, por ejemplo— se conservan. Filtrarlos es una decisión de análisis,
  no de limpieza, y le corresponde a quien analiza. Por eso cada registro trae
  el campo `caracteres`: filtrá vos, con el umbral que puedas justificar.

### Resultado

| | |
|---|---|
| párrafos | **5.428** |
| caracteres en `blog/` | 2.376.248 |
| caracteres en `corpus.jsonl` | 2.376.134 — **el 100,00%** |
| largo mínimo / mediano / máximo | 5 / 348 / 11.237 caracteres |
| párrafos de menos de 40 caracteres | 162 |

Los 114 caracteres de diferencia son espacios en blanco al principio y al final
de cada párrafo.

**Párrafos por año:**

| 2004 | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 435 | 676 | 477 | 504 | 813 | 116 | 356 | 557 | 294 | 226 | 693 | 281 |

El párrafo más largo, de 11.237 caracteres, casi seguro no es un párrafo: es un
tramo donde la marca de corte no aparece. Miralo antes de sacar conclusiones
sobre largos.

---

## El formato de `corpus.jsonl`

Una línea por párrafo, en JSON:

```json
{"anio": 2004, "parrafo": 1, "caracteres": 423, "texto": "Ayer di por finalizada..."}
```

| campo | qué es |
|---|---|
| `anio` | El año, tomado del nombre del archivo, como número entero. Es el único dato de fecha que sobrevivió. |
| `parrafo` | Número de orden dentro del año. **No** es un identificador de texto. |
| `caracteres` | Largo del párrafo. Está para que filtres vos. |
| `texto` | El párrafo. |

Se lee así:

```python
import pandas as pd
corpus = pd.read_json("datos/corpus.jsonl", lines=True)
```

---

## Advertencias

1. **La unidad de análisis es el párrafo, no el texto.** Todo lo que cuentes se
   cuenta sobre párrafos. Decilo en tus conclusiones.

2. **Los párrafos por año no miden productividad.** 2008 tiene 813 párrafos y
   2009 tiene 116, pero no sabemos cuántos textos hubo en cada año ni de qué
   largo. La diferencia puede ser de cantidad, de extensión o de las dos cosas.

3. **La numeración de párrafos es continua dentro del año**, así que el párrafo
   436 de 2004 no existe y el párrafo 1 de 2005 no es el comienzo de nada en
   particular.

4. **No se puede verificar contra el original.** La fuente ya no está.

---

## Cómo regenerar

```
python datos/reconstruir_corpus.py
```

Lee `blog/`, escribe `corpus.jsonl`. No modifica nada en `blog/`.
