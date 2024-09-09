import unittest
import sys
import os

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
print(f"SYS PATH: ****** {sys.path}")
from testcontainers.postgres import PostgresContainer
from database.db_quadro import obter_quadros_usuario
from database.db_pool import reset_connection_pool
import os

class TestDbQuadro(unittest.TestCase):
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

    def test_obter_quadros_usuario_nao_logado(self):
        # Testar a função obter_quadros_usuario quando o usuário não é admin
        quadros = obter_quadros_usuario(None)

        # Verificar se a função retornou os quadros corretos
        self.assertIsNotNone(quadros)
        self.assertEqual(len(quadros), 1)
        self.assertFalse(any(not quadro.publico for quadro in quadros))
        quadro = quadros[0]
        self.assertTrue(quadro.id == 1)
        self.assertTrue(quadro.descricao == 'Quadro para anúncios gerais')
        self.assertFalse(quadro.titulo is None)
        self.assertTrue(quadro.titulo == 'Novo evento')

    def test_obter_quadros_usuario_nao_admin(self):
        # Testar a função obter_quadros_usuario quando o usuário não é admin
        quadros = obter_quadros_usuario(1)

        # Verificar se a função retornou os quadros corretos
        self.assertIsNotNone(quadros)
        self.assertEqual(len(quadros), 3)
        quadro_privado1 = [quadro for quadro in quadros if quadro.id == 4][0] # dona
        quadro_privado2 = [quadro for quadro in quadros if quadro.id == 2][0]  # membro
        quadro_publico = [quadro for quadro in quadros if quadro.publico == True][0]

        self.assertTrue(quadro_publico.id == 1)
        self.assertTrue(quadro_publico.descricao == 'Quadro para anúncios gerais')
        self.assertFalse(quadro_publico.titulo is None)
        self.assertTrue(quadro_publico.titulo == 'Novo evento')
        self.assertTrue(quadro_privado1.id == 4)
        self.assertTrue(quadro_privado1.descricao == 'Quadro para discussão de projetos da Alice')
        self.assertFalse(quadro_privado1.titulo is None)
        self.assertTrue(quadro_privado1.titulo == 'Vamos começar o projeto novo')
        self.assertTrue(quadro_privado2.id == 2)
        self.assertTrue(quadro_privado2.descricao == 'Quadro para discussão de projetos')
        self.assertFalse(quadro_privado2.titulo is None)
        self.assertTrue(quadro_privado2.titulo == 'Novo projeto')



if __name__ == "__main__":
    unittest.main()