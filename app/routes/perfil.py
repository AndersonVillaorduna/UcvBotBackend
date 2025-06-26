import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from mini_db.conexion import conectar_db
import psycopg2.extras

# Configurar logging
logging.basicConfig(level=logging.INFO)

perfil_bp = Blueprint('perfil_bp', __name__)

@perfil_bp.route('/perfil', methods=['GET', 'PUT', 'OPTIONS'])
@cross_origin()
def perfil():
    if request.method == 'OPTIONS':
        return '', 200

    # === GET ===
    if request.method == 'GET':
        # FIXED: Changed from 'v_userName' to 'user_uid' to match the URL parameter
        user_uid = request.args.get('user_uid')
        logging.info(f'🔎 Buscando perfil con UID: {user_uid}')
        
        # Add validation to ensure user_uid is provided
        if not user_uid:
            logging.warning('⚠️ user_uid parameter is required')
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
            """, (user_uid,))  # FIXED: Use user_uid instead of v_userName
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
            return jsonify({'error': str(e)}), 500
        finally:
            # Close database connections properly
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()

    # === PUT ===
    elif request.method == 'PUT':
        try:
            data = request.get_json(force=True)
            user_uid = data.get('user_uid')
            v_userName = data.get('v_userName')
            v_email = data.get('v_email')
            apellidoPaterno = data.get('v_apellidoPaterno')
            apellidoMaterno = data.get('v_apellidoMaterno')

            # Si no viene username, derivarlo del correo
            if not v_userName and v_email:
                v_userName = v_email.split('@')[0]
                logging.info(f'🛠 Derivado username del correo: {v_userName}')

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
            return jsonify({'error': str(e)}), 500
        finally:
            # Close database connections properly
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals():
                conexion.close()