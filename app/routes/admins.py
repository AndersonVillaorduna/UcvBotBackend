from flask import Blueprint, jsonify, request
import uuid
from app.models import admin

adminRoutes = Blueprint('admins',__name__)

@adminRoutes.route('/<string:id>',methods=['GET'])
def findById(id):
    data=admin.findById(id)
    if data:
        return jsonify(data)
    return jsonify({"mensaje":"Admin no encontrado"}),404

@adminRoutes.route('/',methods=['POST'])
def create():
    data=request.json
    id = str(uuid.uuid4())
    user = admin.create(
        id,
        data['v_userName'],
        data["v_email"],
        data["v_password"]
    )
    return jsonify({"mensaje":"Admin creado",
                    "id":id})

@adminRoutes.route('/<string:id>',methods=['PUT'])
def update(id):
    data=request.json
    user = admin.update(id,
                        data['v_userName'],
                        data["v_email"],
                        data["v_password"])
    if user:
        return jsonify({"mensaje":f"Admin {id} actualizado"})
    return jsonify({"mensaje":"Admin no encontrado"}),404

@adminRoutes.route('/<string:id>',methods=['DELETE'])
def delete(id):
    user = admin.delete(id)
    if user:
        return jsonify({"mensaje":f"Admin {id} eliminado"})
    return jsonify({"mensaje":"Admin no encontrado"}),404

@adminRoutes.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data.get('v_userName')
    password = data.get('v_password')
    user = admin.findByUserName(username)
    if user and user['v_password']==password:
        return jsonify({"mensaje":"Login exitoso","user":user}),200
    return jsonify({"mensaje":"Usuario o contraseña incorrectos"}),401


@adminRoutes.route("/reset",methods=['PUT'])
def resetPassword():
    data=request.json
    username=data.get("v_userName")
    email=data.get("v_email")
    password=data.get("v_password")
    user = admin.resetPassword(username,email,password)
    if user:
        return jsonify({"mensaje":"Contraseña actualizada"})
    return jsonify({"mensaje":"Admin no encontrado"}),404