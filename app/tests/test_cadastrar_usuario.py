import os, sys
from datetime import datetime

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
from database.modelo import Usuario
from services.cadastrar_usuario import cadastrar_novo_usuario

# Regra para senha: Tem que ser auto-gerada e depois o usuário tem que alterar
class TestCadastrarUsuarioOk(unittest.TestCase):

    @patch('services.cadastrar_usuario.cadastrar_usuario')
    def test_cadastrar_usuario(self, mock_cadastrar_usuario):
        mock_cadastrar_usuario.return_value = 10
        usuario = Usuario(0, 'Fulano', datetime.now().date(), 'fulano@teste', 'xpto')
        novoId = cadastrar_novo_usuario(usuario)
        self.assertEqual(novoId, 10)
        mock_cadastrar_usuario.assert_called_with(usuario)

    @patch('services.cadastrar_usuario.cadastrar_usuario')
    def test_cadastrar_usuario_erro(self, mock_cadastrar_usuario):
        mock_cadastrar_usuario.side_effect = ValueError('')
        usuario = Usuario(0, 'Fulano', datetime.now().date(), 'fulano@teste', 'xpto')
        with self.assertRaises(ValueError) as context:
            novoId = cadastrar_novo_usuario(usuario)
        mock_cadastrar_usuario.assert_called_with(usuario)
