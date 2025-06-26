from mini_db.conexion import conectar_db

def getAll():
    conexion = conectar_db()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student")
        return cursor.fetchall()
    finally:
        conexion.close()
