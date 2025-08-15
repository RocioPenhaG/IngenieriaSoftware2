from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'is2_proyecto'

# -----------------------
# Conexión a la base
# -----------------------
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Decoradores de seguridad
# -----------------------
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

# -----------------------
# Login
# -----------------------
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

# -----------------------
# Admin dashboard
# -----------------------
@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html')

# -----------------------
# Empleados
# -----------------------
@app.route('/admin/empleados')
@login_required
@role_required('admin')
def listar_empleados():
    conn = get_db_connection()
    empleados = conn.execute('SELECT * FROM empleados').fetchall()
    conn.close()
    return render_template('admin_empleados.html', empleados=empleados)

@app.route('/admin/empleados/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def crear_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        fecha_nacimiento = request.form['fecha_nacimiento']
        estado_civil = request.form['estado_civil']
        cargo = request.form['cargo']
        salario_base = request.form['salario_base']
        fecha_ingreso = request.form['fecha_ingreso']

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO empleados (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_empleados'))

    return render_template('admin_empleados_form.html', empleado=None)

@app.route('/admin/empleados/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_empleado(id):
    conn = get_db_connection()
    empleado = conn.execute('SELECT * FROM empleados WHERE id = ?', (id,)).fetchone()

    if not empleado:
        conn.close()
        return "Empleado no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        fecha_nacimiento = request.form['fecha_nacimiento']
        estado_civil = request.form['estado_civil']
        cargo = request.form['cargo']
        salario_base = request.form['salario_base']
        fecha_ingreso = request.form['fecha_ingreso']

        conn.execute("""
            UPDATE empleados
            SET nombre = ?, cedula = ?, fecha_nacimiento = ?, estado_civil = ?, cargo = ?, salario_base = ?, fecha_ingreso = ?
            WHERE id = ?
        """, (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso, id))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_empleados'))

    conn.close()
    return render_template('admin_empleados_form.html', empleado=empleado)

# -----------------------
# Otros roles
# -----------------------
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

# -----------------------
# Logout
# -----------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------
# Main
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
