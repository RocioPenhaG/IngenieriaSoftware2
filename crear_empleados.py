import sqlite3

conn = sqlite3.connect('usuarios.db')
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
    fecha_ingreso TEXT NOT NULL,
    hijos INTEGER DEFAULT 0,
    ips TEXT
)
""")

conn.commit()
conn.close()

print("Tabla 'empleados' creada o actualizada correctamente.")
