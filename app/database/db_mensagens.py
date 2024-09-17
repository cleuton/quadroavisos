from typing import List
from database.db_pool import get_connection, return_connection, sql
from database.modelo import Mensagem, MensagemComReacoes, Reacao, ReacaoAutor


# Obtém mensagem
def obter_mensagem(id: int) -> Mensagem:
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
            return Mensagem(mensagem[0], mensagem[1], mensagem[2], None, mensagem[3], mensagem[4], mensagem[5], mensagem[6], mensagem[7], mensagem[8])
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter mensagem: {id} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Obtém mensagem com reações
def obter_mensagem_reacoes(id: int) -> MensagemComReacoes:
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
#id, idQuadro, idUsuario, nomeUsuario, dataHora, titulo, texto, anexo, expiraEm, icone
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
            return mensagemComReacoes
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter mensagem com reacoes: {id} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Carrega as mensagens para paginação, trazendo também o nome do autor
def listar_mensagens_desc(quadroId: int, mensagemIdInicial: int, quantidade: int) -> List[Mensagem]:
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
            return None
    except Exception as e:
        print(f"Erro ao obter mensagens para o quadro: {quadroId} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)