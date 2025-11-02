CREATE SCHEMA IF NOT EXISTS biblioteca;

CREATE TABLE IF NOT EXISTS biblioteca.autores (id SERIAL PRIMARY KEY, nome VARCHAR(100) NOT NULL);

CREATE TABLE IF NOT EXISTS biblioteca.livros (
    isbn VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    editora VARCHAR(100) NOT NULL,
    ano_publicacao INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca.livros_autores (
    id SERIAL PRIMARY KEY,
    livro_isbn VARCHAR(20) NOT NULL,
    autor_id INTEGER NOT NULL,
    CONSTRAINT fk_livro FOREIGN KEY (livro_isbn) REFERENCES biblioteca.livros (isbn) ON DELETE CASCADE,
    CONSTRAINT fk_autor FOREIGN KEY (autor_id) REFERENCES biblioteca.autores (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biblioteca.usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    tipo VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS biblioteca.alunos (
    id INTEGER PRIMARY KEY,
    curso VARCHAR(100) NOT NULL,
    CONSTRAINT fk_aluno_usuario FOREIGN KEY (id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biblioteca.professores (
    id INTEGER PRIMARY KEY,
    departamento VARCHAR(100) NOT NULL,
    CONSTRAINT fk_professor_usuario FOREIGN KEY (id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biblioteca.exemplares (
    id SERIAL PRIMARY KEY,
    livro_isbn VARCHAR(20) NOT NULL,
    codigo_exemplar VARCHAR(20) UNIQUE NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_exemplar_livro FOREIGN KEY (livro_isbn) REFERENCES biblioteca.livros (isbn) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS biblioteca.emprestimos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    exemplar_id INTEGER NOT NULL,
    data_emprestimo DATE NOT NULL DEFAULT CURRENT_DATE,
    data_prevista DATE NOT NULL,
    data_devolucao DATE NULL,
    CONSTRAINT fk_emprestimo_usuario FOREIGN KEY (usuario_id) REFERENCES biblioteca.usuarios (id) ON DELETE CASCADE,
    CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (exemplar_id) REFERENCES biblioteca.exemplares (id) ON DELETE CASCADE,
    CONSTRAINT chk_data_prevista CHECK (data_prevista >= data_emprestimo)
);

CREATE INDEX IF NOT EXISTS idx_livros_titulo ON biblioteca.livros (titulo);

CREATE INDEX IF NOT EXISTS idx_exemplares_disponivel ON biblioteca.exemplares (disponivel);

CREATE INDEX IF NOT EXISTS idx_emprestimos_usuario ON biblioteca.emprestimos (usuario_id);

CREATE INDEX IF NOT EXISTS idx_emprestimos_exemplar ON biblioteca.emprestimos (exemplar_id);