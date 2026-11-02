# Glosario de la unidad 011

Las definiciones de una línea aparecen en cada cuaderno, en el lugar donde se usa el término por primera vez. Esta lista las reúne para consultarlas sin buscar. Entre paréntesis, el cuaderno donde se explica.

## Los datos y el modelo

| Término | Qué es |
|---|---|
| **Token** | Unidad de texto que procesa el modelo: una palabra, un pedazo de palabra o un signo. (01) |
| **Vector** | Lista ordenada de números. (01) |
| **Embedding** | El vector que representa a un token dentro del modelo. (01) |
| **Dimensión** | Cada uno de los números de un vector. BETO usa 768; los ejemplos de la unidad, 2 o 4. (01) |
| **Vocabulario** | Conjunto de tokens que el modelo conoce o puede producir. (03) |
| **Posición** | Vector que indica el lugar de un token en la oración y se suma a su embedding. (03) |
| **Datos sintéticos** | Números inventados para mostrar un mecanismo; no describen el comportamiento de un modelo real. (01) |

## Pesos y capas

| Término | Qué es |
|---|---|
| **Red neuronal** | Programa hecho de capas de operaciones con números que se ajustan a partir de ejemplos. (01) |
| **Transformer** | Tipo de red neuronal pensado para procesar secuencias; BETO y GPT lo son. (01) |
| **Neurona o capa lineal** | Operación que multiplica cada número de un vector por un peso y suma un sesgo. (01) |
| **Peso (parámetro)** | Número que el entrenamiento ajusta y que después queda fijo. No cambia con el texto. (01) |
| **Sesgo** | Número fijo que se suma al resultado de una neurona. (01) |
| **Pesos de atención** | Números que el modelo calcula de nuevo para cada oración y que reparten el contexto entre los tokens. No son los pesos del modelo. (02) |
| **RNN (red recurrente)** | Red que lee el texto de a un token y pasa un estado de un paso al siguiente. (01) |

## Atención

| Término | Qué es |
|---|---|
| **Atención** | Cálculo que le asigna un peso a cada token del contexto para mezclar su información. (02) |
| **Consulta, clave y valor (query, key, value)** | Tres papeles de cada token: lo que busca, lo que ofrece para ser comparado y la información que aporta. (02) |
| **Producto punto** | Se multiplican de a pares los números de dos vectores y se suman. En NumPy: `@`. (02) |
| **Puntaje** | Resultado de comparar una consulta con una clave. (02) |
| **Softmax** | Convierte puntajes en pesos positivos que suman 1. (02) |
| **Vector de contexto** | Suma de los vectores del contexto, cada uno multiplicado por su peso. (02) |
| **Matriz de atención** | Una fila de pesos por cada token que consulta. (02) |
| **Máscara causal** | Impide que un token use los que vienen después. (02) |
| **Autorregresivo** | Que produce un token por vez y usa los anteriores para el siguiente. (02) |
| **Decoder-only** | Modelo autorregresivo, como GPT, que solo mira lo anterior. BETO, en cambio, lee la oración completa. (02) |
| **Cabeza de atención** | Juego completo de matrices de consulta, clave y valor. Un modelo usa varias en paralelo. (03) |

## Del bloque al próximo token

| Término | Qué es |
|---|---|
| **Bloque** | Conjunto de piezas que el modelo repite: atención, suma residual, normalización y red feed-forward. (02, 03) |
| **Suma residual** | Se le suma a la salida de una pieza lo que esa pieza recibió. (03) |
| **Normalización** | Reescala los números de un vector para que no crezcan de bloque en bloque. (03) |
| **Red feed-forward** | Pequeña red que transforma cada posición por separado. (03) |
| **Capa de salida** | Multiplica el vector del último token por una matriz con una columna por palabra del vocabulario. (03) |
| **Logit** | Puntaje sin normalizar de una palabra del vocabulario. (03) |
| **Distribución de probabilidad** | Probabilidades positivas que suman 1; softmax la produce a partir de los logits. (03) |
