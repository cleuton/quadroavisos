import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from database.modelo import Quadro
from database.db_quadro import deletar_quadro
import logging

logger = logging.getLogger("backend")

def remover_quadro(idUsuarioLogado: int, idQuadro: int):
    flog = f"{__file__}::remover_quadro;"
    try:
        deletar_quadro(idUsuarioLogado, idQuadro)
        return
    except Exception as e:
        logger.error(f"{flog}{e}")
        raise