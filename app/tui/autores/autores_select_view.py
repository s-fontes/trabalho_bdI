from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Vertical, Horizontal
from textual import on

from tui.base_view import BaseScreen
from services.autores_service import AutorService


class AutoresSelectScreen(BaseScreen):
    CSS = BaseScreen.CSS + """
    #titulo {
        text-align: center;
        color: white;
        padding: 1;
    }

    #tabela_autores {
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

    #dica {
        color: #aaaaaa;
        text-align: center;
        padding: 0 1;
    }
    """

    def __init__(self, on_select, autores_selecionados: set[int] | None = None):
        super().__init__()
        self.on_select = on_select
        self.autores = []
        self.autores_selecionados = set(autores_selecionados or [])

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciar autores do livro", id="titulo"),
            Static("Dica: clique numa linha para alternar seleção.", id="dica"),
            DataTable(id="tabela_autores"),
            Horizontal(
                Button("Confirmar", id="confirmar", variant="success"),
                Button("Cancelar", id="cancelar", variant="error"),
                id="botoes",
            ),
        )
        yield Footer()

    def on_mount(self):
        self.autores = AutorService.listar()
        tabela = self.query_one("#tabela_autores", DataTable)
        tabela.add_columns("ID", "Nome", "Selecionado")
        tabela.cursor_type = "row"
        self._render_table()

    def _render_table(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        tabela.clear()
        for autor in self.autores:
            marcado = "✅" if autor.id in self.autores_selecionados else ""
            tabela.add_row(str(autor.id), autor.nome, marcado)
        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()

    @on(DataTable.RowSelected, "#tabela_autores")
    def alternar_por_click(self, event: DataTable.RowSelected):
        tabela = self.query_one("#tabela_autores", DataTable)
        cursor_row = tabela.cursor_row  # Compatível com versões novas do Textual
        if cursor_row is None:
            return

        row = tabela.get_row_at(cursor_row)
        if not row:
            return

        autor_id = int(row[0])
        if autor_id in self.autores_selecionados:
            self.autores_selecionados.remove(autor_id)
            tabela.update_cell_at((cursor_row, 2), "")
        else:
            self.autores_selecionados.add(autor_id)
            tabela.update_cell_at((cursor_row, 2), "✅")

    @on(Button.Pressed, "#confirmar")
    def confirmar(self):
        autores_map = {a.id: a.nome for a in self.autores}
        selecionados = [(aid, autores_map[aid]) for aid in self.autores_selecionados if aid in autores_map]
        self.app.pop_screen()
        self.on_select(selecionados)

    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        self.app.pop_screen()
