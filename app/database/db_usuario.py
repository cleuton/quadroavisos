from database.db_pool import get_connection, return_connection, sql
from database.modelo import Usuario, PerfilUsuarioQuadro
from database.db_admins import eh_admin
import psycopg2
from typing import List, Optional
import logging

logger = logging.getLogger("backend")

# Obter usuário não checa nada. Será papel da camada de serviço fazer isso
def obter_usuario(id:int) -> Optional[Usuario]:
    flog = f"{__file__}::obter_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute(sql.usuarioById, (id,))
        user = cursor.fetchone()
        
        # Verificar se o usuário foi encontrado
        if user:
            return Usuario(user[0], user[1], user[2], user[3], "*********", user[5])
        else:
            return None
    except Exception as e:
        mensagem = f"Erro ao obter usuário: {id} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def validar_usuario(email:str, password:str) -> Usuario:
    flog = f"{__file__}::validar_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute(sql.usuarioByEmailSenha, (email, password))
        user = cursor.fetchone()
        
        # Verificar se o usuário foi encontrado
        if user:
            return Usuario(user[0], user[1], user[2], user[3], user[4], user[5])
        else:
            return None
    except Exception as e:
        mensagem = f"Erro ao verificar usuário: {email} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def verificar_direito_usuario(idUsuario: int, idQuadro: int) -> PerfilUsuarioQuadro:
    flog = f"{__file__}::verificar_direito_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.validarAcessoUsuario, (idQuadro, idQuadro, idQuadro, idUsuario)) # Precisa repetir idQuadro
        user = cursor.fetchone()

        # Verificar se o usuário foi encontrado
        if user:
            if user[4]: # Quadro público
                membro = True
            else:
                membro = user[3]
            return PerfilUsuarioQuadro(user[0], user[1], user[2], membro)
        else:
            return None
    except Exception as e:
        mensagem = f"Erro ao verificar perfil usuario quadro: {idUsuario} idQuadro: {idQuadro}  : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def ver_perfil_usuario_quadro(idUsuario: int, idQuadro: int) -> bool:
    flog = f"{__file__}::ver_perfil_usuario_quadro;"
    resp = verificar_direito_usuario(idUsuario, idQuadro)
    if resp is None:
        return False
    if resp.eh_administrador or resp.eh_dono_do_quadro or resp.eh_membro_do_quadro:
        return True
    return False

# Os usuários mesmo se auto cadastram
def cadastrar_usuario(usuario: Usuario) -> Optional[int]:
    flog = f"{__file__}::cadastrar_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        # Executar a consulta
        cursor.execute(sql.cadastrarUsuario,(usuario.nome, usuario.dataNascimento.strftime('%Y-%m-%d'), usuario.email, usuario.senha))
        conn.commit()
    except psycopg2.IntegrityError as e:
        # Caso ocorra uma violação de integridade, faz o rollback e trata o erro
        conn.rollback()
        mensagem = f"Erro de integridade ao inserir usuário: {usuario}: {e}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(f"Erro de integridade ao inserir usuário: {usuario}") # A mensagem de retorno é mais simples
    except Exception as e:
        mensagem = f"Erro ao cadastrar o usuario: {usuario.nome} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(f"Erro ao cadastrar o usuario: {usuario.nome}") # Idem
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Atualizar usuário. Somente o próprio pode atualizar seus campos
# O argumento "usuario" deve vir totalmente preenchido. Deve ter havido
# uma consulta anterior
def atualizar_usuario(idUsuario: int, usuario: Usuario):
    flog = f"{__file__}::atualizar_usuario;"
    if idUsuario != usuario.id:
        mensagem = f"Somente o proprio pode atualizar seus dados! Logado: {idUsuario} Atualizado: {usuario.id}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError("Somente o proprio pode atualizar seus dados!")
    usu = obter_usuario(usuario.id)
    if usu is None:
        mensagem = f"Atualizar Usuario inexistente! Id: {usuario.id}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError("Atualizar Usuario inexistente!")
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        # Executar a consulta
        cursor.execute(sql.atualizarUsuario,(usuario.nome, usuario.dataNascimento.strftime('%Y-%m-%d'), usuario.email, usuario.senha, usuario.id))
        conn.commit()

    except Exception as e:
        mensagem = f"Erro ao atualizar o usuario: {usuario.id} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(f"Erro ao atualizar o usuario: {usuario.id} : {e}")
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Deletar usuário. Somente o próprio pode se deletar
def deletar_usuario(idUsuario):
    flog = f"{__file__}::atualizar_usuario;"
    usu = obter_usuario(idUsuario)
    if usu is None:
        mensagem = f"Deletar Usuario inexistente! Id: {idUsuario}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError("Deletar Usuario inexistente!")
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        # Executar a consulta
        cursor.execute(sql.deletarUsuario,(idUsuario,))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao deletar o usuario: {usuario.id} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(mensagem)
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Listar e filtrar usuários: Só um administrador pode fazer isso
def listar_usuarios(idUsuario: int, pesquisa: str) -> List[Usuario]:
    flog = f"{__file__}::listar_usuarios;"
    if not eh_admin(idUsuario):
        mensagem = f"Somente um administrador pode fazer isso! Logado: {idUsuario}"
        logger.error(f"{flog}{mensagem}")
        raise ValueError("Somente um administrador pode fazer isso!")
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.listarFiltrarUsuarios, (f'%{pesquisa}%',))
        user = cursor.fetchall()

        # Verificar se o usuário foi encontrado
        if user:
            return [Usuario(u[0], u[1], u[2], u[3], u[4]) for u in user]
        else:
            return []
    except Exception as e:
        mensagem = f"Erro ao listar/filtrar usuarios: {pesquisa} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def verificar_usuario(idUsuario: int) -> PerfilUsuarioQuadro:
    flog = f"{__file__}::verificar_direito_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.validarAcessoUsuario, (idQuadro, idQuadro, idUsuario))
        user = cursor.fetchone()

        # Verificar se o usuário foi encontrado
        if user:
            return PerfilUsuarioQuadro(user[0], user[1], user[2], user[3])
        else:
            return None
    except Exception as e:
        mensagem = f"Erro ao verificar perfil usuario quadro: {idUsuario} idQuadro: {idQuadro}  : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)
