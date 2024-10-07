import os

from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.acessar_quadro_com_mensagens import paginar_mensagens_quadro
from services.obter_mensagem import obter_mensagem_com_reacoes, obter_anexo_mensagem

mensagens_blueprint = Blueprint('mensagens', __name__)
mensagem_blueprint = Blueprint('mensagem', __name__)
mensagem_anexo_blueprint = Blueprint('mensagem_anexo', __name__)

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

@mensagem_blueprint.route('/mensagem/<idMensagem>', methods=['GET'])
@jwt_required()
def get_mensagem_route(idMensagem: str):
    mensagemComReacoes = obter_mensagem_com_reacoes(idMensagem, get_jwt_identity())
    if not mensagemComReacoes:
        return jsonify('{"status":"Não encontrada"}'), 404
    mensagemRetorno = {
        "mensagem": mensagemComReacoes.mensagem.to_dict(),
        "reacoes": [r.to_dict() for r in mensagemComReacoes.reacoes]
    }
    return jsonify(mensagemRetorno)

@mensagem_anexo_blueprint.route('/mensagem/<idMensagem>/anexo', methods=['GET'])
@jwt_required()
def get_anexo_mensagem_route(idMensagem: str):
    anexo = obter_anexo_mensagem(idMensagem, get_jwt_identity())
    if not anexo:
        return jsonify('{"status":"Não encontrada"}'), 404
    try:
        # Obtendo o diretório onde o script atual (script.py) está localizado
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        # Construindo o caminho absoluto para o diretório de imagens
        caminho_imagens = os.path.abspath(os.path.join(diretorio_script, '..', 'images'))

        response = send_from_directory(caminho_imagens, anexo, mimetype='image/png')

        # Ajusta o header content-disposition para inline (ou remove-o)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers["Content-Disposition"] = "inline; filename={}".format(anexo)
        return response
    except FileNotFoundError:
        abort(404)
