import psycopg2
from database.db_pool import get_connection, return_connection
from database.modelo import Usuario

def obter_usuario(id:int) -> Usuario:
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute("SELECT id, nome, dataNascimento, email, senha FROM usuario WHERE id = %s", (id,))
        user = cursor.fetchone()
        
        # Verificar se o usuário foi encontrado
        if user:
            return Usuario(user[0], user[1], user[2], user[3], user[4])
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter usuário: {id} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def validar_usuario(email:str, password:str) -> Usuario:
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute("SELECT id, nome, dataNascimento, email, senha FROM usuario WHERE email = %s AND senha = %s", (email, password))
        user = cursor.fetchone()
        
        # Verificar se o usuário foi encontrado
        if user:
            return Usuario(user[0], user[1], user[2], user[3], user[4])
        else:
            return None
    except Exception as e:
        print(f"Erro ao verificar usuário: {email} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

