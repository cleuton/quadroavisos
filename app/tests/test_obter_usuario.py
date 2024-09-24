import os, sys
from datetime import datetime

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
from database.modelo import Usuario, QuadroUltimaMensagem, Mensagem
from services.obter_usuario import obter_dados_usuario, obter_usuario_com_quadros

class TestObterUsuario(unittest.TestCase):

    @patch('services.obter_usuario.obter_usuario')
    def test_obter_usuario_ok(self, mock_obter_usuario):
        mock_obter_usuario.return_value = Usuario(id=1, nome='Fulano', email='fulano@teste', dataNascimento=datetime.now().date(),
                               senha="************", ehAdmin=False)
        usuario = obter_dados_usuario(1,1)
        self.assertEqual(usuario.nome, 'Fulano')
        self.assertEqual(usuario.senha, '************')
        self.assertEqual(usuario.ehAdmin, False)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nome, 'Fulano')
        self.assertEqual(usuario.email, 'fulano@teste')

    @patch('services.obter_usuario.obter_usuario')
    def test_obter_usuario_admin_ok(self, mock_obter_usuario):
        def selecionar_usuario(idUsuario):
            if idUsuario == 1:
                return Usuario(id=1, nome='Fulano', email='fulano@teste', dataNascimento=datetime.now().date(),
                               senha="************", ehAdmin=False)
            if idUsuario == 4:
                return Usuario(id=4, nome='Beltrano', email='beltrano@teste', dataNascimento=datetime.now().date(),
                               senha="************", ehAdmin=True)
        mock_obter_usuario.side_effect = selecionar_usuario
        usuario = obter_dados_usuario(4,1)
        self.assertEqual(usuario.nome, 'Fulano')
        self.assertEqual(usuario.senha, '************')
        self.assertEqual(usuario.ehAdmin, False)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nome, 'Fulano')
        self.assertEqual(usuario.email, 'fulano@teste')

    @patch('services.obter_usuario.obter_usuario')
    def test_obter_usuario_nao_admin_erro(self, mock_obter_usuario):
        def selecionar_usuario(idUsuario):
            if idUsuario == 1:
                return Usuario(id=1, nome='Fulano', email='fulano@teste', dataNascimento=datetime.now().date(),
                               senha="************", ehAdmin=False)
            if idUsuario == 4:
                return Usuario(id=4, nome='Beltrano', email='beltrano@teste', dataNascimento=datetime.now().date(),
                               senha="************", ehAdmin=False)
        mock_obter_usuario.side_effect = selecionar_usuario
        with self.assertRaises(ValueError):
            usuario = obter_dados_usuario(4, 1)

