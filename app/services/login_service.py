import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional
from database.db_usuario import validar_usuario
from database.modelo import Usuario
import logging

logger = logging.getLogger("backend")

def login(username: str, password: str) -> Optional[Usuario]:
    flog = f"{__file__}::login;"
    usuario = validar_usuario(username, password)
    if usuario:
        return usuario
    mensagem = f"Tentativa de login inválido. Usuário: {username}"
    logger.error(f"{flog}{mensagem}")
    return None


