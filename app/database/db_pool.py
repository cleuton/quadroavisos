import psycopg2
from psycopg2 import pool
import os
import toml

# Cria o pool de conexões globalmente com parâmetros adequados

connection_pool = None

# Criar a classe que vai armazenar as propriedades
class SqlConfig:
    def __init__(self):
        pass

    def carregar_propriedades(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = toml.load(f)

            if "query" in dados:
                for chave, valor in dados["query"].items():
                    setattr(self, chave, valor)

    def imprimir_dicionario(self):
        print(self.__dict__)

# Carregando propriedades:
sql = SqlConfig()
sql.carregar_propriedades(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql.toml'))
sql.imprimir_dicionario()

def cria_connection_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,  # Número mínimo de conexões no pool
            maxconn=20,  # Número máximo de conexões no pool
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASS', 'password'),
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432'),
            database=os.environ.get('DB_DATABASE', 'backend_db')
        )
        print(f"""**** user {os.environ.get('DB_USER', 'postgres')} password {os.environ.get('DB_PASS', 'password')} host {os.environ.get('DB_HOST', 'localhost')} 
            port {os.environ.get('DB_PORT', '5432')} 
            database {os.environ.get('DB_DATABASE', 'backend_db')}
        """)

# Função para pegar uma conexão do pool
def get_connection():
    global connection_pool
    cria_connection_pool()
    return connection_pool.getconn()

# Função para devolver uma conexão ao pool
def return_connection(conn):
    global connection_pool
    cria_connection_pool()
    connection_pool.putconn(conn)

# Fechar todas as conexões no pool
def close_all_connections():
    global connection_pool
    cria_connection_pool()
    connection_pool.closeall()

def reset_connection_pool():
    global connection_pool
    connection_pool = None
