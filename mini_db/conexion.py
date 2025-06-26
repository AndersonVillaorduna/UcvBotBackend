import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # tu contraseña si tienes
            database="ucvbot"  # nombre exacto de tu BD
        )
        return conexion
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None
