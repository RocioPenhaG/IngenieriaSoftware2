import sqlite3

def actualizar_tabla_empleados():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # 1. Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cedula TEXT NOT NULL UNIQUE,
        fecha_nacimiento TEXT NOT NULL,
        estado_civil TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario_base REAL NOT NULL,
        fecha_ingreso TEXT NOT NULL
    )
    """)

    # 2. Revisar qué columnas tiene actualmente
    cursor.execute("PRAGMA table_info(empleados)")
    columnas = [col[1] for col in cursor.fetchall()]

    # 3. Agregar columnas si faltan
    if "hijos" not in columnas:
        cursor.execute("ALTER TABLE empleados ADD COLUMN hijos INTEGER DEFAULT 0")
        print("Columna 'hijos' agregada.")

    if "ips" not in columnas:
        cursor.execute("ALTER TABLE empleados ADD COLUMN ips TEXT")
        print("Columna 'ips' agregada.")

    conn.commit()
    conn.close()
    print("Actualización de la tabla 'empleados' completada.")

if __name__ == "__main__":
    actualizar_tabla_empleados()
