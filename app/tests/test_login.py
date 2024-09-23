import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from datetime import datetime
import unittest
from unittest.mock import patch
from database.modelo import Usuario
from services.login_service import login

class TestAuth(unittest.TestCase):

    @patch('services.login_service.validar_usuario')
    def test_login(self, mock_validar_usuario):
        # Chama a função `login` que está sendo mockada
        mock_validar_usuario.return_value = Usuario(id=1,nome="Fulano de Tal",dataNascimento=datetime.now().date(),email="fulano@test",
             senha="senha" )
        resultado = login('usuario', 'senha')

        # Verifica se o resultado é o esperado
        self.assertTrue(resultado)
        mock_validar_usuario.assert_called_with('usuario', 'senha')

        # Agora um login retornando falso:
        mock_validar_usuario.return_value = None
        resultado = login('usuario', 'senha')
        self.assertFalse(resultado)

