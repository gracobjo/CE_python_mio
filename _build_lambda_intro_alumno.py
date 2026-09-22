# -*- coding: utf-8 -*-
"""Genera la versión ALUMNO a partir del notebook introductorio PROFESOR."""
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "CE_Python_LAMBDA_MAP_FSTRING_DATOS_PROFESOR.ipynb"
DST = ROOT / "CE_Python_LAMBDA_MAP_FSTRING_DATOS_ALUMNO.ipynb"

COLAB_ALUMNO = (
    "https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/"
    "CE_Python_LAMBDA_MAP_FSTRING_DATOS_ALUMNO.ipynb"
)
AVANZADO = "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES"

HEADER_ALUMNO = f"""# Funciones Lambda en Python

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB_ALUMNO})

## Funciones lambda, f-strings, map() y transformación de datos

Una función `lambda` permite crear **funciones pequeñas de una sola expresión**. En este notebook la usarás junto con conceptos que ya conoces: `def`, listas, diccionarios, `if`/`else`, bucles `for` y f-strings.

Este cuaderno es la **versión del alumnado**: incluye enunciados, prácticas y comprobación automática, **sin** las soluciones del profesorado.

> **Nivel**: cero / intermedio inicial.  
> **No** se tratan aquí `filter`, `sorted`, decoradores ni comprensiones de listas complejas. Eso está en el cuaderno avanzado `{AVANZADO}`.
"""

COMO_USAR = """---
## Cómo usar este notebook

1. Lee cada celda Markdown **antes** de ejecutar el código siguiente.
2. Ejecuta las celdas de código en orden (muchas reutilizan variables de celdas anteriores).
3. **Predice** el resultado antes de pulsar Ejecutar.
4. Completa los ejercicios donde pone `# TODO`.
5. No modifiques las celdas de comprobación automática.
6. Si un ejercicio no pasa, vuelve a la explicación anterior y reintenta.

> **Consejo**: el objetivo no es memorizar la sintaxis, sino **entender qué está haciendo Python** en cada paso.
"""


def src_text(cell) -> str:
    s = cell.get("source", "")
    return "".join(s) if isinstance(s, list) else (s or "")


def set_source(cell, text: str) -> None:
    if not text.endswith("\n"):
        text += "\n"
    cell["source"] = [text]


def main() -> None:
    with open(SRC, encoding="utf-8") as f:
        nb = json.load(f)

    kept = []
    removed = 0
    for cell in nb["cells"]:
        if cell.get("metadata", {}).get("solo_profesor"):
            removed += 1
            continue
        kept.append(deepcopy(cell))

    if kept:
        set_source(kept[0], HEADER_ALUMNO)
    if len(kept) > 1 and "Cómo usar este notebook" in src_text(kept[1]):
        set_source(kept[1], COMO_USAR)

    for cell in kept:
        text = src_text(cell)
        if "Checklist final" in text and "solución del profesorado" in text:
            text = text.replace(
                "Si algo falla: vuelve a la celda de explicación anterior **antes** de mirar la solución del profesorado.",
                "Si algo falla: vuelve a la celda de explicación anterior y reintenta el ejercicio.",
            )
            set_source(cell, text)

    nb["cells"] = kept
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")

    solo = sum(1 for c in nb["cells"] if c.get("metadata", {}).get("solo_profesor"))
    has_sol_label = any(
        "Solución (solo para el profesorado" in src_text(c) for c in nb["cells"]
    )
    print(f"Escrito: {DST}")
    print(f"Celdas: {len(nb['cells'])} (eliminadas {removed})")
    print(f"solo_profesor restantes: {solo}")
    print(f"etiquetas solución profesorado: {has_sol_label}")


if __name__ == "__main__":
    main()
