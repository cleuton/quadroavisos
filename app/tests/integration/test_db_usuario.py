import unittest

import sys
import os

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from testcontainers.postgres import PostgresContainer
from database.db_usuario import validar_usuario, obter_usuario, verificar_direito_usuario
from database.db_pool import reset_connection_pool

class TestDbUsuario(unittest.TestCase):

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

    def setUp(self):
        # Configurações iniciais para os testes
        self.email = "alice@example.com"
        self.password = "senha123"
        self.invalid_email = "invalid@example.com"
        self.invalid_password = "invalid123"
        self.user_id = 1

    def tearDown(self):
        pass

    def test_validar_usuario_valid(self):
        # Testar verificação de usuário com credenciais válidas
        result = validar_usuario(self.email, self.password)
        self.assertTrue(result)

    def test_validar_usuario_invalid_email(self):
        # Testar verificação de usuário com email inválido
        result = validar_usuario(self.invalid_email, self.password)
        self.assertFalse(result)

    def test_validar_usuario_invalid_password(self):
        # Testar verificação de usuário com senha inválida
        result = validar_usuario(self.email, self.invalid_password)
        self.assertFalse(result)

    def test_validar_usuario_invalid_credentials(self):
        # Testar verificação de usuário com credenciais inválidas
        result = validar_usuario(self.invalid_email, self.invalid_password)
        self.assertFalse(result)

    def test_obter_usuario_valid(self):
        # Testar obtenção de usuário com ID válido
        user = obter_usuario(self.user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user_id)
        self.assertEqual(user.email, self.email)

    def test_obter_usuario_invalid(self):
        # Testar obtenção de usuário com ID inválido
        user = obter_usuario(9999)  # ID que não existe
        self.assertIsNone(user)

    def test_obter_usuario_exception(self):
        # Testar obtenção de usuário com ID inválido que causa exceção
        user = obter_usuario("invalid_id")  # ID inválido que causa exceção
        self.assertFalse(user)

    def test_perfil_usuario_quadro(self):
        # Usuario administrador
        idUsuarioAdmin = 4
        idQuadro = 3
        resp = verificar_direito_usuario(idUsuarioAdmin, idQuadro)
        self.assertTrue(resp.nome == 'Delmiro Admin')
        self.assertTrue(resp.eh_administrador)
        self.assertFalse(resp.eh_membro_do_quadro)
        self.assertFalse(resp.eh_dono_do_quadro)

        # Usuario dono do quadro
        idUsuario = 1
        idQuadro = 1
        resp = verificar_direito_usuario(idUsuario, idQuadro)
        self.assertTrue(resp.nome == 'Alice Silva')
        self.assertFalse(resp.eh_administrador)
        self.assertFalse(resp.eh_membro_do_quadro)
        self.assertTrue(resp.eh_dono_do_quadro)

        # Usuario nao tem direito algum
        idUsuario = 5
        idQuadro = 3
        resp = verificar_direito_usuario(idUsuario, idQuadro)
        self.assertTrue(resp.nome == 'Enésio não Aprovado')
        self.assertFalse(resp.eh_administrador)
        self.assertFalse(resp.eh_membro_do_quadro)
        self.assertFalse(resp.eh_dono_do_quadro)

        # Usuario inexistente
        idUsuario = 15
        idQuadro = 3
        resp = verificar_direito_usuario(idUsuario, idQuadro)
        self.assertTrue(resp is None)


if __name__ == "__main__":
    unittest.main()