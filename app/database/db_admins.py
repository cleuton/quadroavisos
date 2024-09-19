from database.db_pool import get_connection, return_connection
from database.modelo import Administradores
import logging

logger = logging.getLogger("backend")

# Retorna se um usuário é Administrador
def eh_admin(id:int) -> bool:
    flog = f"{__file__}::eh_admin;"
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute("SELECT * FROM administradores WHERE idUsuario = %s", (id,))
        admin = cursor.fetchone()
        
        # Verificar se o usuário existe em administradores
        if admin:
            return True
        else:
            return False
    except Exception as e:
        mensagem = f"Erro ao obter admin para: {id} : {e}"
        logger.error(f"{flog} {mensagem}")
        raise
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

