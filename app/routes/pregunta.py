from flask import Blueprint, request, jsonify
import datetime, uuid, os, json
from dotenv import load_dotenv
import google.generativeai as genai
from mini_db.conexion import conectar_db
import uuid

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

pregunta_bp = Blueprint('pregunta_bp', __name__)

@pregunta_bp.route('/pregunta', methods=['POST'])
def procesar_pregunta():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        user_uid = data.get('user_uid')
        session_id = data.get('session_id')

        if not prompt or not user_uid or not session_id:
            return jsonify({"error": "Faltan datos"}), 400

        model = genai.GenerativeModel('gemini-2.5-flash')
        respuesta = model.generate_content(prompt).text.strip()

        v_id = str(uuid.uuid4())
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, user_uid))

        cursor.execute("""
            INSERT INTO chat (v_id, v_title, student_id, respuesta, fecha, level_id, session_id)
            VALUES (%s, %s, %s, %s, %s, NULL, %s)
        """, (v_id, prompt, user_uid, respuesta, datetime.datetime.now(), session_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"respuesta": respuesta})

    except Exception as e:
        print("❌ Error interno:", str(e))
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500


@pregunta_bp.route('/sesion', methods=['POST'])
def crear_sesion():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        student_id = data.get('student_id')

        if not session_id or not student_id:
            return jsonify({"error": "Faltan datos"}), 400

        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM chat_session WHERE session_id = %s", (session_id,))
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("""
                INSERT INTO chat_session (session_id, student_id)
                VALUES (%s, %s)
            """, (session_id, student_id))
            conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Sesión registrada correctamente"})

    except Exception as e:
        print("❌ Error creando sesión:", str(e))
        return jsonify({"error": "Error creando sesión", "detalle": str(e)}), 500


@pregunta_bp.route('/historial/<session_id>/<student_id>', methods=['GET'])
def obtener_historial(session_id, student_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT v_title, respuesta
            FROM chat
            WHERE session_id = %s AND student_id = %s
            ORDER BY fecha ASC
        """, (session_id, student_id))

        mensajes = cursor.fetchall()
        cursor.close()
        conn.close()

        historial = []
        for pregunta, respuesta in mensajes:
            historial.append({"de": "usuario", "texto": pregunta})
            historial.append({"de": "bot", "texto": respuesta})

        return jsonify(historial)

    except Exception as e:
        print("❌ Error al obtener historial:", str(e))
        return jsonify({"error": "Error al obtener historial", "detalle": str(e)}), 500


@pregunta_bp.route('/sesiones/<student_id>', methods=['GET'])
def obtener_sesiones(student_id):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT session_id, MAX(fecha) as ultima_fecha
            FROM chat
            WHERE student_id = %s
            GROUP BY session_id
            ORDER BY ultima_fecha DESC
        """, (student_id,))
        sesiones = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify([{"session_id": s[0], "ultima_fecha": s[1].isoformat()} for s in sesiones])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Subir pregunta desde el front.
@pregunta_bp.route('/generar_preguntas', methods=['POST'])
def generar_preguntas():
    data = request.get_json()
    historial = data.get('mensajes', [])

    if not isinstance(historial, list) or not all(isinstance(m, str) for m in historial):
        return jsonify({"error": "Historial debe ser una lista de strings"}), 400

    texto_historial = "\n".join([f"Usuario: {m}" for m in historial])

    prompt = f"""
Eres un generador de exámenes. A partir de esta conversación del estudiante:

{texto_historial}

Genera 20 preguntas de opción múltiple en formato JSON, como este:

[
  {{
    "texto": "¿Qué es una variable en Java?",
    "opciones": ["Una clase", "Una función", "Un contenedor de datos", "Ninguna de las anteriores"],
    "respuestaCorrecta": "Un contenedor de datos"
  }}
]
El resultado debe ser un JSON válido de 20 objetos, sin explicaciones adicionales. No uses Markdown.
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        preguntas = json.loads(response.text.strip())
        return jsonify(preguntas)

    except Exception as e:
        print("❌ Error generando preguntas con Gemini:", str(e))
        return jsonify({"error": "Error al generar preguntas", "detalle": str(e)}), 500
    

@pregunta_bp.route('/CargarPreguntas', methods=['GET'])
def cargar_preguntas():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT v_content FROM alternative")
        preguntas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(preguntas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@pregunta_bp.route('/InsertarPregunta', methods=['POST'])
def insertar_pregunta():
    try:
        data = request.get_json()
        v_content = data.get('v_content')

        if not v_content:
            return jsonify({"error": "Falta el campo v_content"}), 400

        v_id = str(uuid.uuid4())

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alternative (v_id, v_content) VALUES (%s, %s)", (v_id, v_content))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Pregunta insertada correctamente", "v_id": v_id})
    except Exception as e:
        return