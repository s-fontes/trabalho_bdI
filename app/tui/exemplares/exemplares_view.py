from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Horizontal, Vertical
from textual import on

from tui.base_view import BaseScreen
from tui.dialogs import ConfirmDialog
from services.exemplares_service import ExemplarService
from tui.exemplares.exemplar_cadastro_dialog import ExemplarCadastroDialog


class ExemplaresScreen(BaseScreen):
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

    #tabela_exemplares {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }
    """

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciamento de Exemplares", id="titulo"),
            Horizontal(
                Button("Cadastrar", id="btn_cadastrar"),
                Button("Editar", id="btn_editar"),
                Button("Excluir", id="btn_excluir"),
                Button("Voltar", id="btn_voltar"),
                id="botoes",
            ),
            DataTable(id="tabela_exemplares"),
        )
        yield Footer()

    def on_mount(self):
        tabela = self.query_one("#tabela_exemplares", DataTable)
        tabela.add_columns("ID", "Livro (Título / ISBN)", "Código", "Disponível")
        tabela.cursor_type = "row"
        self.listar_exemplares()
        self._update_actions()

    def _update_actions(self):
        tabela = self.query_one("#tabela_exemplares", DataTable)
        btn_excluir = self.query_one("#btn_excluir", Button)
        btn_editar = self.query_one("#btn_editar", Button)
        estado_vazio = tabela.row_count == 0
        btn_excluir.disabled = estado_vazio
        btn_editar.disabled = estado_vazio

    def listar_exemplares(self):
        tabela = self.query_one("#tabela_exemplares", DataTable)
        tabela.clear()
        for ex in ExemplarService.listar():
            titulo = ex.livro.titulo if ex.livro else "(Livro não encontrado)"
            disponivel = "✅" if ex.disponivel else "❌"
            tabela.add_row(str(ex.id), f"{titulo} ({ex.livro_isbn})", ex.codigo_exemplar, disponivel)
        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()
        self._update_actions()

    @on(Button.Pressed, "#btn_cadastrar")
    def abrir_cadastro(self):
        self.app.push_screen(ExemplarCadastroDialog(self.cadastrar_exemplar))

    def cadastrar_exemplar(self, dados: dict):
        msg = ExemplarService.cadastrar(
            dados["livro_isbn"],
            dados.get("codigo_exemplar"),
        )
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_exemplares()

    @on(Button.Pressed, "#btn_editar")
    def abrir_edicao(self):
        tabela = self.query_one("#tabela_exemplares", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há exemplares para editar.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um exemplar na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return

        exemplar_id = int(row[0])
        dados_existentes = {
            "livro_isbn": row[1].split("(")[-1].rstrip(")"),
            "codigo_exemplar": row[2],
        }

        self.app.push_screen(
            ExemplarCadastroDialog(
                lambda dados: self.editar_exemplar(exemplar_id, dados),
                dados_existentes=dados_existentes,
            )
        )

    def editar_exemplar(self, exemplar_id: int, dados: dict):
        msg = ExemplarService.editar(
            exemplar_id,
            dados["livro_isbn"],
            dados["codigo_exemplar"],
            True,
        )
        self.app.notify(msg)
        self.listar_exemplares()

    @on(Button.Pressed, "#btn_excluir")
    def abrir_exclusao(self):
        tabela = self.query_one("#tabela_exemplares", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há exemplares para excluir.")
            return
        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um exemplar na tabela.")
            return
        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return

        exemplar_id = int(row[0])
        codigo = row[2]
        self.app.push_screen(
            ConfirmDialog(
                f"Deseja excluir o exemplar '{codigo}'?",
                lambda: self.excluir_exemplar(exemplar_id),
            )
        )

    def excluir_exemplar(self, exemplar_id: int):
        msg = ExemplarService.excluir(exemplar_id)
        self.app.notify(msg)
        self.listar_exemplares()

    @on(Button.Pressed, "#btn_voltar")
    def voltar(self):
        self.app.pop_screen()
