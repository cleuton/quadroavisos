CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    dataNascimento DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL
);
CREATE INDEX idx_usuario_nome ON usuario(nome);
CREATE INDEX idx_usuario_email ON usuario(email);

-- Create table administradores
CREATE TABLE administradores (
    id SERIAL PRIMARY KEY,
    idUsuario INT NOT NULL REFERENCES usuario(id)
);
CREATE INDEX idx_administradores_idUsuario ON administradores(idUsuario);

-- Create table quadro
CREATE TABLE quadro (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    dono INT NOT NULL REFERENCES usuario(id),
    publico BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_quadro_nome ON quadro(nome);
CREATE INDEX idx_quadro_dono ON quadro(dono);

-- Create table membrosQuadro
CREATE TABLE membrosQuadro (
    id SERIAL PRIMARY KEY,
    idQuadro INT NOT NULL REFERENCES quadro(id),
    idUsuario INT NOT NULL REFERENCES usuario(id),
    aprovado BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX idx_membrosQuadro_idQuadro ON membrosQuadro(idQuadro);
CREATE INDEX idx_membrosQuadro_idUsuario ON membrosQuadro(idUsuario);

-- Create table mensagem
CREATE TABLE mensagem (
    id SERIAL PRIMARY KEY,
    idQuadro INT NOT NULL REFERENCES quadro(id),
    idUsuario INT NOT NULL REFERENCES usuario(id),
    dataHora TIMESTAMP NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    texto TEXT NOT NULL,
    anexo VARCHAR(255),
    expiraEm TIMESTAMP,
    icone VARCHAR(255)
);
CREATE INDEX idx_mensagem_dataHora ON mensagem(dataHora DESC);
CREATE INDEX idx_mensagem_idQuadro ON mensagem(idQuadro);
CREATE INDEX idx_mensagem_titulo ON mensagem(titulo);
CREATE INDEX idx_mensagem_idUsuario ON mensagem(idUsuario);

-- Create table reacoes
CREATE TABLE reacoes (
    id SERIAL PRIMARY KEY,
    dataHora TIMESTAMP NOT NULL,
    idMensagem INT NOT NULL REFERENCES mensagem(id),
    idUsuario INT NOT NULL REFERENCES usuario(id),
    tipo VARCHAR(255) NOT NULL
);
CREATE INDEX idx_reacoes_idMensagem ON reacoes(idMensagem);
CREATE INDEX idx_reacoes_idUsuario ON reacoes(idUsuario);

-- Inserir dados iniciais

-- Insert fake data into usuario
INSERT INTO usuario (nome, dataNascimento, email, senha) VALUES
('Alice Silva', '1990-01-01', 'alice@example.com', 'senha123'),
('Bob Santos', '1985-05-15', 'bob@example.com', 'senha456'),
('Carlos Pereira', '1978-09-23', 'carlos@example.com', 'senha789'),
('Delmiro Admin', '1979-10-20', 'delmiro@example.com', 'senha989'),
('Enésio não Aprovado', '1982-01-10', 'enesio@example.com', 'senha001');

-- Insert fake data into administradores
-- Só o usuário Delmiro Admin é administrador
INSERT INTO administradores (idUsuario) VALUES (4);

-- Insert fake data into quadro
-- Quadro de Projetos é privado, mas o dono é Bob Santos que também tem um segundo quadro
-- Alice é dona do quadro público e do quadro 4
INSERT INTO quadro (nome, descricao, dono, publico) VALUES
('Quadro de Anúncios', 'Quadro para anúncios gerais', 1, TRUE),
('Quadro de Projetos', 'Quadro para discussão de projetos', 2, FALSE),
('Outro quadro do Bob', 'Quadro para discussão de projetos 2 do Bob', 2, FALSE),
('Quadro de Projetos da Alice', 'Quadro para discussão de projetos da Alice', 1, FALSE);

-- Insert fake data into membrosQuadro
-- Os quadros públicos não precisam ter membros
-- Alice é membro do quadro 2 e carlos do quadro 3
-- Enésio pediu para ser membro do quadro 3, mas Bob, o dono, não aprovou ainda
-- ATENCAO: Mesmo sendo dono de um quadro, o usuário tem que constar como membro
INSERT INTO membrosQuadro (idQuadro, idUsuario, aprovado) VALUES
(2, 1, TRUE),
(2, 2, TRUE),
(3, 3, TRUE),
(3, 2, TRUE),
(3, 5, FALSE),
(4, 1, TRUE);

-- Insert fake data into mensagem
INSERT INTO mensagem (idQuadro, idUsuario, dataHora, titulo, texto, anexo, icone) VALUES
(1, 1, '2024-09-01 10:00:00', 'Mensagem de boas vindas', 'Bem-vindos ao quadro de anúncios!', 'diagrama1.png', 'normal.png'),
(1, 2, '2024-09-02 11:00:00', 'Novo evento', 'Novo evento na próxima semana.', NULL, 'atencao.png'),
(2, 2, '2024-09-03 12:00:00', 'Novo projeto', 'Discussão sobre o novo projeto.', 'diagrama2.png', 'normal.png'),
(3, 2, '2024-09-05 12:10:00', 'Novo projeto1', 'Discussão sobre o novo projeto 1.', NULL, 'atencao.png'),
(3, 2, '2024-09-06 12:11:00', 'Novo projeto2', 'Discussão sobre o novo projeto 2.', 'diagrama3.png', 'normal.png'),
(3, 2, '2024-09-07 12:12:00', 'Novo projeto3', 'Discussão sobre o novo projeto 3.', NULL, 'atencao.png'),
(4, 1, '2024-09-07 12:12:00', 'Vamos começar o projeto novo', 'Discussão sobre o novo projeto da Alice.', NULL, 'normal.png');


-- Insert fake data into reacoes
INSERT INTO reacoes (dataHora, idMensagem, idUsuario, tipo) VALUES
('2023-01-01 10:05:00', 1, 2, 'curtir.png'),
('2023-01-02 11:05:00', 2, 1, 'curtir.png'),
('2023-01-03 12:05:00', 3, 1, 'olhos.png'),
('2023-01-03 12:05:00', 6, 3, 'curioso.png');