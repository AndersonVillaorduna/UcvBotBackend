from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from mini_db.conexion import conectar_db
import uuid

levelRoutes = Blueprint('levelRoutes', __name__)

@levelRoutes.route('/nivel', methods=['POST', 'OPTIONS'])
@cross_origin()
def guardar_puntaje():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight CORS

    try:
        data = request.get_json(force=True)
        puntaje = data.get('puntaje')
        estudiante_id = data.get('student_id')
        nombre_estudiante = data.get('nombre')

        # Generar UUID para v_id
        nivel_id = str(uuid.uuid4())

        conn = conectar_db()
        cursor = conn.cursor()

        # Usar v_id en lugar de id_level
        query = "INSERT INTO level (v_id, puntaje, student_id, v_name) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nivel_id, puntaje, estudiante_id, nombre_estudiante))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Puntaje guardado correctamente'}), 200

    except Exception as e:
        print("❌ Error al guardar puntaje:", e)
        return jsonify({'error': str(e)}), 500
