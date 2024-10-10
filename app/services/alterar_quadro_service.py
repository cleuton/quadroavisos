import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from database.modelo import Quadro
from database.db_quadro import alterar_quadro
import logging

logger = logging.getLogger("backend")

def atualizar_quadro(quadro: Quadro, idUsuarioLogado: int):
    flog = f"{__file__}::alterar_quadro;"
    try:
        alterar_quadro(idUsuarioLogado, quadro)
        return
    except Exception as e:
        logger.error(f"{flog}{e}")
        raise