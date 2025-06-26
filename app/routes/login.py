from flask import Blueprint, request, jsonify
from mini_db.conexion import conectar_db
import bcrypt

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')

    try:
        conexion = conectar_db()
        if conexion is None:
            return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500

        cursor = conexion.cursor()
        email_completo = f"{username}@ucvvirtual.edu.pe"

        cursor.execute("""
            SELECT v_userUID, v_userName, v_apellidoPaterno, v_password 
            FROM student 
            WHERE v_email = %s
        """, (email_completo,))
        resultado = cursor.fetchone()

        if resultado:
            user_uid, nombre, apellido, hashed_password = resultado
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({
                    'mensaje': 'Inicio de sesión exitoso',
                    'success': True,
                    'user_uid': user_uid,       # <- nombre coherente con la BD
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email_completo,
                    'rol': 'student'
                }), 200
            else:
                return jsonify({'error': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
