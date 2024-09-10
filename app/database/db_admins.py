from database.db_pool import get_connection, return_connection
from database.modelo import Administradores

# Retorna se um usuário é Administrador
def eh_admin(id:int) -> bool:
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
        print(f"Erro ao obter admin para: {id} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

