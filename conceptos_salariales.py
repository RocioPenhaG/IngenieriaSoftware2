# archivo: init_conceptos_salariales.py
import sqlite3

def inicializar_conceptos():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conceptos_salariales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        descripcion TEXT
    )
    """)

    # Insertar algunos conceptos básicos si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM conceptos_salariales")
    count = cursor.fetchone()[0]

    if count == 0:
        conceptos_iniciales = [
            ("Sueldo Básico", "Ingreso", "Pago base mensual"),
            ("Bono de Productividad", "Ingreso", "Premio por desempeño"),
            ("Horas Extras", "Ingreso", "Pago por horas adicionales"),
            ("IPS", "Descuento", "Aporte a la seguridad social"),
            ("Anticipo", "Descuento", "Adelanto de salario")
        ]
        cursor.executemany(
            "INSERT INTO conceptos_salariales (nombre, tipo, descripcion) VALUES (?, ?, ?)",
            conceptos_iniciales
        )
        print("Conceptos salariales iniciales insertados")
    else:
        print("Ya existen conceptos en la tabla. No se insertaron nuevos.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_conceptos()
