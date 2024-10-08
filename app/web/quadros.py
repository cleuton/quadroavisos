from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.obter_quadros_usuario import obter_quadros
import json

# Criação de um blueprint para modularizar as rotas
quadros_blueprint = Blueprint('quadros', __name__)

@quadros_blueprint.route('/quadros', methods=['GET'])
@jwt_required()
def listar_quadros_route():
    quadros_usuario = obter_quadros(get_jwt_identity())
    quadros_serializavel = [quadro.to_dict() for quadro in quadros_usuario]
    return jsonify(quadros_serializavel)