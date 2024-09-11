from typing import List
from database.db_pool import get_connection, return_connection, sql
from database.modelo import Mensagem

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