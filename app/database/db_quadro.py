from typing import List, Optional
from database.db_pool import get_connection, return_connection, sql
from database.modelo import Quadro, QuadroUltimaMensagem, QuadroComDono
from database.db_admins import eh_admin
from database.db_usuario import ver_perfil_usuario_quadro
import logging

logger = logging.getLogger("backend")

# Retorna um Quadro independentemente do usuário ser membro ou administrador
def obter_quadro(id:int, idUsuario: int) -> Quadro:
    flog = f"{__file__}::obter_quadro;"
    if not ver_perfil_usuario_quadro(idUsuario, id):
        mensagem = f"Usuario: {idUsuario} nao tem permissao para acessar esse quadro: {id}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError("Usuario nao tem permissao para acessar esse quadro")
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute(sql.quadroById, (id,))
        quadro = cursor.fetchone()
        
        # Verificar se o quadro foi encontrado
        if quadro:
            return Quadro(quadro[0], quadro[1], quadro[2], quadro[3], quadro[4])
        else:
            return None
    except Exception as e:
        mensagem = f"Erro ao obter quadro: {id} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Retorna a lista de Quadros considerando o perfil do usuário (membro, dono ou administrador)
# Se o idUsuario não for informado ou for 0, retorna todos os quadros públicos
def obter_quadros_usuario(idUsuario: Optional[int]) -> List[QuadroUltimaMensagem]:
    flog = f"{__file__}::obter_quadros_usuario;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Se o usuário não estiver logado, retornar os quadros públicos
        if idUsuario is None or idUsuario == 0:
            return _quadros_usuario_nao_identificado(cursor)

        # Usuário foi informado, vamos ver se é administrador:
        admin = eh_admin(idUsuario)
        # Se o usuário for administrador, retornar todos os quadros:
        if admin:
            return _quadros_admin(cursor)

        # Para os outros casos, executar a consulta considerando o usuário
        return _quadros_por_usuario(cursor, idUsuario)

    except Exception as e:
        mensagem = f"Erro ao obter quadros do usuário: {idUsuario} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def _quadros_usuario_nao_identificado(cursor):
    cursor.execute(sql.quadroPublico)
    quadros = cursor.fetchall()
    if quadros:
        return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
    else:
        return None

def _quadros_admin(cursor):
    cursor.execute(sql.quadroAdmin)
    quadros = cursor.fetchall()
    if quadros:
        return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
    else:
        return None

def _quadros_por_usuario(cursor, idUsuario):
    # Precisa repetir o idUsuario porque tem o parâmetro duas vezes
    cursor.execute(sql.quadroUsuario, (idUsuario, idUsuario))
    quadros = cursor.fetchall()

    # Verificar se os quadros foram encontrados
    if quadros:
        return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
    else:
        return None

# Só administradores podem criar quadros
def criar_quadro(idUsuario: int, quadro: Quadro):
    flog = f"{__file__}::criar_quadro;"
    if not eh_admin(idUsuario):
        mensagem = f"Usuario: {idUsuario} nao eh administrador"
        logger.error(f"{flog} {mensagem}")
        raise ValueError("Usuario sem permissao")
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.criarQuadro, (quadro.nome, quadro.descricao, quadro.dono, quadro.publico))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao criar quadro: {quadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Lista os quadros encontrados, sem última mensagem, baseados no título do quadro e na pesquisa
# Traz o nome do dono do quadro
def listar_filtrar_quadro(pesquisa: str) -> List[QuadroComDono]:
    flog = f"{__file__}::listar_filtrar_quadro;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executa a consulta
        cursor.execute(sql.listarFiltrarQuadros, (f"%{pesquisa}%",))
        quadros = cursor.fetchall()

        # Verificar se os quadros foram encontrados
        if quadros:
            return [QuadroComDono(Quadro(q[0], q[1], q[2], q[3], q[4]), q[5]) for q in quadros]
        else:
            return []
    except Exception as e:
        mensagem = f"Erro ao listar / filtrar quadros: {pesquisa} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

