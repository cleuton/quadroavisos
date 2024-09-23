import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
from database.modelo import Quadro, QuadroUltimaMensagem
from services.obter_quadros_usuario import obter_quadros

class TestObterQuadrosUsuario(unittest.TestCase):

    @patch('services.obter_quadros_usuario.obter_quadros_usuario')
    def test_obter_quadros_usuario_anonimo(self, mock_obter_quadros_usuario):
        #def __init__(self, id: int, nome: str, descricao: str, dono: int, publico: bool , dataHora: datetime, icone: str, titulo: str):
        mock_obter_quadros_usuario.return_value = [
            QuadroUltimaMensagem(
                id = 1,
                nome = "Quadro 1",
                descricao = "descricao Quadro 1",
                dono = 1,
                publico = True,
                dataHora = "2021-01-01 00:00:00",
                icone = "icone Quadro 1",
                titulo = "titulo Quadro 1"
            )
        ]
        resultados = obter_quadros(1)
        self.assertEqual(1, len(resultados))
        self.assertEqual(1, resultados[0].id)
        self.assertEqual("Quadro 1", resultados[0].nome)
        mock_obter_quadros_usuario.assert_called_with(1)
        mock_obter_quadros_usuario.return_value = [
            QuadroUltimaMensagem(
                id = 2,
                nome = "Quadro 2",
                descricao = "descricao Quadro 2",
                dono = 1,
                publico = True,
                dataHora = "2021-01-01 00:00:00",
                icone = "icone Quadro 2",
                titulo = "titulo Quadro 2"
            )
        ]
        resultados = obter_quadros(None)
        self.assertEqual(1, len(resultados))
        self.assertEqual(2, resultados[0].id)
        self.assertEqual("Quadro 2", resultados[0].nome)
        mock_obter_quadros_usuario.assert_called_with(None)


