import logging
import traceback
from flask import Blueprint, request, jsonify
from mini_db.conexion import conectar_db
import psycopg2.extras

logging.basicConfig(level=logging.INFO)

perfil_bp = Blueprint('perfil_bp', __name__)

@perfil_bp.route('/perfil', methods=['GET', 'PUT'])
def perfil():

    if request.method == 'GET':
        user_uid = request.args.get('user_uid')
        logging.info(f'🔎 Buscando perfil con UID: {user_uid}')
        
        if not user_uid:
            logging.warning('⚠️ Falta parámetro user_uid')
            return jsonify({'error': 'user_uid parameter is required'}), 400

        try:
            conexion = conectar_db()
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("""
                SELECT 
                    v_userName, 
                    v_email, 
                    v_apellidoPaterno, 
                    v_apellidoMaterno
                FROM student
                WHERE v_userUID = %s
            """, (user_uid,))
            
            usuario = cursor.fetchone()

            if usuario:
                datos_usuario = {
                    "v_userName": usuario["v_userName"],
                    "v_email": usuario["v_email"],
                    "v_apellidoPaterno": usuario["v_apellidoPaterno"],
                    "v_apellidoMaterno": usuario["v_apellidoMaterno"]
                }
                logging.info(f'✅ Usuario encontrado: {datos_usuario}')
                return jsonify(datos_usuario), 200
            else:
                logging.warning('⚠️ Usuario no encontrado')
                return jsonify({'error': 'Usuario no encontrado'}), 404

        except Exception as e:
            logging.error(f'❌ Error al obtener perfil: {e}')
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    elif request.method == 'PUT':
        try:
            data = request.get_json(force=True)
            user_uid = data.get('user_uid')
            v_userName = data.get('v_userName')
            v_email = data.get('v_email')
            apellidoPaterno = data.get('v_apellidoPaterno')
            apellidoMaterno = data.get('v_apellidoMaterno')

            if not v_userName and v_email:
                v_userName = v_email.split('@')[0]
                logging.info(f'🛠 Derivado nombre del correo: {v_userName}')

            logging.info(f'🔄 Actualizando perfil UID {user_uid} con: {v_userName}, {v_email}, {apellidoPaterno}, {apellidoMaterno}')

            conexion = conectar_db()
            cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("""
                UPDATE student SET 
                    v_userName = %s,
                    v_email = %s,
                    v_apellidoPaterno = %s,
                    v_apellidoMaterno = %s
                WHERE v_userUID = %s
            """, (v_userName, v_email, apellidoPaterno, apellidoMaterno, user_uid))
            conexion.commit()

            logging.info('✅ Perfil actualizado correctamente')
            return jsonify({'mensaje': 'Perfil actualizado correctamente'}), 200

        except Exception as e:
            logging.error(f'❌ Error al actualizar perfil: {e}')
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()
