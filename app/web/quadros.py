from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.obter_quadros_usuario import obter_quadros
from services.cadastrar_quadro_service import registrar_quadro
from services.alterar_quadro_service import atualizar_quadro
from services.deletar_quadro_service import remover_quadro
from database.modelo import Quadro
import json

# Criação de um blueprint para modularizar as rotas
quadros_blueprint = Blueprint('quadros', __name__)
post_quadros_blueprint = Blueprint('post_quadros', __name__)
put_quadros_blueprint = Blueprint('put_quadros', __name__)

delete_quadros_blueprint = Blueprint('delete_quadros', __name__)


@quadros_blueprint.route('/quadros', methods=['GET'])
@jwt_required()
def listar_quadros_route():
    quadros_usuario = obter_quadros(get_jwt_identity())
    quadros_serializavel = [quadro.to_dict() for quadro in quadros_usuario]
    return jsonify(quadros_serializavel)


@post_quadros_blueprint.route('/quadros', methods=['POST'])
@jwt_required()
def novo_quadro_route():
    idUsuario = get_jwt_identity()
    novo_quadro = Quadro.from_dict(request.json)
    idQuadro = registrar_quadro(novo_quadro, idUsuario)
    return {"idQuadro": idQuadro}, 201


@put_quadros_blueprint.route('/quadros/<idQuadro>', methods=['PUT'])
@jwt_required()
def alterar_quadro_route(idQuadro: int):
    idUsuario = get_jwt_identity()
    quadro = Quadro.from_dict(request.json)
    if int(idQuadro) != quadro.id:
        return '{"status": "Erro! Identificador na URL diferente do recurso passado"}', 422
    atualizar_quadro(quadro, idUsuario)
    return '', 204


@delete_quadros_blueprint.route('/quadros/<idQuadro>', methods=['DELETE'])
@jwt_required()
def eliminar_quadro_route(idQuadro: int):
    idUsuario = get_jwt_identity()
    remover_quadro(idUsuario, idQuadro)
    return '', 204
