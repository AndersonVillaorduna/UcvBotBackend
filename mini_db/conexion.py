import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()

def conectar_db():
    try:
        db_url = os.getenv("urldatabase")
        if not db_url:
            print("❌ Error: La variable de entorno 'urldatabase' no está configurada.")
            return None

        conexion = psycopg2.connect(db_url)
        return conexion
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None
