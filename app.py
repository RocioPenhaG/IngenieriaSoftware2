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
# Gestión de Usuarios
# -----------------------
@app.route('/admin/usuarios')
@login_required
@role_required('admin')
def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def crear_usuario():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO usuarios (correo, password, rol) VALUES (?, ?, ?)',
            (correo, password, rol)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    return render_template('admin_usuarios_form.html', usuario=None)

@app.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if not usuario:
        conn.close()
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        rol = request.form['rol']

        conn.execute("""
            UPDATE usuarios
            SET correo=?, password=?, rol=?
            WHERE id=?
        """, (correo, password, rol, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    conn.close()
    return render_template('admin_usuarios_form.html', usuario=usuario)

@app.route('/admin/usuarios/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def eliminar_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if not usuario:
        conn.close()
        return "Usuario no encontrado", 404

    if request.method == 'POST':
        conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    conn.close()
    return render_template('admin_usuarios_eliminar.html', usuario=usuario)


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
        hijos = request.form['hijos']
        ips = request.form['ips']

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO empleados 
            (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso, hijos, ips)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso, hijos, ips))
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
        hijos = request.form['hijos']
        ips = request.form['ips']

        conn.execute("""
            UPDATE empleados
            SET nombre=?, cedula=?, fecha_nacimiento=?, estado_civil=?, cargo=?, salario_base=?, fecha_ingreso=?, hijos=?, ips=?
            WHERE id=?
        """, (nombre, cedula, fecha_nacimiento, estado_civil, cargo, salario_base, fecha_ingreso, hijos, ips, id))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_empleados'))

    conn.close()
    return render_template('admin_empleados_form.html', empleado=empleado)

""" @app.route('/admin/empleados/eliminar/<int:id>')
@login_required
@role_required('admin')
def eliminar_empleado(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM empleados WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_empleados')) """

@app.route('/admin/empleados/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def eliminar_empleado(id):
    conn = get_db_connection()
    empleado = conn.execute("SELECT * FROM empleados WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        conn.execute("DELETE FROM empleados WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash('Empleado eliminado correctamente', 'success')
        return redirect(url_for('listar_empleados'))

    conn.close()
    # GET: mostrar página de confirmación
    return render_template('empleados_eliminar.html', empleado=empleado)


# -----------------------
# Conceptos Salariales
# -----------------------
@app.route('/admin/conceptos')
@login_required
@role_required('admin')
def listar_conceptos():
    conn = get_db_connection()
    conceptos = conn.execute('SELECT * FROM conceptos_salariales').fetchall()
    conn.close()
    return render_template('admin_conceptos.html', conceptos=conceptos)

@app.route('/admin/conceptos/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def crear_concepto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        recurrente = 1 if 'recurrente' in request.form else 0
        afecta_ips = 1 if 'afecta_ips' in request.form else 0
        afecta_aguinaldo = 1 if 'afecta_aguinaldo' in request.form else 0
        monto_fijo = request.form.get('monto_fijo') or None
        porcentaje = request.form.get('porcentaje') or None

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO conceptos_salariales
            (nombre, tipo, recurrente, afecta_ips, afecta_aguinaldo, monto_fijo, porcentaje)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, recurrente, afecta_ips, afecta_aguinaldo, monto_fijo, porcentaje))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_conceptos'))

    return render_template('admin_conceptos_form.html', concepto=None)

@app.route('/admin/conceptos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_concepto(id):
    conn = get_db_connection()
    concepto = conn.execute('SELECT * FROM conceptos_salariales WHERE id = ?', (id,)).fetchone()

    if not concepto:
        conn.close()
        return "Concepto no encontrado", 404

    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        recurrente = 1 if 'recurrente' in request.form else 0
        afecta_ips = 1 if 'afecta_ips' in request.form else 0
        afecta_aguinaldo = 1 if 'afecta_aguinaldo' in request.form else 0
        monto_fijo = request.form.get('monto_fijo') or None
        porcentaje = request.form.get('porcentaje') or None

        conn.execute("""
            UPDATE conceptos_salariales
            SET nombre=?, tipo=?, recurrente=?, afecta_ips=?, afecta_aguinaldo=?, monto_fijo=?, porcentaje=?
            WHERE id=?
        """, (nombre, tipo, recurrente, afecta_ips, afecta_aguinaldo, monto_fijo, porcentaje, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_conceptos'))

    conn.close()
    return render_template('admin_conceptos_form.html', concepto=concepto)

@app.route('/admin/conceptos/eliminar/<int:id>')
@login_required
@role_required('admin')
def eliminar_concepto(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM conceptos_salariales WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_conceptos'))


# -----------------------
# Conceptos puntuales por empleado
# -----------------------
@app.route('/admin/conceptos_empleado/<int:empleado_id>')
@login_required
@role_required('admin')
def listar_conceptos_empleado(empleado_id):
    conn = get_db_connection()
    empleado = conn.execute('SELECT * FROM empleados WHERE id=?', (empleado_id,)).fetchone()
    conceptos = conn.execute("""
        SELECT ce.id, cs.nombre, cs.tipo, ce.monto_fijo, ce.porcentaje, ce.fecha_aplicacion
        FROM conceptos_empleado ce
        JOIN conceptos_salariales cs ON ce.concepto_id = cs.id
        WHERE ce.empleado_id=?
    """, (empleado_id,)).fetchall()
    conn.close()
    return render_template('admin_conceptos_empleado.html', empleado=empleado, conceptos=conceptos)


@app.route('/admin/conceptos_empleado/nuevo/<int:empleado_id>', methods=['GET','POST'])
@login_required
@role_required('admin')
def crear_concepto_empleado(empleado_id):
    conn = get_db_connection()
    empleado = conn.execute('SELECT * FROM empleados WHERE id=?', (empleado_id,)).fetchone()
    conceptos = conn.execute('SELECT * FROM conceptos_salariales').fetchall()
    
    if request.method == 'POST':
        concepto_id = request.form['concepto_id']
        monto_fijo = request.form.get('monto_fijo') or None
        porcentaje = request.form.get('porcentaje') or None
        fecha_aplicacion = request.form['fecha_aplicacion']
        
        conn.execute("""
            INSERT INTO conceptos_empleado (empleado_id, concepto_id, monto_fijo, porcentaje, fecha_aplicacion, recurrente)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (empleado_id, concepto_id, monto_fijo, porcentaje, fecha_aplicacion))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_conceptos_empleado', empleado_id=empleado_id))
    
    conn.close()
    return render_template('admin_conceptos_empleado_form.html', empleado=empleado, conceptos=conceptos)


@app.route('/admin/conceptos_empleado/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def editar_concepto_empleado(id):
    conn = get_db_connection()
    concepto = conn.execute('SELECT * FROM conceptos_empleado WHERE id = ?', (id,)).fetchone()
    if not concepto:
        conn.close()
        return "Concepto no encontrado", 404

    empleado = conn.execute('SELECT * FROM empleados WHERE id = ?', (concepto['empleado_id'],)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        monto_fijo = request.form.get('monto_fijo') or None
        porcentaje = request.form.get('porcentaje') or None

        conn.execute("""
            UPDATE conceptos_empleado
            SET nombre=?, tipo=?, monto_fijo=?, porcentaje=?
            WHERE id=?
        """, (nombre, tipo, monto_fijo, porcentaje, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_conceptos_empleado', empleado_id=empleado['id']))

    conn.close()
    return render_template('admin_concepto_empleado_form.html', empleado=empleado, concepto=concepto)

@app.route('/admin/conceptos_empleado/eliminar/<int:id>')
@login_required
@role_required('admin')
def eliminar_concepto_empleado(id):
    conn = get_db_connection()
    concepto = conn.execute('SELECT * FROM conceptos_empleado WHERE id = ?', (id,)).fetchone()
    if not concepto:
        conn.close()
        return "Concepto no encontrado", 404
    empleado_id = concepto['empleado_id']
    conn.execute('DELETE FROM conceptos_empleado WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_conceptos_empleado', empleado_id=empleado_id))

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
