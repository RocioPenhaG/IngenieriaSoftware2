import sqlite3

# Conectar (si no existe login.db, se crea)
conn = sqlite3.connect("login.db")
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Insertar usuario de prueba (solo si no existe)
try:
    cursor.execute("INSERT INTO usuarios (correo, password) VALUES (?, ?)", 
                   ("test@example.com", "1234"))
    print("Usuario de prueba creado: test@example.com / 1234")
except sqlite3.IntegrityError:
    print("ℹ Usuario de prueba ya existe")

# Guardar y cerrar
conn.commit()
conn.close()
print("Base de datos lista: login.db")
