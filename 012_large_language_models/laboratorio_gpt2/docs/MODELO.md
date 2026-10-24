# Modelo base: DeepESP/gpt2-spanish

Ficha del modelo con el que ajusta el laboratorio y criterio de elección. Los datos salen de la ficha pública del modelo en Hugging Face (consultada el 9 de octubre de 2026) y de la lectura de sus archivos; lo que no está documentado se dice explícitamente.

## Datos

| Aspecto | Valor |
|---|---|
| Identificador | `DeepESP/gpt2-spanish` |
| Revisión fijada | `1b935e39cf9893108bd2f4fb5317f48ae1c3ab5e` (rama principal al momento de elegirlo) |
| Autoría | Alejandro Oñate Latorre y Jorge Ortiz Fuentes, comunidad DeepESP |
| Licencia | MIT (declarada en la ficha) |
| Arquitectura | GPT-2 pequeño (`GPT2LMHeadModel`): 12 capas, 12 cabezas, 768 dimensiones, unos 124 millones de parámetros |
| Contexto | 1024 tokens |
| Tokenizador | BPE a nivel de bytes, vocabulario de 50.257 tokens, entrenado desde cero con texto en español; incluye `<\|endoftext\|>` (id 50256) |
| Tamaño en disco | unos 250 MB en el checkpoint original (`float16`); 500 MB al guardar en `float32` |
| Última actualización | octubre de 2021 |

## Qué se sabe de sus datos

Según la ficha: entrenado desde cero con 11,5 GB de textos en español, 3,5 GB de artículos de Wikipedia y 8 GB de libros (narrativa, cuentos, teatro, poesía, ensayo y divulgación). La ficha advierte que los datos **no fueron filtrados**, de modo que el modelo puede generar contenido ofensivo o discriminatorio.

## Qué no se sabe

- Cuáles son los libros concretos. No hay lista de títulos ni de autores.
- Si hay textos de Quiroga, de los autores de `datos/textos` o de otros autores del corpus de trabajo. Por lo tanto, **no se puede afirmar que el modelo «no conoce» un texto** ni que lo reproduce porque lo aprendió en el ajuste.
- Cómo se evaluó el modelo. La ficha no informa métricas.
- Qué proporción de español rioplatense hay en sus datos.

## Criterio de selección

Se compararon por su ficha pública tres candidatos de español con arquitectura GPT-2 pequeña:

| Candidato | Licencia | Datos declarados | Notas |
|---|---|---|---|
| `DeepESP/gpt2-spanish` | MIT | 11,5 GB: Wikipedia + libros | Datos con peso literario (8 GB de libros); es el que usa la unidad de transfer learning y ya está en la caché local |
| `datificate/gpt2-small-spanish` | Apache-2.0 | Wikipedia | Más descargado, pero solo texto enciclopédico |
| `PlanTL-GOB-ES/gpt2-base-bne` | Apache-2.0 | Biblioteca Nacional de España | Ficha sin etiqueta de tarea ni de biblioteca; no se verificó que cargue directo con `AutoModelForCausalLM` |

Se eligió `DeepESP/gpt2-spanish` por tres razones: licencia permisiva, un entrenamiento con libros (más cercano a lo que se ajusta acá: cuentos) y continuidad con la unidad de transfer learning. La elección **no** implica que sea el mejor modelo en español ni que su español sea el adecuado para cualquier uso.

## Hallazgo de ejecución: la precisión

El checkpoint está guardado en `float16`. Con `transformers` 5.19, `from_pretrained` lo carga en ese formato si no se indica otra cosa. En una prueba nuestra, **entrenar en `float16` con AdamW dio `nan` en todos los pesos tras el primer paso**, tanto en CPU como en MPS. Con `dtype=torch.float32` el ajuste fue estable. Por eso el laboratorio carga siempre en `float32`, y la configuración registra `precisión: float32`. No se probó `bfloat16` ni `float16` con escalado de pérdida.

Una consecuencia: guardar un checkpoint ajustado ocupa unos 500 MB, el doble que el original.

## Advertencias de carga

Al cargar aparece un aviso `UNEXPECTED: transformer.h.{0...11}.attn.masked_bias`. Es un búfer que el checkpoint original guardó y la versión actual de `transformers` ya no usa; el propio aviso dice que se puede ignorar si la arquitectura es la misma. Se comprobó que la pérdida calculada a mano coincide con la del modelo.

## Condiciones de uso

MIT para el modelo. Los textos con los que se ajuste tienen sus propias condiciones (ver `datos/quiroga/FUENTE.md` y `datos/textos/LEEME.md`). Un modelo ajustado con textos con derechos vigentes **no debe publicarse** sin resolver esa cuestión; el laboratorio no sube nada a servicios externos.
