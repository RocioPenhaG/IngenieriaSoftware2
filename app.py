from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones"

# Función para conectar a la base
def get_db_connection():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND password = ?", (correo, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session["correo"] = usuario["correo"]
            session["rol"] = usuario["rol"]

            if usuario["rol"] == "admin":
                return redirect(url_for("admin"))
            elif usuario["rol"] == "gerente":
                return redirect(url_for("gerente"))
            elif usuario["rol"] == "empleado":
                return redirect(url_for("empleado"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html", usuario=session["correo"])

@app.route("/gerente")
def gerente():
    if session.get("rol") != "gerente":
        return redirect(url_for("login"))
    return render_template("gerente.html", usuario=session["correo"])

@app.route("/empleado")
def empleado():
    if session.get("rol") != "empleado":
        return redirect(url_for("login"))
    return render_template("empleado.html", usuario=session["correo"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
