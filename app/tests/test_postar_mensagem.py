import os, sys
from datetime import datetime

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
from database.modelo import Mensagem
from services.postar_mensagem import postar_mensagem

class TestPostarMensagem(unittest.TestCase):

    @patch('services.postar_mensagem.cadastrar_mensagem')
    def test_postar_mensagem_ok(self, mock_cadastrar_mensagem):
        mock_cadastrar_mensagem.return_value = 200
        mensagem = Mensagem(0, 2, 1, '', datetime.now(),
                                         'Mensagem 1', 'Texto 1', None, None, None)
        id = postar_mensagem(1, mensagem)
        self.assertEqual(id, 200)
        mock_cadastrar_mensagem.assert_called_with(1, mensagem)

    @patch('services.postar_mensagem.cadastrar_mensagem')
    def test_postar_mensagem_sem_permissao(self, mock_cadastrar_mensagem):
        mock_cadastrar_mensagem.side_effect = ValueError("")
        mensagem = Mensagem(0, 2, 1, '', datetime.now(),
                                         'Mensagem 1', 'Texto 1', None, None, None)
        with self.assertRaises(ValueError) as context:
            postar_mensagem(1, mensagem)
        mock_cadastrar_mensagem.assert_called_with(1, mensagem)