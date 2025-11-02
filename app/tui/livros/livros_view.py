from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Horizontal, Vertical
from textual import on

from tui.base_view import BaseScreen
from tui.dialogs import ConfirmDialog
from services.livros_service import LivroService
from tui.livros.livro_cadastro_dialog import LivroCadastroDialog


class LivrosScreen(BaseScreen):
    """Tela CRUD de livros, com estilo consistente e integração com o diálogo de cadastro/edição."""

    CSS = BaseScreen.CSS + """
    #titulo {
        text-align: center;
        color: white;
        padding: 1;
    }

    #botoes {
        align: center middle;
        padding: 1;
    }

    #botoes Button {
        margin: 0 1;
        width: 16;
    }

    #tabela_livros {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }
    """

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciamento de Livros", id="titulo"),
            Horizontal(
                Button("Cadastrar", id="btn_cadastrar"),
                Button("Editar", id="btn_editar"),
                Button("Excluir", id="btn_excluir"),
                Button("Voltar", id="btn_voltar"),
                id="botoes",
            ),
            DataTable(id="tabela_livros"),
        )
        yield Footer()

    def on_mount(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        tabela.add_columns("ISBN", "Título", "Editora", "Ano", "Autores")
        tabela.cursor_type = "row"
        self.listar_livros()
        self._update_actions()

    # ---------------------------------------------------------
    # UTILITÁRIOS
    # ---------------------------------------------------------

    def _update_actions(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        btn_excluir = self.query_one("#btn_excluir", Button)
        btn_editar = self.query_one("#btn_editar", Button)
        estado_vazio = tabela.row_count == 0
        btn_excluir.disabled = estado_vazio
        btn_editar.disabled = estado_vazio

    def listar_livros(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        tabela.clear()
        for livro in LivroService.listar():
            autores = ", ".join(a.nome for a in livro.autores) if livro.autores else "(Sem autores)"
            tabela.add_row(livro.isbn, livro.titulo, livro.editora, str(livro.ano_publicacao), autores)
        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()
        self._update_actions()

    # ---------------------------------------------------------
    # AÇÕES DE BOTÕES
    # ---------------------------------------------------------

    @on(Button.Pressed, "#btn_cadastrar")
    def abrir_cadastro(self):
        self.app.push_screen(LivroCadastroDialog(self.cadastrar_livro))

    def cadastrar_livro(self, dados: dict):
        msg = LivroService.cadastrar(
            dados["isbn"],
            dados["titulo"],
            dados["editora"],
            dados["ano"],
            dados["ids_autores"],
        )
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_livros()
            self.app.pop_screen()  # volta para a tela de livros após salvar

    @on(Button.Pressed, "#btn_editar")
    def abrir_edicao(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há livros para editar.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um livro na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return
        isbn, titulo, editora, ano, *_ = row
        dados_existentes = {
            "isbn": isbn,
            "titulo": titulo,
            "editora": editora,
            "ano": int(ano),
        }
        self.app.push_screen(LivroCadastroDialog(lambda d: self.editar_livro(isbn, d), dados_existentes))

    def editar_livro(self, isbn: str, dados: dict):
        msg = LivroService.editar(
            isbn,
            dados["titulo"],
            dados["editora"],
            dados["ano"],
            dados["ids_autores"],
        )
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_livros()
            self.app.pop_screen()  # volta após editar

    @on(Button.Pressed, "#btn_excluir")
    def abrir_exclusao(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há livros para excluir.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um livro na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return
        isbn, titulo = row[0], row[1]
        self.app.push_screen(ConfirmDialog(f"Deseja excluir '{titulo}'?", lambda: self.excluir_livro(isbn)))

    def excluir_livro(self, isbn: str):
        msg = LivroService.excluir(isbn)
        self.app.notify(msg)
        self.listar_livros()

    @on(Button.Pressed, "#btn_voltar")
    def voltar(self):
        self.app.pop_screen()
