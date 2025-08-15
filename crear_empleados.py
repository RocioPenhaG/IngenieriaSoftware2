import sqlite3

conn = sqlite3.connect('usuarios.db')  # usa la misma base que tu app
cursor = conn.cursor()

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

conn.commit()
conn.close()

print("Tabla 'empleados' creada correctamente.")
