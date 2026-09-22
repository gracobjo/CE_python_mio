"""Genera la versión ALUMNO a partir del notebook PROFESOR."""
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_PROFESOR.ipynb"
DST = ROOT / "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_ALUMNO.ipynb"

COLAB_ALUMNO = (
    "https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/"
    "CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES_ALUMNO.ipynb"
)

HEADER_ALUMNO = f"""# Python — Lambda, filter, map, sorted y decoradores

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB_ALUMNO})

A continuación se desarrollan con **profundidad teórica y práctica** los epígrafes de **programación funcional ligera** (`lambda`, `filter`, `map`, `sorted`) y **decoradores**, como **continuación** del notebook de control de flujo y funciones. Se asume que ya conoces `def`, parámetros, ámbito LEGB, closures básicas y `match`/`case`.

Cada epígrafe incluye: **conceptos clave**, **explicación razonada**, **práctica guiada ejecutable**, **errores frecuentes**, **batería de test de nivel examen** y **ejercicio propuesto con comprobación automática**.

Este cuaderno es la **versión del alumnado**: incluye enunciados, prácticas y comprobación automática, **sin** las soluciones del profesorado.

### Qué vas a conseguir con este material

1. Entender `lambda` como expresión callable, no como «atajo mágico».
2. Usar `filter` y `map` sabiendo que son **iteradores perezosos**.
3. Dominar `sorted` con `key` y ordenaciones multi-criterio.
4. Construir decoradores (simples, con parámetros y apilados).
5. Reconocer patrones reales: logging, cronómetro, auth, caché, reintentos…
6. Comprobar automáticamente tus soluciones.
7. Preparar preguntas de examen de nivel difícil.

### Requisitos

- Python **3.10 o superior** (`match` / `case` en algún ejemplo).
- Solo biblioteca estándar: **no** hace falta pandas, numpy ni frameworks web.
"""

COMO_USAR = """---
## Cómo usar este notebook

1. Ejecuta primero la celda de **comprobación del intérprete**.
2. Estudia cada epígrafe en orden: primero teoría, después práctica.
3. **Predice** el resultado de los ejemplos antes de ejecutarlos.
4. Completa los ejercicios donde pone `# TODO` o `...`.
5. No modifiques las celdas de comprobación: ellas te dicen cuántos casos has acertado.
6. Si un ejercicio no pasa, lee de nuevo la **explicación razonada** y los **errores frecuentes** antes de reintentar.

> **Consejo de estudio**: las preguntas tipo test no preguntan «qué palabra clave se usa». Preguntan qué objeto devuelve `filter`, si un `lambda` puede llevar sentencias, en qué orden se aplican varios `@decorador`, o qué captura un closure.
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

    # Adaptar cabecera y «cómo usar»
    if kept:
        set_source(kept[0], HEADER_ALUMNO)
    if len(kept) > 1 and "Cómo usar este notebook" in src_text(kept[1]):
        set_source(kept[1], COMO_USAR)

    # Ajustar checklist si menciona solución del profesorado
    for cell in kept:
        text = src_text(cell)
        if "Checklist final" in text and "solución del profesorado" in text:
            text = text.replace(
                "- [ ] He pasado los ejercicios con autocorrección (`✓` / `✗`).",
                "- [ ] He pasado los ejercicios con autocorrección (`✓` / `✗`) sin mirar soluciones externas.",
            )
            text = text.replace(
                "❌ lee errores frecuentes antes de la solución del profesorado.",
                "❌ lee errores frecuentes y reintenta el ejercicio.",
            )
            set_source(cell, text)

    nb["cells"] = kept
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")

    # Verificación
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
