import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin  # ✅ IMPORTANTE
from mini_db.conexion import conectar_db
import psycopg2.extras

perfil_bp = Blueprint('perfil_bp', __name__)

@perfil_bp.route('/perfil', methods=['GET', 'PUT', 'OPTIONS'])
@cross_origin()  # ✅ SOLUCIÓN AL ERROR CORS
def perfil():
    if request.method == 'OPTIONS':
        return '', 200  # ✅ Respuesta rápida a la verificación previa (preflight)

    if request.method == 'GET':
        user_uid = request.args.get('user_uid')
        try:
            conexion = conectar_db()
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("""
                SELECT v_userName, v_email, v_username, v_apellidoPaterno, v_apellidoMaterno
                FROM student WHERE v_userUID = %s
            """, (user_uid,))
            usuario = cursor.fetchone()
            if usuario:
                return jsonify(dict(usuario)), 200
            else:
                return jsonify({'error': 'Usuario no encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json(force=True)
            user_uid = data.get('user_uid')
            nombre = data.get('nombre')
            correo = data.get('email')
            username = data.get('username')
            apellidoPaterno = data.get('apellidoPaterno')
            apellidoMaterno = data.get('apellidoMaterno')

            conexion = conectar_db()
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE student SET 
                    v_userName = %s,
                    v_email = %s,
                    v_username = %s,
                    v_apellidoPaterno = %s,
                    v_apellidoMaterno = %s
                WHERE v_userUID = %s
            """, (nombre, correo, username, apellidoPaterno, apellidoMaterno, user_uid))
            conexion.commit()
            return jsonify({'mensaje': 'Perfil actualizado correctamente'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
