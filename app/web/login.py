from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from services.login_service import login

# Criação de um blueprint para modularizar as rotas
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login_route():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    # Lógica de autenticação (exemplo simples)
    if not email or not senha:
        return jsonify({'error': 'Email and senha incorretos'}), 403
    usuario = login(email, senha)
    if not usuario:
        return jsonify({'error': 'Email and senha incorretos'}), 403
    token = create_access_token(identity=usuario.id)
    usuario_dict = usuario.__dict__()
    usuario_dict['token'] = token
    return jsonify(usuario_dict)
