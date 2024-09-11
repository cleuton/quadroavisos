import unittest
import sys
import os

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
print(f"SYS PATH: ****** {sys.path}")
from testcontainers.postgres import PostgresContainer
from database.db_mensagens import listar_mensagens_desc, obter_mensagem
from database.db_pool import reset_connection_pool
import os

class TestMensagens(unittest.TestCase):
    _postgres = None
    @classmethod
    def setUpClass(cls):
        print(f"******* SetupClass INVOKED ******")
        sql_script_path = os.path.dirname(os.path.abspath(__file__))
        print(sql_script_path)
        cls._postgres = PostgresContainer("postgres:latest").with_volume_mapping(sql_script_path,
                                                                        "/docker-entrypoint-initdb.d")
        cls._postgres.start()
        os.environ["DB_CONN"] = cls._postgres.get_connection_url()
        os.environ["DB_HOST"] = cls._postgres.get_container_host_ip()
        os.environ["DB_PORT"] = cls._postgres.get_exposed_port(5432)
        os.environ["DB_USER"] = cls._postgres.username
        os.environ["DB_PASS"] = cls._postgres.password
        os.environ["DB_DATABASE"] = cls._postgres.dbname
        reset_connection_pool()

    @classmethod
    def tearDownClass(cls):
        cls._postgres.stop()

    def test_listar_mensagens(self):
        # Testar a função listar_mensagens_desc todas
        mensagens = listar_mensagens_desc(3, 6, 4)
        print(f"Mensagens: {mensagens}")
        # Verificar se a função retornou as mensagens corretas
        id = 6
        for m in mensagens:
            print(f"Lida no teste: {m.__dict__}")
            self.assertTrue(m.idQuadro == 3)
            self.assertTrue(m.id == id)
            id -= 1
            self.assertFalse(m.nomeUsuario is None)

    def test_obter_mensagem(self):
        msg = obter_mensagem(6)
        print(f"Mensagem: {msg.__dict__}")
        self.assertTrue(msg.id == 6)
        self.assertTrue(msg.nomeUsuario is None)
        self.assertTrue(msg.idQuadro == 3)
        self.assertTrue(msg.titulo == 'Novo projeto3')
