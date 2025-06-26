from flask import Blueprint, jsonify, request

messageRoutes = Blueprint('messages',__name__)

@messageRoutes.route('/',methods=['GET'])
def findById(id):
    data=request.json
    return jsonify(data)

@messageRoutes.route('/',methods=['POST'])
def create():
    data=request.json
    return jsonify(data)

@messageRoutes.route('/',methods=['PUT'])
def update(id):
    data=request.json
    return jsonify(data)

@messageRoutes.route('/',methods=['POST'])
def delete(id):
    data=request.json
    return jsonify(data)