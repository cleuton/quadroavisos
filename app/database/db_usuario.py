from database.db_pool import get_connection, return_connection, sql
from database.modelo import Usuario, PerfilUsuarioQuadro


def obter_usuario(id:int) -> Usuario:
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
            return Usuario(user[0], user[1], user[2], user[3], user[4])
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter usuário: {id} : {e}")
        return None
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
        cursor.execute(sql.usuarioByEmailSenha, (email, password))
        user = cursor.fetchone()
        
        # Verificar se o usuário foi encontrado
        if user:
            return Usuario(user[0], user[1], user[2], user[3], user[4])
        else:
            return None
    except Exception as e:
        print(f"Erro ao verificar usuário: {email} : {e}")
        return None
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def verificar_direito_usuario(idUsuario: int, idQuadro: int) -> PerfilUsuarioQuadro:
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
        print(f"Erro ao verificar perfil usuario quadro. IdUsuario: {idUsuario} idQuadro: {idQuadro}  : {e}")
        return None
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

def ver_perfil_usuario_quadro(idUsuario: int, idQuadro: int) -> bool:
    resp = verificar_direito_usuario(idUsuario, idQuadro)
    if resp is None:
        return False
    if resp.eh_administrador or resp.eh_dono_do_quadro or resp.eh_membro_do_quadro:
        return True
    return False


