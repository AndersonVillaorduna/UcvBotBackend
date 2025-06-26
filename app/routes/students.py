from flask import Blueprint, jsonify, request
from app.models import student

studentRoutes = Blueprint('students',__name__)

@studentRoutes.route('/',methods=['GET'])
def getAll():
    data=student.getAll()
    if data:
        return jsonify(data)
    return jsonify({"mensaje":"No encontrado"}),404

