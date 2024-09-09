import psycopg2
from psycopg2 import pool
import os

# Cria o pool de conexões globalmente com parâmetros adequados

connection_pool = None

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
