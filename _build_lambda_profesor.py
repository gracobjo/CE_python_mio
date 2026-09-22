# -*- coding: utf-8 -*-
"""Genera CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_PROFESOR.ipynb (nbformat 4)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_PROFESOR.ipynb"


def src(text: str):
    if not text.endswith("\n"):
        text += "\n"
    return [text]


def md(text: str, solo_profesor: bool = False):
    meta = {"solo_profesor": True} if solo_profesor else {}
    return {"cell_type": "markdown", "metadata": meta, "source": src(text)}


def code(text: str, solo_profesor: bool = False):
    meta = {"solo_profesor": True} if solo_profesor else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": meta,
        "outputs": [],
        "source": src(text),
    }


def check_block(fn_call_template: str, casos: list, call_expr: str) -> str:
    """Autocorrección estilo referencia. call_expr usa _entrada (puede ser tupla)."""
    lines = ["_casos = ["]
    for entrada, esperado in casos:
        lines.append(f"    ({entrada!r}, {esperado!r}),")
    lines.append("]")
    lines.append("_ok = 0")
    lines.append("for _entrada, _esperado in _casos:")
    lines.append("    try:")
    lines.append(f"        _r = {call_expr}")
    lines.append("    except Exception as _e:")
    lines.append('        print(f"✗ Error al probar {_entrada!r}: {_e}")')
    lines.append("        continue")
    lines.append("    if _r == _esperado:")
    lines.append("        _ok += 1")
    lines.append(f'        print(f"✓ {fn_call_template}")')
    lines.append("    else:")
    lines.append(
        f'        print(f"✗ {fn_call_template}  (esperado {{_esperado!r}})")'
    )
    lines.append('print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")')
    return "\n".join(lines)


def sol_banner():
    return md(
        "**Solución (solo para el profesorado — no se incluye en la versión del alumnado):**",
        solo_profesor=True,
    )


cells = []

# ═══════════════════════════════════════════════════════════════════════════
# CABECERA
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """# Python — Lambda, filter, map, sorted y decoradores

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_PROFESOR.ipynb)

A continuación se desarrollan con **profundidad teórica y práctica** los epígrafes de **programación funcional ligera** (`lambda`, `filter`, `map`, `sorted`) y **decoradores**, como **continuación** del notebook de control de flujo y funciones. Se asume que ya conoces `def`, parámetros, ámbito LEGB, closures básicas y `match`/`case`.

Cada epígrafe incluye: **conceptos clave**, **explicación razonada**, **práctica guiada ejecutable**, **errores frecuentes**, **batería de test de nivel examen** y **ejercicio propuesto con comprobación automática**.

Este cuaderno es la **versión del profesorado**: incluye soluciones completas. Esas celdas van marcadas con:

**Solución (solo para el profesorado — no se incluye en la versión del alumnado):**

### Qué vas a conseguir con este material

1. Entender `lambda` como expresión callable, no como «atajo mágico».
2. Usar `filter` y `map` sabiendo que son **iteradores perezosos**.
3. Dominar `sorted` con `key` y ordenaciones multi-criterio.
4. Construir decoradores (simples, con parámetros y apilados).
5. Reconocer patrones reales: logging, cronómetro, auth, caché, reintentos…
6. Comprobar automáticamente las soluciones.
7. Preparar preguntas de examen de nivel difícil.

### Requisitos

- Python **3.10 o superior** (`match` / `case` en algún ejemplo).
- Solo biblioteca estándar: **no** hace falta pandas, numpy ni frameworks web."""
    )
)

cells.append(
    md(
        """---
## Cómo usar este notebook

1. Ejecuta primero la celda de **comprobación del intérprete**.
2. Estudia cada epígrafe en orden: primero teoría, después práctica.
3. **Predice** el resultado de los ejemplos antes de ejecutarlos.
4. Completa los ejercicios donde pone `# TODO` o `...`.
5. No modifiques las celdas de comprobación: ellas te dicen cuántos casos has acertado.
6. Si un ejercicio no pasa, lee de nuevo la explicación razonada y los errores frecuentes **antes** de mirar la solución.

> **Consejo de estudio**: las preguntas tipo test no preguntan «qué palabra clave se usa». Preguntan qué objeto devuelve `filter`, si un `lambda` puede llevar sentencias, en qué orden se aplican varios `@decorador`, o qué captura un closure."""
    )
)

cells.append(
    md(
        """---
## Índice

### Parte I — Funciones funcionales

1. `lambda`
2. `filter`
3. `map`
4. `sorted`

### Parte II — Decoradores

5. Funciones como objetos (repaso)
6. Funciones que devuelven funciones
7. Primer decorador
8. Decoradores con parámetros
9. Múltiples decoradores
10. Decoradores aplicados a operaciones aritméticas

### Parte III — Casos de uso reales de decoradores

11. Logging  
12. Cronómetro  
13. Autenticación  
14. Validación  
15. Reintentos  
16. Caché  
17. Rate limiting  
18. Debugging  

### Parte IV — Ejercicios integradores"""
    )
)

cells.append(
    md(
        """---
## Configuración inicial — Comprobación del intérprete

Este material usa Python estándar (3.10+). No se instalan librerías externas.

Ejecuta la siguiente celda y comprueba que el kernel es **3.10 o superior**.

- **Colab:** el runtime por defecto ya sirve; no instales paquetes.
- **Jupyter / VS Code / Cursor:** si la versión es baja, cámbiala en **Kernel → Change kernel**."""
    )
)

cells.append(
    code(
        """# ── Comprobación del intérprete ──────────────────────────────────────────────
import sys

IN_COLAB = "google.colab" in sys.modules

print(f"Intérprete activo: {sys.executable}")
print(f"Versión Python: {sys.version}")
print(f"Entorno: {'Google Colab' if IN_COLAB else 'local / Jupyter'}")

if sys.version_info < (3, 10):
    print("\\n⚠ AVISO: este cuaderno usa match/case (Python 3.10+).")
    if IN_COLAB:
        print("  En Colab: Entorno de ejecución → Cambiar tipo de entorno de ejecución.")
    else:
        print("  Cambia el kernel a un intérprete 3.10 o superior.")
else:
    print("\\n✓ Versión adecuada para match/case y el resto del material.")
    if IN_COLAB:
        print("  Puedes usar Entorno de ejecución → Ejecutar todo. No hay que instalar librerías.")"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# PARTE I
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
# PARTE I — FUNCIONES FUNCIONALES

En Python «programación funcional» no significa abandonar objetos: significa **tratar funciones como valores** y transformar datos con operaciones claras (`filtrar`, `mapear`, `ordenar`).

| Herramienta | Pregunta que responde |
|---|---|
| `lambda` | ¿Puedo definir un callable corto *aquí*? |
| `filter` | ¿Qué elementos cumplen el predicado? |
| `map` | ¿Cómo transformo cada elemento? |
| `sorted` | ¿En qué orden debo presentarlos? |

`filter` y `map` **no** materializan listas: devuelven iteradores. Si necesitas reutilizar el resultado, conviértelo con `list(...)` (o genéralo de nuevo)."""
    )
)

# ─── EPÍGRAFE 1 — lambda ───────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 1 — `lambda`

### 1.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **`lambda`** | Expresión que crea una **función anónima** (sin `def` ni nombre obligatorio). |
| **Sintaxis** | `lambda parametros: expresion` — una sola expresión, no un bloque. |
| **Callable** | El resultado de evaluar `lambda` es un objeto función; se puede llamar. |
| **Closure** | Una `lambda` puede capturar variables del ámbito envolvente. |
| **Uso típico** | Argumento `key=` de `sorted`, predicado de `filter`, transformación de `map`. |
| **Límite** | No admite sentencias (`return`, `if` de bloque, bucles, asignaciones). |

```python
f = lambda x: x * 2          # equivalente corto a def f(x): return x * 2
mayor = lambda a, b: a if a > b else b
```

`lambda` **no** es más rápida que `def`. Es más **local**: declara intención en el punto de uso."""
    )
)

cells.append(
    md(
        """### 1.2 Explicación razonada

#### Qué ocurre

Al evaluar `lambda x: x * n`, Python crea un objeto función. Los parámetros se enlazan en la llamada; el cuerpo es **una expresión** cuyo valor se convierte en el retorno implícito.

#### Por qué ocurre

`def` es una **sentencia**: introduce un nombre en el ámbito. `lambda` es una **expresión**: produce un valor callable allí donde hace falta uno (como argumento). Por eso encaja en `sorted(..., key=...)`.

#### Closures con `lambda`

```python
def crear_multiplicador(n):
    return lambda x: x * n   # captura n del ámbito de crear_multiplicador
```

Cada llamada a `crear_multiplicador` crea un closure distinto. `duplicar` y `triplicar` no comparten el mismo `n`.

#### Cuándo usar `lambda`

- Predicados o claves de una sola expresión.
- Transformaciones triviales en `map`/`filter`.
- Callbacks cortos donde un `def` nombrado ensuciaría el código.

#### Cuándo NO usarlo

- Lógica con varias sentencias o manejo de errores.
- Cuando necesitas documentación, tipado rico o depuración cómoda (el nombre ayuda).
- Cuando la expresión supera ~1 línea legible: usa `def`.

#### Detalle de examen

`lambda x: print(x)` **sí** es válida, pero `print` devuelve `None`. La lambda devuelve `None`, no el texto impreso. Confundir efecto lateral con valor de retorno es un error clásico."""
    )
)

cells.append(md("### 1.3 Práctica guiada\n\nPredice cada `print` **antes** de ejecutar. Observa closures y ternarios dentro de `lambda`."))

cells.append(
    code(
        """# ── Práctica guiada 1 — lambda ───────────────────────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) Lambda básica
cuadrado = lambda x: x ** 2
print("cuadrado(5) →", cuadrado(5))
print("tipo →", type(cuadrado))

# 2) Par / impar con ternario
es_par_str = lambda n: "Par" if n % 2 == 0 else "Impar"
for num in [4, 7, 10]:
    print(f"{num} → {es_par_str(num)}")

# 3) Mayor de dos
obtener_mayor = lambda a, b: a if a > b else b
print("mayor(15, 42) →", obtener_mayor(15, 42))

# 4) CÓDIGO USUARIO — closures con lambda
def crear_multiplicador(n):
    return lambda x: x * n

duplicar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)
print(duplicar(5))
print(triplicar(5))

# 5) lambda que «parece» devolver el print… pero retorna None
resultado = (lambda x: print(x))(99)
print("valor retornado por lambda x: print(x) →", resultado)"""
    )
)

cells.append(
    md(
        """### 1.4 Errores frecuentes

**1. Meter sentencias dentro de `lambda`**

INCORRECTO:
```python
lambda x:
    y = x + 1
    return y
```

CORRECTO: usa `def`, o reduce a una expresión: `lambda x: x + 1`.

**2. Confundir `print` con valor de retorno**

INCORRECTO (si esperabas el número):
```python
f = lambda x: print(x)
valor = f(3)   # valor es None
```

CORRECTO: `f = lambda x: x` (o imprime *después* de llamar).

**3. Lambda «compleja» ilegible**

INCORRECTO:
```python
clave = lambda a: a["notas"][0] if a.get("notas") else (-1 if a.get("edad", 0) < 18 else 0)
```

CORRECTO: `def clave(a): ...` con nombre y varias líneas.

**4. Pensar que `lambda` es un tipo distinto**

`type(lambda x: x)` es `function`, igual que un `def`. Solo cambia cómo se crea."""
    )
)

cells.append(
    md(
        """### 1.5 Test (10 preguntas)

1. ¿Qué imprime `print((lambda x: x + 1)(4))`?

a) `<function ...>`
**b) `5`**
c) `None`
d) `SyntaxError`

2. ¿Cuál es válida?

a) `lambda x: return x`
**b) `lambda x: x * 2`**
c) `lambda x: y = x`
d) `lambda x:\\n    print(x)`

3. Tras `f = crear_multiplicador(3)` con el patrón del epígrafe, ¿qué es `f(4)`?

a) `3`
**b) `12`**
c) `lambda`
d) `TypeError`

4. ¿Qué devuelve `(lambda x: print(x))(1)` además de imprimir?

a) `1`
**b) `None`**
c) `"1"`
d) Lanza error

5. ¿Para qué sirve típicamente `lambda` en `sorted`?

a) Ordenar in-place
**b) Definir la clave de comparación como expresión**
c) Convertir a tupla
d) Filtrar elementos

6. ¿`lambda` es más rápida que `def` equivalente?

a) Siempre sí
**b) No: la diferencia no es el motivo de usarla**
c) Solo en CPython 3.12+
d) Solo si no hay closure

7. ¿Qué captura `return lambda x: x * n` dentro de `crear_multiplicador(n)`?

a) Nada: `n` debe ser global
**b) El valor de `n` del ámbito envolvente (closure)**
c) Solo literales
d) Una copia de la lista de argumentos

8. ¿Puede una `lambda` tener cero parámetros?

a) No
**b) Sí: `lambda: 42`**
c) Solo en `map`
d) Solo con `*` 

9. ¿Qué falla en `lista.sort(key=lambda a, b: a - b)` estilo `cmp` de Python 2?

a) Nada
**b) `key` recibe un elemento, no dos (no es función de comparación binaria)**
c) `sort` no admite `key`
d) `lambda` no admite dos parámetros

10. Mejor refactor si la lambda ocupa tres operadores anidados ilegibles:

a) Más lambdas anidadas
**b) Un `def` con nombre claro**
c) `eval`
d) Quitar el `key`"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 1 — area_triangulo

Define una **lambda** `area_triangulo` con parámetros `base` y `altura` que calcule `(base * altura) / 2`.

Casos esperados: `(10, 5) → 25.0`, `(0, 5) → 0.0`, `(8, 3) → 12.0`."""
    )
)

_ex1_todo = '''area_triangulo = None  # TODO: lambda base, altura: ...

_casos = [
    ((10, 5), 25.0),
    ((0, 5), 0.0),
    ((8, 3), 12.0),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = area_triangulo(*_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ area_triangulo{_entrada!r} = {_r!r}")
    else:
        print(f"✗ area_triangulo{_entrada!r} = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex1_sol = '''area_triangulo = lambda base, altura: (base * altura) / 2

_casos = [
    ((10, 5), 25.0),
    ((0, 5), 0.0),
    ((8, 3), 12.0),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = area_triangulo(*_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ area_triangulo{_entrada!r} = {_r!r}")
    else:
        print(f"✗ area_triangulo{_entrada!r} = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex1_todo))
cells.append(sol_banner())
cells.append(code(_ex1_sol, solo_profesor=True))

# ─── EPÍGRAFE 2 — filter ───────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 2 — `filter`

### 2.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **`filter(func, iterable)`** | Conserva elementos para los que `func(elem)` es **truthy**. |
| **Predicado** | Función que, dado un elemento, responde sí/no (truthiness). |
| **Objeto `filter`** | Iterador perezoso; **no** es una lista hasta `list(...)`. |
| **`filter(None, it)`** | Conserva elementos truthy (quita `0`, `''`, `None`, …). |
| **Equivalente** | `(x for x in iterable if func(x))` — comprensión/generador. |

```python
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))  # [2, 4]
```"""
    )
)

cells.append(
    md(
        """### 2.2 Explicación razonada

#### Qué ocurre

`filter` no recorre el iterable al crearse. Cada vez que pides el siguiente elemento, aplica el predicado. Por eso `print(filter(...))` muestra un objeto, no los valores.

#### Por qué ocurre

El diseño perezoso evita construir listas intermedias enormes. Encaja con pipelines `filter` → `map` → consumo.

#### Truthiness del predicado

`def es_par(x): return not (x % 2)` aprovecha que `0` es falsy: si `x` es par, `x % 2` es `0`, `not 0` es `True`.

Cuidado: devolver `0`/`1` como en `longitud_hasta5` también funciona por truthiness, pero es menos legible que `return len(x) <= 5`.

#### Cuándo usar `filter`

- Selección por condición reutilizable.
- Pipelines funcionales cortos.
- Cuando el predicado ya existe (`str.isdigit`, función de dominio).

#### Cuándo NO usarlo

- Si vas a materializar siempre y la comprensión es más clara: `[x for x in datos if ...]`.
- Si necesitas índices o `enumerate` complejo: un `for` explícito suele ser mejor."""
    )
)

cells.append(md("### 2.3 Práctica guiada\n\nObserva el **tipo** del objeto `filter` antes de convertirlo a lista."))

cells.append(
    code(
        """# ── Práctica guiada 2 — filter ───────────────────────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — pares
def es_par(x):
    return not (x % 2)

numeros = [2, 4, 3, 5, 6, 7, 9, 1, 8]
print(type(filter(es_par, numeros)))
print(filter(es_par, numeros))
print(list(filter(es_par, numeros)))

# 2) CÓDIGO USUARIO — longitud <= 5
def longitud_hasta5(x):
    return 0 if len(x) > 5 else 1

palabras = ["bicicleta", "casa", "boligrafo", "cena", "bocadillo", "placa"]
print(list(filter(longitud_hasta5, palabras)))
print(list(filter(lambda x: 0 if len(x) > 5 else 1, palabras)))

# 3) Emails «con @ y dominio con punto»
correos = ["ana@mail.com", "invalido", "luis@empresa.es", "a@b", "ok@x.org"]
emails = list(filter(lambda e: "@" in e and "." in e.split("@")[-1], correos))
print("emails →", emails)

# 4) Aprobados (nota >= 5)
alumnos_notas = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Pedro", "nota": 6},
]
aprobados = list(filter(lambda a: a["nota"] >= 5, alumnos_notas))
print("aprobados →", [a["nombre"] for a in aprobados])"""
    )
)

cells.append(
    md(
        """### 2.4 Errores frecuentes

**1. Olvidar `list(...)` y creer que `filter` es la lista**

INCORRECTO (para reutilizar):
```python
f = filter(es_par, numeros)
print(list(f))
print(list(f))   # segunda vez: vacío
```

CORRECTO: materializa una vez, o vuelve a crear el `filter`.

**2. Predicado que siempre es truthy**

INCORRECTO:
```python
filter(lambda x: print(x), datos)  # print → None → todo se descarta
```

**3. Confundir `filter` con `map`**

`filter` **elige**; `map` **transforma**. Si cambias el valor, usa `map` (o ambos encadenados).

**4. Usar `filter` para «quitar el primero» u operaciones de índice**

Ahí un bucle o slicing es más claro."""
    )
)

cells.append(
    md(
        """### 2.5 Test (10 preguntas)

1. `type(filter(lambda x: True, [1]))` es:

a) `list`
**b) `filter`**
c) `bool`
d) `map`

2. Tras agotar un `filter` con `list(f)`, un segundo `list(f)` suele dar:

a) La misma lista
**b) `[]`**
c) Error
d) Un `map`

3. `list(filter(None, [0, 1, "", "a", None]))` →

a) `[0, 1, "", "a", None]`
**b) `[1, "a"]`**
c) `[0, ""]`
d) Error

4. En `es_par` con `return not (x % 2)`, para `x=4` el predicado es:

a) `0`
**b) `True`**
c) `False`
d) `4`

5. ¿`filter` modifica la lista original?

a) Sí
**b) No**
c) Solo si es `list`
d) Solo con `lambda`

6. Equivalente más idiomático a `list(filter(f, datos))` cuando `f` es simple:

a) `map(f, datos)`
**b) `[x for x in datos if f(x)]`**
c) `sorted(datos, key=f)`
d) `datos.remove(f)`

7. Si el predicado lanza excepción en el 3.er elemento:

a) Se ignora
**b) La excepción aparece al consumir ese elemento**
c) `filter` la captura
d) Devuelve `None`

8. `longitud_hasta5` que devuelve `0` o `1` funciona porque:

a) `filter` exige enteros
**b) `0` es falsy y `1` es truthy**
c) Python convierte a bool solo con `lambda`
d) Es un bug

9. Para filtrar diccionarios por clave `"nota"`:

a) `filter("nota", lista)`
**b) `filter(lambda d: d["nota"] >= 5, lista)`**
c) `map(lambda d: d["nota"], lista)`
d) `sorted(lista)`

10. ¿Por qué `print(filter(...))` no muestra los elementos?

a) Bug de print
**b) Es un iterador; print muestra el objeto, no lo consume como lista**
c) Está vacío
d) Solo funciona en Colab"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 2 — filtrar_primos

Escribe `filtrar_primos(lista)` que devuelva una **lista** con los números primos de `lista` (usa `filter` o equivalente claro; números `< 2` no son primos)."""
    )
)

_ex2_todo = '''def filtrar_primos(lista):
    """Devuelve los primos contenidos en lista."""
    # TODO: implementa aquí tu solución
    ...

_casos = [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 3, 5, 7]),
    ([11, 12, 13], [11, 13]),
    ([0, 1, 4, 9], []),
    ([], []),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = filtrar_primos(_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ filtrar_primos({_entrada!r}) = {_r!r}")
    else:
        print(f"✗ filtrar_primos({_entrada!r}) = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex2_sol = '''def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def filtrar_primos(lista):
    """Devuelve los primos contenidos en lista."""
    return list(filter(es_primo, lista))

_casos = [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 3, 5, 7]),
    ([11, 12, 13], [11, 13]),
    ([0, 1, 4, 9], []),
    ([], []),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = filtrar_primos(_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ filtrar_primos({_entrada!r}) = {_r!r}")
    else:
        print(f"✗ filtrar_primos({_entrada!r}) = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex2_todo))
cells.append(sol_banner())
cells.append(code(_ex2_sol, solo_profesor=True))

# ─── EPÍGRAFE 3 — map ──────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 3 — `map`

### 3.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **`map(func, iterable, ...)`** | Aplica `func` a cada elemento; con varios iterables, empareja en paralelo. |
| **Objeto `map`** | Iterador perezoso (como `filter`). |
| **Aridad** | Con 2 iterables, `func` debe aceptar 2 argumentos, etc. |
| **Longitud** | Se detiene al agotar el iterable **más corto**. |
| **Equivalente** | `(func(x) for x in iterable)` o comprensión. |

```python
list(map(lambda x: x * x, [1, 2, 3]))           # [1, 4, 9]
list(map(lambda x, y: x - y, [4, 8], [3, 5]))  # [1, 3]
```"""
    )
)

cells.append(
    md(
        """### 3.2 Explicación razonada

#### Qué ocurre

`map` guarda la función y los iterables. Al consumir, llama `func(e1)`, `func(e2)`, … o `func(a, b)` si hay dos fuentes.

#### Por qué ocurre

Separa **qué transformación** de **cómo se recorre**. Útil cuando la función ya existe (`str.upper`, `int`, `len`).

#### Cuándo usar `map`

- Transformación uniforme 1-a-1.
- Varias secuencias alineadas (resta elemento a elemento).
- Estilo funcional en pipelines cortos.

#### Cuándo NO usarlo

- Si la transformación tiene ramas complejas: comprensión o `for`.
- Si necesitas filtrar y mapear a la vez: a menudo una comprensión es más legible que `map`+`filter` anidados."""
    )
)

cells.append(md("### 3.3 Práctica guiada\n\nCompara el objeto `map` con su versión materializada en `list`."))

cells.append(
    code(
        """# ── Práctica guiada 3 — map ──────────────────────────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — cuadrado
lista = [1, 2, 3, 4, 5]
print(type(map(lambda x: x*x, lista)))
print(type(list(map(lambda x: x*x, lista))))
print(map(lambda x: x*x, lista))
print(list(map(lambda x: x*x, lista)))

# 2) CÓDIGO USUARIO — resta de dos listas
lista1 = [4, 8, 12, 7]
lista2 = [3, 5, 9, 2]
resultado = list(map(lambda x, y: x - y, lista1, lista2))
print(resultado)  # [1, 3, 3, 5]

# 3) Mayúsculas y longitudes
ciudades = ["sevilla", "zaragoza", "valencia"]
print(list(map(str.upper, ciudades)))
frutas = ["manzana", "pera", "kiwi"]
print(list(map(len, frutas)))

# 4) Celsius → Fahrenheit
celsius = [0, 15, 22, 100]
fahrenheit = list(map(lambda c: round((c * 9/5) + 32, 1), celsius))
print("F →", fahrenheit)"""
    )
)

cells.append(
    md(
        """### 3.4 Errores frecuentes

**1. Olvidar que `map` es perezoso**

INCORRECTO: asumir que `print(map(...))` muestra la lista.

CORRECTO: `print(list(map(...)))`.

**2. Aridad incorrecta con varios iterables**

INCORRECTO:
```python
map(lambda x: x + 1, lista1, lista2)  # TypeError al consumir
```

CORRECTO: `lambda x, y: ...`.

**3. Confundir `map` con efecto lateral**

`list(map(print, datos))` imprime y construye una lista de `None`. Suele ser peor estilo que un `for`.

**4. Encadenar sin materializar y reutilizar**

Igual que `filter`: el iterador se agota."""
    )
)

cells.append(
    md(
        """### 3.5 Test (10 preguntas)

1. `list(map(lambda x: x + 1, [1, 2]))` →

a) `map object`
**b) `[2, 3]`**
c) `[1, 2, 1]`
d) Error

2. Con `map(f, a, b)`, si `len(a)=3` y `len(b)=2`, el resultado tiene:

a) 3 elementos
**b) 2 elementos**
c) 5
d) Error inmediato al crear el map

3. `list(map(str.upper, ["a", "b"]))` →

**a) `["A", "B"]`**
b) `["a", "b"]`
c) `"AB"`
d) Error

4. Diferencia clave `map` vs `filter`:

a) `map` es eager
**b) `map` transforma; `filter` selecciona**
c) `filter` no es iterable
d) Ninguna

5. `type(map(int, ["1"]))` →

a) `list`
**b) `map`**
c) `int`
d) `str`

6. Mejor uso de `map(int, numeros_str)`:

a) Ordenar
**b) Convertir cada cadena a entero**
c) Filtrar no numéricos automáticamente
d) Validar emails

7. `list(map(lambda x, y: x - y, [4, 8], [3, 5]))` →

**a) `[1, 3]`**
b) `[-1, -3]`
c) `[4, 8, 3, 5]`
d) Error

8. ¿`map` altera el iterable original?

a) Sí
**b) No**
c) Solo listas
d) Solo con `lambda`

9. Equivalente a `list(map(f, xs))`:

a) `filter(f, xs)`
**b) `[f(x) for x in xs]`**
c) `sorted(xs, key=f)`
d) `xs.map(f)`

10. ¿Por qué `list(map(print, [1, 2]))` devuelve `[None, None]`?

a) Bug
**b) `print` retorna `None`; map recoge esos retornos**
c) print falla
d) map ignora print"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 3 — formatear_nombres

Escribe `formatear_nombres(lista)` que, con `map`, transforme cada nombre a `"Nombre: X"` donde `X` es `nombre.title()`.

Ejemplo: `["ana", "pedro"]` → `["Nombre: Ana", "Nombre: Pedro"]`."""
    )
)

_ex3_todo = '''def formatear_nombres(lista):
    """Devuelve lista de strings 'Nombre: Titlecase'."""
    # TODO: implementa aquí tu solución
    ...

_casos = [
    (["ana", "pedro", "marta"], ["Nombre: Ana", "Nombre: Pedro", "Nombre: Marta"]),
    (["CARLOS"], ["Nombre: Carlos"]),
    ([], []),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = formatear_nombres(_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ formatear_nombres({_entrada!r}) = {_r!r}")
    else:
        print(f"✗ formatear_nombres({_entrada!r}) = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex3_sol = '''def formatear_nombres(lista):
    """Devuelve lista de strings 'Nombre: Titlecase'."""
    return list(map(lambda n: f"Nombre: {n.title()}", lista))

_casos = [
    (["ana", "pedro", "marta"], ["Nombre: Ana", "Nombre: Pedro", "Nombre: Marta"]),
    (["CARLOS"], ["Nombre: Carlos"]),
    ([], []),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = formatear_nombres(_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ formatear_nombres({_entrada!r}) = {_r!r}")
    else:
        print(f"✗ formatear_nombres({_entrada!r}) = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex3_todo))
cells.append(sol_banner())
cells.append(code(_ex3_sol, solo_profesor=True))

# ─── EPÍGRAFE 4 — sorted ───────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 4 — `sorted`

### 4.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **`sorted(iterable, *, key=None, reverse=False)`** | Devuelve una **nueva lista** ordenada. |
| **`key`** | Callable de **un** argumento; se ordena por `key(elemento)`. |
| **`reverse`** | Si `True`, orden descendente. |
| **Estabilidad** | A igual clave, se conserva el orden relativo original. |
| **`.sort()`** | Método de lista: ordena **in-place** y devuelve `None`. |

```python
sorted([3, 1, 2])
sorted(palabras, key=len)
sorted(numeros, key=lambda x: abs(5 - x))
```"""
    )
)

cells.append(
    md(
        """### 4.2 Explicación razonada

#### Qué ocurre

`sorted` materializa todos los elementos, aplica `key` (si hay), compara y construye una lista nueva. El iterable original no se modifica (salvo que sea la misma lista y uses `.sort()`).

#### Por qué `key` y no `cmp`

Desde Python 3, la API es `key`: más eficiente (la clave se calcula una vez por elemento) y más clara. Para multi-criterio se usa una **tupla de claves** (p. ej. `(-nota, nombre)`).

#### Cuándo usar `sorted`

- Necesitas una lista nueva.
- Ordenar tuplas, sets, dicts (por claves), generadores.
- Ordenaciones por proximidad, longitud, campo de dict, etc.

#### Cuándo NO usarlo

- Si quieres mutar la lista: `lista.sort(...)`.
- Si solo necesitas el mínimo/máximo: `min`/`max` con `key`."""
    )
)

cells.append(md("### 4.3 Práctica guiada\n\nObserva que `sorted` sobre dict ordena **claves**, y que siempre retorna `list`."))

cells.append(
    code(
        """# ── Práctica guiada 4 — sorted ───────────────────────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — lista / tupla / conjunto / dict
print("\\nLista", "-"*100)
lista = [4, 2, 7, 5, 9, 3]
print(sorted(lista))
print(type(sorted(lista)))

print("\\nTupla", "-"*100)
tupla = (4, 2, 7, 5, 9, 3)
print(sorted(tupla))
print(type(sorted(tupla)))  # Devuelve una lista

print("\\nConjunto", "-"*100)
conjunto = {4, 2, 7, 5, 9, 3}
print(sorted(conjunto))
print(type(sorted(conjunto)))  # Devuelve una lista

print("\\nDiccionario", "-"*100)
diccionario = {"c": 3, "a": 1, "b": 2}
print(sorted(diccionario))
print(type(sorted(diccionario)))

# 2) CÓDIGO USUARIO — próximo a cinco
print("\\nNúmeros próximos a 5", "-"*100)

def proximo_a_cinco(x):
    return abs(5-x)

numeros = [7, 2, 9, 1, 5, 10, 4, 3, 8, 6]
print(sorted(numeros, key=proximo_a_cinco))

print("\\nNúmeros próximos a 5 con función lambda", "-"*100)
numeros = [7, 2, 9, 1, 5, 10, 4, 3, 8, 6]
print(sorted(numeros, key=lambda x: abs(5-x)))

# 3) Longitud, lower, tuplas
print(sorted(["elefante", "sol", "mar"], key=len))
print(sorted(["alberto", "Beatriz", "Ana"], key=str.lower))
jugadores = [("Lucas", 850), ("Marina", 990), ("Andrés", 720)]
print(sorted(jugadores, key=lambda j: j[1], reverse=True))"""
    )
)

cells.append(
    md(
        """### 4.4 Errores frecuentes

**1. Usar `cmp` de dos argumentos como `key`**

INCORRECTO: `key=lambda a, b: a - b`.

CORRECTO: `key=lambda x: ...` (un argumento).

**2. Confundir `sorted` con `.sort()`**

```python
r = lista.sort()   # r is None
r = sorted(lista)  # r is list
```

**3. Ordenar tipos mezclados sin clave**

`sorted([1, "a"])` → `TypeError` en Python 3.

**4. Multi-clave mal planteada**

Para «nota descendente, nombre ascendente»: `key=lambda a: (-a["nota"], a["nombre"])`, no dos `sorted` sin cuidado."""
    )
)

cells.append(
    md(
        """### 4.5 Test (10 preguntas)

1. `sorted((3, 1, 2))` devuelve:

a) tupla `(1, 2, 3)`
**b) lista `[1, 2, 3]`**
c) set
d) El mismo objeto tupla

2. `sorted({"b": 2, "a": 1})` →

**a) `["a", "b"]`**
b) `[1, 2]`
c) `[("a", 1), ("b", 2)]`
d) Error

3. Tras `lista.sort()`, el valor de retorno es:

a) la lista
**b) `None`**
c) `True`
d) una copia

4. `key` en `sorted` recibe:

a) Dos elementos a comparar
**b) Un elemento y debe devolver la clave**
c) La lista completa
d) Un booleano

5. `sorted([7, 2, 9], key=lambda x: abs(5 - x))` acerca a 5; el primero es:

**a) `7` o `2` o `9` según distancia — concretamente empieza por el más cercano: `7` y `2` empatan a dist. 2… (estabilidad)**  
En la lista `[7, 2, 9]` distancias `[2, 3, 4]` → **`[7, 2, 9]`**

a) `[9, 7, 2]`
**b) `[7, 2, 9]`**
c) `[2, 7, 9]`
d) `[5, 7, 2]`

6. `reverse=True` con `key=len` ordena:

a) Alfabéticamente
**b) De mayor a menor según la clave**
c) Invierte la lista original sin ordenar
d) Solo números

7. Orden estable significa:

a) Siempre ascendente
**b) A igual clave, se conserva el orden relativo previo**
c) No usa `key`
d) Usa Timsort solo en listas

8. Para ordenar dict por valor:

a) `sorted(d)`
**b) `sorted(d.items(), key=lambda item: item[1])`**
c) `d.sort(key=valor)`
d) `map(sorted, d)`

9. `sorted` vs `filter`:

a) Son lo mismo
**b) `sorted` ordena y materializa lista; `filter` selecciona perezosamente**
c) `filter` ordena
d) `sorted` elimina elementos

10. Multi-criterio típico examen:

a) Dos lambdas en `key`
**b) Devolver una tupla desde `key`**
c) Usar `cmp`
d) Imposible en Python"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 4 — ordenar_por_precio

Escribe `ordenar_por_precio(productos)` que reciba una lista de dicts con claves `"producto"` y `"precio"` y devuelva una **nueva lista** ordenada por precio ascendente."""
    )
)

_ex4_todo = '''def ordenar_por_precio(productos):
    """Ordena productos por precio ascendente (nueva lista)."""
    # TODO: implementa aquí tu solución
    ...

_productos = [
    {"producto": "Teclado", "precio": 79.99},
    {"producto": "Ratón", "precio": 29.50},
    {"producto": "Monitor", "precio": 249.00},
    {"producto": "USB", "precio": 9.99},
]
_casos = [
    (_productos, ["USB", "Ratón", "Teclado", "Monitor"]),
]
_ok = 0
for _entrada, _esperado_nombres in _casos:
    try:
        _r = ordenar_por_precio(_entrada)
        _nombres = [p["producto"] for p in _r]
    except Exception as _e:
        print(f"✗ Error: {_e}")
        continue
    if _nombres == _esperado_nombres:
        _ok += 1
        print(f"✓ orden → {_nombres!r}")
    else:
        print(f"✗ orden → {_nombres!r}  (esperado {_esperado_nombres!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex4_sol = '''def ordenar_por_precio(productos):
    """Ordena productos por precio ascendente (nueva lista)."""
    return sorted(productos, key=lambda p: p["precio"])

_productos = [
    {"producto": "Teclado", "precio": 79.99},
    {"producto": "Ratón", "precio": 29.50},
    {"producto": "Monitor", "precio": 249.00},
    {"producto": "USB", "precio": 9.99},
]
_casos = [
    (_productos, ["USB", "Ratón", "Teclado", "Monitor"]),
]
_ok = 0
for _entrada, _esperado_nombres in _casos:
    try:
        _r = ordenar_por_precio(_entrada)
        _nombres = [p["producto"] for p in _r]
    except Exception as _e:
        print(f"✗ Error: {_e}")
        continue
    if _nombres == _esperado_nombres:
        _ok += 1
        print(f"✓ orden → {_nombres!r}")
    else:
        print(f"✗ orden → {_nombres!r}  (esperado {_esperado_nombres!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex4_todo))
cells.append(sol_banner())
cells.append(code(_ex4_sol, solo_profesor=True))

cells.append(
    md(
        """---
### ✅ Resumen rápido — Parte I

1. `lambda` = expresión callable de **una** expresión.  
2. `filter` / `map` = iteradores; materializa con `list` si reutilizas.  
3. `sorted` = **nueva** lista; `.sort()` muta y retorna `None`.  
4. En examen: pereza, `key` unario, closures con `lambda`."""
    )
)

cells.append(
    code(
        """# ── Autoevaluación rápida Parte I ────────────────────────────────────────────
pares = list(filter(lambda x: x % 2 == 0, range(4)))
cuadrados = list(map(lambda x: x * x, pares))
orden = sorted(cuadrados, reverse=True)
print("pares →", pares)
print("cuadrados →", cuadrados)
print("orden desc →", orden)
assert pares == [0, 2]
assert cuadrados == [0, 4]
assert orden == [4, 0]
print("✓ autoevaluación Parte I OK")"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# PARTE II
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
# PARTE II — DECORADORES

Un **decorador** es una función (u otro callable) que recibe una función y **devuelve otra** (normalmente un envoltorio) que añade comportamiento *antes*, *después* o *en torno* a la original.

En Python, `@decorador` sobre `def f` es azúcar sintáctico de `f = decorador(f)`.

| Pieza | Rol |
|---|---|
| Función como objeto | Se puede asignar, pasar y devolver |
| Función que devuelve función | Base de factories y decoradores |
| Envoltorio (`wrapper`) | Sustituye a la función visible al llamador |
| `functools.wraps` | Preserva `__name__` y docstring de la original |"""
    )
)

# ─── EPÍGRAFE 5 ────────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 5 — Funciones como objetos (repaso)

### 5.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **First-class** | Las funciones son objetos: asignables, almacenables, pasables. |
| **Referencia** | `var = f` no llama a `f`; copia la referencia al objeto función. |
| **Llamada** | `f()` o `var()` ejecutan el cuerpo. |
| **Tabla de despacho** | Un `dict` de nombre → función evita `if`/`match` largos. |

```python
def mi_funcion():
    return "Texto"
var_funcion = mi_funcion
var_funcion()  # "Texto"
```"""
    )
)

cells.append(
    md(
        """### 5.2 Explicación razonada

#### Qué ocurre

`def` enlaza un nombre a un objeto función en el ámbito. Ese objeto tiene atributos (`__name__`, `__doc__`, …) y es callable.

#### Por qué importa para decoradores

El decorador **recibe** ese objeto y **devuelve** otro. Sin funciones-como-valores no hay decoradores.

#### Cuándo usar tablas de funciones

Menús, calculadoras, plugins internos: `operaciones["+"](a, b)`.

#### Cuándo NO

Si cada rama hace algo radicalmente distinto con mucha lógica local, un `match` explícito puede ser más claro."""
    )
)

cells.append(md("### 5.3 Práctica guiada"))

cells.append(
    code(
        """# ── Práctica guiada 5 — funciones como objetos ───────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO
def mi_funcion():
    return "Texto"

var_funcion = mi_funcion

print(mi_funcion())
print(mi_funcion)
print(var_funcion())
print(var_funcion)
print("¿misma función?", mi_funcion is var_funcion)

# 2) Tabla de operaciones
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

tabla = {"+": sumar, "-": restar}
print(tabla["+"](10, 3))
print(tabla["-"](10, 3))"""
    )
)

cells.append(
    md(
        """### 5.4 Errores frecuentes

**1. Llamar al asignar**

INCORRECTO: `var = mi_funcion()` guarda el *resultado*.

CORRECTO: `var = mi_funcion` guarda la *función*.

**2. Olvidar paréntesis al llamar**

`print(var_funcion)` muestra el objeto; `print(var_funcion())` ejecuta.

**3. Mutar un default mutable en la función almacenada**

El clasicismo de `def f(x, lista=[])` sigue aplicando aunque pases `f` como objeto."""
    )
)

cells.append(
    md(
        """### 5.5 Test (10 preguntas)

1. Tras `g = f` (sin llamar), `g is f` es:

**a) `True`**
b) `False`
c) Error
d) Solo si retornan lo mismo

2. `print(mi_funcion)` muestra:

a) El return
**b) La representación del objeto función**
c) Siempre `None`
d) El código fuente completo

3. Una tabla `{"suma": sumar}` permite:

a) Solo strings
**b) Despachar la operación por clave**
c) Ordenar funciones
d) Crear lambdas automáticamente

4. `var = mi_funcion()` guarda:

a) La función
**b) El valor retornado por la llamada**
c) Un decorador
d) Un map

5. ¿Se puede poner una función en una lista?

**a) Sí**
b) No
c) Solo lambdas
d) Solo si es async

6. `tabla["+"](2, 3)` equivale a:

a) `tabla(2, 3)`
**b) `sumar(2, 3)` si esa era la función guardada**
c) `"+" (2, 3)`
d) Error de sintaxis

7. First-class significa:

a) Más prioritaria en el GC
**b) Tratables como cualquier otro objeto**
c) Solo módulos
d) Sin closures

8. ¿`lambda` produce el mismo tipo de objeto que `def`?

**a) Sí (`function`)**
b) No (`lambda` type)
c) Solo en 3.12+
d) Solo sin parámetros

9. Para pasar una función como callback:

a) Hay que usar `eval`
**b) Se pasa la referencia: `procesar(mi_funcion)`**
c) Solo con decoradores
d) Imposible

10. `mi_funcion.__name__` suele ser:

a) El módulo
**b) `"mi_funcion"`**
c) El return
d) `None`"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 5 — tabla_operaciones

Implementa `tabla_operaciones()` que devuelva un dict con claves `"suma"`, `"resta"`, `"mult"`, `"div"` asociadas a funciones, y `aplicar(op, a, b)` que use esa tabla. `div` debe devolver `None` si `b == 0`."""
    )
)

_ex5_todo = '''def tabla_operaciones():
    # TODO: dict nombre -> función
    ...

def aplicar(op, a, b):
    # TODO: usa tabla_operaciones()
    ...

_casos = [
    (("suma", 2, 3), 5),
    (("resta", 10, 4), 6),
    (("mult", 3, 5), 15),
    (("div", 8, 2), 4.0),
    (("div", 8, 0), None),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = aplicar(*_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ aplicar{_entrada!r} = {_r!r}")
    else:
        print(f"✗ aplicar{_entrada!r} = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex5_sol = '''def tabla_operaciones():
    return {
        "suma": lambda a, b: a + b,
        "resta": lambda a, b: a - b,
        "mult": lambda a, b: a * b,
        "div": lambda a, b: None if b == 0 else a / b,
    }

def aplicar(op, a, b):
    return tabla_operaciones()[op](a, b)

_casos = [
    (("suma", 2, 3), 5),
    (("resta", 10, 4), 6),
    (("mult", 3, 5), 15),
    (("div", 8, 2), 4.0),
    (("div", 8, 0), None),
]
_ok = 0
for _entrada, _esperado in _casos:
    try:
        _r = aplicar(*_entrada)
    except Exception as _e:
        print(f"✗ Error al probar {_entrada!r}: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ aplicar{_entrada!r} = {_r!r}")
    else:
        print(f"✗ aplicar{_entrada!r} = {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex5_todo))
cells.append(sol_banner())
cells.append(code(_ex5_sol, solo_profesor=True))

# ─── EPÍGRAFE 6 ────────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 6 — Funciones que devuelven funciones

### 6.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **Factory** | Función que **crea y devuelve** otra función. |
| **Closure** | La interna recuerda variables de la externa. |
| **`match`/`case`** | Forma limpia de elegir qué función devolver (3.10+). |
| **Base del decorador** | Un decorador es, en esencia, una factory de envoltorios. |

```python
def operar(orden):
    def incrementar(n):
        return n + 1
    ...
    match orden:
        case "i":
            return incrementar
```"""
    )
)

cells.append(
    md(
        """### 6.2 Explicación razonada

#### Qué ocurre

Al llamar `operar("i")` se definen (o se referencian) funciones internas y se **retorna** una de ellas. Todavía no se aplica a un número hasta `var_funcion(6)`.

#### Por qué ocurre

Separar *configuración* (`orden`) de *uso* (`n`) permite crear comportamientos a medida (estilo Strategy).

#### Cuándo usar

- Familias de operaciones configurables.
- Preámbulo de decoradores con parámetros.

#### Cuándo NO

- Si siempre es la misma función: no hace falta factory.
- Si el estado mutable compartido entre llamadas se vuelve sutil (cuidado con defaults y listas)."""
    )
)

cells.append(md("### 6.3 Práctica guiada"))

cells.append(
    code(
        """# ── Práctica guiada 6 — devolver funciones ───────────────────────────────────
# Predice cada print ANTES de ejecutar.

# CÓDIGO USUARIO — operar con match
def operar(orden):
    def incrementar(n):
        return n + 1
    def decrementar(n):
        return n - 1

    match orden:
        case "i":
            return incrementar
        case "d":
            return decrementar

var_funcion = operar("i")
print(var_funcion(6))

var_funcion = operar("d")
print(var_funcion(10))

# Factory con parámetro numérico
def crear_potencia(exponente):
    def potencia(base):
        return base ** exponente
    return potencia

al_cubo = crear_potencia(3)
print("2^3 →", al_cubo(2))"""
    )
)

cells.append(
    md(
        """### 6.4 Errores frecuentes

**1. Devolver la llamada en vez de la función**

INCORRECTO: `return incrementar(n)` dentro de `operar`.

CORRECTO: `return incrementar`.

**2. Olvidar el `case` por defecto**

Si `orden` no encaja, `match` sin `case _` deja implícito `None` como retorno → luego `TypeError` al llamar.

**3. Closure tardía en bucle** (`lambda: i` dentro de `for i`) — clásico; usa argumento por defecto `lambda i=i: i`."""
    )
)

cells.append(
    md(
        """### 6.5 Test (10 preguntas)

1. `operar("i")` sin llamarla después devuelve:

a) Un entero
**b) Una función**
c) `"i"`
d) `None`

2. `operar("i")(6)` →

**a) `7`**
b) `6`
c) `5`
d) Error

3. ¿Hace falta `match` para devolver funciones?

a) Sí, obligatorio
**b) No; es una forma clara de elegir**
c) Solo con lambda
d) Solo en clases

4. Una factory es útil cuando:

a) Nunca hay parámetros
**b) Configuras comportamiento y reutilizas el callable**
c) Quieres evitar funciones
d) Solo para I/O

5. Si `operar("x")` no tiene `case _`, tipicamente:

a) Devuelve `incrementar`
**b) Devuelve `None` y fallará al llamar**
c) Lanza siempre
d) Devuelve `"x"`

6. `crear_potencia(3)(2)` →

**a) `8`**
b) `6`
c) `5`
d) `9`

7. Relación con decoradores:

a) Ninguna
**b) El decorador también recibe/devuelve funciones**
c) Son opuestos
d) Solo con clases

8. ¿La interna ve variables de la externa?

**a) Sí (closure), con reglas LEGB**
b) Nunca
c) Solo globals
d) Solo con `nonlocal`

9. `var = operar("d"); var(10)` →

**a) `9`**
b) `11`
c) `10`
d) `d`

10. Mejor que muchos `if` sueltos al elegir operación:

a) Copiar-pegar
**b) Factory / tabla / match que devuelve callables**
c) `goto`
d) Hilos"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 6 — hacer_operacion

`hacer_operacion(simbolo)` debe devolver una función binaria para `+`, `-`, `*`, `/`. Si el símbolo no es válido, devolver `None`. División por 0 → `None`."""
    )
)

_ex6_todo = '''def hacer_operacion(simbolo):
    # TODO: devuelve función binaria o None
    ...

_casos = [
    (("+", 8, 2), 10),
    (("-", 8, 2), 6),
    (("*", 8, 2), 16),
    (("/", 8, 2), 4.0),
    (("/", 8, 0), None),
]
_ok = 0
for (sim, a, b), _esperado in _casos:
    try:
        _fn = hacer_operacion(sim)
        _r = None if _fn is None else _fn(a, b)
    except Exception as _e:
        print(f"✗ Error: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ {sim} {a} {b} → {_r!r}")
    else:
        print(f"✗ {sim} {a} {b} → {_r!r}  (esperado {_esperado!r})")
# símbolo inválido
_fn = hacer_operacion("%")
if _fn is None:
    _ok += 1
    print("✓ símbolo inválido → None")
else:
    print(f"✗ símbolo inválido → {_fn!r}")
print(f"\\nResultado: {_ok}/{len(_casos)+1} casos correctos")'''

_ex6_sol = '''def hacer_operacion(simbolo):
    def sumar(a, b):
        return a + b
    def restar(a, b):
        return a - b
    def mult(a, b):
        return a * b
    def div(a, b):
        return None if b == 0 else a / b

    match simbolo:
        case "+":
            return sumar
        case "-":
            return restar
        case "*":
            return mult
        case "/":
            return div
        case _:
            return None

_casos = [
    (("+", 8, 2), 10),
    (("-", 8, 2), 6),
    (("*", 8, 2), 16),
    (("/", 8, 2), 4.0),
    (("/", 8, 0), None),
]
_ok = 0
for (sim, a, b), _esperado in _casos:
    try:
        _fn = hacer_operacion(sim)
        _r = None if _fn is None else _fn(a, b)
    except Exception as _e:
        print(f"✗ Error: {_e}")
        continue
    if _r == _esperado:
        _ok += 1
        print(f"✓ {sim} {a} {b} → {_r!r}")
    else:
        print(f"✗ {sim} {a} {b} → {_r!r}  (esperado {_esperado!r})")
_fn = hacer_operacion("%")
if _fn is None:
    _ok += 1
    print("✓ símbolo inválido → None")
else:
    print(f"✗ símbolo inválido → {_fn!r}")
print(f"\\nResultado: {_ok}/{len(_casos)+1} casos correctos")'''

cells.append(code(_ex6_todo))
cells.append(sol_banner())
cells.append(code(_ex6_sol, solo_profesor=True))

# ─── EPÍGRAFE 7 ────────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 7 — Primer decorador

### 7.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **Decorador** | Callable que recibe una función y devuelve otra (envoltorio). |
| **Aplicación manual** | `f = decorador(f)`. |
| **Sintaxis `@`** | Azúcar: se aplica al definir. |
| **Envoltorio** | Función interna que llama a la original (antes/después/transformando). |
| **Retorno** | El wrapper debería **devolver** lo que devuelve la original (salvo que el diseño diga lo contrario). |

```python
def decorador(f):
    def antes_y_despues(texto):
        print("Ejecución antes")
        f(texto)
        print("Ejecución después")
    return antes_y_despues
```"""
    )
)

cells.append(
    md(
        """### 7.2 Explicación razonada

#### Qué ocurre

`decorador(imprimir)` crea `antes_y_despues`, que cierra sobre `f`. Al llamar la función decorada, se ejecuta el wrapper, no el `imprimir` «desnudo».

#### Por qué `@`

Reduce ruido y hace visible la política transversal (log, auth…) junto a la definición.

#### Cuándo usar

Comportamiento transversal repetido: timing, logs, validación ligera.

#### Cuándo NO

Si solo se usa una vez y oscurece el flujo: una llamada explícita puede bastar.

#### Detalle

Si el wrapper **no** hace `return f(...)`, el llamador recibe `None` aunque la original devolviera un valor."""
    )
)

cells.append(md("### 7.3 Práctica guiada"))

cells.append(
    code(
        """# ── Práctica guiada 7 — primer decorador ─────────────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — antes_y_despues (aplicación manual)
def decorador(f):
    def antes_y_despues(texto):
        print("Ejecución antes")
        f(texto)
        print("Ejecución después")
    return antes_y_despues

def imprimir(t):
    print(f"En la función imprimir: {t}")

funcion_decorada = decorador(imprimir)
funcion_decorada("HOLA")

print("-" * 40)

# 2) CÓDIGO USUARIO — capitaliza y return
def decorador(f):
    def interna(texto):
        return f(texto.capitalize())
    return interna

@decorador
def imprimir(t):
    return f"En la función imprimir: {t}"

print(imprimir("esto es un texto para probar la función."))"""
    )
)

cells.append(
    md(
        """### 7.4 Errores frecuentes

**1. No devolver el wrapper**

INCORRECTO: el decorador hace side-effects y no `return`.

**2. No propagar el return**

INCORRECTO: `f(...);` sin `return` → el API cambia a `None`.

**3. Firma rígida**

Si la original admite `*args`, el wrapper debería también (o usar `*args, **kwargs`).

**4. Olvidar que `@d` es `f = d(f)`** — el orden mental importa con varios decoradores."""
    )
)

cells.append(
    md(
        """### 7.5 Test (10 preguntas)

1. `@decorador` sobre `def f` equivale a:

a) `decorador()`
**b) `f = decorador(f)`**
c) `f = decorador`
d) `decorador = f`

2. En el ejemplo `antes_y_despues`, ¿quién se llama al invocar la función decorada?

a) Solo `imprimir`
**b) El wrapper, que a su vez llama a `imprimir`**
c) `decorador` otra vez
d) Nadie

3. Si el wrapper no hace `return f(...)`, el llamador obtiene:

a) El valor de `f`
**b) `None` (salvo que el wrapper retorne otra cosa)**
c) Error siempre
d) `True`

4. ¿Un decorador debe llamarse `decorador`?

a) Sí, obligatorio
**b) No; es solo un nombre**
c) Solo en mayúsculas
d) Solo con `@`

5. Aplicación manual correcta:

a) `decorador = imprimir`
**b) `funcion_decorada = decorador(imprimir)`**
c) `imprimir(decorador)`
d) `decorador.imprimir()`

6. El capitalizador del ejemplo transforma:

a) El nombre de la función
**b) El argumento `texto` con `.capitalize()` antes de pasar a `f`**
c) El valor de retorno a mayúsculas
d) Nada

7. ¿Puede el wrapper añadir prints sin cambiar el return?

**a) Sí, si hace `return f(...)`**
b) No
c) Solo con clases
d) Solo async

8. Primera línea típica dentro del decorador:

a) `global f`
**b) Definir una función interna wrapper**
c) `import f`
d) `del f`

9. ¿`@decorador` se ejecuta en tiempo de definición o de llamada?

a) Solo al llamar
**b) El decorador se aplica al definir; el wrapper corre al llamar**
c) Nunca
d) En import de numpy

10. Motivo de examen para fallar tests de decoradores:

a) Usar `def`
**b) Olvidar `return` del resultado de la función original**
c) Usar español en prints
d) Usar `lambda`"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 7 — contar_llamadas

Implementa el decorador `contar_llamadas` que imprima cuántas veces se ha llamado a la función (1, 2, 3, …) y propague el valor de retorno. Usa `nonlocal` o un atributo en el wrapper."""
    )
)

_ex7_todo = '''def contar_llamadas(func):
    # TODO: decorador que cuenta e imprime llamadas
    ...

@contar_llamadas
def saluda(nombre):
    return f"Hola, {nombre}"

_ok = 0
_r1 = saluda("Ana")
_r2 = saluda("Luis")
if _r1 == "Hola, Ana" and _r2 == "Hola, Luis":
    _ok += 1
    print("✓ retornos correctos")
else:
    print(f"✗ retornos {_r1!r}, {_r2!r}")
print(f"\\nResultado: {_ok}/1 casos correctos (revisa también los prints del contador)")'''

_ex7_sol = '''def contar_llamadas(func):
    contador = 0
    def wrapper(*args, **kwargs):
        nonlocal contador
        contador += 1
        print(f"Llamada nº {contador} a {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@contar_llamadas
def saluda(nombre):
    return f"Hola, {nombre}"

_ok = 0
_r1 = saluda("Ana")
_r2 = saluda("Luis")
if _r1 == "Hola, Ana" and _r2 == "Hola, Luis":
    _ok += 1
    print("✓ retornos correctos")
else:
    print(f"✗ retornos {_r1!r}, {_r2!r}")
print(f"\\nResultado: {_ok}/1 casos correctos (revisa también los prints del contador)")'''

cells.append(code(_ex7_todo))
cells.append(sol_banner())
cells.append(code(_ex7_sol, solo_profesor=True))

# ─── EPÍGRAFE 8 ────────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 8 — Decoradores con parámetros

### 8.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **Tres niveles** | Exterior (parámetros) → decorador real → wrapper. |
| **`@decorador(arg)`** | Primero se llama `decorador(arg)` y el resultado decora la función. |
| **Caja / configuración** | El parámetro configura el comportamiento del wrapper. |

```python
def decorador(caja):
    def decorador_interior(f):
        def antes_y_despues(texto):
            ...
        return antes_y_despues
    return decorador_interior
```"""
    )
)

cells.append(
    md(
        """### 8.2 Explicación razonada

#### Qué ocurre

`@decorador("mayusculas")` equivale a:
1. `tmp = decorador("mayusculas")`  → obtiene `decorador_interior`
2. `f = tmp(f)` → obtiene el wrapper

#### Por qué tres niveles

Hace falta un nivel extra para **recibir argumentos del decorador** distintos de la función decorada.

#### Cuándo usar

Reintentos (`n`), rate limit, modos (`mayusculas`/`minusculas`), mensajes de operación.

#### Cuándo NO

Si no hay parámetros, no compliques con tres niveles: usa un decorador simple."""
    )
)

cells.append(md("### 8.3 Práctica guiada"))

cells.append(
    code(
        """# ── Práctica guiada 8 — decoradores con parámetros ───────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — decorador(caja)
def decorador(caja):
    def decorador_interior(f):
        def antes_y_despues(texto):
            print("Ejecución antes")
            if caja == "mayusculas":
                f(texto.upper())
            if caja == "minusculas":
                f(texto.lower())
            print("Ejecución después")
        return antes_y_despues
    return decorador_interior

@decorador("mayusculas")
def imprimir(t):
    print(f"En la función imprimir: {t}")

imprimir("Hola")

print("-" * 40)

# 2) CÓDIGO USUARIO — decorador(operacion) para aritmética
def decorador(operacion):
    def decorador_interior(func):
        def interna(x, y):
            print(f"El resultado de la {operacion} es: {func(x, y)}")
        return interna
    return decorador_interior

@decorador("suma")
def sumar(x, y):
    return x + y

sumar(8, 4)"""
    )
)

cells.append(
    md(
        """### 8.4 Errores frecuentes

**1. Escribir `@decorador "mayusculas"`** — sintaxis inválida; van paréntesis.

**2. Confundir niveles**: devolver el wrapper desde el nivel exterior en vez de `decorador_interior`.

**3. Olvidar `return decorador_interior`** — `@decorador(x)` sería `None` y fallaría.

**4. Usar el mismo nombre `decorador` en celdas distintas** — en notebooks pisa definiciones previas; en examen define nombres claros."""
    )
)

cells.append(
    md(
        """### 8.5 Test (10 preguntas)

1. `@d(1)` primero evalúa:

a) `d(f)`
**b) `d(1)` y el resultado decora `f`**
c) Solo `f`
d) `1(f)`

2. Niveles mínimos típicos con parámetros:

a) 1
b) 2
**c) 3**
d) 4

3. En el ejemplo `caja == "mayusculas"`, ¿quién ve `caja`?

a) Solo el módulo
**b) El wrapper vía closure**
c) Nadie
d) Solo `f`

4. Si `decorador(caja)` no retorna `decorador_interior`:

a) Funciona igual
**b) `@decorador(...)` falla (None no es callable)**
c) Se ignora el parámetro
d) Usa lambda automático

5. ¿`@decorador` sin paréntesis pasa parámetros?

a) Sí, siempre
**b) No: sin `()` es decorador simple**
c) Pasa `self`
d) Pasa `__name__`

6. Equivalencia:

a) `@d(x)` ≡ `f = d(f)(x)`
**b) `@d(x)` ≡ `f = d(x)(f)`**
c) `@d(x)` ≡ `f = d(x, f)`
d) Ninguna

7. Caso de uso típico:

**a) `@reintentar(3)`**
b) Sustituir `def`
c) Crear clases
d) Importar C

8. El parámetro `operacion` en el ejemplo sirve para:

a) Calcular
**b) Configurar el mensaje / comportamiento del wrapper**
c) Tipar x e y
d) Ordenar

9. ¿Se puede combinar con `functools.wraps`?

**a) Sí, en el wrapper interno**
b) No
c) Solo sin parámetros
d) Solo en PyPy

10. Error clásico en examen:

a) Usar español
**b) Devolver el wrapper desde el nivel equivocado**
c) Usar `print`
d) Usar `match`"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 8 — con_reintentos

`con_reintentos(n)` debe reintentar hasta `n` veces si la función lanza excepción. Si agota los intentos, relanza la última excepción. Entre intentos puedes usar `time.sleep(0.01)`."""
    )
)

_ex8_todo = '''import time

def con_reintentos(n):
    # TODO: decorador con parámetro n
    ...

_contador = {"v": 0}

@con_reintentos(3)
def inestable():
    _contador["v"] += 1
    if _contador["v"] < 3:
        raise ValueError("fallo temporal")
    return "ok"

_ok = 0
_contador["v"] = 0
try:
    _r = inestable()
    if _r == "ok" and _contador["v"] == 3:
        _ok += 1
        print("✓ reintentos hasta éxito")
    else:
        print(f"✗ r={_r!r} cont={_contador['v']}")
except Exception as _e:
    print(f"✗ excepción inesperada: {_e}")

_contador["v"] = 0

@con_reintentos(2)
def siempre_falla():
    _contador["v"] += 1
    raise RuntimeError("boom")

try:
    siempre_falla()
    print("✗ debía fallar")
except RuntimeError:
    if _contador["v"] == 2:
        _ok += 1
        print("✓ agota intentos y relanza")
    else:
        print(f"✗ cont={_contador['v']}")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

_ex8_sol = '''import time

def con_reintentos(n):
    def decorador(func):
        def wrapper(*args, **kwargs):
            ultimo = None
            for intento in range(1, n + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ultimo = e
                    if intento == n:
                        raise
                    time.sleep(0.01)
            raise ultimo
        return wrapper
    return decorador

_contador = {"v": 0}

@con_reintentos(3)
def inestable():
    _contador["v"] += 1
    if _contador["v"] < 3:
        raise ValueError("fallo temporal")
    return "ok"

_ok = 0
_contador["v"] = 0
try:
    _r = inestable()
    if _r == "ok" and _contador["v"] == 3:
        _ok += 1
        print("✓ reintentos hasta éxito")
    else:
        print(f"✗ r={_r!r} cont={_contador['v']}")
except Exception as _e:
    print(f"✗ excepción inesperada: {_e}")

_contador["v"] = 0

@con_reintentos(2)
def siempre_falla():
    _contador["v"] += 1
    raise RuntimeError("boom")

try:
    siempre_falla()
    print("✗ debía fallar")
except RuntimeError:
    if _contador["v"] == 2:
        _ok += 1
        print("✓ agota intentos y relanza")
    else:
        print(f"✗ cont={_contador['v']}")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

cells.append(code(_ex8_todo))
cells.append(sol_banner())
cells.append(code(_ex8_sol, solo_profesor=True))

# ─── EPÍGRAFE 9 ────────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 9 — Múltiples decoradores

### 9.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **Apilado** | Varios `@` sobre la misma función. |
| **Orden** | Se aplican de **abajo hacia arriba** (el más cercano a `def` primero). |
| **Equivalencia** | `@d1` / `@d2` / `def f` ≡ `f = d1(d2(f))`. |

```python
@decorador1
@decorador2
def saludar():
    ...
# ≡ saludar = decorador1(decorador2(saludar))
```"""
    )
)

cells.append(
    md(
        """### 9.2 Explicación razonada

#### Qué ocurre

Primero `decorador2` envuelve la original; después `decorador1` envuelve el resultado. Al llamar, entra primero el wrapper de `decorador1`.

#### Por qué el orden importa

Log + timing + auth: el orden cambia qué se mide o si el log ve un fallo de auth.

#### Cuándo usar

Pipelines transversales claros y documentados.

#### Cuándo NO

Apilar cinco decoradores opacos sin tests: pesadilla de depuración."""
    )
)

cells.append(md("### 9.3 Práctica guiada"))

cells.append(
    code(
        """# ── Práctica guiada 9 — múltiples decoradores ────────────────────────────────
# Predice el ORDEN de los prints ANTES de ejecutar.

# CÓDIGO USUARIO
def decorador1(func):
    def interna():
        print("Decorador 1: ANTES")
        func()  # Si no se llama no se ejecuta el decorador2
        print("Decorador 1: DESPUÉS")
    return interna

def decorador2(func):
    def interna():
        print("Decorador 2: ANTES")
        func()
        print("Decorador 2: DESPUÉS")
    return interna

@decorador1
@decorador2
def saludar():
    print("¡Hola! Soy la función original")

saludar()"""
    )
)

cells.append(
    md(
        """### 9.4 Errores frecuentes

**1. Leer el orden de arriba a abajo como orden de aplicación** — es al revés en la aplicación; en la ejecución el exterior entra primero.

**2. Olvidar llamar a `func()`** en un wrapper intermedio: se «traga» el resto de la pila.

**3. Wrappers que no aceptan los mismos `*args`** al combinar con funciones que sí los tienen."""
    )
)

cells.append(
    md(
        """### 9.5 Test (10 preguntas)

1. `@d1` / `@d2` / `def f` ≡

a) `f = d2(d1(f))`
**b) `f = d1(d2(f))`**
c) `f = d1(d2)`
d) `f = d2(d1)`

2. En el ejemplo usuario, el primer print al llamar es:

**a) `Decorador 1: ANTES`**
b) `Decorador 2: ANTES`
c) `¡Hola!`
d) `Decorador 1: DESPUÉS`

3. Si `decorador1` no llama a `func()`:

a) Igual se ejecuta todo
**b) No se ejecuta decorador2 ni la original**
c) Error de sintaxis
d) Se llama dos veces

4. El decorador más cercano a `def` se aplica:

a) El último
**b) El primero (hacia dentro)**
c) Nunca
d) En paralelo

5. Al ejecutar, el wrapper **exterior** es:

a) `decorador2`
**b) `decorador1`**
c) Ambos a la vez
d) La original

6. ¿Cuántos wrappers hay tras dos decoradores simples?

a) 0
b) 1
**c) 2 (anidados)**
d) 3

7. Buena práctica al apilar:

a) Máximo ruido
**b) Documentar el orden y probarlo**
c) Evitar `return`
d) Usar `eval`

8. Equivalente mental útil:

a) Cola FIFO de decoradores en el source de arriba a abajo = aplicación
**b) Cebolla: el de más arriba es la capa exterior en la llamada**
c) Orden aleatorio
d) Solo importa el nombre

9. Si ambos wrappers imprimen ANTES/DESPUÉS, el DESPUÉS de d1 ocurre:

a) Antes que el de d2
**b) Después de cerrar la llamada a d2 (típicamente el último print)**
c) Nunca
d) Solo con errores

10. Para log + cronómetro, si cronometras fuera del log:

a) Da igual
**b) Mides también el tiempo de loguear (según apilado)**
c) Python lo optimiza
d) Prohibido"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 9 — apilar log + cronometro

Implementa `log_llamada` y `cronometro_simple` y aplícalos (en ese orden de `@`) a `trabajo` de forma que se vea el log y se mida tiempo. Ambos deben propagar el return."""
    )
)

_ex9_todo = '''import time

def log_llamada(func):
    # TODO
    ...

def cronometro_simple(func):
    # TODO
    ...

@log_llamada
@cronometro_simple
def trabajo(n):
    s = 0
    for i in range(n):
        s += i
    return s

_ok = 0
_r = trabajo(1000)
if _r == sum(range(1000)):
    _ok += 1
    print("✓ return correcto")
else:
    print(f"✗ return {_r!r}")
print(f"\\nResultado: {_ok}/1 casos correctos (mira prints de log/tiempo)")'''

_ex9_sol = '''import time

def log_llamada(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] entra {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] sale {func.__name__}")
        return resultado
    return wrapper

def cronometro_simple(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        resultado = func(*args, **kwargs)
        print(f"[TIME] {func.__name__}: {time.time() - t0:.6f}s")
        return resultado
    return wrapper

@log_llamada
@cronometro_simple
def trabajo(n):
    s = 0
    for i in range(n):
        s += i
    return s

_ok = 0
_r = trabajo(1000)
if _r == sum(range(1000)):
    _ok += 1
    print("✓ return correcto")
else:
    print(f"✗ return {_r!r}")
print(f"\\nResultado: {_ok}/1 casos correctos (mira prints de log/tiempo)")'''

cells.append(code(_ex9_todo))
cells.append(sol_banner())
cells.append(code(_ex9_sol, solo_profesor=True))

# ─── EPÍGRAFE 10 ───────────────────────────────────────────────────────────

cells.append(
    md(
        """---
## Epígrafe 10 — Decoradores aplicados a operaciones aritméticas

### 10.1 Conceptos clave

| Concepto | Definición |
|---|---|
| **Decorar operaciones** | Wrappers que imprimen resultados o validan operandos. |
| **`decorador_comprobar`** | Guarda: evita división por cero antes de llamar. |
| **Combinación** | Parámetro de nombre de operación + comprobación. |
| **Efecto API** | Si el wrapper solo imprime y no retorna, la función «decorada» ya no sirve en expresiones. |

Patrón de diseño pedagógico: ver cómo una misma idea (envolver) se especializa en validación vs presentación."""
    )
)

cells.append(
    md(
        """### 10.2 Explicación razonada

#### Qué ocurre

Un decorador genérico `interna(x, y): print(func(x,y))` cambia la semántica: la función pasa a usarse por **efecto**, no por valor.

`decorador_comprobar` decide si llama o no según `y == 0`.

#### Cuándo usar

Demos, tracing, validaciones previas.

#### Cuándo NO en producción

Wrappers que tragan el return o solo hacen `print` sin logging estructurado. Prefiere `return` + logger."""
    )
)

cells.append(md("### 10.3 Práctica guiada\n\nIntegra los tres patrones del código de usuario y combínalos en `dividir`."))

cells.append(
    code(
        """# ── Práctica guiada 10 — operaciones aritméticas ─────────────────────────────
# Predice cada print ANTES de ejecutar.

# 1) CÓDIGO USUARIO — decorador que imprime resultado
def decorador(func):
    def interna(x, y):
        print(f"El resultado es: {func(x, y)}")
    return interna

@decorador
def sumar(x, y):
    return x + y

@decorador
def restar(x, y):
    return x - y

@decorador
def multiplicar(x, y):
    return x * y

@decorador
def dividir(x, y):
    if y == 0:
        return "Error: No se puede dividir por cero"
    return x / y

sumar(10, 5)
restar(10, 5)
multiplicar(10, 5)
dividir(10, 2)
dividir(10, 0)

print("-" * 40)

# 2) CÓDIGO USUARIO — decorador_comprobar
def decorador_comprobar(func):
    def interna(x, y):
        if y == 0:
            print("Se intenta dividir entre 0")
        else:
            func(x, y)
    return interna

@decorador_comprobar
def division_segura(x, y):
    print(f"{x} / {y} = {x / y}")

division_segura(20, 4)
division_segura(20, 0)

print("-" * 40)

# 3) Combinar parámetro + comprobar en dividir
def etiquetar(operacion):
    def deco(func):
        def interna(x, y):
            print(f"[{operacion}]", end=" ")
            return func(x, y)
        return interna
    return deco

@etiquetar("división")
@decorador_comprobar
def dividir_combo(x, y):
    print(f"{x} / {y} = {x / y}")

dividir_combo(9, 3)
dividir_combo(9, 0)"""
    )
)

cells.append(
    md(
        """### 10.4 Errores frecuentes

**1. Usar el resultado de una función decorada solo-con-print** en una expresión: obtienes `None`.

**2. Validar *después* de llamar** — la división por cero ya explotó.

**3. Apilar mal**: etiqueta por fuera vs por dentro cambia si ves el mensaje cuando `y==0`.

**4. Duplicar nombres `decorador`/`dividir` entre celdas** y perderte qué versión queda activa."""
    )
)

cells.append(
    md(
        """### 10.5 Test (10 preguntas)

1. En el decorador que solo hace `print(func(x,y))`, `sumar(2,3)` retorna:

a) `5`
**b) `None`**
c) `"5"`
d) Error

2. `decorador_comprobar` con `y==0`:

a) Divide igual
**b) Imprime aviso y no llama a `func`**
c) Retorna 0
d) Lanza siempre

3. ¿Por qué `dividir` del primer bloque no lanza al dividir por 0?

a) Python lo permite
**b) La función original captura el caso y retorna un string de error**
c) El decorador evita la llamada
d) `print` absorbe errores

4. Validar tipos con decorador es:

a) Imposible
**b) Posible comprobando `isinstance` en el wrapper**
c) Solo con mypy
d) Solo en C

5. Combinar `@etiquetar` y `@comprobar`: el orden afecta:

**a) Sí: qué mensajes ves y cuándo**
b) Nunca
c) Solo en Colab
d) Solo con async

6. Mejor API productiva para `sumar` decorada:

a) Solo print
**b) `return` del resultado (+ log opcional)**
c) Devolver el decorador
d) No usar funciones

7. `decorador_comprobar` recibe:

a) x e y
**b) La función a envolver**
c) Un bool
d) Un módulo

8. Si `func` dentro del comprobar sí se llama con `y!=0`:

a) Nunca imprime
**b) Ejecuta el cuerpo original**
c) Salta a otra celda
d) Ordena

9. El string `"Error: No se puede dividir..."` es:

a) Una excepción
**b) Un valor de retorno (diseño pedagógico)**
c) Un decorador
d) Un tipo

10. Idea central del epígrafe:

a) Sustituir operadores
**b) Separar presentación/validación de la operación mediante envoltorios**
c) Eliminar `return`
d) Prohibir `/`"""
    )
)

cells.append(
    md(
        """#### 📝 Ejercicio propuesto 10 — validar_tipos

Escribe `validar_tipos(*tipos)` decorador con parámetros: comprueba `isinstance(arg, tipo)` por posición. Si falla, lanza `TypeError`. Si ok, llama y retorna."""
    )
)

_ex10_todo = '''def validar_tipos(*tipos):
    # TODO
    ...

@validar_tipos(int, int)
def suma_enteros(a, b):
    return a + b

_ok = 0
if suma_enteros(2, 3) == 5:
    _ok += 1
    print("✓ suma_enteros(2,3)")
else:
    print("✗ suma incorrecta")
try:
    suma_enteros(2, 3.5)
    print("✗ debía lanzar TypeError")
except TypeError:
    _ok += 1
    print("✓ TypeError con float")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

_ex10_sol = '''def validar_tipos(*tipos):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for i, (arg, tipo) in enumerate(zip(args, tipos)):
                if not isinstance(arg, tipo):
                    raise TypeError(
                        f"argumento {i} esperaba {tipo.__name__}, recibió {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorador

@validar_tipos(int, int)
def suma_enteros(a, b):
    return a + b

_ok = 0
if suma_enteros(2, 3) == 5:
    _ok += 1
    print("✓ suma_enteros(2,3)")
else:
    print("✗ suma incorrecta")
try:
    suma_enteros(2, 3.5)
    print("✗ debía lanzar TypeError")
except TypeError:
    _ok += 1
    print("✓ TypeError con float")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

cells.append(code(_ex10_todo))
cells.append(sol_banner())
cells.append(code(_ex10_sol, solo_profesor=True))

cells.append(
    md(
        """---
### ✅ Resumen rápido — Parte II

1. Función como objeto → se asigna y se pasa.  
2. Factory → devuelve callables (base del decorador).  
3. `@d` ≡ `f = d(f)`; `@d(x)` ≡ `f = d(x)(f)`.  
4. Varios `@`: aplicación de abajo arriba; ejecución entra por el exterior.  
5. Propaga siempre el `return` salvo diseño explícito en contrario."""
    )
)

cells.append(
    code(
        """# ── Autoevaluación rápida Parte II ───────────────────────────────────────────
def dos_veces(func):
    def wrapper(x):
        return func(func(x))
    return wrapper

@dos_veces
def mas_uno(x):
    return x + 1

print("mas_uno(3) con @dos_veces →", mas_uno(3))  # (3+1)+1 = 5
assert mas_uno(3) == 5
print("✓ autoevaluación Parte II OK")"""
    )
)

cells.append(
    md(
        """---
### Glosario breve

| Término | Significado |
|---|---|
| Predicado | Función que interpreta sí/no (truthiness) |
| Iterador perezoso | Produce valores bajo demanda |
| Wrapper / envoltorio | Función que rodea a otra |
| `wraps` | Copia metadatos de la original al wrapper |
| Memoización | Guardar resultados para no recomputar |
| Rate limit | Tope de llamadas por unidad de tiempo |"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# PARTE III — Casos de uso reales
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
# PARTE III — CASOS DE USO REALES DE DECORADORES

En frameworks (Flask, Django, FastAPI, pytest) los decoradores expresan **políticas transversales**: autenticación, rutas, marcas de test, caché… Aquí verás ocho patrones clásicos con biblioteca estándar.

| # | Patrón | Idea |
|---|---|---|
| 11 | Logging | Registrar cuándo entra/sale una función |
| 12 | Cronómetro | Medir duración |
| 13 | Autenticación | Bloquear si el usuario no está autenticado |
| 14 | Validación | Comprobar tipos/valores |
| 15 | Reintentos | Repetir ante fallos transitorios |
| 16 | Caché | Memoizar por argumentos |
| 17 | Rate limiting | Limitar llamadas por ventana temporal |
| 18 | Debugging | Trazar args y resultado |"""
    )
)

# 11 Logging
cells.append(
    md(
        """---
## 11. Logging con `datetime`

Registra marca temporal y nombre de la función. En producción usarías el módulo `logging`; aquí basta `print` + `datetime` para ver el patrón.

💡 **Nota de examen**: el wrapper debe aceptar `*args, **kwargs` y **devolver** el resultado."""
    )
)

cells.append(
    code(
        """# ── Caso real 11 — Logging ───────────────────────────────────────────────────
from datetime import datetime
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{fecha}] INICIO {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[{fecha}] FIN    {func.__name__} → {resultado!r}")
        return resultado
    return wrapper

@log
def saludar(nombre):
    return f"Hola, {nombre}"

print(saludar("Ana"))"""
    )
)

# 12 Cronómetro
cells.append(
    md(
        """---
## 12. Cronómetro con `time.time()`

Mide el tiempo wall-clock de una llamada. Útil para detectar cuellos de botella (con la salvedad de que medir también tiene coste).

💡 **Nota de examen**: guarda `inicio` antes de llamar y resta al final."""
    )
)

cells.append(
    code(
        """# ── Caso real 12 — Cronómetro ────────────────────────────────────────────────
import time
from functools import wraps

def cronometro(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        duracion = time.time() - inicio
        print(f"⏱ {func.__name__} tardó {duracion:.6f} s")
        return resultado
    return wrapper

@cronometro
def calcular_suma(n):
    return sum(range(n))

print("suma →", calcular_suma(200_000))"""
    )
)

# 13 Auth
cells.append(
    md(
        """---
## 13. Autenticación con dict de usuario

El primer argumento (o uno nombrado) representa al usuario. Si `autenticado` es falso, no se ejecuta la función protegida.

💡 **Nota de examen**: el decorador no «magia seguridad»: solo centraliza la comprobación."""
    )
)

cells.append(
    code(
        """# ── Caso real 13 — Autenticación ─────────────────────────────────────────────
from functools import wraps

def requiere_auth(func):
    @wraps(func)
    def wrapper(usuario, *args, **kwargs):
        if not usuario.get("autenticado"):
            return "Acceso denegado"
        return func(usuario, *args, **kwargs)
    return wrapper

@requiere_auth
def ver_notas(usuario):
    return f"Notas de {usuario['nombre']}: [8, 7, 9]"

admin = {"nombre": "Ana", "autenticado": True}
invitado = {"nombre": "Guest", "autenticado": False}
print(ver_notas(admin))
print(ver_notas(invitado))"""
    )
)

# 14 Validación
cells.append(
    md(
        """---
## 14. Validación con `isinstance`

Comprueba tipos antes de entrar al núcleo de la función. Es validación **en tiempo de ejecución** (distinta del tipado estático).

💡 **Nota de examen**: `isinstance(3.0, int)` es False; `bool` es subclase de `int`."""
    )
)

cells.append(
    code(
        """# ── Caso real 14 — Validación isinstance ─────────────────────────────────────
from functools import wraps

def validar_enteros(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if not isinstance(arg, int) or isinstance(arg, bool):
                raise TypeError(f"arg[{i}] debe ser int, no {type(arg).__name__}")
        return func(*args, **kwargs)
    return wrapper

@validar_enteros
def potencia(base, exp):
    return base ** exp

print(potencia(2, 5))
try:
    potencia(2, 2.5)
except TypeError as e:
    print("capturado:", e)"""
    )
)

# 15 Reintentos
cells.append(
    md(
        """---
## 15. Reintentos (`try`/`except` + `time.sleep`)

Patrón retry ante errores transitorios. Parametriza número de intentos y espera.

💡 **Nota de examen**: estructura de tres niveles porque el decorador lleva parámetros."""
    )
)

cells.append(
    code(
        """# ── Caso real 15 — Reintentos ────────────────────────────────────────────────
import time
from functools import wraps

def reintentar(veces=3, delay=0.05):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"intento {intento}/{veces} falló: {e}")
                    if intento == veces:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorador

# Demostración determinista: falla 3 veces y luego acierta
_fallos_restantes = {"n": 3}

@reintentar(veces=4, delay=0.02)
def tirada_inestable():
    if _fallos_restantes["n"] > 0:
        _fallos_restantes["n"] -= 1
        raise ConnectionError("red inestable")
    return "ok"

print("resultado →", tirada_inestable())

# Caso extremo: se agotan los reintentos (no debe tumbar «Ejecutar todo»)
@reintentar(veces=2, delay=0.01)
def siempre_falla():
    raise ConnectionError("caída total")

try:
    siempre_falla()
except ConnectionError as e:
    print("tras agotar reintentos →", e)"""
    )
)

# 16 Caché
cells.append(
    md(
        """---
## 16. Caché en dict (memoización)

Guarda resultados por clave de argumentos. Ideal para funciones **puras** y costosas. (En stdlib existe `functools.lru_cache`.)

💡 **Nota de examen**: argumentos deben ser *hashables* si usas tupla como clave."""
    )
)

cells.append(
    code(
        """# ── Caso real 16 — Caché ─────────────────────────────────────────────────────
from functools import wraps

def cache(func):
    memoria = {}
    @wraps(func)
    def wrapper(*args):
        if args in memoria:
            print(f"⚡ caché hit {args}")
            return memoria[args]
        print(f"💭 calculando {args}")
        valor = func(*args)
        memoria[args] = valor
        return valor
    return wrapper

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))
print(fib(10))  # segunda vez: hits de caché en la recursión ya calentada / top-level"""
    )
)

# 17 Rate limiting
cells.append(
    md(
        """---
## 17. Rate limiting con timestamps

Limita cuántas llamadas caben en una ventana de tiempo. Guarda marcas en una lista y descarta las antiguas.

💡 **Nota de examen**: usa `functools.wraps` y closure sobre la lista de timestamps."""
    )
)

cells.append(
    code(
        """# ── Caso real 17 — Rate limiting ─────────────────────────────────────────────
import time
from functools import wraps

def rate_limit(max_llamadas, ventana_segundos):
    def decorador(func):
        llamadas = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            ahora = time.time()
            # eliminar marcas fuera de ventana
            while llamadas and llamadas[0] <= ahora - ventana_segundos:
                llamadas.pop(0)
            if len(llamadas) >= max_llamadas:
                raise RuntimeError("Rate limit excedido")
            llamadas.append(ahora)
            return func(*args, **kwargs)
        return wrapper
    return decorador

@rate_limit(3, 1.0)
def ping():
    return "pong"

for i in range(3):
    print(i, ping())
try:
    print(ping())
except RuntimeError as e:
    print("capturado:", e)"""
    )
)

# 18 Debugging
cells.append(
    md(
        """---
## 18. Debugging de args / resultado

Muestra argumentos y valor de retorno. Muy útil en desarrollo; quítalo o degrádalo a logger en producción.

💡 **Nota de examen**: `repr` evita ambigüedades con strings vs números."""
    )
)

cells.append(
    code(
        """# ── Caso real 18 — Debugging ─────────────────────────────────────────────────
from functools import wraps

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        firma = ", ".join(args_repr + kwargs_repr)
        print(f"→ {func.__name__}({firma})")
        resultado = func(*args, **kwargs)
        print(f"← {func.__name__} = {resultado!r}")
        return resultado
    return wrapper

@debug
def area(base, altura):
    return (base * altura) / 2

print("valor:", area(10, 5))"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# PARTE IV — Integradores
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
# PARTE IV — EJERCICIOS INTEGRADORES

Usa el dataset de alumnos siguiente (cópialo en tus soluciones cuando haga falta):

```python
alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
]
```

Cada ejercicio tiene celda TODO + solución del profesorado."""
    )
)

# Integrador 1
cells.append(
    md(
        """#### 📝 Integrador 1 — filter + map + lambda (aprobados y medias)

Escribe `medias_aprobados(alumnos)` que:
1. Calcule la media de cada alumno.
2. Filtre quienes tengan media ≥ 5.
3. Devuelva lista de dicts `{"nombre": ..., "media": ...}` con media redondeada a 2 decimales, usando `filter`/`map`/`lambda` (o equivalentes claros)."""
    )
)

_int1_todo = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
]

def medias_aprobados(alumnos):
    # TODO
    ...

_esperado = [
    {"nombre": "Ana", "media": 8.0},
    {"nombre": "Pedro", "media": 9.0},
]
_ok = 0
try:
    _r = medias_aprobados(alumnos)
except Exception as _e:
    _r = None
    print(f"✗ Error: {_e}")
if _r == _esperado:
    _ok += 1
    print(f"✓ {_r!r}")
else:
    print(f"✗ {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

_int1_sol = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
]

def medias_aprobados(alumnos):
    con_media = map(
        lambda a: {
            "nombre": a["nombre"],
            "media": round(sum(a["notas"]) / len(a["notas"]), 2),
        },
        alumnos,
    )
    return list(filter(lambda a: a["media"] >= 5, con_media))

_esperado = [
    {"nombre": "Ana", "media": 8.0},
    {"nombre": "Pedro", "media": 9.0},
]
_ok = 0
_r = medias_aprobados(alumnos)
if _r == _esperado:
    _ok += 1
    print(f"✓ {_r!r}")
else:
    print(f"✗ {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

cells.append(code(_int1_todo))
cells.append(sol_banner())
cells.append(code(_int1_sol, solo_profesor=True))

# Integrador 2
cells.append(
    md(
        """#### 📝 Integrador 2 — sorted multi-clave

`ordenar_alumnos(alumnos)` debe ordenar por **media descendente** y, a igualdad, por **nombre ascendente**. Devuelve lista de nombres en ese orden.

Ayuda: `key=lambda a: (-media, a["nombre"])`."""
    )
)

_int2_todo = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
    {"nombre": "Bea", "edad": 20, "notas": [8, 7, 9]},
]

def ordenar_alumnos(alumnos):
    # TODO: lista de nombres ordenada
    ...

_esperado = ["Pedro", "Ana", "Bea", "Luis"]
_ok = 0
try:
    _r = ordenar_alumnos(alumnos)
except Exception as _e:
    _r = None
    print(f"✗ Error: {_e}")
if _r == _esperado:
    _ok += 1
    print(f"✓ {_r!r}")
else:
    print(f"✗ {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

_int2_sol = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
    {"nombre": "Bea", "edad": 20, "notas": [8, 7, 9]},
]

def ordenar_alumnos(alumnos):
    def media(a):
        return sum(a["notas"]) / len(a["notas"])
    ordenados = sorted(alumnos, key=lambda a: (-media(a), a["nombre"]))
    return [a["nombre"] for a in ordenados]

_esperado = ["Pedro", "Ana", "Bea", "Luis"]
_ok = 0
_r = ordenar_alumnos(alumnos)
if _r == _esperado:
    _ok += 1
    print(f"✓ {_r!r}")
else:
    print(f"✗ {_r!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

cells.append(code(_int2_todo))
cells.append(sol_banner())
cells.append(code(_int2_sol, solo_profesor=True))

# Integrador 3
cells.append(
    md(
        """#### 📝 Integrador 3 — decorador `validar_rango(minimo, maximo)`

Decorador con parámetros que comprueba que el **primer argumento posicional** esté en `[minimo, maximo]`. Si no, lanza `ValueError`. Propaga el return si es válido."""
    )
)

_int3_todo = '''def validar_rango(minimo, maximo):
    # TODO
    ...

@validar_rango(0, 10)
def clasificar(nota):
    return "ok" if nota >= 5 else "ko"

_ok = 0
if clasificar(7) == "ok":
    _ok += 1
    print("✓ 7")
try:
    clasificar(11)
    print("✗ debía lanzar")
except ValueError:
    _ok += 1
    print("✓ ValueError fuera de rango")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

_int3_sol = '''def validar_rango(minimo, maximo):
    def decorador(func):
        def wrapper(*args, **kwargs):
            if not args:
                raise TypeError("se esperaba al menos un argumento")
            valor = args[0]
            if not (minimo <= valor <= maximo):
                raise ValueError(f"{valor} fuera de [{minimo}, {maximo}]")
            return func(*args, **kwargs)
        return wrapper
    return decorador

@validar_rango(0, 10)
def clasificar(nota):
    return "ok" if nota >= 5 else "ko"

_ok = 0
if clasificar(7) == "ok":
    _ok += 1
    print("✓ 7")
try:
    clasificar(11)
    print("✗ debía lanzar")
except ValueError:
    _ok += 1
    print("✓ ValueError fuera de rango")
print(f"\\nResultado: {_ok}/2 casos correctos")'''

cells.append(code(_int3_todo))
cells.append(sol_banner())
cells.append(code(_int3_sol, solo_profesor=True))

# Integrador 4
cells.append(
    md(
        """#### 📝 Integrador 4 — pipeline log + cache sobre estadísticas

Implementa `log_simple` y `cache_simple` y decora `estadisticas(alumnos)` que devuelve `{"media_curso": float, "n": int}` (media de todas las notas del curso).

Orden: `@log_simple` encima de `@cache_simple`. La segunda llamada con los mismos datos debe mostrar hit de caché (y log)."""
    )
)

_int4_todo = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
]

def log_simple(func):
    # TODO
    ...

def cache_simple(func):
    # TODO: clave = id(alumnos) o tupla de tuplas
    ...

@log_simple
@cache_simple
def estadisticas(alumnos):
    # TODO
    ...

_ok = 0
_r1 = estadisticas(alumnos)
_r2 = estadisticas(alumnos)
_esperada = round((8+7+9+4+5+3+9+10+8) / 9, 2)
if _r1 == _r2 == {"media_curso": _esperada, "n": 9}:
    _ok += 1
    print(f"✓ {_r1!r}")
else:
    print(f"✗ {_r1!r} / {_r2!r}")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

_int4_sol = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "notas": [8, 7, 9]},
    {"nombre": "Luis", "edad": 21, "notas": [4, 5, 3]},
    {"nombre": "Pedro", "edad": 19, "notas": [9, 10, 8]},
]

def log_simple(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def cache_simple(func):
    memoria = {}
    def wrapper(alumnos):
        clave = tuple((a["nombre"], tuple(a["notas"])) for a in alumnos)
        if clave in memoria:
            print("⚡ caché hit estadísticas")
            return memoria[clave]
        valor = func(alumnos)
        memoria[clave] = valor
        return valor
    return wrapper

@log_simple
@cache_simple
def estadisticas(alumnos):
    todas = [n for a in alumnos for n in a["notas"]]
    return {"media_curso": round(sum(todas) / len(todas), 2), "n": len(todas)}

_ok = 0
_r1 = estadisticas(alumnos)
_r2 = estadisticas(alumnos)
_esperada = round((8+7+9+4+5+3+9+10+8) / 9, 2)
if _r1 == _r2 == {"media_curso": _esperada, "n": 9}:
    _ok += 1
    print(f"✓ {_r1!r}")
else:
    print(f"✗ {_r1!r} / {_r2!r}")
print(f"\\nResultado: {_ok}/1 casos correctos")'''

cells.append(code(_int4_todo))
cells.append(sol_banner())
cells.append(code(_int4_sol, solo_profesor=True))

# Tabla + checklist + cierre
cells.append(
    md(
        """---
## Tabla comparativa final

| Herramienta | Propósito | Retorna | Ejemplo típico |
|---|---|---|---|
| `lambda` | Callable anónimo de una expresión | callable (`function`) | `key=lambda x: x["precio"]` |
| `filter` | Seleccionar por predicado | objeto `filter` (iterador) | `list(filter(es_par, nums))` |
| `map` | Transformar elemento a elemento | objeto `map` (iterador) | `list(map(str.upper, xs))` |
| `sorted` | Ordenar materializando | `list` | `sorted(items, key=...)` |
| decorador | Envolver una función con política extra | función modificada (wrapper) | `@log` / `@cache` |"""
    )
)

cells.append(
    md(
        """---
## Checklist final

- [ ] Entiendo que `lambda` es una expresión callable, no un bloque.
- [ ] Sé que `filter`/`map` son perezosos y se agotan.
- [ ] Domino `sorted(..., key=..., reverse=...)`.
- [ ] Puedo escribir un decorador simple y uno con parámetros (3 niveles).
- [ ] Sé el orden de múltiples `@decorador`.
- [ ] Reconozco patrones: log, timing, auth, validación, retry, cache, rate limit, debug.
- [ ] He pasado los ejercicios con autocorrección (`✓` / `✗`).

### Cierre

Este material enlaza la visión de **funciones como valores** del notebook de control de flujo con herramientas del día a día en Python. El siguiente paso natural es `functools` (`wraps`, `lru_cache`, `partial`) y, en web, decoradores de rutas y dependencias."""
    )
)

# Extra celdas para superar ~150 si hiciera falta: mapa rápido
cells.append(
    md(
        """---
## Mapa rápido de decisión

| Quieres… | Usa… |
|---|---|
| Callable de una línea en un argumento | `lambda` o `def` corta |
| Quedarte con un subconjunto | `filter` o comprensión |
| Transformar todos | `map` o comprensión |
| Presentar ordenado | `sorted` |
| Política transversal reutilizable | decorador |
| Decorador configurable | tres niveles / fábrica |"""
    )
)

cells.append(
    md(
        """---
## Criterios de evaluación (orientativos)

| Nivel | Evidencia |
|---|---|
| Aprobado | Ejercicios 1–4 y un decorador simple correctos |
| Notable | Decoradores con parámetros + apilado razonado |
| Sobresaliente | Integradores + explicación del orden y de la pereza de `map`/`filter` |

📚 Estudia prediciendo salidas; ✅ comprueba con las celdas; ❌ lee errores frecuentes antes de la solución del profesorado."""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# Escribir notebook
# ═══════════════════════════════════════════════════════════════════════════

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    },
    "cells": cells,
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)
    f.write("\n")

solo = sum(1 for c in cells if c.get("metadata", {}).get("solo_profesor"))
print(f"Escrito: {OUT}")
print(f"Celdas: {len(cells)}")
print(f"solo_profesor: {solo}")
