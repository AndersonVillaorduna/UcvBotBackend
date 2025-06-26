from flask import Blueprint, request, jsonify
from mini_db.conexion import conectar_db
import uuid
import psycopg2.extras

levelRoutes = Blueprint('levelRoutes', __name__)

@levelRoutes.route('/nivel', methods=['POST'])
def guardar_puntaje():
    try:
        data = request.get_json()
        puntaje = data.get('puntaje')
        estudiante_id = data.get('student_id')
        nombre_estudiante = data.get('nombre')

        nivel_id = str(uuid.uuid4())

        conexion = conectar_db()
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = "INSERT INTO level (v_id, puntaje, student_id, v_name) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nivel_id, puntaje, estudiante_id, nombre_estudiante))
        conexion.commit()

        cursor.close()
        conexion.close()

        return jsonify({'mensaje': 'Puntaje guardado correctamente'}), 200

    except Exception as e:
        print("❌ Error al guardar puntaje:", e)
        return jsonify({'error': str(e)}), 500
