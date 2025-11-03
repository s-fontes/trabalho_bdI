from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Vertical, Horizontal
from textual import on

from tui.base_view import BaseScreen
from services.livros_service import LivroService


class LivroSelectScreen(BaseScreen):
    CSS = BaseScreen.CSS + """
    #titulo {
        text-align: center;
        color: white;
        padding: 1;
    }

    #tabela_livros {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }

    #botoes {
        align: center middle;
        padding: 1;
    }

    #botoes Button {
        margin: 0 1;
        width: 18;
    }
    """

    def __init__(self, on_select):
        super().__init__()
        self.on_select = on_select

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Selecione o livro para o exemplar", id="titulo"),
            DataTable(id="tabela_livros"),
            Horizontal(
                Button("Confirmar", id="confirmar", variant="success"),
                Button("Cancelar", id="cancelar", variant="error"),
                id="botoes",
            ),
        )
        yield Footer()

    def on_mount(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        tabela.add_columns("ISBN", "Título", "Editora", "Ano")
        tabela.cursor_type = "row"

        livros = LivroService.listar()
        for livro in livros:
            tabela.add_row(livro.isbn, livro.titulo, livro.editora, str(livro.ano_publicacao))

        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()

    @on(Button.Pressed, "#confirmar")
    def confirmar(self):
        tabela = self.query_one("#tabela_livros", DataTable)
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um livro.")
            return

        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida.")
            return

        isbn, titulo = row[0], row[1]
        self.app.pop_screen()
        self.on_select(isbn, titulo)

    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        self.app.pop_screen()
