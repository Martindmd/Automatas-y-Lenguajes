# Prácticas de Autómatas y Lenguajes. Curso 2026/27

## Práctica 3: Análisis Sintáctico y Semántico

**Duración:** 4 semanas.  
**Entrega:** fecha indicada en Moodle, antes de clase y del control correspondiente.  
**Peso:** 45% de la nota de prácticas.

### Descripción del enunciado

En esta práctica estudiaremos distintos conceptos relacionados con el análisis sintáctico y semántico. Empezaremos con nuestra propia implementación de un analizador sintáctico (descendente) para gramáticas LL(1) y posteriormente utilizaremos las herramientas del módulo `ply` (Python Lex-Yacc) de Python para construir parsers de análisis sintáctico (ascendente) para GIC extendidas con gramáticas de atributos.

Los objetivos de la práctica son:

- Calcular los conjuntos primero y siguiente de los símbolos no terminales de una gramática.
- Construir la tabla de análisis para un analizador sintáctico descendente LL(1) a partir de los conjuntos primero y siguiente de la gramática.
- Entender y programar el algoritmo de análisis sintáctico descendente LL(1) a partir de la descripción de la tabla de análisis.
- Construir parsers LALR con gramáticas de atributos utilizando Lex-Yacc, y entender qué características hacen que una gramática sea apropiada para un análisis LALR.

Se recuerda que los objetivos de aprendizaje planteados deben ser adquiridos por ambos miembros de la pareja. Se realizará un control para comprobarlo y, si este no es el caso en algún miembro de la pareja, se le suspenderá la práctica con una evaluación de NO APTO.

### Descripción de los ficheros suministrados

Se facilitan los siguientes ficheros para los ejercicios 1–4:

- `src/grammar.py`: contiene, entre otras, las clases `Grammar` y `LL1Table`, que deberán completarse con los métodos pedidos.
- `src/utils.py`: contiene funciones de utilidad para leer una gramática a partir de su descripción y representar tablas y árboles. No se debe modificar ni entregar este fichero.
- `test_analyze.py`, `test_first.py`, `test_follow.py`, `test_ll1_table.py` y `test_contracts.py`: contienen tests de ejemplo en formato `unittest`, útiles como punto de partida para desarrollar nuevos tests.

Para los ejercicios 5–6 se facilitarán posteriormente `src/g1_lexer.py`, `src/g1_parser.py`, `src/json_lexer.py`, `src/json_parser.py`, `test_g1.py` y `test_json.py`. Los analizadores léxicos, la configuración de PLY y las funciones de entrada se suministrarán preparados. Las interfaces y el comportamiento exigido son los descritos en este enunciado.

Utilizad Python 3.10 o posterior. Desde el directorio del material, los tests LL(1) se ejecutan con:

```bash
python3 -m unittest discover -v
```

Los métodos pendientes lanzan inicialmente `NotImplementedError`: es normal que los tests fallen antes de completar los ejercicios. No es necesario tener PLY instalado para trabajar en los ejercicios 1–4. Para los ejercicios 5–6 será necesario el módulo `ply`.

Los ejemplos facilitados no son exhaustivos. Añadid al menos **dos casos nuevos por ejercicio de programación (1–5, 6.1 y 6.2)**, incluyendo casos límite o incorrectos, y explicad brevemente en los tests qué comprueba cada uno. No eliminéis ni alteréis las expectativas de los tests suministrados.

### Convenciones para los ejercicios 1–4

Se conserva la representación proporcionada: cada símbolo terminal o no terminal es una cadena de un carácter; las partes derechas son cadenas de símbolos. La producción vacía se representa con `""`. El símbolo `$` se reserva para el fin de entrada y no forma parte de las producciones de la gramática.

Los métodos deben conservar sus nombres y argumentos. Podéis añadir métodos auxiliares y atributos, incluyendo conjuntos precomputados, sin modificar las interfaces ni `utils.py`. Los algoritmos de primero y siguiente deben funcionar también con producciones recursivas y ciclos: no se supone que la gramática sea LL(1) para calcular estos conjuntos.

## Ejercicio 1: Análisis sintáctico descendente (2 puntos)

En este ejercicio se implementará el algoritmo de análisis sintáctico descendente LL(1) a partir de una tabla de análisis dada. Para ello es necesario completar el método `analyze` de la clase `LL1Table` en `grammar.py`. El método recibe la cadena a analizar, `input_string`, y el axioma o símbolo inicial, `start`. Debe devolver un árbol de derivación si la cadena es sintácticamente correcta de acuerdo con la tabla, o generar una excepción de tipo `SyntaxError` si no lo es.

Se utiliza la excepción `SyntaxError` definida en `src/grammar.py`. El argumento `start` debe ser un no terminal de la tabla; en otro caso se lanzará `ValueError`.

La cadena de entrada debe incluir **exactamente un `$` al final**, por ejemplo `"i+i$"`. La palabra vacía se pasa como `"$"`. Una entrada sin ese marcador, con marcadores repetidos, con símbolos desconocidos o con contenido después de `$` debe rechazarse. La tabla suministrada incluye la columna `$`.

La construcción del árbol es obligatoria. Los hijos se ordenan como los símbolos de la parte derecha aplicada; una producción vacía genera un único hijo `ParseTree("")`. El marcador `$` no se incluye en el árbol. Por ejemplo, para la gramática `S -> aS | λ`, la entrada `"a$"` produce:

```python
ParseTree("S", [ParseTree("a"), ParseTree("S", [ParseTree("")])])
```

En `test_analyze.py` y `test_contracts.py` se facilitan tests. Recordad que es vuestra responsabilidad realizar tests adicionales.

## Ejercicio 2: Cálculo del conjunto primero (1 punto)

Se debe completar, en la clase `Grammar`, el método `compute_first`, que calcula el conjunto primero para una determinada cadena recibida como argumento (`sentence`). Esta cadena debe estar formada únicamente por símbolos terminales y no terminales de la gramática. En caso contrario, el método deberá lanzar `ValueError`, incluso si el símbolo incorrecto aparece después de un prefijo no anulable.

El método debe devolver un conjunto con todos los símbolos contenidos en primero de la cadena, siendo cada símbolo una cadena de un carácter, o la cadena vacía si λ pertenece a dicho conjunto. En particular, `compute_first("")` devuelve `{""}`.

En `test_first.py` y `test_contracts.py` se facilitan tests. Tanto en este ejercicio como en el siguiente, es recomendable computar una sola vez los valores de primero y siguiente necesarios y usar estos valores precomputados para las consultas. Recordad comprobar la convergencia de los cálculos cuando hay recursión.

## Ejercicio 3: Cálculo del conjunto siguiente (1,5 puntos)

Se debe completar, en la clase `Grammar`, el método `compute_follow`, que calcula el conjunto siguiente para un símbolo no terminal recibido como argumento (`symbol`). El método debe generar `ValueError` si el argumento no pertenece al conjunto de símbolos no terminales de la gramática.

En caso contrario devolverá un conjunto con todos los símbolos contenidos en siguiente, siendo cada símbolo una cadena de un carácter, que puede incluir el carácter de fin de cadena `$`. Este conjunto nunca contiene `""`. El conjunto siguiente del axioma incluye `$`.

En `test_follow.py` y `test_contracts.py` se facilitan tests. Considerad todas las apariciones de un no terminal en una parte derecha y los sufijos que pueden generar la palabra vacía.

## Ejercicio 4: Cálculo de la tabla de análisis LL(1) (1,5 puntos)

Completad el método `get_ll1_table` de la clase `Grammar`, que calcula la tabla de análisis LL(1). Debe devolver un objeto `LL1Table`, o `None` si la gramática no es LL(1), es decir, si hay distintas partes derechas en una misma casilla.

Las filas corresponden a los no terminales y las columnas a los terminales y `$`. Una casilla sin producción contiene `None`; una producción vacía se representa con `""`. Considerad tanto los conflictos entre conjuntos primero como los que aparecen por producciones anulables y conjuntos siguiente. Se supone que las listas de producciones no contienen duplicados idénticos.

En `test_ll1_table.py` se comprueban directamente las casillas y la detección de conflictos. `test_analyze.py` incluye además comprobaciones conjuntas de construcción de tabla y análisis.

## Ejercicio 5: Implementar un parser LALR con gramática de atributos (1 punto)

Completad, en `g1_parser.py`, las acciones semánticas para implementar el parser y la gramática de atributos para el lenguaje:

$$L = \{a^n b^n c^k \mid n \geq 0,\ k \geq n+1\}.$$

Se debe incluir atributos para los símbolos no terminales. Se suministrará la siguiente gramática sintáctica; la condición sobre los contadores se comprobará mediante atributos:

```text
Language -> A B C
A        -> a A | λ
B        -> b B | λ
C        -> c C | λ
```

La llamada `parser.parse(texto)` devolverá `True` si la entrada pertenece al lenguaje y `False` en otro caso, incluidos los errores léxicos y sintácticos. Se ignorarán espacios, tabuladores y saltos de línea. No se añade `$` a las entradas de PLY.

Por ejemplo, `"c"`, `"abcc"` y `"aabbccc"` son válidas; `""`, `"aabbcc"`, `"acc"`, `"abaaabbccc"` y `"ab?cc"` no lo son. Un error no permite aceptar únicamente un sufijo válido de la entrada. Las llamadas sucesivas deben ser independientes.

La infraestructura suministrada gestionará los errores y el estado entre llamadas. En `test_g1.py` se facilitarán tests de ejemplo.

## Ejercicio 6: Análisis LALR de JSON simplificado y estudio de conflictos (3 puntos)

### Parte 1: Parser y construcción de valores (1 punto)

Completad las reglas y acciones semánticas de `json_parser.py` para analizar el siguiente subconjunto de JSON. El objetivo es construir valores de Python mediante atributos sintetizados de la gramática.

```text
value   -> object | array | STRING | NUMBER | TRUE | FALSE | NULL
object  -> { } | { members }
members -> pair | members , pair
pair    -> STRING : value
array   -> [ ] | [ elements ]
elements -> value | elements , value
```

El símbolo inicial es `value`: la entrada puede ser un objeto, un array o un valor primitivo. En esta notación, `{`, `}`, `[`, `]`, `,` y `:` son terminales; `|` separa alternativas. Las llaves y corchetes vacíos representan objetos y arrays vacíos, respectivamente.

El analizador léxico suministrado reconocerá:

- `STRING`: texto entre comillas dobles. El contenido puede estar vacío y puede contener caracteres Unicode y espacios, pero no comillas dobles, barras inversas ni caracteres de control U+0000–U+001F. **No se admiten secuencias de escape.** El token contiene la cadena sin comillas.
- `NUMBER`: números de la forma `-?(0|[1-9][0-9]*)(\.[0-9]+)?`. No se admiten signo `+`, ceros iniciales, exponentes ni decimales sin cifras a ambos lados del punto. El token contiene un `int` si no hay punto, y un `float` si lo hay. Los datos y tests utilizarán números de magnitud representable como valores finitos de Python.
- `TRUE`, `FALSE` y `NULL`: las palabras `true`, `false` y `null`, en minúsculas.
- Los seis signos de puntuación de la gramática. Fuera de las cadenas se ignoran únicamente espacio, tabulador, retorno de carro y salto de línea. No se admiten comentarios.

La llamada `parser.parse(texto)` debe devolver el valor Python correspondiente:

| Construcción | Resultado |
| --- | --- |
| Objeto | `dict` con claves `str` |
| Array | `list`, conservando el orden |
| Cadena | `str` |
| Número sin/con punto | `int` / `float` |
| `true`, `false`, `null` | `True`, `False`, `None` |

Por ejemplo:

```text
Entrada: {"title": "Toy Story", "genres": ["Animation", "Comedy"], "rating": null}
```

```python
# Resultado:
{"title": "Toy Story", "genres": ["Animation", "Comedy"], "rating": None}
```

Se permiten objetos y arrays anidados y arrays con elementos de distintos tipos. Debéis construir el resultado en las acciones semánticas de PLY: no se permite delegar el análisis en `json.loads`, `eval`, `ast.literal_eval`, otra biblioteca ni un parser alternativo. Sí podéis usar `json.loads` en vuestros tests para comparar resultados de entradas válidas de este subconjunto.

### Parte 2: Validación y casos incorrectos (1 punto)

El parser debe consumir la entrada completa. Una entrada mal formada debe lanzar la excepción **incorporada de Python `SyntaxError`**, no devolver un valor parcial. La infraestructura suministrada hará esta gestión en los errores léxicos y sintácticos; vuestras reglas deben respetar la gramática y no aceptar construcciones adicionales.

Además, como restricción semántica de esta práctica, **no se permiten claves duplicadas dentro de un mismo objeto**. Detectadlas en las acciones semánticas y lanzad `ValueError`. Una misma clave en objetos diferentes sí está permitida. Esta es una política del ejercicio, no una afirmación de que todos los analizadores JSON rechacen duplicados.

Ejemplos:

| Entrada | Resultado esperado |
| --- | --- |
| `{}` | `{}` |
| `[]` | `[]` |
| `null` | `None` (resultado válido) |
| `{"a": [1, -2.5, true, null]}` | Diccionario con la lista correspondiente |
| `{"a": {"a": 1}}` | Válida: las claves están en objetos distintos |
| `{"a": 1, "a": 2}` | `ValueError` |
| `{"a": 1,}` | `SyntaxError` |
| `[1,]` | `SyntaxError` |
| `{"a" 1}` | `SyntaxError` |
| `01`, `1e3`, `+1` | `SyntaxError` |
| `{} []` | `SyntaxError`: dos valores completos |
| Entrada vacía o solo espacios | `SyntaxError` |

Las llamadas sucesivas deben ser independientes, incluso después de un error. No añadáis `$` al texto. Se facilitarán ejemplos y tests en `test_json.py`; no se requiere MongoDB, un validador de esquemas ni un dataset externo. La solución debe funcionar con cualquier entrada del subconjunto especificado.

### Parte 3: Diferencias entre gramáticas (1 punto)

Consideraremos dos gramáticas para el fragmento de unidades de los números romanos. Este apartado es teórico: **no hay que implementar parsers de números romanos**.

```text
G1 (recursión izquierda)             G2 (recursión derecha)
Units -> LowUnits                   Units -> LowUnits
Units -> I V                        Units -> I V
Units -> V LowUnits                 Units -> V LowUnits
Units -> I X                        Units -> I X
LowUnits -> LowUnits I | λ           LowUnits -> I LowUnits | λ
```

Los terminales son `I`, `V` y `X`; el axioma es `Units`. Para este análisis se consideran exactamente las producciones escritas, sin añadir la restricción semántica de tres repeticiones.

Responded en `Memoria.pdf`:

1. Construye los conjuntos primero y siguiente de los no terminales de ambas gramáticas.
2. Para ambas gramáticas, construye el estado inicial del autómata **LR(1) canónico**, aumentando la gramática con `S' -> Units`, y todos los estados a los que se llega mediante una transición desde el inicial. Indica las transiciones y los símbolos de anticipación de los ítems. No es necesario construir el resto del autómata.
3. Rellena las entradas de la tabla ACTION/GOTO que pueden determinarse con esos estados. Para desplazamientos cuyo destino quede fuera del fragmento dibujado, basta indicar «desplazar». ¿Existen conflictos? ¿De qué tipo? Explica qué permite concluir encontrar un conflicto en este fragmento y qué **no** permite concluir su ausencia.
4. Explica el efecto del conflicto inicial de G1 al analizar `I` frente a `IV`, suponiendo que se resuelve a favor de desplazar. Relaciónalo con la producción vacía y el símbolo de anticipación. No concluyas que toda recursión izquierda es inadecuada para LR.

Los ficheros `parser.out` que genera PLY describen un analizador **LALR**, no el autómata LR(1) canónico solicitado. Podéis usarlos como apoyo si construís ejemplos por vuestra cuenta, pero no son necesarios ni sustituyen la justificación anterior.

## Planificación

| Trabajo | Semana |
| --- | --- |
| Ejercicios 1 y 2 | 1 |
| Ejercicios 3 y 4 | 2 |
| Ejercicio 5 y comienzo del 6 (parser JSON) | 3 |
| Ejercicio 6 (validación, tests y memoria) | 4 |

## Normas de entrega

La entrega la realizará un solo miembro de la pareja a través de Moodle. Entregad un ZIP `P3_AUTLEN_26_27_GXXXX_PYY.zip`, con un único directorio del mismo nombre sin la extensión, donde XXXX es el número de grupo e YY el número de pareja. Debe contener:

- `src/grammar.py`, para los ejercicios 1–4.
- `src/g1_parser.py` y `src/json_parser.py`, para los ejercicios 5–6. En estos dos ficheros completad las reglas y acciones indicadas; podéis añadir auxiliares para las acciones, pero no modificar los analizadores léxicos ni la infraestructura suministrada.
- `src/__init__.py` y los ficheros de tests con vuestros casos adicionales.
- `Memoria.pdf`, con las respuestas al ejercicio 6, parte 3.

Incluid los nombres de ambos miembros en un comentario de los ficheros entregados. No entreguéis `utils.py`, los lexers, entornos de Python, cachés ni los ficheros generados `parser.out` y `parsetab*.py`. Para ejecutar localmente los tests sí deben permanecer disponibles las utilidades y lexers suministrados.

Los ejercicios suman 10 puntos. Se valorarán la corrección, el cumplimiento de las restricciones de implementación, los tests añadidos y las explicaciones. El funcionamiento de un ejercicio se comprobará de forma independiente cuando sea posible; los tests conjuntos servirán también para comprobar la integración. Un error o un límite de tiempo en un caso no conlleva una penalización adicional acumulativa. Los problemas que impidan evaluar una parte requerirán revisión.
