import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import Optional, List
from database.modelo import Usuario, QuadroUltimaMensagem
from database.db_usuario import obter_usuario
from database.db_quadro import obter_quadros_usuario
import logging

logger = logging.getLogger("backend")

# Só pode obter os dados de um usuário: O próprio ou um admim. E a senha nunca vem em aberto
def obter_dados_usuario(idUsuarioLogado: int, idUsuario: int) -> Optional[Usuario]:
    flog = f"{__file__}::obter_dados_usuario;"
    if not (idUsuarioLogado == idUsuario):
        usuarioLogado = obter_usuario(idUsuarioLogado)
        if not usuarioLogado.ehAdmin:
            mensagem = f"Usuario: {idUsuarioLogado} tentando obter dados do usuário: {idUsuario} sem ter direito!"
            logger.error(f"{flog}{mensagem}")
            raise ValueError(mensagem)
    return obter_usuario(idUsuario)

# Este método retorna instância de QuadroUltimaMensagem
def obter_usuario_com_quadros(idUsuarioLogado: int, idUsuario: int) -> Optional[List[QuadroUltimaMensagem]]:
    flog = f"{__file__}::obter_usuario_com_quadros;"
    if not (idUsuarioLogado == idUsuario):
        usuarioLogado = obter_usuario(idUsuarioLogado)
        if not usuarioLogado.ehAdmin:
            mensagem = f"Usuario: {idUsuarioLogado} tentando obter quadros do usuário: {idUsuario} sem ter direito!"
            logger.error(f"{flog}{mensagem}")
            raise ValueError(mensagem)
    return obter_quadros_usuario(idUsuario)

