import os, sys
from datetime import datetime

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
from database.modelo import Quadro, Mensagem
from services.acessar_quadro_com_mensagens import paginar_mensagens_quadro

class TestObterQuadrosUsuario(unittest.TestCase):

    @patch('services.acessar_quadro_com_mensagens.obter_quadro')
    @patch('services.acessar_quadro_com_mensagens.listar_mensagens_desc')
    def test_paginar_mensagens_quadro(self, mock_listar_mensagens_desc,mock_obter_quadro):
        mock_obter_quadro.return_value = Quadro(1, 'Quadro 1', 'Descrição quadro 1', 3, False, 20)
        mensagens = []
        for i in range(5):
            idMensagem = i+1
            mensagens.append(
                Mensagem(idMensagem, 1, i+1, 'Bob Santos', datetime.now(), f"Titulo msg {idMensagem}", f"Texto mensagem {idMensagem}", None, None, None)
            )
        mock_listar_mensagens_desc.return_value = mensagens
        # Temos 55 mensagens
        quadro = paginar_mensagens_quadro(1,1, 1, 5)
        self.assertFalse(quadro is None)
        #quadroId: int, mensagemInicial: int, quantidade: int, idUsuario: int) -> List[Mensagem]:
        mock_listar_mensagens_desc.assert_called_with(1, 0, 5, 1)

    @patch('services.acessar_quadro_com_mensagens.obter_quadro')
    @patch('services.acessar_quadro_com_mensagens.listar_mensagens_desc')
    def test_paginar_mensagens_quadro_pagina_meio(self, mock_listar_mensagens_desc, mock_obter_quadro):
        mock_obter_quadro.return_value = Quadro(1, 'Quadro 1', 'Descrição quadro 1', 3, False, 55)
        mensagens = []
        for i in range(5):
            idMensagem = i + 1
            mensagens.append(
                Mensagem(idMensagem, 1, i + 1, 'Bob Santos', datetime.now(), f"Titulo msg {idMensagem}",
                         f"Texto mensagem {idMensagem}", None, None, None)
            )
        mock_listar_mensagens_desc.return_value = mensagens
        # Vamos supor que temos 55 mensagens
        quadro = paginar_mensagens_quadro(1, 1, 8, 5)
        self.assertFalse(quadro is None)
        mock_listar_mensagens_desc.assert_called_with(1, 35, 5, 1)

    @patch('services.acessar_quadro_com_mensagens.obter_quadro')
    @patch('services.acessar_quadro_com_mensagens.listar_mensagens_desc')
    def test_paginar_mensagens_quadro_pagina_depois_fim(self, mock_listar_mensagens_desc, mock_obter_quadro):
        mock_obter_quadro.return_value = Quadro(1, 'Quadro 1', 'Descrição quadro 1', 3, False, 55)
        mensagens = []
        for i in range(5):
            idMensagem = i + 1
            mensagens.append(
                Mensagem(idMensagem, 1, i + 1, 'Bob Santos', datetime.now(), f"Titulo msg {idMensagem}",
                         f"Texto mensagem {idMensagem}", None, None, None)
            )
        mock_listar_mensagens_desc.return_value = mensagens
        # Vamos supor que temos 55 mensagens
        quadro = paginar_mensagens_quadro(1, 1, 20, 5)
        self.assertTrue(len(quadro) == 0)
        self.assertFalse(mock_listar_mensagens_desc.called)