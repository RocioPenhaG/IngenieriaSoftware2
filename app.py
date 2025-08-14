from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'is2_proyecto'

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def role_required(role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'rol' not in session or session['rol'] != role:
                return "Acceso no autorizado", 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE correo = ? AND password = ?', (correo, password)).fetchone()
        conn.close()

        if user:
            session['usuario'] = user['correo']
            session['rol'] = user['rol']

            if user['rol'] == 'admin':
                return redirect(url_for('admin'))
            elif user['rol'] == 'gerente':
                return redirect(url_for('gerente'))
            elif user['rol'] == 'asistente':
                return redirect(url_for('asistente'))
            elif user['rol'] == 'empleado':
                return redirect(url_for('empleado'))
            else:
                return "Rol no definido", 403
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html')

@app.route('/gerente')
@login_required
@role_required('gerente')
def gerente():
    return render_template('gerente.html')

@app.route('/asistente')
@login_required
@role_required('asistente')
def asistente():
    return render_template('asistente.html')

@app.route('/empleado')
@login_required
@role_required('empleado')
def empleado():
    return render_template('empleado.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
