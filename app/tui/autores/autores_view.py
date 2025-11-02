from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Horizontal, Vertical
from textual import on

from tui.base_view import BaseScreen
from tui.dialogs import ConfirmDialog, InputDialog, EditDialog
from services.autores_service import AutorService


class AutoresScreen(BaseScreen):
    """Tela CRUD de autores com layout consistente e estilo padronizado."""

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

    #tabela_autores {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }
    """

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciamento de Autores", id="titulo"),
            Horizontal(
                Button("Cadastrar", id="btn_cadastrar"),
                Button("Editar", id="btn_editar"),
                Button("Excluir", id="btn_excluir"),
                Button("Voltar", id="btn_voltar"),
                id="botoes",
            ),
            DataTable(id="tabela_autores"),
        )
        yield Footer()

    def on_mount(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        tabela.add_columns("ID", "Nome")
        tabela.cursor_type = "row"
        self.listar_autores()
        self._update_actions()

    def _update_actions(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        btn_excluir = self.query_one("#btn_excluir", Button)
        btn_editar = self.query_one("#btn_editar", Button)
        estado_vazio = tabela.row_count == 0
        btn_excluir.disabled = estado_vazio
        btn_editar.disabled = estado_vazio

    # ---------------------------------------------------------
    # OPERAÇÕES CRUD
    # ---------------------------------------------------------

    def listar_autores(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        tabela.clear()
        for autor in AutorService.listar():
            tabela.add_row(str(autor.id), autor.nome)
        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()
        self._update_actions()

    @on(Button.Pressed, "#btn_cadastrar")
    def abrir_cadastro(self):
        self.app.push_screen(InputDialog("Cadastrar novo autor", "Nome do autor...", self.cadastrar_autor))

    def cadastrar_autor(self, nome: str):
        msg = AutorService.cadastrar(nome)
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_autores()

    @on(Button.Pressed, "#btn_editar")
    def abrir_edicao(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há autores para editar.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um autor na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return
        autor_id, nome_atual = int(row[0]), row[1]
        self.app.push_screen(EditDialog(autor_id, nome_atual, self.editar_autor))

    def editar_autor(self, autor_id: int, novo_nome: str):
        msg = AutorService.editar(autor_id, novo_nome)
        self.app.notify(msg)
        self.listar_autores()

    @on(Button.Pressed, "#btn_excluir")
    def abrir_exclusao(self):
        tabela = self.query_one("#tabela_autores", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há autores para excluir.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um autor na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return
        autor_id, nome = int(row[0]), row[1]
        self.app.push_screen(ConfirmDialog(f"Deseja excluir '{nome}'?", lambda: self.excluir_autor(autor_id)))

    def excluir_autor(self, autor_id: int):
        msg = AutorService.excluir(autor_id)
        self.app.notify(msg)
        self.listar_autores()

    @on(Button.Pressed, "#btn_voltar")
    def voltar(self):
        self.app.pop_screen()
