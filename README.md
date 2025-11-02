# 📚 Sistema de Biblioteca Universitária

Projeto da disciplina **Banco de Dados I (UERJ)**.
O sistema permite controlar o empréstimo de livros de uma biblioteca universitária com:

- Interface TUI (modo texto) com Textual
- Integração com banco PostgreSQL
- Registro de histórico de empréstimos
- Lógica de disponibilidade de exemplares
- Scripts SQL de criação e populamento do banco
- Automatização com `Makefile`

---

## 🎯 Objetivo

Gerenciar empréstimos de livros físicos da biblioteca, permitindo que usuários (alunos ou professores) retirem exemplares disponíveis e os devolvam.
Cada exemplar é único e não pode estar emprestado a mais de uma pessoa ao mesmo tempo.

---

## 🧱 Estrutura do Projeto

```
trabalho_bdI/
├── app/                        # Código Python da aplicação
│   ├── core/                   # Logger
│   ├── db/                     # Models SQLAlchemy
│   ├── services/               # Lógica de negócio (empréstimos, usuários, etc.)
│   ├── tui/                    # Interface textual com Textual
│   └── main.py                 # Ponto de entrada
├── schema_biblioteca.sql       # Script de criação do banco
├── populate.sql                # Script de dados de exemplo
├── docker-compose.yml          # Configuração do ambiente Docker
├── requirements.txt            # Dependências Python
├── Makefile                    # Comandos automatizados
└── README.md
```

---

## ⚙️ Como Executar

### 1. Configure o `.env`

Crie um arquivo `.env` com as variáveis de ambiente:

```env
PG_USER=postgres
PG_PASSWORD=postgres
PG_DB=dbI
PG_HOST=localhost
PG_PORT=5432
```

---

### 2. Use os comandos Make

Com o Docker instalado, você pode utilizar os seguintes comandos:

| Comando         | Ação realizada                                  |
|-----------------|-------------------------------------------------|
| `make up`       | Sobe o ambiente Docker (`docker-compose up`)   |
| `make down`     | Para os containers                             |
| `make clean`    | Remove containers e dados persistentes         |
| `make create`   | Executa o script `schema_biblioteca.sql`       |
| `make populate` | Insere dados de exemplo via `populate.sql`     |
| `make run`      | Inicia a interface TUI                         |

---

## ▶️ Executar a Interface TUI

```bash
make run
```

A interface textual será exibida, permitindo gerenciamento de empréstimos, usuários, autores e livros.

---

## 🛠️ Dependências

- Python 3.11+
- SQLAlchemy 2.x
- Textual
- Docker + Docker Compose
- PostgreSQL

Instale as dependências Python com:

```bash
pip install -r requirements.txt
```