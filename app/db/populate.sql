TRUNCATE TABLE biblioteca.emprestimos,
biblioteca.exemplares,
biblioteca.livros_autores,
biblioteca.alunos,
biblioteca.professores,
biblioteca.usuarios,
biblioteca.livros,
biblioteca.autores RESTART IDENTITY CASCADE;

INSERT INTO
    biblioteca.autores (nome)
VALUES
    ('Machado de Assis'),
    ('Clarice Lispector'),
    ('Jorge Amado'),
    ('José Saramago'),
    ('George Orwell'),
    ('J. K. Rowling'),
    ('Fernando Pessoa'),
    ('Graciliano Ramos'),
    ('Lygia Fagundes Telles'),
    ('Erico Verissimo');

INSERT INTO
    biblioteca.livros (isbn, titulo, editora, ano_publicacao)
VALUES
    (
        '9788533615540',
        'Dom Casmurro',
        'Editora Globo',
        1899
    ),
    (
        '9788533615541',
        'Memórias Póstumas de Brás Cubas',
        'Editora Globo',
        1881
    ),
    (
        '9788532520753',
        'A Hora da Estrela',
        'Rocco',
        1977
    ),
    (
        '9788532520754',
        'Perto do Coração Selvagem',
        'Rocco',
        1943
    ),
    (
        '9788522006351',
        'Capitães da Areia',
        'Companhia das Letras',
        1937
    ),
    (
        '9788522006352',
        'Gabriela, Cravo e Canela',
        'Companhia das Letras',
        1958
    ),
    (
        '9788535926873',
        'Ensaio sobre a Cegueira',
        'Companhia das Letras',
        1995
    ),
    (
        '9788535926874',
        'O Evangelho Segundo Jesus Cristo',
        'Companhia das Letras',
        1991
    ),
    ('9780451524935', '1984', 'Signet Classics', 1949),
    (
        '9780451524936',
        'A Revolução dos Bichos',
        'Signet Classics',
        1945
    ),
    (
        '9788532530806',
        'Harry Potter e a Pedra Filosofal',
        'Rocco',
        1997
    ),
    (
        '9788532530807',
        'Harry Potter e a Câmara Secreta',
        'Rocco',
        1998
    ),
    (
        '9788503012925',
        'Mensagem',
        'Publicações Europa-América',
        1934
    ),
    (
        '9788503012926',
        'Livro do Desassossego',
        'Companhia das Letras',
        1982
    ),
    ('9788503012927', 'Vidas Secas', 'Record', 1938),
    ('9788503012928', 'São Bernardo', 'Record', 1934),
    (
        '9788503012929',
        'Antes do Baile Verde',
        'Companhia das Letras',
        1970
    ),
    (
        '9788503012930',
        'O Tempo e o Vento',
        'Globo',
        1949
    ),
    (
        '9788503012931',
        'Incidente em Antares',
        'Globo',
        1971
    ),
    (
        '9788503012932',
        'Ficções do Interlúdio',
        'Companhia das Letras',
        1929
    );

INSERT INTO
    biblioteca.livros_autores (livro_isbn, autor_id)
VALUES
    ('9788533615540', 1),
    ('9788533615541', 1),
    ('9788532520753', 2),
    ('9788532520754', 2),
    ('9788522006351', 3),
    ('9788522006352', 3),
    ('9788535926873', 4),
    ('9788535926874', 4),
    ('9780451524935', 5),
    ('9780451524936', 5),
    ('9788532530806', 6),
    ('9788532530807', 6),
    ('9788503012925', 7),
    ('9788503012926', 7),
    ('9788503012927', 8),
    ('9788503012928', 8),
    ('9788503012929', 9),
    ('9788503012930', 10),
    ('9788503012931', 10),
    ('9788503012932', 7),
    ('9788535926873', 7),
    ('9788522006352', 9),
    ('9788503012926', 9);

INSERT INTO
    biblioteca.usuarios (nome, email, cpf, tipo)
VALUES
    (
        'Ana Souza',
        'ana.souza@uerj.br',
        '11111111111',
        'aluno'
    ),
    (
        'Bruno Lima',
        'bruno.lima@uerj.br',
        '22222222222',
        'aluno'
    ),
    (
        'Carla Dias',
        'carla.dias@uerj.br',
        '33333333333',
        'aluno'
    ),
    (
        'Daniel Nogueira',
        'daniel.nogueira@uerj.br',
        '44444444444',
        'professor'
    ),
    (
        'Elisa Campos',
        'elisa.campos@uerj.br',
        '55555555555',
        'professor'
    ),
    (
        'Felipe Torres',
        'felipe.torres@uerj.br',
        '66666666666',
        'professor'
    ),
    (
        'Gabriel Pinto',
        'gabriel.pinto@uerj.br',
        '77777777777',
        'aluno'
    ),
    (
        'Helena Rocha',
        'helena.rocha@uerj.br',
        '88888888888',
        'aluno'
    ),
    (
        'Rafael Souza',
        'rafael.souza@uerj.br',
        '00000000000',
        'aluno'
    );

INSERT INTO
    biblioteca.alunos (id, curso)
VALUES
    (1, 'Engenharia de Computação'),
    (2, 'Matemática'),
    (3, 'História'),
    (7, 'Letras'),
    (8, 'Física');

INSERT INTO
    biblioteca.professores (id, departamento)
VALUES
    (4, 'Ciência da Computação'),
    (5, 'Matemática'),
    (6, 'Letras');

INSERT INTO
    biblioteca.exemplares (livro_isbn, codigo_exemplar, disponivel)
VALUES
    ('9788533615540', 'EX0001', TRUE),
    ('9788533615540', 'EX0002', TRUE),
    ('9788533615541', 'EX0003', TRUE),
    ('9788532520753', 'EX0004', TRUE),
    ('9788522006351', 'EX0005', TRUE),
    ('9788535926873', 'EX0006', TRUE),
    ('9780451524935', 'EX0007', TRUE),
    ('9788532530806', 'EX0008', TRUE),
    ('9788503012925', 'EX0009', TRUE),
    ('9788503012927', 'EX0010', TRUE),
    ('9788503012930', 'EX0011', TRUE),
    ('9788532520754', 'EX0012', TRUE),
    ('9788532530807', 'EX0013', TRUE),
    ('9788522006352', 'EX0014', TRUE),
    ('9788503012932', 'EX0015', TRUE),
    ('9788503012932', 'EX0016', TRUE),
    ('9788503012932', 'EX0017', TRUE);

INSERT INTO
    biblioteca.emprestimos (
        usuario_id,
        exemplar_id,
        data_emprestimo,
        data_prevista,
        data_devolucao
    )
VALUES
    (
        1,
        1,
        CURRENT_DATE - INTERVAL '12 days',
        CURRENT_DATE - INTERVAL '5 days',
        CURRENT_DATE - INTERVAL '3 days'
    ),
    (
        2,
        2,
        CURRENT_DATE - INTERVAL '10 days',
        CURRENT_DATE - INTERVAL '3 days',
        CURRENT_DATE - INTERVAL '1 days'
    ),
    (
        3,
        3,
        CURRENT_DATE - INTERVAL '5 days',
        CURRENT_DATE + INTERVAL '2 days',
        NULL
    ),
    (
        4,
        4,
        CURRENT_DATE - INTERVAL '8 days',
        CURRENT_DATE + INTERVAL '7 days',
        NULL
    ),
    (
        5,
        5,
        CURRENT_DATE - INTERVAL '15 days',
        CURRENT_DATE - INTERVAL '1 days',
        NULL
    ),
    (
        6,
        6,
        CURRENT_DATE - INTERVAL '4 days',
        CURRENT_DATE + INTERVAL '10 days',
        NULL
    ),
    (
        7,
        7,
        CURRENT_DATE - INTERVAL '3 days',
        CURRENT_DATE + INTERVAL '4 days',
        NULL
    ),
    (
        8,
        8,
        CURRENT_DATE - INTERVAL '2 days',
        CURRENT_DATE + INTERVAL '5 days',
        NULL
    ),
    (
        1,
        9,
        CURRENT_DATE - INTERVAL '1 days',
        CURRENT_DATE + INTERVAL '6 days',
        NULL
    ),
    (
        2,
        10,
        CURRENT_DATE - INTERVAL '7 days',
        CURRENT_DATE + INTERVAL '8 days',
        NULL
    ),
    (
        3,
        11,
        CURRENT_DATE - INTERVAL '6 days',
        CURRENT_DATE + INTERVAL '9 days',
        NULL
    ),
    (
        4,
        12,
        CURRENT_DATE - INTERVAL '5 days',
        CURRENT_DATE + INTERVAL '10 days',
        NULL
    ),
    (
        5,
        13,
        CURRENT_DATE - INTERVAL '9 days',
        CURRENT_DATE - INTERVAL '2 days',
        CURRENT_DATE - INTERVAL '1 days'
    ),
    (
        6,
        14,
        CURRENT_DATE - INTERVAL '14 days',
        CURRENT_DATE - INTERVAL '4 days',
        NULL
    ),
    (
        7,
        15,
        CURRENT_DATE - INTERVAL '2 days',
        CURRENT_DATE + INTERVAL '10 days',
        NULL
    );

UPDATE biblioteca.exemplares
SET
    disponivel = FALSE
WHERE
    id IN (
        SELECT
            exemplar_id
        FROM
            biblioteca.emprestimos
        WHERE
            data_devolucao IS NULL
    );

COMMIT;