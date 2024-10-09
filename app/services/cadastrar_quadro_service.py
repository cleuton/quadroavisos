import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from database.modelo import Quadro
from database.db_quadro import criar_quadro
import logging

logger = logging.getLogger("backend")

def registrar_quadro(quadro: Quadro, idUsuarioLogado: int) -> Optional[int]:
    flog = f"{__file__}::registrar_quadro;"
    try:
        idQuadro = criar_quadro(idUsuarioLogado, quadro)
        return idQuadro
    except Exception as e:
        logger.error(f"{flog}{e}")
        raise