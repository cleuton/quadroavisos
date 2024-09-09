from typing import List, Optional
from database.db_pool import get_connection, return_connection
from database.modelo import Quadro, QuadroUltimaMensagem
from database.db_admins import eh_admin


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
def obter_quadros_usuario(idUsuario: Optional[int]) -> List[QuadroUltimaMensagem]:
    conn = None
    cursor = None
    try:
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        
        # Se o usuário não estiver logado, retornar os quadros públicos
        if idUsuario is None or idUsuario == 0:
            cursor.execute("""
                       WITH ultima_mensagem AS (
                            SELECT m.*, 
                                ROW_NUMBER() OVER (PARTITION BY m.idQuadro ORDER BY m.dataHora DESC) AS row_num
                                FROM mensagem m
                        )
                       SELECT Q.id, Q.nome, Q.descricao, Q.dono, Q.publico, um.dataHora, um.icone, um.titulo 
                                FROM quadro Q                                 
                                    LEFT JOIN ultima_mensagem um ON Q.id = um.idQuadro AND um.row_num = 1
                       WHERE publico = TRUE
                           """)
            quadros = cursor.fetchall()
            if quadros:
                return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
            else:
                return None

        # Usuário foi informado, vamos ver se é administrador:
        admin = eh_admin(idUsuario)

        if admin: 
            # Se o usuário for administrador, retornar todos os quadros:
            cursor.execute("""
                WITH ultima_mensagem AS (
                        SELECT m.*, 
                            ROW_NUMBER() OVER (PARTITION BY m.idQuadro ORDER BY m.dataHora DESC) AS row_num
                            FROM mensagem m
                    )
                SELECT Q.id, Q.nome, Q.descricao, Q.dono, Q.publico, um.dataHora, um.icone, um.titulo 
                            FROM quadro Q                                 
                                LEFT JOIN ultima_mensagem um ON Q.id = um.idQuadro AND um.row_num = 1
            """)
            quadros = cursor.fetchall()
            if quadros:
                return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
            else:
                return None
        else:
            # Executar a consulta considerando o usuário
            cursor.execute("""
                WITH ultima_mensagem AS (
                    SELECT m.*, 
                        ROW_NUMBER() OVER (PARTITION BY m.idQuadro ORDER BY m.dataHora DESC) AS row_num
                    FROM mensagem m
                )
                SELECT q.id, q.nome, q.descricao, q.dono, q.publico, um.dataHora, um.icone, um.titulo
                FROM quadro q
                JOIN membrosquadro mq ON q.id = mq.idQuadro
                LEFT JOIN ultima_mensagem um ON q.id = um.idQuadro AND um.row_num = 1
                WHERE mq.idUsuario = %s -- Apenas quadros onde o usuário é membro ou dono (donos têm que ser membros também)
                UNION
                SELECT q.id, q.nome, q.descricao, q.dono, q.publico, um.dataHora, um.icone, um.titulo
                FROM quadro q
                LEFT JOIN ultima_mensagem um ON q.id = um.idQuadro AND um.row_num = 1
                WHERE q.publico = TRUE;  -- Inclui também os quadros públicos""", (idUsuario,))

            quadros = cursor.fetchall()

            # Verificar se os quadros foram encontrados
            if quadros:
                return [QuadroUltimaMensagem(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7]) for q in quadros]
            else:
                return None
    except Exception as e:
        print(f"Erro ao obter quadros do usuário: {idUsuario} : {e}")
        return None
    finally:
        # Fechar o cursor e devolver a conexão ao pool
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)