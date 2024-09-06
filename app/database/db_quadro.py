from typing import List, Optional
from database.db_pool import get_connection, return_connection
from database.modelo import Usuario, Quadro, MembrosQuadro, Mensagem, Administradores

# Retorna um Quadro independentemente do usuário ser membro ou administrador
def obter_quadro(id:int) -> Quadro:
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute("SELECT id, nome, descricao, dono, publico FROM quadro WHERE id = %s", (id,))
        quadro = cursor.fetchone()
        
        # Verificar se o quadro foi encontrado
        if quadro:
            return Quadro(quadro[0], quadro[1], quadro[2], quadro[3], quadro[4])
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter quadro: {id} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)

# Retorna a lista de Quadros considerando o perfil do usuário (membro, dono ou administrador)
# Se o idUsuario não for informado ou for 0, retorna todos os quadros públicos
def obter_quadros_usuario(idUsuario: Optional[int], public:bool) -> List[Quadro]:
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Se o usuário não estiver logado, retornar os quadros públicos
        if idUsuario is None or idUsuario == 0:
            cursor.execute("SELECT id, nome, descricao, dono, publico FROM quadro WHERE publico = %s", (public,))
        else:
            # Executar a consulta considerando o usuário
                        cursor.execute("""
                SELECT q.id, q.nome, q.descricao, q.dono, q.publico 
                FROM quadro q 
                JOIN membros_quadro m ON q.id = m.idQuadro 
                WHERE m.idUsuario = %s
                UNION
                SELECT q.id, q.nome, q.descricao, q.dono, q.publico 
                FROM quadro q 
                WHERE q.publico = TRUE
            """, (idUsuario,))

        quadros = cursor.fetchall()
        
        # Verificar se os quadros foram encontrados
        if quadros:
            return [Quadro(q[0], q[1], q[2], q[3], q[4]) for q in quadros]
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter quadros do usuário: {idUsuario} : {e}")
        return False
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)