# TPI 1 · El corpus como decisión

**Armar un corpus, probar una hipótesis, mostrar el resultado**

Laboratorio de Tecnologías del PLN · IFTS N° 24 · DGETyFP · CABA
Profesor Matías Barreto · Ciclo lectivo 2026

**Grupal. Domiciliario. Integra las unidades 3 y 4.**

---

## De qué se trata

Van a elegir una pregunta sobre textos, armar el corpus que permita contestarla y
contestarla con las técnicas de la cursada: minería de texto para contar, spaCy para
mirar la lengua, y gráficos y concordancias para mostrar el resultado.

No hay tema asignado ni corpus provisto. Esta vez el material lo eligen ustedes.

Lo que se evalúa es el **criterio**, no la cantidad de código. Un hallazgo modesto,
medido bien y con las decisiones a la vista, vale más que una batería de técnicas
aplicadas sin saber para qué.

---

## Los grupos

Se trabaja en **dos grupos**, y cada uno toma un macrogénero:

| | Material | Preguntas que habilita |
|---|---|---|
| **Laboratorio A** | Ficción y narrativa: cuentos, capítulos, relatos | Voz narrativa, tiempos verbales, léxico, evolución de un autor, diferencias entre autores |
| **Laboratorio B** | No ficción: noticias, editoriales, discursos, ensayos | Encuadre, quién habla y quién es hablado, actores, temas, atribución |

El macrogénero define el material, no el resultado. Ningún fenómeno lingüístico es
exclusivo de la ficción ni de la no ficción: un cuento puede estar lleno de entidades
institucionales, una crónica puede tener alta densidad narrativa. Esa incertidumbre es
justamente lo que hay que poner a prueba.

### Quién hace qué

Estos roles salen de las tareas que ustedes mismos marcaron como más cómodas en la
encuesta de inicio. **Son una sugerencia para repartirse, no un organigrama.**

| Rol | En este trabajo es |
|---|---|
| Investigar | Elegir el material, rastrear las fuentes, verificar procedencia |
| Proponer ideas | Formular la tesis, clasificar el abanico de la Fase 1 |
| Organizar el trabajo | Repartir, poner fechas internas, que el cuaderno corra entero |
| Acompañar a quien se queda atrás | Que nadie del grupo termine sin haber tocado el código |
| Resolver problemas técnicos | El entorno, spaCy, lo que rompe |
| Registrar y documentar | La bitácora, `FUENTE.md`, la tabla de cambios de `utils.py` |
| Crear o producir | Los gráficos, la nube, cómo se ve el informe |
| Comunicar y presentar | El informe, los títulos de los gráficos |
| Coordinar personas | Que los tiempos de todos entren en el mismo repositorio |

Repártanse en función de eso, con tres condiciones:

1. **Todos corren el cuaderno completo al menos una vez.** No se aprueba habiendo mirado.
2. **Los roles rotan** entre la Fase 1 y la Fase 3, y queda anotado quién hizo qué.
3. **Quien le preguntó a la IA no es quien valida la respuesta.** Si la misma persona
   pide y aprueba, no hubo auditoría.

Acompañar a quien se está quedando atrás es un rol como cualquiera de los otros: existe
en este trabajo y cuenta.

---

## Cómo se le pide a la IA, y cómo se audita

En cada fase hay dos movimientos:

> **Voy** — le pedís algo a la IA.
> **Vengo** — volvés con lo que trajo y decidís, con criterio propio, qué se sostiene.

El *Voy* es rápido. El *Vengo* es el trabajo.

**Lo que se evalúa no es el prompt, sino la auditoría que hicieron sobre lo que el modelo
les devolvió.**

### La IA hace cuatro trabajos distintos, y no se auditan igual

**Escribe código.** Le pedís una función que cuente adjetivos por documento. Esa se
audita corriéndola: anda o no anda, el número da o no da. Es la más fácil, porque cuando
falla, falla ruidosamente.

**Propone preguntas.** Te dice que tu hipótesis se puede contrastar con TF-IDF. Acá no
hay celda que corras para verificarlo: hay que preguntarse si TF-IDF mide lo que ustedes
quieren medir. TF-IDF les dice qué palabra distingue un documento del resto del corpus;
no les dice si un texto es más emotivo que otro. Suena parecido y no es lo mismo.

**Propone criterios.** Le pedís una rúbrica para armar el corpus y te devuelve cinco
criterios impecables que sirven para cualquier corpus del mundo. Se audita aplicándola:
si la rúbrica no descarta ni un solo texto, no filtró nada.

**Explica conceptos.** Te explica por qué `smooth_idf=True` cambia el resultado. Esta es
la peligrosa. Una explicación falsa no rompe nada, suena bien, y les queda adentro. Se
audita contra la fuente: la documentación de scikit-learn, o el cuaderno donde lo vimos.

### Tres maneras de comprobar, las tres ya las usaron

**Ir a ver los casos.** La IA les dice que *che* aparece tanto porque es la marca del
habla rioplatense. Corren `concordancia_de(corpus, "che")` y de veinte apariciones, seis
son Ernesto Guevara. El conteo estaba bien; la explicación, no. Lo hicieron en el anexo
de la unidad 3.

**Cambiar una sola cosa y volver a preguntar.** Le preguntan si su hipótesis es viable y
dice que sí. Se la vuelven a preguntar cambiando una palabra —«noticias» por
«editoriales»— y ahora dice que no. Si la respuesta se da vuelta con un cambio así, no
estaba contestando sobre el caso de ustedes. Es la misma prueba de pares mínimos que le
hicieron a spaCy en el cuaderno `04`.

**Escribir de antemano qué los haría descartar.** Antes de pedir las cinco preguntas,
anoten: *«vamos a descartar cualquiera que necesite más de veinte textos, y cualquiera
que dependa de entender ironía»*. Después descartar es fácil. Si no lo escribieron antes,
todo lo que devuelve el modelo va a parecer razonable.

### La bitácora

No es un archivo aparte. Va **dentro del cuaderno**, donde pasó, en una celda de
markdown:

> **Consulta a la IA**
> Qué pedimos · Qué contestó (resumido) · Qué comprobamos y cómo · Qué quedó y qué tiramos

Tres o cuatro en todo el trabajo, en los momentos que importaron. No hace falta registrar
cada intercambio.

---

## Fase 1 · La pregunta

Es el momento más importante y el que más se subestima. Una pregunta mal formulada
produce cuentas correctas que no dicen nada.

Esta fase no existe para producir una hipótesis. Existe para que aprendan **qué es una
hipótesis y en qué se distingue de un tema**.

### Lo que tienen disponible para preguntar

| | Qué mide | Con qué |
|---|---|---|
| **Léxico** | Qué términos son frecuentes y cuáles distintivos | BoW, frecuencia relativa, TF-IDF |
| **Actores** | Qué personas, lugares e instituciones aparecen | spaCy NER |
| **Acción** | Qué verbos predominan y con qué sujetos se asocian | POS, lematización |
| **Morfología verbal** | Qué tiempos, modos y personas gramaticales dominan | `token.morph` |
| **Enunciación** | Quién habla, cita, describe, evalúa o narra | Pronombres, verbos de habla, concordancias |

Fuera de alcance, para que no pierdan tiempo: ironía, intención del autor, calidad
literaria, veracidad de una afirmación, sentimiento fino. Todo lo que necesite
**entender** el texto en vez de **describirlo**.

### Paso 1.1 · Voy · El abanico

Pídanle a la IA cinco propuestas, no una. Van a llegar desparejas: algunas bien formadas,
otras no. Esa desigualdad es el material de trabajo del paso siguiente, así que no
descarten nada todavía.

> **Prompt**
>
> «Somos estudiantes universitarios de la materia Laboratorio de Tecnologías de
> Procesamiento del Lenguaje Natural. Se nos pidió conformar un corpus de entre 12 y 20
> textos en español de [Ficción / No Ficción], con el fin de realizar un análisis de
> estilo cuantitativo mediante minería de textos (frecuencias, Bag of Words y TF-IDF).
>
> Necesitamos que actúes como consultor experto en lingüística computacional y nos
> propongas 5 posibles preguntas guía de investigación o hipótesis lingüísticas que sean
> metodológica y matemáticamente viables de responder analizando un corpus tan pequeño de
> este género. Enfocá las hipótesis en rasgos formales medibles cuantitativamente:
> distribución gramatical de categorías de palabras, densidad léxica, polaridad o
> patrones de adjetivación.»

Copien la respuesta completa en el documento de trabajo del grupo. Se usa entera en el
paso siguiente.

### Paso 1.2 · Vengo · Clasificar el abanico

Acá está el corazón del trabajo. No se trata de elegir la mejor de las cinco: se trata de
entender qué las diferencia.

**Elegir permite esquivar el criterio; clasificar obliga a formularlo.**

Sin elegir todavía, repartan las cinco propuestas en tres grupos y escriban una línea
justificando cada ubicación.

| | |
|---|---|
| **A** | **Contrastables.** Se sabe qué se cuenta y contra qué se compara |
| **B** | **Nombran algo real, pero todavía no medible.** El fenómeno existe; falta traducirlo a una magnitud |
| **C** | **No viables con este corpus.** Exigen interpretación, contexto cultural profundo o muchos más textos |

### Paso 1.3 · Formular el criterio

Con los tres grupos armados, escriban en tres o cuatro líneas y con sus propias palabras
qué distingue al grupo A del grupo B. No qué distingue una propuesta de otra: **qué
distingue a los grupos.**

Ese enunciado es el resultado principal de la Fase 1 y va en la bitácora.

### Paso 1.4 · Operacionalizar

Recién ahora eligen una. Y la eligen **del grupo B, no del A**.

Tomar una del A significa llevarse una hipótesis ya resuelta por la máquina sin practicar
la traducción, que es la operación que importa.

Traducir la hipótesis elegida implica contestar por escrito tres preguntas:

1. Qué se cuenta exactamente.
2. Contra qué se compara ese conteo.
3. Qué resultado la refutaría.

> **Un caso**
>
> *«Los textos de Roberto Arlt mencionan a Buenos Aires como el epicentro del mundo.»*
>
> Grupo B. El fenómeno es real y observable, pero «epicentro» nombra una relación, no una
> cantidad, y toda relación necesita un segundo término. Al contestar *contra qué se
> compara* aparece lo que faltaba: una periferia.
>
> Operacionalizada podría quedar como la proporción de topónimos porteños frente a
> topónimos extranjeros, o como los adjetivos que aparecen cerca de «Buenos Aires» en una
> ventana de contexto acotada.

### Paso 1.5 · El título-tesis

Redacten la formulación final como una afirmación, no como una etiqueta temática.

| | |
|---|---|
| **Título-etiqueta** · rechazado | *Análisis de palabras en noticias de economía* |
| **Título-tesis** · aceptado | *La prensa económica atribuye la inflación a factores externos un 40% más que a variables locales* |

El primero muestra un tema. No afirma nada, así que **no puede estar equivocado**, y por
eso tampoco puede estar bien. El segundo dice algo que los datos pueden confirmar o
refutar. Esa es toda la diferencia.

**Control anti-sesgo.** ¿La tesis da por sentado un resultado esperable del macrogénero?
Si el trabajo consiste en confirmar lo que ya sabíamos, reformúlenla.

**Control de recorte.** Revisen que el resultado no venga garantizado por la selección del
material. Unas aguafuertes *porteñas* hablando de Buenos Aires no confirman nada: el
hallazgo lo produjo el recorte, no los datos.

### Paso 1.6 · Voy · Consulta de viabilidad

La hipótesis ya está formulada. Falta comprobar que se pueda contrastar con las técnicas
que efectivamente vimos, y no con otras que no vamos a usar.

> **Prompt**
>
> «Esta es nuestra hipótesis de trabajo: "[Título-Tesis]". Vamos a contrastarla sobre un
> corpus de entre 12 y 20 textos en español usando exclusivamente estas técnicas: Bag of
> Words, frecuencias relativas, TF-IDF, spaCy NER, análisis POS, lematización, morfología
> verbal con token.morph y concordancias.
>
> Indicá qué variable textual habría que contrastar, con cuál de esas técnicas se obtiene,
> y qué operación de comparación permitiría confirmar o refutar la afirmación. Si alguna
> parte de la hipótesis no es contrastable con este repertorio, señalalo explícitamente.»

### Paso 1.7 · Vengo · Ajuste final

Si la IA señala que algo no es contrastable con el repertorio disponible, hay dos salidas
legítimas: **acotar la hipótesis** a lo que sí se puede medir, o **cambiar la técnica**
prevista.

Lo que no es una salida es dejar la hipótesis intacta esperando que el análisis la
sostenga igual.

Registren en la bitácora qué señaló el modelo y qué decidieron hacer con esa señal.

---

## Fase 2 · El corpus

**Entre 12 y 20 textos, en español**, del macrogénero de su laboratorio.

**El corpus de la cursada no se usa.** Casciari fue el material con el que aprendimos las
técnicas; acá hay que componer un corpus propio. Componerlo es parte de lo que se evalúa.

> Un corpus es texto más procedencia. Un texto sin fecha, sin autor y sin contexto de
> emisión no es un dato: es un residuo digital.

### Paso 2.1 · Voy · La rúbrica de fuentes

> **Prompt**
>
> «Como especialista en curaduría de datos textuales, sugerime una rúbrica de 5 criterios
> de control para conformar un corpus balanceado de entre 12 y 20 textos en español
> orientados a contrastar la hipótesis: "[Título-Tesis]". Necesitamos controlar:
> dispersión de longitud (tokens), estabilidad del registro lingüístico, balance temporal
> o de autoría, trazabilidad ética de las fuentes y formato de almacenamiento
> estructurado.»

### Paso 2.2 · Vengo · Ajustar y aplicar

La rúbrica que devuelve el modelo es genérica por construcción: sirve igual para
cualquier corpus. **Ajústenla a su tesis antes de aplicarla**, y agreguen al menos un
criterio que solo tenga sentido en este objeto de estudio. Si alguno de los cinco ejes no
aplica —el balance de autoría en un corpus de autor único, por ejemplo— reemplácenlo por
otro que sí discrimine.

Después aplíquenla, y **reporten cuál criterio no pudieron cumplir**. Casi siempre hay
uno. Ese es el dato.

**A la IA no se le pide que sugiera, invente o provea los textos.** La selección y la
validación de los documentos es decisión del grupo.

### La recolección

Con `trafilatura` o `BeautifulSoup`, como en la unidad 2, o por extracción manual
documentada. El cuaderno `pair_programming_ia/de_una_url_a_un_corpus.ipynb` hace este paso
completo: partan de ahí y no de cero.

**Se sugiere hacer la experiencia de scraping**, porque recolectar es donde se aprende qué
es la procedencia: qué se pierde al extraer, qué queda afuera, qué hay que declarar.

Dicho eso, hay una alternativa legítima para el laboratorio de ficción:
`004_spacy/datos/cuentos_latinoamericanos.csv`, los 719 cuentos de 57 autores que scrapeó
Karen Palacio de Ciudad Seva. Se puede usar, y trae su propio trabajo: **es un dataset
armado por otra persona y tiene defectos.** Si eligen ese camino, auditarlo es parte de la
Fase 2 —qué trae, qué le falta, qué está mal— y ese informe reemplaza al de la
recolección. No trae año de publicación, así que cierra las preguntas temporales.

En los dos casos, **el corpus final son entre 12 y 20 textos**: si salen del CSV, hay que
elegirlos con la misma rúbrica y documentar el recorte igual.

Va en `datos/corpus.jsonl`, una línea por documento, siete campos:

```json
{"id": "doc_01", "titulo": "Título de la obra o nota", "autor": "Nombre del autor", "fecha": "2024-03-15", "fuente_url": "https://repositorio.org/texto1", "categoria": "Editorial", "texto": "Contenido completo normalizado..."}
```

El campo `categoria` es el que va a agrupar la comparación: el medio, el autor, la época,
la sección. Elíjanlo pensando en la tesis.

### Checklist del curador

1. **Dispersión de longitud.** Calcular `len(texto.split())` por documento. ¿Hay uno de
   200 palabras compitiendo con otro de 15.000? Documentar la disparidad: va a
   condicionar todo lo que sigue.
2. **Limpieza de artefactos.** Espacios duros (`\xa0`), encabezados de digitalización,
   errores de OCR, restos de HTML o JS. Ojo con los párrafos duplicados: en el corpus de
   la cursada había doce.
3. **Redacción de `FUENTE.md`.** Quién produjo los textos originales, licencias de acceso,
   transformaciones de limpieza aplicadas, criterios de exclusión, y una sección final:
   **qué no se puede preguntar con este corpus.**

### Bitácora del curador

Por cada documento se registra:

`01` Título · `02` Autor o medio · `03` Fecha · `04` Fuente, con fecha de acceso ·
`05` Criterio de rúbrica que cumple, y por qué · `06` **Qué aporta para contrastar la
tesis** · `07` Observaciones de limpieza

Hay dos criterios distintos en juego: si el texto cumple la rúbrica técnica, y si además
le sirve a la tesis. **No alcanza con lo primero.**

> **Antes de cerrar el corpus**
>
> Relean su título-tesis. ¿Hay algún texto que están incluyendo porque cumple la rúbrica,
> pero que no aporta nada para contrastarla? Reemplácenlo.

---

## Fase 3 · El análisis

Todo lo de las unidades 3 y 4, en un solo cuaderno y en un solo recorrido.

No son dos análisis pegados. Son tres pasos de un mismo argumento:

> **contar → mirar → volver al texto**

### Contar · unidad 3

> **Prompt**
>
> «Tenemos un archivo `corpus.jsonl` con textos en español y sus metadatos, y esta
> hipótesis: "[Título-Tesis]". Escribí código en Python con pandas y scikit-learn que
> genere: (1) una matriz documento-término con CountVectorizer, (2) frecuencias relativas
> por cada 10.000 palabras descartando palabras vacías, y (3) la matriz TF-IDF con
> TfidfVectorizer.
>
> Escribilo paso a paso, con una operación por línea y nombres de variable que digan de
> qué hablan. Explicá qué hace cada parámetro que cambie el resultado.»

**Cuatro auditorías, todas obligatorias y todas vistas en clase:**

1. **Frecuencia cruda contra normalizada.** Muestren **un caso concreto de su corpus**
   donde una palabra parezca dominante solo porque el documento es más largo, y cómo la
   frecuencia relativa lo corrige.
2. **La falacia del TTR.** Calculen el TTR de cada texto y crúcenlo con su largo. ¿Los
   textos cortos dan «más ricos»?
3. **TF-IDF: sklearn contra el pizarrón.** Por qué una palabra que está en todos los
   documentos no da 0,000. `smooth_idf=True` y la norma L2.
4. **Palabras vacías.** ¿Qué sacó la lista automática? ¿Se llevó pronombres o negaciones
   que su tesis necesita?

### Mirar · unidad 4

Lo que la bolsa de palabras destruyó: orden, morfología, sintaxis, entidades.

> **Prompt**
>
> «Escribí código en Python que cargue el modelo `es_core_news_lg` de spaCy y procese los
> textos de nuestro `corpus.jsonl` con `nlp.pipe()`. Necesitamos extraer: (1) entidades
> nombradas, (2) análisis morfológico con `token.morph` —tiempo, modo y persona verbal— y
> (3) palabras clave filtrando por `pos_` en NOUN, VERB o ADJ.
>
> Devolvé los resultados como tablas de pandas, listas para graficar. Una operación por
> línea, y explicá cada filtro.»

Elijan **dos o tres** operaciones que sirvan a su pregunta; el repertorio completo está en
`004/08`. Y dos cosas obligatorias:

- **Auditar el modelo.** Documenten al menos dos errores sobre su corpus. Los conocen:
  mayúscula después de punto tomada como entidad, voseo mal lematizado, organizaciones
  clasificadas como personas.
- **Intervenir el pipeline.** Un `EntityRuler` antes del `ner` con los términos propios de
  su corpus, o un `PhraseMatcher` para lo que quieran contar.

```python
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([{"label": "CONCEPTO_CLAVE", "pattern": "lucha de clases"}])
```

### Volver al texto

Este es el paso que separa un análisis de una planilla, y el que más se olvida.

> **Toda afirmación cuantitativa del informe viene acompañada de al menos tres
> concordancias de su término.**

Si dicen que *crisis* se triplica, muestren tres apariciones con su contexto. Es una línea
de código —`concordancia_de()`, ya la tienen— y es lo único que distingue un número que
dice algo de un número que solamente es correcto.

---

## Fase 4 · Mostrarlo

Un gráfico en PLN es un argumento, no una decoración.

**Mínimo: dos gráficos y una nube.** Uno de los gráficos sale de los conteos, el otro de
spaCy.

> Un conteo de spaCy —tiempos verbales por documento, entidades por categoría, proporción
> de adjetivos— es una tabla igual que cualquier otra. Se grafica con el mismo `plt.bar`
> de la unidad 3. En la unidad 4 no graficamos nada, pero no porque no se pueda.

### Las reglas

- **El título del gráfico es la tesis, no la etiqueta.** No *«Frecuencia de términos»*
  sino *«El término X duplica su peso relativo en el medio Y»*.
- **El eje vertical arranca en cero** cuando son frecuencias relativas. Ya vieron qué pasa
  cuando no.
- **La nube va, con su párrafo al lado**, contestando: ¿qué pregunta **no** puede
  contestar esta nube? Una nube sola no sostiene ninguna afirmación. Varias nubes
  comparadas sí pueden: depende de qué comparen, no de qué sean.

### El informe

Va en el `README.md` y no pasa de una carilla:

1. El título-tesis
2. Qué encontraron
3. **Qué los desmintió**
4. Qué preguntas se pueden hacer ahora que antes no

---

## Si la tesis resulta falsa

**Una tesis refutada aprueba. Una tesis forzada desaprueba.**

Si los datos dan en contra, el trabajo es reportarlo. No cambien la pregunta para que dé
bien, y no prueben quince combinaciones hasta que una dé la diferencia que buscaban: esa
diferencia no significa nada, la encontraron porque buscaron mucho.

En la unidad 4 lo probamos dos veces —los apellidos del `04`, los vectores del `07`— y las
dos veces la sospecha no se confirmó. Las dos veces está escrito así en el cuaderno. Una
prueba que solo puede darles la razón no es una prueba: es una ilustración.

---

## El código

El código de este trabajo lo van a leer sus compañeros en la auditoría cruzada, y lo van a
leer ustedes dentro de dos semanas. Escríbanlo para eso:

- Si hay que leer una línea dos veces para saber qué hace, pártanla en dos.
- Un bucle largo y claro es mejor que una línea ingeniosa.
- Los nombres dicen de qué hablan: `frecuencias_por_medio`, no `df2`.
- **Si la IA devuelve algo que no pueden explicar línea por línea, no lo pongan.**
  Pídanselo más simple, o escríbanlo ustedes.

### `utils.py`: heredado y adaptado

Parten del `utils.py` de `003/anexo`. **No lo copien tal cual y no lo escriban de cero:**
adáptenlo a su corpus. Está escrito para un corpus de blog agrupado por año; el de ustedes
son documentos con metadatos.

| Función | Qué le pasa |
|---|---|
| `limpiar`, `contar_con_contenido`, `conteos_de_contenido`, `caracteristicas_de` | Quedan **intactas** |
| `cargar_palabras_vacias` | Cambia la ruta |
| `agrupar_por_anio` | Se generaliza a `agrupar_por(corpus, columna)` |
| `concordancia_de` | Cambia `fila.anio` por su columna de agrupación |
| `cargar_anio`, `cortar_en_parrafos`, `armar_corpus` | **Se reemplazan:** su corpus ya viene en documentos |
| `cargar_lexicon`, `puntuar_texto` | Opcionales, solo si la tesis es afectiva |

Entregan una tabla de tres columnas —**intacta / adaptada / nueva**— con una línea de
motivo en cada adaptada.

Adaptar código heredado es, además, el mejor lugar para auditar a la IA: si le piden que
generalice `caracteristicas_de`, tienen el original al lado para comprobar si la
adaptación conserva la operación.

---

## Qué se entrega

```
TPI1_[Laboratorio]/
├── README.md              El informe, y la lista de integrantes con apellido y nombre
├── FUENTE.md              Procedencia del corpus y qué no se le puede preguntar
├── requirements.txt       Con uv
├── utils.py               Heredado y adaptado, con la tabla de cambios
├── datos/
│   └── corpus.jsonl       Entre 12 y 20 textos con metadatos completos
├── 00_corpus.ipynb        Cómo se armó. Se corre una vez
└── 01_analisis.ipynb      El trabajo. Corre entero de arriba a abajo
```

Son dos cuadernos, pero **no partidos por técnica**: el `00` arma el corpus y no se vuelve
a tocar, el `01` es el análisis completo, de los conteos a spaCy a la vuelta al texto.
Partirlo en «text mining» y «spaCy» daría dos trabajos pegados, y lo interesante está
justo en el cruce: TF-IDF les tira una palabra rara, la concordancia les muestra los
casos, spaCy les dice que era un nombre propio y no un sustantivo. Eso es **un**
argumento.

**Antes de entregar, corran `01_analisis.ipynb` de punta a punta con el kernel
reiniciado.** Si una celda falla, tiene que fallar a propósito y estar explicado.

---

## Auditoría cruzada

En clase, en el encuentro de cierre. **Cada grupo audita al otro**, sobre lo que haya. Es
interesante justamente porque van a juzgar un corpus de un macrogénero que no trabajaron.

**No bloquea la aprobación de nadie:** si el otro grupo no llegó, no es problema de
ustedes.

| Qué se mira | La pregunta |
|---|---|
| Corpus | ¿Se puede reproducir con `FUENTE.md` y `corpus.jsonl`? |
| Medición | ¿Normalizaron por largo? ¿Auditaron el TTR? |
| Vuelta al texto | ¿Cada afirmación tiene sus concordancias? |
| Modelo | ¿Auditaron los errores de spaCy o aceptaron la salida? |
| Imagen | ¿El gráfico sostiene lo que su título afirma? |
| **Criterio propio** | **¿Hay algo que la IA propuso y el grupo rechazó con fundamento?** |

La última fila es la que más importa. Un trabajo donde la IA nunca se equivocó es un
trabajo donde nadie miró.

Media carilla, no más.

---

## Evaluación

**Aprobado / Desaprobado**, con una reentrega después de las correcciones y del dictamen
de la auditoría cruzada.

Se evalúa, en este orden:

1. Que la tesis se pueda medir y se pueda refutar
2. Que el corpus tenga procedencia y sus límites declarados
3. Que las mediciones estén auditadas y tengan vuelta al texto
4. Que el criterio propio se vea: qué descartaron y por qué
5. Que el código se entienda

No se evalúa la cantidad de técnicas aplicadas, ni la extensión, ni que la hipótesis haya
dado bien.

---

## Cierre

Una página, al final del `README.md`, sobre dos cosas:

1. **Un caso concreto** en que la IA les dio algo defectuoso con tono convincente: código
   que no corría, un parámetro que no existe, una explicación falsa. Qué fue y cómo lo
   detectaron.
2. **La distancia entre los modelos y su corpus.** `es_core_news_lg` aprendió a etiquetar
   con AnCora y a reconocer entidades con WikiNER: prensa y enciclopedia, sobre todo
   peninsular. ¿Qué de su material le queda lejos?

Y algo que conviene tener presente: hay grupos en la región construyendo alternativas
—BETO en la Universidad de Chile, RoBERTuito y pysentimiento en el CONICET, la UBA y la
UNC. No todo se hace afuera.

---

## Marco pedagógico

La idea de ir hacia la máquina y volver con criterio propio —el **voy y vengo** de esta
consigna— viene de:

Chamorro, F.; González, N.; Milillo, C.; Tarasow, F. (2024). *Bailando con la IA en el
aula: un vals con ChatGPT.* PENT FLACSO Argentina. pent.flacso.org.ar/producciones

Es una referencia sobre cómo usar IA generativa en el aula, no un marco teórico del
análisis lingüístico.
