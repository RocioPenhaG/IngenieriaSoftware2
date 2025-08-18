# archivo: alterar_conceptos_salariales.py
import sqlite3

def asegurar_columnas_conceptos():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # Verificamos las columnas existentes
    cursor.execute("PRAGMA table_info(conceptos_salariales)")
    columnas = [col[1] for col in cursor.fetchall()]
    print("Columnas actuales:", columnas)

    # Si no existe 'descripcion', la agregamos
    if "descripcion" not in columnas:
        cursor.execute("ALTER TABLE conceptos_salariales ADD COLUMN descripcion TEXT")
        print("Columna 'descripcion' agregada ✅")
    else:
        print("La columna 'descripcion' ya existe.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    asegurar_columnas_conceptos()
