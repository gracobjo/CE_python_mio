# -*- coding: utf-8 -*-
"""Genera CE_Python_LAMBDA_MAP_FSTRING_DATOS_PROFESOR.ipynb (nbformat 4).

Notebook introductorio: lambda, f-string, map() y transformación de datos
(listas de diccionarios). Puente hacia el cuaderno avanzado de
filter / sorted / decoradores.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "CE_Python_LAMBDA_MAP_FSTRING_DATOS_PROFESOR.ipynb"

COLAB_PROF = (
    "https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/"
    "CE_Python_LAMBDA_MAP_FSTRING_DATOS_PROFESOR.ipynb"
)
AVANZADO = "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES"


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
        f"""# Funciones Lambda en Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB_PROF})

## Funciones lambda, f-strings, map() y transformación de datos

Una función `lambda` permite crear **funciones pequeñas de una sola expresión**. En este notebook la usarás junto con conceptos que ya conoces: `def`, listas, diccionarios, `if`/`else`, bucles `for` y f-strings.

Este cuaderno es la **versión del profesorado**: incluye soluciones completas. Esas celdas van marcadas con:

**Solución (solo para el profesorado — no se incluye en la versión del alumnado):**

> **Nivel**: cero / intermedio inicial.  
> **No** se tratan aquí `filter`, `sorted`, decoradores ni comprensiones de listas complejas. Eso está en el cuaderno avanzado `{AVANZADO}`."""
    )
)

cells.append(
    md(
        """---
## Cómo usar este notebook

1. Lee cada celda Markdown **antes** de ejecutar el código siguiente.
2. Ejecuta las celdas de código en orden (muchas reutilizan variables de celdas anteriores).
3. **Predice** el resultado antes de pulsar Ejecutar.
4. Completa los ejercicios donde pone `# TODO`.
5. No modifiques las celdas de comprobación automática.
6. Si un ejercicio no pasa, vuelve a la explicación anterior **antes** de mirar la solución.

> **Consejo**: el objetivo no es memorizar la sintaxis, sino **entender qué está haciendo Python** en cada paso."""
    )
)

cells.append(
    md(
        """---
## Objetivos

Al terminar este notebook sabrás:

1. Qué es una función `lambda`.
2. Diferenciar `def` y `lambda`.
3. Guardar una `lambda` en una variable.
4. Utilizar `lambda` con `if` / `else`.
5. Utilizar `lambda` dentro de un f-string.
6. Comprender una función que **devuelve** una `lambda`.
7. Utilizar `lambda` con `map()`.
8. Comprender por qué se usa `list(map(...))`.
9. Utilizar `lambda` con listas.
10. Utilizar `lambda` con **listas de diccionarios**.
11. Combinar `lambda` + `map()` + f-string.
12. Aplicar estos conceptos a datos similares a un dataset."""
    )
)

cells.append(
    md(
        """---
## Índice

1. Recordatorio: funciones con `def`
2. Qué es una `lambda`
3. `lambda` con varios parámetros
4. `lambda` con `if` / `else`
5. `lambda` + f-string
6. `lambda` y diccionarios
7. Función que devuelve una `lambda`
8. Introducción a `map()`
9. Por qué `list()`
10. `map()` + `lambda`
11. `map` + `lambda` + f-string
12. Lista de diccionarios (dataset sencillo)
13. `map` + `lambda` sobre diccionarios
14. Combinación final + ejercicios
15. Resumen y siguiente paso"""
    )
)

cells.append(
    md(
        """---
## Configuración — Comprobación rápida

Solo biblioteca estándar. Comprueba que el intérprete responde."""
    )
)

cells.append(
    code(
        """# ── Comprobación del intérprete ──────────────────────────────────────────────
import sys

print(f"Python {sys.version.split()[0]}")
print("Listo para trabajar con lambda, map y f-strings.")"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 1. RECORDATORIO def
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 1. Recordatorio: funciones normales (`def`)

Antes de `lambda`, recordamos una función tradicional:

```python
def doble(numero):
    return numero * 2
```

| Pieza | Significado |
|---|---|
| `def` | Define una función |
| `doble` | Nombre de la función |
| `numero` | Parámetro (dato de entrada) |
| `return` | Valor que devuelve la función |
| `doble(5)` | Llamada: sustituye `numero` por `5` |

Resultado esperado de `doble(5)` → `10`."""
    )
)

cells.append(
    code(
        """# Función tradicional con def
def doble(numero):
    return numero * 2

print(doble(5))   # esperado: 10"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. QUÉ ES LAMBDA
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 2. ¿Qué es una `lambda`?

Una `lambda` es una **función pequeña** que normalmente se escribe en **una sola expresión**.

**Sintaxis:**

```python
lambda parametros: resultado
```

**Equivalencia:**

```python
def doble(x):
    return x * 2
```

frente a:

```python
lambda x: x * 2
```

La `lambda` **no** necesita `def` ni `return`: el valor de la expresión *es* el retorno.

Suele guardarse en una variable para poder llamarla varias veces:

```python
doble = lambda x: x * 2
```"""
    )
)

cells.append(
    code(
        """# Misma idea que def doble, pero con lambda
doble = lambda x: x * 2

print(doble(5))    # esperado: 10
print(doble(10))   # esperado: 20"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 3. VARIOS PARÁMETROS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 3. `lambda` con distintos parámetros

Una `lambda` puede recibir **más de un** parámetro, separados por comas:

```python
lambda a, b: a + b
```

Funciona igual que en un `def`: al llamar, pasas los argumentos en el mismo orden."""
    )
)

cells.append(
    code(
        """sumar = lambda a, b: a + b

print(sumar(3, 5))     # esperado: 8
print(sumar(10, 20))   # esperado: 30"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 4. IF / ELSE
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 4. `lambda` con `if` / `else`

Dentro de una `lambda` solo cabe **una expresión**. El `if`/`else` en una línea (operador ternario) sí es una expresión:

```python
lambda x: valor_si_verdadero if condicion else valor_si_falso
```

Ejemplo:

```python
lambda nota: "Aprobado" if nota >= 5 else "Suspenso"
```

> No uses bloques `if` con indentación dentro de una `lambda`. Si necesitas varias líneas, usa `def`."""
    )
)

cells.append(
    code(
        """estado = lambda nota: "Aprobado" if nota >= 5 else "Suspenso"

print(estado(8))   # esperado: Aprobado
print(estado(4))   # esperado: Suspenso"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 5. F-STRING
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 5. `lambda` + f-string

Dentro de las llaves `{}` de un f-string puedes poner **expresiones** y **llamadas a funciones** (incluida una `lambda` guardada en una variable).

Ejemplo:

```python
f"Nota: {nota} → {estado(nota)}"
```

Aquí `estado(nota)` se evalúa primero; el resultado se inserta en el texto."""
    )
)

cells.append(
    code(
        """# Reutilizamos la lambda 'estado' de la celda anterior
nota = 8

print(f"Nota: {nota} → {estado(nota)}")
# esperado: Nota: 8 → Aprobado"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 6. DICCIONARIOS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 6. `lambda` y diccionarios

Un diccionario representa un **registro** (una fila de datos):

```python
alumno = {
    "nombre": "Ana",
    "edad": 20,
    "nota": 8
}
```

Acceso a campos:

```python
alumno["nombre"]   # "Ana"
alumno["edad"]     # 20
alumno["nota"]     # 8
```

Esos valores se pueden pasar a una `lambda` o usar dentro de un f-string."""
    )
)

cells.append(
    code(
        """alumno = {
    "nombre": "Ana",
    "edad": 20,
    "nota": 8
}

estado = lambda nota: "Aprobado" if nota >= 5 else "Suspenso"

print(
    f"{alumno['nombre']} | "
    f"{alumno['edad']} años | "
    f"Nota: {alumno['nota']} | "
    f"{estado(alumno['nota'])}"
)
# esperado: Ana | 20 años | Nota: 8 | Aprobado"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 7. FUNCIÓN QUE DEVUELVE LAMBDA
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 7. Función que devuelve una `lambda`

A veces una función `def` **no** devuelve un texto o un número: devuelve **otra función**.

```python
def modificar_texto(texto):
    return lambda a: texto + a
```

Paso a paso:

1. `modificar_texto` es una función normal (`def`).
2. Su `return` no es un string final: es una **lambda**.
3. Esa lambda **recuerda** el valor de `texto` que recibió al crearse.
4. Más tarde la llamas con el argumento `a`.

Esquema:

```text
modificar_texto("Hola ")
        ↓
lambda a: "Hola " + a
        ↓
poner_despues
        ↓
poner_despues("Ana")
        ↓
"Hola Ana"
```

> No hace falta llamar a esto «closure» todavía: basta con entender que la lambda **guarda** el `texto` del momento en que se creó."""
    )
)

cells.append(
    code(
        """def modificar_texto(texto):
    # Devuelve una función (lambda), no un string
    return lambda a: texto + a

poner_despues = modificar_texto("Hola ")

print(poner_despues("Ana"))    # esperado: Hola Ana
print(poner_despues("Luis"))   # esperado: Hola Luis"""
    )
)

cells.append(
    md(
        """### La misma operación en una sola línea

Puedes encadenar las dos llamadas:

```python
modificar_texto("Hola ")("Ana")
```

Es equivalente a:

```python
poner_despues = modificar_texto("Hola ")
resultado = poner_despues("Ana")
```

Primero se crea la lambda; después se llama con `"Ana"`."""
    )
)

cells.append(
    code(
        """def modificar_texto(texto):
    return lambda a: texto + a

# En dos pasos
resultado1 = modificar_texto("Hola ")
resultado2 = resultado1("Ana")

# En una sola expresión
resultado3 = modificar_texto("Hola ")("Ana")

print(resultado2)   # esperado: Hola Ana
print(resultado3)   # esperado: Hola Ana"""
    )
)

cells.append(
    md(
        """### También dentro de un f-string

La función devuelta se puede llamar dentro de `{}`."""
    )
)

cells.append(
    code(
        """def modificar_texto(texto):
    return lambda a: texto + a

poner_despues = modificar_texto("Hola ")

print(f"Resultado: {poner_despues('Ana')}")
# esperado: Resultado: Hola Ana"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 8. MAP
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 8. Introducción a `map()`

`map()` aplica una función a **cada** elemento de una lista (u otro iterable).

```text
lista
  ↓
map()
  ↓
aplica una función a cada elemento
  ↓
resultado
```

Ejemplo con una función `def`:

```python
elementos = [1, 2, 3, 4, 5]
map(doble, elementos)   # aplica doble a 1, 2, 3, 4 y 5
```

Para ver los valores como lista usamos `list(...)` (lo explicamos en el siguiente apartado)."""
    )
)

cells.append(
    code(
        """elementos = [1, 2, 3, 4, 5]

def doble(x):
    return x * 2

resultado = list(map(doble, elementos))

print(resultado)
# esperado: [2, 4, 6, 8, 10]"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 9. POR QUÉ LIST
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 9. ¿Por qué `list()`?

`map()` **no** devuelve una lista de inmediato: devuelve un objeto `map` (un iterador «perezoso»).

```python
resultado = map(doble, elementos)
print(resultado)        # algo como <map object at 0x...>
print(list(resultado))  # [2, 4, 6, 8, 10]
```

Usamos `list(...)` cuando queremos **materializar** el resultado y poder imprimirlo o reutilizarlo como lista.

> Si consumes el iterador una vez (por ejemplo con `list`), se agota: no puedes recorrerlo otra vez sin volver a crear el `map`."""
    )
)

cells.append(
    code(
        """elementos = [1, 2, 3, 4, 5]

def doble(x):
    return x * 2

resultado = map(doble, elementos)

print(resultado)           # objeto map (no la lista)
print(list(resultado))     # esperado: [2, 4, 6, 8, 10]"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 10. MAP + LAMBDA
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 10. `map()` + `lambda`

Si la operación es pequeña, no hace falta crear un `def` con nombre.

Comparación:

```python
def doble(x):
    return x * 2

list(map(doble, elementos))
```

con:

```python
list(map(lambda x: x * 2, elementos))
```

Ambas producen el mismo resultado. La `lambda` se define **en el punto de uso**."""
    )
)

cells.append(
    code(
        """elementos = [1, 2, 3, 4, 5]

def doble(x):
    return x * 2

resultado1 = list(map(doble, elementos))
resultado2 = list(map(lambda x: x * 2, elementos))

print(resultado1)   # esperado: [2, 4, 6, 8, 10]
print(resultado2)   # esperado: [2, 4, 6, 8, 10]"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 11. MAP + LAMBDA + F-STRING
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 11. `map` + `lambda` + f-string

La `lambda` también puede **generar texto**. Por ejemplo:

```python
lambda x: f"El doble de {x} es {x * 2}"
```

Combinado con `map`, transformas cada número en una frase."""
    )
)

cells.append(
    code(
        """elementos = [1, 2, 3, 4, 5]

resultado = list(
    map(
        lambda x: f"El doble de {x} es {x * 2}",
        elementos
    )
)

print(resultado)
# esperado: ['El doble de 1 es 2', 'El doble de 2 es 4', ...]"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 12. LISTA DE DICCIONARIOS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 12. Lista de diccionarios (dataset sencillo)

Una estructura muy habitual:

```python
alumnos = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Marta", "nota": 7}
]
```

| Idea | En el código |
|---|---|
| Dataset / tabla | la lista `alumnos` |
| Fila / registro | cada diccionario |
| Columna / campo | claves `"nombre"`, `"nota"` |

Es la misma idea que filas y columnas, sin pandas todavía."""
    )
)

cells.append(
    code(
        """alumnos = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Marta", "nota": 7}
]

for alumno in alumnos:
    print(alumno)"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# 13. MAP SOBRE DICCIONARIOS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## 13. `map` + `lambda` sobre diccionarios

La `lambda` recibe **cada diccionario completo**:

```python
lambda alumno: ...
```

Dentro puedes usar:

```python
alumno["nombre"]
alumno["nota"]
```"""
    )
)

cells.append(
    code(
        """resultado = list(
    map(
        lambda alumno: f"{alumno['nombre']} → {alumno['nota']}",
        alumnos
    )
)

print(resultado)
# esperado: ['Ana → 8', 'Luis → 4', 'Marta → 7']"""
    )
)

cells.append(
    md(
        """---
## 14. Combinación: `map` + `lambda` + `if`/`else` + f-string

Objetivo:

```text
Ana → 8 → Aprobado
Luis → 4 → Suspenso
Marta → 7 → Aprobado
```

La lambda debe:

1. Recibir un alumno (diccionario).
2. Leer nombre y nota.
3. Decidir Aprobado / Suspenso.
4. Construir el texto con un f-string."""
    )
)

cells.append(
    code(
        """resultado = list(
    map(
        lambda alumno:
            f"{alumno['nombre']} → "
            f"{alumno['nota']} → "
            f"{'Aprobado' if alumno['nota'] >= 5 else 'Suspenso'}",
        alumnos
    )
)

for texto in resultado:
    print(texto)"""
    )
)

cells.append(
    md(
        """### Explicación paso a paso

```python
lambda alumno:
```

El parámetro es un diccionario.

```python
alumno["nombre"]   # nombre
alumno["nota"]     # nota
"Aprobado" if alumno["nota"] >= 5 else "Suspenso"   # clasificación
```

El f-string une todo en un solo texto:

```text
alumno
   ↓
alumno["nombre"] / alumno["nota"]
   ↓
if / else
   ↓
f-string
   ↓
texto
```"""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# EJERCICIOS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## Ejercicios

Completa cada celda donde pone `# TODO`. La comprobación automática te dirá cuántos casos has acertado."""
    )
)

# —— Ejercicio 1 ——
cells.append(
    md(
        """### 📝 Ejercicio 1 — Duplicar notas con `map` y `lambda`

Dada:

```python
notas = [2, 4, 5, 7, 8, 10]
```

Usa `map()` y `lambda` para duplicar cada nota. Asigna el resultado a `resultado`.

Esperado: `[4, 8, 10, 14, 16, 20]`."""
    )
)

_ex1_todo = '''notas = [2, 4, 5, 7, 8, 10]

resultado = None  # TODO: list(map(lambda x: ..., notas))

_casos = [
    (resultado, [4, 8, 10, 14, 16, 20]),
]
_ok = 0
for _obtenido, _esperado in _casos:
    if _obtenido == _esperado:
        _ok += 1
        print(f"✓ resultado = {_obtenido!r}")
    else:
        print(f"✗ resultado = {_obtenido!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

_ex1_sol = '''notas = [2, 4, 5, 7, 8, 10]

resultado = list(map(lambda x: x * 2, notas))

_casos = [
    (resultado, [4, 8, 10, 14, 16, 20]),
]
_ok = 0
for _obtenido, _esperado in _casos:
    if _obtenido == _esperado:
        _ok += 1
        print(f"✓ resultado = {_obtenido!r}")
    else:
        print(f"✗ resultado = {_obtenido!r}  (esperado {_esperado!r})")
print(f"\\nResultado: {_ok}/{len(_casos)} casos correctos")'''

cells.append(code(_ex1_todo))
cells.append(sol_banner())
cells.append(code(_ex1_sol, solo_profesor=True))

# —— Ejercicio 2 ——
cells.append(
    md(
        """### 📝 Ejercicio 2 — Aprobado / Suspenso por alumno

Con:

```python
alumnos = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Marta", "nota": 7}
]
```

Usa `map()` y `lambda` para obtener una lista de textos:

```text
Ana → Aprobado
Luis → Suspenso
Marta → Aprobado
```

Guarda esa lista en `resultado`."""
    )
)

_ex2_todo = '''alumnos = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Marta", "nota": 7}
]

resultado = None  # TODO: list(map(lambda alumno: f"...", alumnos))

_esperado = [
    "Ana → Aprobado",
    "Luis → Suspenso",
    "Marta → Aprobado",
]
if resultado == _esperado:
    print("✓ resultado correcto")
    for texto in resultado:
        print(texto)
    print("\\nResultado: 1/1 casos correctos")
else:
    print(f"✗ resultado = {resultado!r}")
    print(f"  esperado = {_esperado!r}")
    print("\\nResultado: 0/1 casos correctos")'''

_ex2_sol = '''alumnos = [
    {"nombre": "Ana", "nota": 8},
    {"nombre": "Luis", "nota": 4},
    {"nombre": "Marta", "nota": 7}
]

resultado = list(
    map(
        lambda alumno:
            f"{alumno['nombre']} → "
            f"{'Aprobado' if alumno['nota'] >= 5 else 'Suspenso'}",
        alumnos
    )
)

_esperado = [
    "Ana → Aprobado",
    "Luis → Suspenso",
    "Marta → Aprobado",
]
if resultado == _esperado:
    print("✓ resultado correcto")
    for texto in resultado:
        print(texto)
    print("\\nResultado: 1/1 casos correctos")
else:
    print(f"✗ resultado = {resultado!r}")
    print(f"  esperado = {_esperado!r}")
    print("\\nResultado: 0/1 casos correctos")'''

cells.append(code(_ex2_todo))
cells.append(sol_banner())
cells.append(code(_ex2_sol, solo_profesor=True))

# —— Ejercicio 3 ——
cells.append(
    md(
        """### 📝 Ejercicio 3 — Informe completo con edad

Con:

```python
alumnos = [
    {"nombre": "Ana", "edad": 20, "nota": 8},
    {"nombre": "Luis", "edad": 17, "nota": 4},
    {"nombre": "Marta", "edad": 22, "nota": 9}
]
```

Usa `map()` + `lambda` + f-string. El resultado debe ser:

```text
Ana | 20 años | Nota: 8 | Aprobado
Luis | 17 años | Nota: 4 | Suspenso
Marta | 22 años | Nota: 9 | Aprobado
```

Guarda la lista en `resultado`."""
    )
)

_ex3_todo = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "nota": 8},
    {"nombre": "Luis", "edad": 17, "nota": 4},
    {"nombre": "Marta", "edad": 22, "nota": 9}
]

resultado = None  # TODO: list(map(lambda alumno: f"...", alumnos))

_esperado = [
    "Ana | 20 años | Nota: 8 | Aprobado",
    "Luis | 17 años | Nota: 4 | Suspenso",
    "Marta | 22 años | Nota: 9 | Aprobado",
]
if resultado == _esperado:
    print("✓ resultado correcto")
    for texto in resultado:
        print(texto)
    print("\\nResultado: 1/1 casos correctos")
else:
    print(f"✗ resultado = {resultado!r}")
    print(f"  esperado = {_esperado!r}")
    print("\\nResultado: 0/1 casos correctos")'''

_ex3_sol = '''alumnos = [
    {"nombre": "Ana", "edad": 20, "nota": 8},
    {"nombre": "Luis", "edad": 17, "nota": 4},
    {"nombre": "Marta", "edad": 22, "nota": 9}
]

resultado = list(
    map(
        lambda alumno:
            f"{alumno['nombre']} | "
            f"{alumno['edad']} años | "
            f"Nota: {alumno['nota']} | "
            f"{'Aprobado' if alumno['nota'] >= 5 else 'Suspenso'}",
        alumnos
    )
)

_esperado = [
    "Ana | 20 años | Nota: 8 | Aprobado",
    "Luis | 17 años | Nota: 4 | Suspenso",
    "Marta | 22 años | Nota: 9 | Aprobado",
]
if resultado == _esperado:
    print("✓ resultado correcto")
    for texto in resultado:
        print(texto)
    print("\\nResultado: 1/1 casos correctos")
else:
    print(f"✗ resultado = {resultado!r}")
    print(f"  esperado = {_esperado!r}")
    print("\\nResultado: 0/1 casos correctos")'''

cells.append(code(_ex3_todo))
cells.append(sol_banner())
cells.append(code(_ex3_sol, solo_profesor=True))

# ═══════════════════════════════════════════════════════════════════════════
# RESUMEN Y CIERRE
# ═══════════════════════════════════════════════════════════════════════════

cells.append(
    md(
        """---
## Resumen

| Concepto | Función |
|---|---|
| `lambda` | Crear funciones pequeñas de una expresión |
| `def` | Crear funciones normales (bloques, varias sentencias) |
| `map()` | Aplicar una función a varios elementos |
| `list()` | Convertir el resultado de `map()` en lista |
| f-string | Construir textos dinámicos |
| `if` / `else` (ternario) | Decidir dentro de una expresión |
| diccionario | Representar un registro |
| lista de diccionarios | Representar datos similares a un dataset |"""
    )
)

cells.append(
    md(
        """---
## Idea final

Cadena conceptual que has practicado:

```text
DATOS
  ↓
LISTA
  ↓
MAP
  ↓
LAMBDA
  ↓
TRANSFORMACIÓN
  ↓
F-STRING
  ↓
RESULTADO
```

Relación con datasets reales:

```text
Dataset
   ↓
Filas / registros
   ↓
Transformación
   ↓
Nueva información
```

Este patrón te prepara para CSV, `pandas` y otras herramientas: la idea (recorrer registros y transformar campos) es la misma."""
    )
)

cells.append(
    md(
        f"""---
## Siguiente paso

Cuando domines este notebook, continúa con **`{AVANZADO}`** (versiones alumno/profesor), donde se desarrollan:

1. `filter()`
2. `sorted()` con `lambda` / `key`
3. Pipelines `map` + `filter`
4. `lambda` con criterios más elaborados
5. Comprensiones de listas (como alternativa legible)
6. Decoradores y casos de uso reales
7. Baterías de test de nivel examen

No hace falta estudiarlos todos de golpe: avanza epígrafe a epígrafe."""
    )
)

cells.append(
    md(
        """---
## Checklist final

- [ ] Sé explicar con mis palabras qué es una `lambda`.
- [ ] Distingo cuándo basta `lambda` y cuándo conviene `def`.
- [ ] Entiendo por qué `map` necesita `list(...)` para ver la lista.
- [ ] Puedo transformar una lista de diccionarios con `map` + f-string.
- [ ] He pasado los tres ejercicios con autocorrección (`✓` / `✗`).

Si algo falla: vuelve a la celda de explicación anterior **antes** de mirar la solución del profesorado."""
    )
)

# ═══════════════════════════════════════════════════════════════════════════
# ESCRITURA
# ═══════════════════════════════════════════════════════════════════════════

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "cells": cells,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")

solo = sum(1 for c in cells if c.get("metadata", {}).get("solo_profesor"))
print(f"Escrito: {OUT}")
print(f"Celdas: {len(cells)}")
print(f"solo_profesor: {solo}")
