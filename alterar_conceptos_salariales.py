# archivo: alterar_conceptos_salariales.py
import sqlite3

def asegurar_columnas_conceptos():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # Verificamos las columnas existentes
    cursor.execute("PRAGMA table_info(conceptos_salariales)")
    columnas = [col[1] for col in cursor.fetchall()]
    print("Columnas actuales:", columnas)

    # Agregar columna 'descripcion' si falta
    if "descripcion" not in columnas:
        cursor.execute("ALTER TABLE conceptos_salariales ADD COLUMN descripcion TEXT")
        print("Columna 'descripcion' agregada ✅")
    else:
        print("La columna 'descripcion' ya existe.")

    # Agregar columna 'monto' si falta
    if "monto" not in columnas:
        cursor.execute("ALTER TABLE conceptos_salariales ADD COLUMN monto REAL DEFAULT 0")
        print("Columna 'monto' agregada ✅")
    else:
        print("La columna 'monto' ya existe.")

    # Agregar columna 'imponible' si falta
    if "imponible" not in columnas:
        cursor.execute("ALTER TABLE conceptos_salariales ADD COLUMN imponible INTEGER DEFAULT 1")
        print("Columna 'imponible' agregada ✅")
    else:
        print("La columna 'imponible' ya existe.")

    conn.commit()
    conn.close()
    print("Actualización de columnas completada ✅")

if __name__ == "__main__":
    asegurar_columnas_conceptos()
