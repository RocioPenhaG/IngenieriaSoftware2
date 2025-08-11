from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3

app = Flask(__name__, template_folder='template')
app.secret_key = "is2_proyecto"

def get_db_connection():
    conn = sqlite3.connect("login.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/acceso-login', methods=['POST'])
def login():
    correo = request.form['txtCorreo']
    password = request.form['txtPassword']

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE correo = ? AND password = ?", 
                        (correo, password)).fetchone()
    conn.close()

    if user:
        session['usuario'] = correo
        return redirect(url_for('dashboard'))
    else:
        return "Usuario o contraseña incorrectos", 401

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return f"Bienvenido {session['usuario']}!"
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
