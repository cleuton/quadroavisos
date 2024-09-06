import unittest
from database.db_usuario import validar_usuario, obter_usuario

class TestDbUsuario(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()