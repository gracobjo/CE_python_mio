"""
notebook_renderer.py
Convierte notebooks Jupyter (.ipynb) a HTML estructurado para el portal CE Python.
"""
import json
import re
import html as html_lib
from pathlib import Path

import markdown as md_lib
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


# ─── Configuración URLs externas ──────────────────────────────────────────────

COLAB_URLS = {
    'alumno':   'https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/CE_Python_ALUMNO.ipynb',
    'profesor': 'https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/CE_Python_PROFESOR.ipynb',
}
GITHUB_URLS = {
    'alumno':   'https://github.com/gracobjo/CE_python_mio/blob/master/CE_Python_ALUMNO.ipynb',
    'profesor': 'https://github.com/gracobjo/CE_python_mio/blob/master/CE_Python_PROFESOR.ipynb',
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

_CHAR_MAP = str.maketrans(
    'áàâäéèêëíìîïóòôöúùûüñç',
    'aaaaeeeeiiiioooouuuunc'
)

def slugify(text: str) -> str:
    """Genera un anchor slug a partir de un texto."""
    text = text.lower().translate(_CHAR_MAP)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'\s+', '-', text.strip()) or 'section'


def src(raw) -> str:
    """Convierte la fuente de una celda (str o list) a cadena."""
    return ''.join(raw) if isinstance(raw, list) else (raw or '')


_ANSI = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(text: str) -> str:
    return _ANSI.sub('', text)


def pygments_css() -> str:
    return HtmlFormatter(style='monokai', cssclass='hl').get_style_defs('.hl')


# ─── Renderizado de outputs ───────────────────────────────────────────────────

def render_output(out: dict) -> str:
    otype = out.get('output_type', '')

    if otype == 'stream':
        text = strip_ansi(src(out.get('text', '')))
        cls = 'out-stderr' if out.get('name') == 'stderr' else 'out-stdout'
        return f'<pre class="nb-out {cls}">{html_lib.escape(text)}</pre>'

    if otype in ('display_data', 'execute_result'):
        data = out.get('data', {})
        if 'image/png' in data:
            return (f'<div class="nb-out out-img">'
                    f'<img src="data:image/png;base64,{data["image/png"]}" alt="gráfico"/>'
                    f'</div>')
        if 'image/svg+xml' in data:
            return f'<div class="nb-out out-img">{src(data["image/svg+xml"])}</div>'
        if 'text/html' in data:
            return f'<div class="nb-out out-html">{src(data["text/html"])}</div>'
        if 'text/plain' in data:
            return f'<pre class="nb-out out-plain">{html_lib.escape(src(data["text/plain"]))}</pre>'

    if otype == 'error':
        ename = html_lib.escape(out.get('ename', 'Error'))
        evalue = html_lib.escape(out.get('evalue', ''))
        tb = html_lib.escape('\n'.join(strip_ansi(l) for l in out.get('traceback', [])))
        return f'<pre class="nb-out out-error"><b>{ename}: {evalue}</b>\n{tb}</pre>'

    return ''


# ─── Clasificación de celdas ─────────────────────────────────────────────────

def classify(source: str, cell_type: str, meta: dict) -> str:
    if meta.get('solo_profesor'):
        return 'prof-only'
    if cell_type == 'markdown':
        sl = source.lower()
        first = source.lstrip().split('\n', 1)[0].strip()
        if first.startswith('#'):
            return 'heading'
        if first == '---':
            return 'divider'
        if '📝 ejercicio propuesto' in sl:
            return 'ejercicio'
        if re.search(r'###?\s+[\d.]+\s+test', sl):
            return 'test'
        return 'theory'
    if cell_type == 'code':
        sl = source.lower()
        if '# todo:' in sl:
            return 'ex-code'
        if '# ──' in source or '# ─' in source:
            return 'practice'
        return 'code'
    return 'code'


# ─── Renderizado principal ────────────────────────────────────────────────────

_MD_EXT = ['tables', 'fenced_code', 'sane_lists', 'attr_list']

BADGES = {
    'ejercicio': '<span class="badge bdg-gold">📝 Ejercicio propuesto</span>',
    'test':      '<span class="badge bdg-blue">📋 Test de autoevaluación</span>',
    'practice':  '<span class="badge bdg-green">⚡ Práctica guiada</span>',
    'ex-code':   '<span class="badge bdg-gold">📝 Completa el código</span>',
    'prof-only': '<span class="badge bdg-purple">🔑 Solución — solo Profesor</span>',
}


def render_notebook(nb_path: Path) -> dict:
    """
    Parsea y renderiza un notebook Jupyter a HTML.

    Devuelve:
        cells_html   : lista de cadenas HTML (una por celda)
        toc          : lista de {level, title, anchor}
        pygments_css : CSS de Pygments para incluir en el template
    """
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)

    cells_html: list[str] = []
    toc: list[dict] = []
    anchor_cnt: dict[str, int] = {}

    # Formateador Pygments compartido
    formatter = HtmlFormatter(style='monokai', cssclass='hl')

    def make_anchor(raw_title: str) -> str:
        a = slugify(re.sub(r'[\*_`]', '', raw_title))
        if a in anchor_cnt:
            anchor_cnt[a] += 1
            a = f'{a}-{anchor_cnt[a]}'
        else:
            anchor_cnt[a] = 0
        return a

    def heading_sub(m: re.Match) -> str:
        hashes, title = m.group(1), m.group(2).strip()
        level = len(hashes)
        anchor = make_anchor(title)
        clean = re.sub(r'[\*_`]', '', title)
        if level <= 2:
            toc.append({'level': level, 'title': clean, 'anchor': anchor})
        return f'{hashes} <span id="{anchor}" class="toc-anchor"></span>{title}'

    for cell in nb.get('cells', []):
        cell_type = cell.get('cell_type', '')
        source    = src(cell.get('source', ''))
        meta      = cell.get('metadata', {})
        cid       = cell.get('id', '')
        outputs   = cell.get('outputs', [])
        exc       = cell.get('execution_count')

        if not source.strip():
            continue

        kind = classify(source, cell_type, meta)

        # ── Celda Markdown ────────────────────────────────────────────────────
        if cell_type == 'markdown':
            if kind == 'divider':
                cells_html.append('<hr class="nb-divider"/>')
                continue

            processed = re.sub(
                r'^(#{1,6})\s+(.+)$', heading_sub, source, flags=re.MULTILINE
            )
            body = md_lib.markdown(processed, extensions=_MD_EXT)
            badge = BADGES.get(kind, '')

            cells_html.append(
                f'<article class="nb-cell cell-{kind}" data-id="{cid}">'
                f'{badge}'
                f'<div class="md-body">{body}</div>'
                f'</article>'
            )

        # ── Celda de código ───────────────────────────────────────────────────
        elif cell_type == 'code':
            hl = highlight(source, PythonLexer(), formatter)
            outs_html = ''.join(render_output(o) for o in outputs)
            badge = BADGES.get(kind, '')
            exec_lbl = (
                f'<span class="exec-lbl">In&nbsp;[{exc}]</span>'
                if exc else ''
            )
            run_btn = (
                '<button class="btn-run" onclick="runCell(this)" title="Ejecutar celda">'
                '<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">'
                '<polygon points="5 3 19 12 5 21 5 3"/></svg>'
                ' Ejecutar'
                '</button>'
            )
            copy_btn = (
                '<button class="btn-copy" onclick="copyCode(this)" title="Copiar código">'
                '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                'stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"/>'
                '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
                ' Copiar'
                '</button>'
            )
            cells_html.append(
                f'<article class="nb-cell cell-{kind}" data-id="{cid}">'
                f'<div class="code-hdr">{badge}{exec_lbl}<div class="code-actions">{run_btn}{copy_btn}</div></div>'
                f'<div class="code-body">{hl}</div>'
                f'{f"<div class=\"outputs\">{outs_html}</div>" if outs_html else ""}'
                f'</article>'
            )

    return {
        'cells_html':   cells_html,
        'toc':          toc,
        'pygments_css': pygments_css(),
    }
