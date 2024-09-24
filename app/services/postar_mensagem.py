import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from datetime import datetime
from database.modelo import Mensagem
from database.db_mensagens import cadastrar_mensagem
import logging

logger = logging.getLogger("backend")

# Lembrando que idUsuario é o usuário atualmente logado
def postar_mensagem(idUsuario: int, mensagem: Mensagem) -> Optional[int]:
    flog = f"{__file__}::cadastrar_mensagem;"
    try:
        return cadastrar_mensagem(idUsuario, mensagem)
    except ValueError as e:
        logger.error(f"{flog}{e}")
        raise
