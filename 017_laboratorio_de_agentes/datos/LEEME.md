# Procedencia de los datos

## Qué hay en `biblioteca.json`

| Parte | Contenido | Cuaderno |
|---|---|---|
| `hoy` | La fecha que se toma como «hoy» (3 de noviembre de 2026), para que los vencimientos no dependan del día en que se ejecuta el cuaderno. | 01, 02 |
| `reglas` | El reglamento: 14 días de préstamo y hasta dos renovaciones. | 01, 02 |
| `socios` | Seis personas socias, con DNI, nombre y sede. | 01, 02 |
| `prestamos` | Ocho préstamos, con código, vencimiento, renovaciones usadas y si otra persona reservó el libro. | 01, 02 |
| `catalogo` | Ocho libros, con los ejemplares disponibles en cada sede y una nota del catálogo. | 02 |

## Datos sintéticos

Todo el archivo es **sintético**: lo escribió el equipo del curso para esta unidad. La Biblioteca Popular Hojas Sueltas no existe; los nombres, los DNI, los préstamos y las notas son inventados y no corresponden a ninguna persona. Los títulos y autores del catálogo son obras reales y se usan solo como referencia bibliográfica.

Cada préstamo de Lucía Ferreyra pone a prueba una regla (uno renovable, uno sin renovaciones, uno reservado) y Ramón Quiroga tiene un préstamo vencido.

## La nota con el ataque

La nota de *Los siete locos* contiene, a propósito, instrucciones para el asistente: es el ataque que se mide en el cuaderno 02. La dirección `reactivacion@hojas-sueltas.example` usa un dominio reservado para ejemplos, que no puede pertenecer a nadie. El cuaderno 02 la reemplaza en memoria por una variante con un número de teléfono que no puede estar asignado (`11 0000-0192`), sin modificar este archivo.

## Licencia

Se distribuye bajo la licencia de contenidos del repositorio (CC BY-SA 4.0). No contiene datos personales.
