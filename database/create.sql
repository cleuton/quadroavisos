-- Deleta tudo

-- Drop indices if they exist
DROP INDEX IF EXISTS idx_usuario_nome;
DROP INDEX IF EXISTS idx_usuario_email;
DROP INDEX IF EXISTS idx_administradores_idUsuario;
DROP INDEX IF EXISTS idx_quadro_nome;
DROP INDEX IF EXISTS idx_quadro_dono;
DROP INDEX IF EXISTS idx_membrosQuadro_idQuadro;
DROP INDEX IF EXISTS idx_membrosQuadro_idUsuario;
DROP INDEX IF EXISTS idx_mensagem_idQuadro;
DROP INDEX IF EXISTS idx_mensagem_idUsuario;
DROP INDEX IF EXISTS idx_reacoes_idMensagem;
DROP INDEX IF EXISTS idx_reacoes_idUsuario;

-- Drop tables if they exist
DROP TABLE IF EXISTS reacoes;
DROP TABLE IF EXISTS mensagem;
DROP TABLE IF EXISTS membrosQuadro;
DROP TABLE IF EXISTS quadro;
DROP TABLE IF EXISTS administradores;
DROP TABLE IF EXISTS usuario;


-- Create table usuario

DO $$ BEGIN
    RAISE NOTICE 'Creating table usuario';
END $$;

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
    texto TEXT NOT NULL,
    anexo VARCHAR(255),
    icone VARCHAR(255)
);
CREATE INDEX idx_mensagem_idQuadro ON mensagem(idQuadro);
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
('Carlos Pereira', '1978-09-23', 'carlos@example.com', 'senha789');

-- Insert fake data into administradores
INSERT INTO administradores (idUsuario) VALUES
(1),
(2);

-- Insert fake data into quadro
INSERT INTO quadro (nome, descricao, dono, publico) VALUES
('Quadro de Anúncios', 'Quadro para anúncios gerais', 1, TRUE),
('Quadro de Projetos', 'Quadro para discussão de projetos', 2, FALSE);

-- Insert fake data into membrosQuadro
INSERT INTO membrosQuadro (idQuadro, idUsuario, aprovado) VALUES
(1, 1, TRUE),
(1, 2, TRUE),
(2, 3, FALSE);

-- Insert fake data into mensagem
INSERT INTO mensagem (idQuadro, idUsuario, dataHora, texto, anexo, icone) VALUES
(1, 1, '2023-01-01 10:00:00', 'Bem-vindos ao quadro de anúncios!', NULL, NULL),
(1, 2, '2023-01-02 11:00:00', 'Novo evento na próxima semana.', NULL, NULL),
(2, 2, '2023-01-03 12:00:00', 'Discussão sobre o novo projeto.', NULL, NULL);

-- Insert fake data into reacoes
INSERT INTO reacoes (dataHora, idMensagem, idUsuario, tipo) VALUES
('2023-01-01 10:05:00', 1, 2, 'curtir'),
('2023-01-02 11:05:00', 2, 1, 'curtir'),
('2023-01-03 12:05:00', 3, 3, 'curtir');