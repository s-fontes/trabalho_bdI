CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA biblioteca;
CREATE TYPE biblioteca.tipo_usuario AS ENUM ('aluno', 'professor');


CREATE TABLE biblioteca.autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE biblioteca.livros (
    isbn VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    editora VARCHAR(100) NOT NULL,
    ano_publicacao INTEGER NOT NULL
);

CREATE TABLE biblioteca.livros_autores (
    livro_isbn VARCHAR(20) NOT NULL,
    autor_id INTEGER NOT NULL,
    CONSTRAINT pk_livros_autores PRIMARY KEY (livro_isbn, autor_id),
    CONSTRAINT fk_livro FOREIGN KEY (livro_isbn) REFERENCES biblioteca.livros (isbn) ON DELETE CASCADE,
    CONSTRAINT fk_autor FOREIGN KEY (autor_id) REFERENCES biblioteca.autores (id) ON DELETE CASCADE
);

CREATE TABLE biblioteca.usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    tipo biblioteca.tipo_usuario NOT NULL
);

CREATE TABLE biblioteca.alunos (
    id INTEGER PRIMARY KEY,
    curso VARCHAR(100) NOT NULL,
    CONSTRAINT fk_aluno_usuario FOREIGN KEY (id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE
);

CREATE TABLE biblioteca.professores (
    id INTEGER PRIMARY KEY,
    departamento VARCHAR(100) NOT NULL,
    CONSTRAINT fk_professor_usuario FOREIGN KEY (id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE
);

CREATE TABLE biblioteca.exemplares (
    id SERIAL PRIMARY KEY,
    livro_isbn VARCHAR(20) NOT NULL,
    codigo_exemplar VARCHAR(20) UNIQUE NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_exemplar_livro FOREIGN KEY (livro_isbn) REFERENCES biblioteca.livros (isbn) ON DELETE CASCADE
);

CREATE TABLE biblioteca.emprestimos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    exemplar_id INTEGER NOT NULL,
    hora_emprestimo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_prevista DATE NOT NULL,
    hora_devolucao TIMESTAMP NULL,
    CONSTRAINT fk_emprestimo_usuario FOREIGN KEY (usuario_id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE,
    CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (exemplar_id) REFERENCES biblioteca.exemplares (id) ON DELETE CASCADE,
    CONSTRAINT chk_data_prevista CHECK (data_prevista >= date(hora_emprestimo))
);

CREATE INDEX idx_livros_titulo ON biblioteca.livros USING gin (titulo gin_trgm_ops);

CREATE INDEX idx_exemplares_disponivel ON biblioteca.exemplares (disponivel)
WHERE disponivel = TRUE;

CREATE INDEX idx_emprestimos_usuario ON biblioteca.emprestimos (usuario_id);

CREATE INDEX idx_emprestimos_exemplar ON biblioteca.emprestimos (exemplar_id);