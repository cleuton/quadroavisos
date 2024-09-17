import unittest
import sys
import os

# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
print(f"SYS PATH: ****** {sys.path}")
from testcontainers.postgres import PostgresContainer
from database.db_mensagens import listar_mensagens_desc, obter_mensagem, obter_mensagem_reacoes, reagir
from database.db_pool import reset_connection_pool
from database.modelo import Reacao, ReacaoAutor
import os

class TestMensagens(unittest.TestCase):
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

    def test_listar_mensagens(self):
        # Testar a função listar_mensagens_desc todas usuario membro do quadro
        mensagens = listar_mensagens_desc(3, 6, 4, 3)
        print(f"Mensagens: {mensagens}")
        # Verificar se a função retornou as mensagens corretas
        id = 6
        for m in mensagens:
            print(f"Lida no teste: {m.__dict__}")
            self.assertTrue(m.idQuadro == 3)
            self.assertTrue(m.id == id)
            id -= 1
            self.assertFalse(m.nomeUsuario is None)

        # Testar a função listar_mensagens_desc todas usuario administrador
        mensagens = listar_mensagens_desc(3, 6, 4, 4)
        print(f"Mensagens: {mensagens}")
        # Verificar se a função retornou as mensagens corretas
        id = 6
        for m in mensagens:
            print(f"Lida no teste: {m.__dict__}")
            self.assertTrue(m.idQuadro == 3)
            self.assertTrue(m.id == id)
            id -= 1
            self.assertFalse(m.nomeUsuario is None)

        # Testar a função listar_mensagens_desc todas usuario nao eh membro nem dono do quadro
        with self.assertRaises(ValueError) as context:
            mensagens = listar_mensagens_desc(3, 6, 4, 5)
        self.assertEqual(str(context.exception), "Usuario nao tem permissao para acessar essa mensagem")

        self.assertRaises(ValueError)

    def test_obter_mensagem(self):
        # Obtem mensagem com usuario sendo membro do quadro
        msg = obter_mensagem(6, 3)
        print(f"Mensagem: {msg.__dict__}")
        self.assertTrue(msg.id == 6)
        self.assertTrue(msg.nomeUsuario is None)
        self.assertTrue(msg.idQuadro == 3)
        self.assertTrue(msg.titulo == 'Novo projeto3')

        # Obtem mensagem com usuario sendo administrador
        msg = obter_mensagem(6, 4)
        print(f"Mensagem: {msg.__dict__}")
        self.assertTrue(msg.id == 6)
        self.assertTrue(msg.nomeUsuario is None)
        self.assertTrue(msg.idQuadro == 3)
        self.assertTrue(msg.titulo == 'Novo projeto3')

        # Obtem mensagem com usuario nao tendo direito de ver a mensagem
        with self.assertRaises(ValueError) as context:
            msg = obter_mensagem(6, 5)
        self.assertEqual(str(context.exception), "Usuario nao tem permissao para acessar essa mensagem")

    def test_obter_mensagem_com_reacoes(self):
        # Usuario tem direito ao quadro
        msg = obter_mensagem_reacoes(6, 3)
        id_autor = 2
        nome_autor = "Bob Santos"
        reacoes = [
            ReacaoAutor(Reacao(5, '2023-01-04 12:10:00', 6, 1, 'curtir.png'), 'Alice Silva'),
            ReacaoAutor(Reacao(4,'2023-01-03 12:05:00', 6, 3, 'curioso.png'),'Carlos Pereira'),
        ]
        self.assertTrue(msg.mensagem.id == 6)
        self.assertTrue(msg.mensagem.idUsuario == id_autor)
        self.assertTrue(msg.mensagem.nomeUsuario == nome_autor)
        self.assertTrue(msg.mensagem.idQuadro == 3)
        self.assertTrue(msg.mensagem.titulo == 'Novo projeto3')
        self.assertTrue(len(msg.reacoes) == 2)
        self.assertTrue(msg.reacoes[0].nomeAutor == reacoes[0].nomeAutor)
        self.assertTrue(msg.reacoes[0].reacao.id == reacoes[0].reacao.id)
        self.assertTrue(msg.reacoes[0].reacao.dataHora == reacoes[0].reacao.dataHora)
        self.assertTrue(msg.reacoes[0].reacao.idMensagem == reacoes[0].reacao.idMensagem)
        self.assertTrue(msg.reacoes[0].reacao.idUsuario == reacoes[0].reacao.idUsuario)
        self.assertTrue(msg.reacoes[0].reacao.tipo == reacoes[0].reacao.tipo)
        self.assertTrue(msg.reacoes[1].nomeAutor == reacoes[1].nomeAutor)
        self.assertTrue(msg.reacoes[1].reacao.id == reacoes[1].reacao.id)
        self.assertTrue(msg.reacoes[1].reacao.dataHora == reacoes[1].reacao.dataHora)
        self.assertTrue(msg.reacoes[1].reacao.idMensagem == reacoes[1].reacao.idMensagem)
        self.assertTrue(msg.reacoes[1].reacao.idUsuario == reacoes[1].reacao.idUsuario)
        self.assertTrue(msg.reacoes[1].reacao.tipo == reacoes[1].reacao.tipo)

        # Usuario eh administrador
        msg = obter_mensagem_reacoes(6, 4)
        id_autor = 2
        nome_autor = "Bob Santos"
        reacoes = [
            ReacaoAutor(Reacao(5, '2023-01-04 12:10:00', 6, 1, 'curtir.png'), 'Alice Silva'),
            ReacaoAutor(Reacao(4,'2023-01-03 12:05:00', 6, 3, 'curioso.png'),'Carlos Pereira'),
        ]
        self.assertTrue(msg.mensagem.id == 6)
        self.assertTrue(msg.mensagem.idUsuario == id_autor)
        self.assertTrue(msg.mensagem.nomeUsuario == nome_autor)
        self.assertTrue(msg.mensagem.idQuadro == 3)
        self.assertTrue(msg.mensagem.titulo == 'Novo projeto3')
        self.assertTrue(len(msg.reacoes) == 2)
        self.assertTrue(msg.reacoes[0].nomeAutor == reacoes[0].nomeAutor)
        self.assertTrue(msg.reacoes[0].reacao.id == reacoes[0].reacao.id)
        self.assertTrue(msg.reacoes[0].reacao.dataHora == reacoes[0].reacao.dataHora)
        self.assertTrue(msg.reacoes[0].reacao.idMensagem == reacoes[0].reacao.idMensagem)
        self.assertTrue(msg.reacoes[0].reacao.idUsuario == reacoes[0].reacao.idUsuario)
        self.assertTrue(msg.reacoes[0].reacao.tipo == reacoes[0].reacao.tipo)
        self.assertTrue(msg.reacoes[1].nomeAutor == reacoes[1].nomeAutor)
        self.assertTrue(msg.reacoes[1].reacao.id == reacoes[1].reacao.id)
        self.assertTrue(msg.reacoes[1].reacao.dataHora == reacoes[1].reacao.dataHora)
        self.assertTrue(msg.reacoes[1].reacao.idMensagem == reacoes[1].reacao.idMensagem)
        self.assertTrue(msg.reacoes[1].reacao.idUsuario == reacoes[1].reacao.idUsuario)
        self.assertTrue(msg.reacoes[1].reacao.tipo == reacoes[1].reacao.tipo)

        # Usuario nao tem direito ao quadro
        with self.assertRaises(ValueError) as context:
            msg = obter_mensagem_reacoes(6, 5)
        self.assertEqual(str(context.exception), "Usuario nao tem permissao para acessar essa mensagem")


    def reagir_mensagem(self):
        # Nao existe reacao deste usuario a esta mensagem:
        id_mensagem = 4
        id_usuario = 2
        id_quadro = 3
        reagir(id_mensagem, id_usuario, id_quadro, 'curtir.png')
        msgr = obter_mensagem_reacoes(id_mensagem, id_usuario)
        self.assertTrue(len(msgr.reacoes) == 1)
        self.assertTrue(msgr.reacoes[0].reacao.tipo == 'curtir.png')
        self.assertTrue(msgr.reacoes[0].nomeAutor == 'Bob Santos')

        # existe reacao deste usuario a esta mensagem, vamos mudar:
        id_mensagem = 4
        id_usuario = 2
        id_quadro = 3
        reagir(id_mensagem, id_usuario, id_quadro, 'curious.png')
        msgr = obter_mensagem_reacoes(id_mensagem, id_usuario)
        self.assertTrue(len(msgr.reacoes) == 1)
        self.assertTrue(msgr.reacoes[0].reacao.tipo == 'curious.png')
        self.assertTrue(msgr.reacoes[0].nomeAutor == 'Bob Santos')

        # tentar reagir a uma mensagem sem ter direito a ela:
        id_mensagem = 4
        id_usuario = 5
        id_quadro = 3
        with self.assertRaises(ValueError) as context:
            reagir(id_mensagem, id_usuario, id_quadro, 'curious.png')
        self.assertEqual(str(context.exception), "Usuario nao tem permissao para acessar essa mensagem")



