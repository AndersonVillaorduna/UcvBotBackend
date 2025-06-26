from flask import Blueprint, request, jsonify
import uuid
import bcrypt
from mini_db.conexion import conectar_db

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()

    username = data.get('username')
    apellidoPaterno = data.get('apellidoPaterno')
    apellidoMaterno = data.get('apellidoMaterno')
    carrera = data.get('carrera')
    email = data.get('email')
    password = data.get('password')

    user_id = str(uuid.uuid4())

    try:
        conexion = conectar_db()
        if conexion is None:
            return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500

        cursor = conexion.cursor()

        # ✅ Verificar si el email ya existe
        cursor.execute("SELECT * FROM student WHERE v_email = %s", (email,))
        existe = cursor.fetchone()
        if existe:
            cursor.close()
            conexion.close()
            return jsonify({'error': 'Este correo ya está registrado.'}), 409

        # ✅ Encriptar la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # ✅ Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO student (
                v_userUID, v_userName, v_apellidoPaterno, v_apellidoMaterno,
                v_carrera, v_email, v_password, v_photoURL,
                level_id, v_correctExercises, v_incorrectExercises, v_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, '', NULL, 0, 0, 0)
        """, (
            user_id, username, apellidoPaterno, apellidoMaterno,
            carrera, email, hashed_password
        ))

        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Registro exitoso', 'userUID': user_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
