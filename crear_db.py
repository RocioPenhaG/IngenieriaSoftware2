import sqlite3

# Conexión a la base
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")

# Usuarios de prueba
usuarios = [
    ("admin@example.com", "1234", "admin"),
    ("gerente@example.com", "1234", "gerente"),
    ("empleado@example.com", "1234", "empleado")
]

# Insertar datos
for correo, password, rol in usuarios:
    try:
        cursor.execute("INSERT INTO usuarios (correo, password, rol) VALUES (?, ?, ?)",
                       (correo, password, rol))
    except sqlite3.IntegrityError:
        pass  # Ya existe

conn.commit()
conn.close()
print("Base de datos creada con usuarios de prueba")
