from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from app.routes.students import studentRoutes
from app.routes.admins import adminRoutes
from app.routes.alternative import alternativeRoutes
from app.routes.chat import chatRoutes
from app.routes.level import levelRoutes
from app.routes.message import messageRoutes
from app.routes.registro import registro_bp
from app.routes.login import login_bp
from app.routes.perfil import perfil_bp 
from app.routes.pregunta import pregunta_bp

app = Flask(__name__)
app.config['DEBUG'] = True  # ✅ Esto permite ver el traceback del error
CORS(app)

@app.route('/')
def home():
    return "✅ UCV Bot API está activa"

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pregunta = data.get('pregunta', '')
    respuesta = f"Simulación: recibí tu pregunta '{pregunta}' y estoy procesando..."
    return jsonify({'respuesta': respuesta})

# Registrar rutas
app.register_blueprint(studentRoutes, url_prefix='/api/students')
app.register_blueprint(messageRoutes, url_prefix='/api/messages')
app.register_blueprint(levelRoutes, url_prefix='/api/level')
app.register_blueprint(adminRoutes, url_prefix='/api/admins')
app.register_blueprint(alternativeRoutes, url_prefix='/api/alternative')
app.register_blueprint(chatRoutes, url_prefix='/api/chats')
app.register_blueprint(registro_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(perfil_bp, url_prefix='/api')
app.register_blueprint(pregunta_bp, url_prefix='/api')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render usa PORT
    app.run(host="0.0.0.0", port=port)
