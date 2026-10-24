# Procedencia de los datos

## Qué se usa en cada cuaderno

| Archivo | Cuaderno | Uso |
|---|---|---|
| `clasificacion.json` | 01, 02, 03 | 36 avisos con tres etiquetas. Los cuadernos evalúan con las particiones `val` y `test` y sacan ejemplos de `train`. |
| `aviso_ner.txt` | 03 | Un aviso largo de una actividad cultural, para extraer campos. |
| `politicas_biblioteca.md` | 04 | Reglamento breve de una biblioteca. |
| `busqueda_ejemplo.json` | 04 | Cuatro resultados de búsqueda **sintéticos** para ejecutar sin clave de SerpAPI. |
| `corpus.json` | (ninguno) | Copia de la unidad 010; no lo usa esta unidad. |

## Textos sintéticos (CC0-1.0)

`clasificacion.json`, `aviso_ner.txt`, `politicas_biblioteca.md` y `corpus.json` son copias sin cambios de los textos sintéticos de `010_transfer_learning/datos/`. No son documentos institucionales reales ni fragmentos de autores, no contienen datos personales y se ofrecen bajo CC0-1.0.

`busqueda_ejemplo.json` se escribió para esta unidad con la forma de la clave `organic_results` de SerpAPI. Los títulos, fragmentos y direcciones son inventados (`ejemplo.org`) y no describen jornadas reales. Sirve para ejecutar el cuaderno 04 sin clave; con clave se reemplaza por resultados reales.

## Casos inventados dentro de los cuadernos

En el cuaderno 02, cinco avisos difíciles y tres con órdenes escondidas; en el 04, 120 avisos internos de relleno. Son sintéticos y sirven para provocar fallas, no para estimar cuánto falla un modelo.
