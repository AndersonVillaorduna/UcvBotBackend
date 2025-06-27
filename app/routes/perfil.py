from flask import Blueprint, request, jsonify
from mini_db.conexion import conectar_db
import logging
import psycopg2.extras

perfil_bp = Blueprint('perfil_bp', __name__)
logging.basicConfig(level=logging.INFO)

@perfil_bp.route('/perfil', methods=['GET'])
def obtener_perfil():
    user_uid = request.args.get('user_uid')

    try:
        conexion = conectar_db()
        if not conexion:
            logging.error("❌ No se pudo conectar a la base de datos")
            return jsonify({'error': 'Fallo en la conexión a la base de datos'}), 500

        cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("""
            SELECT 
                v_userUID AS "user_uid",
                v_userName AS "nombre",
                v_apellidoPaterno AS "apellidoPaterno",
                v_apellidoMaterno AS "apellidoMaterno",
                v_email AS "correo",
                SPLIT_PART(v_email, '@', 1) AS "usuario",
                v_photoURL AS "foto"
            FROM student
            WHERE v_userUID = %s
        """, (user_uid,))

        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()

        if resultado:
            return jsonify(dict(resultado))
        else:
            logging.warning('⚠️ Usuario no encontrado')
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except Exception as e:
        logging.exception("❌ Error al obtener perfil")
        return jsonify({'error': str(e)}), 500

@perfil_bp.route('/perfil', methods=['PUT'])
def actualizar_perfil():
    try:
        data = request.get_json(force=True)
        user_uid = data.get('user_uid')
        nombre = data.get('nombre')
        apellidoPaterno = data.get('apellidoPaterno')
        apellidoMaterno = data.get('apellidoMaterno')
        foto = data.get('foto')

        if not all([user_uid, nombre, apellidoPaterno, apellidoMaterno]):
            return jsonify({'error': 'Faltan datos requeridos'}), 400

        # Permitir imágenes base64 hasta 1.5MB aprox (base64 es ~33% más grande que el archivo real)
        if foto and len(foto) > 1500000:
            return jsonify({'error': 'La imagen es demasiado grande. Usa una menor a 1.5MB'}), 400

        # Validar tipo MIME base64 (opcional)
        if foto and not (foto.startswith('data:image/jpeg;base64,') or foto.startswith('data:image/png;base64,')):
            return jsonify({'error': 'Formato de imagen no permitido. Solo JPG o PNG'}), 400

        logging.info(f"🔄 Actualizando perfil UID {user_uid}")

        conexion = conectar_db()
        if not conexion:
            logging.error("❌ No se pudo conectar a la base de datos para actualizar")
            return jsonify({'error': 'Fallo en la conexión a la base de datos'}), 500

        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE student
            SET v_userName = %s,
                v_apellidoPaterno = %s,
                v_apellidoMaterno = %s,
                v_photoURL = %s
            WHERE v_userUID = %s
        """, (nombre, apellidoPaterno, apellidoMaterno, foto, user_uid))

        conexion.commit()
        cursor.close()
        conexion.close()

        logging.info("✅ Perfil actualizado correctamente")
        return jsonify({'mensaje': 'Perfil actualizado correctamente'}), 200

    except Exception as e:
        logging.exception("❌ Error en PUT /perfil")
        return jsonify({'error': str(e)}), 500
