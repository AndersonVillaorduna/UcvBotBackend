import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from mini_db.conexion import conectar_db
import psycopg2.extras

# Configurar logging (si no está configurado antes)
logging.basicConfig(level=logging.INFO)

perfil_bp = Blueprint('perfil_bp', __name__)

@perfil_bp.route('/perfil', methods=['GET', 'PUT', 'OPTIONS'])
@cross_origin()
def perfil():
    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'GET':
        user_uid = request.args.get('user_uid')
        logging.info(f'🔎 Buscando perfil con UID: {user_uid}')
        try:
            conexion = conectar_db()
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("""
                SELECT v_userName, v_email, v_username, v_apellidoPaterno, v_apellidoMaterno
                FROM student WHERE v_userUID = %s
            """, (user_uid,))
            usuario = cursor.fetchone()

            if usuario:
                datos_usuario = dict(usuario)
                logging.info(f'✅ Usuario encontrado: {datos_usuario}')
                print(f'✅ Usuario encontrado: {datos_usuario}')
                return jsonify(datos_usuario), 200
            else:
                logging.warning('⚠️ Usuario no encontrado')
                return jsonify({'error': 'Usuario no encontrado'}), 404
        except Exception as e:
            logging.error(f'❌ Error al obtener perfil: {e}')
            return jsonify({'error': str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json(force=True)
            user_uid = data.get('user_uid')
            nombre = data.get('v_userName')
            correo = data.get('v_email')
            username = data.get('v_username')
            apellidoPaterno = data.get('v_apellidoPaterno')
            apellidoMaterno = data.get('v_apellidoMaterno')

            # Si no viene username, derivarlo del correo
            if not username and correo:
                username = correo.split('@')[0]
                logging.info(f'🛠 Derivado username del correo: {username}')

            logging.info(f'🔄 Actualizando perfil UID {user_uid} con: {nombre}, {correo}, {username}, {apellidoPaterno}, {apellidoMaterno}')

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

            logging.info('✅ Perfil actualizado correctamente')
            return jsonify({'mensaje': 'Perfil actualizado correctamente'}), 200

        except Exception as e:
            logging.error(f'❌ Error al actualizar perfil: {e}')
            return jsonify({'error': str(e)}), 500
