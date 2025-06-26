from flask import Blueprint, request, jsonify
from mini_db.conexion import conectar_db
import logging

perfil_bp = Blueprint('perfil_bp', __name__)

@perfil_bp.route('/perfil', methods=['GET'])
def obtener_perfil():
    user_uid = request.args.get('user_uid')

    try:
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                v_userUID AS user_uid,
                v_userName AS nombre,
                v_apellidoPaterno AS apellidoPaterno,
                v_apellidoMaterno AS apellidoMaterno,
                v_email AS correo,
                SUBSTRING_INDEX(v_email, '@', 1) AS usuario,
                v_photoURL AS foto
            FROM student
            WHERE v_userUID = %s
        """, (user_uid,))

        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
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

        if foto and len(foto) > 500000:
            return jsonify({'error': 'La imagen es muy grande'}), 400

        logging.debug(f"📦 Datos recibidos: {data}")

        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE student
            SET v_userName = %s,
                v_apellidoPaterno = %s,
                v_apellidoMaterno = %s,
                v_photoURL = %s
            WHERE v_userUID = %s
        """, (nombre, apellidoPaterno, apellidoMaterno, foto, user_uid))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': 'Perfil actualizado correctamente'}), 200
    except Exception as e:
        logging.exception("❌ Error en PUT /perfil")
        return jsonify({'error': str(e)}), 500