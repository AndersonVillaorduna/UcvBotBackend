from flask import Blueprint, jsonify, request

chatRoutes = Blueprint('chats',__name__)

@chatRoutes.route('/',methods=['GET'])
def findById(id):
    data=request.json
    return jsonify(data)

@chatRoutes.route('/',methods=['POST'])
def create():
    data=request.json
    return jsonify(data)

@chatRoutes.route('/',methods=['PUT'])
def update(id):
    data=request.json
    return jsonify(data)

@chatRoutes.route('/',methods=['POST'])
def delete(id):
    data=request.json
    return jsonify(data)