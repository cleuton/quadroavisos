from datetime import datetime
from time import strptime
from typing import List
from database.db_pool import get_connection, return_connection, sql
from database.modelo import Mensagem, MensagemComReacoes, Reacao, ReacaoAutor
from database.db_usuario import ver_perfil_usuario_quadro
import logging

logger = logging.getLogger("backend")

# Obtém mensagem
def obter_mensagem(id: int, idUsuario: int) -> Mensagem:
    flog = f"{__file__}::obter_mensagem;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.mensagem, (id,))
        mensagem = cursor.fetchone()
        if mensagem:
            msg = Mensagem(mensagem[0], mensagem[1], mensagem[2], None, mensagem[3], mensagem[4], mensagem[5], mensagem[6], mensagem[7], mensagem[8])
            if not ver_perfil_usuario_quadro(idUsuario, msg.idQuadro):
                mensagem = "Usuario nao tem permissao para acessar essa mensagem"
                logger.error(f"{flog}{mensagem}")
                raise ValueError(mensagem)
            return msg
        else:
            return None
    except ValueError as v:
        raise
    except Exception as e:
        mensagem = f"Erro ao obter mensagem: {id} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Obtém mensagem com reações
def obter_mensagem_reacoes(id: int, idUsuario: int) -> MensagemComReacoes:
    flog = f"{__file__}::obter_mensagem_reacoes;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.mensagemComReacoes, (id,))
        mcr = cursor.fetchall()
        inicio = True
        mensagemComReacoes = None
        if mcr:
            mensagemComReacoes = MensagemComReacoes(
                Mensagem(
                    mcr[0][0], #id
                    mcr[0][1], #idQuadro
                    mcr[0][2], #idUsuario
                    mcr[0][9], #nomeUsuarioAutor (vem depois dos dados da mensagem na query)
                    mcr[0][3], #dataHora
                    mcr[0][4], #titulo
                    mcr[0][5], #texto
                    mcr[0][6], #anexo
                    mcr[0][7], #expiraEm
                    mcr[0][8]), #icone
                [], #lista de reações
            )
            for reacao in mcr:
                mensagemComReacoes.reacoes.append(ReacaoAutor(Reacao(reacao[10], reacao[11], reacao[12], reacao[13], reacao[14]), reacao[15]))
            if not ver_perfil_usuario_quadro(idUsuario, mensagemComReacoes.mensagem.idQuadro):
                mensagem = "Usuario nao tem permissao para acessar essa mensagem"
                logger.error(f"{flog}{mensagem}")
                raise ValueError(mensagem)
            return mensagemComReacoes
        else:
            return None
    except ValueError as v:
        raise
    except Exception as e:
        mensagem = f"Erro ao obter mensagem com reacoes: {id} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Carrega as mensagens para paginação, trazendo também o nome do autor
def listar_mensagens_desc(quadroId: int, mensagemIdInicial: int, quantidade: int, idUsuario: int) -> List[Mensagem]:
    flog = f"{__file__}::listar_mensagens_desc;"
    if not ver_perfil_usuario_quadro(idUsuario, quadroId):
        mensagem = "Usuario nao tem permissao para acessar essa mensagem"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(sql.mensagensDesc, (quadroId, mensagemIdInicial, quantidade))
        mensagens = cursor.fetchall()
        if mensagens:
            return [Mensagem(m[0], m[1], m[2], m[9], m[3], m[4], m[5], m[6], m[7], m[8]) for m in mensagens]
        else:
            return []
    except Exception as e:
        mensagem = f"Erro ao listar mensagens: {quadroId} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def reagir(idMensagem: int, idUsuario: int, idQuadro: int, tipo: str):
    flog = f"{__file__}::listar_mensagens_desc;"
    if not ver_perfil_usuario_quadro(idUsuario, idQuadro):
        mensagem = "Usuario nao tem permissao para acessar essa mensagem"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        dataHora = datetime.now()
        # Executar a consulta
        cursor.execute(sql.upsertReacaoMensagem, (dataHora, idMensagem, idUsuario, tipo))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao reagir a mensagem: {idMensagem} usuario: {idUsuario} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def cadastrar_mensagem(idUsuario: int, idQuadro: int, msg: Mensagem):
    flog = f"{__file__}::cadastrar_mensagem;"
    if not ver_perfil_usuario_quadro(idUsuario, idQuadro):
        mensagem = "Usuario nao tem permissao para acessar essa mensagem"
        logger.error(f"{flog}{mensagem}")
        raise ValueError(mensagem)
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        dataHora = datetime.now()
        # Executar a consulta
        cursor.execute(sql.cadastrarMensagem,(idQuadro, idUsuario, msg.dataHora.strftime('%Y-%m-%d %H:%M:%S'), msg.titulo, msg.texto, msg.anexo, msg.expiraEm.strftime('%Y-%m-%d %H:%M:%S'), msg.icone))
        conn.commit()
    except Exception as e:
        mensagem = f"Erro ao cadastrar a mensagem: {msg} usuario: {idUsuario} quadro: {idQuadro} : {e}"
        logger.error(f"{flog}{mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

