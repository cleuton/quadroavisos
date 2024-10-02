CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    dataNascimento DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    CONSTRAINT unique_usuario UNIQUE (nome, dataNascimento, email)
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

-- Create table reacao
CREATE TABLE reacao (
    id SERIAL PRIMARY KEY,
    dataHora TIMESTAMP NOT NULL,
    idMensagem INT NOT NULL REFERENCES mensagem(id),
    idUsuario INT NOT NULL REFERENCES usuario(id),
    tipo VARCHAR(255) NOT NULL
);
CREATE INDEX idx_reacoes_idMensagem ON reacao(idMensagem);
CREATE INDEX idx_reacoes_idUsuario ON reacao(idUsuario);
CREATE INDEX idx_reacoes_dataHora ON reacao(dataHora desc);

-- Inserir dados iniciais

-- Insert fake data into usuario
INSERT INTO usuario (nome, dataNascimento, email, senha) VALUES
('Alice Silva', '1990-01-01', 'alice@example.com', 'senha123'),
('Bob Santos', '1985-05-15', 'bob@example.com', 'senha456'),
('Carlos Pereira', '1978-09-23', 'carlos@example.com', 'senha789'),
('Delmiro Admin', '1979-10-20', 'delmiro@example.com', 'senha989'),
('Enésio não Aprovado', '1982-01-10', 'enesio@example.com', 'senha001'),
('Fulano de tal', '1982-01-10', 'fulano@example.com', 'senha999');

-- Insert fake data into administradores
-- Só o usuário Delmiro Admin é administrador
INSERT INTO administradores (idUsuario) VALUES (4);

-- Insert fake data into quadro
-- Quadro de Projetos é privado, mas o dono é Bob Santos(2) que também tem um segundo quadro
-- Alice(1) é dona do quadro público e do quadro 4
INSERT INTO quadro (nome, descricao, dono, publico) VALUES
('Quadro de Anúncios', 'Quadro para anúncios gerais', 1, TRUE),
('Quadro de Projetos', 'Quadro para discussão de projetos', 2, FALSE),
('Outro quadro do Bob', 'Quadro para discussão de projetos 2 do Bob', 2, FALSE),
('Quadro de Projetos da Alice', 'Quadro para discussão de projetos da Alice', 1, FALSE),
('Quadro de Projetos 2', 'Quadro para discussão de projetos da 2', 6, FALSE),
('Quadro de Projetos 3', 'Quadro para discussão de projetos da 3', 6, FALSE),
('Quadro de Projetos 4', 'Quadro para discussão de projetos da 4', 6, FALSE),
('Quadro de Projetos 5', 'Quadro para discussão de projetos da 5', 6, FALSE),
('Quadro de Projetos 6', 'Quadro para discussão de projetos da 6', 6, FALSE);

-- Insert fake data into membrosQuadro
-- Os quadros públicos não precisam ter membros
-- donos de quadro:
--      "Quadro de Anúncios"(1) - Alice(1)
--      "Quadro de Projetos"(2) - Bob(2)
--      "Outro quadro do Bob"(3) - Bob(2)
--      "Quadro de Projetos da Alice"(4) - Alice(1)
-- Membros de quadro:
--      "Quadro de Anúncios"(1) - todos. É público.
--      "Quadro de Projetos"(2) - Alice(1).
--      "Outro quadro do Bob"(3) - Carlos(3), Enésio(5)-Não aprovado!!!!
--      "Quadro de Projetos da Alice"(4) - Bob(2).
-- Donos não devem aparecer como membros do quadro
INSERT INTO membrosQuadro (idQuadro, idUsuario, aprovado) VALUES
(2, 1, TRUE),
(3, 3, TRUE),
(3, 2, TRUE),
(3, 5, FALSE),
(4, 2, TRUE),
(4, 6, TRUE);


-- Insert fake data into mensagem
INSERT INTO mensagem (idQuadro, idUsuario, dataHora, titulo, texto, anexo, icone) VALUES
(1, 1, '2024-09-01 10:00:00', 'Mensagem de boas vindas', 'Bem-vindos ao quadro de anúncios!', 'diagrama1.png', 'normal.png'),
(1, 2, '2024-09-02 11:00:00', 'Novo evento', 'Novo evento na próxima semana.', NULL, 'atencao.png'),
(2, 2, '2024-09-03 12:00:00', 'Novo projeto', 'Discussão sobre o novo projeto.', 'diagrama2.png', 'normal.png'),
(3, 2, '2024-09-05 12:10:00', 'Novo projeto1', 'Discussão sobre o novo projeto 1.', NULL, 'atencao.png'),
(3, 2, '2024-09-06 12:11:00', 'Novo projeto2', 'Discussão sobre o novo projeto 2.', 'diagrama3.png', 'normal.png'),
(3, 2, '2024-09-07 12:12:00', 'Novo projeto3', 'Discussão sobre o novo projeto 3.', NULL, 'atencao.png'),
(4, 1, '2024-09-08 12:12:00', 'Vamos começar o projeto novo', 'Discussão sobre o novo projeto da Alice.', NULL, 'normal.png'),
(5, 6, '2024-09-08 10:12:00', 'Vamos começar o projeto novo 1', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 11:12:00', 'Vamos começar o projeto novo 2', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 12:12:00', 'Vamos começar o projeto novo 3', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 13:12:00', 'Vamos começar o projeto novo z', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 14:12:00', 'Vamos começar o projeto novo x', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 15:12:00', 'Vamos começar o projeto novo y', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-08 16:12:00', 'Vamos começar o projeto novo t', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 10:12:00', 'Vamos começar o projeto novo aa', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 12:13:00', 'Vamos começar o projeto novo a1', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 12:14:00', 'Vamos começar o projeto novo b4', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 12:15:00', 'Vamos começar o projeto novo b1', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 13:12:00', 'Vamos começar o projeto novo zz', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-09 13:13:00', 'Vamos começar o projeto novo 45', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-10 14:12:00', 'Vamos começar o projeto novo 987', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-10 15:12:00', 'Vamos começar o projeto novo ffg', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-10 16:12:00', 'Vamos começar o projeto novo xer', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-10 17:12:00', 'Vamos começar o projeto novo 23', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 10:12:00', 'Vamos começar o projeto novo k4', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 11:12:00', 'Vamos começar o projeto novo kj4', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 12:12:00', 'Vamos começar o projeto novo lo9', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 13:12:00', 'Vamos começar o projeto novo velho', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 14:12:00', 'Vamos começar o projeto novo abc', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 15:12:00', 'Vamos começar o projeto novo def', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 16:12:00', 'Vamos começar o projeto novo ghi', 'Discussão sobre o novo projeto.', NULL, 'normal.png'),
(5, 6, '2024-09-11 17:12:00', 'Vamos começar o projeto novo kkk', 'Discussão sobre o novo projeto.', NULL, 'normal.png');




-- Insert fake data into reacoes
INSERT INTO reacao (dataHora, idMensagem, idUsuario, tipo) VALUES
('2023-01-01 10:05:00', 1, 2, 'curtir.png'),
('2023-01-02 11:05:00', 2, 1, 'curtir.png'),
('2023-01-03 12:05:00', 3, 1, 'olhos.png'),
('2023-01-03 12:05:00', 6, 3, 'curioso.png'),
('2023-01-04 12:10:00', 6, 1, 'curtir.png');

-- Muito importante para o upsert de reações:

ALTER TABLE reacao
ADD CONSTRAINT reacao_idMensagem_idUsuario_unique UNIQUE (idMensagem, idUsuario);
