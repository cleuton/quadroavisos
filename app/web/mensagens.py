from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.acessar_quadro_com_mensagens import paginar_mensagens_quadro

mensagens_blueprint = Blueprint('mensagens', __name__)

# /mensagens/<idQuadro>?pagina=nn&qtdemsg=nn
@mensagens_blueprint.route('/mensagens/<idQuadro>', methods=['GET'])
@jwt_required()
def get_mensagens_route(idQuadro: int):
    pagina: int = request.args.get(key='pagina', default=1, type=int)
    qtde_msg_pagina: int = request.args.get(key='qtdemsg', default=10, type=int)
    mensagens = paginar_mensagens_quadro(idUsuarioLogado=get_jwt_identity(),
                                         idQuadroDesejado=idQuadro,
                                         pagina=pagina,
                                         mensagens_por_pagina=qtde_msg_pagina)
    return jsonify([mensagem.to_dict() for mensagem in mensagens])