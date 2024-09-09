class Usuario:
    def __init__(self, id, nome, dataNascimento, email, senha):
        self.id = id
        self.nome = nome
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
    def __init__(self, id, idQuadro, idUsuario, dataHora, titulo, texto, anexo, icone, expiraEm):
        self.id = id
        self.idQuadro = idQuadro
        self.idUsuario = idUsuario
        self.dataHora = dataHora
        self.texto = texto
        self.anexo = anexo
        self.icone = icone
        self.titulo = titulo
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

class Reacoes:
    def __init__(self, id, dataHora, idMensagem, idUsuario, tipo):
        self.id = id
        self.dataHora = dataHora
        self.idMensagem = idMensagem
        self.idUsuario = idUsuario
        self.tipo = tipo

    def __str__(self):
        return f"Reacoes(id={self.id}, dataHora={self.dataHora}, idMensagem={self.idMensagem}, idUsuario={self.idUsuario}, tipo={self.tipo})"

    def __eq__(self, other):
        if isinstance(other, Reacoes):
            return self.id == other.id and self.idMensagem == other.idMensagem and self.idUsuario == other.idUsuario
        return False

    def __hash__(self):
        return hash((self.id, self.idMensagem, self.idUsuario))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

class QuadroUltimaMensagem:
    def __init__(self, id, nome, descricao, dono, publico, dataHora, icone, titulo):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.dono = dono
        self.publico = publico
        self.dataHora = dataHora
        self.icone = icone
        self.titulo = titulo
