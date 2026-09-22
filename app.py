"""
app.py — Portal CE Python
Sistema de login por roles (Profesor / Alumno) con visor y ejecutor interactivo de notebooks.
Soporta CE_Python_CONTROL_FLUJO_FUNCIONES_PROFESOR.ipynb y cualquier archivo .ipynb presente en el proyecto.
"""
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pathlib import Path
import json
import re
import sys
import subprocess
import notebook_renderer

app = Flask(__name__)
app.secret_key = 'ce-python-portal-2026-xK9mP3qRvT'

BASE = Path(__file__).parent.resolve()
EXCLUDE_DIRS = {'.venv', '.git', '.ipynb_checkpoints', '__pycache__'}

USERS = {
    'profesor': {
        'password':   'profesor123',
        'role':       'profesor',
        'label':      'Profesorado',
        'icon':       '👩‍🏫',
        'default_nb': 'CE_Python_PROFESOR.ipynb',
    },
    'alumno': {
        'password':   'alumno123',
        'role':       'alumno',
        'label':      'Alumnado',
        'icon':       '👨‍🎓',
        'default_nb': 'CE_Python_ALUMNO.ipynb',
    },
}

KNOWN_NOTEBOOKS = {
    'CE_Python.ipynb': {
        'title': 'Curso completo (Base)',
        'badge': 'General',
        'badge_class': 'bdg-gold',
    },
    'CE_Python_ALUMNO.ipynb': {
        'title': 'Curso completo — Alumnado',
        'badge': 'Alumno',
        'badge_class': 'bdg-blue',
    },
    'CE_Python_PROFESOR.ipynb': {
        'title': 'Curso completo — Profesorado',
        'badge': 'Profesor',
        'badge_class': 'bdg-purple',
    },
    'CE_Python_CONTROL_FLUJO_FUNCIONES_PROFESOR.ipynb': {
        'title': 'Control de flujo y funciones (Profesor)',
        'badge': 'Profesor',
        'badge_class': 'bdg-purple',
    },
    'CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES.ipynb': {
        'title': 'Lambda, Filter, Map, Sorted y Decoradores',
        'badge': 'Avanzado',
        'badge_class': 'bdg-gold',
    },
}

# Cache para cuadernos parseados: {str(abs_path): {'mtime': float, 'data': dict}}
_cache: dict[str, dict] = {}


def extract_notebook_title(path: Path) -> str:
    """Extrae el primer encabezado Markdown del notebook si existe."""
    try:
        with open(path, encoding='utf-8') as f:
            nb = json.load(f)
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source_raw = cell.get('source', '')
                src_text = ''.join(source_raw) if isinstance(source_raw, list) else source_raw
                for line in src_text.splitlines():
                    line = line.strip()
                    if line.startswith('#'):
                        clean = re.sub(r'^#+\s*', '', line)
                        clean = re.sub(r'[\*_`]', '', clean)
                        return clean[:60]
    except Exception:
        pass
    return path.stem.replace('_', ' ').title()


def get_available_notebooks() -> list[dict]:
    """Descubre dinámicamente todos los archivos .ipynb del repositorio."""
    notebooks = []
    for p in BASE.rglob('*.ipynb'):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        rel = p.relative_to(BASE).as_posix()
        name = p.name

        if name in KNOWN_NOTEBOOKS:
            meta = KNOWN_NOTEBOOKS[name]
            title = meta['title']
            badge = meta['badge']
            badge_class = meta['badge_class']
        else:
            uname = name.upper()
            if 'PROFESOR' in uname:
                badge = 'Profesor'
                badge_class = 'bdg-purple'
            elif 'ALUMNO' in uname:
                badge = 'Alumno'
                badge_class = 'bdg-blue'
            else:
                badge = 'Cuaderno'
                badge_class = 'bdg-green'
            title = extract_notebook_title(p)

        colab_url = f'https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/{rel}'
        github_url = f'https://github.com/gracobjo/CE_python_mio/blob/master/{rel}'

        notebooks.append({
            'filename': name,
            'rel_path': rel,
            'abs_path': p,
            'title': title,
            'badge': badge,
            'badge_class': badge_class,
            'colab_url': colab_url,
            'github_url': github_url,
        })

    # Orden preferencial: conocidos primero, luego alfabético
    def sort_key(item):
        known_order = [
            'CE_Python_ALUMNO.ipynb',
            'CE_Python_PROFESOR.ipynb',
            'CE_Python_CONTROL_FLUJO_FUNCIONES_PROFESOR.ipynb',
            'CE_Python_LAMBDA_FILTER_MAP_SORTED_DECORADORES.ipynb',
            'CE_Python.ipynb',
        ]
        if item['filename'] in known_order:
            return (0, known_order.index(item['filename']))
        return (1, item['filename'].lower())

    return sorted(notebooks, key=sort_key)


def get_rendered(nb_path: Path) -> dict:
    """Renderiza el notebook con caché invalidada automáticamente si el archivo cambia en disco."""
    nb_path = nb_path.resolve()
    mtime = nb_path.stat().st_mtime
    key = str(nb_path)
    if key not in _cache or _cache[key].get('mtime') != mtime:
        _cache[key] = {
            'mtime': mtime,
            'data': notebook_renderer.render_notebook(nb_path)
        }
    return _cache[key]['data']


@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('notebook'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST':
        username = request.form.get('username', '').lower().strip()
        password = request.form.get('password', '')
        if username in USERS and USERS[username]['password'] == password:
            session.clear()
            session['user'] = username
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('notebook'))
        error = 'Usuario o contraseña incorrectos. Inténtalo de nuevo.'
    return render_template('login.html', error=error, next_url=next_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/notebook')
@app.route('/notebook/<path:nb_name>')
def notebook(nb_name: str | None = None):
    if 'user' not in session:
        target = request.full_path if request.query_string else request.path
        return redirect(url_for('login', next=target))

    username = session['user']
    user_info = USERS.get(username, USERS['alumno'])
    available = get_available_notebooks()

    if not available:
        return "No se encontraron cuadernos .ipynb en el proyecto.", 404

    # Determinar qué notebook mostrar:
    # 1. Parámetro query ?nb=...
    # 2. Parámetro de ruta /notebook/<nb_name>
    # 3. Argumento pasado por CLI al arrancar la app (si existe)
    # 4. Cuaderno por defecto según rol de usuario
    requested = request.args.get('nb') or nb_name or app.config.get('CLI_DEFAULT_NB') or user_info['default_nb']

    selected = None
    for nb in available:
        if (nb['rel_path'] == requested or
            nb['filename'] == requested or
            nb['rel_path'].lower() == requested.lower() or
            nb['filename'].lower() == requested.lower()):
            selected = nb
            break

    if not selected:
        # Fallback al primer cuaderno disponible
        selected = available[0]

    rendered = get_rendered(selected['abs_path'])

    # Configurar datos del usuario activo con el cuaderno actual
    active_user = dict(user_info)
    active_user['nb_name'] = selected['filename']
    active_user['colab_url'] = selected['colab_url']
    active_user['github_url'] = selected['github_url']

    return render_template(
        'notebook.html',
        rendered=rendered,
        user=active_user,
        username=username,
        notebooks=available,
        current_nb=selected
    )


@app.route('/api/run_cell', methods=['POST'])
def run_cell():
    """Ejecuta una celda de código Python en un subproceso aislado y devuelve la salida."""
    if 'user' not in session:
        return jsonify({'error': 'No autorizado. Inicia sesión.'}), 401

    payload = request.get_json(silent=True) or {}
    code = payload.get('code', '')
    if not code.strip():
        return jsonify({'stdout': '', 'stderr': '', 'exit_code': 0})

    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            cwd=str(BASE),
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'stdout': '',
            'stderr': '⏱ Tiempo de ejecución excedido (límite: 10 segundos).',
            'exit_code': -1
        })
    except Exception as exc:
        return jsonify({
            'stdout': '',
            'stderr': f'Error al ejecutar celda: {exc}',
            'exit_code': -1
        })


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Portal CE Python')
    parser.add_argument('notebook', nargs='?', help='Nombre o ruta del cuaderno .ipynb a abrir por defecto')
    parser.add_argument('--port', type=int, default=8080, help='Puerto del servidor (default: 8080)')
    parser.add_argument('--no-debug', action='store_true', help='Desactivar modo debug')

    args, unknown = parser.parse_known_args()

    if args.notebook:
        app.config['CLI_DEFAULT_NB'] = args.notebook
        print(f"📓 Cuaderno seleccionado por CLI: {args.notebook}")

    detected = get_available_notebooks()
    print(f"\n🚀 Portal CE Python disponible en: http://localhost:{args.port}")
    print(f"📁 Cuadernos detectados ({len(detected)}):")
    for nb in detected:
        print(f"   • [{nb['badge']}] {nb['filename']} — {nb['title']}")
    print()

    app.run(debug=not args.no_debug, port=args.port)

