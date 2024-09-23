import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import List, Optional
from database.modelo import QuadroUltimaMensagem
from database.db_quadro import obter_quadros_usuario
import logging

logger = logging.getLogger("backend")

def obter_quadros(idUsuario: Optional[int]) -> List[QuadroUltimaMensagem]:
    flog = f"{__file__}::obter_quadros;"
    quadros = obter_quadros_usuario(idUsuario)
    if not quadros:
        if not idUsuario:
            mensagem = f"Login anônimo sem nenhum quadro público!"
            logger.error(f"{flog}{mensagem}")
        else:
            mensagem = f"Login do usuário: {idUsuario} sem nenhum quadro retornado!!!!"
            logger.error(f"{flog}{mensagem}")
        return []
    return quadros
