"""
app.py — Portal CE Python
Sistema de login por roles (Profesor / Alumno) con visor de notebook interactivo.
"""
from flask import Flask, render_template, request, session, redirect, url_for
from pathlib import Path
import notebook_renderer

app = Flask(__name__)
app.secret_key = 'ce-python-portal-2026-xK9mP3qRvT'

BASE = Path(__file__).parent

USERS = {
    'profesor': {
        'password':   'profesor123',
        'role':       'profesor',
        'label':      'Profesorado',
        'icon':       '👩‍🏫',
        'notebook':   BASE / 'CE_Python_PROFESOR.ipynb',
        'nb_name':    'CE_Python_PROFESOR.ipynb',
        'colab_url':  'https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/CE_Python_PROFESOR.ipynb',
        'github_url': 'https://github.com/gracobjo/CE_python_mio/blob/master/CE_Python_PROFESOR.ipynb',
    },
    'alumno': {
        'password':   'alumno123',
        'role':       'alumno',
        'label':      'Alumnado',
        'icon':       '👨‍🎓',
        'notebook':   BASE / 'CE_Python_ALUMNO.ipynb',
        'nb_name':    'CE_Python_ALUMNO.ipynb',
        'colab_url':  'https://colab.research.google.com/github/gracobjo/CE_python_mio/blob/master/CE_Python_ALUMNO.ipynb',
        'github_url': 'https://github.com/gracobjo/CE_python_mio/blob/master/CE_Python_ALUMNO.ipynb',
    },
}

# Cache para no re-parsear el notebook en cada request
_cache: dict = {}


def get_rendered(username: str) -> dict:
    if username not in _cache:
        _cache[username] = notebook_renderer.render_notebook(USERS[username]['notebook'])
    return _cache[username]


@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('notebook'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').lower().strip()
        password = request.form.get('password', '')
        if username in USERS and USERS[username]['password'] == password:
            session.clear()
            session['user'] = username
            return redirect(url_for('notebook'))
        error = 'Usuario o contraseña incorrectos. Inténtalo de nuevo.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/notebook')
def notebook():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    user = USERS[username]
    rendered = get_rendered(username)
    return render_template('notebook.html', rendered=rendered, user=user, username=username)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
