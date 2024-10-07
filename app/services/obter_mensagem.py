import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database.modelo import MensagemComReacoes
from typing import Optional
from database.db_mensagens import obter_mensagem, obter_reacoes_com_nome_usuario
import logging

logger = logging.getLogger("backend")

def obter_mensagem_com_reacoes(idMensagem: int, idUsuarioLogado: int) -> Optional[MensagemComReacoes]:
    mensagem = obter_mensagem(idMensagem, idUsuarioLogado)
    if mensagem:
        reacoes = obter_reacoes_com_nome_usuario(idMensagem, mensagem.idQuadro, idUsuarioLogado)
        mensagemComReacoes = MensagemComReacoes(mensagem, reacoes)
        return mensagemComReacoes
    return None

def obter_anexo_mensagem(idMensagem: int, idUsuarioLogado: int) -> Optional[str]:
    mensagem = obter_mensagem(idMensagem, idUsuarioLogado)
    if mensagem:
        return mensagem.anexo
    return None



