from flask import Blueprint, jsonify, request

alternativeRoutes = Blueprint('alternative',__name__)

@alternativeRoutes.route('/',methods=['GET'])
def findById(id):
    data=request.json
    return jsonify(data)

@alternativeRoutes.route('/',methods=['POST'])
def create():
    data=request.json
    return jsonify(data)

@alternativeRoutes.route('/',methods=['PUT'])
def update(id):
    data=request.json
    return jsonify(data)

@alternativeRoutes.route('/',methods=['POST'])
def delete(id):
    data=request.json
    return jsonify(data)