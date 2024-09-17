from datetime import datetime
from datetime import date


class Usuario:
    def __init__(self, id: int, nome: str, dataNascimento: date, email: str, senha: str):
        self.id = id
        self.nome = nome
        if type(dataNascimento) != date:
            self.dataNascimento = datetime.strptime(dataNascimento,'%Y-%m-%d').date()
        else:
            self.dataNascimento = dataNascimento
        self.email = email
        self.senha = senha

    def __str__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, dataNascimento={self.dataNascimento}, email={self.email}, senha={self.senha})"

    def __eq__(self, other):
        if isinstance(other, Usuario):
            return self.id == other.id and self.email == other.email
        return False

    def __hash__(self):
        return hash((self.id, self.email))

    def __lt__(self, other):
        return self.nome < other.nome

    def __gt__(self, other):
        return self.nome > other.nome

class Administradores:
    def __init__(self, id, idUsuario):
        self.id = id
        self.idUsuario = idUsuario

    def __str__(self):
        return f"Administradores(id={self.id}, idUsuario={self.idUsuario})"

    def __eq__(self, other):
        if isinstance(other, Administradores):
            return self.id == other.id and self.idUsuario == other.idUsuario
        return False

    def __hash__(self):
        return hash((self.id, self.idUsuario))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

class Quadro:
    def __init__(self, id, nome, descricao, dono, publico):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dono = dono
        self.publico = publico

    def __str__(self):
        return f"Quadro(id={self.id}, nome={self.nome}, descricao={self.descricao}, dono={self.dono}, publico={self.publico})"

    def __eq__(self, other):
        if isinstance(other, Quadro):
            return self.id == other.id and self.nome == other.nome
        return False

    def __hash__(self):
        return hash((self.id, self.nome))

    def __lt__(self, other):
        return self.nome < other.nome

    def __gt__(self, other):
        return self.nome > other.nome

class MembrosQuadro:
    def __init__(self, id, idQuadro, idUsuario, aprovado):
        self.id = id
        self.idQuadro = idQuadro
        self.idUsuario = idUsuario
        self.aprovado = aprovado

    def __str__(self):
        return f"MembrosQuadro(id={self.id}, idQuadro={self.idQuadro}, idUsuario={self.idUsuario}, aprovado={self.aprovado})"

    def __eq__(self, other):
        if isinstance(other, MembrosQuadro):
            return self.id == other.id and self.idQuadro == other.idQuadro and self.idUsuario == other.idUsuario
        return False

    def __hash__(self):
        return hash((self.id, self.idQuadro, self.idUsuario))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

class Mensagem:
    def __init__(self, id: int, idQuadro: int, idUsuario: int , nomeUsuario: str, dataHora: datetime, titulo: str, texto: str, anexo: str, expiraEm: datetime, icone: str):
        self.id = id
        self.idQuadro = idQuadro
        self.idUsuario = idUsuario
        self.nomeUsuario = nomeUsuario
        if type(dataHora) == str:
            self.dataHora = datetime.strptime(dataHora,'%Y-%m-%d %H:%M:%S')
        else:
            self.dataHora = dataHora
        self.texto = texto
        self.anexo = anexo
        self.icone = icone
        self.titulo = titulo
        if expiraEm != None:
            if type(expiraEm) == str:
                self.expiraEm = datetime.strptime(expiraEm,'%Y-%m-%d %H:%M:%S')
        else:
            self.expiraEm = expiraEm

    def __str__(self):
        return f"Mensagem(id={self.id}, idQuadro={self.idQuadro}, idUsuario={self.idUsuario}, dataHora={self.dataHora}, texto={self.texto}, anexo={self.anexo}, icone={self.icone})"

    def __eq__(self, other):
        if isinstance(other, Mensagem):
            return self.id == other.id and self.idQuadro == other.idQuadro and self.idUsuario == other.idUsuario
        return False

    def __hash__(self):
        return hash((self.id, self.idQuadro, self.idUsuario))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

class Reacao:
    def __init__(self, id: int, dataHora: datetime, idMensagem: int, idUsuario: int, tipo: str):
        self.id = id
        if type(dataHora) == str:
            self.dataHora = datetime.strptime(dataHora,'%Y-%m-%d %H:%M:%S')
        else:
            self.dataHora = dataHora
        self.idMensagem = idMensagem
        self.idUsuario = idUsuario
        self.tipo = tipo

    def __str__(self):
        return f"Reacoes(id={self.id}, dataHora={self.dataHora}, idMensagem={self.idMensagem}, idUsuario={self.idUsuario}, tipo={self.tipo})"

    def __eq__(self, other):
        if isinstance(other, Reacao):
            return self.id == other.id and self.idMensagem == other.idMensagem and self.idUsuario == other.idUsuario
        return False

    def __hash__(self):
        return hash((self.id, self.idMensagem, self.idUsuario))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

class QuadroUltimaMensagem:
    def __init__(self, id: int, nome: str, descricao: str, dono: int, publico: bool , dataHora: datetime, icone: str, titulo: str):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dono = dono
        self.publico = publico
        if type(dataHora) == str:
            self.dataHora = datetime.strptime(dataHora, '%Y-%m-%d %H:%M:%S')
        else:
            self.dataHora = dataHora
        self.icone = icone
        self.titulo = titulo

class ReacaoAutor:
    def __init__(self, reacao: Reacao, nomeAutor: str):
        self.reacao = reacao
        self.nomeAutor = nomeAutor

class MensagemComReacoes:
    def __init__(self, mensagem: Mensagem, reacoes: [ReacaoAutor]):
        self.mensagem = mensagem
        self.reacoes = reacoes

class PerfilUsuarioQuadro:
    def __init__(self, nome: str, eh_administrador: bool, eh_dono_do_quadro: bool, eh_membro_do_quadro: bool):
        self.nome = nome
        self.eh_administrador = eh_administrador
        self.eh_dono_do_quadro = eh_dono_do_quadro
        self.eh_membro_do_quadro = eh_membro_do_quadro




