from mini_db.conexion import conectar_db
import psycopg2.extras
def getAll():
    conexion = conectar_db()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM student")
        return cursor.fetchall()
    finally:
        conexion.close()
