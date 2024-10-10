from typing import List, Optional
from database.db_pool import get_connection, return_connection, sql
from database.modelo import Quadro, QuadroUltimaMensagem, QuadroComDono, PerfilUsuarioQuadro, MembrosQuadro
from database.db_admins import eh_admin
from database.db_usuario import ver_perfil_usuario_quadro, verificar_direito_usuario
import logging

logger = logging.getLogger("backend")

# Retorna um Quadro com a quantidade de mensagens nele
def obter_quadro(id:int, idUsuario: int) -> Quadro:
    flog = f"{__file__}::obter_quadro;"

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
            if (not quadro[4]) and (quadro[3] != idUsuario): # Se o quadro não for público
                if not ver_perfil_usuario_quadro(idUsuario, id):
                    mensagem = f"Usuario: {idUsuario} nao tem permissao para acessar esse quadro: {id}"
                    logger.error(f"{flog} {mensagem}")
                    raise ValueError("Usuario nao tem permissao para acessar esse quadro")

            return Quadro(quadro[0], quadro[1], quadro[2], quadro[3], quadro[4], quadro[5])
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
def criar_quadro(idUsuario: int, quadro: Quadro) -> Optional[int]:
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
        idQuadro = cursor.fetchone()[0]
        conn.commit()
        return idQuadro
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

# Só administradores podem alterar quadros
def alterar_quadro(idUsuario: int, quadro: Quadro):
    flog = f"{__file__}::alterar_quadro;"
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
        cursor.execute(sql.atualizarQuadro, (quadro.nome, quadro.descricao, quadro.id))
        registros_afetados = cursor.rowcount
        if registros_afetados != 1:
            mensagem = f"Tentativa de alterar o quadro {quadro.nome} com erro"
            logger.error(f"{flog} {mensagem}")
            raise ValueError(mensagem)
        conn.commit()
        return
    except Exception as e:
        mensagem = f"Erro ao alterar quadro: {quadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Só administradores podem deletar quadros
def deletar_quadro(idUsuario: int, idQuadro: int):
    flog = f"{__file__}::deletar_quadro;"
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

        # Executar a consultaS
        cursor.execute(sql.deletarQuadro, (idQuadro,))
        registros_afetados = cursor.rowcount
        if registros_afetados != 1:
            mensagem = f"Tentativa de deletar o quadro {idQuadro} com erro"
            logger.error(f"{flog} {mensagem}")
            raise ValueError(mensagem)
        mensagem = f"Usuário com id: {idUsuario} deletou o quadro com id: {idQuadro}"
        logger.warn(f"{flog} {mensagem}")
        conn.commit()
        return
    except Exception as e:
        mensagem = f"Erro ao deletar quadro: {idQuadro} : {e}"
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

# Um usuário pode solicitar para ser membro de um quadro, mas deve ser aprovado pelo dono posteriormente
def solicitar_membro_quadro(idUsuario: int, idQuadro: int):
    flog = f"{__file__}::solicitar_membro_quadro;"
    perfil = ver_perfil_usuario_quadro(idUsuario, idQuadro)
    if perfil is None:
        mensagem = f"Usuario: {idUsuario} não encontrado pedindo acesso ao quadro: {idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    if perfil:
        mensagem = f"Usuario: {idUsuario} já é administrador, dono ou membro do quadro: {idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.inserirMembroQuadro, (idQuadro, idUsuario,))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao tornar o usuario: {idUsuario} membro do quadro: {idQuadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Somente o dono de um quadro pode remover usuários de serem membros dele
def remover_membro_quadro(idUsuario: int, membrosQuadro: MembrosQuadro):
    flog = f"{__file__}::remover_membro_quadro;"
    perfil = verificar_direito_usuario(idUsuario, membrosQuadro.idQuadro)
    if perfil is None:
        mensagem = f"Usuario: {idUsuario} dono do quadro não encontrado para remover um usuário do quadro: {membrosQuadro.idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    if not perfil.eh_dono_do_quadro:
        mensagem = f"Usuario: {idUsuario} não é dono do quadro {membrosQuadro.idQuadro} e pede a remoção do usuário: {membrosQuadro.idUsuario}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.removerMembroQuadro, (membrosQuadro.idQuadro, membrosQuadro.idUsuario,))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao remover o usuario: {membrosQuadro.idUsuario} de membro do quadro: {membrosQuadro.idQuadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# O dono do quadro ou um administrador podem solicitar a lista de membros de um quadro
def listar_membros_quadro(idUsuario, idQuadro) -> List[MembrosQuadro]:
    flog = f"{__file__}::listar_membros_quadro;"
    perfil = verificar_direito_usuario(idUsuario, idQuadro)
    if perfil is None:
        mensagem = f"Usuario: {idUsuario} não encontrado para listar membros do quadro: {idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    if (not perfil.eh_administrador) and not (perfil.eh_dono_do_quadro):
        mensagem = f"Usuario: {idUsuario} não é dono do quadro {idQuadro} e nem administrador e pede a listagem dos membros do quadro: {idUsuario}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.listarMembrosQuadro, (idQuadro,))
        membros = cursor.fetchall()
        if membros:
            return [MembrosQuadro(m[0], m[1], m[2], m[3], m[4]) for m in membros]
        else:
            return []
    except Exception as e:
        mensagem = f"Erro ao listar membros do quadro: {idQuadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Somente o dono de um quadro pode aprovar usuários a serem membros dele
def aprovar_membro_quadro(idUsuario: int, membrosQuadro: MembrosQuadro):
    flog = f"{__file__}::aprovar_membro_quadro;"
    perfil = verificar_direito_usuario(idUsuario, membrosQuadro.idQuadro)
    if perfil is None:
        mensagem = f"Usuario: {idUsuario} dono do quadro não encontrado para aprovar um usuário membro do quadro: {membrosQuadro.idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    if not perfil.eh_dono_do_quadro:
        mensagem = f"Usuario: {idUsuario} não é dono do quadro {membrosQuadro.idQuadro} para aprovar o usuário: {membrosQuadro.idUsuario} como membro do quadro"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)
    if membrosQuadro.aprovado:
        mensagem = f"Usuario: {idUsuario} já é membro aprovado do quadro: {membrosQuadro.idQuadro}"
        logger.error(f"{flog} {mensagem}")
        raise ValueError(mensagem)

    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.aprovarMembroQuadro, (membrosQuadro.idQuadro, membrosQuadro.idUsuario,))
        afetados = cursor.rowcount
        if afetados != 1:
            mensagem = f"Usuario: {membrosQuadro.idUsuario} não consta como tendo solicitado acesso ao quadro: {membrosQuadro.idQuadro}"
            logger.error(f"{flog} {mensagem}")
            raise ValueError(mensagem)
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao aprovar o usuario: {membrosQuadro.idUsuario} como membro do quadro: {membrosQuadro.idQuadro} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)
