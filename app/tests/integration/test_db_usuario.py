import unittest
from database.db_pool import get_connection, return_connection, sql
import sys
import os
from datetime import datetime

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from testcontainers.postgres import PostgresContainer
from database.db_usuario import validar_usuario, obter_usuario, verificar_direito_usuario, cadastrar_usuario, \
    atualizar_usuario, deletar_usuario, listar_usuarios
from database.db_pool import reset_connection_pool
from database.modelo import Usuario

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
        print(f">>>>>>>>>>>>>>>>>>>>>> Port: {cls._postgres.get_exposed_port(5432)} <<<<<<<<<<<<<<<<<<<<<<<")

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
        idUsuario = 1
        email = 'alice@example.com'
        user = obter_usuario(idUsuario)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, idUsuario)
        self.assertEqual(user.email, email)
        self.assertFalse(user.ehAdmin)

        # Testar usuario admin:
        idUsuario = 1
        email = 'alice@example.com'
        user = obter_usuario(idUsuario)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, idUsuario)
        self.assertEqual(user.email, email)
        self.assertTrue(user.ehAdmin)

        # Testar usuario inexistente:
        idUsuario = 0
        user = obter_usuario(idUsuario)
        self.assertIsNone(user)

    def test_obter_usuario_invalid(self):
        # Testar obtenção de usuário com ID inválido
        user = obter_usuario(9999)  # ID que não existe
        self.assertIsNone(user)

    def test_obter_usuario_exception(self):
        # Testar obtenção de usuário com ID inválido que causa exceção
        with self.assertRaises(Exception) as context:
            user = obter_usuario("invalid_id")  # ID inválido que causa exceção

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

    def test_cadastrar_atualizar_deletar_usuario(self):
        # Obter uma conexão do pool
        conn = get_connection()
        cursor = conn.cursor()
        # Obter o valor do próximo idUsuario:
        cursor.execute("SELECT MAX(id) FROM usuario;")
        resultado = cursor.fetchone()
        if not resultado[0]:
            maxId = 0
        else:
            maxId = resultado[0]
        # Criar um novo usuario
        idUsuario =  maxId + 1
        usuario = Usuario(0, 'fulano de tal', datetime.strptime('1970-04-10', '%Y-%m-%d').date(),
                          'fulano@teste.com', 'senha123')
        id = cadastrar_usuario(usuario)
        usuario_db = obter_usuario(idUsuario)
        self.assertFalse(usuario_db is None)
        self.assertEqual(usuario_db.nome, usuario.nome)
        self.assertEqual(usuario_db.email, usuario.email)
        self.assertEqual(usuario_db.senha, usuario.senha)
        self.assertEqual(usuario_db.dataNascimento, usuario.dataNascimento)

        # Cadastrar usuário já existente
        usuario = Usuario(0, 'fulano de tal', datetime.strptime('1970-04-10', '%Y-%m-%d').date(),
                          'fulano@teste.com', 'sdfdfdfdfdenha123')
        with self.assertRaises(ValueError) as context:
            cadastrar_usuario(usuario)
        self.assertEqual(str(context.exception), f"Erro de integridade ao inserir usuário: {usuario}")

        # Atualizar um usuario
        usuario.id = idUsuario
        usuario.nome = 'Novo nome'
        usuario.email = 'novo@email'
        usuario.senha = '<PASSWORD>'
        usuario.dataNascimento = datetime.strptime('1971-05-14', '%Y-%m-%d').date()
        atualizar_usuario(idUsuario, usuario)
        usuario_db = obter_usuario(idUsuario)
        self.assertFalse(usuario_db is None)
        self.assertEqual(usuario_db.nome, usuario.nome)
        self.assertEqual(usuario_db.email, usuario.email)
        self.assertEqual(usuario_db.dataNascimento, usuario.dataNascimento)

        # Atualizar usuario inexistente:
        usuario = Usuario(0, 'fulano de tal', datetime.strptime('1970-04-10', '%Y-%m-%d').date(),
                          'fulano@teste.com', 'sdfdfdfdfdenha123')
        with self.assertRaises(ValueError) as context:
            atualizar_usuario(0,usuario)
        self.assertEqual(str(context.exception), "Atualizar Usuario inexistente!")

        # Deletar um usuario
        deletar_usuario(idUsuario)
        usuario_db = obter_usuario(idUsuario)
        self.assertTrue(usuario_db is None)

        # Deletar um usuario inexistente
        with self.assertRaises(ValueError) as context:
            deletar_usuario(0)
        self.assertEqual(str(context.exception), "Deletar Usuario inexistente!")

    def test_listar_filtrar_usuarios(self):
        # Listagem bem sucedida
        idUsuario = 4 # Admin! Depende do script create.sql dos testes!!!!!
        pesquisa = 'os' # Deve listar 2: Bob Santos e Carlos Pereira
        usuarios = listar_usuarios(idUsuario, pesquisa)
        self.assertTrue(len(usuarios) == 2)
        self.assertEqual(usuarios[0].nome, 'Bob Santos')
        self.assertEqual(usuarios[1].nome, 'Carlos Pereira')

if __name__ == "__main__":
    unittest.main()