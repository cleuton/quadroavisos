import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from datetime import datetime
from database.modelo import Usuario
from database.db_usuario import cadastrar_usuario
import logging

logger = logging.getLogger("backend")

def cadastrar_novo_usuario(usuario: Usuario) -> Optional[int]:
    flog = f"{__file__}::cadastrar_usuario;"
    try:
        return cadastrar_usuario(usuario)
    except ValueError as e:
        logger.error(f"{flog}{e}")
        raise